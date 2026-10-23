# gerar_interiores_andar2.py — desenha, por código, o FUNDO de cada loja do
# segundo andar do Centro de Convivência: a Loja Universitária, a Gráfica
# Quântica e o Cine Andrômeda (docs/fases/centro_de_convivencia.md, seção 7).
#
# Este arquivo não gera nada sozinho: o gerar_andar2.py chama montar_fundo()
# daqui e grava os fundos em assets/sprites/cenario/praca/fundo_<sala>.png.
#
# Como nos restaurantes (gerar_interiores.py), a parede é uma fileira de peças
# de 80 px, cada uma com um DETALHE, sobre uma base de materiais da loja, e o
# piso é uma imagem só. A porta de vidro é colada na peça da porta.
#
# O jeito de cada loja:
#   LOJA UNIVERSITÁRIA (azul)    parede branca e lambri azul, estantes de
#                                moletons, araras, o brasão da universidade e um
#                                provador de cortina (o esconderijo);
#   GRÁFICA QUÂNTICA (limão)     concreto e aço, escaninhos de papel, cartuchos
#                                de tinta C-M-Y-K e faixas de segurança no piso;
#   CINE ANDRÔMEDA (violeta)     duas salas: o saguão de veludo (cartazes,
#                                cardápio da pipoca e o arco SALA 1) e a sala
#                                de projeção, que é uma sala à parte (entra-se
#                                pelo arco), com a tela larga e as poltronas.

import math

import numpy as np

import gerar_praca_base as base
import gerar_interiores as gi

Imagem, RAMPAS, SOMBRA, dilatar = base.Imagem, base.RAMPAS, base.SOMBRA, base.dilatar
ruido = base.ruido
ciclico = base.ruido_ciclico
L = base.PECA
H = base.ALTURA_PAREDE
LUZ = 0.8

TEMAS = {
    "loja_uni": "azul",
    "grafica": "limao",
    "cinema": "violeta",
    "sala_cinema": "violeta",
    "cabine": "violeta",
}


# ---------------------------------------------------------------------------
# Base da parede
# ---------------------------------------------------------------------------


def parede(tema, semente=0):
    neon = base.NEON[TEMAS[tema]]
    img = Imagem(L, H)
    X, Y = img.X, img.Y
    fino = ciclico(L, H, 2, 2, 3000 + semente)
    manchas = ciclico(L, H, 40, 16, 3001 + semente)
    alto = img.ret(0, 12, L, 62)
    baixo = img.ret(0, 64, L, 100)
    if tema == "loja_uni":
        v = (0.62 + 0.1 * manchas + 0.04 * fino) * LUZ
        img.pintar(alto, "papel_branco", v)
        img.pintar(alto & ((X % 40) == 0), "papel_branco", v - 0.22, achatar=False)
        img.pintar(alto & ((X % 40) == 1), "papel_branco", v + 0.1, achatar=False)
        img.pintar(baixo, "carpete", 0.4 + 0.1 * manchas)
        img.pintar(baixo & ((X % 20) == 0), "carpete", 0.16, achatar=False)
        img.pintar(baixo & ((X % 20) == 1), "carpete", 0.56, achatar=False)
        img.pintar(img.ret(0, 64, L, 66), "papel_branco", 0.72)
    elif tema == "grafica":
        v = (0.5 + 0.14 * manchas + 0.05 * fino) * LUZ
        img.pintar(alto, "concreto_fut", v)
        img.pintar(alto & ((X % 40) == 0), "concreto_fut", v - 0.3, achatar=False)
        img.pintar(alto & (((Y - 12) % 25) == 0), "concreto_fut", v - 0.2, achatar=False)
        escorrido = ciclico(L, H, 4, 56, 3002 + semente)
        img.pintar(alto & (escorrido > 0.74), "concreto_fut", v - 0.2)
        img.pintar(baixo, "inox", (0.36 + 0.1 * manchas) * LUZ)
        img.pintar(baixo & ((X % 16) == 0), "inox", 0.12, achatar=False)
        for x in range(3, L, 16):
            for y in (68, 94):
                img.pintar(img.ret(x, y, x + 2, y + 2), "inox", 0.7)
        faixa = img.ret(0, 96, L, 100)
        listra = (((X + Y) // 4) % 2) == 0
        img.pintar(faixa & listra, "areia", 0.7)
        img.pintar(faixa & ~listra, "grafite", 0.06)
    elif tema == "cinema":
        v = (0.4 + 0.12 * manchas + 0.04 * fino) * LUZ
        dobra = 0.5 + 0.5 * np.sin(X * 0.62)
        img.pintar(alto, "veludo", v + 0.22 * dobra)
        img.pintar(baixo, "madeira_fut", (0.38 + 0.08 * manchas) * LUZ)
        img.pintar(baixo & ((X % 20) == 0), "madeira_fut", 0.12, achatar=False)
        img.pintar(baixo & ((X % 20) == 1), "madeira_fut", 0.5, achatar=False)
    elif tema == "cabine":
        v = (0.3 + 0.1 * manchas + 0.04 * fino) * LUZ
        img.pintar(alto, "concreto_fut", v)
        img.pintar(alto & ((X % 40) == 0), "concreto_fut", v - 0.22, achatar=False)
        img.pintar(alto & (Y == 34), "inox", 0.3, achatar=False)
        img.pintar(baixo, "madeira_fut", (0.3 + 0.08 * manchas) * LUZ)
        img.pintar(baixo & ((X % 16) == 0), "madeira_fut", 0.1, achatar=False)
        img.pintar(baixo & ((X % 16) == 1), "madeira_fut", 0.44, achatar=False)
    else:
        v = (0.22 + 0.08 * manchas + 0.03 * fino) * LUZ
        img.pintar(alto, "grafite", v)
        losango = (((X + (Y - 12)) % 12) == 0) | (((X - (Y - 12)) % 12) == 0)
        img.pintar(alto & losango, "grafite", v - 0.12, achatar=False)
        img.pintar(baixo, "veludo", (0.3 + 0.06 * manchas) * LUZ)
    img.pintar(img.ret(0, 62, L, 64), "grafite", 0.1)
    img.pintar(img.ret(0, 62, L, 63), neon, 0.55, achatar=False)
    img.pintar(img.ret(0, 100, L, 101), "grafite", 0.1)
    gi.teto(img, neon, fino)
    gi.rodape(img, fino)
    img.fino, img.manchas, img.neon = fino, manchas, neon
    return img


def moldura(img, x0, y0, x1, y1, rampa="inox", tom=0.45):
    gi.moldura(img, x0, y0, x1, y1, rampa, tom)


# ---------------------------------------------------------------------------
# Detalhes da Loja Universitária
# ---------------------------------------------------------------------------

CORES_ROUPA = ("neon_azul", "papel_branco", "carpete", "grafite", "neon_azul", "papel_branco")


def u_lisa(semente=0):
    return parede("loja_uni", semente)


def u_prateleira(semente=1):
    """Três prateleiras com pilhas de camisetas e moletons dobrados, nas cores
    da universidade (azul, branco, grafite)."""
    img = parede("loja_uni", semente)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(3100 + semente)
    img.pintar(img.ret(6, 16, 74, 98), "inox", 0.16)
    for y in (42, 70, 96):
        img.pintar(img.ret(6, y, 74, y + 3), "inox", 0.5 + 0.2 * (Y == y))
    for y_base_prat in (42, 70, 96):
        x = 9
        while x < 68:
            larg = int(rng.integers(10, 15))
            pilhas = int(rng.integers(2, 5))
            rampa = CORES_ROUPA[int(rng.integers(0, len(CORES_ROUPA)))]
            for k in range(pilhas):
                topo = y_base_prat - (k + 1) * 5
                img.pintar(img.ret(x, topo, x + larg, topo + 5), rampa, 0.42 + 0.12 * (k % 2) + 0.14 * (X == x))
                img.pintar(img.ret(x, topo, x + larg, topo + 1), rampa, 0.7, achatar=False)
            x += larg + int(rng.integers(1, 4))
    return img


def u_cabides(semente=2):
    """Trilho de cabides na parede com jaquetas, camisas e um cachecol."""
    img = parede("loja_uni", semente)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(3110 + semente)
    img.pintar(img.ret(6, 28, 74, 30), "inox", 0.6 + 0.2 * (Y == 28))
    for x in (8, 72):
        img.pintar(img.ret(x - 1, 26, x + 2, 34), "inox", 0.4)
    for k in range(7):
        x0 = 10 + k * 9
        rampa = CORES_ROUPA[int(rng.integers(0, len(CORES_ROUPA)))]
        comp = int(rng.integers(26, 44))
        img.pintar(img.ret(x0 + 3, 30, x0 + 4, 34), "inox", 0.6)
        img.pintar(img.poligono([(x0, 36), (x0 + 3.5, 33), (x0 + 7, 36), (x0 + 8, 36 + comp), (x0 - 1, 36 + comp)]), rampa, 0.46 + 0.14 * (k % 2))
        img.pintar(img.ret(x0 + 3, 34, x0 + 4, 36 + comp), rampa, 0.22, achatar=False)
    return img


def u_brasao(semente=3):
    """O brasão da universidade em neon azul: um escudo com um livro aberto e
    uma estrela, e a palavra UNIVERSIDADE embaixo."""
    img = parede("loja_uni", semente)
    X, Y = img.X, img.Y
    rampa = "neon_azul"
    escudo = img.poligono([(24, 22), (56, 22), (56, 52), (40, 66), (24, 52)])
    img.pintar(escudo, "grafite", 0.06)
    img.pintar(escudo & ~(img.poligono([(26, 24), (54, 24), (54, 51), (40, 63), (26, 51)])), rampa, 0.82, achatar=False)
    img.pintar(img.poligono([(40, 27), (41.5, 31), (45.5, 31), (42.3, 33.5), (43.5, 37.5), (40, 35), (36.5, 37.5), (37.7, 33.5), (34.5, 31), (38.5, 31)]), "neon_ambar", 0.9, achatar=False)
    img.pintar(img.poligono([(30, 44), (40, 41), (40, 55), (30, 52)]), rampa, 0.6, achatar=False)
    img.pintar(img.poligono([(50, 44), (40, 41), (40, 55), (50, 52)]), rampa, 0.78, achatar=False)
    img.pintar(img.ret(40, 41, 41, 55), "grafite", 0.05)
    largura_texto = base.largura_do_texto("UNIVERSIDADE", 8)
    base.escrever(img, 40 - largura_texto // 2, 74, "UNIVERSIDADE", rampa, 0.92, 8)
    return img


def u_espelho(semente=4):
    """Espelho de corpo inteiro, com moldura de aço e o reflexo da sala."""
    img = parede("loja_uni", semente)
    X, Y = img.X, img.Y
    moldura(img, 18, 16, 62, 98, "inox", 0.42)
    vidro = img.ret(21, 19, 59, 95)
    img.pintar(vidro, "gelo", 0.26 + 0.1 * ((Y - 19) / 76.0) + 0.04 * img.fino)
    img.pintar(vidro & (X > 38) & (X < 47) & (Y > 44) & (Y < 90), "carpete", 0.3)
    img.pintar(img.elipse(42.5, 41, 3.5, 4) & vidro, "carpete", 0.34)
    reflexo = vidro & ((np.abs((X - Y) + 14) < 3) | (np.abs((X - Y) + 2) < 1.2))
    img.pintar(reflexo, "gelo", 0.72, achatar=False)
    img.pintar(img.ret(34, 96, 46, 100), "inox", 0.3)
    return img


def u_provador(semente=5):
    """Provador de cortina: uma cabine com a cortina azul entreaberta e o vão
    escuro no meio. É onde o Gabriel se esconde (nicho)."""
    img = parede("loja_uni", semente)
    X, Y = img.X, img.Y
    img.pintar(img.ret(12, 20, 68, 112), "inox", 0.42 + 0.2 * (Y == 20) + 0.1 * (X == 12))
    vao = img.ret(16, 24, 64, 112)
    prof = np.clip((Y - 24) / 88.0, 0, 1)
    img.pintar(vao, "grafite", 0.03 + 0.04 * prof)
    img.pintar(img.ret(16, 24, 22, 112), "grafite", 0.12, achatar=False)
    img.pintar(img.ret(14, 24, 66, 27), "inox", 0.7)
    for lado in (0, 1):
        x_a, x_b = (16, 30) if lado == 0 else (50, 64)
        cortina = img.ret(x_a, 27, x_b, 108)
        dobra = 0.5 + 0.5 * np.sin((X - x_a) * (0.9 if lado == 0 else 0.9) + lado)
        img.pintar(cortina, "neon_azul", 0.2 + 0.2 * dobra + 0.04 * img.fino)
        img.pintar(cortina & ((X - x_a) % 7 == 0), "carpete", 0.3, achatar=False)
        img.pintar(img.ret(x_a, 104, x_b, 108), "carpete", 0.2)
    for x in range(18, 64, 6):
        img.pintar(img.ret(x, 25, x + 1, 28), "inox", 0.8)
    img.pintar(img.ret(34, 20, 46, 23), "grafite", 0.07)
    base.escrever(img, 40 - base.largura_do_texto("PROVA", 8) // 2, 14, "PROVA", "neon_azul", 0.7, 8)
    return img


# ---------------------------------------------------------------------------
# Detalhes da Gráfica Quântica
# ---------------------------------------------------------------------------

CORES_PAPEL = ("papel_branco", "ciano", "neon_magenta", "neon_ambar", "papel_branco", "neon_limao")


def g_lisa(semente=0):
    return parede("grafica", semente)


def g_escaninhos(semente=1):
    """Escaninhos de papel: uma grade de 4 x 3 vãos escuros com resmas e folhas
    saindo, de várias cores."""
    img = parede("grafica", semente)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(3200 + semente)
    img.pintar(img.ret(6, 16, 74, 98), "inox", 0.3)
    for gy in range(3):
        for gx in range(4):
            x0, y0 = 8 + gx * 16.5, 18 + gy * 26.5
            x0, y0 = int(x0), int(y0)
            img.pintar(img.ret(x0, y0, x0 + 15, y0 + 24), "grafite", 0.05)
            cheio = int(rng.integers(0, 4))
            for k in range(cheio):
                rampa = CORES_PAPEL[int(rng.integers(0, len(CORES_PAPEL)))]
                img.pintar(img.ret(x0 + 1, y0 + 22 - k * 5, x0 + 14, y0 + 24 - k * 5), rampa, 0.5 + 0.1 * k)
                img.pintar(img.ret(x0 + 1, y0 + 22 - k * 5, x0 + 14, y0 + 23 - k * 5), "papel_branco", 0.82, achatar=False)
            if rng.random() < 0.5:
                img.pintar(img.poligono([(x0 + 4, y0 + 9), (x0 + 12, y0 + 9), (x0 + 13, y0 + 15), (x0 + 5, y0 + 16)]), "papel_branco", 0.78)
    return img


def g_cartazes(semente=2):
    """Parede de cartazes presos com fita: quatro folhas de tamanhos e cores
    diferentes, uma delas rasgada, cada uma com um bloco de texto em linhas."""
    img = parede("grafica", semente)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(3210 + semente)
    for (x0, y0, x1, y1, cor) in ((8, 22, 32, 56, "neon_magenta"), (36, 18, 58, 44, "ciano"), (40, 48, 72, 90, "neon_limao"), (10, 62, 34, 92, "neon_ambar")):
        img.pintar(img.ret(x0, y0, x1, y1), "papel_branco", 0.82 - 0.06 * (X == x0))
        img.pintar(img.ret(x0 + 2, y0 + 2, x1 - 2, y0 + 12), cor, 0.52)
        for k in range(int((y1 - y0 - 18) // 4)):
            comp = int(rng.integers(6, max(7, x1 - x0 - 6)))
            img.pintar(img.ret(x0 + 3, y0 + 15 + k * 4, x0 + 3 + comp, y0 + 16 + k * 4), "grafite", 0.2, achatar=False)
        img.pintar(img.ret(x0 + 2, y0 - 1, x0 + 7, y0 + 1), "papel_branco", 0.45)
        img.pintar(img.ret(x1 - 7, y0 - 1, x1 - 2, y0 + 1), "papel_branco", 0.45)
    img.pintar(img.poligono([(36, 44), (46, 44), (40, 49), (37, 47)]), "concreto_fut", 0.46)
    return img


def g_tintas(semente=3):
    """Rack de cartuchos de tinta: duas fileiras de cartuchos C, M, Y e K, cada
    um com um LED e uma etiqueta, e um cartucho vazio caído."""
    img = parede("grafica", semente)
    X, Y = img.X, img.Y
    img.pintar(img.ret(8, 20, 72, 92), "inox", 0.2)
    cores = ("ciano", "neon_magenta", "neon_ambar", "grafite")
    for fila, y0 in enumerate((24, 58)):
        img.pintar(img.ret(10, y0 + 28, 70, y0 + 31), "inox", 0.5 + 0.2 * (Y == y0 + 28))
        for k in range(8):
            x0 = 12 + k * 7
            rampa = cores[k % 4]
            nivel = int(((k * 5 + fila * 3) % 7) + 12)
            img.pintar(img.ret(x0, y0 + 4, x0 + 5, y0 + 28), "inox", 0.3)
            img.pintar(img.ret(x0 + 1, y0 + 28 - nivel, x0 + 4, y0 + 28), rampa, 0.46 + 0.14 * (X == x0 + 1) if rampa != "grafite" else 0.08)
            img.pintar(img.ret(x0 + 1, y0 + 6, x0 + 4, y0 + 8), "papel_branco", 0.7)
            led = base.hexa("#6cf28e")[0] if (k + fila) % 3 else base.hexa("#ff5a3a")[0]
            img.cor(img.ret(x0 + 2, y0 + 10, x0 + 3, y0 + 11), led)
    return img


def g_rolos(semente=4):
    """Prateleira de rolos de papel vistos de ponta: círculos brancos com o
    miolo escuro, em duas fileiras."""
    img = parede("grafica", semente)
    X, Y = img.X, img.Y
    img.pintar(img.ret(6, 18, 74, 98), "inox", 0.16)
    for y in (56, 96):
        img.pintar(img.ret(6, y, 74, y + 3), "inox", 0.5 + 0.2 * (Y == y))
    rng = np.random.default_rng(3230 + semente)
    for y_c in (44, 84):
        for x_c in (19, 40, 61):
            if rng.random() < 0.85:
                r = 9 + int(rng.integers(0, 2))
                img.pintar(img.elipse(x_c, y_c, r, r), "papel_branco", 0.74 - 0.2 * ((X - x_c) + (Y - y_c) > 6) + 0.05 * img.fino)
                img.pintar(img.elipse(x_c, y_c, r - 3, r - 3), "papel_branco", 0.66)
                img.pintar(img.elipse(x_c, y_c, 3, 3), "grafite", 0.05)
                for k in range(3):
                    img.pintar((np.abs(np.hypot(X + 0.5 - x_c, Y + 0.5 - y_c) - (4 + k * 2)) < 0.5), "papel_branco", 0.46, achatar=False)
    return img


def g_painel(semente=5):
    """Painel de controle da impressora grande: uma tela com a barra de
    andamento parada em erro (vermelho) e uma fileira de botões."""
    img = parede("grafica", semente)
    X, Y = img.X, img.Y
    moldura(img, 10, 22, 70, 86, "inox", 0.34)
    tela = img.ret(14, 26, 66, 62)
    img.pintar(tela, "grafite", 0.05 + 0.04 * (Y % 3 == 0))
    base.escrever(img, 18, 29, "ERRO 41", "neon_vermelho", 0.9, 8)
    img.pintar(img.ret(18, 44, 62, 48), "neon_limao", 0.18, achatar=False)
    img.pintar(img.ret(18, 44, 36, 48), "neon_limao", 0.78, achatar=False)
    img.pintar(img.ret(18, 52, 48, 53), "neon_limao", 0.42, achatar=False)
    img.pintar(img.ret(18, 56, 40, 57), "neon_limao", 0.3, achatar=False)
    for k in range(6):
        img.pintar(img.ret(15 + k * 8, 68, 20 + k * 8, 73), ("neon_vermelho", "inox", "inox", "neon_limao", "inox", "inox")[k], 0.5)
    img.cor(img.ret(60, 76, 62, 78), base.hexa("#ff5a3a")[0])
    img.pintar(img.ret(14, 78, 40, 80), "inox", 0.22)
    return img


def g_nicho(semente=6):
    """Nicho da sala dos fundos: um vão escuro com uma porta de aço entreaberta."""
    img = parede("grafica", semente)
    X, Y = img.X, img.Y
    img.pintar(img.ret(14, 22, 66, 112), "inox", 0.44 + 0.2 * (Y == 22) + 0.1 * (X == 14))
    vao = img.ret(18, 26, 62, 112)
    prof = np.clip((Y - 26) / 86.0, 0, 1)
    img.pintar(vao, "grafite", 0.03 + 0.05 * prof)
    img.pintar(img.ret(18, 26, 24, 112), "grafite", 0.14, achatar=False)
    img.pintar(img.ret(52, 26, 62, 112), "inox", 0.3 + 0.1 * (X == 52))
    img.pintar(img.ret(55, 60, 59, 76), "grafite", 0.06)
    faixa = img.ret(18, 26, 62, 32)
    img.pintar(faixa & ((((X + Y) // 4) % 2) == 0), "areia", 0.7)
    img.pintar(faixa & ((((X + Y) // 4) % 2) == 1), "grafite", 0.06)
    return img


# ---------------------------------------------------------------------------
# Detalhes do Cine Andrômeda (saguão e sala)
# ---------------------------------------------------------------------------


def c_lisa(semente=0):
    return parede("cinema", semente)


def c_cartazes(semente=1, variante=0):
    """Três cartazes de filme emoldurados em dourado, com lâmpadas de marquise
    acima. A 'variante' troca as cores dos cartazes."""
    img = parede("cinema", semente)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(3300 + semente)
    for k, x0 in enumerate((6, 29, 52)):
        img.pintar(img.ret(x0 - 1, 22, x0 + 21, 82), "neon_ambar", 0.3 + 0.15 * (Y == 22))
        quadro = img.ret(x0, 23, x0 + 20, 81)
        conjuntos = ((("neon_violeta", "neon_ambar"), ("neon_magenta", "ciano"), ("neon_azul", "neon_limao")),
                     (("neon_azul", "neon_ambar"), ("neon_violeta", "neon_limao"), ("neon_magenta", "papel_branco")))
        cores = conjuntos[variante][k]
        img.pintar(quadro, cores[0], 0.22 + 0.3 * (1 - (Y - 23) / 58.0))
        img.pintar(img.elipse(x0 + 10, 44 + 3 * k, 6, 6) & quadro, cores[1], 0.68 + 0.2 * ((X - x0 - 10) < 0))
        img.pintar(img.poligono([(x0 + 3, 81), (x0 + 6, 60), (x0 + 10, 56), (x0 + 14, 60), (x0 + 17, 81)]) & quadro, "grafite", 0.05)
        img.pintar(img.ret(x0 + 2, 74, x0 + 2 + int(rng.integers(8, 16)), 75) & quadro, "papel_branco", 0.8, achatar=False)
        img.pintar(img.elipse(x0 + 10, 19, 1.3, 1.3), "neon_ambar", 1.0 if k % 2 == 0 else 0.5, achatar=False)
    return img


def c_planta(semente=7):
    """Um vaso grande com uma palmeira de interior, entre duas arandelas de luz
    âmbar."""
    img = parede("cinema", semente)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(3320 + semente)
    for x in (12, 68):
        img.pintar(img.ret(x - 2, 30, x + 3, 40), "grafite", 0.1)
        img.pintar(img.elipse(x, 40, 3, 2), "neon_ambar", 0.7, achatar=False)
        img.pintar(img.poligono([(x - 3, 30), (x + 4, 30), (x + 8, 48), (x - 7, 48)]) & (((X + Y) % 2) == 0), "neon_ambar", 0.2, achatar=False)
    for k in range(9):
        ang = np.radians(-165 + k * 18.75)
        comp = 26 + 8 * rng.random()
        meio = (40 + comp * 0.55 * np.cos(ang), 80 + comp * 0.55 * np.sin(ang) - 4)
        ponta = (40 + comp * 0.95 * np.cos(ang), 80 + comp * 0.8 * np.sin(ang) + 6)
        img.pintar(img.caminho([(40, 80), meio, ponta], 1.3), "verde", 0.4 + 0.2 * rng.random())
        img.pintar(img.caminho([meio, ponta], 0.6), "bioluz", 0.55)
    img.pintar(img.poligono([(24, 80), (56, 80), (53, 100), (27, 100)]), "grafite", 0.2 + 0.1 * (X < 36))
    img.pintar(img.ret(24, 80, 56, 83), "neon_ambar", 0.4)
    return img


def c_relogio(semente=8):
    """Relógio redondo de parede com o aro âmbar, e a plaquinha de SAÍDA."""
    img = parede("cinema", semente)
    X, Y = img.X, img.Y
    cx, cy = 40, 48
    img.pintar(img.elipse(cx, cy, 17, 17), "neon_ambar", 0.3 + 0.1 * (Y < cy))
    img.pintar(img.elipse(cx, cy, 15, 15), "grafite", 0.07)
    for k in range(12):
        a = np.radians(k * 30)
        x, y = int(round(cx + 12.5 * np.sin(a))), int(round(cy - 12.5 * np.cos(a)))
        img.pintar(img.ret(x, y, x + 1, y + 1), "neon_ambar", 0.9, achatar=False)
    img.pintar(img.caminho([(cx, cy), (cx + 6, cy - 7)], 0.7), "papel_branco", 0.9, achatar=False)
    img.pintar(img.caminho([(cx, cy), (cx - 2, cy - 11)], 0.6), "papel_branco", 0.9, achatar=False)
    img.pintar(img.elipse(cx, cy, 1.4, 1.4), "neon_ambar", 1.0, achatar=False)
    img.pintar(img.ret(26, 76, 54, 88), "grafite", 0.06)
    img.pintar(img.ret(26, 76, 54, 77), "neon_verde", 0.4, achatar=False)
    base.escrever(img, 40 - base.largura_do_texto("SAÍDA", 8) // 2, 79, "SAÍDA", "neon_verde", 0.92, 8)
    return img


def c_cardapio(semente=2):
    """Cardápio holográfico da bomboniere: PIPOCA em letras grandes, três
    tamanhos de balde com preço e um ícone de milho."""
    img = parede("cinema", semente)
    X, Y = img.X, img.Y
    moldura(img, 8, 20, 72, 92, "inox", 0.4)
    tela = img.ret(11, 23, 69, 89)
    img.pintar(tela, "grafite", 0.05 + 0.04 * (Y % 3 == 0))
    largura_texto = base.largura_do_texto("PIPOCA", 16)
    base.escrever(img, 40 - largura_texto // 2, 26, "PIPOCA", "neon_ambar", 0.92, 16)
    for k, (comp, alt) in enumerate(((10, 12), (14, 16), (18, 20))):
        x0 = 15 + k * 17
        balde = img.poligono([(x0, 86 - alt), (x0 + comp * 0.8, 86 - alt), (x0 + comp * 0.7, 86), (x0 + comp * 0.1, 86)])
        img.pintar(balde, "neon_vermelho", 0.55)
        img.pintar(balde & (((X - x0) // 3) % 2 == 0), "papel_branco", 0.7)
        img.pintar(img.elipse(x0 + comp * 0.4, 86 - alt - 1, comp * 0.5, 3) & tela, "papel_branco", 0.86)
    img.pintar(img.ret(14, 54, 66, 55), "neon_violeta", 0.5, achatar=False)
    return img


def c_arco_sala(semente=3):
    """A entrada da sala de projeção: arco de latão com a luz violeta, o vão
    escuro e o letreiro SALA 1."""
    img = parede("cinema", semente)
    X, Y = img.X, img.Y
    img.pintar(img.ret(10, 24, 70, 112), "neon_ambar", 0.28 + 0.14 * (Y == 24) + 0.08 * (X == 10))
    vao = img.ret(14, 28, 66, 112)
    prof = np.clip((Y - 28) / 84.0, 0, 1)
    img.pintar(vao, "veludo", 0.04 + 0.04 * prof)
    img.pintar(vao & (Y > 28) & (Y < 40), "neon_violeta", 0.2 * (1 - (Y - 28) / 12.0), achatar=False)
    img.pintar(img.ret(10, 24, 70, 26), "neon_ambar", 0.5, achatar=False)
    for lado in (0, 1):
        x_a = 14 if lado == 0 else 56
        img.pintar(img.ret(x_a, 28, x_a + 10, 112), "veludo", 0.26 + 0.2 * (0.5 + 0.5 * np.sin(X * 0.9)))
    img.pintar(img.ret(24, 14, 56, 22), "grafite", 0.06)
    base.escrever(img, 40 - base.largura_do_texto("SALA 1", 8) // 2, 14, "SALA 1", "neon_violeta", 0.92, 8)
    return img


def c_nicho(semente=4):
    """Nicho atrás de uma cortina de veludo pesada, onde cabe uma pessoa."""
    img = parede("cinema", semente)
    X, Y = img.X, img.Y
    img.pintar(img.ret(14, 22, 66, 112), "neon_ambar", 0.26 + 0.12 * (Y == 22))
    vao = img.ret(18, 26, 62, 112)
    prof = np.clip((Y - 26) / 86.0, 0, 1)
    img.pintar(vao, "grafite", 0.03 + 0.04 * prof)
    img.pintar(img.ret(18, 26, 30, 112), "veludo", 0.3 + 0.24 * (0.5 + 0.5 * np.sin(X * 0.95)))
    img.pintar(img.ret(50, 26, 62, 112), "veludo", 0.3 + 0.24 * (0.5 + 0.5 * np.sin(X * 0.95 + 2)))
    img.pintar(img.ret(18, 26, 62, 31), "veludo", 0.2)
    img.pintar(img.ret(18, 29, 62, 30), "neon_ambar", 0.5, achatar=False)
    return img


def s_painel(semente=5):
    """Painel acústico da sala, com três arandelas de luz violeta fraca."""
    img = parede("sala_cinema", semente)
    X, Y = img.X, img.Y
    for x in (14, 40, 66):
        img.pintar(img.ret(x - 3, 30, x + 4, 46), "inox", 0.3)
        img.pintar(img.ret(x - 2, 31, x + 3, 45), "grafite", 0.05)
        img.pintar(img.ret(x - 1, 33, x + 2, 43), "neon_violeta", 0.5, achatar=False)
    return img


def s_lisa(semente=6):
    return parede("sala_cinema", semente)


def tela_larga(largura=240, altura=112):
    """A parede da TELA: a moldura de aço preta com a borda de luz violeta e a
    superfície escura com um reflexo; a imagem em movimento (as barras de teste
    que piscam) é um sprite animado à parte."""
    img = Imagem(largura, altura)
    X, Y = img.X, img.Y
    fino = ciclico(largura, altura, 2, 2, 3400)
    losango = (((X + (Y - 12)) % 12) == 0) | (((X - (Y - 12)) % 12) == 0)
    v = 0.2 * LUZ
    img.pintar(img.ret(0, 12, largura, 100), "grafite", v)
    img.pintar(img.ret(0, 12, largura, 100) & losango, "grafite", v - 0.12, achatar=False)
    img.pintar(img.ret(0, 100, largura, 112), "veludo", 0.3)
    gi.teto(img, "neon_violeta", fino)
    gi.rodape(img, fino)
    img.pintar(img.ret(2, 14, largura - 2, 100), "inox", 0.22 + 0.16 * (Y == 14))
    img.pintar(img.ret(5, 17, largura - 5, 97), "grafite", 0.02)
    img.pintar(img.ret(3, 15, largura - 3, 16), "neon_violeta", 0.6, achatar=False)
    img.pintar(img.ret(3, 98, largura - 3, 99), "neon_violeta", 0.5, achatar=False)
    return img


# ---------------------------------------------------------------------------
# Detalhes da cabine de projeção
# ---------------------------------------------------------------------------


def p_janela(semente=1):
    """A janelinha de projeção: um vão comprido com o vidro escuro de onde sai
    o feixe de luz violeta (pontilhado) para a sala, e o painel de botões
    embaixo."""
    img = parede("cabine", semente)
    X, Y = img.X, img.Y
    moldura(img, 8, 30, 72, 52, "inox", 0.4)
    vidro = img.ret(11, 33, 69, 49)
    img.pintar(vidro, "grafite", 0.04)
    feixe = img.poligono([(18, 41), (68, 34), (68, 48)]) & vidro
    img.pintar(feixe & (((X + Y) % 2) == 0), "neon_violeta", 0.46, achatar=False)
    img.pintar(img.ret(14, 40, 19, 43) & vidro, "papel_branco", 0.9, achatar=False)
    moldura(img, 12, 58, 68, 80, "inox", 0.34)
    img.pintar(img.ret(14, 60, 66, 78), "grafite", 0.07)
    cores = ("neon_verde", "neon_ambar", "inox", "neon_vermelho", "inox", "neon_verde", "inox", "neon_ambar")
    for k, rampa in enumerate(cores):
        img.pintar(img.ret(16 + k * 6, 63, 19 + k * 6, 66), rampa, 0.6)
    for k in range(3):
        img.pintar(img.ret(16, 69 + k * 3, 62, 70 + k * 3), "inox", 0.2)
        img.pintar(img.ret(20 + k * 16, 68 + k * 3, 23 + k * 16, 72 + k * 3), "inox", 0.74)
    return img


def p_horarios(semente=2):
    """Quadro de sessões: o título em violeta e três horários em âmbar, cada um
    com a barra de lotação."""
    img = parede("cabine", semente)
    X, Y = img.X, img.Y
    moldura(img, 8, 18, 72, 92, "inox", 0.4)
    img.pintar(img.ret(11, 21, 69, 89), "grafite", 0.05 + 0.04 * (Y % 3 == 0))
    base.escrever(img, 40 - base.largura_do_texto("SESSÕES", 8) // 2, 24, "SESSÕES", "neon_violeta", 0.92, 8)
    img.pintar(img.ret(14, 35, 66, 36), "neon_violeta", 0.4, achatar=False)
    for k, (hora, lotacao) in enumerate((("19:30", 30), ("21:00", 44), ("23:15", 12))):
        y = 41 + k * 15
        base.escrever(img, 15, y, hora, "neon_ambar", 0.9, 8)
        img.pintar(img.ret(44, y + 2, 66, y + 5), "grafite", 0.12)
        img.pintar(img.ret(44, y + 2, 44 + int(lotacao / 2), y + 5), "neon_verde", 0.6, achatar=False)
    return img


def p_rolos(semente=3):
    """Prateleira de latas de filme, vistas de frente: discos de aço com a
    etiqueta colorida, em duas fileiras."""
    img = parede("cabine", semente)
    X, Y = img.X, img.Y
    img.pintar(img.ret(6, 18, 74, 98), "inox", 0.14)
    for y in (56, 96):
        img.pintar(img.ret(6, y, 74, y + 3), "inox", 0.5 + 0.2 * (Y == y))
    cores = ("neon_violeta", "neon_ambar", "neon_azul", "neon_magenta")
    for linha, y_c in enumerate((43, 83)):
        for k, x_c in enumerate((17, 32, 47, 62)):
            r = 6.5
            lata = img.elipse(x_c, y_c, r, r)
            img.pintar(lata, "inox", 0.36 + 0.3 * (((X - x_c) + (Y - y_c)) < 0))
            img.pintar(img.elipse(x_c, y_c, 4, 4), "grafite", 0.1)
            img.pintar(img.elipse(x_c, y_c, 1.4, 1.4), "inox", 0.6)
            img.pintar(img.ret(x_c - 5, y_c + 4, x_c + 5, y_c + 6) & lata, cores[(k + linha) % 4], 0.6)
    return img


def p_uniforme(semente=4):
    """Os ganchos do lanterninha: o paletó vinho com os botões dourados, a
    lanterna pendurada e a plaqueta com o nome TADEU."""
    img = parede("cabine", semente)
    X, Y = img.X, img.Y
    img.pintar(img.ret(10, 24, 70, 26), "inox", 0.6 + 0.2 * (Y == 24))
    for x in (14, 40, 64):
        img.pintar(img.ret(x - 1, 26, x + 2, 30), "inox", 0.7)
    img.pintar(img.poligono([(24, 30), (32, 28), (40, 30), (44, 38), (42, 76), (22, 76), (20, 38)]), "veludo", 0.46 + 0.22 * ((X - 20) < 8))
    img.pintar(img.ret(31, 30, 33, 76), "veludo", 0.2, achatar=False)
    for y in (42, 54, 66):
        img.pintar(img.elipse(35, y, 1.4, 1.4), "neon_ambar", 0.9, achatar=False)
    img.pintar(img.ret(54, 30, 58, 34), "inox", 0.6)
    img.pintar(img.ret(55, 34, 57, 52), "inox", 0.4)
    img.pintar(img.poligono([(52, 52), (60, 52), (62, 62), (50, 62)]), "grafite", 0.14)
    img.pintar(img.ret(52, 52, 60, 53), "neon_ambar", 0.7, achatar=False)
    img.pintar(img.ret(22, 84, 58, 96), "grafite", 0.07)
    img.pintar(img.ret(22, 84, 58, 85), "inox", 0.5)
    base.escrever(img, 40 - base.largura_do_texto("TADEU", 8) // 2, 86, "TADEU", "neon_violeta", 0.9, 8)
    return img


def piso_cabine(largura, altura, y0=112):
    """Chão de concreto escuro da cabine, com um tapete de veludo velho no meio
    e os cabos grossos que saem do projetor para a janela."""
    img = Imagem(largura, altura)
    X, Y = img.X, img.Y
    chao = Y >= y0
    fino = ciclico(largura, altura, 2, 2, 3530)
    manchas = ruido(largura, altura, 50, 20, 3531)
    v = (0.26 + 0.12 * manchas + 0.04 * fino) * LUZ - 0.14 * np.clip((20 - (Y - y0)) / 20, 0, 1)
    img.pintar(chao, "concreto_fut", v)
    img.pintar(chao & ((((Y - y0) % 32) == 0) | ((X % 64) == 0)), "concreto_fut", v - 0.18, achatar=False)
    tapete = chao & (X >= 120) & (X < 300) & (Y >= y0 + 36) & (Y < y0 + 90)
    img.pintar(tapete, "veludo", 0.34 + 0.1 * manchas)
    img.pintar(tapete & (((X + Y) % 10) == 0), "veludo", 0.16, achatar=False)
    borda = chao & (X >= 118) & (X < 302) & (Y >= y0 + 34) & (Y < y0 + 92) & ~tapete
    img.pintar(borda, "neon_ambar", 0.3, achatar=False)
    cabo = img.caminho([(150, y0 + 6), (160, y0 + 24), (190, y0 + 30), (200, y0 + 52)], 1.2) & chao
    img.pintar(cabo, "grafite", 0.06)
    img.pintar(np.roll(cabo, -1, axis=0) & ~cabo & chao, "grafite", 0.22, achatar=False)
    img.cor(chao & (Y == y0), SOMBRA)
    img.chao = chao
    return img


# ---------------------------------------------------------------------------
# Pisos
# ---------------------------------------------------------------------------


def piso_loja_uni(largura, altura, y0=112):
    """Carpete azul-escuro com a passadeira de losangos claros no meio e o
    filete branco nas bordas."""
    img = Imagem(largura, altura)
    X, Y = img.X, img.Y
    chao = Y >= y0
    fino = ciclico(largura, altura, 2, 2, 3500)
    manchas = ruido(largura, altura, 60, 20, 3501)
    v = (0.3 + 0.1 * manchas + 0.06 * fino) * LUZ - 0.18 * np.clip((20 - (Y - y0)) / 20, 0, 1)
    img.pintar(chao, "carpete", v)
    img.pintar(chao & (((X + Y) % 10) == 0) & (((X - Y) % 10) != 0), "carpete", v + 0.08, achatar=False)
    passadeira = chao & (Y >= y0 + 44) & (Y < y0 + 84)
    img.pintar(passadeira, "carpete", v + 0.18)
    losango = (((X + Y) % 16) == 0) | (((X - Y) % 16) == 0)
    img.pintar(passadeira & losango, "papel_branco", 0.42, achatar=False)
    img.pintar(chao & ((Y == y0 + 44) | (Y == y0 + 83)), "papel_branco", 0.62, achatar=False)
    img.cor(chao & (Y == y0), SOMBRA)
    img.chao = chao
    return img


ZONAS_DE_SEGURANCA = ((100, 150, 260, 212), (300, 150, 440, 212))


def piso_grafica(largura, altura, y0=112):
    """Concreto polido (epóxi) com juntas de dilatação, as faixas amarelas
    de segurança em volta das máquinas e um ralo de vez em quando."""
    img = Imagem(largura, altura)
    X, Y = img.X, img.Y
    chao = Y >= y0
    fino = ciclico(largura, altura, 2, 2, 3510)
    manchas = ruido(largura, altura, 50, 20, 3511)
    sorteio = np.random.default_rng(3512).random(((altura // 32) + 3, (largura // 48) + 3))
    tom = sorteio[(Y - y0) // 32 + 1, X // 48]
    v = (0.34 + 0.14 * tom + 0.12 * manchas + 0.04 * fino) * LUZ
    img.pintar(chao, "concreto_fut", v)
    img.pintar(chao & ((((Y - y0) % 32) == 0) | ((X % 48) == 0)), "concreto_fut", v - 0.2, achatar=False)
    for (xa, ya, xb, yb) in ZONAS_DE_SEGURANCA:
        borda = img.ret(xa, ya, xb, yb) & ~img.ret(xa + 2, ya + 2, xb - 2, yb - 2) & chao
        tracejado = (((X + Y) // 5) % 2) == 0
        img.pintar(borda & tracejado, "areia", 0.7, achatar=False)
        img.pintar(borda & ~tracejado, "grafite", 0.08, achatar=False)
    for (cx, cy) in ((250, 222), (470, 226)):
        ralo = img.elipse(cx, cy, 9, 3.5) & chao
        img.pintar(ralo, "inox", 0.3)
        img.pintar(ralo & (((X - cx) % 3) == 0), "grafite", 0.05, achatar=False)
    mancha_tinta = chao & (ruido(largura, altura, 22, 10, 3513) > 0.9)
    img.pintar(mancha_tinta, "ciano", 0.1 + 0.08 * fino, achatar=False)
    mancha_magenta = chao & (ruido(largura, altura, 26, 12, 3514) > 0.92)
    img.pintar(mancha_magenta, "neon_magenta", 0.1 + 0.08 * fino, achatar=False)
    img.cor(chao & (Y == y0), SOMBRA)
    img.chao = chao
    return img


def piso_cinema(largura, altura, x_soleira, y0=112, luzes=()):
    """O saguão tem carpete de veludo com um desenho de estrelas; a partir de
    x_soleira o carpete é o escuro da sala de projeção (com um batente de latão
    na divisa, se ela cair no meio da imagem), e 'luzes' são as linhas de luz de
    balizamento no sentido da profundidade (os corredores entre as poltronas).
    O saguão é x_soleira = largura; a sala, x_soleira = 0."""
    img = Imagem(largura, altura)
    X, Y = img.X, img.Y
    chao = Y >= y0
    fino = ciclico(largura, altura, 2, 2, 3520)
    manchas = ruido(largura, altura, 60, 20, 3521)
    sala = X >= x_soleira
    v = (0.3 + 0.1 * manchas + 0.05 * fino) * LUZ - 0.16 * np.clip((20 - (Y - y0)) / 20, 0, 1)
    img.pintar(chao & ~sala, "veludo", v + 0.1)
    estrela = (((X % 24) == 12) & (((Y - y0) % 24) == 12)) | (((X % 24) == 11) & (((Y - y0) % 24) == 12)) | (((X % 24) == 13) & (((Y - y0) % 24) == 12)) | (((X % 24) == 12) & ((((Y - y0) % 24) == 11) | (((Y - y0) % 24) == 13)))
    img.pintar(chao & ~sala & estrela, "neon_ambar", 0.34, achatar=False)
    img.pintar(chao & sala, "veludo", v - 0.06)
    img.pintar(chao & sala & (((X + Y) % 8) == 0), "veludo", 0.12, achatar=False)
    for x in luzes:
        img.pintar(img.ret(x, y0 + 4, x + 2, altura - 4) & chao & (((Y // 6) % 2) == 0), "neon_violeta", 0.5, achatar=False)
    if 0 < x_soleira < largura:
        soleira = img.ret(x_soleira - 3, y0, x_soleira + 3, altura) & chao
        img.pintar(soleira, "neon_ambar", 0.38 + 0.2 * (X == x_soleira - 3))
    img.cor(chao & (Y == y0), SOMBRA)
    img.chao = chao
    return img


# ---------------------------------------------------------------------------
# As salas montadas
# ---------------------------------------------------------------------------

SALAS = {
    "loja_uni": {"tema": "loja_uni", "largura": 560, "altura": 240, "pecas": [
        "PORTA:azul", ("u_prateleira", 1), ("u_cabides", 2), ("u_brasao", 3), ("u_prateleira", 11), ("u_provador", 5), ("u_espelho", 4)]},
    "grafica": {"tema": "grafica", "largura": 560, "altura": 240, "pecas": [
        "PORTA:limao", ("g_escaninhos", 1), ("g_painel", 5), ("g_tintas", 3), ("g_cartazes", 2), ("g_rolos", 4), ("g_nicho", 6)]},
    "cinema": {"tema": "cinema", "largura": 640, "altura": 320, "pecas": [
        "PORTA:violeta", ("c_cartazes", 1), ("c_cardapio", 2), ("c_planta", 7), ("c_cartazes_b", 9), ("c_nicho", 4),
        ("c_relogio", 8), ("c_arco_sala", 3)]},
    "sala_cinema": {"tema": "sala_cinema", "largura": 480, "altura": 320, "pecas": [
        "PORTA:violeta|SAÍDA", ("s_painel", 5), "TELA", "TELA", "TELA", "PORTA:ciano|CABINE"]},
    "cabine": {"tema": "cabine", "largura": 400, "altura": 220, "pecas": [
        "PORTA:ciano", ("p_janela", 1), ("p_horarios", 2), ("p_rolos", 3), ("p_uniforme", 4)]},
}

FUNCOES = {
    "u_prateleira": u_prateleira, "u_cabides": u_cabides, "u_brasao": u_brasao, "u_espelho": u_espelho, "u_provador": u_provador,
    "g_escaninhos": g_escaninhos, "g_painel": g_painel, "g_tintas": g_tintas, "g_cartazes": g_cartazes, "g_rolos": g_rolos,
    "g_nicho": g_nicho, "c_cartazes": c_cartazes, "c_cardapio": c_cardapio, "c_nicho": c_nicho, "c_arco_sala": c_arco_sala,
    "c_planta": c_planta, "c_relogio": c_relogio, "c_cartazes_b": lambda semente: c_cartazes(semente, 1),
    "s_painel": s_painel, "p_janela": p_janela, "p_horarios": p_horarios, "p_rolos": p_rolos, "p_uniforme": p_uniforme,
}

PISOS = {
    "loja_uni": piso_loja_uni, "grafica": piso_grafica, "cabine": piso_cabine,
    "cinema": lambda largura, altura: piso_cinema(largura, altura, largura),
    "sala_cinema": lambda largura, altura: piso_cinema(largura, altura, 0, luzes=(180, 380)),
}


def placa_da_porta(peca, texto, cor):
    """A plaquinha de neon com o nome da sala, em cima da porta (o quadro da
    porta começa em y = 24, e a placa fica em y de 13 a 22)."""
    X, Y = peca.X, peca.Y
    rampa = base.NEON[cor]
    largura_texto = base.largura_do_texto(texto, 8)
    x0 = 40 - largura_texto // 2 - 3
    peca.pintar(peca.ret(x0, 12, x0 + largura_texto + 6, 22), "grafite", 0.07)
    peca.pintar(peca.ret(x0, 12, x0 + largura_texto + 6, 13), rampa, 0.4, achatar=False)
    peca.pintar(peca.ret(x0, 21, x0 + largura_texto + 6, 22), rampa, 0.4, achatar=False)
    base.escrever(peca, x0 + 3, 13, texto, rampa, 0.92, 8)


def montar_fundo(nome):
    import gerar_porta_restaurante as porta
    sala = SALAS[nome]
    tema = sala["tema"]
    img = Imagem(sala["largura"], sala["altura"])
    tela = tela_larga()
    parte_da_tela = 0
    for coluna, item in enumerate(sala["pecas"]):
        if isinstance(item, str) and item.startswith("PORTA:"):
            cor_porta, _, rotulo = item.split(":")[1].partition("|")
            peca = porta.peca_de_parede(parede(tema, 70 + coluna), cor_porta)
            if rotulo:
                placa_da_porta(peca, rotulo, cor_porta)
        elif item == "TELA":
            peca = Imagem(L, H)
            peca.px[:] = tela.px[:, parte_da_tela * L:(parte_da_tela + 1) * L]
            parte_da_tela += 1
        else:
            funcao, semente = item
            peca = FUNCOES[funcao](semente)
        img.colar(peca, coluna * L, 0)
    piso = PISOS[nome](sala["largura"], sala["altura"])
    img.px[piso.chao] = piso.px[piso.chao]
    portas = [(coluna * L + 10, 24, coluna * L + 70, H) for coluna, item in enumerate(sala["pecas"])
              if isinstance(item, str) and item.startswith("PORTA:")]
    return img, base.camada_emissiva(img, portas)
