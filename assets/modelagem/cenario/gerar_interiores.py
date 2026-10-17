# gerar_interiores.py — desenha, por código, o FUNDO de cada restaurante do
# Centro de Convivência e o da passarela: a parede (112 px em cima) e o piso.
# Ver o cabeçalho de gerar_restaurantes.py para a ideia de cada sala.
#
# Este arquivo não gera nada sozinho: o gerar_restaurantes.py chama as funções
# daqui e grava os fundos em assets/sprites/cenario/praca/fundo_<sala>.png.
#
# Como a parede é montada: uma fileira de peças de 80 px, cada uma com um
# DETALHE (cardápio de holograma, prateleira, passa-pratos, quadro...), sobre
# uma base de materiais do restaurante (madeira e azulejo, tijolo, aço...).
# As portas (de vidro, com a folha que corre) são coladas por cima, na peça
# da porta, pelo gerar_porta_restaurante.peca_de_parede.

import math

import numpy as np

import gerar_praca_base as base

Imagem, RAMPAS, SOMBRA, dilatar = base.Imagem, base.RAMPAS, base.SOMBRA, base.dilatar
ruido = base.ruido
ciclico = base.ruido_ciclico
L = base.PECA
H = base.ALTURA_PAREDE
LUZ = 0.8


TEMAS = {
    "loja_1": {"neon": "ambar", "alto": "madeira_fut", "baixo": "azulejo_branco"},
    "loja_2": {"neon": "verde", "alto": "verde_agua", "baixo": "xadrez_claro"},
    "camara": {"neon": "ciano", "alto": "gelo", "baixo": "inox"},
    "loja_3": {"neon": "vermelho", "alto": "tijolo", "baixo": "azulejo_branco"},
    "loja_4": {"neon": "magenta", "alto": "grafite", "baixo": "couro"},
    "passarela": {"neon": "ciano", "alto": "grafite", "baixo": "inox"},
}


# ---------------------------------------------------------------------------
# Base da parede
# ---------------------------------------------------------------------------


def teto(img, rampa_neon, fino):
    img.pintar(img.ret(0, 0, L, 12), "grafite", 0.2 + 0.08 * fino + 0.16 * (img.Y == 11))
    img.pintar(img.ret(0, 7, L, 9), "grafite", 0.07)
    img.pintar(img.ret(2, 7, L - 2, 8), rampa_neon, 0.32, achatar=False)


def rodape(img, fino):
    img.pintar(img.ret(0, 100, L, H), "grafite", 0.22 + 0.08 * fino + 0.14 * (img.Y == 100))
    for x in range(10, L - 8, 20):
        img.pintar(img.ret(x, 104, x + 8, 108), "grafite", 0.07)


def parede_tema(tema, semente=0):
    """Os materiais da parede de cada restaurante. O que está EM CIMA (y de 12
    a 62) e o que está EMBAIXO (y de 64 a 100, o lambri), separados por um
    friso de neon da cor do restaurante."""
    t = TEMAS[tema]
    neon = base.NEON[t["neon"]]
    img = Imagem(L, H)
    X, Y = img.X, img.Y
    fino = ciclico(L, H, 2, 2, 1000 + semente)
    manchas = ciclico(L, H, 40, 16, 1001 + semente)
    alto = img.ret(0, 12, L, 62)
    baixo = img.ret(0, 64, L, 100)
    if tema == "loja_1":
        ripas = (X % 5) == 0
        v = (0.5 + 0.14 * manchas + 0.05 * fino) * LUZ
        img.pintar(alto, "madeira_fut", v - 0.08 * ripas)
        img.pintar(alto & (X % 5 == 1), "madeira_fut", v + 0.12, achatar=False)
    elif tema == "loja_2":
        v = (0.46 + 0.14 * manchas + 0.05 * fino) * LUZ
        img.pintar(alto, "verde_agua", v)
        img.pintar(alto & ((X % 40) == 0), "verde_agua", v - 0.22, achatar=False)
        img.pintar(alto & ((X % 40) == 1), "verde_agua", v + 0.14, achatar=False)
    elif tema == "camara":
        v = (0.5 + 0.12 * manchas + 0.05 * fino) * LUZ
        img.pintar(alto, "gelo", v)
        img.pintar(alto & ((X % 40) == 0), "gelo", v - 0.3, achatar=False)
        for x in (3, 37, 43, 77):
            for y in (16, 58):
                img.pintar(img.ret(x, y, x + 2, y + 2), "inox", 0.72)
    elif tema == "loja_3":
        fileira = (Y - 12) // 6
        desloc = 8 * (fileira % 2)
        tijolo = alto & (((X + desloc) % 16) != 0) & (((Y - 12) % 6) != 0)
        sorteio = np.random.default_rng(1010 + semente).random((20, 12))
        tom = sorteio[np.clip(fileira, 0, 19), ((X + desloc) // 16) % 12]
        img.pintar(alto, "tijolo", 0.12)
        img.pintar(tijolo, "tijolo", (0.5 + 0.28 * tom + 0.08 * manchas) * LUZ)
    elif tema == "loja_4":
        v = (0.34 + 0.1 * manchas + 0.04 * fino) * LUZ
        img.pintar(alto, "grafite", v)
        hexa = (((X + 10 * ((Y // 10) % 2)) % 20) == 0) | ((Y % 10) == 0)
        img.pintar(alto & hexa, "grafite", v - 0.18, achatar=False)
    else:
        v = (0.4 + 0.14 * manchas + 0.05 * fino) * LUZ
        img.pintar(alto, "grafite", v)
        img.pintar(alto & ((X % 40) == 0), "grafite", v - 0.2, achatar=False)
    # Friso de neon entre o de cima e o lambri.
    img.pintar(img.ret(0, 62, L, 64), "grafite", 0.1)
    img.pintar(img.ret(0, 62, L, 63), neon, 0.55, achatar=False)
    # O lambri.
    if tema in ("loja_1", "loja_3"):
        tom = (0.7 + 0.1 * manchas + 0.04 * fino) * LUZ
        altura_azulejo, largura_azulejo = (8, 16) if tema == "loja_1" else (10, 10)
        desloc = (largura_azulejo // 2) * (((Y - 64) // altura_azulejo) % 2) if tema == "loja_1" else 0
        img.pintar(baixo, "azulejo_branco", tom)
        rejunte = baixo & ((((Y - 64) % altura_azulejo) == 0) | (((X + desloc) % largura_azulejo) == 0))
        img.pintar(rejunte, "azulejo_branco", tom - 0.3, achatar=False)
    elif tema == "loja_2":
        xadrez = (((X // 8) + ((Y - 64) // 8)) % 2) == 0
        img.pintar(baixo & xadrez, "xadrez_claro", 0.6 * LUZ + 0.08 * manchas)
        img.pintar(baixo & ~xadrez, "xadrez_escuro", 0.5 * LUZ + 0.08 * manchas)
    elif tema == "camara":
        img.pintar(baixo, "inox", (0.44 + 0.1 * manchas) * LUZ)
        img.pintar(baixo & ((X % 20) == 0), "inox", 0.14, achatar=False)
        for x in range(4, L, 20):
            img.pintar(img.ret(x + 3, 70, x + 13, 72), "inox", 0.12)
            img.pintar(img.ret(x + 3, 74, x + 13, 76), "inox", 0.12)
    elif tema == "loja_4":
        img.pintar(baixo, "couro", (0.4 + 0.1 * manchas) * LUZ)
        losango = (((X + (Y - 64)) % 14) == 0) | (((X - (Y - 64)) % 14) == 0)
        img.pintar(baixo & losango, "couro", 0.14, achatar=False)
        img.pintar(baixo & (((X % 14) == 7) & (((Y - 64) % 14) == 7)), neon, 0.5, achatar=False)
    else:
        img.pintar(baixo, "inox", (0.4 + 0.1 * manchas) * LUZ)
        img.pintar(baixo & ((X % 40) == 0), "inox", 0.14, achatar=False)
    img.pintar(img.ret(0, 100, L, 101), "grafite", 0.1)
    teto(img, neon, fino)
    rodape(img, fino)
    img.fino, img.manchas, img.neon = fino, manchas, neon
    return img


# ---------------------------------------------------------------------------
# Detalhes da parede (cada um devolve uma peça de 80 x 112)
# ---------------------------------------------------------------------------


def moldura(img, x0, y0, x1, y1, rampa="inox", tom=0.45):
    img.pintar(img.ret(x0, y0, x1, y1), rampa, tom + 0.16 * (img.Y == y0) + 0.1 * (img.X == x0) - 0.1 * (img.X == x1 - 1))


def lisa(tema, semente=0):
    return parede_tema(tema, semente)


def cardapio_holo(tema, semente=1):
    """Cardápio em holograma: moldura de aço, fundo escuro e uma lista de
    pratos (linhas curtas e preços) na cor do restaurante, com um ícone."""
    img = parede_tema(tema, semente)
    X, Y = img.X, img.Y
    neon = img.neon
    moldura(img, 10, 22, 70, 94)
    tela = img.ret(13, 25, 67, 91)
    img.pintar(tela, "grafite", 0.05 + 0.04 * (Y % 3 == 0))
    img.pintar(img.ret(17, 29, 63, 31), neon, 0.82, achatar=False)
    rng = np.random.default_rng(1100 + semente)
    for k in range(6):
        y = 37 + k * 9
        comp = int(rng.integers(16, 30))
        img.pintar(img.ret(17, y, 17 + comp, y + 2), neon, 0.55, achatar=False)
        img.pintar(img.ret(52, y, 52 + int(rng.integers(5, 11)), y + 2), neon, 0.8, achatar=False)
        if k % 2 == 0:
            img.pintar(img.ret(17, y + 3, 17 + comp // 2, y + 4), neon, 0.28, achatar=False)
    img.pintar(img.ret(13, 25, 67, 26), neon, 0.22, achatar=False)
    return img


CORES_PRATELEIRA = {
    "loja_1": ("neon_ambar", "ceramica", "neon_verde", "madeira_fut"),
    "loja_2": ("neon_verde", "verde_agua", "ceramica", "neon_ambar"),
    "camara": ("gelo", "gelo", "inox", "neon_verde"),
    "loja_3": ("neon_vermelho", "neon_ambar", "neon_verde", "ceramica"),
    "loja_4": ("neon_magenta", "neon_violeta", "ciano", "neon_ambar"),
    "passarela": ("inox", "gelo", "ciano", "grafite"),
}


def prateleira(tema, semente=2):
    """Duas prateleiras com potes, latas e caixas nas cores do restaurante."""
    img = parede_tema(tema, semente)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(1200 + semente)
    cores = CORES_PRATELEIRA[tema]
    img.pintar(img.ret(6, 18, 74, 96), "inox", 0.12)
    for y in (46, 74, 94):
        img.pintar(img.ret(6, y, 74, y + 3), "inox", 0.5 + 0.2 * (Y == y))
    for linha, (y_base_prat, alt_max) in enumerate(((46, 22), (74, 22))):
        x = 9
        while x < 68:
            larg = int(rng.integers(5, 9))
            alt = int(rng.integers(10, alt_max))
            rampa = cores[int(rng.integers(0, len(cores)))]
            pote = img.ret(x, y_base_prat - alt, x + larg, y_base_prat)
            img.pintar(pote, rampa, 0.4 + 0.18 * (X == x) + 0.2 * rng.random())
            if tema in ("loja_1", "loja_2"):
                img.pintar(img.ret(x + 1, y_base_prat - alt - 3, x + larg - 1, y_base_prat - alt), "inox", 0.55)
            img.pintar(img.ret(x + 1, y_base_prat - alt + 3, x + larg - 1, y_base_prat - alt + 6), "ceramica", 0.7)
            x += larg + int(rng.integers(1, 4))
    return img


def passa_pratos(tema, semente=3):
    """Abertura para a cozinha: balcão de aço, a luz da cozinha lá dentro
    (na cor do restaurante), utensílios pendurados e uma campainha."""
    img = parede_tema(tema, semente)
    X, Y = img.X, img.Y
    neon = img.neon
    moldura(img, 8, 20, 72, 80, "inox", 0.4)
    vao = img.ret(11, 23, 69, 77)
    prof = np.clip((Y - 23) / 54.0, 0, 1)
    img.pintar(vao, "grafite", 0.1)
    img.pintar(vao, neon, 0.12 + 0.2 * (1 - prof) ** 1.3)
    for x in (20, 30, 42, 54, 62):
        img.pintar(img.ret(x, 23, x + 1, 36 + (x % 7)), "inox", 0.5)
        img.pintar(img.ret(x - 2, 36 + (x % 7), x + 3, 40 + (x % 7)), "inox", 0.62)
    img.pintar(img.ret(11, 60, 69, 66), "grafite", 0.06)
    img.pintar(img.ret(20, 56, 28, 66), "inox", 0.3)
    img.pintar(img.ret(46, 52, 60, 66), "inox", 0.25)
    img.pintar(img.ret(6, 77, 74, 84), "inox", 0.55 + 0.22 * (Y == 77))
    img.pintar(img.elipse(40, 76, 3, 2), "inox", 0.8)
    img.pintar(img.ret(40, 73, 41, 76), neon, 0.9, achatar=False)
    return img


def quadro_holo(tema, semente=4):
    """Pôster em holograma (círculo e onda), como o das fachadas."""
    img = parede_tema(tema, semente)
    X, Y = img.X, img.Y
    neon = img.neon
    moldura(img, 20, 20, 60, 70)
    tela = img.ret(22, 22, 58, 68)
    img.pintar(tela, "grafite", 0.06)
    img.pintar(img.elipse(40, 40, 9, 9) & tela, neon, 0.5)
    img.pintar(img.elipse(40, 40, 5, 5) & tela, neon, 0.88, achatar=False)
    onda = (np.abs(Y + 0.5 - (58 + 3 * np.sin((X - 24) / 3.0))) < 1.1) & (X > 23) & (X < 57)
    img.pintar(onda, neon, 0.8, achatar=False)
    img.pintar(img.ret(26, 63, 54, 64), neon, 0.35, achatar=False)
    return img


def janela_para_praca(tema, semente=5):
    """Janela larga para a praça: vidro escuro com o céu e a luz da praça."""
    img = parede_tema(tema, semente)
    X, Y = img.X, img.Y
    neon = img.neon
    moldura(img, 6, 20, 74, 90, "inox", 0.4)
    vidro = img.ret(9, 23, 71, 87)
    img.pintar(vidro, "grafite", 0.07)
    noite = np.array(base.kit.NOITE)
    prof = np.clip((Y - 23) / 64.0, 0, 1)
    indice = np.clip(np.floor((0.2 + 0.55 * prof) * len(noite) + img.limiar), 0, len(noite) - 1).astype(int)
    img.px[vidro] = noite[indice][vidro]
    rng = np.random.default_rng(1300 + semente)
    for _ in range(14):
        ex, ey = int(rng.integers(10, 70)), int(rng.integers(24, 60))
        img.px[ey, ex] = base.kit.ESTRELA[0]
    img.pintar(img.ret(40, 22, 41, 88), "inox", 0.4)
    reflexo = vidro & ((np.abs((X - Y) + 30) < 1.5) | (np.abs((X - Y) + 14) < 0.8))
    img.pintar(reflexo, "gelo", 0.6, achatar=False)
    img.pintar(img.ret(6, 90, 74, 94), "inox", 0.5 + 0.2 * (Y == 90))
    return img


def planta_de_parede(tema, semente=6):
    """Floreira com plantas bioluminescentes, trepadeira subindo a parede."""
    img = parede_tema(tema, semente)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(1400 + semente)
    img.pintar(img.ret(12, 80, 68, 100), "grafite", 0.3 + 0.14 * (Y == 80))
    img.pintar(img.ret(14, 82, 66, 99), "laje", 0.24)
    for k in range(8):
        x0 = 18 + k * 6 + int(rng.integers(-1, 2))
        topo = 44 + int(rng.integers(0, 28))
        talo = img.caminho([(x0, 84), (x0 + rng.uniform(-3, 3), (84 + topo) / 2), (x0 + rng.uniform(-5, 5), topo)], 0.7)
        img.pintar(talo, "verde", 0.4 + 0.2 * rng.random())
        folha = img.elipse(x0 + rng.uniform(-4, 4), topo, rng.uniform(3, 6), rng.uniform(2, 4))
        img.pintar(folha, "bioluz", 0.55 + 0.35 * rng.random())
    cipo = img.caminho([(60 + 2 * math.sin(k * 0.8), 24 + k * 8) for k in range(8)], 0.6)
    img.pintar(cipo, "verde", 0.3 + 0.3 * img.fino)
    return img


def garrafas(tema, semente=7):
    """O fundo do bar: prateleiras iluminadas por trás, garrafas que brilham."""
    img = parede_tema(tema, semente)
    X, Y = img.X, img.Y
    neon = img.neon
    rng = np.random.default_rng(1500 + semente)
    img.pintar(img.ret(6, 18, 74, 96), "grafite", 0.05)
    cores = ("neon_magenta", "neon_violeta", "ciano", "neon_ambar", "neon_verde")
    for y in (38, 60, 82):
        img.pintar(img.ret(6, y, 74, y + 3), "inox", 0.45 + 0.2 * (Y == y))
        img.pintar(img.ret(8, y - 2, 72, y), neon, 0.2, achatar=False)
        x = 9
        while x < 68:
            larg = int(rng.integers(4, 8))
            alt = int(rng.integers(12, 20))
            rampa = cores[int(rng.integers(0, len(cores)))]
            img.pintar(img.ret(x, y - alt, x + larg, y), rampa, 0.42 + 0.2 * (X == x) + 0.18 * rng.random())
            img.pintar(img.ret(x + 1, y - alt - 4, x + larg - 1, y - alt), rampa, 0.3)
            img.pintar(img.ret(x + 1, y - alt + 2, x + 2, y - 3), "ceramica", 0.85, achatar=False)
            x += larg + int(rng.integers(1, 4))
    return img


def quadro_eletrico(tema, semente=8):
    """Parede com a caixa de disjuntores da cozinha (a do Painel de Comutação
    fica na frente, como objeto): eletrodutos e a fiação grossa descendo."""
    img = parede_tema(tema, semente)
    X, Y = img.X, img.Y
    neon = img.neon
    moldura(img, 14, 18, 66, 76, "inox", 0.32)
    img.pintar(img.ret(17, 21, 63, 73), "grafite", 0.08)
    for k in range(4):
        img.pintar(img.ret(20 + k * 11, 26, 28 + k * 11, 40), "inox", 0.22)
        img.pintar(img.ret(23 + k * 11, 29 + (k % 2) * 5, 25 + k * 11, 33 + (k % 2) * 5), neon, 0.5 + 0.2 * (k % 2))
    for x in range(20, 62, 4):
        img.cor(img.ret(x, 52, x + 1, 53), (base.hexa("#6cf28e")[0], base.hexa("#ffc24a")[0], base.hexa("#ff5a3a")[0])[(x // 4) % 3])
    for x in (30, 40, 50):
        img.pintar(img.caminho([(x, 76), (x + 2 * math.sin(x), 90), (x - 3, 104)], 1.1), "inox", 0.2)
    return img


def duto_e_coifa(tema, semente=9):
    """Coifa de aço sobre o fogão, com o duto subindo e uma luz de trabalho."""
    img = parede_tema(tema, semente)
    X, Y = img.X, img.Y
    neon = img.neon
    img.pintar(img.poligono([(18, 56), (62, 56), (56, 36), (24, 36)]), "inox", 0.4 + 0.2 * ((X < 40) & (Y < 46)))
    img.pintar(img.ret(32, 12, 48, 36), "inox", 0.34 + 0.16 * (X < 36))
    for x in range(22, 60, 5):
        img.pintar(img.ret(x, 52, x + 3, 55), "grafite", 0.07)
    img.pintar(img.ret(20, 56, 60, 58), "inox", 0.6)
    img.pintar(img.ret(26, 59, 54, 61), neon, 0.7, achatar=False)
    img.pintar(img.ret(24, 62, 56, 80), neon, 0.12 + 0.1 * ((X + Y) % 4 == 0), achatar=False)
    return img


def escotilha(tema, semente=11):
    """A escotilha de manutenção por onde o Gabriel subiu: lacrada do lado
    de cá, com as faixas de perigo e a luz vermelha."""
    img = parede_tema(tema, semente)
    X, Y = img.X, img.Y
    moldura(img, 12, 40, 68, 108, "inox", 0.34)
    img.pintar(img.ret(16, 44, 64, 104), "inox", 0.26 + 0.1 * ciclico(L, H, 2, 2, 1450))
    for y in (52, 70, 88):
        img.pintar(img.ret(18, y, 62, y + 2), "inox", 0.14)
    for (x, y) in ((20, 48), (58, 48), (20, 98), (58, 98)):
        img.pintar(img.ret(x, y, x + 2, y + 2), "inox", 0.74)
    for x in range(14, 66, 8):
        img.pintar(img.poligono([(x, 108), (x + 4, 108), (x + 8, 104), (x + 4, 104)]), "neon_ambar", 0.75, achatar=False)
    img.pintar(img.ret(34, 36, 46, 40), "grafite", 0.06)
    img.cor(img.ret(38, 37, 42, 39), base.hexa("#ff5a3a")[0])
    img.pintar(img.ret(36, 70, 44, 74), "inox", 0.8)
    return img


def nicho_interior(tema, semente=12):
    """Nicho de serviço: um vão escuro onde cabe uma pessoa, na parede."""
    img = parede_tema(tema, semente)
    X, Y = img.X, img.Y
    img.pintar(img.ret(18, 22, 62, 100), "inox", 0.4 + 0.2 * (Y == 22))
    vao = img.ret(21, 25, 59, 100)
    prof = np.clip((Y - 25) / 75.0, 0, 1)
    img.pintar(vao, "grafite", 0.03 + 0.05 * prof)
    img.pintar(img.ret(21, 25, 26, 100), "grafite", 0.14, achatar=False)
    img.pintar(img.ret(23, 27, 57, 28), img.neon, 0.2, achatar=False)
    return img


def extintor_e_aviso(tema, semente=10):
    img = parede_tema(tema, semente)
    X, Y = img.X, img.Y
    img.pintar(img.ret(28, 56, 40, 94), "neon_vermelho", 0.45 + 0.2 * (X == 28))
    img.pintar(img.ret(30, 50, 38, 56), "inox", 0.5)
    img.pintar(img.ret(34, 46, 36, 50), "inox", 0.7)
    img.pintar(img.ret(46, 40, 66, 56), "ceramica", 0.75)
    img.pintar(img.ret(48, 44, 64, 46), "neon_vermelho", 0.6)
    img.pintar(img.ret(48, 49, 60, 50), "grafite", 0.2)
    return img


# ---------------------------------------------------------------------------
# Pisos
# ---------------------------------------------------------------------------


def piso_madeira(largura, altura, y0=112):
    """Tábuas largas de madeira clara, de 16 px de altura, com juntas sorteadas
    e um tapete retangular no meio."""
    img = Imagem(largura, altura)
    X, Y = img.X, img.Y
    chao = Y >= y0
    fino = ciclico(largura, altura, 2, 2, 1600)
    manchas = ruido(largura, altura, 50, 20, 1601)
    fileira = (Y - y0) // 16
    rng = np.random.default_rng(1602)
    tabuas = rng.random((fileira.max() + 2, largura // 20 + 4))
    desloc = ((fileira * 53) % 70)
    seg = ((X + desloc) // 70)
    tom = tabuas[fileira, np.clip(seg, 0, tabuas.shape[1] - 1)]
    v = (0.36 + 0.2 * tom + 0.1 * manchas + 0.05 * fino) * LUZ - 0.2 * np.clip((20 - (Y - y0)) / 20, 0, 1)
    img.pintar(chao, "madeira_fut", v)
    junta = chao & (((Y - y0) % 16 == 0) | ((X + desloc) % 70 == 0))
    img.pintar(junta, "madeira_fut", v - 0.24, achatar=False)
    img.pintar(chao & ((Y - y0) % 16 == 1), "madeira_fut", v + 0.08, achatar=False)
    img.cor(chao & (Y == y0), SOMBRA)
    img.chao = chao
    return img


def piso_xadrez(largura, altura, y0=112):
    """Xadrez de 16 x 12 px, brilhante, com reflexos em diagonal da luz de
    cima e cacos de azulejo faltando."""
    img = Imagem(largura, altura)
    X, Y = img.X, img.Y
    chao = Y >= y0
    fino = ciclico(largura, altura, 2, 2, 1610)
    manchas = ruido(largura, altura, 60, 24, 1611)
    xad = (((X // 16) + ((Y - y0) // 12)) % 2) == 0
    v = (0.5 + 0.1 * manchas + 0.04 * fino) * LUZ
    img.pintar(chao & xad, "xadrez_claro", v)
    img.pintar(chao & ~xad, "xadrez_escuro", v)
    junta = chao & (((X % 16) == 0) | (((Y - y0) % 12) == 0))
    img.pintar(junta, "xadrez_escuro", 0.06, achatar=False)
    reflexo = chao & (np.abs(((X + 2 * Y) % 170) - 8) < 1.2)
    img.pintar(reflexo, "xadrez_claro", 0.9, achatar=False)
    img.cor(chao & (Y == y0), SOMBRA)
    img.chao = chao
    return img


def piso_grade(largura, altura, y0=112):
    """Piso de grade de aço com chapas, geada nos cantos e canaletas."""
    img = Imagem(largura, altura)
    X, Y = img.X, img.Y
    chao = Y >= y0
    fino = ciclico(largura, altura, 2, 2, 1620)
    manchas = ruido(largura, altura, 40, 20, 1621)
    img.pintar(chao, "inox", (0.3 + 0.1 * manchas + 0.04 * fino) * LUZ)
    chapa = chao & ((((X // 32) + ((Y - y0) // 16)) % 2) == 0)
    img.pintar(chapa, "inox", (0.42 + 0.1 * manchas) * LUZ)
    furos = chao & (((X % 4) == 1) & (((Y - y0) % 4) == 1)) & ~chapa
    img.pintar(furos, "grafite", 0.04)
    img.pintar(chao & (((X % 32) == 0) | (((Y - y0) % 16) == 0)), "inox", 0.12, achatar=False)
    gelo = chao & (ruido(largura, altura, 30, 14, 1622) > 0.76)
    img.pintar(gelo, "gelo", 0.22 + 0.26 * fino)
    img.cor(chao & (Y == y0), SOMBRA)
    img.chao = chao
    return img


def piso_ladrilho(largura, altura, y0=112):
    """Ladrilho vermelho de cozinha, 16 x 16, com rejunte escuro e manchas de
    gordura."""
    img = Imagem(largura, altura)
    X, Y = img.X, img.Y
    chao = Y >= y0
    fino = ciclico(largura, altura, 2, 2, 1630)
    manchas = ruido(largura, altura, 50, 20, 1631)
    sorteio = np.random.default_rng(1632).random(((altura // 16) + 3, (largura // 16) + 3))
    tom = sorteio[(Y - y0) // 16 + 1, X // 16]
    v = (0.38 + 0.22 * tom + 0.08 * manchas + 0.04 * fino) * LUZ
    img.pintar(chao, "tijolo", v)
    img.pintar(chao & (((X % 16) == 0) | (((Y - y0) % 16) == 0)), "tijolo", 0.06, achatar=False)
    img.pintar(chao & (((Y - y0) % 16) == 1) & ((X % 16) != 0), "tijolo", v + 0.1, achatar=False)
    gordura = chao & (ruido(largura, altura, 24, 12, 1633) > 0.86)
    img.pintar(gordura, "tijolo", 0.2 + 0.1 * fino)
    img.cor(chao & (Y == y0), SOMBRA)
    img.chao = chao
    return img


def piso_bar(largura, altura, y0=112):
    """Piso escuro polido com frisos de luz magenta no sentido da profundidade."""
    img = Imagem(largura, altura)
    X, Y = img.X, img.Y
    chao = Y >= y0
    fino = ciclico(largura, altura, 2, 2, 1640)
    manchas = ruido(largura, altura, 60, 24, 1641)
    placa = ((X // 32) + ((Y - y0) // 16)) % 2
    v = (0.3 + 0.08 * placa + 0.1 * manchas + 0.04 * fino) * LUZ
    img.pintar(chao, "grafite", v)
    img.pintar(chao & (((X % 32) == 0) | (((Y - y0) % 16) == 0)), "grafite", v - 0.16, achatar=False)
    friso = chao & ((X % 160) == 80) & (Y > y0 + 4) & (((Y // 8) % 3) != 0)
    img.pintar(friso, "neon_magenta", 0.4, achatar=False)
    reflexo = chao & (np.abs(((X - 2 * Y) % 230) - 9) < 1.0)
    img.pintar(reflexo, "grafite", 0.55, achatar=False)
    img.cor(chao & (Y == y0), SOMBRA)
    img.chao = chao
    return img


def piso_passarela(largura, altura, y0=112):
    """Chapas de aço da passarela, com frisos de luz ciano nas bordas."""
    img = Imagem(largura, altura)
    X, Y = img.X, img.Y
    chao = Y >= y0
    fino = ciclico(largura, altura, 2, 2, 1650)
    manchas = ruido(largura, altura, 50, 16, 1651)
    img.pintar(chao, "inox", (0.32 + 0.1 * manchas + 0.04 * fino) * LUZ)
    img.pintar(chao & (((X % 40) == 0) | (((Y - y0) % 20) == 0)), "inox", 0.12, achatar=False)
    img.pintar(chao & (((X % 40) == 1) | (((Y - y0) % 20) == 1)), "inox", 0.5, achatar=False)
    img.pintar(chao & (Y == y0 + 4) & ((X % 10) < 6), "ciano", 0.3, achatar=False)
    img.pintar(chao & (Y == altura - 6) & ((X % 10) < 6), "ciano", 0.3, achatar=False)
    img.cor(chao & (Y == y0), SOMBRA)
    img.chao = chao
    return img


PISOS = {
    "loja_1": piso_madeira,
    "loja_2": piso_xadrez,
    "camara": piso_grade,
    "loja_3": piso_ladrilho,
    "loja_4": piso_bar,
    "passarela": piso_passarela,
}


# ---------------------------------------------------------------------------
# As salas montadas
# ---------------------------------------------------------------------------

# Cada sala: tema, largura, altura e a lista de peças de 80 px, da esquerda
# para a direita. "PORTA:cor" é a porta de vidro; (nome, True) espelha a peça.
SALAS = {
    "loja_1": {"tema": "loja_1", "largura": 400, "altura": 240, "pecas": [
        "PORTA:ambar", ("cardapio_holo", 1), ("passa_pratos", 3), ("prateleira", 2), ("planta_de_parede", 6)]},
    "loja_2": {"tema": "loja_2", "largura": 640, "altura": 280, "pecas": [
        "PORTA:verde", ("cardapio_holo", 11), ("janela_para_praca", 5), ("prateleira", 12), ("nicho_interior", 14),
        ("quadro_holo", 4), "PORTA:ciano", ("planta_de_parede", 16)]},
    "camara": {"tema": "camara", "largura": 400, "altura": 240, "pecas": [
        "PORTA:ciano", ("prateleira", 21), ("lisa", 22), ("extintor_e_aviso", 23), ("lisa", 24)]},
    "loja_3": {"tema": "loja_3", "largura": 480, "altura": 260, "pecas": [
        "PORTA:vermelho", ("duto_e_coifa", 31), ("passa_pratos", 33), ("extintor_e_aviso", 38), ("prateleira", 32),
        ("quadro_holo", 34)]},
    "loja_4": {"tema": "loja_4", "largura": 640, "altura": 360, "pecas": [
        "PORTA:magenta", ("garrafas", 41), ("quadro_holo", 44), ("garrafas", 42), ("nicho_interior", 45), ("garrafas", 47),
        ("quadro_holo", 46), ("lisa", 48)]},
    "passarela": {"tema": "passarela", "largura": 640, "altura": 180, "pecas": [
        ("escotilha", 51), ("janela_para_praca", 52), ("quadro_holo", 53), ("janela_para_praca", 54), ("lisa", 55),
        ("janela_para_praca", 56), "PORTA:ciano", ("lisa", 57)]},
}

FUNCOES = {
    "lisa": lisa, "cardapio_holo": cardapio_holo, "prateleira": prateleira, "passa_pratos": passa_pratos,
    "quadro_holo": quadro_holo, "janela_para_praca": janela_para_praca, "planta_de_parede": planta_de_parede,
    "garrafas": garrafas, "quadro_eletrico": quadro_eletrico, "duto_e_coifa": duto_e_coifa,
    "extintor_e_aviso": extintor_e_aviso, "escotilha": escotilha, "nicho_interior": nicho_interior,
}


def montar_fundo(nome):
    import gerar_porta_restaurante as porta
    sala = SALAS[nome]
    tema = sala["tema"]
    img = Imagem(sala["largura"], sala["altura"])
    for coluna, item in enumerate(sala["pecas"]):
        if isinstance(item, str) and item.startswith("PORTA:"):
            peca = porta.peca_de_parede(parede_tema(tema, 70 + coluna), item.split(":")[1])
        else:
            funcao, semente = item
            peca = FUNCOES[funcao](tema, semente) if funcao != "lisa" else lisa(tema, semente)
        img.colar(peca, coluna * L, 0)
    piso = PISOS[tema](sala["largura"], sala["altura"])
    img.px[piso.chao] = piso.px[piso.chao]
    portas = [(coluna * L + 10, 24, coluna * L + 70, H) for coluna, item in enumerate(sala["pecas"])
              if isinstance(item, str) and item.startswith("PORTA:")]
    return img, base.camada_emissiva(img, portas)
