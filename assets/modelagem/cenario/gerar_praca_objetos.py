# gerar_praca_objetos.py — desenha, por código, os OBJETOS da praça de
# alimentação e dos restaurantes do Centro de Convivência: mesas e cadeiras
# futuristas, postes, árvores de cúpula, balcões, fornos...
#
# Como rodar (Python 3 + numpy + Pillow):
#
#   python assets/modelagem/cenario/gerar_praca_objetos.py
#
# O que sai (em assets/sprites/cenario/praca/objetos/<objeto>.png): cada
# objeto é um sprite que o Gabriel contorna (y-sort); o "pé" de cada um
# sai no terminal, como no gerar_dtec.py, e a pegada (a caixa de colisão no
# chão) está em OBJETOS, no fim deste arquivo.
# Com CATALOGO=1 monta uma folha com os objetos. Não commitar.
#
# Como se desenha um objeto redondo ou cilíndrico: o tom de cada pixel
# depende do seu lugar no volume, como nas bobinas do DTEC. Para um cilindro
# vertical, o tom segue o cosseno do ângulo ao longo da largura (cos(dx * 1.3),
# com dx de -1 a 1): o meio é o mais claro, as bordas escurecem. Para uma
# esfera, o tom cai com 1 - d^2 a partir do ponto de luz (em cima, à esquerda).

import math

import numpy as np

import gerar_praca_base as base

Imagem, RAMPAS, dilatar = base.Imagem, base.RAMPAS, base.dilatar
ruido = base.ruido
ciclico = base.ruido
LUZ = 0.82


def tom_cilindro(img, x0, x1):
    """O tom de 0 a 1 de um cilindro entre x0 e x1: mais claro um pouco à
    esquerda do meio (a luz vem de cima, da esquerda)."""
    dx = (img.X + 0.5 - (x0 + x1) / 2.0 + 0.12 * (x1 - x0)) / ((x1 - x0) / 2.0)
    return np.clip(np.cos(np.clip(dx, -1.0, 1.0) * 1.25), 0.0, 1.0)


def neon_linha(img, mascara, rampa, valor=0.9):
    img.pintar(mascara, rampa, valor, achatar=False)


# ---------------------------------------------------------------------------
# Praça
# ---------------------------------------------------------------------------


def cadeira_fut():
    """Cadeira de casca moldada, vista de lado (virada para a direita): o
    assento e o encosto de uma peça só, grafite com o friso de neon ciano,
    sobre uma haste fina com base redonda."""
    img = Imagem(22, 30)
    X, Y = img.X, img.Y
    img.pintar(img.ret(10, 17, 12, 26), "inox", 0.5 + 0.2 * (X == 10))
    img.pintar(img.elipse(11, 27, 7, 2), "inox", 0.45)
    img.pintar(img.ret(8, 26, 14, 28), "inox", 0.3)
    assento = img.poligono([(4, 15), (17, 15), (19, 18), (4, 19)])
    img.pintar(assento, "grafite", 0.4 + 0.2 * (Y == 15))
    encosto = img.poligono([(3, 3), (7, 2), (8, 16), (4, 18), (2, 12)])
    img.pintar(encosto, "grafite", 0.44 + 0.2 * (X < 5))
    neon_linha(img, img.caminho([(3.5, 4), (4.5, 16)], 0.5) & encosto, "ciano", 0.85)
    neon_linha(img, img.ret(5, 19, 18, 20), "ciano", 0.55)
    img.contornar()
    return img, 11, 28


def mesa_holo():
    """Mesa redonda de pedestal: tampo de cerâmica clara com a borda de neon
    e, no meio, o projetor de onde sobe o holograma do cardápio (um cone
    ciano com ícones flutuando)."""
    img = Imagem(64, 66)
    X, Y = img.X, img.Y
    # Pedestal e base.
    img.pintar(img.ret(29, 38, 35, 56), "inox", 0.34 + 0.34 * (X < 32) - 0.1 * (X > 33))
    img.pintar(img.elipse(32, 58, 17, 5), "inox", 0.34)
    img.pintar(img.elipse(32, 57, 15, 4), "inox", 0.5)
    # Tampo (elipse em perspectiva), com a borda e o friso de neon.
    tampo = img.elipse(32, 36, 28, 9)
    img.pintar(img.elipse(32, 38, 28, 9), "grafite", 0.2)
    img.pintar(tampo, "ceramica", 0.52 + 0.28 * ((X - 32) < -6) * ((Y - 36) < 0) + 0.06 * ciclico(64, 66, 2, 2, 1700))
    img.pintar(tampo & ~img.elipse(32, 36, 25, 7), "ceramica", 0.3, achatar=False)
    neon_linha(img, img.elipse(32, 36, 27, 8) & ~img.elipse(32, 36, 26, 7), "ciano", 0.6)
    # Projetor e holograma (cone translúcido de pontilhado + ícones).
    img.pintar(img.elipse(32, 34, 6, 2), "inox", 0.62)
    img.pintar(img.elipse(32, 33, 3, 1), "ciano", 0.95, achatar=False)
    cone = img.poligono([(30, 33), (34, 33), (45, 6), (19, 6)]) & (((X + Y) % 2) == 0)
    img.pintar(cone, "ciano", 0.18 + 0.2 * (1 - (Y - 6) / 27.0), achatar=False)
    img.pintar(img.elipse(32, 6, 13, 2.5), "ciano", 0.5, achatar=False)
    img.pintar(img.ret(24, 11, 40, 12), "ciano", 0.9, achatar=False)
    img.pintar(img.ret(26, 15, 38, 16), "ciano", 0.7, achatar=False)
    img.pintar(img.ret(28, 19, 36, 20), "ciano", 0.55, achatar=False)
    img.pintar(img.elipse(32, 25, 3, 3), "ciano", 0.8, achatar=False)
    img.contornar()
    return img, 32, 62


def banco_curvo():
    """Banco de praça curvo: assento e encosto de uma peça só, estofado
    escuro, com uma faixa de neon por baixo (que acende no chão)."""
    img = Imagem(72, 34)
    X, Y = img.X, img.Y
    encosto = img.poligono([(2, 8), (70, 8), (68, 18), (4, 18)])
    img.pintar(encosto, "couro", 0.42 + 0.22 * (Y < 11))
    assento = img.poligono([(4, 18), (68, 18), (70, 26), (2, 26)])
    img.pintar(assento, "couro", 0.34 + 0.2 * (Y < 20))
    img.pintar(img.ret(2, 26, 70, 29), "grafite", 0.12)
    for x in (8, 60):
        img.pintar(img.ret(x, 26, x + 4, 33), "inox", 0.4)
    neon_linha(img, img.ret(6, 29, 66, 30), "neon_violeta", 0.8)
    img.pintar(img.ret(6, 30, 66, 33) & ((X + Y) % 2 == 0), "neon_violeta", 0.3, achatar=False)
    for x in range(10, 64, 12):
        img.pintar(img.ret(x, 8, x + 1, 26), "couro", 0.16, achatar=False)
    img.contornar()
    return img, 36, 30


def guarda_sol_holo():
    """Guarda-sol de holograma: um mastro de aço com a base pesada e, no alto,
    uma cúpula translúcida de luz (ciano, em pontilhado) flutuando, com os
    raios do anel de luz."""
    img = Imagem(64, 84)
    X, Y = img.X, img.Y
    img.pintar(img.ret(30, 20, 34, 74), "inox", 0.4 + 0.4 * (X == 30) - 0.1 * (X == 33))
    img.pintar(img.elipse(32, 78, 16, 4), "inox", 0.36)
    img.pintar(img.elipse(32, 77, 13, 3), "inox", 0.5)
    img.pintar(img.ret(26, 16, 38, 22), "inox", 0.55 + 0.2 * (Y == 16))
    img.cor(img.ret(31, 18, 33, 20), base.hexa("#8cf2ff")[0])
    cupula = img.elipse(32, 20, 30, 17) & (Y < 21)
    img.pintar(cupula & (((X + Y) % 2) == 0), "ciano", 0.3, achatar=False)
    anel = img.elipse(32, 20, 30, 17) & ~img.elipse(32, 20, 28, 15) & (Y < 21)
    img.pintar(anel, "ciano", 0.8, achatar=False)
    for ang in (-60, -30, 0, 30, 60):
        a = math.radians(ang)
        img.pintar(img.linha(32, 20, 32 + 28 * math.sin(a), 20 - 15 * math.cos(a), 0.45), "ciano", 0.55, achatar=False)
    img.pintar(img.ret(2, 20, 62, 21), "ciano", 0.9, achatar=False)
    img.contornar()
    return img, 32, 80


def poste_luz():
    """Poste de luz da praça: haste fina de aço e um globo de luz âmbar. A
    luz de verdade vem de uma PointLight2D no Godot."""
    img = Imagem(28, 96)
    X, Y = img.X, img.Y
    img.pintar(img.ret(12, 24, 16, 90), "inox", 0.36 + 0.4 * (X == 12) - 0.1 * (X == 15))
    img.pintar(img.elipse(14, 92, 8, 3), "inox", 0.34)
    img.pintar(img.elipse(14, 91, 6, 2), "inox", 0.5)
    img.pintar(img.ret(10, 18, 18, 26), "inox", 0.5 + 0.2 * (Y == 18))
    img.pintar(img.elipse(14, 12, 9, 9), "neon_ambar", 0.6 + 0.35 * (1 - np.clip(((X - 12) ** 2 + (Y - 10) ** 2) / 70.0, 0, 1)))
    img.pintar(img.elipse(13, 10, 4, 4), "neon_ambar", 1.0, achatar=False)
    img.pintar(img.ret(5, 20, 23, 22), "inox", 0.3)
    img.contornar()
    return img, 14, 94


def vaso_planta():
    """Vaso grande de cerâmica escura com uma planta de folhas largas que
    brilham em ciano e verde, e as flores em ponta."""
    img = Imagem(44, 56)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(1750)
    vaso = img.poligono([(8, 34), (36, 34), (33, 52), (11, 52)])
    img.pintar(vaso, "grafite", 0.2 + 0.3 * (1 - np.clip(np.abs(X - 18) / 14.0, 0, 1)) - 0.1 * (X > 30))
    img.pintar(img.ret(6, 32, 38, 36), "grafite", 0.45 + 0.15 * (Y == 32))
    neon_linha(img, img.ret(9, 44, 35, 45), "bioluz", 0.55)
    for k in range(9):
        a = math.radians(-70 + k * 17.5 + rng.uniform(-4, 4))
        comp = rng.uniform(16, 28)
        x1, y1 = 22 + comp * math.sin(a), 34 - comp * math.cos(a)
        img.pintar(img.caminho([(22, 34), ((22 + x1) / 2, 30 - comp * 0.3), (x1, y1)], 0.7), "verde", 0.4 + 0.2 * rng.random())
        folha = img.elipse(x1, y1, rng.uniform(4, 7), rng.uniform(2.5, 4))
        img.pintar(folha, "bioluz", 0.5 + 0.4 * rng.random())
        img.pintar(img.ret(int(x1) - 1, int(y1) - 1, int(x1) + 1, int(y1)), "bioluz", 1.0, achatar=False)
    img.contornar()
    return img, 22, 52


def arvore_cupula():
    """Árvore que cresceu sob a cúpula: tronco retorcido de raízes grossas, a
    copa em nuvens de folhas que brilham em verde-água e as trepadeiras. É a
    árvore velha da Biblioteca, mas de outro mundo: 1000 anos depois, ela
    ficou azul."""
    W, Hh = 128, 168
    img = Imagem(W, Hh)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(1760)
    # Tronco: largura que afina para cima, com torção; raízes abertas na base.
    topo_tronco = 70
    eixo = 64 + 5 * np.sin((Y - topo_tronco) / 18.0)
    largura = 7 + 9 * np.clip((Y - topo_tronco) / 90.0, 0, 1)
    tronco = (Y >= topo_tronco) & (Y < 156) & (np.abs(X + 0.5 - eixo) < largura)
    sombra_t = np.clip((X + 0.5 - (eixo - largura)) / (2 * largura), 0, 1)
    img.pintar(tronco, "casca", 0.62 - 0.4 * sombra_t + 0.16 * ciclico(W, Hh, 2, 8, 1761))
    img.pintar(tronco & (ciclico(W, Hh, 3, 20, 1762) > 0.7), "casca", 0.18, achatar=False)
    for dx, sinal in ((-18, -1), (-8, -1), (8, 1), (20, 1)):
        raiz = img.caminho([(64 + dx * 0.2, 140), (64 + dx * 0.7, 152), (64 + dx * 1.3, 158)], 3.2 - abs(dx) / 14.0)
        img.pintar(raiz, "casca", 0.44 - 0.14 * (sinal > 0) + 0.1 * ciclico(W, Hh, 2, 2, 1763))
    # Ramos principais.
    for (x1, y1, esp) in ((26, 56, 4.0), (104, 52, 4.0), (46, 36, 3.2), (86, 30, 3.0), (64, 22, 3.4)):
        ramo = img.caminho([(64, 94), ((64 + x1) / 2 + rng.uniform(-6, 6), (94 + y1) / 2), (x1, y1)], esp)
        img.pintar(ramo, "casca", 0.42 + 0.14 * rng.random())
    # A copa: nuvens de folhas (elipses) com o tom mais claro em cima.
    centros = [(30, 54, 24, 16), (98, 50, 24, 16), (48, 34, 26, 16), (82, 28, 26, 15), (64, 20, 22, 14),
               (16, 66, 12, 8), (112, 62, 12, 8), (64, 46, 20, 12)]
    for (cx, cy, rx, ry) in centros:
        nuvem = img.elipse(cx, cy, rx, ry) & (ruido(W, Hh, 5, 4, 1764) + 0.2 > 0.35)
        img.pintar(nuvem, "bioluz", 0.3 + 0.38 * (1 - (Y - (cy - ry)) / (2.0 * ry)) + 0.1 * ciclico(W, Hh, 2, 2, 1765))
    folhas = ruido(W, Hh, 4, 4, 1766) > 0.78
    copa = np.zeros((Hh, W), dtype=bool)
    for (cx, cy, rx, ry) in centros:
        copa |= img.elipse(cx, cy, rx, ry)
    img.pintar(copa & folhas, "bioluz", 0.95, achatar=False)
    # Trepadeiras caindo da copa.
    for x0 in (20, 40, 88, 108):
        cipo = img.caminho([(x0 + 3 * math.sin(k * 0.7), 58 + k * 9) for k in range(9)], 0.7)
        img.pintar(cipo, "verde", 0.34 + 0.22 * rng.random())
    img.contornar()
    return img, 64, 156


def totem_pedidos():
    """Totem de pedidos: um poste com a tela do cardápio acesa (na cor ciano),
    o leitor de pagamento e uma luzinha de ligado."""
    img = Imagem(30, 62)
    X, Y = img.X, img.Y
    img.pintar(img.ret(11, 40, 19, 56), "inox", 0.4 + 0.3 * (X == 11) - 0.1 * (X == 18))
    img.pintar(img.elipse(15, 58, 10, 3), "inox", 0.36)
    img.pintar(img.poligono([(3, 6), (27, 6), (27, 40), (3, 40)]), "inox", 0.36 + 0.3 * (Y == 6) + 0.14 * (X == 3))
    img.pintar(img.ret(6, 9, 24, 30), "grafite", 0.05)
    for k, y in enumerate(range(11, 28, 5)):
        neon_linha(img, img.ret(8, y, 8 + 8 + (k * 5) % 9, y + 1), "ciano", 0.7)
        neon_linha(img, img.ret(20, y, 22, y + 1), "ciano", 0.9)
    img.pintar(img.ret(6, 32, 24, 38), "grafite", 0.1)
    img.cor(img.ret(8, 34, 10, 36), base.hexa("#6cf28e")[0])
    img.pintar(img.ret(14, 33, 22, 37), "grafite", 0.22)
    img.contornar()
    return img, 15, 59


def holograma_central():
    """O holograma do emblema da praça: o disco emissor no chão e, flutuando,
    três anéis girando em volta de uma esfera de luz."""
    img = Imagem(96, 120)
    X, Y = img.X, img.Y
    img.pintar(img.elipse(48, 112, 36, 9), "inox", 0.3)
    img.pintar(img.elipse(48, 110, 34, 8), "inox", 0.46)
    img.pintar(img.elipse(48, 110, 26, 6), "grafite", 0.1)
    neon_linha(img, img.elipse(48, 110, 28, 7) & ~img.elipse(48, 110, 27, 6), "ciano", 0.9)
    feixe = img.poligono([(40, 108), (56, 108), (60, 40), (36, 40)]) & (((X + Y) % 3) == 0)
    img.pintar(feixe, "ciano", 0.14, achatar=False)
    esfera = img.elipse(48, 50, 16, 16)
    d2 = ((X - 44) ** 2 + (Y - 45) ** 2) / 220.0
    img.pintar(esfera, "ciano", np.clip(0.95 - 0.55 * d2, 0.25, 1.0))
    img.pintar(img.elipse(44, 45, 5, 5), "ciano", 1.0, achatar=False)
    for (rx, ry, inc) in ((34, 8, 0), (30, 14, 40), (22, 20, -35)):
        a = math.radians(inc)
        pontos = [(48 + rx * math.cos(t) * math.cos(a) - ry * math.sin(t) * math.sin(a),
                   50 + rx * math.cos(t) * math.sin(a) + ry * math.sin(t) * math.cos(a))
                  for t in np.linspace(0, 2 * np.pi, 80)]
        img.pintar(img.caminho(pontos, 0.55), "ciano", 0.78, achatar=False)
    img.contornar() if False else None
    return img, 48, 112


# ---------------------------------------------------------------------------
# Tapioca Orbital
# ---------------------------------------------------------------------------


def balcao_tapioca():
    """Balcão da tapiocaria: tampo de madeira clara com a chapa redonda de
    tapioca acesa (âmbar), um fumacinha, potes de recheio e o painel frontal
    de ripas com o friso de neon."""
    img = Imagem(112, 56)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 22, 110, 52), "madeira_fut", 0.4 + 0.3 * (Y == 22) * 0 + 0.06 * ciclico(112, 56, 2, 2, 1800))
    img.pintar(img.ret(2, 22, 110, 52) & ((X % 6) == 0), "madeira_fut", 0.2, achatar=False)
    img.pintar(img.ret(0, 18, 112, 24), "ceramica", 0.64 + 0.2 * (Y == 18))
    img.pintar(img.ret(0, 24, 112, 26), "grafite", 0.14)
    neon_linha(img, img.ret(4, 48, 108, 49), "neon_ambar", 0.7)
    # Chapa redonda.
    img.pintar(img.elipse(34, 18, 20, 4.5), "inox", 0.3)
    img.pintar(img.elipse(34, 17, 18, 3.5), "neon_ambar", 0.5 + 0.35 * ((X - 34) < 0))
    img.pintar(img.elipse(34, 17, 10, 2), "neon_ambar", 0.9, achatar=False)
    for x in (24, 30, 38, 44):
        img.pintar(img.ret(x, 6 - (x % 5), x + 1, 14), "ceramica", 0.35 + 0.2 * ((x % 3) == 0), achatar=False)
    # Potes de recheio.
    for k, (x, rampa) in enumerate(((66, "neon_vermelho"), (76, "neon_verde"), (86, "neon_ambar"), (96, "neon_magenta"))):
        img.pintar(img.ret(x, 8, x + 8, 19), rampa, 0.4 + 0.18 * (X == x) + 0.1 * k)
        img.pintar(img.ret(x - 1, 6, x + 9, 9), "inox", 0.6)
    # Luminária de bancada.
    img.pintar(img.ret(56, 2, 58, 18), "inox", 0.5)
    img.pintar(img.ret(52, 0, 64, 4), "inox", 0.6)
    img.pintar(img.ret(54, 4, 62, 6), "neon_ambar", 0.9, achatar=False)
    img.contornar()
    return img, 56, 52


def maquina_cafe():
    """Máquina de café futurista: torre de aço com o visor ciano, a saída
    dupla e a xícara que gira acesa."""
    img = Imagem(36, 58)
    X, Y = img.X, img.Y
    img.pintar(img.ret(4, 4, 32, 52), "inox", 0.36 + 0.3 * (X < 8) + 0.14 * (Y < 6))
    img.pintar(img.ret(8, 8, 28, 22), "grafite", 0.06)
    neon_linha(img, img.ret(10, 11, 26, 12), "ciano", 0.85)
    neon_linha(img, img.ret(10, 15, 20, 16), "ciano", 0.6)
    img.pintar(img.ret(11, 28, 15, 36), "inox", 0.7)
    img.pintar(img.ret(21, 28, 25, 36), "inox", 0.7)
    img.pintar(img.ret(14, 44, 22, 52), "ceramica", 0.8)
    img.pintar(img.ret(8, 38, 28, 44), "grafite", 0.14)
    img.cor(img.ret(6, 24, 8, 26), base.hexa("#ffc24a")[0])
    img.pintar(img.ret(2, 52, 34, 56), "inox", 0.3)
    img.contornar()
    return img, 18, 56


def mesa_cafe():
    """Mesinha alta de dois lugares: tampo redondo de madeira com o prato de
    tapioca em cima e uma luz âmbar na borda."""
    img = Imagem(40, 44)
    X, Y = img.X, img.Y
    img.pintar(img.ret(18, 20, 22, 38), "inox", 0.36 + 0.3 * (X == 18))
    img.pintar(img.elipse(20, 40, 12, 3), "inox", 0.3)
    img.pintar(img.elipse(20, 18, 17, 6), "grafite", 0.16)
    img.pintar(img.elipse(20, 17, 17, 6), "madeira_fut", 0.52 + 0.2 * ((X - 20) < -4))
    neon_linha(img, img.elipse(20, 17, 17, 6) & ~img.elipse(20, 17, 16, 5), "neon_ambar", 0.7)
    img.pintar(img.elipse(15, 15, 5, 2), "ceramica", 0.82)
    img.pintar(img.elipse(15, 14, 3, 1), "neon_ambar", 0.7, achatar=False)
    img.pintar(img.ret(25, 11, 29, 15), "ceramica", 0.7)
    img.contornar()
    return img, 20, 41


def banqueta():
    """Banqueta alta: assento redondo estofado, haste e o apoio de pés."""
    img = Imagem(22, 38)
    X, Y = img.X, img.Y
    img.pintar(img.ret(9, 12, 13, 32), "inox", 0.4 + 0.3 * (X == 9))
    img.pintar(img.elipse(11, 34, 8, 2.5), "inox", 0.32)
    img.pintar(img.elipse(11, 24, 6, 1.5), "inox", 0.55)
    img.pintar(img.elipse(11, 12, 9, 4), "grafite", 0.14)
    img.pintar(img.elipse(11, 11, 9, 4), "couro", 0.48 + 0.2 * ((X - 11) < -2))
    img.contornar()
    return img, 11, 35


def estufa_salgados():
    """Estufa de vidro iluminada (âmbar) com salgados e pães nas bandejas."""
    img = Imagem(48, 56)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 4, 46, 50), "inox", 0.36 + 0.3 * (X < 5) + 0.14 * (Y < 6))
    vidro = img.ret(5, 8, 43, 42)
    img.pintar(vidro, "grafite", 0.06)
    img.pintar(vidro, "neon_ambar", 0.14 + 0.1 * (Y < 18))
    for y in (18, 28, 38):
        img.pintar(img.ret(5, y, 43, y + 2), "inox", 0.5)
        x = 8
        while x < 40:
            larg = 5 + (x * 3) % 4
            img.pintar(img.ret(x, y - 5, x + larg, y), "madeira_fut", 0.6 + 0.2 * ((x % 2) == 0))
            img.pintar(img.ret(x, y - 5, x + larg, y - 4), "neon_ambar", 0.7, achatar=False)
            x += larg + 2
    img.pintar(img.ret(3, 44, 45, 52), "grafite", 0.14)
    neon_linha(img, img.ret(5, 46, 43, 47), "neon_ambar", 0.8)
    reflexo = vidro & ((np.abs((X - Y) + 12) < 1.5) | (np.abs((X - Y) + 2) < 0.8))
    img.pintar(reflexo, "gelo", 0.6, achatar=False)
    img.contornar()
    return img, 24, 52


# ---------------------------------------------------------------------------
# Self Nebulosa
# ---------------------------------------------------------------------------


def bufe():
    """Balcão de bufê: protetor de vidro curvo em cima, cubas de comida com
    luzes de aquecimento verdes (cada cuba de uma cor), a pista de bandejas
    na frente e o painel do balcão com o friso de neon verde."""
    W, Hh = 144, 64
    img = Imagem(W, Hh)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 34, 142, 60), "inox", 0.34 + 0.3 * (Y == 34) * 0 + 0.06 * ciclico(W, Hh, 2, 2, 1810))
    img.pintar(img.ret(2, 34, 142, 60) & ((X % 24) == 0), "inox", 0.14, achatar=False)
    img.pintar(img.ret(0, 30, W, 36), "inox", 0.62 + 0.2 * (Y == 30))
    neon_linha(img, img.ret(4, 55, 140, 56), "neon_verde", 0.7)
    comidas = ("neon_vermelho", "neon_ambar", "neon_verde", "neon_violeta", "neon_ambar", "neon_vermelho")
    for k, rampa in enumerate(comidas):
        x0 = 6 + k * 23
        img.pintar(img.ret(x0, 26, x0 + 20, 31), "inox", 0.3)
        img.pintar(img.ret(x0 + 1, 22, x0 + 19, 28), rampa, 0.34 + 0.22 * ((X - x0) % 5 == 0) + 0.06 * k)
        img.pintar(img.ret(x0 + 1, 22, x0 + 19, 23), rampa, 0.8, achatar=False)
    protetor = img.ret(2, 4, 142, 26) & ~img.ret(4, 6, 140, 24)
    img.pintar(protetor, "gelo", 0.6, achatar=False)
    img.pintar(img.ret(4, 6, 140, 24) & ((X + Y) % 9 == 0), "gelo", 0.4, achatar=False)
    for x in range(8, 140, 23):
        img.pintar(img.ret(x, 4, x + 1, 22), "inox", 0.6)
        img.pintar(img.ret(x - 3, 2, x + 4, 4), "neon_verde", 0.85, achatar=False)
    img.pintar(img.ret(4, 60, 140, 62), "grafite", 0.1)
    img.contornar()
    return img, 72, 60


def rack_bandejas():
    """Carrinho de bandejas e pratos empilhados, com os pratos brancos."""
    img = Imagem(30, 56)
    X, Y = img.X, img.Y
    img.pintar(img.ret(3, 4, 5, 46), "inox", 0.5 + 0.2 * (X == 3))
    img.pintar(img.ret(25, 4, 27, 46), "inox", 0.4)
    for y in (12, 24, 36):
        img.pintar(img.ret(3, y, 27, y + 2), "inox", 0.6 + 0.2 * (Y == y))
        for x in range(6, 25, 5):
            img.pintar(img.ret(x, y - 4, x + 4, y), "ceramica", 0.84)
            img.pintar(img.ret(x, y - 4, x + 4, y - 3), "ceramica", 0.98, achatar=False)
    for (x, y) in ((6, 50), (23, 50)):
        img.pintar(img.elipse(x, y, 3, 3), "grafite", 0.14)
    img.pintar(img.ret(2, 46, 28, 49), "inox", 0.4)
    img.contornar()
    return img, 15, 52


def mesa_vidro():
    """Mesa quadrada de tampo de vidro (visto em perspectiva) com a borda
    de neon verde e o apoio central."""
    img = Imagem(60, 46)
    X, Y = img.X, img.Y
    img.pintar(img.ret(27, 20, 33, 40), "inox", 0.34 + 0.3 * (X == 27))
    img.pintar(img.elipse(30, 41, 14, 3), "inox", 0.3)
    tampo = img.poligono([(8, 14), (52, 14), (58, 24), (2, 24)])
    img.pintar(img.poligono([(8, 16), (52, 16), (58, 26), (2, 26)]), "grafite", 0.14)
    img.pintar(tampo, "gelo", 0.3 + 0.16 * (Y < 17))
    reflexo = tampo & ((np.abs((X * 1.0 - Y * 2) + 4) < 2) | (np.abs((X * 1.0 - Y * 2) + 28) < 1))
    img.pintar(reflexo, "gelo", 0.8, achatar=False)
    neon_linha(img, tampo & ~img.poligono([(9, 15), (51, 15), (56, 23), (4, 23)]), "neon_verde", 0.75)
    img.contornar()
    return img, 30, 42


def lixeira_reciclagem():
    img = Imagem(20, 34)
    X, Y = img.X, img.Y
    img.pintar(img.ret(3, 6, 17, 30), "inox", 0.36 + 0.3 * (X < 7))
    img.pintar(img.ret(1, 4, 19, 8), "inox", 0.55 + 0.2 * (Y == 4))
    img.pintar(img.ret(6, 12, 14, 22), "neon_verde", 0.5)
    img.pintar(img.ret(8, 14, 12, 20), "grafite", 0.1)
    neon_linha(img, img.ret(8, 16, 12, 17), "neon_verde", 0.9)
    img.contornar()
    return img, 10, 31


# ---------------------------------------------------------------------------
# Câmara fria
# ---------------------------------------------------------------------------


def prateleira_fria():
    """Estante de aço da câmara: três prateleiras com caixas térmicas, gelo
    pendurado e geada nos cantos."""
    img = Imagem(76, 76)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(1830)
    img.pintar(img.ret(3, 4, 6, 72), "inox", 0.5 + 0.2 * (X == 3))
    img.pintar(img.ret(70, 4, 73, 72), "inox", 0.4)
    for y in (24, 46, 68):
        img.pintar(img.ret(3, y, 73, y + 3), "inox", 0.55 + 0.2 * (Y == y))
        x = 8
        while x < 66:
            larg = int(rng.integers(10, 18))
            alt = int(rng.integers(10, 18))
            rampa = ("gelo", "inox", "gelo", "neon_verde")[int(rng.integers(0, 4))]
            img.pintar(img.ret(x, y - alt, x + larg, y), rampa, 0.4 + 0.2 * rng.random() + 0.14 * (X == x))
            img.pintar(img.ret(x, y - alt, x + larg, y - alt + 2), "gelo", 0.8)
            img.pintar(img.ret(x + 2, y - alt + 5, x + larg - 2, y - alt + 7), "grafite", 0.2)
            x += larg + 2
    geada = ruido(76, 76, 6, 6, 1831) > 0.7
    img.pintar(geada & (img.opaco() | True) & img.ret(2, 3, 74, 74), "gelo", 0.5, achatar=False) if False else None
    for x in (14, 30, 52, 64):
        img.pintar(img.ret(x, 3, x + 1, 8), "gelo", 0.85, achatar=False)
        img.pintar(img.ret(x, 8, x + 1, 10), "gelo", 0.6, achatar=False)
    img.contornar()
    return img, 38, 74


def caixas_termicas():
    """Pilha de caixas térmicas azuis e brancas com tampas e gelo escorrendo."""
    img = Imagem(48, 40)
    X, Y = img.X, img.Y
    for (x0, y0, x1, y1, rampa) in ((2, 20, 26, 38, "gelo"), (24, 24, 46, 38, "inox"), (6, 8, 22, 20, "gelo")):
        img.pintar(img.ret(x0, y0, x1, y1), rampa, 0.46 + 0.28 * (Y == y0) + 0.12 * (X == x0) - 0.08 * (X == x1 - 1))
        img.pintar(img.ret(x0, y0 + 3, x1, y0 + 4), rampa, 0.24)
        img.pintar(img.ret((x0 + x1) // 2 - 3, y0 + 6, (x0 + x1) // 2 + 3, y0 + 8), "inox", 0.78)
    img.pintar(img.ret(2, 36, 46, 38) & ((X % 3) == 0), "gelo", 0.9, achatar=False)
    img.contornar()
    return img, 24, 38


def tanque_cripto():
    """Tanque criogênico: um cilindro de vidro fosco com névoa fria lá
    dentro, tampa e base de aço, medidor de temperatura e a geada."""
    img = Imagem(36, 76)
    X, Y = img.X, img.Y
    img.pintar(img.ret(4, 8, 32, 64), "gelo", 0.18 + 0.4 * tom_cilindro(img, 4, 32))
    img.pintar(img.ret(6, 40, 30, 64) & (ruido(36, 76, 5, 4, 1840) > 0.4), "gelo", 0.7, achatar=False)
    img.pintar(img.ret(4, 4, 32, 10), "inox", 0.5 + 0.2 * (Y == 4))
    img.pintar(img.ret(2, 62, 34, 70), "inox", 0.4 + 0.2 * (Y == 62))
    img.pintar(img.ret(8, 70, 28, 74), "inox", 0.28)
    img.pintar(img.ret(14, 14, 22, 24), "grafite", 0.06)
    neon_linha(img, img.ret(15, 17, 21, 18), "ciano", 0.9)
    neon_linha(img, img.ret(15, 20, 19, 21), "ciano", 0.55)
    img.pintar(img.ret(4, 8, 32, 64) & ((np.abs((X - Y) + 14) < 1.4)), "gelo", 0.95, achatar=False)
    img.contornar()
    return img, 18, 72


def gerador_frio():
    """Gerador reserva da câmara fria: carcaça de aço com as faixas de perigo,
    mostradores, o encaixe vazio (onde a célula de energia ficava) e cabos."""
    img = Imagem(64, 60)
    X, Y = img.X, img.Y
    img.pintar(img.ret(3, 10, 61, 54), "inox", 0.34 + 0.3 * (Y == 10) + 0.14 * (X == 3) - 0.08 * (X == 60))
    img.pintar(img.ret(3, 46, 61, 54), "grafite", 0.14)
    for x in range(4, 60, 8):
        img.pintar(img.poligono([(x, 54), (x + 4, 54), (x + 8, 46), (x + 4, 46)]), "neon_ambar", 0.8, achatar=False)
    img.pintar(img.ret(8, 16, 34, 40), "grafite", 0.08)
    img.pintar(img.ret(10, 18, 32, 38), "grafite", 0.04)
    neon_linha(img, img.ret(14, 24, 28, 25), "ciano", 0.3)
    neon_linha(img, img.ret(14, 28, 24, 29), "ciano", 0.3)
    img.pintar(img.elipse(48, 26, 7, 7), "inox", 0.55)
    img.pintar(img.elipse(48, 26, 5, 5), "grafite", 0.08)
    img.pintar(img.linha(48, 26, 51, 22, 0.5), "neon_vermelho", 0.9, achatar=False)
    img.pintar(img.ret(40, 38, 58, 44), "grafite", 0.1)
    for x in (42, 47, 52):
        img.cor(img.ret(x, 40, x + 2, 42), (base.hexa("#6cf28e")[0], base.hexa("#ffc24a")[0], base.hexa("#ff5a3a")[0])[(x // 5) % 3])
    img.pintar(img.ret(14, 2, 18, 10), "inox", 0.5)
    img.pintar(img.caminho([(50, 12), (54, 4), (62, 2)], 1.4), "grafite", 0.14)
    img.contornar()
    return img, 32, 56


# ---------------------------------------------------------------------------
# Pizzaria Quasar
# ---------------------------------------------------------------------------


def forno_plasma():
    """Forno de plasma: bloco de aço escuro com a boca em arco acesa de laranja,
    a chaminé com o anel de luz e o painel de temperatura."""
    img = Imagem(88, 92)
    X, Y = img.X, img.Y
    img.pintar(img.ret(36, 0, 52, 24), "inox", 0.32 + 0.3 * (X < 40))
    img.pintar(img.ret(32, 22, 56, 28), "inox", 0.5)
    corpo = img.ret(6, 28, 82, 86)
    img.pintar(corpo, "inox", 0.3 + 0.1 * ciclico(88, 92, 2, 2, 1850) + 0.14 * (Y == 28) + 0.08 * (X < 10))
    img.pintar(img.ret(6, 28, 82, 36), "tijolo", 0.5 + 0.2 * (Y == 28))
    boca = img.elipse(44, 62, 24, 20) & (Y > 44)
    boca |= img.ret(20, 56, 68, 82)
    img.pintar(boca, "grafite", 0.04)
    d = np.sqrt(((X - 44) / 24.0) ** 2 + ((Y - 70) / 22.0) ** 2)
    img.pintar(boca, "neon_vermelho", np.clip(0.9 - 0.7 * d, 0.1, 1.0))
    img.pintar(boca & (d < 0.4), "neon_ambar", 0.95, achatar=False)
    img.pintar(dilatar(boca) & ~boca & corpo, "inox", 0.62)
    img.pintar(img.ret(4, 84, 84, 90), "grafite", 0.12)
    img.pintar(img.ret(10, 40, 24, 50), "grafite", 0.06)
    neon_linha(img, img.ret(12, 43, 22, 44), "neon_vermelho", 0.9)
    neon_linha(img, img.ret(12, 46, 18, 47), "neon_ambar", 0.7)
    img.pintar(img.ret(66, 40, 78, 50), "grafite", 0.06)
    img.cor(img.ret(70, 44, 74, 46), base.hexa("#ffc24a")[0])
    img.contornar()
    return img, 44, 88


def bancada_inox():
    """Bancada de aço da cozinha com a massa aberta, o rolo, as caixas de
    ingredientes e a prateleira de utensílios por baixo."""
    img = Imagem(96, 50)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 18, 94, 46), "inox", 0.34 + 0.06 * ciclico(96, 50, 2, 2, 1860))
    img.pintar(img.ret(2, 18, 94, 46) & ((X % 32) == 0), "inox", 0.14, achatar=False)
    img.pintar(img.ret(0, 14, 96, 20), "inox", 0.66 + 0.2 * (Y == 14))
    img.pintar(img.ret(2, 42, 94, 45), "inox", 0.2)
    img.pintar(img.ret(6, 22, 26, 38), "grafite", 0.08)
    img.pintar(img.ret(34, 22, 54, 38), "grafite", 0.08)
    img.pintar(img.elipse(40, 12, 16, 3), "ceramica", 0.78)
    img.pintar(img.elipse(40, 11, 14, 2), "ceramica", 0.92)
    img.pintar(img.ret(62, 11, 82, 13), "madeira_fut", 0.6)
    img.pintar(img.ret(60, 10, 63, 14), "madeira_fut", 0.4)
    for (x, rampa) in ((8, "neon_vermelho"), (14, "neon_verde"), (20, "neon_ambar")):
        img.pintar(img.ret(x, 6, x + 5, 14), rampa, 0.5)
    img.pintar(img.ret(66, 28, 90, 38), "neon_vermelho", 0.2, achatar=False)
    img.contornar()
    return img, 48, 46


def mesa_pizza():
    """Mesa redonda de aço com uma pizza inteira e as fatias em volta."""
    img = Imagem(56, 44)
    X, Y = img.X, img.Y
    img.pintar(img.ret(26, 18, 30, 36), "inox", 0.36 + 0.3 * (X == 26))
    img.pintar(img.elipse(28, 38, 12, 3), "inox", 0.3)
    img.pintar(img.elipse(28, 18, 25, 8), "grafite", 0.14)
    img.pintar(img.elipse(28, 17, 25, 8), "inox", 0.52 + 0.2 * ((X - 28) < -6))
    img.pintar(img.elipse(28, 16, 12, 4), "ferrugem", 0.5)
    img.pintar(img.elipse(28, 15, 10, 3), "neon_ambar", 0.55)
    for (x, y) in ((22, 15), (28, 14), (33, 16), (26, 17)):
        img.pintar(img.ret(x, y, x + 2, y + 1), "neon_vermelho", 0.7, achatar=False)
    img.contornar()
    return img, 28, 40


def caixas_pizza():
    img = Imagem(30, 40)
    X, Y = img.X, img.Y
    for k, y in enumerate((26, 16, 6)):
        img.pintar(img.ret(2 + k, y, 28 - k, y + 10), "madeira_fut", 0.6 + 0.2 * (Y == y) + 0.1 * k)
        img.pintar(img.ret(2 + k, y + 4, 28 - k, y + 5), "madeira_fut", 0.36)
        img.pintar(img.ret(11, y + 2, 19, y + 6), "neon_vermelho", 0.6)
    img.pintar(img.ret(0, 36, 30, 38), "grafite", 0.14)
    img.contornar()
    return img, 15, 38


# ---------------------------------------------------------------------------
# Churrasco Solar
# ---------------------------------------------------------------------------


def grelha_solar():
    """A grelha solar: uma torre vertical com cinco espetos que giram em volta
    de uma coluna de plasma magenta, o reservatório e o exaustor."""
    img = Imagem(88, 96)
    X, Y = img.X, img.Y
    img.pintar(img.ret(14, 74, 74, 90), "inox", 0.34 + 0.3 * (Y == 74) + 0.12 * (X == 14))
    img.pintar(img.ret(14, 84, 74, 90), "grafite", 0.14)
    img.pintar(img.ret(36, 6, 52, 14), "inox", 0.6 + 0.2 * (Y == 6))
    img.pintar(img.ret(40, 14, 48, 74), "neon_magenta", 0.2 + 0.45 * (1 - np.clip(np.abs(X - 44) / 4.0, 0, 1)))
    img.pintar(img.ret(43, 14, 45, 74), "neon_magenta", 0.98, achatar=False)
    base_y = (22, 34, 46, 58, 68)
    for k, y in enumerate(base_y):
        lado = -1 if k % 2 == 0 else 1
        img.pintar(img.ret(44 + (0 if lado > 0 else -24), y, 44 + (24 if lado > 0 else 0), y + 2), "inox", 0.6)
        for j in range(3):
            x = 46 + lado * (6 + j * 7) if lado > 0 else 42 - (6 + j * 7)
            img.pintar(img.ret(x, y - 6, x + 5, y), "ferrugem" if j % 2 else "neon_vermelho", 0.5 + 0.2 * j)
            img.pintar(img.ret(x, y - 6, x + 5, y - 5), "neon_ambar", 0.8, achatar=False)
    img.pintar(img.ret(10, 90, 78, 94), "grafite", 0.1)
    neon_linha(img, img.ret(16, 87, 72, 88), "neon_magenta", 0.7)
    img.contornar()
    return img, 44, 92


def balcao_bar():
    """Balcão do bar: tampo de vidro escuro com o friso de neon magenta, o
    painel frontal de couro com os pontos de luz e o apoio de pés."""
    W, Hh = 144, 56
    img = Imagem(W, Hh)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 24, 142, 52), "couro", 0.4 + 0.1 * ciclico(W, Hh, 2, 2, 1870))
    losango = (((X + (Y - 24)) % 14) == 0) | (((X - (Y - 24)) % 14) == 0)
    img.pintar(img.ret(2, 24, 142, 52) & losango, "couro", 0.14, achatar=False)
    img.pintar(img.ret(2, 24, 142, 52) & (((X % 14) == 7) & (((Y - 24) % 14) == 7)), "neon_magenta", 0.8, achatar=False)
    img.pintar(img.ret(0, 18, W, 26), "grafite", 0.22 + 0.2 * (Y == 18))
    neon_linha(img, img.ret(2, 24, 142, 25), "neon_magenta", 0.85)
    img.pintar(img.ret(2, 50, 142, 54), "inox", 0.4 + 0.14 * (Y == 50))
    for x in (20, 60, 100):
        img.pintar(img.ret(x, 8, x + 5, 18), "neon_violeta", 0.45)
        img.pintar(img.ret(x + 1, 4, x + 4, 8), "neon_violeta", 0.6)
    img.pintar(img.ret(118, 10, 130, 18), "ceramica", 0.7)
    img.contornar()
    return img, 72, 52


def banqueta_alta():
    """Banqueta de bar: assento de couro magenta, haste cromada e o apoio de pés."""
    img = Imagem(22, 42)
    X, Y = img.X, img.Y
    img.pintar(img.ret(9, 14, 13, 36), "inox", 0.42 + 0.3 * (X == 9))
    img.pintar(img.elipse(11, 38, 8, 2.5), "inox", 0.32)
    img.pintar(img.elipse(11, 28, 6, 1.6), "inox", 0.6)
    img.pintar(img.elipse(11, 14, 9, 4), "grafite", 0.14)
    img.pintar(img.elipse(11, 13, 9, 4), "couro", 0.5 + 0.2 * ((X - 11) < -2))
    neon_linha(img, img.elipse(11, 13, 9, 4) & ~img.elipse(11, 13, 8, 3), "neon_magenta", 0.8)
    img.contornar()
    return img, 11, 39


def caixas_carga():
    """Caixas e paletes de carga do elevador, com as faixas de perigo."""
    img = Imagem(64, 48)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 40, 62, 46), "madeira_fut", 0.4)
    img.pintar(img.ret(2, 40, 62, 41), "madeira_fut", 0.6)
    for (x0, y0, x1, y1, rampa) in ((4, 16, 30, 40, "inox"), (32, 20, 60, 40, "grafite"), (10, 2, 26, 16, "inox")):
        img.pintar(img.ret(x0, y0, x1, y1), rampa, 0.38 + 0.28 * (Y == y0) + 0.12 * (X == x0) - 0.08 * (X == x1 - 1))
        img.pintar(img.ret(x0, y0 + 4, x1, y0 + 5), rampa, 0.18)
        for x in range(x0 + 2, x1 - 4, 8):
            img.pintar(img.poligono([(x, y1 - 2), (x + 3, y1 - 2), (x + 6, y1 - 7), (x + 3, y1 - 7)]), "neon_ambar", 0.75, achatar=False)
    img.contornar()
    return img, 32, 46


def elevador_carga():
    """A porta do elevador de carga: duas folhas de aço grosso com as faixas
    de perigo, o painel de andares e a luz de status (vermelha enquanto está
    sem energia). É o sprite da comporta que se recolhe (GradeSeguranca)."""
    img = Imagem(64, 84)
    X, Y = img.X, img.Y
    img.pintar(img.ret(0, 0, 64, 84), "inox", 0.4 + 0.14 * (Y == 0) + 0.1 * (X == 0) - 0.1 * (X == 63))
    img.pintar(img.ret(6, 8, 58, 80), "grafite", 0.1)
    for (xa, xb) in ((7, 32), (32, 57)):
        img.pintar(img.ret(xa, 9, xb, 79), "inox", 0.34 + 0.08 * ciclico(64, 84, 2, 2, 1880) + 0.16 * (X == xa))
        for y in range(16, 74, 14):
            img.pintar(img.ret(xa + 2, y, xb - 2, y + 2), "inox", 0.2)
    img.pintar(img.ret(31, 9, 33, 79), "grafite", 0.06)
    for y in range(60, 79, 4):
        for x in range(8, 56, 6):
            img.pintar(img.poligono([(x, y + 4), (x + 3, y + 4), (x + 6, y), (x + 3, y)]), "neon_ambar", 0.75, achatar=False)
    img.pintar(img.ret(24, 1, 40, 7), "grafite", 0.06)
    img.cor(img.ret(30, 3, 34, 5), base.hexa("#ff5a3a")[0])
    img.pintar(img.ret(58, 36, 62, 48), "grafite", 0.06)
    img.cor(img.ret(59, 38, 61, 39), base.hexa("#ff5a3a")[0])
    img.cor(img.ret(59, 42, 61, 43), base.hexa("#ffc24a")[0])
    return img, 0, 0


def cacos_louca():
    """Cacos de louça branca e de vidro espalhados (o que sobrou das bandejas):
    ladrilhos fininhos que fazem barulho no piso, como o tapete de cacos de antes."""
    img = Imagem(80, 30)
    rng = np.random.default_rng(1890)
    for _ in range(46):
        x, y = int(rng.integers(2, 76)), int(rng.integers(2, 26))
        rampa, tom = (("ceramica", 0.9) if rng.random() > 0.45 else ("gelo", 0.7))
        img.pintar(img.ret(x, y, x + 2 + int(rng.integers(0, 2)), y + 1), rampa, tom, achatar=False)
        if rng.random() > 0.6:
            img.pintar(img.ret(x + 1, y + 1, x + 2, y + 2), "inox", 0.4, achatar=False)
    for _ in range(4):
        x, y = int(rng.integers(8, 68)), int(rng.integers(6, 22))
        img.pintar(img.elipse(x, y, 5, 2.5), "ceramica", 0.84)
        img.pintar(img.elipse(x, y, 3, 1.4), "ceramica", 0.6)
    return img, 0, 0


OBJETOS = {
    # praça
    "cadeira_fut": (cadeira_fut, (12, 4)),
    "mesa_holo": (mesa_holo, (44, 8)),
    "banco_curvo": (banco_curvo, (66, 6)),
    "guarda_sol_holo": (guarda_sol_holo, (16, 5)),
    "poste_luz": (poste_luz, (8, 4)),
    "vaso_planta": (vaso_planta, (24, 6)),
    "arvore_cupula": (arvore_cupula, (30, 9)),
    "totem_pedidos": (totem_pedidos, (10, 4)),
    "holograma_central": (holograma_central, (50, 10)),
    # tapioca orbital
    "balcao_tapioca": (balcao_tapioca, (104, 8)),
    "maquina_cafe": (maquina_cafe, (28, 6)),
    "mesa_cafe": (mesa_cafe, (24, 6)),
    "banqueta": (banqueta, (12, 4)),
    "estufa_salgados": (estufa_salgados, (42, 6)),
    # self nebulosa
    "bufe": (bufe, (136, 8)),
    "rack_bandejas": (rack_bandejas, (24, 5)),
    "mesa_vidro": (mesa_vidro, (46, 7)),
    "lixeira_reciclagem": (lixeira_reciclagem, (14, 4)),
    # câmara fria
    "prateleira_fria": (prateleira_fria, (68, 7)),
    "caixas_termicas": (caixas_termicas, (42, 6)),
    "tanque_cripto": (tanque_cripto, (24, 6)),
    "gerador_frio": (gerador_frio, (58, 8)),
    # pizzaria quasar
    "forno_plasma": (forno_plasma, (80, 9)),
    "bancada_inox": (bancada_inox, (88, 7)),
    "mesa_pizza": (mesa_pizza, (22, 6)),
    "caixas_pizza": (caixas_pizza, (24, 5)),
    # churrasco solar
    "grelha_solar": (grelha_solar, (66, 8)),
    "balcao_bar": (balcao_bar, (136, 8)),
    "banqueta_alta": (banqueta_alta, (12, 4)),
    "caixas_carga": (caixas_carga, (56, 6)),
}

# Peças sem pegada (enfeites de chão e a porta do elevador): saem à parte.
ENFEITES = {"cacos_louca": cacos_louca, "elevador_carga": elevador_carga}


def main():
    print("Gerando os objetos da praça em assets/sprites/cenario/praca/objetos")
    objetos = {}
    for nome, (f, pegada) in OBJETOS.items():
        img, px, py = f()
        base.salvar(img, f"{nome}.png", "objetos")
        print(f"    {nome}: pé em ({px}, {py}) -> offset = Vector2({-px}, {-py}), pegada {pegada}")
        objetos[nome] = img
    for nome, f in ENFEITES.items():
        img, _, _ = f()
        base.salvar(img, f"{nome}.png", "objetos")
        objetos[nome] = img
    lista = list(objetos.items())
    base.salvar_catalogo("praca_objetos", lista, 6, 2)


if __name__ == "__main__":
    main()
