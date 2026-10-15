# preparar_detalhe.py — prepara a imagem detalhada de um item (a que aparece
# na tela de "item novo") a partir da imagem crua que saiu do gerador de imagem.
#
# Como rodar (Python 3 + numpy + Pillow):
#
#   python assets/modelagem/itens/preparar_detalhe.py <imagem_crua> <id_do_item> [opções]
#
#   ex.: python assets/modelagem/itens/preparar_detalhe.py ~/Downloads/lanterna.webp lanterna
#
# Opção:
#   --furo X,Y      um vão fechado do desenho (o meio de uma argola, o espaço
#                   entre os cabos do alicate) que ficou com um resto de brilho
#                   do fundo. X,Y é um ponto dentro do vão, em pixels da imagem
#                   crua. Pode repetir: --furo 500,520 --furo 990,350
#   --passo N       o limite de mudança de cor ao escorrer pelo brilho
#                   (padrão 7). Se o fundo comer uma parte escura do objeto,
#                   tente 4 ou 5. Pequeno demais, sobra brilho.
#
# O que sai:
#   assets/sprites/itens/<id_do_item>_detalhe.png   RGBA, fundo transparente, cortada rente
#
# Depois, no recurso do item (dados/itens/<id_do_item>.tres), aponte o campo
# "Imagem detalhe" para o PNG. Item sem esse campo mostra o ícone ampliado.
#
# Por que o fundo precisa sair: o gerador de imagem entrega o objeto sobre um
# fundo, e a tela de item novo desenha o objeto sobre uma luz escura. Um
# retângulo em volta estragaria tudo.
#
# O problema: o fundo quase nunca é de uma cor só. Tem vinheta (escurece nos
# cantos), um brilho atrás do objeto, poeira. E o objeto às vezes tem partes
# quase da cor do fundo (o corpo cinza-escuro do notebook). Por isso o
# trabalho é feito em quatro passos.
#
# 1. Um modelo do fundo (mínimos quadrados). Supomos que a cor do fundo varia
#    devagar pela imagem: cada canal (R, G, B) é um polinômio de grau 4 em x e y,
#
#        fundo(x, y) = soma de c_ij * x^i * y^j,   com i + j <= 4
#
#    São 15 coeficientes por canal, achados por mínimos quadrados
#    (np.linalg.lstsq). Começamos só com uma faixa da borda da imagem, que é
#    fundo com certeza. A cada volta medimos o resíduo |cor - modelo| de todos
#    os pixels e refazemos o ajuste só com os que ficaram perto do modelo.
#    Assim o objeto, que fica longe, não puxa o polinômio (ajuste robusto).
#
# 2. O brilho perto do objeto (convolução normalizada). Um polinômio não
#    acompanha um brilho forte e concentrado. Então medimos o resíduo nos
#    pixels que já sabemos que são fundo e o espalhamos para os vizinhos com
#    uma média ponderada:
#
#        correção = borrar(resíduo * M) / borrar(M)
#
#    onde M vale 1 no fundo conhecido e 0 no resto, e "borrar" é uma média
#    numa janela (três médias em caixa seguidas, que se aproximam de uma
#    gaussiana). Dividir por borrar(M) faz a média considerar só os pixels de
#    fundo. Somamos a correção ao modelo e repetimos três vezes.
#
# 3. Quem é fundo (busca em largura, BFS). Um pixel parece fundo se a cor dele
#    está a menos de T_FUNDO do modelo (distância euclidiana no espaço RGB).
#    Uma BFS parte de todos os pixels da borda e anda pelos vizinhos que
#    parecem fundo. Depois, uma segunda BFS "escorre" pelo brilho: anda para
#    o vizinho se a cor muda pouco de um pixel para o outro (menos de PASSO).
#    O brilho é suave; o contorno preto do desenho é um degrau grande, e ali a
#    busca para. Uma parte do objeto da mesma cor do fundo, mas cercada pelo
#    contorno, não é alcançada e continua opaca.
#
#    Vãos fechados (o meio de uma argola) também não são alcançados pela
#    borda. Os que parecem fundo e são grandes saem sozinhos; os que ficaram
#    com brilho saem com --furo: uma BFS que parte do ponto dado e escorre
#    pelo vão (mesma regra do PASSO) até bater no contorno.
#
# 4. Limpeza. Cada mancha opaca é um componente conexo (de novo por BFS).
#    Fica só o objeto: manchas com menos de 2% do tamanho da maior (poeira,
#    estrelinhas do fundo, ruído do JPEG) somem.
#
# O alfa sai 0 ou 1 (pixel art tem borda dura). A imagem é reduzida no fim,
# e a redução suaviza a borda.
#
# Peça ao gerador de imagem o item SEM sombra no chão: uma sombra de borda
# dura fica grudada no objeto. A imagem do rádio, que tem sombra, foi feita
# com a versão anterior deste script (commit 0399b1a do PR #107), para fundo de uma cor
# só: ela media a distância até a reta do preto à cor do fundo (c ≈ k * f,
# com k = (c · f) / (f · f), um produto escalar), e a sombra caía nessa reta.

import argparse
import os
from collections import deque

import numpy as np
from PIL import Image

PASTA_PROJETO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")

GRAU = 4            # grau do polinômio do fundo
T_FUNDO = 14.0      # distância de cor até o modelo para o pixel parecer fundo
PASSO = 7.0         # mudança de cor máxima entre vizinhos ao escorrer pelo brilho
LIMITE_BRILHO = 3.0 # escorrer só por pixels a menos de 3 * T_FUNDO do modelo
RAIO = 12           # raio da média em caixa da correção (na imagem reduzida 4x)
FURO_MINIMO = 0.002 # vão fechado com mais que 0,2% da imagem sai sozinho
PECA_MINIMA = 0.02  # mancha com menos de 2% da maior é sujeira
MARGEM = 8
LIMITE_LADO = 512


def busca_em_largura(pode_andar, sementes, passo_ok=None):
    """BFS: marca todo pixel alcançável a partir das sementes, andando para os
    4 vizinhos onde pode_andar é verdadeiro (e, se houver, onde passo_ok
    deixa sair do pixel atual para o vizinho)."""
    altura, largura = pode_andar.shape
    alcancado = np.zeros_like(pode_andar)
    fila = deque()
    for y, x in sementes:
        if pode_andar[y, x] and not alcancado[y, x]:
            alcancado[y, x] = True
            fila.append((y, x))
    while fila:
        y, x = fila.popleft()
        for vy, vx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= vy < altura and 0 <= vx < largura and pode_andar[vy, vx] and not alcancado[vy, vx]:
                if passo_ok is None or passo_ok(y, x, vy, vx):
                    alcancado[vy, vx] = True
                    fila.append((vy, vx))
    return alcancado


def bordas(altura, largura):
    return [(y, x) for y in range(altura) for x in (0, largura - 1)] + \
           [(y, x) for x in range(largura) for y in (0, altura - 1)]


def componentes(mascara):
    """Rotula cada mancha conexa da máscara (1, 2, 3...) e conta os pixels."""
    rotulos = np.zeros(mascara.shape, dtype=np.int32)
    tamanhos = [0]
    for y, x in np.argwhere(mascara):
        if rotulos[y, x]:
            continue
        mancha = busca_em_largura(mascara & (rotulos == 0), [(y, x)])
        tamanhos.append(int(mancha.sum()))
        rotulos[mancha] = len(tamanhos) - 1
    return rotulos, np.array(tamanhos)


def termos(xn, yn):
    return np.stack([xn ** i * yn ** j for i in range(GRAU + 1) for j in range(GRAU + 1 - i)], axis=-1)


def ajustar_polinomio(pix, escala=4):
    """Passo 1: polinômio do fundo por mínimos quadrados, refeito só com os
    pixels perto do modelo."""
    altura, largura, _ = pix.shape
    ys, xs = np.mgrid[0:altura:escala, 0:largura:escala]
    amostra = pix[::escala, ::escala]
    a = termos(xs.ravel() / largura * 2 - 1, ys.ravel() / altura * 2 - 1)
    faixa = max(2, ys.shape[0] // 12)
    usar = np.zeros(ys.shape, dtype=bool)
    usar[:faixa] = usar[-faixa:] = True
    usar[:, :faixa] = usar[:, -faixa:] = True
    usar = usar.ravel()
    for _ in range(12):
        coef, *_ = np.linalg.lstsq(a[usar], amostra.reshape(-1, 3)[usar], rcond=None)
        modelo = (a @ coef).reshape(amostra.shape)
        residuo = distancia(amostra, modelo).ravel()
        novo = residuo < max(T_FUNDO, 2.5 * np.median(residuo[usar]))
        if (novo == usar).all():
            break
        usar = novo
    yy, xx = np.mgrid[0:altura, 0:largura]
    return (termos(xx / largura * 2 - 1, yy / altura * 2 - 1) @ coef).reshape(pix.shape)


def media_em_caixa(a, raio):
    """Média numa janela de 2 * raio + 1 em cada eixo, com somas acumuladas."""
    for eixo in (0, 1):
        borda = [(0, 0), (0, 0)]
        borda[eixo] = (raio + 1, raio)
        soma = np.cumsum(np.pad(a, borda, mode="edge"), axis=eixo)
        if eixo == 0:
            a = (soma[2 * raio + 1:] - soma[:-2 * raio - 1]) / (2 * raio + 1)
        else:
            a = (soma[:, 2 * raio + 1:] - soma[:, :-2 * raio - 1]) / (2 * raio + 1)
    return a


def borrar(a, raio):
    for _ in range(3):
        a = media_em_caixa(a, raio)
    return a


def corrigir_brilho(pix, fundo, conhecido, escala=4):
    """Passo 2: convolução normalizada do resíduo medido no fundo conhecido."""
    residuo = (pix - fundo)[::escala, ::escala]
    m = conhecido[::escala, ::escala].astype(np.float64)
    pesos = borrar(m, RAIO)
    correcao = np.stack([borrar(residuo[..., c] * m, RAIO) for c in range(3)], axis=-1)
    correcao /= np.maximum(pesos, 1e-6)[..., None]
    correcao[pesos < 1e-3] = 0
    correcao = np.kron(correcao, np.ones((escala, escala, 1)))[:pix.shape[0], :pix.shape[1]]
    return fundo + correcao


def distancia(c, f):
    return np.sqrt(((c - f) ** 2).sum(axis=-1))


def escorrer(pix, fundo, perto, sementes, passo):
    """Passo 3, segunda BFS: anda pelo brilho suave a partir do fundo conhecido."""
    salto_lado = distancia(pix[:, 1:], pix[:, :-1])
    salto_baixo = distancia(pix[1:], pix[:-1])

    def passo_ok(y, x, vy, vx):
        if vy == y:
            return salto_lado[y, min(x, vx)] < passo
        return salto_baixo[min(y, vy), x] < passo

    return busca_em_largura(perto | fundo, sementes, passo_ok) | fundo


def mascara_do_objeto(pix, furos, passo=PASSO):
    altura, largura, _ = pix.shape
    modelo = ajustar_polinomio(pix)
    for volta in range(4):
        d = distancia(pix, modelo)
        fundo = busca_em_largura(d < T_FUNDO, bordas(altura, largura))
        if volta < 3:
            modelo = corrigir_brilho(pix, modelo, fundo)
    perto = d < LIMITE_BRILHO * T_FUNDO
    fundo = escorrer(pix, fundo, perto, list(map(tuple, np.argwhere(fundo))), passo)
    if furos:
        fundo |= escorrer(pix, np.zeros_like(fundo), np.ones_like(fundo), [(y, x) for x, y in furos], passo)
    rotulos, tamanhos = componentes((d < T_FUNDO) & ~fundo)
    vao = tamanhos >= FURO_MINIMO * altura * largura
    vao[0] = False
    transparente = fundo | vao[rotulos]
    rotulos, tamanhos = componentes(~transparente)
    manter = tamanhos >= PECA_MINIMA * tamanhos.max()
    manter[0] = False
    return manter[rotulos]


def cortar_rente(rgba):
    visivel = rgba[..., 3] > 12
    linhas = np.where(visivel.any(axis=1))[0]
    colunas = np.where(visivel.any(axis=0))[0]
    y0 = max(linhas[0] - MARGEM, 0)
    y1 = min(linhas[-1] + MARGEM + 1, rgba.shape[0])
    x0 = max(colunas[0] - MARGEM, 0)
    x1 = min(colunas[-1] + MARGEM + 1, rgba.shape[1])
    return rgba[y0:y1, x0:x1]


def ponto(texto):
    x, y = texto.split(",")
    return int(x), int(y)


def main():
    parser = argparse.ArgumentParser(description="Prepara a imagem detalhada de um item (fundo transparente, corte rente).")
    parser.add_argument("entrada", help="imagem crua (png, jpg ou webp)")
    parser.add_argument("item", help="id do item, o mesmo de dados/itens/<id>.tres")
    parser.add_argument("--furo", type=ponto, action="append", default=[], metavar="X,Y",
                        help="ponto dentro de um vão fechado que deve ficar transparente")
    parser.add_argument("--passo", type=float, default=PASSO,
                        help="mudança de cor máxima ao escorrer pelo brilho (padrão %(default)s)")
    args = parser.parse_args()

    rgb = np.array(Image.open(args.entrada).convert("RGB"))
    opaco = mascara_do_objeto(rgb.astype(np.float64), args.furo, args.passo)
    rgba = np.zeros(rgb.shape[:2] + (4,), dtype=np.uint8)
    rgba[opaco, :3] = rgb[opaco]
    rgba[opaco, 3] = 255
    imagem = Image.fromarray(cortar_rente(rgba), "RGBA")
    if max(imagem.size) > LIMITE_LADO:
        escala = LIMITE_LADO / max(imagem.size)
        imagem = imagem.resize((round(imagem.width * escala), round(imagem.height * escala)), Image.LANCZOS)
    caminho = os.path.join(PASTA_ITENS, f"{args.item}_detalhe.png")
    imagem.save(caminho, optimize=True)
    print("  salvo:", os.path.relpath(caminho, PASTA_PROJETO), f"({imagem.width}x{imagem.height})")


if __name__ == "__main__":
    main()
