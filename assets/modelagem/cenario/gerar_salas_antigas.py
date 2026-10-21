# gerar_salas_antigas.py — desenha, por código, as peças das duas SALAS
# ANTIGAS do bunker (docs/fases/bunker.md): interiores de casa montados lá
# embaixo, que mostram a obsessão do Carlos pelo passado SEM EXPLICAR
# (Enredo Principal, seção 8, Ato 3). Uma é a sala de visitas de um casarão
# do fim do século XIX; a outra, a sala de estar de uma casa dos anos 80.
#
# Mesmo estilo e mesmas medidas do kit do bunker (gerar_bunker.py), que este
# script importa: paleta, dithering, contorno, peças de 80 x 112 de parede,
# 128 px de chão e 128 x 64 de chão de fundo.
#
# Como rodar (Python 3 + numpy):
#
#   python assets/modelagem/cenario/gerar_salas_antigas.py
#
# O que sai (em assets/sprites/cenario/bunker/salas_antigas/):
#   paredes/<peça>.png   80 x 112: um pedaço da parede do fundo
#   chao/<peça>.png      128 x 68: o chão de perto; <peça>_fundo.png 128 x 64
#   objetos/<objeto>.png os móveis (y-sort); o "pé" de cada um sai no terminal
#
# ---------------------------------------------------------------------------
# O QUE CONTA QUE É UM CENÁRIO MONTADO NO BUNKER
# ---------------------------------------------------------------------------
#
# As duas salas parecem casas de verdade da cintura para baixo. Em cima, o
# papel de parede para alguns pixels antes do teto, e aparece a laje de
# concreto do bunker com a eletrocalha e os cabos: alguém montou a casa
# dentro do concreto. Ninguém explica (Enredo: "o jogo não diz quem as
# montou nem por quê").
#
#   - Século XIX: papel de parede vinho com listras e florzinhas, lambri de
#     madeira escura até a cintura, moldura dourada, janela de madeira com a
#     cortina pesada... e concreto atrás do vidro.
#   - Anos 80: papel de parede bege com o padrão geométrico marrom e
#     laranja, estante embutida com a TV de tubo e o videocassete, carpete.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "bunker", "salas_antigas")

_spec = importlib.util.spec_from_file_location("gerar_bunker", os.path.join(PASTA_SCRIPT, "gerar_bunker.py"))
bunker = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bunker)
kit = bunker.kit
bib = kit.bib

Imagem, RAMPAS, SOMBRA = bib.Imagem, bib.RAMPAS, bib.SOMBRA
ciclico = kit.ruido_ciclico
L = 80
Y_CHAO = kit.Y_CHAO
ALTURA = kit.ALTURA
LUZ = kit.LUZ

RAMPAS.update({
    "vinho": bib.hexa("#1c080c", "#2e0d14", "#45131d", "#5e1b28", "#7a2534", "#963243"),
    "dourado": bib.hexa("#2a1d06", "#4a330b", "#735212", "#9c741c", "#c49a2c", "#e3c056"),
    "nogueira": bib.hexa("#120a06", "#1e110a", "#2c1a0f", "#3c2415", "#4f301c", "#643e25"),
    "bege80": bib.hexa("#3a3226", "#5a4e3c", "#7d6f56", "#a09071", "#c0b08d", "#d9cba8"),
    "marrom80": bib.hexa("#1f140b", "#332012", "#4a2f1a", "#634024", "#7d5330", "#97683e"),
    "laranja80": bib.hexa("#3a1a06", "#5e2c0b", "#874112", "#b0591b", "#d37428", "#ea9440"),
    "verde80": bib.hexa("#161c10", "#243018", "#344521", "#465c2b", "#5a7436"),
})


def laje_do_bunker(img, semente):
    """O teto do bunker por cima da casa: laje de concreto e a eletrocalha
    com os cabos, como no kit do bunker. O papel de parede para em y = 20."""
    X, Y = img.X, img.Y
    fino = ciclico(L, Y_CHAO, 2, 2, 501)
    img.pintar(img.ret(0, 0, L, 20), "concreto", 0.12 + 0.06 * fino + 0.08 * (Y == 9))
    img.pintar(img.ret(0, 12, L, 15), "aco", 0.3 + 0.25 * (Y == 12))
    for k, (flecha, rampa, tom) in enumerate(((3, "aco", 0.12), (2, "vermelho", 0.3))):
        ys = 15.5 + k * 0.8 + flecha * np.sin(np.pi * ((X - 3) % 40) / 40)
        img.pintar((np.abs(Y + 0.5 - ys) < 0.6), rampa, tom, achatar=False)
    img.cor(img.ret(0, 20, L, 21), SOMBRA)
    return fino


# ---------------------------------------------------------------------------
# Século XIX
# ---------------------------------------------------------------------------


def parede_xix(semente=0):
    img = Imagem(L, Y_CHAO)
    X, Y = img.X, img.Y
    fino = laje_do_bunker(img, semente)
    manchas = ciclico(L, Y_CHAO, 40, 20, 510 + semente)
    papel = img.ret(0, 21, L, 66)
    listra = (X % 10) < 3
    img.pintar(papel, "vinho", 0.42 + 0.1 * manchas + 0.05 * fino + 0.12 * listra)
    flor = papel & ~listra & (((X % 10) == 6) & ((Y % 12) == 4) | ((X % 10) == 6) & ((Y % 12) == 5))
    img.pintar(flor, "dourado", 0.55, achatar=False)
    rasgado = (ciclico(L, Y_CHAO, 8, 8, 512 + semente) > 0.86) & img.ret(0, 21, L, 30)
    img.pintar(rasgado, "concreto", 0.25)
    img.pintar(img.ret(0, 64, L, 67), "nogueira", 0.7 + 0.2 * (Y == 64))
    lambri = img.ret(0, 67, L, 100)
    img.pintar(lambri, "nogueira", 0.45 + 0.06 * fino)
    for x0 in (4, 44):
        almofada = img.ret(x0, 72, x0 + 32, 95)
        img.pintar(almofada, "nogueira", 0.35 + 0.1 * (Y == 72) - 0.1 * (Y == 94))
    img.pintar(img.ret(0, 100, L, Y_CHAO), "nogueira", 0.25 + 0.15 * (Y == 100))
    img.fino, img.manchas = fino, manchas
    return img


def antiga_xix_papel():
    return parede_xix()


def antiga_xix_quadro():
    """Moldura dourada com uma paisagem escurecida: mar e coqueiro."""
    img = parede_xix(1)
    X, Y = img.X, img.Y
    img.pintar(img.ret(20, 26, 60, 58), "dourado", 0.5 + 0.3 * ((X + Y) % 5 == 0))
    tela = img.ret(24, 30, 56, 54)
    img.pintar(tela & (Y < 42), "vidro", 0.35)
    img.pintar(tela & (Y >= 42), "vidro", 0.18 + 0.08 * ((X + Y) % 3 == 0))
    img.pintar(img.ret(44, 34, 46, 50), "nogueira", 0.6)
    img.pintar(img.elipse(45, 34, 6, 2), "verde", 0.4)
    img.pintar(img.ret(39, 22, 41, 26), "dourado", 0.3)
    return img


def antiga_xix_janela():
    """Janela de madeira com a cortina pesada aberta pelos lados. Atrás do
    vidro não tem rua: tem o concreto do bunker."""
    img = parede_xix(2)
    X, Y = img.X, img.Y
    img.pintar(img.ret(22, 26, 58, 62), "nogueira", 0.55)
    vidro = img.ret(25, 29, 55, 59)
    img.pintar(vidro, "concreto", 0.2 + 0.08 * ((X * 3 + Y) % 7 == 0))
    img.pintar(img.ret(39, 29, 41, 59) | img.ret(25, 43, 55, 45), "nogueira", 0.5)
    for (x0, x1) in ((12, 26), (54, 68)):
        dobra = ((X - x0) % 4) < 2
        img.pintar(img.ret(x0, 22, x1, 66), "vinho", 0.25 + 0.15 * dobra)
    img.pintar(img.ret(10, 21, 70, 24), "dourado", 0.45)
    return img


def antiga_xix_porta():
    """A porta de madeira da sala, aberta: o vão escuro dá no corredor do
    bunker (o concreto e a luz vermelha lá fora)."""
    img = parede_xix(3)
    X, Y = img.X, img.Y
    xa, xb, ya = 22, 58, 34
    img.pintar(img.ret(xa - 4, ya - 4, xb + 4, Y_CHAO), "nogueira", 0.6 + 0.15 * (Y == ya - 4))
    img.pintar(img.ret(xa, ya, xb, Y_CHAO), "concreto", 0.06 + 0.04 * ((Y % 6) == 0))
    img.pintar(img.ret(xa, Y_CHAO - 10, xb, Y_CHAO) & ((X + Y) % 3 == 0), "vermelho", 0.3)
    img.pintar(img.ret(26, 26, 54, 34), "nogueira", 0.4)
    return img


def assoalho():
    """Tábuas de madeira corridas, gastas e enceradas."""
    img = Imagem(128, ALTURA)
    X, Y = img.X, img.Y
    chao = img.ret(0, Y_CHAO, 128, ALTURA)
    fino = ciclico(128, ALTURA, 2, 2, 520)
    veio = ciclico(128, ALTURA, 32, 3, 521)
    tabua = ((Y - Y_CHAO) // 6) % 2
    img.pintar(chao, "nogueira", 0.48 + 0.1 * veio + 0.05 * fino - 0.05 * tabua)
    juntas = chao & (((Y - Y_CHAO) % 6) == 0)
    juntas |= chao & ((((X + 37 * ((Y - Y_CHAO) // 6)) % 64) == 0))
    img.pintar(juntas, "nogueira", 0.2, achatar=False)
    img.cor(img.ret(0, Y_CHAO, 128, Y_CHAO + 1), SOMBRA)
    return img


def assoalho_fundo():
    img = Imagem(128, kit.ALTURA_FUNDO)
    X, Y = img.X, img.Y
    fino = kit.ruido_ciclico_2d(img.w, img.h, 2, 2, 520)
    veio = kit.ruido_ciclico_2d(img.w, img.h, 32, 4, 521)
    tudo = img.ret(0, 0, img.w, img.h)
    tabua = (Y // 8) % 2
    img.pintar(tudo, "nogueira", 0.48 + 0.1 * veio + 0.05 * fino - 0.05 * tabua)
    juntas = ((Y % 8) == 0) | (((X + 37 * (Y // 8)) % 64) == 0)
    img.pintar(tudo & juntas, "nogueira", 0.2, achatar=False)
    return img


def sofa_xix():
    """Sofá de madeira torneada com o estofado de veludo vinho."""
    img = Imagem(64, 34)
    X, Y = img.X, img.Y
    encosto = img.poligono([(6, 6), (20, 2), (44, 2), (58, 6), (58, 18), (6, 18)])
    img.pintar(encosto, "vinho", 0.45 + 0.15 * (Y < 6))
    img.pintar(img.ret(6, 4, 58, 6) & encosto, "dourado", 0.45)
    img.pintar(img.ret(4, 16, 60, 24), "vinho", 0.5 + 0.2 * (Y == 16))
    img.pintar(img.ret(2, 12, 7, 26) | img.ret(57, 12, 62, 26), "nogueira", 0.5)
    img.pintar(img.ret(4, 24, 60, 27), "nogueira", 0.4)
    for x in (6, 30, 56):
        img.pintar(img.ret(x, 27, x + 3, 33), "nogueira", 0.35)
    img.contornar()
    return img, 32, 32


def poltrona_xix():
    img = Imagem(30, 34)
    X, Y = img.X, img.Y
    img.pintar(img.poligono([(5, 4), (15, 1), (25, 4), (25, 18), (5, 18)]), "vinho", 0.45 + 0.15 * (Y < 5))
    img.pintar(img.ret(3, 16, 27, 24), "vinho", 0.5 + 0.2 * (Y == 16))
    img.pintar(img.ret(1, 12, 5, 26) | img.ret(25, 12, 29, 26), "nogueira", 0.5)
    for x in (4, 24):
        img.pintar(img.ret(x, 26, x + 3, 33), "nogueira", 0.35)
    img.contornar()
    return img, 15, 32


def mesa_lampiao():
    """Mesa redonda com a toalha de renda e o lampião a querosene aceso."""
    img = Imagem(36, 46)
    X, Y = img.X, img.Y
    img.pintar(img.elipse(18, 24, 16, 5), "branco", 0.7 + 0.15 * ((X + Y) % 3 == 0))
    img.pintar(img.poligono([(3, 24), (33, 24), (30, 34), (6, 34)]) & ((X + Y) % 4 != 0), "branco", 0.6)
    img.pintar(img.ret(16, 30, 20, 44), "nogueira", 0.45)
    img.pintar(img.ret(10, 42, 26, 45), "nogueira", 0.35)
    img.pintar(img.ret(14, 16, 22, 21), "dourado", 0.55)
    img.pintar(img.elipse(18, 11, 4, 6), "vidro", 0.6)
    img.pintar(img.elipse(18, 12, 2, 3), "lampada", 0.95)
    img.pintar(img.ret(16, 3, 20, 6), "aco", 0.4)
    img.contornar()
    return img, 18, 44


def relogio_pendulo():
    img = Imagem(18, 62)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 4, 16, 60), "nogueira", 0.5 + 0.15 * (X == 2))
    img.pintar(img.poligono([(1, 6), (9, 0), (17, 6)]), "nogueira", 0.55)
    img.pintar(img.elipse(9, 13, 5, 5), "branco", 0.75)
    img.pintar(img.linha(9, 13, 9, 10, 0.5) | img.linha(9, 13, 11, 14, 0.5), "aco", 0.1)
    img.pintar(img.ret(5, 22, 13, 50), "vidro", 0.25)
    img.pintar(img.ret(8, 22, 10, 42), "dourado", 0.5)
    img.pintar(img.elipse(9, 43, 3, 3), "dourado", 0.75)
    img.contornar()
    return img, 9, 60


def cristaleira():
    img = Imagem(34, 58)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 4, 32, 56), "nogueira", 0.5 + 0.12 * (X == 2))
    img.pintar(img.ret(1, 2, 33, 5), "nogueira", 0.6)
    for y0 in (8, 22):
        img.pintar(img.ret(5, y0, 29, y0 + 12), "vidro", 0.3)
        for x in range(7, 28, 6):
            img.pintar(img.elipse(x + 1, y0 + 8, 2, 3), "branco", 0.7)
    img.pintar(img.ret(5, 38, 29, 52), "nogueira", 0.4)
    img.pintar(img.ret(16, 44, 18, 46), "dourado", 0.7)
    img.contornar()
    return img, 17, 56


# ---------------------------------------------------------------------------
# Anos 80
# ---------------------------------------------------------------------------


def parede_80(semente=0):
    img = Imagem(L, Y_CHAO)
    X, Y = img.X, img.Y
    fino = laje_do_bunker(img, semente + 10)
    manchas = ciclico(L, Y_CHAO, 40, 20, 530 + semente)
    papel = img.ret(0, 21, L, 100)
    img.pintar(papel, "bege80", 0.55 + 0.08 * manchas + 0.04 * fino)
    u, v = (X % 20), ((Y - 21) % 20)
    losango = (np.abs(u - 10) + np.abs(v - 10)) == 7
    img.pintar(papel & losango, "marrom80", 0.55, achatar=False)
    img.pintar(papel & ((np.abs(u - 10) + np.abs(v - 10)) == 3), "laranja80", 0.65, achatar=False)
    descolado = (ciclico(L, Y_CHAO, 8, 10, 532 + semente) > 0.88) & img.ret(0, 21, L, 34)
    img.pintar(descolado, "concreto", 0.25)
    img.pintar(img.ret(0, 100, L, Y_CHAO), "marrom80", 0.35 + 0.15 * (Y == 100))
    img.fino, img.manchas = fino, manchas
    return img


def antiga_80_papel():
    return parede_80()


def antiga_80_estante():
    """Estante embutida: a TV de tubo, o videocassete com o relógio piscando
    em 12:00, as fitas e os discos."""
    img = parede_80(1)
    X, Y = img.X, img.Y
    img.pintar(img.ret(4, 26, 76, 100), "marrom80", 0.45 + 0.1 * (X == 4))
    img.pintar(img.ret(7, 29, 73, 97), "marrom80", 0.22)
    img.pintar(img.ret(7, 62, 73, 65), "marrom80", 0.45)
    img.pintar(img.ret(14, 33, 50, 60), "bege80", 0.4 + 0.1 * (Y == 33))
    tela = img.elipse(30, 46, 13, 10) & img.ret(17, 36, 44, 57)
    img.pintar(tela, "vidro", 0.3 + 0.12 * ((Y % 2) == 0))
    img.pintar(img.ret(45, 38, 48, 56) & ((Y % 3) == 0), "aco", 0.6)
    img.pintar(img.ret(14, 66, 50, 72), "aco", 0.2)
    img.pintar(img.ret(40, 68, 46, 70), "laranja80", 0.9)
    for k, x in enumerate(range(54, 71, 4)):
        img.pintar(img.ret(x, 36 + (k % 2), x + 3, 60), ("aco", "marrom80", "laranja80")[k % 3], 0.4)
    for k, x in enumerate(range(10, 70, 3)):
        img.pintar(img.ret(x, 76, x + 2, 94), ("aco", "vermelho", "verde80", "laranja80")[k % 4], 0.35)
    return img


def antiga_80_quadro():
    """Um quadro de moldura fina com o pôr do sol em faixas, de loja de
    decoração."""
    img = parede_80(2)
    X, Y = img.X, img.Y
    img.pintar(img.ret(18, 30, 62, 62), "aco", 0.6)
    tela = img.ret(20, 32, 60, 60)
    faixa = (Y - 32) // 5
    img.pintar(tela & (faixa < 3), "laranja80", 0.75 - 0.12 * faixa)
    img.pintar(tela & (faixa >= 3), "marrom80", 0.45 - 0.05 * (faixa - 3))
    img.pintar(img.elipse(40, 46, 7, 7) & tela & (Y < 47), "laranja80", 0.95)
    return img


def antiga_80_porta():
    img = parede_80(3)
    X, Y = img.X, img.Y
    xa, xb, ya = 22, 58, 34
    img.pintar(img.ret(xa - 4, ya - 4, xb + 4, Y_CHAO), "marrom80", 0.55 + 0.15 * (Y == ya - 4))
    img.pintar(img.ret(xa, ya, xb, Y_CHAO), "concreto", 0.06 + 0.04 * ((Y % 6) == 0))
    img.pintar(img.ret(xa, Y_CHAO - 10, xb, Y_CHAO) & ((X + Y) % 3 == 0), "vermelho", 0.3)
    return img


def carpete():
    img = Imagem(128, ALTURA)
    X, Y = img.X, img.Y
    chao = img.ret(0, Y_CHAO, 128, ALTURA)
    fino = ciclico(128, ALTURA, 2, 2, 540)
    manchas = ciclico(128, ALTURA, 32, 10, 541)
    img.pintar(chao, "laranja80", 0.32 + 0.08 * manchas + 0.08 * fino)
    img.pintar(chao & (((X + Y) % 4) == 0), "marrom80", 0.4, achatar=False)
    img.cor(img.ret(0, Y_CHAO, 128, Y_CHAO + 1), SOMBRA)
    return img


def carpete_fundo():
    img = Imagem(128, kit.ALTURA_FUNDO)
    X, Y = img.X, img.Y
    fino = kit.ruido_ciclico_2d(img.w, img.h, 2, 2, 540)
    manchas = kit.ruido_ciclico_2d(img.w, img.h, 32, 16, 541)
    tudo = img.ret(0, 0, img.w, img.h)
    img.pintar(tudo, "laranja80", 0.32 + 0.08 * manchas + 0.08 * fino)
    img.pintar(tudo & (((X + Y) % 4) == 0), "marrom80", 0.4, achatar=False)
    return img


def sofa_80():
    """Sofá de três lugares com o tecido xadrez marrom e as almofadas."""
    img = Imagem(66, 32)
    X, Y = img.X, img.Y
    corpo = img.ret(2, 4, 64, 26)
    xadrez = (((X // 4) + (Y // 4)) % 2) == 0
    img.pintar(corpo, "marrom80", 0.4 + 0.12 * xadrez + 0.1 * (Y < 6))
    img.pintar(img.ret(2, 14, 64, 17), "marrom80", 0.25)
    img.pintar(img.ret(0, 8, 6, 26) | img.ret(60, 8, 66, 26), "marrom80", 0.5)
    img.pintar(img.ret(12, 8, 22, 15), "laranja80", 0.6)
    img.pintar(img.ret(44, 8, 54, 15), "verde80", 0.5)
    for x in (4, 60):
        img.pintar(img.ret(x, 26, x + 3, 31), "aco", 0.3)
    img.contornar()
    return img, 33, 30


def mesinha_80():
    """Mesinha de centro com o telefone de disco e uma revista."""
    img = Imagem(40, 24)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 8, 38, 12), "vidro", 0.45 + 0.2 * (Y == 8))
    img.pintar(img.ret(4, 12, 7, 22) | img.ret(33, 12, 36, 22), "aco", 0.55)
    img.pintar(img.ret(8, 3, 20, 8), "bege80", 0.6 + 0.15 * (Y == 3))
    img.pintar(img.elipse(14, 6, 3, 2) & ~img.elipse(14, 6, 1, 1), "aco", 0.3)
    img.pintar(img.ret(7, 1, 21, 3), "bege80", 0.7)
    img.pintar(img.ret(24, 5, 34, 8), "laranja80", 0.6)
    img.contornar()
    return img, 20, 22


def vitrola():
    """Rack baixo com o toca-discos, e as duas caixas de som do lado."""
    img = Imagem(58, 36)
    X, Y = img.X, img.Y
    img.pintar(img.ret(14, 14, 44, 34), "marrom80", 0.45 + 0.12 * (Y == 14))
    img.pintar(img.ret(16, 18, 42, 24), "aco", 0.25)
    img.pintar(img.ret(15, 9, 43, 14), "aco", 0.5 + 0.2 * (Y == 9))
    img.pintar(img.elipse(26, 11, 8, 2), "aco", 0.08)
    img.pintar(img.elipse(26, 11, 2, 1), "laranja80", 0.8)
    img.pintar(img.linha(36, 10, 31, 12, 0.5), "aco", 0.8)
    for x0 in (1, 45):
        img.pintar(img.ret(x0, 4, x0 + 12, 34), "marrom80", 0.35)
        img.pintar(img.elipse(x0 + 6, 13, 4, 4) | img.elipse(x0 + 6, 25, 5, 5), "aco", 0.15)
    img.contornar()
    return img, 29, 34


def abajur_80():
    img = Imagem(18, 54)
    X, Y = img.X, img.Y
    img.pintar(img.poligono([(4, 2), (14, 2), (17, 14), (1, 14)]), "bege80", 0.7 + 0.15 * (Y < 4))
    img.pintar(img.ret(8, 14, 10, 50), "dourado", 0.55)
    img.pintar(img.elipse(9, 51, 6, 2), "dourado", 0.45)
    img.contornar()
    return img, 9, 52


PAREDES = {
    "antiga_xix_papel": antiga_xix_papel,
    "antiga_xix_quadro": antiga_xix_quadro,
    "antiga_xix_janela": antiga_xix_janela,
    "antiga_xix_porta": antiga_xix_porta,
    "antiga_80_papel": antiga_80_papel,
    "antiga_80_estante": antiga_80_estante,
    "antiga_80_quadro": antiga_80_quadro,
    "antiga_80_porta": antiga_80_porta,
}
CHAOS = {"assoalho": assoalho, "carpete": carpete}
CHAOS_FUNDO = {"assoalho_fundo": assoalho_fundo, "carpete_fundo": carpete_fundo}
OBJETOS = {
    "sofa_xix": (sofa_xix, (60, 6)),
    "poltrona_xix": (poltrona_xix, (26, 5)),
    "mesa_lampiao": (mesa_lampiao, (24, 5)),
    "relogio_pendulo": (relogio_pendulo, (16, 4)),
    "cristaleira": (cristaleira, (32, 5)),
    "sofa_80": (sofa_80, (62, 6)),
    "mesinha_80": (mesinha_80, (36, 5)),
    "vitrola": (vitrola, (56, 6)),
    "abajur_80": (abajur_80, (10, 3)),
}


def main():
    print("Gerando as salas antigas em", os.path.relpath(PASTA, PASTA_PROJETO))
    for nome, f in PAREDES.items():
        f().salvar(f"{nome}.png", os.path.join(PASTA, "paredes"))
    for nome, f in CHAOS.items():
        img = f()
        img.px = img.px[Y_CHAO:].copy()
        img.h = img.px.shape[0]
        img.salvar(f"{nome}.png", os.path.join(PASTA, "chao"))
    for nome, f in CHAOS_FUNDO.items():
        f().salvar(f"{nome}.png", os.path.join(PASTA, "chao"))
    for nome, (f, pegada) in OBJETOS.items():
        img, px, py = f()
        img.salvar(f"{nome}.png", os.path.join(PASTA, "objetos"))
        print(f"    {nome}: pé em ({px}, {py}) -> offset = Vector2({-px}, {-py}), pegada {pegada}")


if __name__ == "__main__":
    main()
