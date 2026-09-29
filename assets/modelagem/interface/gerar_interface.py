# gerar_interface.py — desenha, por código, os ÍCONES DOS ITENS e as peças
# da INTERFACE (inventário e espaços de gadget), no mesmo estilo da
# Biblioteca: mesma paleta, mesmo dithering, mesmo contorno escuro.
#
# Como rodar (Python 3 + numpy, igual ao gerar_biblioteca.py):
#
#   python assets/modelagem/interface/gerar_interface.py
#
# O que sai:
#   assets/sprites/itens/<item>.png                16 x 16 px: ícone do item (inventário)
#   assets/sprites/itens/<item>_chao.png           o item caído no chão, na escala do
#                                                  cenário (1 px ≈ 3,6 cm: um pote tem ~6 px)
#   assets/sprites/interface/espaco.png            20 x 20 px: um espaço vazio da grade
#   assets/sprites/interface/espaco_selecionado.png  o mesmo, com a borda acesa
#   assets/sprites/interface/painel.png            24 x 24 px: fundo das janelas, em
#                                                  "9 fatias" (NinePatchRect no Godot)
#   assets/sprites/interface/papel_<estilo>.png    200 x 156 px: a folha onde se lê um
#                                                  documento (tela de leitura e caderno)
#
# Os papéis não são "9 fatias": cada um é desenhado já no tamanho em que
# aparece, porque as pautas e o quadriculado precisam cair exatamente
# embaixo das linhas de texto. A fonte Tiny5 no tamanho 8 tem 9 px de
# altura e o Godot põe 3 px entre as linhas: uma linha de texto a cada
# 12 px. O texto começa em y = TOPO_TEXTO, então a pauta da linha i fica em
# TOPO_TEXTO + 10 + 12 * i (1 px abaixo das letras que descem, como g e p).
# Se mudar essas medidas aqui, mude também em cenas/interface/tela_documento.tscn.
#
# Este script IMPORTA as funções do gerar_biblioteca.py (paleta, pintar com
# dithering, contorno...), como o gerar_kit.py faz. Assim um ícone novo sai
# automaticamente com as mesmas cores do cenário.
#
# Painel em "9 fatias": a imagem é dividida em 3 x 3 pedaços. Os 4 cantos
# ficam do tamanho original, as 4 bordas esticam só num sentido e o meio
# estica nos dois. Assim uma imagem pequena vira uma janela de qualquer
# tamanho sem deformar a moldura. No Godot, o NinePatchRect faz isso: as
# margens (patch_margin) dizem onde cortar — aqui, 6 px de cada lado.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")
PASTA_INTERFACE = os.path.join(PASTA_PROJETO, "assets", "sprites", "interface")

# Importa o gerar_biblioteca.py como um módulo (sem rodar o main dele).
_spec = importlib.util.spec_from_file_location(
    "gerar_biblioteca",
    os.path.join(PASTA_PROJETO, "assets", "modelagem", "salas", "biblioteca", "gerar_biblioteca.py"))
bib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bib)

Imagem, RAMPAS, CONTORNO, ruido = bib.Imagem, bib.RAMPAS, bib.CONTORNO, bib.ruido

TAMANHO_ICONE = 16
TAMANHO_ESPACO = 20
TAMANHO_PAINEL = 24
MARGEM_PAINEL = 6       # patch_margin do NinePatchRect (mude lá se mudar aqui)


# ---------------------------------------------------------------------------
# Ícones dos itens
# ---------------------------------------------------------------------------


def pote_fungos():
    """A lanterna do Gabriel: um pote de conserva de vidro com fungos
    bioluminescentes dentro (docs/mecanicas/iluminacao_e_fungos.md).
    Vidro escuro e frio, tampa de metal enferrujada, fungos ciano no fundo
    e um reflexo claro de 1 px na lateral, que é o que faz parecer vidro."""
    img = Imagem(TAMANHO_ICONE, TAMANHO_ICONE)
    X, Y = img.X, img.Y
    fino = ruido(img.w, img.h, 2, 2, 7)
    # Corpo do pote: um retângulo de cantos cortados (ombro em cima).
    corpo = img.poligono([(3, 5), (4, 4), (12, 4), (13, 5), (13, 14), (12, 15), (4, 15), (3, 14)])
    # Vidro: escuro, um pouco mais claro na esquerda (a luz vem de lá).
    img.pintar(corpo, "metal", 0.22 + 0.12 * (1 - (X - 3) / 10) + 0.06 * fino)
    # Brilho de dentro: a metade de baixo do vidro fica esverdeada/ciano,
    # iluminada pelos próprios fungos.
    brilho = corpo & (Y >= 9)
    img.pintar(brilho, "fungo", 0.05 + 0.3 * (Y - 9) / 6)
    # Fungos: três chapéus claros no fundo do pote (talo escuro, chapéu
    # claro, um ponto branco em cima: o mesmo desenho dos fungos do cenário).
    for (x, y, r) in ((5, 12, 1.5), (8, 10, 2.0), (11, 12, 1.2)):
        img.pintar(img.ret(x, y + 1, x + 1, 15), "fungo", 0.45)
        img.pintar(img.elipse(x + 0.5, y + 0.5, r + 0.5, r * 0.55 + 0.5), "fungo", 0.85)
        img.cor(img.ret(x, y, x + 1, y + 1), RAMPAS["fungo"][5])
    # Reflexo do vidro: uma linha clara vertical à esquerda.
    img.pintar(img.ret(4, 6, 5, 11), "ceu", 0.55)
    img.cor(img.ret(4, 6, 5, 7), RAMPAS["ceu"][5])
    # Tampa de metal enferrujada (mais larga que a boca do pote).
    tampa = img.ret(4, 1, 12, 4)
    img.pintar(tampa, "ferrugem", 0.35 + 0.25 * (Y == 1) + 0.1 * fino)
    img.pintar(img.ret(4, 3, 12, 4), "ferrugem", 0.2)          # borda de baixo, na sombra
    # Rótulo de papel velho, meio rasgado.
    rotulo = img.ret(6, 6, 11, 9) & ~((X == 10) & (Y == 8))
    img.pintar(rotulo, "papel", 0.45 + 0.2 * fino)
    img.contornar(CONTORNO)
    return img


def pote_fungos_chao():
    """O mesmo pote, caído no chão da sala. No cenário 1 px vale ~3,6 cm
    (o Gabriel tem 49 px), então um pote de conserva de ~25 cm tem 7 px de
    altura. Pouco detalhe: tampa, vidro, brilho ciano embaixo e o reflexo."""
    img = Imagem(9, 10)
    X, Y = img.X, img.Y
    corpo = img.poligono([(1, 3), (2, 2), (7, 2), (8, 3), (8, 8), (7, 9), (2, 9), (1, 8)])
    img.pintar(corpo, "metal", 0.3)
    img.pintar(corpo & (Y >= 5), "fungo", 0.35 + 0.35 * (Y - 5) / 4)
    img.cor(img.ret(4, 6, 5, 7), RAMPAS["fungo"][5])
    img.pintar(img.ret(2, 4, 3, 6), "ceu", 0.6)                 # reflexo do vidro
    img.pintar(img.ret(2, 1, 8, 3), "ferrugem", 0.4 + 0.2 * (Y == 1))   # tampa
    img.contornar(CONTORNO)
    return img


def radio():
    """O rádio portátil que o Valdir usava na ronda (um HT de 2008): corpo
    de plástico preto, antena de borracha à esquerda, tela pequena de LCD
    esverdeado e a grade do alto-falante embaixo. O botão de falar (PTT)
    fica na lateral, em ferrugem."""
    img = Imagem(TAMANHO_ICONE, TAMANHO_ICONE)
    X, Y = img.X, img.Y
    fino = ruido(img.w, img.h, 2, 2, 11)
    # Antena: um bastão grosso de 2 px, mais claro na ponta.
    img.pintar(img.ret(4, 0, 6, 5), "metal", 0.18 + 0.2 * (Y == 0))
    # Corpo: retângulo de cantos cortados, mais claro na esquerda.
    corpo = img.poligono([(4, 5), (5, 4), (12, 4), (13, 5), (13, 15), (12, 16), (5, 16), (4, 15)])
    img.pintar(corpo, "metal", 0.12 + 0.18 * (1 - (X - 4) / 9) + 0.05 * fino)
    # Botão de falar na lateral esquerda.
    img.pintar(img.ret(3, 7, 4, 10), "ferrugem", 0.5)
    # Tela de LCD: verde apagado, com uma linha mais clara (os números).
    tela = img.ret(6, 6, 12, 9)
    img.pintar(tela, "verde", 0.55)
    img.pintar(img.ret(7, 7, 11, 8), "verde", 0.8)
    # Grade do alto-falante: pontos alternados, como furos.
    furos = img.ret(6, 11, 12, 15) & ((X + Y) % 2 == 0)
    img.pintar(furos, "metal", 0.02)
    # Brilho de 1 px na quina de cima do corpo.
    img.pintar(img.ret(5, 5, 7, 6), "metal", 0.7)
    img.contornar(CONTORNO)
    return img


def radio_chao():
    """O mesmo rádio caído no chão, na escala do cenário: um HT tem uns
    20 cm, então ~6 px de corpo mais a antena."""
    img = Imagem(7, 11)
    img.pintar(img.ret(1, 0, 2, 4), "metal", 0.3)
    corpo = img.ret(1, 3, 6, 10)
    img.pintar(corpo, "metal", 0.22)
    img.pintar(img.ret(2, 4, 5, 6), "verde", 0.6)
    img.pintar(img.ret(2, 7, 5, 9) & ((img.X + img.Y) % 2 == 0), "metal", 0.02)
    img.contornar(CONTORNO)
    return img


# Nome do arquivo -> função que desenha. Um item novo entra aqui.
ICONES = {
    "pote_fungos": pote_fungos,
    "pote_fungos_chao": pote_fungos_chao,
    "radio": radio,
    "radio_chao": radio_chao,
}


# ---------------------------------------------------------------------------
# Papéis (tela de leitura de documentos e caderno do Gabriel)
# ---------------------------------------------------------------------------

LARGURA_PAPEL = 200
ALTURA_PAPEL = 156
TOPO_TITULO = 8         # onde começa o título (1 linha)
TOPO_TEXTO = 24         # onde começa o texto
PASSO_LINHA = 12        # 9 px de letra + 3 px de espaço entre linhas
LINHAS_TEXTO = 9        # linhas por página (o resto vai para a próxima)
MARGEM_TEXTO = 14       # x onde começa o texto

# Os papéis são as únicas coisas CLARAS do jogo: precisam ser lidos. Por
# isso têm rampas próprias, mais claras que a rampa "papel" do cenário
# (que é papel de mil anos, quase marrom).
PERGAMINHO = bib.hexa("#4a3419", "#6b4f27", "#8c6d3a", "#a8894f", "#c0a266", "#d2b87e", "#dfca94")
PAPEL_CLARO = bib.hexa("#7d7868", "#9f9985", "#bdb69e", "#d3cbb2", "#e2dbc4", "#ece6d2")
AZUL_PAUTA = bib.hexa("#9aabc4")[0]
VERMELHO_MARGEM = bib.hexa("#c07a70")[0]
CINZA_GRADE = bib.hexa("#c9c6b8")[0]
TINTA_MARROM = bib.hexa("#3a2210")[0]


def pautas():
    """Os y das pautas: uma embaixo do título e uma embaixo de cada linha
    de texto."""
    return [TOPO_TITULO + 10] + [TOPO_TEXTO + 10 + PASSO_LINHA * i for i in range(LINHAS_TEXTO)]


def borda_rasgada(img, forca, semente):
    """Máscara da folha com as bordas irregulares. Para cada lado, um ruído
    diz quantos pixels "comer" naquela altura (ou coluna): de 0 a 'forca'.
    Borda de papel velho nunca é reta."""
    w, h = img.w, img.h
    r = ruido(w, h, 5, 5, semente)
    esq = np.floor(forca * r[:, 0])[:, None]
    dir_ = np.floor(forca * r[:, w // 2])[:, None]
    cima = np.floor(forca * r[h // 2, :])[None, :]
    baixo = np.floor(forca * r[h // 3, :])[None, :]
    X, Y = img.X, img.Y
    return (X >= esq) & (X < w - dir_) & (Y >= cima) & (Y < h - baixo)


def perto_da_borda(folha, passos):
    """Quantos passos de 'encolher' a folha até o pixel sumir: 0 na borda,
    'passos' no miolo. Serve para escurecer as bordas (papel velho amarela
    e suja primeiro nas pontas)."""
    dist = np.zeros(folha.shape)
    m = folha.copy()
    for i in range(passos):
        p = np.pad(m, 1)
        m = m & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
        dist += m
    return dist / passos


def papel_pergaminho():
    """O diário do Baltazar (1750): pergaminho amarelado, bordas comidas e
    escuras, manchas de umidade. No canto de baixo, o esboço a pena que ele
    fez do robô: a cabeça, o olho de vidro e duas linhas saindo do olho, o
    "cone" do que o robô enxerga (docs/personagens/robos.md: a visão dos
    robôs é um cone, calculado por produto escalar)."""
    img = Imagem(LARGURA_PAPEL, ALTURA_PAPEL)
    X, Y = img.X, img.Y
    folha = borda_rasgada(img, 4, 21)
    manchas = ruido(img.w, img.h, 30, 24, 22)
    fino = ruido(img.w, img.h, 2, 2, 23)
    borda = perto_da_borda(folha, 10)
    v = 0.62 + 0.14 * manchas + 0.04 * fino - 0.45 * (1 - borda)
    # Duas manchas de umidade: círculos um pouco mais escuros.
    for (cx, cy, r) in ((168, 30, 14), (40, 120, 10)):
        v = v - 0.12 * img.elipse(cx, cy, r, r * 0.8)
    img.pintar(folha, PERGAMINHO, v)
    img.contornar(PERGAMINHO[0])
    # Esboço do robô (tinta marrom, traço de 1 px).
    tinta = np.zeros(folha.shape, dtype=bool)
    cabeca = img.elipse(26, 142, 9, 7) & ~img.elipse(26, 142, 8, 6)
    olho = img.elipse(29, 141, 3, 3) & ~img.elipse(29, 141, 2, 2)
    tinta |= cabeca | olho | img.ret(29, 141, 30, 142)
    tinta |= img.linha(32, 140, 62, 128) | img.linha(32, 142, 62, 150)
    tinta |= img.linha(19, 148, 17, 152) | img.linha(33, 148, 35, 152)
    img.cor(tinta & folha, TINTA_MARROM)
    return img


def papel_caderno_clarice():
    """O bilhete da Clarice (1994): folha de fichário, com os furos do lado,
    pautas azuis, a margem vermelha e um adesivo de estrela no canto. Em
    cima, o pedaço de fita adesiva que a prendia na tela do terminal."""
    img = Imagem(LARGURA_PAPEL, ALTURA_PAPEL)
    X, Y = img.X, img.Y
    folha = img.ret(0, 0, img.w, img.h)
    fino = ruido(img.w, img.h, 2, 2, 31)
    manchas = ruido(img.w, img.h, 40, 30, 32)
    borda = perto_da_borda(folha, 6)
    img.pintar(folha, PAPEL_CLARO, 0.82 + 0.08 * manchas + 0.03 * fino - 0.3 * (1 - borda))
    for y in pautas():
        img.cor(img.ret(0, y, img.w, y + 1) & ~img.ret(0, 0, 10, img.h), AZUL_PAUTA)
    img.cor(img.ret(10, 0, 11, img.h), VERMELHO_MARGEM)
    # Furos do fichário: três círculos vazados na esquerda.
    for cy in (30, 78, 126):
        img.apagar(img.elipse(5, cy, 2.5, 2.5))
    # Fita adesiva no alto, meio transparente (tom mais claro e amarelado).
    fita = img.poligono([(84, 0), (118, 0), (117, 7), (85, 8)])
    img.pintar(fita, bib.hexa("#d8d0a8", "#e6dfbd", "#f0ead0"), 0.5 + 0.3 * fino)
    # Adesivo de estrela no canto de cima (cor forte: é de 1994).
    estrela = []
    for i in range(10):
        ang = np.pi / 2 + i * np.pi / 5
        r = 7 if i % 2 == 0 else 3
        estrela.append((184 + r * np.cos(ang), 12 - r * np.sin(ang)))
    adesivo = img.poligono(estrela)
    img.pintar(adesivo, bib.hexa("#7a2a55", "#b0417a", "#d9669c", "#f19bc0"), 0.55 + 0.3 * (Y < 11))
    img.contornar(PAPEL_CLARO[0])
    return img


def papel_caderno_gabriel():
    """O caderno do Gabriel (2026): folha quadriculada de caderno de
    faculdade, com a espiral em cima. O quadriculado é bem fraco, para não
    brigar com o texto. Os bilhetes de "G." dos ciclos anteriores usam
    esta mesma folha (docs/historia/revelacao_central.md)."""
    img = Imagem(LARGURA_PAPEL, ALTURA_PAPEL)
    X, Y = img.X, img.Y
    folha = img.ret(0, 3, img.w, img.h)
    fino = ruido(img.w, img.h, 2, 2, 41)
    manchas = ruido(img.w, img.h, 40, 30, 42)
    borda = perto_da_borda(folha, 6)
    img.pintar(folha, PAPEL_CLARO, 0.85 + 0.06 * manchas + 0.03 * fino - 0.25 * (1 - borda))
    grade = folha & (((X % 6) == 0) | (((Y - 4) % 6) == 0)) & (Y > 5)
    img.cor(grade, CINZA_GRADE)
    # Espiral: furos redondos no alto e os aros de metal passando por eles.
    for x in range(8, img.w - 4, 8):
        img.apagar(img.elipse(x, 5, 1.6, 1.6))
        img.pintar(img.ret(x - 1, 0, x + 1, 5), "metal", 0.55)
    img.contornar(PAPEL_CLARO[0])
    return img


PAPEIS = {
    "papel_pergaminho": papel_pergaminho,
    "papel_caderno_clarice": papel_caderno_clarice,
    "papel_caderno_gabriel": papel_caderno_gabriel,
}


# ---------------------------------------------------------------------------
# Peças da interface
# ---------------------------------------------------------------------------


def espaco(aceso=False):
    """Um espaço da grade do inventário: um nicho escavado no concreto.
    A borda de cima e da esquerda fica escura e a de baixo e da direita
    clara (é o "chanfro para dentro": parece fundo, como uma prateleira).
    Aceso = selecionado: a borda vira a cor do sol, a mesma dos raios que
    entram pelo teto."""
    n = TAMANHO_ESPACO
    img = Imagem(n, n)
    fino = ruido(n, n, 2, 2, 3)
    tudo = img.ret(0, 0, n, n)
    img.pintar(tudo, "concreto", 0.32 + 0.08 * fino)
    dentro = img.ret(2, 2, n - 2, n - 2)
    img.cor(dentro, RAMPAS["concreto"][0])
    # Chanfro: sombra em cima/esquerda, luz embaixo/direita (1 px cada).
    img.pintar(img.ret(1, 1, n - 1, 2) | img.ret(1, 1, 2, n - 1), "concreto", 0.12)
    img.pintar(img.ret(1, n - 2, n - 1, n - 1) | img.ret(n - 2, 1, n - 1, n - 1), "concreto", 0.55)
    if aceso:
        borda = tudo & ~img.ret(1, 1, n - 1, n - 1)
        img.pintar(borda, "sol", 0.72)
        img.pintar(img.ret(1, 1, n - 1, 2) | img.ret(1, 1, 2, n - 1), "sol", 0.35)
    else:
        img.cor(tudo & ~img.ret(1, 1, n - 1, n - 1), CONTORNO)
    return img


def painel():
    """Fundo das janelas (inventário): concreto escuro e manchado, com uma
    moldura de 2 px (contorno quase preto + fio claro por dentro).
    Os cantos são cortados em diagonal, como uma placa gasta."""
    n = TAMANHO_PAINEL
    img = Imagem(n, n)
    fino = ruido(n, n, 2, 2, 5)
    manchas = ruido(n, n, 6, 6, 6)
    tudo = img.poligono([(1, 0), (n - 1, 0), (n, 1), (n, n - 1), (n - 1, n), (1, n), (0, n - 1), (0, 1)])
    img.pintar(tudo, "concreto", 0.14 + 0.08 * manchas + 0.05 * fino)
    borda = tudo & ~img.ret(1, 1, n - 1, n - 1)
    img.cor(borda, CONTORNO)
    fio = img.ret(1, 1, n - 1, n - 1) & ~img.ret(2, 2, n - 2, n - 2)
    img.pintar(fio, "concreto", 0.42 + 0.1 * fino)
    return img


def main():
    print("Gerando ícones e interface")
    for nome, funcao in ICONES.items():
        funcao().salvar(f"{nome}.png", PASTA_ITENS)
    espaco().salvar("espaco.png", PASTA_INTERFACE)
    espaco(aceso=True).salvar("espaco_selecionado.png", PASTA_INTERFACE)
    painel().salvar("painel.png", PASTA_INTERFACE)
    for nome, funcao in PAPEIS.items():
        funcao().salvar(f"{nome}.png", PASTA_INTERFACE)


if __name__ == "__main__":
    main()
