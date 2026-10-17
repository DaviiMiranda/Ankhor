# gerar_andar2_objetos.py — desenha, por código, os OBJETOS do segundo andar do
# Centro de Convivência: o corredor do mezanino, a Loja Universitária, a
# Gráfica Quântica e o Cine Andrômeda (docs/fases/centro_de_convivencia.md,
# seção 7).
#
# Como rodar (Python 3 + numpy + Pillow):
#
#   python assets/modelagem/cenario/gerar_andar2_objetos.py
#
# O que sai (em assets/sprites/cenario/praca/objetos/<objeto>.png): cada objeto
# é um sprite que o Gabriel contorna (y-sort), com o "pé" (o ponto do chão)
# e a pegada (a caixa de colisão no chão) em OBJETOS, no fim deste arquivo, do
# mesmo jeito do gerar_praca_objetos.py. A TELA do cinema é um sprite animado:
# sai como uma folha de 4 quadros (tela_cinema_folha.png) mais o SpriteFrames
# (tela_cinema_quadros.tres). O COFRE (fechado e aberto) não é um objeto
# comum: é o sistema cenas/sistemas/cofre.tscn, e os sprites saem em
# assets/sprites/cenario/objetos/ (cofre.png e cofre_aberto.png).
# Com CATALOGO=1 monta uma folha com os objetos. Não commitar.

import math
import os

import numpy as np

import gerar_praca_base as base
import gerar_praca_objetos as go

Imagem, RAMPAS, dilatar = base.Imagem, base.RAMPAS, base.dilatar
ruido = base.ruido
ciclico = base.ruido


def neon(img, mascara, rampa, valor=0.9):
    img.pintar(mascara, rampa, valor, achatar=False)


def caixa(img, x0, y0, x1, y1, rampa, tom=0.4):
    """Um bloco de material com o realce da luz (em cima e à esquerda) e a
    sombra (à direita e embaixo)."""
    X, Y = img.X, img.Y
    img.pintar(img.ret(x0, y0, x1, y1), rampa, tom + 0.16 * (Y == y0) + 0.1 * (X == x0) - 0.1 * (X == x1 - 1) - 0.08 * (Y == y1 - 1))


# ---------------------------------------------------------------------------
# O corredor do mezanino
# ---------------------------------------------------------------------------


def maquina_venda():
    """Máquina de venda: corpo de grafite, vitrine com quatro fileiras de
    embalagens coloridas, painel com a tela e os botões e a aba de entrega."""
    img = Imagem(32, 52)
    X, Y = img.X, img.Y
    caixa(img, 1, 2, 31, 50, "grafite", 0.3)
    img.pintar(img.ret(4, 8, 22, 40), "grafite", 0.05)
    cores = ("neon_azul", "neon_magenta", "neon_ambar", "neon_verde", "neon_vermelho")
    for fila in range(4):
        y = 12 + fila * 8
        img.pintar(img.ret(4, y + 5, 22, y + 6), "inox", 0.5)
        for k in range(4):
            img.pintar(img.ret(5 + k * 4, y + 1, 8 + k * 4, y + 5), cores[(k + fila * 2) % 5], 0.55)
    img.pintar(img.ret(24, 8, 29, 16), "grafite", 0.05)
    neon(img, img.ret(25, 9, 28, 11), "ciano", 0.9)
    for r in range(3):
        for c in range(2):
            img.pintar(img.ret(24 + c * 3, 19 + r * 4, 26 + c * 3, 21 + r * 4), "inox", 0.62)
    img.pintar(img.ret(6, 42, 22, 48), "grafite", 0.04)
    img.pintar(img.ret(6, 42, 22, 43), "inox", 0.6)
    neon(img, img.ret(3, 3, 29, 5), "ciano", 0.85)
    neon(img, img.ret(4, 8, 5, 40), "ciano", 0.3)
    img.contornar()
    return img, 16, 51


def banco_mirante():
    """Banco de ripas de madeira escura sobre uma viga de aço e dois pés, com
    um friso de luz por baixo."""
    img = Imagem(62, 28)
    X, Y = img.X, img.Y
    for k in range(4):
        y = 6 + k * 4
        img.pintar(img.ret(2, y, 60, y + 3), "madeira_fut", 0.46 + 0.12 * (k % 2) + 0.1 * (X < 8))
        img.pintar(img.ret(2, y, 60, y + 1), "madeira_fut", 0.7, achatar=False)
    caixa(img, 4, 20, 58, 23, "inox", 0.4)
    for x in (8, 48):
        caixa(img, x, 22, x + 5, 27, "inox", 0.34)
    neon(img, img.ret(8, 23, 54, 24), "ciano", 0.7)
    img.contornar()
    return img, 31, 27


def diretorio_holo():
    """Totem de informações: uma coluna de aço com a tela e, em cima, um
    mapa em holograma flutuando (um anel azul com três pontos)."""
    img = Imagem(26, 58)
    X, Y = img.X, img.Y
    img.pintar(img.elipse(13, 55, 11, 3), "inox", 0.34)
    caixa(img, 7, 22, 19, 54, "inox", 0.38)
    img.pintar(img.ret(9, 27, 17, 40), "grafite", 0.05)
    neon(img, img.ret(10, 29, 16, 30), "neon_azul", 0.85)
    neon(img, img.ret(10, 33, 14, 34), "neon_azul", 0.55)
    neon(img, img.ret(10, 36, 16, 37), "neon_azul", 0.4)
    img.cor(img.ret(12, 44, 14, 46), base.hexa("#6cf28e")[0])
    neon(img, img.elipse(13, 20, 3, 1.4), "ciano", 0.95)
    cone = img.poligono([(11, 20), (15, 20), (22, 4), (4, 4)]) & (((X + Y) % 2) == 0)
    neon(img, cone, "neon_azul", 0.2 + 0.2 * (1 - Y / 20.0))
    anel = (np.abs(((X + 0.5 - 13) / 8.0) ** 2 + ((Y + 0.5 - 7) / 2.5) ** 2 - 1.0) < 0.35)
    neon(img, anel, "neon_azul", 0.9)
    for (x, y, c) in ((8, 7, "neon_limao"), (16, 6, "neon_violeta"), (13, 9, "neon_azul")):
        neon(img, img.ret(x, y, x + 1, y + 1), c, 1.0)
    img.contornar()
    return img, 13, 56


def carrinho_limpeza():
    """Carrinho de limpeza abandonado: caixa de plástico azul com o balde, o
    esfregão encostado e duas rodinhas, uma delas quebrada."""
    img = Imagem(40, 34)
    X, Y = img.X, img.Y
    caixa(img, 4, 12, 30, 28, "neon_azul", 0.24)
    img.pintar(img.ret(5, 18, 29, 19), "carpete", 0.2)
    caixa(img, 6, 6, 18, 12, "inox", 0.5)
    img.pintar(img.ret(7, 7, 17, 9), "grafite", 0.08)
    img.pintar(img.caminho([(30, 26), (36, 4)], 0.9), "madeira_fut", 0.6)
    img.pintar(img.poligono([(33, 4), (39, 4), (40, 9), (33, 9)]), "papel_branco", 0.6)
    img.pintar(img.ret(22, 4, 28, 12), "neon_limao", 0.4)
    img.pintar(img.elipse(9, 30, 3, 3), "grafite", 0.1)
    img.pintar(img.elipse(25, 31, 3, 2), "grafite", 0.1)
    img.pintar(img.ret(10, 28, 11, 31), "inox", 0.3)
    img.contornar()
    return img, 17, 32


def jardineira():
    """Jardineira comprida de aço, com folhagem que brilha e flores
    bioluminescentes."""
    img = Imagem(72, 40)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(4010)
    caixa(img, 2, 26, 70, 38, "grafite", 0.34)
    img.pintar(img.ret(4, 28, 68, 29), "ciano", 0.3, achatar=False)
    img.pintar(img.ret(4, 24, 68, 27), "laje", 0.2)
    for k in range(16):
        x0 = 6 + k * 4 + rng.uniform(-1, 1)
        topo = 6 + float(rng.integers(0, 14))
        talo = img.caminho([(x0, 26), (x0 + rng.uniform(-2, 2), (26 + topo) / 2), (x0 + rng.uniform(-3, 3), topo)], 0.7)
        img.pintar(talo, "verde", 0.4 + 0.2 * rng.random())
        img.pintar(img.elipse(x0 + rng.uniform(-3, 3), topo, rng.uniform(2.5, 4.5), rng.uniform(2, 3.5)), "bioluz", 0.5 + 0.4 * rng.random())
    for x in (14, 34, 54):
        neon(img, img.elipse(x, 8 + (x % 5), 1.6, 1.6), "neon_violeta", 1.0)
    img.contornar()
    return img, 36, 37


def luminaria_chao():
    """Luminária de piso alta: haste fina de aço com a base redonda e um anel
    de luz no topo."""
    img = Imagem(18, 68)
    X, Y = img.X, img.Y
    img.pintar(img.elipse(9, 65, 7, 2.5), "inox", 0.4)
    img.pintar(img.ret(8, 12, 10, 64), "inox", 0.5 + 0.3 * (X == 8))
    img.pintar(img.elipse(9, 8, 7, 3), "grafite", 0.1)
    neon(img, img.elipse(9, 8, 6, 2.2) & ~img.elipse(9, 8, 4, 1.2), "ciano", 0.95)
    neon(img, img.elipse(9, 8, 3.5, 1.1), "ciano", 0.6)
    img.contornar()
    return img, 9, 66


def cadeira_espera():
    """Fileira de três cadeiras de casca presas a uma mesma viga de aço, vista
    de frente."""
    img = Imagem(66, 34)
    X, Y = img.X, img.Y
    caixa(img, 2, 22, 64, 25, "inox", 0.4)
    for x in (10, 54):
        caixa(img, x, 24, x + 3, 33, "inox", 0.34)
    for k in range(3):
        x0 = 4 + k * 20
        casca = img.poligono([(x0, 8), (x0 + 16, 8), (x0 + 18, 22), (x0 - 2, 22)])
        img.pintar(casca, "carpete", 0.4 + 0.2 * ((X - x0) < 4) + 0.1 * (Y < 11))
        img.pintar(img.ret(x0 + 1, 15, x0 + 15, 21), "carpete", 0.28)
        neon(img, img.ret(x0 + 2, 9, x0 + 14, 10), "neon_azul", 0.7)
    img.contornar()
    return img, 33, 33


# ---------------------------------------------------------------------------
# Loja Universitária
# ---------------------------------------------------------------------------


def arara(variante=0):
    """Arara de roupas: dois postes e uma barra com peças penduradas (jaquetas
    e moletons nas cores da universidade)."""
    img = Imagem(60, 58)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(4100 + variante)
    cores = (("neon_azul", "papel_branco", "carpete", "neon_azul"), ("papel_branco", "carpete", "neon_azul", "grafite"))[variante]
    img.pintar(img.ret(6, 8, 8, 54), "inox", 0.5 + 0.3 * (X == 6))
    img.pintar(img.ret(52, 8, 54, 54), "inox", 0.5 + 0.3 * (X == 52))
    img.pintar(img.ret(4, 8, 56, 10), "inox", 0.62 + 0.2 * (Y == 8))
    for x in (2, 50):
        caixa(img, x, 53, x + 10, 56, "inox", 0.34)
    for k in range(9):
        x0 = 10 + k * 5
        rampa = cores[int(rng.integers(0, len(cores)))]
        comp = int(rng.integers(22, 34))
        img.pintar(img.ret(x0 + 1, 10, x0 + 2, 13), "inox", 0.7)
        img.pintar(img.poligono([(x0 - 1, 15), (x0 + 1.5, 12), (x0 + 4, 15), (x0 + 5, 15 + comp), (x0 - 2, 15 + comp)]), rampa, 0.42 + 0.14 * (k % 2) + 0.1 * ((X - x0) < 1))
    img.contornar()
    return img, 30, 57


def manequim_uni():
    """Manequim de loja com a jaqueta azul e o cachecol, sobre a base de aço."""
    img = Imagem(26, 62)
    X, Y = img.X, img.Y
    cx = 13
    img.pintar(img.elipse(cx, 59, 9, 2.5), "inox", 0.34)
    img.pintar(img.ret(cx - 1, 40, cx + 1, 58), "inox", 0.5)
    img.pintar(img.elipse(cx, 6, 3.6, 4.2), "papel_branco", 0.74 - 0.18 * ((X - cx) > 1))
    img.pintar(img.ret(cx - 1, 10, cx + 1, 14), "papel_branco", 0.56)
    tronco = img.poligono([(cx - 9, 14), (cx + 9, 14), (cx + 6, 40), (cx - 6, 40)])
    img.pintar(tronco, "neon_azul", 0.34 + 0.22 * ((X - cx) < -3))
    img.pintar(tronco & (np.abs(Y - 26) < 1.2), "papel_branco", 0.8, achatar=False)
    img.pintar(img.ret(cx - 4, 12, cx + 5, 16), "neon_limao", 0.5)
    for lado in (-1, 1):
        img.pintar(img.caminho([(cx + lado * 9, 15), (cx + lado * 11, 34)], 1.2), "neon_azul", 0.28)
    img.pintar(tronco & (X == cx), "carpete", 0.2, achatar=False)
    img.contornar()
    return img, 13, 60


def balcao_caixa_uni():
    """Balcão do caixa: tampo branco, frente de carpete azul com o friso de
    neon, a registradora holográfica e um mostruário de chaveiros."""
    img = Imagem(88, 50)
    X, Y = img.X, img.Y
    caixa(img, 2, 20, 86, 48, "carpete", 0.34)
    img.pintar(img.ret(2, 20, 86, 25), "papel_branco", 0.72 + 0.2 * (Y == 20))
    neon(img, img.ret(6, 34, 82, 35), "neon_azul", 0.85)
    img.pintar(img.ret(4, 40, 84, 41), "carpete", 0.14, achatar=False)
    caixa(img, 60, 12, 78, 20, "inox", 0.4)
    img.pintar(img.ret(62, 13, 76, 19), "grafite", 0.06)
    neon(img, img.ret(63, 14, 75, 15), "neon_azul", 0.9)
    neon(img, img.ret(63, 16, 70, 17), "neon_azul", 0.6)
    cone = img.poligono([(66, 12), (72, 12), (80, 0), (58, 0)]) & (((X + Y) % 2) == 0)
    neon(img, cone, "neon_azul", 0.22)
    for k in range(5):
        img.pintar(img.ret(8 + k * 5, 10, 11 + k * 5, 20), ("neon_azul", "papel_branco", "carpete", "neon_limao", "neon_azul")[k], 0.5)
        img.pintar(img.ret(9 + k * 5, 8, 10 + k * 5, 10), "inox", 0.7)
    img.pintar(img.ret(36, 14, 52, 20), "papel_branco", 0.62)
    img.pintar(img.ret(38, 16, 50, 17), "carpete", 0.3, achatar=False)
    img.contornar()
    return img, 44, 48


def estante_moletons():
    """Estante solta de três andares com pilhas de moletons e camisetas
    dobradas, vista de frente."""
    img = Imagem(60, 56)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(4120)
    img.pintar(img.ret(3, 4, 57, 52), "inox", 0.16)
    caixa(img, 2, 4, 5, 54, "inox", 0.42)
    caixa(img, 55, 4, 58, 54, "inox", 0.34)
    cores = ("neon_azul", "papel_branco", "carpete", "grafite", "neon_azul")
    for y_base_prat in (20, 36, 52):
        img.pintar(img.ret(3, y_base_prat, 57, y_base_prat + 2), "inox", 0.5 + 0.2 * (Y == y_base_prat))
        x = 6
        while x < 50:
            larg = int(rng.integers(8, 13))
            for k in range(int(rng.integers(2, 4))):
                topo = y_base_prat - (k + 1) * 5
                rampa = cores[int(rng.integers(0, len(cores)))]
                img.pintar(img.ret(x, topo, x + larg, topo + 5), rampa, 0.44 + 0.12 * (k % 2) + 0.12 * (X == x))
                img.pintar(img.ret(x, topo, x + larg, topo + 1), rampa, 0.72, achatar=False)
            x += larg + int(rng.integers(1, 3))
    img.contornar()
    return img, 30, 55


def mesa_dobrados():
    """Mesa de exposição com pilhas de camisetas dobradas e uma etiqueta."""
    img = Imagem(56, 34)
    X, Y = img.X, img.Y
    caixa(img, 2, 18, 54, 22, "papel_branco", 0.66)
    for x in (6, 46):
        caixa(img, x, 22, x + 3, 33, "inox", 0.36)
    for (x0, n, rampa) in ((6, 4, "neon_azul"), (20, 3, "papel_branco"), (34, 4, "carpete")):
        for k in range(n):
            img.pintar(img.ret(x0, 17 - (k + 1) * 4, x0 + 13, 17 - k * 4), rampa, 0.42 + 0.12 * (k % 2))
            img.pintar(img.ret(x0, 17 - (k + 1) * 4, x0 + 13, 18 - (k + 1) * 4 + 1), rampa, 0.72, achatar=False)
    img.pintar(img.ret(48, 14, 53, 18), "neon_limao", 0.6)
    img.contornar()
    return img, 28, 33


def cesto_promocao():
    """Cesto de aramado com bonés e cachecóis em promoção e uma etiqueta."""
    img = Imagem(32, 28)
    X, Y = img.X, img.Y
    img.pintar(img.poligono([(3, 12), (29, 12), (26, 26), (6, 26)]), "inox", 0.3)
    img.pintar(img.poligono([(3, 12), (29, 12), (26, 26), (6, 26)]) & ((((X + Y) % 4) == 0) | (((X - Y) % 4) == 0)), "inox", 0.6, achatar=False)
    for (x, cor) in ((8, "neon_azul"), (14, "papel_branco"), (20, "carpete"), (11, "neon_limao"), (24, "neon_azul")):
        img.pintar(img.elipse(x + 2, 11, 4, 3), cor, 0.5)
        img.pintar(img.ret(x - 1, 11, x + 6, 12), cor, 0.3)
    caixa(img, 12, 2, 22, 8, "neon_ambar", 0.4)
    img.pintar(img.ret(13, 4, 21, 5), "grafite", 0.1)
    img.contornar()
    return img, 16, 26


def espelho_standing():
    """Espelho de pé numa moldura de aço, levemente inclinado, com o reflexo
    em diagonal."""
    img = Imagem(30, 64)
    X, Y = img.X, img.Y
    img.pintar(img.caminho([(7, 62), (15, 52)], 0.9), "inox", 0.4)
    img.pintar(img.caminho([(23, 62), (15, 52)], 0.9), "inox", 0.4)
    caixa(img, 6, 2, 24, 54, "inox", 0.46)
    vidro = img.ret(8, 4, 22, 52)
    img.pintar(vidro, "gelo", 0.3 + 0.12 * ((Y - 4) / 48.0))
    reflexo = vidro & ((np.abs((X - Y) + 10) < 2) | (np.abs((X - Y) + 22) < 1))
    img.pintar(reflexo, "gelo", 0.74, achatar=False)
    img.contornar()
    return img, 15, 62


# ---------------------------------------------------------------------------
# Gráfica Quântica
# ---------------------------------------------------------------------------


def plotter_grande():
    """Plotter de impressão em grande formato: o corpo largo de aço sobre o
    pedestal de duas pernas, a tela, os LEDs de tinta (C, M, Y) e a folha
    larga saindo e se enrolando no chão."""
    img = Imagem(88, 62)
    X, Y = img.X, img.Y
    for x in (10, 72):
        caixa(img, x, 34, x + 5, 56, "inox", 0.36)
        caixa(img, x - 3, 56, x + 8, 59, "inox", 0.3)
    caixa(img, 4, 8, 84, 34, "inox", 0.36)
    img.pintar(img.ret(6, 10, 82, 14), "grafite", 0.14)
    img.pintar(img.ret(8, 17, 58, 30), "grafite", 0.06)
    img.pintar(img.ret(10, 28, 56, 30), "grafite", 0.02)
    caixa(img, 62, 17, 80, 30, "grafite", 0.12)
    img.pintar(img.ret(64, 19, 78, 25), "grafite", 0.04)
    neon(img, img.ret(65, 20, 77, 21), "neon_limao", 0.9)
    neon(img, img.ret(65, 22, 72, 23), "neon_limao", 0.55)
    for k, cor in enumerate(("ciano", "neon_magenta", "neon_ambar")):
        neon(img, img.ret(64 + k * 5, 27, 67 + k * 5, 29), cor, 0.95)
    img.pintar(img.ret(10, 34, 78, 37), "papel_branco", 0.8 + 0.1 * (Y == 34))
    folha = img.poligono([(12, 37), (76, 37), (74, 50), (80, 58), (60, 61), (14, 61), (8, 54), (14, 48)])
    img.pintar(folha, "papel_branco", 0.74 - 0.16 * (Y > 52) + 0.05 * ((X // 6) % 2))
    for y in (42, 46, 50):
        img.pintar(img.ret(18, y, 18 + 10 + (y % 14) * 3, y + 1), "ciano" if y == 42 else "neon_magenta", 0.4, achatar=False)
    img.contornar()
    return img, 44, 60


def copiadora():
    """Copiadora grande: tampa articulada em cima, painel de controle, a
    gaveta de papel e a linha de luz do escâner."""
    img = Imagem(48, 56)
    X, Y = img.X, img.Y
    caixa(img, 3, 22, 45, 52, "ceramica", 0.44)
    caixa(img, 1, 10, 47, 22, "ceramica", 0.54)
    img.pintar(img.ret(4, 12, 44, 14), "grafite", 0.1)
    img.pintar(img.ret(5, 15, 43, 20), "gelo", 0.3)
    neon(img, img.ret(5, 17, 43, 18), "neon_verde", 0.85)
    caixa(img, 30, 24, 43, 32, "grafite", 0.1)
    neon(img, img.ret(32, 26, 41, 27), "ciano", 0.9)
    for k in range(3):
        img.pintar(img.ret(32 + k * 4, 29, 34 + k * 4, 31), "inox", 0.6)
    for y in (36, 44):
        caixa(img, 6, y, 40, y + 6, "ceramica", 0.34)
        img.pintar(img.ret(18, y + 2, 28, y + 3), "grafite", 0.1)
    img.pintar(img.ret(14, 4, 34, 10), "papel_branco", 0.8)
    img.pintar(img.ret(14, 4, 34, 5), "papel_branco", 0.9, achatar=False)
    for x in (6, 38):
        img.pintar(img.ret(x, 52, x + 4, 56), "grafite", 0.1)
    img.contornar()
    return img, 24, 55


def guilhotina():
    """Guilhotina de papel sobre a mesa baixa: a base com a régua marcada, a
    lâmina e a alavanca comprida."""
    img = Imagem(52, 40)
    X, Y = img.X, img.Y
    for x in (6, 42):
        caixa(img, x, 24, x + 4, 39, "inox", 0.34)
    caixa(img, 2, 18, 50, 25, "inox", 0.42)
    img.pintar(img.ret(4, 20, 48, 22), "papel_branco", 0.7)
    for x in range(6, 48, 4):
        img.pintar(img.ret(x, 20, x + 1, 22), "grafite", 0.1, achatar=False)
    img.pintar(img.ret(8, 14, 40, 18), "papel_branco", 0.86)
    img.pintar(img.poligono([(6, 18), (42, 10), (44, 12), (6, 20)]), "inox", 0.74)
    img.pintar(img.caminho([(42, 11), (48, 2)], 1.4), "neon_limao", 0.5)
    img.pintar(img.elipse(48, 2, 2.4, 2.4), "grafite", 0.1)
    neon(img, img.ret(14, 21, 30, 22), "neon_limao", 0.7)
    img.contornar()
    return img, 26, 38


def impressora_3d():
    """Impressora 3D de bancada: uma gaiola de vidro com o cabeçote e uma peça
    pela metade brilhando em verde-limão."""
    img = Imagem(40, 56)
    X, Y = img.X, img.Y
    caixa(img, 2, 40, 38, 54, "grafite", 0.3)
    neon(img, img.ret(6, 47, 34, 48), "neon_limao", 0.7)
    cara = img.ret(4, 6, 36, 40)
    img.pintar(cara, "grafite", 0.06)
    img.pintar(cara & (((X + Y) % 2) == 0), "gelo", 0.22)
    for x in (4, 35):
        caixa(img, x, 4, x + 2, 42, "inox", 0.5)
    caixa(img, 4, 4, 36, 7, "inox", 0.5)
    img.pintar(img.ret(10, 12, 30, 14), "inox", 0.6)
    caixa(img, 17, 11, 25, 17, "grafite", 0.18)
    neon(img, img.ret(20, 17, 22, 21), "neon_limao", 1.0)
    peca = img.poligono([(12, 38), (28, 38), (26, 28), (14, 28)])
    neon(img, peca, "neon_limao", 0.62)
    neon(img, peca & (Y % 3 == 0), "neon_limao", 0.9)
    img.pintar(img.ret(10, 38, 30, 40), "inox", 0.4)
    img.contornar()
    return img, 20, 55


def estante_resmas():
    """Estante de aço com pilhas de resmas de papel embrulhadas e algumas
    caixas de papel colorido."""
    img = Imagem(58, 60)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(4200)
    img.pintar(img.ret(3, 4, 55, 56), "inox", 0.14)
    caixa(img, 2, 3, 5, 58, "inox", 0.44)
    caixa(img, 53, 3, 56, 58, "inox", 0.34)
    for y_base_prat in (22, 40, 58):
        img.pintar(img.ret(3, y_base_prat - 1, 55, y_base_prat + 1), "inox", 0.5 + 0.2 * (Y == y_base_prat - 1))
        x = 7
        while x < 48:
            larg = int(rng.integers(9, 14))
            n = int(rng.integers(2, 4))
            rampa = ("papel_branco", "papel_branco", "ciano", "neon_magenta", "neon_ambar")[int(rng.integers(0, 5))]
            for k in range(n):
                topo = y_base_prat - 1 - (k + 1) * 5
                img.pintar(img.ret(x, topo, x + larg, topo + 5), "papel_branco", 0.74 + 0.08 * (k % 2))
                img.pintar(img.ret(x, topo + 2, x + larg, topo + 3), rampa, 0.5, achatar=False)
            x += larg + int(rng.integers(1, 3))
    img.contornar()
    return img, 29, 59


def mesa_corte():
    """Mesa grande de corte com o tapete verde riscado, réguas e pilhas de
    papel."""
    img = Imagem(88, 36)
    X, Y = img.X, img.Y
    for x in (6, 76):
        caixa(img, x, 22, x + 5, 35, "inox", 0.34)
    caixa(img, 2, 12, 86, 24, "grafite", 0.3)
    tapete = img.ret(4, 8, 84, 20)
    img.pintar(tapete, "verde", 0.34 + 0.06 * (Y == 8))
    img.pintar(tapete & ((((X - 4) % 8) == 0) | (((Y - 8) % 6) == 0)), "verde", 0.62, achatar=False)
    img.pintar(img.ret(10, 4, 34, 10), "papel_branco", 0.8)
    img.pintar(img.ret(10, 4, 34, 5), "papel_branco", 0.92, achatar=False)
    img.pintar(img.ret(40, 6, 62, 10), "papel_branco", 0.74)
    img.pintar(img.ret(66, 2, 78, 10), "ciano", 0.5)
    img.pintar(img.ret(66, 2, 78, 3), "ciano", 0.8, achatar=False)
    img.pintar(img.ret(6, 18, 82, 20), "inox", 0.6)
    img.contornar()
    return img, 44, 34


def balcao_grafica():
    """Balcão de atendimento da gráfica: tampo claro, frente de aço com o friso
    limão, a tela de senhas holográfica e uma pilha de folhetos."""
    img = Imagem(88, 50)
    X, Y = img.X, img.Y
    caixa(img, 2, 20, 86, 48, "inox", 0.34)
    img.pintar(img.ret(2, 20, 86, 25), "papel_branco", 0.68 + 0.2 * (Y == 20))
    neon(img, img.ret(6, 34, 82, 35), "neon_limao", 0.82)
    for x in range(8, 84, 12):
        img.pintar(img.ret(x, 38, x + 8, 44), "grafite", 0.12)
    caixa(img, 8, 10, 28, 20, "grafite", 0.12)
    neon(img, img.ret(10, 12, 26, 13), "neon_limao", 0.9)
    base.escrever(img, 11, 14, "A 041", "neon_limao", 0.9, 8)
    cone = img.poligono([(14, 10), (22, 10), (30, -2), (6, -2)]) & (((X + Y) % 2) == 0)
    neon(img, cone, "neon_limao", 0.2)
    for k in range(4):
        img.pintar(img.ret(60, 15 - k * 2, 74, 17 - k * 2), "papel_branco", 0.74 + 0.08 * (k % 2))
        img.pintar(img.ret(60, 15 - k * 2, 74, 16 - k * 2), ("ciano", "neon_magenta", "neon_ambar", "neon_limao")[k], 0.5, achatar=False)
    img.contornar()
    return img, 44, 48


def rolo_papel():
    """Rolo grande de papel em pé, sobre uma base de aço com o eixo no meio."""
    img = Imagem(26, 42)
    X, Y = img.X, img.Y
    cx = 13
    img.pintar(img.elipse(cx, 39, 11, 2.6), "inox", 0.32)
    rolo = img.ret(3, 6, 23, 38)
    img.pintar(rolo, "papel_branco", go.tom_cilindro(img, 3, 23) * 0.7 + 0.2)
    img.pintar(img.elipse(cx, 6, 10, 3), "papel_branco", 0.82)
    img.pintar(img.elipse(cx, 6, 4.5, 1.6), "grafite", 0.06)
    img.pintar(img.ret(3, 36, 23, 38), "papel_branco", 0.4)
    img.pintar(img.ret(cx - 1, 0, cx + 1, 6), "inox", 0.6)
    img.contornar()
    return img, cx, 40


# ---------------------------------------------------------------------------
# Cine Andrômeda
# ---------------------------------------------------------------------------


def bilheteria_balcao():
    """Cabine de bilheteria: o guichê de vidro com a luz violeta, o balcão com a
    ranhura, o letreiro de holograma e o toldo listrado."""
    img = Imagem(68, 62)
    X, Y = img.X, img.Y
    caixa(img, 2, 36, 66, 60, "veludo", 0.3)
    img.pintar(img.ret(2, 36, 66, 40), "neon_ambar", 0.46 + 0.2 * (Y == 36))
    neon(img, img.ret(6, 50, 62, 51), "neon_violeta", 0.8)
    vidro = img.ret(8, 10, 60, 36)
    img.pintar(vidro, "grafite", 0.07)
    img.pintar(vidro, "neon_violeta", 0.12 + 0.18 * (1 - (Y - 10) / 26.0))
    reflexo = vidro & ((np.abs((X - Y) + 6) < 2) | (np.abs((X - Y) + 20) < 1))
    img.pintar(reflexo, "gelo", 0.55, achatar=False)
    img.pintar(img.ret(22, 30, 46, 33), "inox", 0.14)
    for x in (6, 60):
        caixa(img, x, 8, x + 3, 38, "inox", 0.46)
    toldo = img.ret(2, 2, 66, 10)
    listra = (((X // 6) % 2) == 0)
    img.pintar(toldo & listra, "neon_violeta", 0.5)
    img.pintar(toldo & ~listra, "grafite", 0.2)
    img.pintar(img.ret(2, 2, 66, 3), "inox", 0.6)
    img.pintar(img.ret(2, 9, 66, 10) & ((X % 6) < 4), "grafite", 0.1)
    base.escrever(img, 34 - base.largura_do_texto("INGRESSOS", 8) // 2, 16, "INGRESSOS", "neon_violeta", 0.95, 8)
    img.contornar()
    return img, 34, 60


def balcao_pipoca():
    """Bomboniere: balcão listrado de vermelho e branco com a máquina de pipoca
    (cabine de vidro com pipoca estourando e a luz âmbar), a estufa e a pilha
    de baldes."""
    img = Imagem(104, 62)
    X, Y = img.X, img.Y
    caixa(img, 2, 30, 102, 60, "grafite", 0.28)
    listra = (((X // 6) % 2) == 0)
    faixa = img.ret(2, 36, 102, 56)
    img.pintar(faixa & listra, "neon_vermelho", 0.42)
    img.pintar(faixa & ~listra, "papel_branco", 0.66)
    img.pintar(img.ret(2, 30, 102, 35), "inox", 0.6 + 0.2 * (Y == 30))
    neon(img, img.ret(4, 57, 100, 58), "neon_ambar", 0.7)
    caixa(img, 8, 6, 40, 30, "inox", 0.34)
    cabine = img.ret(11, 9, 37, 28)
    img.pintar(cabine, "grafite", 0.06)
    neon(img, cabine & (Y > 18), "neon_ambar", 0.22)
    rng = np.random.default_rng(4300)
    for _ in range(46):
        x, y = int(rng.integers(12, 36)), int(rng.integers(12, 28))
        img.pintar(img.ret(x, y, x + 2, y + 2), "papel_branco", 0.8 if rng.random() > 0.3 else 0.6, achatar=False)
    neon(img, img.ret(10, 7, 38, 9), "neon_ambar", 0.95)
    neon(img, img.elipse(24, 4, 4, 2), "neon_vermelho", 0.8)
    caixa(img, 48, 14, 72, 30, "inox", 0.3)
    img.pintar(img.ret(50, 16, 70, 28), "grafite", 0.06)
    neon(img, img.ret(50, 16, 70, 17), "neon_ambar", 0.7)
    for x in range(52, 70, 5):
        img.pintar(img.ret(x, 20, x + 3, 28), "papel_branco", 0.6)
    for k, x in enumerate((80, 90)):
        for j in range(4):
            balde = img.poligono([(x, 12 + j * 4), (x + 8, 12 + j * 4), (x + 7, 17 + j * 4), (x + 1, 17 + j * 4)])
            img.pintar(balde & (((X - x) // 2) % 2 == 0), "neon_vermelho", 0.46)
            img.pintar(balde & (((X - x) // 2) % 2 == 1), "papel_branco", 0.7)
    img.contornar()
    return img, 52, 60


def poltronas(quantas=4):
    """Fileira de poltronas de cinema vista de TRÁS (de frente para a tela):
    encostos altos de veludo com a borda de latão, o número da poltrona e os
    porta-copos entre elas."""
    largura = quantas * 19 + 4
    img = Imagem(largura, 40)
    X, Y = img.X, img.Y
    for k in range(quantas):
        x0 = 2 + k * 19
        encosto = img.poligono([(x0 + 1, 8), (x0 + 16, 8), (x0 + 17, 34), (x0, 34)])
        img.pintar(encosto, "veludo", 0.34 + 0.24 * ((X - x0) < 5) + 0.08 * (Y < 12))
        img.pintar(img.elipse(x0 + 8.5, 9, 8, 4), "veludo", 0.5 + 0.16 * ((X - x0) < 6))
        neon(img, img.ret(x0 + 2, 8, x0 + 15, 9), "neon_ambar", 0.4)
        img.pintar(img.ret(x0 + 5, 20, x0 + 12, 24), "grafite", 0.06)
        base.escrever(img, x0 + 6, 21, str((k * 3 + 7) % 9 + 1), "neon_ambar", 0.5, 8)
        img.pintar(img.ret(x0 + 1, 33, x0 + 16, 36), "grafite", 0.1)
        if k:
            img.pintar(img.ret(x0 - 3, 26, x0, 28), "inox", 0.5)
    img.pintar(img.ret(0, 36, largura, 40), "veludo", 0.12)
    img.contornar()
    return img, largura // 2, 38


def standee_filme():
    """Cartaz de papelão recortado em pé: a figura do filme, o título e as
    lâmpadas da marquise em volta, sobre uma base de aço."""
    img = Imagem(32, 66)
    X, Y = img.X, img.Y
    img.pintar(img.ret(6, 60, 26, 64), "inox", 0.34)
    caixa(img, 4, 4, 28, 60, "grafite", 0.14)
    quadro = img.ret(6, 6, 26, 56)
    img.pintar(quadro, "neon_violeta", 0.2 + 0.3 * (1 - (Y - 6) / 50.0))
    img.pintar(img.elipse(16, 22, 7, 7), "neon_ambar", 0.7 + 0.2 * ((X - 16) < 0))
    img.pintar(img.poligono([(9, 56), (11, 36), (16, 31), (21, 36), (23, 56)]) & quadro, "grafite", 0.05)
    img.pintar(img.elipse(16, 30, 3, 3.5) & quadro, "grafite", 0.05)
    img.pintar(img.ret(8, 50, 24, 54), "grafite", 0.05)
    neon(img, img.ret(10, 51, 22, 52), "neon_violeta", 0.9)
    for y in range(8, 58, 6):
        neon(img, img.ret(4, y, 5, y + 1), "neon_ambar", 1.0 if (y // 6) % 2 else 0.5)
        neon(img, img.ret(27, y, 28, y + 1), "neon_ambar", 0.5 if (y // 6) % 2 else 1.0)
    img.contornar()
    return img, 16, 63


def cordao_fila():
    """Dois postes de aço com o cordão de veludo âmbar entre eles, para
    organizar a fila."""
    img = Imagem(60, 30)
    X, Y = img.X, img.Y
    for x in (6, 52):
        img.pintar(img.elipse(x, 27, 5, 2), "inox", 0.4)
        img.pintar(img.ret(x - 1, 8, x + 1, 27), "inox", 0.5 + 0.3 * (X == x - 1))
        img.pintar(img.elipse(x, 7, 3, 3), "neon_ambar", 0.6)
    corda = [(6, 8), (18, 15), (30, 18), (42, 15), (52, 8)]
    mascara = img.caminho(corda, 1.1)
    img.pintar(mascara, "veludo", 0.6)
    neon(img, img.caminho(corda, 0.5), "veludo", 0.9)
    img.contornar()
    return img, 30, 28


# ---------------------------------------------------------------------------
# A tela do cinema (animada)
# ---------------------------------------------------------------------------

LARGURA_TELA, ALTURA_TELA = 230, 78
QUADROS_TELA = 4


def quadro_tela(k):
    """Um quadro da tela: as barras de teste de uma transmissão sem sinal (as
    cores deslocam uma barra a cada quadro), com chiado em linhas e uma faixa
    clara que sobe, como um cinescópio velho."""
    img = Imagem(LARGURA_TELA, ALTURA_TELA)
    X, Y = img.X, img.Y
    cores = ("papel_branco", "neon_ambar", "ciano", "neon_verde", "neon_magenta", "neon_vermelho", "neon_azul")
    largura_barra = LARGURA_TELA / 7.0
    idx = ((X / largura_barra).astype(int) + k) % 7
    for i, rampa in enumerate(cores):
        img.pintar((idx == i) & (Y < ALTURA_TELA - 18), rampa, 0.46 + 0.1 * (Y % 2 == 0))
    img.pintar(Y >= ALTURA_TELA - 18, "grafite", 0.08)
    for i in range(7):
        img.pintar((idx == (i + 3) % 7) & (Y >= ALTURA_TELA - 18) & (Y < ALTURA_TELA - 12), cores[(i + 2) % 7], 0.3)
    rng = np.random.default_rng(4400 + k)
    chiado = rng.random((ALTURA_TELA, LARGURA_TELA)) < 0.08
    img.pintar(chiado, "papel_branco", 0.7, achatar=False)
    img.pintar((Y % 3) == 0, "grafite", 0.04, achatar=False)
    y_faixa = (k * 21 + 6) % ALTURA_TELA
    faixa = np.abs(Y - y_faixa) < 4
    img.pintar(faixa, "papel_branco", 0.58, achatar=False)
    base.escrever(img, LARGURA_TELA // 2 - base.largura_do_texto("SEM SINAL", 16) // 2, 22, "SEM SINAL", "grafite", 0.04, 16)
    img.pintar(img.ret(0, 0, LARGURA_TELA, 1), "papel_branco", 0.2, achatar=False)
    img.px[..., 3] = 255
    return img


def gravar_tela_cinema():
    pasta = os.path.join(base.PASTA_PRACA, "objetos")
    os.makedirs(pasta, exist_ok=True)
    quadros = [quadro_tela(k) for k in range(QUADROS_TELA)]
    folha = np.zeros((ALTURA_TELA, LARGURA_TELA * QUADROS_TELA, 4), dtype=np.uint8)
    for i, q in enumerate(quadros):
        folha[:, i * LARGURA_TELA:(i + 1) * LARGURA_TELA] = q.px
    base.bib.salvar_png(os.path.join(pasta, "tela_cinema_folha.png"), folha)
    linhas = ['[gd_resource type="SpriteFrames" format=3]', "",
              '[ext_resource type="Texture2D" path="res://assets/sprites/cenario/praca/objetos/tela_cinema_folha.png" id="1_folha"]', ""]
    for i in range(QUADROS_TELA):
        linhas += [f'[sub_resource type="AtlasTexture" id="Quadro{i}"]', 'atlas = ExtResource("1_folha")',
                   f"region = Rect2({i * LARGURA_TELA}, 0, {LARGURA_TELA}, {ALTURA_TELA})", ""]
    linhas += ["[resource]", "animations = [{", '"frames": [{']
    itens = [f'"duration": 1.0,\n"texture": SubResource("Quadro{i}")' for i in range(QUADROS_TELA)]
    linhas.append("}, {\n".join(itens) + "\n}],")
    linhas += ['"loop": true,', '"name": &"chiado",', '"speed": 5.0', "}]", ""]
    with open(os.path.join(pasta, "tela_cinema_quadros.tres"), "w", encoding="utf-8", newline="\n") as arquivo:
        arquivo.write("\n".join(linhas))
    return quadros


# ---------------------------------------------------------------------------
# O cofre (puzzle do cinema)
# ---------------------------------------------------------------------------


def cofre(aberto=False):
    """Cofre de aço compacto: corpo grafite com o topo chanfrado, a porta com a
    roda de abrir, o teclado com três dígitos de luz ciano, as dobradiças e um
    LED (vermelho trancado, verde aberto). Aberto, a porta vira uma lâmina
    fina de lado e aparece o vão escuro com uma prateleira."""
    img = Imagem(40, 48)
    X, Y = img.X, img.Y
    for x in (4, 31):
        caixa(img, x, 44, x + 5, 47, "inox", 0.3)
    caixa(img, 2, 4, 38, 44, "grafite", 0.34)
    img.pintar(img.ret(2, 4, 38, 7), "inox", 0.46 + 0.2 * (Y == 4))
    vao = img.ret(5, 9, 35, 41)
    if not aberto:
        caixa(img, 5, 9, 35, 41, "inox", 0.3)
        placa = img.ret(8, 12, 32, 38)
        img.pintar(placa, "grafite", 0.24 + 0.1 * (Y < 16) + 0.06 * (X < 11))
        d = np.hypot(X + 0.5 - 17, Y + 0.5 - 26)
        img.pintar((d < 7) & (d >= 5), "inox", 0.62)
        img.pintar(d < 5, "grafite", 0.12)
        img.pintar(d < 2, "inox", 0.7)
        for ang in (0, 90):
            a = math.radians(ang)
            img.pintar(img.linha(17 - 6 * math.cos(a), 26 - 6 * math.sin(a), 17 + 6 * math.cos(a), 26 + 6 * math.sin(a), 0.6) & (d < 6.5), "inox", 0.62)
        img.pintar(img.ret(23, 13, 32, 22), "grafite", 0.03)
        for k in range(3):
            neon(img, img.ret(24 + k * 3, 16, 26 + k * 3, 19), "ciano", 0.95)
        img.cor(img.ret(30, 23, 31, 24), base.hexa("#ff5a3a")[0])
        img.pintar(img.ret(23, 30, 32, 31), "inox", 0.22)
    else:
        prof = np.clip((X - 5) / 30.0, 0, 1)
        img.pintar(vao, "grafite", 0.03 + 0.05 * (1 - prof))
        img.pintar(img.ret(6, 25, 34, 27), "inox", 0.4)
        img.pintar(img.ret(6, 25, 34, 26), "inox", 0.62, achatar=False)
        neon(img, img.ret(10, 30, 12, 31), "ciano", 0.6)
        img.pintar(img.ret(5, 9, 11, 41), "inox", 0.34 + 0.2 * (X == 5))
        img.pintar(img.ret(7, 11, 10, 39), "grafite", 0.2)
        img.pintar(img.ret(8, 24, 9, 30), "inox", 0.7)
        img.cor(img.ret(30, 11, 31, 12), base.hexa("#6cf28e")[0])
    for y in (14, 33):
        img.pintar(img.ret(3, y, 5, y + 4), "inox", 0.7)
    img.contornar()
    return img, 20, 46


OBJETOS = {
    # mezanino
    "maquina_venda": (maquina_venda, (26, 6)),
    "banco_mirante": (banco_mirante, (54, 6)),
    "diretorio_holo": (diretorio_holo, (12, 5)),
    "carrinho_limpeza": (carrinho_limpeza, (34, 6)),
    "jardineira": (jardineira, (66, 7)),
    "luminaria_chao": (luminaria_chao, (8, 4)),
    "cadeira_espera": (cadeira_espera, (58, 6)),
    # loja universitária
    "arara_a": (lambda: arara(0), (52, 6)),
    "arara_b": (lambda: arara(1), (52, 6)),
    "manequim_uni": (manequim_uni, (14, 5)),
    "balcao_caixa_uni": (balcao_caixa_uni, (84, 8)),
    "estante_moletons": (estante_moletons, (54, 7)),
    "mesa_dobrados": (mesa_dobrados, (50, 6)),
    "cesto_promocao": (cesto_promocao, (26, 5)),
    "espelho_standing": (espelho_standing, (14, 4)),
    # gráfica quântica
    "plotter_grande": (plotter_grande, (80, 9)),
    "copiadora": (copiadora, (42, 7)),
    "guilhotina": (guilhotina, (46, 7)),
    "impressora_3d": (impressora_3d, (34, 7)),
    "estante_resmas": (estante_resmas, (52, 7)),
    "mesa_corte": (mesa_corte, (82, 8)),
    "balcao_grafica": (balcao_grafica, (84, 8)),
    "rolo_papel": (rolo_papel, (18, 5)),
    # cine andrômeda
    "bilheteria_balcao": (bilheteria_balcao, (62, 8)),
    "balcao_pipoca": (balcao_pipoca, (98, 8)),
    "poltronas_4": (lambda: poltronas(4), (72, 7)),
    "poltronas_3": (lambda: poltronas(3), (54, 7)),
    "standee_filme": (standee_filme, (20, 5)),
    "cordao_fila": (cordao_fila, (52, 4)),
}


def main():
    print("Gerando os objetos do segundo andar em assets/sprites/cenario/praca/objetos")
    objetos = {}
    for nome, (f, pegada) in OBJETOS.items():
        img, px, py = f()
        base.salvar(img, f"{nome}.png", "objetos")
        print(f"    {nome}: pé em ({px}, {py}) -> offset = Vector2({-px}, {-py}), pegada {pegada}")
        objetos[nome] = img
    pasta_cofre = os.path.join(base.PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")
    for nome, aberto in (("cofre", False), ("cofre_aberto", True)):
        img, px, py = cofre(aberto)
        img.salvar(f"{nome}.png", pasta_cofre)
        print(f"    {nome}: pé em ({px}, {py}) -> offset = Vector2({-px}, {-py})")
        objetos[nome] = img
    quadros = gravar_tela_cinema()
    objetos["tela_cinema_0"] = quadros[0]
    base.salvar_catalogo("andar2_objetos", list(objetos.items()), 6, 2)


if __name__ == "__main__":
    main()
