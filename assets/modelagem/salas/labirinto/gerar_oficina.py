# gerar_oficina.py — gera a ARTE da oficina do Zane e dos nós de controle do
# Labirinto: os hologramas e as peças eletrônicas jogadas pelo chão.
#
# Como rodar (Python 3 + numpy):
#
#   python assets/modelagem/salas/labirinto/gerar_oficina.py
#
# O que sai:
#   assets/sprites/cenario/objetos/holograma_onda.png     40 x 56  forma de onda com falhas de sinal
#   assets/sprites/cenario/objetos/holograma_barras.png   40 x 56  gráfico de barras e um medidor
#   assets/sprites/cenario/objetos/holograma_codigo.png   40 x 56  linhas de código com cursor
#   assets/sprites/salas/labirinto/componentes_0.png      placa de circuito
#   assets/sprites/salas/labirinto/componentes_1.png      cabo enrolado
#   assets/sprites/salas/labirinto/componentes_2.png      peças soltas (resistores, capacitor, parafuso)
#   assets/sprites/salas/labirinto/componentes_3.png      bandeja de chips
# Com PREVIA=<pasta>, também salva previa_oficina.png nessa pasta (não commitar).
#
# ---------------------------------------------------------------------------
# COMO UM HOLOGRAMA É DESENHADO
# ---------------------------------------------------------------------------
#
# Um holograma é uma tela que flutua sobre um emissor. No Godot ele é
# desenhado SEM LUZ (material "unshaded"): brilha mesmo no escuro, como os
# olhos dos robôs. Por isso a imagem precisa carregar a própria translucidez:
#
#   - o miolo do painel tem alfa baixo (~60 de 255): dá para ver a parede
#     atrás dele;
#   - a borda e o conteúdo têm alfa alto: o que "é luz" fica nítido;
#   - as LINHAS DE VARREDURA (uma fileira em cada três com alfa reduzido)
#     dão a textura de projeção. Em termos de matemática: alfa(y) é
#     multiplicado por 0,45 quando y % 3 == 2, uma onda quadrada vertical;
#   - as FALHAS DE SINAL deslocam uma faixa de fileiras 2 px para o lado,
#     como se o quadro tivesse chegado fora de sincronia;
#   - o FEIXE entre o emissor e o painel é um trapézio de alfa ~35.
#
# A forma de onda da primeira variação é a soma de duas senoides,
#   y(x) = A1 · sen(2π·x/λ1) + A2 · sen(2π·x/λ2 + φ),
# desenhada como uma polilinha de pixels. O comprimento de onda λ2 não é
# múltiplo de λ1, então a curva não repete dentro do painel e parece sinal.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")
PASTA_SALA = os.path.join(PASTA_PROJETO, "assets", "sprites", "salas", "labirinto")
PREVIA = os.environ.get("PREVIA", "")

_spec = importlib.util.spec_from_file_location(
    "gerar_biblioteca",
    os.path.join(PASTA_PROJETO, "assets", "modelagem", "salas", "biblioteca", "gerar_biblioteca.py"))
bib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bib)
Imagem, RAMPAS, salvar_png = bib.Imagem, bib.RAMPAS, bib.salvar_png

LARGURA, ALTURA = 40, 56
PAINEL = (4, 2, 36, 30)          # x0, y0, x1, y1 (o x1 e o y1 não entram)
EMISSOR_Y = 46                    # onde começa a base do emissor

# Rampa do holograma: do azul-petróleo escuro ao quase branco.
CIANO = bib.hexa("#04333d", "#0a6173", "#17b2c9", "#5be6f5", "#c9fcff")
LARANJA = bib.hexa("#4a2a08", "#9a5a14", "#e0902a", "#ffd27a")
ALPHA_MIOLO = 60
ALPHA_LINHA = 235
ALPHA_VARREDURA = 0.45


def rgba(cor, alfa):
    return [cor[0], cor[1], cor[2], int(alfa)]


def moldura_do_painel(img):
    """O vidro do painel: miolo translúcido, borda nítida de 1 px e os
    quatro cantos cortados em 1 px (um cantinho 'chanfrado')."""
    x0, y0, x1, y1 = PAINEL
    miolo = img.ret(x0, y0, x1, y1)
    img.cor(miolo, rgba(CIANO[1], ALPHA_MIOLO))
    borda = miolo & ~img.ret(x0 + 1, y0 + 1, x1 - 1, y1 - 1)
    img.cor(borda, rgba(CIANO[3], ALPHA_LINHA))
    for cx, cy in ((x0, y0), (x1 - 1, y0), (x0, y1 - 1), (x1 - 1, y1 - 1)):
        img.apagar(img.ret(cx, cy, cx + 1, cy + 1))
    img.cor(img.ret(x0 + 2, y0, x0 + 9, y0 + 1), rgba(CIANO[4], 255))


def conteudo_onda(img):
    x0, y0, x1, y1 = PAINEL
    meio = (y0 + y1) / 2.0
    xs = np.arange(x0 + 2, x1 - 2)
    y = (6.0 * np.sin(2 * np.pi * (xs - x0) / 14.0)
         + 3.5 * np.sin(2 * np.pi * (xs - x0) / 5.3 + 0.9))
    pontos = [(float(x) + 0.5, meio + float(v)) for x, v in zip(xs, y)]
    img.cor(img.caminho(pontos, 0.6), rgba(CIANO[4], ALPHA_LINHA))
    for x in range(x0 + 3, x1 - 3, 4):
        img.cor(img.ret(x, int(meio), x + 1, int(meio) + 1), rgba(CIANO[2], 200))
    img.cor(img.ret(x0 + 3, y1 - 5, x0 + 15, y1 - 4), rgba(CIANO[3], 220))
    img.cor(img.ret(x1 - 9, y0 + 4, x1 - 5, y0 + 8), rgba(LARANJA[2], 255))


def conteudo_barras(img):
    x0, y0, x1, y1 = PAINEL
    base = y1 - 4
    alturas = (7, 13, 9, 17, 11)
    for i, altura in enumerate(alturas):
        bx = x0 + 4 + i * 5
        img.cor(img.ret(bx, base - altura, bx + 3, base), rgba(CIANO[3], ALPHA_LINHA))
        img.cor(img.ret(bx, base - altura, bx + 3, base - altura + 1), rgba(CIANO[4], 255))
    img.cor(img.ret(x0 + 2, base, x1 - 2, base + 1), rgba(CIANO[2], 220))
    anel = img.elipse(x1 - 8, y0 + 8, 5.5, 5.5) & ~img.elipse(x1 - 8, y0 + 8, 3.5, 3.5)
    img.cor(anel, rgba(CIANO[3], ALPHA_LINHA))
    img.cor(img.linha(x1 - 8, y0 + 8, x1 - 5, y0 + 5, 0.6), rgba(LARANJA[3], 255))


def conteudo_codigo(img):
    x0, y0, x1, y1 = PAINEL
    comprimentos = (14, 9, 18, 6, 12, 16)
    recuos = (0, 3, 3, 0, 3, 6)
    for i, (n, recuo) in enumerate(zip(comprimentos, recuos)):
        y = y0 + 4 + i * 4
        cor = CIANO[3] if i != 2 else LARANJA[2]
        img.cor(img.ret(x0 + 3 + recuo, y, x0 + 3 + recuo + n, y + 1), rgba(cor, ALPHA_LINHA))
        img.cor(img.ret(x0 + 3 + recuo + n + 2, y, x0 + 3 + recuo + n + 4, y + 1), rgba(CIANO[2], 190))
    img.cor(img.ret(x0 + 3, y1 - 5, x0 + 5, y1 - 2), rgba(CIANO[4], 255))


def varredura_e_falhas(img, falhas):
    """Aplica as linhas de varredura e desloca as faixas de falha (cada
    uma é (primeira fileira, última fileira, deslocamento em px))."""
    for y in range(img.h):
        if y % 3 == 2:
            img.px[y, :, 3] = (img.px[y, :, 3] * ALPHA_VARREDURA).astype(np.uint8)
    for y0, y1, desloca in falhas:
        faixa = img.px[y0:y1].copy()
        img.px[y0:y1] = np.roll(faixa, desloca, axis=1)


def feixe_e_emissor(img):
    """O trapézio de luz que sobe do emissor ao painel, e a base: um disco
    de metal escuro com um anel de LED ciano."""
    x0, y0, x1, y1 = PAINEL
    for y in range(y1, EMISSOR_Y):
        t = (y - y1) / float(EMISSOR_Y - y1)
        meia = 3 + (1.0 - t) * 11
        cx = LARGURA / 2.0
        linha = img.ret(int(cx - meia), y, int(cx + meia), y + 1)
        img.cor(linha, rgba(CIANO[2], 38 - 18 * t))
    metal = RAMPAS["metal"]
    base = img.elipse(LARGURA / 2.0, EMISSOR_Y + 5, 11, 4.5)
    img.cor(base, rgba(metal[2], 255))
    img.cor(img.elipse(LARGURA / 2.0, EMISSOR_Y + 4, 9, 3.2), rgba(metal[3], 255))
    anel = img.elipse(LARGURA / 2.0, EMISSOR_Y + 4, 7, 2.4) & ~img.elipse(LARGURA / 2.0, EMISSOR_Y + 4, 5, 1.4)
    img.cor(anel, rgba(CIANO[3], 255))
    img.cor(img.ret(int(LARGURA / 2) - 1, EMISSOR_Y + 3, int(LARGURA / 2) + 1, EMISSOR_Y + 4), rgba(CIANO[4], 255))


def holograma(conteudo, falhas):
    img = Imagem(LARGURA, ALTURA)
    feixe_e_emissor(img)
    moldura_do_painel(img)
    conteudo(img)
    varredura_e_falhas(img, falhas)
    return img


# ---------------------------------------------------------------------------
# Peças no chão
# ---------------------------------------------------------------------------

PLACA = bib.hexa("#0b1a12", "#12301f", "#1d4a2e", "#2c6a40")
OURO = bib.hexa("#4a3a10", "#8a6c1c", "#c9a63a", "#f0d878")
ESCURO = bib.hexa("#0a0a0c", "#17181c", "#26282e", "#3a3d45")


def placa_de_circuito():
    """Uma placa verde com trilhas douradas, um chip preto e pontos de
    solda. As trilhas são caminhos de pixels: segmentos horizontais e
    verticais ligando o chip às bordas, como numa placa de verdade."""
    img = Imagem(22, 14)
    corpo = img.ret(1, 1, 21, 13)
    img.pintar(corpo, PLACA, 0.55 + 0.1 * (img.Y % 2))
    img.pintar(corpo & ~img.ret(2, 2, 20, 12), PLACA, 0.15)
    for caminho in ([(3, 4), (8, 4), (8, 6)], [(3, 9), (9, 9), (9, 7)],
                    [(14, 6), (14, 3), (18, 3)], [(14, 8), (14, 10), (18, 10)]):
        img.cor(img.caminho(caminho, 0.5), rgba(OURO[2], 255))
    chip = img.ret(9, 5, 15, 9)
    img.pintar(chip, ESCURO, 0.5)
    for x in range(10, 15, 2):
        img.cor(img.ret(x, 4, x + 1, 5), rgba(OURO[3], 255))
        img.cor(img.ret(x, 9, x + 1, 10), rgba(OURO[3], 255))
    for x, y in ((3, 4), (3, 9), (18, 3), (18, 10)):
        img.cor(img.ret(x - 1, y - 1, x + 1, y + 1), rgba(OURO[3], 255))
    img.cor(img.ret(5, 6, 6, 7), rgba([60, 220, 120], 255))
    return img


def cabo_enrolado():
    """Um cabo preto em espiral achatada (uma elipse vazia) com a ponta
    solta e o conector dourado."""
    img = Imagem(24, 12)
    for raio in (1.0, 0.72, 0.44):
        anel = img.elipse(10, 6, 9 * raio, 4.6 * raio) & ~img.elipse(10, 6, 9 * raio - 1.6, 4.6 * raio - 1.3)
        img.pintar(anel, "metal", 0.42)
    img.cor(img.caminho([(18, 6), (21, 8), (23, 7)], 0.7), rgba(RAMPAS["metal"][3], 255))
    img.cor(img.ret(21, 5, 23, 7), rgba(OURO[2], 255))
    img.cor(img.ret(4, 3, 7, 4), rgba(RAMPAS["metal"][5], 255))
    return img


def pecas_soltas():
    """Dois resistores (corpo bege com faixas coloridas e terminais), um
    capacitor azul em pé e um parafuso."""
    img = Imagem(26, 12)
    bege = bib.hexa("#4a4030", "#8a7a5a", "#c2ae82")
    for y, cores in ((2, ([200, 60, 50], [240, 200, 60], [60, 120, 220])),
                     (8, ([60, 160, 90], [90, 60, 40], [220, 220, 220]))):
        img.cor(img.ret(1, y, 4, y + 1), rgba(ESCURO[3], 255))
        img.cor(img.ret(13, y, 16, y + 1), rgba(ESCURO[3], 255))
        img.cor(img.ret(4, y - 1, 13, y + 2), rgba(bege[1], 255))
        img.cor(img.ret(4, y - 1, 13, y), rgba(bege[2], 255))
        for k, c in enumerate(cores):
            img.cor(img.ret(6 + k * 2, y - 1, 7 + k * 2, y + 2), rgba(c, 255))
    img.cor(img.ret(19, 2, 23, 9), rgba([36, 70, 140], 255))
    img.cor(img.ret(19, 2, 23, 3), rgba([90, 130, 200], 255))
    img.cor(img.ret(23, 3, 24, 9), rgba([20, 40, 90], 255))
    img.cor(img.ret(20, 9, 21, 11), rgba(ESCURO[3], 255))
    img.cor(img.ret(22, 9, 23, 11), rgba(ESCURO[3], 255))
    img.cor(img.elipse(17.5, 10.5, 1.4, 1.4), rgba(RAMPAS["metal"][4], 255))
    return img


def bandeja_de_chips():
    """Uma bandeja de metal rasa com duas fileiras de chips pretos."""
    img = Imagem(24, 14)
    metal = RAMPAS["metal"]
    img.pintar(img.ret(1, 1, 23, 13), "metal", 0.5)
    img.pintar(img.ret(1, 1, 23, 2), "metal", 0.85)
    img.pintar(img.ret(2, 2, 22, 12), "metal", 0.3)
    for fila in range(2):
        for k in range(4):
            x, y = 4 + k * 5, 4 + fila * 5
            img.cor(img.ret(x, y, x + 4, y + 3), rgba(ESCURO[1], 255))
            img.cor(img.ret(x, y, x + 4, y + 1), rgba(ESCURO[3], 255))
            img.cor(img.ret(x + 1, y + 3, x + 2, y + 4), rgba(metal[5], 255))
            img.cor(img.ret(x + 3, y + 3, x + 4, y + 4), rgba(metal[5], 255))
    return img


def main():
    print("Gerando a oficina do Zane e os nós de controle")
    os.makedirs(PASTA_OBJETOS, exist_ok=True)
    os.makedirs(PASTA_SALA, exist_ok=True)
    onda = holograma(conteudo_onda, ((9, 12, 2), (17, 19, -2)))
    barras = holograma(conteudo_barras, ((12, 14, -2),))
    codigo = holograma(conteudo_codigo, ((7, 9, 2), (20, 22, 2)))
    onda.salvar("holograma_onda.png", PASTA_OBJETOS)
    barras.salvar("holograma_barras.png", PASTA_OBJETOS)
    codigo.salvar("holograma_codigo.png", PASTA_OBJETOS)
    pecas = [placa_de_circuito(), cabo_enrolado(), pecas_soltas(), bandeja_de_chips()]
    for i, img in enumerate(pecas):
        img.salvar(f"componentes_{i}.png", PASTA_SALA)
    if PREVIA:
        folha = Imagem(150, 84)
        folha.px[:, :] = [22, 24, 30, 255]
        x = 4
        for img in (onda, barras, codigo):
            folha.colar(img, x, 4)
            x += 46
        x = 4
        for img in pecas:
            folha.colar(img, x, 66)
            x += img.w + 4
        ampliada = np.kron(folha.px, np.ones((4, 4, 1), dtype=np.uint8))
        salvar_png(os.path.join(PREVIA, "previa_oficina.png"), ampliada)
        print("  prévia: previa_oficina.png (não commitar)")


if __name__ == "__main__":
    main()
