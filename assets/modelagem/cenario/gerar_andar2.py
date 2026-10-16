# gerar_andar2.py — desenha, por código, o SEGUNDO ANDAR (o mezanino) da praça de
# alimentação do Centro de Convivência (docs/fases/centro_de_convivencia.md,
# seção 7) e as peças novas da praça que levam até ele (as escadas).
#
# Como rodar (Python 3 + numpy + Pillow):
#
#   python assets/modelagem/cenario/gerar_andar2.py
#
# O que sai (em assets/sprites/cenario/praca/):
#   fundo_andar2.png          2000 x 640 px: a cúpula, as fachadas das três lojas,
#                             o piso do corredor e o vazio do andar de baixo
#   fundo_andar2_luz.png      só os pixels que brilham (neon, vitrines, frisos),
#                             que viram a luz do mezanino (ver gerar_praca_base.py)
#   corrimao_andar2.png       o corrimão de vidro, num sprite à parte que o Godot
#                             põe NA FRENTE do Gabriel (ele anda sempre atrás dele)
#   letreiros/letreiro_<loja>.png e _aceso.png   os letreiros das três lojas e do hall
#
# O fundo da praça (gerar_praca.py) também usa as escadas daqui.
# Com CATALOGO=1 monta folhas com as peças. Não commitar.
#
# ---------------------------------------------------------------------------
# A GEOMETRIA DO MEZANINO
# ---------------------------------------------------------------------------
#
# O desenho do Davi mostra um anel em volta do vazio da praça: o hall com a
# escada no meio de cima e as lojas na curva, com um corrimão na borda de
# dentro e o andar de baixo escuro. Na vista lateral, o anel é uma FAIXA que
# acompanha o arco da praça (a mesma equação, gerar_praca_base.y_base):
#
#     parede de trás      y_base(c)             (o arco)
#     beirada da laje     y_frente(c) = y_base(c) + 112
#     abaixo da beirada   o vazio (o térreo, que não aparece)
#
# O corrimão fica na beirada. Como y_base muda de 16 em 16 px a cada coluna
# (de 64 px nas pontas), a beirada vira uma escada de degraus, e em cada degrau
# o corrimão faz uma quina: um poste que sobe e desce o desnível, que é como
# o corrimão curvo da planta aparece nesta vista.

import math
import os

import numpy as np

import gerar_praca_base as base
import gerar_praca as gp
import gerar_porta_restaurante as porta
import gerar_restaurantes as restaurantes

Imagem, RAMPAS, SOMBRA, dilatar = base.Imagem, base.RAMPAS, base.SOMBRA, base.dilatar
ruido = base.ruido
ciclico = base.ruido_ciclico
hexa = base.hexa
L = base.PECA
H = base.ALTURA_PAREDE
LUZ = 0.8
LARGURA, ALTURA = base.ANDAR2_LARGURA, base.ANDAR2_ALTURA


# ---------------------------------------------------------------------------
# A parede do mezanino
# ---------------------------------------------------------------------------


def m_base(semente=0):
    """Revestimento de aço escovado em ripas verticais (o oposto da cerâmica
    clara do térreo): juntas a cada 40 px, uma faixa azul-escura no meio, o
    beiral de grafite em cima e o rodapé com respiros embaixo."""
    img = Imagem(L, H)
    X, Y = img.X, img.Y
    fino = ciclico(L, H, 2, 2, 2000 + semente)
    manchas = ciclico(L, H, 40, 16, 2001 + semente)
    escorrido = ciclico(L, H, 4, 56, 2002 + semente)
    corpo = img.ret(0, 12, L, 100)
    v = (0.42 + 0.2 * manchas + 0.05 * fino - 0.18 * (escorrido > 0.7)) * LUZ - 0.18 * np.clip((30 - Y) / 18, 0, 1)
    img.pintar(corpo, "inox", v)
    img.pintar(corpo & ((X % 8) == 0), "inox", v - 0.14, achatar=False)
    img.pintar(corpo & ((X % 8) == 1), "inox", v + 0.1, achatar=False)
    img.pintar(corpo & ((X % 40) == 0), "inox", v - 0.3, achatar=False)
    img.pintar(img.ret(0, 58, L, 61), "carpete", 0.46)
    img.pintar(img.ret(0, 60, L, 61), "neon_azul", 0.12, achatar=False)
    img.pintar(img.ret(0, 0, L, 12), "grafite", 0.3 + 0.1 * fino + 0.14 * (Y == 11))
    img.pintar(img.ret(0, 5, L, 7), "grafite", 0.1)
    img.pintar(img.ret(2, 5, L - 2, 6), "ciano", 0.12, achatar=False)
    img.pintar(img.ret(0, 100, L, H), "grafite", 0.24 + 0.08 * fino + 0.14 * (Y == 100))
    for x in range(8, L - 8, 14):
        img.pintar(img.ret(x, 104, x + 8, 109), "grafite", 0.08)
        for y in (105, 107):
            img.pintar(img.ret(x + 1, y, x + 7, y + 1), "grafite", 0.34, achatar=False)
    img.v, img.fino, img.manchas = v, fino, manchas
    return img


def m_musgo(img, semente, forca=0.4):
    gp.musgo_na_base(img, semente, forca)


def m_lisa(semente=0):
    img = m_base(semente)
    m_musgo(img, semente)
    return img


def m_lisa_rachada(semente=1):
    img = m_base(semente)
    gp.rachadura_fachada(img, 22, 2030 + semente)
    gp.rachadura_fachada(img, 56, 2031 + semente)
    m_musgo(img, semente, 0.7)
    return img


def m_dutos(semente=2):
    """Duto de ventilação grande com a grade e uma hélice parada, e canos que
    sobem pela parede."""
    img = m_base(semente)
    X, Y = img.X, img.Y
    img.pintar(img.ret(10, 22, 70, 74), "inox", 0.3 + 0.2 * (Y == 22) + 0.1 * (X == 10))
    img.pintar(img.ret(14, 26, 66, 70), "grafite", 0.06)
    cx, cy = 40, 48
    for k in range(4):
        a = math.radians(k * 45 + 12)
        img.pintar(img.linha(cx - 20 * math.cos(a), cy - 20 * math.sin(a), cx + 20 * math.cos(a), cy + 20 * math.sin(a), 1.7)
                   & img.ret(14, 26, 66, 70) & (np.hypot(X - cx, Y - cy) < 21), "inox", 0.34)
    img.pintar(img.elipse(cx, cy, 5, 5), "inox", 0.56)
    img.pintar(img.elipse(cx, cy, 2, 2), "grafite", 0.1)
    for y in range(28, 70, 5):
        img.pintar(img.ret(14, y, 66, y + 1) & ~img.elipse(cx, cy, 22, 22), "grafite", 0.16, achatar=False)
    for x in (8, 72):
        img.pintar(img.ret(x - 2, 12, x + 2, 100), "inox", 0.36 + 0.3 * (X == x - 2))
        for y in (30, 60, 86):
            img.pintar(img.ret(x - 3, y, x + 3, y + 3), "inox", 0.62)
    img.cor(img.ret(60, 76, 62, 78), base.hexa("#ffc24a")[0])
    m_musgo(img, semente, 0.3)
    return img


def m_painel_info(semente=3):
    """Painel de informações em holograma: moldura de aço, mapa do andar (um
    anel com três pontos) e setas, em azul claro."""
    img = m_base(semente)
    X, Y = img.X, img.Y
    rampa = "neon_azul"
    img.pintar(img.ret(12, 22, 68, 92), "inox", 0.4 + 0.2 * (Y == 22) + 0.1 * (X == 12))
    tela = img.ret(15, 25, 65, 89)
    img.pintar(tela, "grafite", 0.05 + 0.04 * (Y % 3 == 0))
    img.pintar(img.ret(18, 28, 62, 30), rampa, 0.8, achatar=False)
    cx, cy = 40, 56
    d = np.hypot((X + 0.5 - cx) / 17.0, (Y + 0.5 - cy) / 11.0)
    anel = (d < 1.0) & (d > 0.8) & tela
    img.pintar(anel, rampa, 0.7, achatar=False)
    img.pintar((d <= 0.8) & tela & (((X + Y) % 3) == 0), rampa, 0.22, achatar=False)
    for (px, py, cor) in ((24, 58, "neon_limao"), (31, 48, "neon_azul"), (54, 52, "neon_violeta")):
        img.pintar(img.elipse(px, py, 2, 2), cor, 0.95, achatar=False)
    img.pintar(img.ret(36, 66, 44, 68), "ciano", 0.9, achatar=False)
    img.pintar(img.ret(18, 78, 36, 79), rampa, 0.55, achatar=False)
    img.pintar(img.ret(18, 82, 30, 83), rampa, 0.4, achatar=False)
    img.pintar(img.ret(46, 78, 62, 79), rampa, 0.55, achatar=False)
    m_musgo(img, semente, 0.2)
    return img


def m_planta(semente=4):
    """Jardim suspenso: uma calha de aço com samambaias que caem pela parede,
    e plantas que brilham em verde-água."""
    img = m_base(semente)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(2040 + semente)
    img.pintar(img.ret(8, 30, 72, 38), "inox", 0.4 + 0.2 * (Y == 30))
    img.pintar(img.ret(10, 32, 70, 37), "laje", 0.2)
    for k in range(13):
        x0 = 12 + k * 4.6 + rng.uniform(-1, 1)
        comp = int(rng.integers(14, 52))
        ponta_x = x0 + rng.uniform(-6, 6)
        talo = img.caminho([(x0, 36), (x0 + (ponta_x - x0) * 0.4, 36 + comp * 0.6), (ponta_x, 36 + comp)], 0.7)
        img.pintar(talo, "verde", 0.34 + 0.24 * rng.random())
        img.pintar(img.elipse(ponta_x, 36 + comp, rng.uniform(2, 4), rng.uniform(2, 4)), "bioluz", 0.5 + 0.4 * rng.random())
    for (x0, y0) in ((16, 28), (40, 26), (62, 29)):
        img.pintar(img.elipse(x0, y0, 5, 4), "bioluz", 0.6 + 0.3 * rng.random())
        img.pintar(img.ret(x0, y0 - 1, x0 + 1, y0), "bioluz", 1.0, achatar=False)
    return img


def m_vidro_hall(semente=5):
    """A janela alta do hall, de piso a teto, com a noite lá fora e as nervuras
    da cúpula refletidas."""
    img = m_base(semente)
    X, Y = img.X, img.Y
    img.pintar(img.ret(6, 30, 74, 100), "inox", 0.4 + 0.2 * (Y == 30) + 0.1 * (X == 6) - 0.1 * (X == 73))
    vidro = img.ret(9, 33, 71, 97)
    noite = np.array(base.kit.NOITE)
    prof = np.clip((Y - 33) / 64.0, 0, 1)
    indice = np.clip(np.floor((0.15 + 0.6 * prof) * len(noite) + img.limiar), 0, len(noite) - 1).astype(int)
    img.px[vidro] = noite[indice][vidro]
    rng = np.random.default_rng(2050 + semente)
    for _ in range(12):
        img.px[int(rng.integers(34, 70)), int(rng.integers(10, 70))] = base.kit.ESTRELA[0]
    for x in (29, 51):
        img.pintar(img.ret(x, 32, x + 2, 98), "inox", 0.42 + 0.3 * (X == x))
    img.pintar(img.ret(9, 62, 71, 64), "inox", 0.4)
    reflexo = vidro & ((np.abs((X - Y) + 36) < 1.4) | (np.abs((X - Y) + 14) < 0.8))
    img.pintar(reflexo, "gelo", 0.6, achatar=False)
    img.pintar(img.ret(6, 97, 74, 101), "inox", 0.5 + 0.2 * (Y == 97))
    return img


def m_nicho(semente=6):
    """Nicho de manutenção do mezanino: um vão fundo e escuro na parede."""
    img = m_base(semente)
    X, Y = img.X, img.Y
    img.pintar(img.ret(14, 22, 66, 112), "inox", 0.44 + 0.2 * (Y == 22) + 0.1 * (X == 14))
    vao = img.ret(18, 26, 62, 112)
    prof = np.clip((Y - 26) / 86.0, 0, 1)
    img.pintar(vao, "grafite", 0.04 + 0.05 * prof)
    img.pintar(img.ret(18, 26, 24, 112), "grafite", 0.16 - 0.1 * (X - 18) / 6.0, achatar=False)
    img.pintar(img.ret(56, 26, 62, 112), "grafite", 0.03, achatar=False)
    img.pintar(img.ret(20, 28, 60, 29), "ciano", 0.16, achatar=False)
    img.pintar(img.ret(18, 26, 62, 30), "grafite", 0.02, achatar=False)
    for x0 in (20, 54):
        cipo = img.caminho([(x0 + 2 * math.sin(k * 0.9), 22 + k * 7) for k in range(7)], 0.7)
        img.pintar(cipo, "verde", 0.3 + 0.3 * img.fino)
    img.pintar(img.ret(14, 100, 66, 104), "grafite", 0.2)
    return img


# ---------------------------------------------------------------------------
# As escadas (a do mezanino e as duas do térreo)
# ---------------------------------------------------------------------------


def escada(parede, sentido, texto, cor="ciano", y_topo=36, interditada=False):
    """Uma porta de escada, sobre a peça de parede 'parede' (80 x 112).

    Vista de frente, uma escada que SOBE se afasta de nós subindo: cada degrau
    é mais alto e mais estreito que o da frente (perspectiva), e a luz vem do
    patamar lá em cima. A que DESCE é o contrário: vista de cima, os degraus
    de trás ficam mais baixos e mais estreitos, e a luz vem lá de baixo.
    Cada degrau k de 0 (o da frente) a N-1 tem a altura y_k e a largura w_k
    mudando por passos fixos, e o espelho (a face vertical) é mais escuro que
    o piso do degrau."""
    img = Imagem(parede.w, parede.h)
    img.px[:] = parede.px
    X, Y = img.X, img.Y
    rampa = base.NEON[cor]
    base_y = 112
    moldura = img.ret(14, y_topo - 4, 66, base_y)
    img.pintar(moldura, "inox", 0.44 + 0.2 * (Y == y_topo - 4) + 0.1 * (X == 14) - 0.1 * (X == 65))
    vao = img.ret(18, y_topo, 62, base_y)
    img.pintar(vao, "grafite", 0.03)
    passos = 8
    for k in range(passos - 1, -1, -1):
        t = k / float(passos - 1)
        if sentido == "sobe":
            y = base_y - 3 - k * 8
        else:
            y = y_topo + 18 + k * 8
        w = 42 - 20 * t
        xa, xb = int(round(40 - w / 2)), int(round(40 + w / 2))
        tom = 0.5 - 0.3 * t if sentido == "sobe" else 0.2 + 0.32 * t
        degrau = img.ret(xa, y - 6, xb, y + 2) & vao
        img.pintar(degrau, "grafite", tom * 0.7 + 0.1)
        espelho = img.ret(xa, y - 1, xb, y + 3) & vao
        img.pintar(espelho, "grafite", tom * 0.5)
        img.pintar(img.ret(xa, y - 6, xb, y - 5) & vao, rampa, 0.78 if sentido == "desce" else 0.62 - 0.3 * t, achatar=False)
    prof = np.clip((Y - y_topo) / float(base_y - y_topo), 0, 1)
    if sentido == "sobe":
        luz = vao & (Y < y_topo + 20)
        img.pintar(luz, rampa, 0.26 + 0.34 * (1 - (Y - y_topo) / 20.0), achatar=False)
        img.pintar(vao & (Y < y_topo + 20) & (((X + Y) % 2) == 0), rampa, 0.5, achatar=False)
    else:
        luz = vao & (Y > base_y - 22)
        img.pintar(luz, rampa, 0.22 + 0.3 * (Y - (base_y - 22)) / 22.0, achatar=False)
        img.pintar(img.ret(18, y_topo, 62, y_topo + 4), "grafite", 0.01)
    for lado in (-1, 1):
        x_a, x_b = (20, 30) if lado < 0 else (60, 50)
        y_a, y_b = (base_y - 14, base_y - 62) if sentido == "sobe" else (y_topo + 18, y_topo + 66)
        corrimao = img.caminho([(x_a, y_a), (x_b, y_b)], 0.9) & vao
        img.pintar(corrimao, "inox", 0.74)
        img.pintar(img.caminho([(x_a, y_a + 3), (x_b, y_b + 3)], 0.5) & vao, "inox", 0.3)
    img.pintar(img.ret(14, y_topo - 4, 66, y_topo - 2), rampa, 0.7, achatar=False)
    placa = img.ret(20, 12, 60, 24)
    img.pintar(placa, "grafite", 0.07)
    img.pintar(img.ret(20, 12, 60, 13) | img.ret(20, 23, 60, 24), rampa, 0.4, achatar=False)
    largura_texto = base.largura_do_texto(texto, 8)
    base.escrever(img, 40 - largura_texto // 2, 14, texto, rampa, 0.92, 8)
    if interditada:
        grade = img.ret(18, y_topo + 18, 62, base_y - 6) & vao
        img.pintar(grade & (((X - 18) % 6) < 2), "inox", 0.42)
        img.pintar(grade & (((Y - y_topo) % 9) < 2), "inox", 0.34)
        for k in range(3):
            fita = img.poligono([(14, y_topo + 24 + k * 26), (66, y_topo + 36 + k * 26), (66, y_topo + 44 + k * 26), (14, y_topo + 32 + k * 26)])
            faixas = (((X + Y) // 5) % 2) == 0
            img.pintar(fita & faixas, "neon_ambar", 0.8, achatar=False)
            img.pintar(fita & ~faixas, "grafite", 0.06)
    img.pintar(img.ret(14, 100, 66, 104) & ~vao, "grafite", 0.2)
    return img


# ---------------------------------------------------------------------------
# As lojas do mezanino (fachadas)
# ---------------------------------------------------------------------------


def toldo(img, rampa, claro="papel_branco", y0=14, y1=26, listra=6, diagonal=False):
    X, Y = img.X, img.Y
    caixa = img.ret(4, y0, 76, y1)
    faixa = ((((X + (Y if diagonal else 0)) // listra) % 2) == 0)
    img.pintar(caixa & faixa, rampa, 0.5)
    img.pintar(caixa & ~faixa, claro, 0.62 if claro == "papel_branco" else 0.2)
    img.pintar(img.ret(4, y0, 76, y0 + 1), "inox", 0.6)
    img.pintar(img.ret(4, y1 - 2, 76, y1) & ((X % 6) < 4), "grafite", 0.1)
    img.pintar(img.ret(4, y1 - 1, 76, y1), rampa, 0.2)


def moldura_vitrine(img, rampa, brilho_interno=0.2):
    X, Y = img.X, img.Y
    img.pintar(img.ret(6, 24, 74, 100), "inox", 0.42 + 0.2 * (Y == 24) + 0.1 * (X == 6) - 0.1 * (X == 73))
    vidro = img.ret(9, 27, 71, 97)
    img.pintar(vidro, "grafite", 0.08)
    prof = np.clip((Y - 27) / 70.0, 0, 1)
    img.pintar(vidro, rampa, 0.12 + brilho_interno * (1 - prof) + 0.04 * img.fino)
    img.pintar(img.ret(4, 97, 76, 101), "inox", 0.5 + 0.2 * (Y == 97))
    return vidro


def reflexo_vitrine(img, vidro, desloc=36):
    X, Y = img.X, img.Y
    reflexo = vidro & ((np.abs((X - Y) + desloc) < 2) | (np.abs((X - Y) + desloc - 14) < 1))
    img.pintar(reflexo, "gelo", 0.55, achatar=False)


def manequim(img, cx, y_pe, camisa, calca="grafite", mascara=None, escala=1.0):
    X, Y = img.X, img.Y
    m = mascara if mascara is not None else np.ones_like(X, dtype=bool)
    topo = y_pe - 46 * escala
    img.pintar(img.elipse(cx, topo + 4, 3.2, 3.8) & m, "papel_branco", 0.78 - 0.18 * ((X - cx) > 1))
    img.pintar(img.ret(cx - 1, topo + 7, cx + 1, topo + 10) & m, "papel_branco", 0.6)
    tronco = img.poligono([(cx - 7, topo + 10), (cx + 7, topo + 10), (cx + 5, topo + 28 * escala), (cx - 5, topo + 28 * escala)]) & m
    img.pintar(tronco, camisa, 0.46 + 0.22 * ((X - cx) < -2))
    img.pintar(tronco & (np.abs(Y - (topo + 17)) < 1.2), "papel_branco", 0.8, achatar=False)
    img.pintar(img.ret(cx - 5, topo + 28 * escala, cx + 6, topo + 40 * escala) & m & ~img.ret(cx, topo + 28 * escala, cx + 1, y_pe), calca, 0.2)
    img.pintar(img.ret(cx - 1, topo + 40 * escala, cx + 1, y_pe) & m, "inox", 0.4)
    img.pintar(img.ret(cx - 7, y_pe - 1, cx + 8, y_pe + 1) & m, "inox", 0.34)
    for lado in (-1, 1):
        img.pintar(img.caminho([(cx + lado * 7, topo + 11), (cx + lado * 9, topo + 24)], 0.9) & m, camisa, 0.36)


def vitrine_loja_uni(semente=10):
    """Vitrine da Loja Universitária: toldo azul e branco, dois manequins de
    moletom e jaqueta e uma arara com camisetas penduradas."""
    img = m_base(semente)
    X, Y = img.X, img.Y
    rampa = "neon_azul"
    vidro = moldura_vitrine(img, rampa, 0.24)
    img.pintar(img.ret(11, 40, 69, 41) & vidro, "inox", 0.6)
    for x in range(14, 68, 6):
        img.pintar(img.ret(x, 41, x + 1, 44) & vidro, "inox", 0.5)
        cor = ("neon_azul", "papel_branco", "carpete", "neon_azul", "papel_branco")[(x // 6) % 5]
        img.pintar(img.ret(x - 2, 44, x + 3, 56) & vidro, cor, 0.5 + 0.1 * ((x // 6) % 3))
    for cx, cam in ((26, "neon_azul"), (54, "carpete")):
        manequim(img, cx, 94, cam, mascara=vidro & ~img.ret(11, 36, 69, 58))
    img.pintar(img.ret(11, 94, 69, 97) & vidro, "grafite", 0.05)
    for x in (18, 40, 62):
        img.pintar(img.poligono([(x, 28), (x + 5, 28), (x + 2.5, 33)]) & vidro, rampa, 0.9, achatar=False)
    toldo(img, rampa)
    reflexo_vitrine(img, vidro, 34)
    m_musgo(img, semente, 0.3)
    return img


def vitrine_grafica(semente=11):
    """Vitrine da Gráfica Quântica: toldo de listras diagonais limão e grafite,
    três cartazes coloridos, a impressora grande ao fundo soltando uma fita de
    papel e os quatro pontos de cor (ciano, magenta, amarelo, preto)."""
    img = m_base(semente)
    X, Y = img.X, img.Y
    rampa = "neon_limao"
    vidro = moldura_vitrine(img, rampa, 0.2)
    for (x0, y0, x1, y1, cor) in ((12, 32, 28, 56, "ciano"), (31, 30, 47, 50, "neon_magenta"), (50, 34, 68, 58, "neon_ambar")):
        img.pintar(img.ret(x0 - 1, y0 - 1, x1 + 1, y1 + 1) & vidro, "papel_branco", 0.84)
        img.pintar(img.ret(x0, y0, x1, y1) & vidro, cor, 0.5)
        img.pintar(img.ret(x0 + 2, y0 + 3, x1 - 2, y0 + 5) & vidro, "papel_branco", 0.9)
        img.pintar(img.elipse((x0 + x1) / 2.0, y0 + 14, 4, 4) & vidro, "grafite", 0.2)
    img.pintar(img.ret(11, 70, 69, 94) & vidro, "grafite", 0.14 + 0.1 * (Y == 70))
    img.pintar(img.ret(14, 74, 46, 86) & vidro, "inox", 0.34 + 0.2 * (Y == 74))
    img.pintar(img.ret(18, 77, 42, 83) & vidro, "grafite", 0.06)
    img.pintar(img.ret(50, 72, 66, 92) & vidro, "inox", 0.28 + 0.2 * (X == 50))
    img.cor(img.ret(54, 76, 56, 78) & vidro, hexa("#6cf28e")[0])
    img.pintar(img.ret(20, 86, 40, 87) & vidro, "papel_branco", 0.88)
    fita = img.caminho([(30, 87), (30, 91), (36, 93), (44, 93)], 1.6) & vidro
    img.pintar(fita, "papel_branco", 0.8)
    img.pintar(fita & (Y % 3 == 0), "papel_branco", 0.5, achatar=False)
    for k, cor in enumerate(("ciano", "neon_magenta", "neon_ambar", "grafite")):
        img.pintar(img.elipse(20 + k * 5, 64, 1.8, 1.8) & vidro, cor, 0.9 if cor != "grafite" else 0.05, achatar=False)
    toldo(img, rampa, "grafite", diagonal=True, listra=7)
    reflexo_vitrine(img, vidro, 20)
    m_musgo(img, semente, 0.25)
    return img


def poster_arte(img, x0, y0, x1, y1, variante):
    """A arte de um cartaz de filme (duas cenas abstratas): um planeta com anel
    e foguete, e uma figura contra o sol."""
    X, Y = img.X, img.Y
    quadro = img.ret(x0, y0, x1, y1)
    cx = (x0 + x1) / 2.0
    if variante == 0:
        img.pintar(quadro, "neon_violeta", 0.18 + 0.2 * (1 - (Y - y0) / float(y1 - y0)))
        img.pintar(img.elipse(cx, y0 + 18, 11, 11) & quadro, "neon_violeta", 0.5 + 0.3 * ((X - cx) < -3))
        anel = (np.abs(((X + 0.5 - cx) / 17.0) ** 2 + ((Y + 0.5 - (y0 + 18)) / 4.0) ** 2 - 1.0) < 0.25) & quadro
        img.pintar(anel, "neon_ambar", 0.78, achatar=False)
        img.pintar(img.poligono([(cx - 2, y0 + 44), (cx + 2, y0 + 44), (cx + 2, y0 + 56), (cx, y0 + 60), (cx - 2, y0 + 56)]) & quadro, "papel_branco", 0.82)
        img.pintar(img.poligono([(cx - 1, y0 + 60), (cx + 1, y0 + 60), (cx, y0 + 66)]) & quadro, "neon_ambar", 0.95, achatar=False)
    else:
        img.pintar(quadro, "neon_magenta", 0.2 + 0.26 * (Y - y0) / float(y1 - y0))
        img.pintar(img.elipse(cx, y0 + 28, 13, 13) & quadro, "neon_ambar", 0.7 + 0.2 * ((X - cx) < 0))
        img.pintar(img.poligono([(cx - 9, y1 - 1), (cx - 6, y0 + 36), (cx - 2, y0 + 30), (cx + 2, y0 + 30), (cx + 6, y0 + 36), (cx + 9, y1 - 1)]) & quadro, "grafite", 0.05)
        img.pintar(img.elipse(cx, y0 + 26, 3.5, 4) & quadro, "grafite", 0.05)
        img.pintar(img.ret(x0, y1 - 8, x1, y1) & quadro & (((X * 7) % 11) < 6), "grafite", 0.07)


def cartaz_cinema(variante=0, semente=12):
    """Caixa de luz com um cartaz de filme, moldura de aço, lâmpadas de marquise
    em cima (as que acendem em sequência) e o título embaixo."""
    img = m_base(semente + variante)
    X, Y = img.X, img.Y
    img.pintar(img.ret(10, 22, 70, 100), "inox", 0.38 + 0.2 * (Y == 22) + 0.1 * (X == 10) - 0.1 * (X == 69))
    poster_arte(img, 14, 28, 66, 86, variante)
    img.pintar(img.ret(14, 28, 66, 29), "papel_branco", 0.4)
    img.pintar(img.ret(18, 88, 62, 91), "grafite", 0.06)
    img.pintar(img.ret(20, 89, 42 + 6 * variante, 90), "neon_violeta", 0.9, achatar=False)
    for x in range(14, 68, 6):
        img.pintar(img.elipse(x, 24.5, 1.4, 1.4), "neon_ambar", 1.0 if (x // 6) % 2 == variante else 0.55, achatar=False)
    img.pintar(img.ret(10, 94, 70, 97), "grafite", 0.1)
    img.pintar(img.ret(14, 95, 66, 96), "neon_violeta", 0.5, achatar=False)
    m_musgo(img, semente + variante, 0.25)
    return img


def bilheteria(semente=13, espelhar=False):
    """Guichê de ingressos: toldo violeta, vidro com a luz do guichê, a ranhura
    de dinheiro e o letreiro de holograma INGRESSOS. Com 'espelhar', a peça é
    virada e só então o texto é escrito (senão as letras saem de trás para a
    frente)."""
    img = m_base(semente)
    X, Y = img.X, img.Y
    rampa = "neon_violeta"
    vidro = moldura_vitrine(img, rampa, 0.26)
    img.pintar(img.ret(11, 74, 69, 82) & vidro, "grafite", 0.08 + 0.1 * (Y == 74))
    img.pintar(img.ret(11, 82, 69, 94) & vidro, "grafite", 0.05)
    img.pintar(img.ret(26, 77, 54, 79) & vidro, "inox", 0.12)
    img.pintar(img.ret(36, 70, 44, 74) & vidro, "inox", 0.5)
    img.pintar(img.elipse(40, 58, 5, 5) & vidro, "grafite", 0.04)
    img.pintar(img.ret(36, 62, 44, 70) & vidro, "grafite", 0.04)
    img.pintar(img.ret(13, 90, 25, 92) & vidro, "neon_ambar", 0.6, achatar=False)
    toldo(img, rampa, "grafite")
    reflexo_vitrine(img, vidro, 30)
    m_musgo(img, semente, 0.25)
    if espelhar:
        img = gp.espelho(img)
    largura_texto = base.largura_do_texto("INGRESSOS", 8)
    base.escrever(img, 40 - largura_texto // 2, 31, "INGRESSOS", rampa, 0.95, 8)
    return img


# ---------------------------------------------------------------------------
# O fundo do mezanino
# ---------------------------------------------------------------------------

SEQUENCIA = [
    "m_lisa_rachada", "vitrine_grafica", "PORTA:grafica", ("vitrine_grafica", True), "m_dutos",
    "m_nicho", "vitrine_loja_uni", "PORTA:loja_uni", ("vitrine_loja_uni", True), "m_painel_info",
    "m_planta", "m_vidro_hall", "ESCADA", ("m_vidro_hall", True), ("m_planta", True),
    ("m_painel_info", True), ("m_dutos", True), "m_lisa", "m_planta_b", ("m_nicho", True),
    "cartaz_cinema_a", "bilheteria", "PORTA:cinema", "bilheteria_b", ("cartaz_cinema_b", True),
]

PECAS = {
    "m_lisa": lambda: m_lisa(0),
    "m_lisa_rachada": m_lisa_rachada,
    "m_dutos": m_dutos,
    "m_painel_info": m_painel_info,
    "m_planta": m_planta,
    "m_planta_b": lambda: m_planta(14),
    "m_vidro_hall": m_vidro_hall,
    "m_nicho": m_nicho,
    "vitrine_grafica": vitrine_grafica,
    "vitrine_loja_uni": vitrine_loja_uni,
    "bilheteria": bilheteria,
    "bilheteria_b": lambda: bilheteria(13, True),
    "cartaz_cinema_a": lambda: cartaz_cinema(0),
    "cartaz_cinema_b": lambda: cartaz_cinema(1, 15),
}


def peca_da_coluna(coluna, pecas):
    item = SEQUENCIA[coluna]
    espelhar = False
    if isinstance(item, tuple):
        item, espelhar = item
    if item.startswith("PORTA:"):
        loja = item.split(":")[1]
        return porta.peca_de_parede(m_base(30 + coluna), base.COR_LOJA[loja])
    if item == "ESCADA":
        return escada(m_base(9), "desce", "PRAÇA")
    peca = pecas[item]
    return gp.espelho(peca) if espelhar else peca


def mapas_de_altura():
    colunas = np.minimum(np.arange(LARGURA) // L, base.COLUNAS_PRACA - 1)
    yb = np.array([base.y_base(c) for c in range(base.COLUNAS_PRACA)])[colunas]
    return yb, yb + base.LARGURA_BALCAO


def piso_mezanino():
    """Placas de aço escuro de 64 x 16 px (as fileiras se alternam como
    tijolos) só na faixa do corredor, entre a parede (y_base) e a beirada
    (y_frente). Um tapete de passadeira azul acompanha o corredor pelo meio, e
    uma linha de luz ciano tracejada marca a beirada, 12 px antes do vazio. A
    contagem das placas parte de y = 0 e x = 0 da sala, como no piso da praça,
    para as colunas se encaixarem."""
    img = Imagem(LARGURA, ALTURA)
    X, Y = img.X, img.Y
    yb, yf = mapas_de_altura()
    ybase = yb[None, :] * np.ones((ALTURA, 1), dtype=int)
    yfrente = yf[None, :] * np.ones((ALTURA, 1), dtype=int)
    chao = (Y >= ybase) & (Y < yfrente)
    fascia = (Y >= yfrente) & (Y < yfrente + base.ESPESSURA_LAJE)
    vazio = Y >= yfrente + base.ESPESSURA_LAJE
    fileira = Y // 16
    desloc = 32 * (fileira % 2)
    placa = (X + desloc) // 64
    sorteio = np.random.default_rng(2100).random((fileira.max() + 2, LARGURA // 64 + 3))
    tom = sorteio[fileira, placa]
    fino = ciclico(LARGURA, ALTURA, 2, 2, 2101)
    manchas = ruido(LARGURA, ALTURA, 60, 30, 2102)
    sujeira = np.clip((Y - ybase) / 22.0, 0, 1)
    valor = (0.3 + 0.2 * tom + 0.14 * manchas + 0.05 * fino) * LUZ - 0.2 * (1 - sujeira)
    img.pintar(chao, "grafite", valor)
    junta = chao & (((Y % 16) == 0) | (((X + desloc) % 64) == 0))
    img.pintar(junta, "grafite", valor - 0.2, achatar=False)
    img.pintar(chao & ((Y % 16) == 1) & (((X + desloc) % 64) != 0), "grafite", valor + 0.08, achatar=False)
    passadeira = chao & (Y >= ybase + 34) & (Y < ybase + 76)
    losango = (((X + Y) % 12) == 0) | (((X - Y) % 12) == 0)
    img.pintar(passadeira, "carpete", 0.3 + 0.1 * manchas + 0.04 * fino)
    img.pintar(passadeira & losango & (((X + Y) % 24) == 0), "carpete", 0.12, achatar=False)
    img.pintar(chao & ((Y == ybase + 34) | (Y == ybase + 75)), "carpete", 0.7, achatar=False)
    guia = chao & (Y == yfrente - 12) & ((X % 12) < 8)
    img.pintar(guia, "ciano", 0.62, achatar=False)
    img.cor(chao & (Y == ybase), SOMBRA)
    img.chao, img.ybase, img.yfrente, img.fino, img.manchas = chao, ybase, yfrente, fino, manchas
    img.fascia, img.vazio = fascia, vazio
    return img


def pintar_laje_e_vazio(img):
    """A frente da laje (a espessura, com a luz de balizamento) e, abaixo dela,
    o vazio do andar de baixo: quase preto, com uma névoa azulada que sobe,
    feixes de luz ciano muito fracos e pontinhos de neon bem longe."""
    X, Y = img.X, img.Y
    f = img.fascia
    t = np.clip((Y - img.yfrente) / float(base.ESPESSURA_LAJE), 0, 1)
    img.pintar(f, "grafite", 0.34 - 0.24 * t + 0.04 * img.fino)
    img.pintar(f & (Y == img.yfrente), "grafite", 0.6, achatar=False)
    img.pintar(f & (Y == img.yfrente + 4) & ((X % 20) < 12), "ciano", 0.5, achatar=False)
    v = img.vazio
    fundo = np.clip((Y - img.yfrente - base.ESPESSURA_LAJE) / 150.0, 0, 1)
    nevoa = ruido(LARGURA, ALTURA, 90, 40, 2110)
    img.pintar(v, "laje", 0.12 * (1 - fundo) ** 1.4 + 0.05 * nevoa * (1 - fundo) + 0.01)
    rng = np.random.default_rng(2111)
    intensidade = np.exp(-(((X + 60) % 380 - 190) / 46.0) ** 2) * (1 - fundo) ** 1.6
    pontilhado = v & (rng.random((ALTURA, LARGURA)) < intensidade * 0.22)
    img.pintar(pontilhado, "ciano", 0.12, achatar=False)
    cores = ("neon_ambar", "neon_verde", "neon_vermelho", "neon_magenta", "ciano")
    for _ in range(90):
        x, y = int(rng.integers(8, LARGURA - 8)), int(rng.integers(0, ALTURA))
        if v[y, x] and fundo[y, x] > 0.25:
            img.pintar(img.ret(x, y, x + 1, y + 1), cores[int(rng.integers(0, len(cores)))], 0.16 + 0.1 * rng.random(), achatar=False)
    for c in range(base.COLUNAS_PRACA - 1):
        a, b = base.y_frente(c), base.y_frente(c + 1)
        if a != b:
            xb = (c + 1) * L
            lado = img.ret(xb - 1, min(a, b), xb + 1, max(a, b) + base.ESPESSURA_LAJE)
            img.pintar(lado & (f | v), "grafite", 0.04, achatar=False)


def fundo_andar2():
    pecas = {nome: f() for nome, f in PECAS.items()}
    tela = Imagem(LARGURA, ALTURA)
    tela.colar(gp.cupula(LARGURA, 280), 0, 0)
    for c in range(base.COLUNAS_PRACA):
        tela.colar(peca_da_coluna(c, pecas), c * L, base.y_base(c) - H)
    chao = piso_mezanino()
    gp.musgo_no_piso(chao, 2120)
    gp.rachaduras_no_piso(chao, 40, 2121)
    y_hall = base.y_base(base.COLUNA_ESCADA_MEZANINO) + 60
    gp.emblema_central(chao, LARGURA // 2, y_hall, 120, 30)
    for loja, coluna in base.LOJAS_ANDAR2.items():
        x_porta = coluna * L + 41
        y_porta = base.y_base(coluna) + 12
        gp.trilha_ate_a_porta(chao, (x_porta, y_porta + 4), (x_porta, base.y_frente(coluna) - 20), 40, 28, base.NEON[base.COR_LOJA[loja]])
    c_esc = base.COLUNA_ESCADA_MEZANINO
    gp.trilha_ate_a_porta(chao, (c_esc * L + 41, base.y_base(c_esc) + 16), (LARGURA // 2, y_hall - 28), 46, 30, base.NEON["ciano"])
    pintar_laje_e_vazio(chao)
    cheio = chao.chao | chao.fascia | chao.vazio
    tela.px[cheio] = chao.px[cheio]
    gp.cantos_em_degrau(tela)
    portas = [(c * L + 10, base.y_base(c) - H + 24, c * L + 70, base.y_base(c)) for c in list(base.LOJAS_ANDAR2.values())]
    return tela, base.camada_emissiva(tela, portas)


# ---------------------------------------------------------------------------
# O corrimão (sprite na frente do Gabriel)
# ---------------------------------------------------------------------------

ALTURA_CORRIMAO = 30


def corrimao():
    """O corrimão de vidro ao longo da beirada: passa-mão de aço com uma linha
    de luz ciano (que brilha) por baixo, painéis de vidro entre os postes de
    40 em 40 px (pontilhado, para ver o Gabriel através) e a base. Alguns
    painéis quebraram. Em cada degrau da beirada o corrimão faz uma quina: um
    poste alto que cobre o desnível."""
    img = Imagem(LARGURA, ALTURA)
    X, Y = img.X, img.Y
    _, yf = mapas_de_altura()
    yfrente = yf[None, :] * np.ones((ALTURA, 1), dtype=int)
    topo = yfrente - ALTURA_CORRIMAO
    rng = np.random.default_rng(2130)
    quebrado = rng.random(LARGURA // 40 + 1) < 0.2
    painel = (Y >= topo + 3) & (Y < yfrente - 3)
    inteiro = ~quebrado[X // 40]
    vidro = painel & inteiro & (((X + Y) % 2) == 0)
    img.pintar(vidro, "gelo", 0.36 + 0.2 * (((X - Y) % 17) < 2), achatar=False)
    rachado = painel & ~inteiro & ((np.abs(((X % 40) * 0.6) - (Y - topo) + 4) < 0.8) | (np.abs(((X % 40) * 0.5) + (Y - topo) - 36) < 0.7)) & ((X % 40) < 12)
    img.pintar(rachado, "gelo", 0.5, achatar=False)
    img.pintar((Y >= topo) & (Y < topo + 2), "inox", 0.78)
    img.pintar((Y == topo), "inox", 0.95, achatar=False)
    img.pintar((Y == topo + 2), "ciano", 0.82, achatar=False)
    img.pintar((Y >= yfrente - 3) & (Y < yfrente), "inox", 0.34 + 0.2 * (Y == yfrente - 3))
    poste = (X % 40 < 3) & (Y >= topo) & (Y < yfrente)
    img.pintar(poste, "inox", 0.46 + 0.3 * (X % 40 == 0))
    for c in range(base.COLUNAS_PRACA - 1):
        a, b = base.y_frente(c), base.y_frente(c + 1)
        if a == b:
            continue
        xb = (c + 1) * L
        y_alto = min(a, b) - ALTURA_CORRIMAO
        quina = img.ret(xb - 1, y_alto, xb + 2, max(a, b))
        img.pintar(quina, "inox", 0.5 + 0.28 * (X == xb - 1))
        img.pintar(img.ret(xb - 1, y_alto, xb + 2, y_alto + 2), "inox", 0.9, achatar=False)
        img.pintar(img.ret(xb + 1, y_alto + 2, xb + 2, max(a, b) - ALTURA_CORRIMAO + 3), "ciano", 0.82, achatar=False)
    return img


# ---------------------------------------------------------------------------
# Letreiros
# ---------------------------------------------------------------------------


def letreiros():
    saida = {}
    for loja in ("grafica", "loja_uni", "cinema"):
        saida[f"letreiro_{loja}"] = restaurantes.letreiro(base.NOME_LOJA[loja], base.COR_LOJA[loja])
    saida["letreiro_mezanino"] = restaurantes.letreiro("SEGUNDO ANDAR", "ciano", 240, 28, 16, pes=False)
    return saida


def main():
    print("Gerando o segundo andar em", os.path.relpath(base.PASTA_PRACA, base.PASTA_PROJETO))
    pecas = {nome: f() for nome, f in PECAS.items()}
    escadas = {
        "escada_sobe": escada(gp.fachada_base(14), "sobe", "MEZANINO"),
        "escada_interditada": escada(gp.fachada_base(10), "sobe", "FECHADA", interditada=True),
        "escada_desce": escada(m_base(9), "desce", "PRAÇA"),
    }
    base.salvar_catalogo("andar2_fachadas", list(pecas.items()) + list(escadas.items()), 6)
    tela, luz = fundo_andar2()
    base.salvar(tela, "fundo_andar2.png")
    grade = corrimao()
    luz.colar(base.camada_emissiva(grade), 0, 0)
    base.salvar(luz, "fundo_andar2_luz.png")
    base.salvar(grade, "corrimao_andar2.png")
    import gerar_interiores_andar2 as interiores
    fundos = []
    for nome in interiores.SALAS:
        fundo, luz_fundo = interiores.montar_fundo(nome)
        base.salvar(fundo, f"fundo_{nome}.png")
        base.salvar(luz_fundo, f"fundo_{nome}_luz.png")
        fundos.append((f"fundo_{nome}", fundo))
    base.salvar_catalogo("andar2_fundos", fundos, 2, 1)
    amostra = []
    for nome, (apagado, aceso) in letreiros().items():
        base.salvar(apagado, f"{nome}.png", "letreiros")
        base.salvar(aceso, f"{nome}_aceso.png", "letreiros")
        visto = Imagem(apagado.w, apagado.h)
        visto.colar(apagado, 0, 0)
        visto.colar(aceso, 0, 0)
        amostra += [(nome, apagado), (nome + "_ac", visto)]
    base.salvar_catalogo("andar2_letreiros", amostra, 2, 2)


if __name__ == "__main__":
    main()
