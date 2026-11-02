# gerar_cabine_vr.py — desenha por código, pixel a pixel, as cabines da Sala VR
# do Cine Andrômeda (docs/fases/centro_de_convivencia.md, seção 7.7). É o mesmo
# tamanho e o mesmo jeito do pedestal da sala segura (gerar_sala_segura.py), para
# a animação de pegar e pôr o visor funcionar igual, mas na cor do cinema e com o
# visor do próprio cinema, e não os óculos do Zane.
#
# Como rodar (Python 3 + Pillow):
#   python assets/modelagem/cenario/gerar_cabine_vr.py
#
# O que sai, em assets/sprites/cenario/objetos/:
#   cabine_vr.png        28 x 24, o pedestal de veludo e aço com a telinha apagada
#   cabine_vr_luz.png    28 x 24, só os pixels que acendem (a doca e a tela do filme
#                        que funciona), para ir por cima, sem sofrer a luz da sala
#   visor_cinema.png     20 x 7, o visor que fica em cima do pedestal

import os

from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")


def cor(hexa):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


CONTORNO = cor("#120d18")
VINHO_ESCURO = cor("#2a1830")
VINHO = cor("#43264c")
VINHO_CLARO = cor("#6a4276")
ACO = cor("#7a7f8e")
TELA = cor("#100a14")
VERMELHO = cor("#a32020")
VERMELHO_VIVO = cor("#ff6a4a")
LENTE = cor("#1c2436")
LENTE_BRILHO = cor("#4a5e86")

LARGURA, ALTURA = 28, 24


def ret(img, x, y, largura, altura, c):
    for j in range(y, y + altura):
        for i in range(x, x + largura):
            img.putpixel((i, j), c)


def pedestal():
    img = Image.new("RGBA", (LARGURA, ALTURA), (0, 0, 0, 0))
    # Plinto (a base, mais larga e escura).
    ret(img, 1, 21, 26, 3, CONTORNO)
    ret(img, 2, 21, 24, 2, VINHO_ESCURO)
    ret(img, 2, 21, 24, 1, ACO)
    # Corpo.
    ret(img, 3, 7, 22, 15, CONTORNO)
    ret(img, 4, 8, 20, 13, VINHO)
    ret(img, 4, 8, 1, 13, VINHO_CLARO)
    ret(img, 23, 8, 1, 13, VINHO_ESCURO)
    ret(img, 4, 20, 20, 1, VINHO_ESCURO)
    # Tampo, mais largo que o corpo.
    ret(img, 1, 4, 26, 4, CONTORNO)
    ret(img, 2, 5, 24, 2, ACO)
    ret(img, 2, 6, 24, 1, VINHO_CLARO)
    ret(img, 2, 7, 24, 1, VINHO_ESCURO)
    # Doca do visor e telinha apagada.
    ret(img, 6, 5, 16, 1, VINHO_ESCURO)
    ret(img, 7, 10, 14, 10, CONTORNO)
    ret(img, 8, 11, 12, 8, TELA)
    return img


def luz():
    img = Image.new("RGBA", (LARGURA, ALTURA), (0, 0, 0, 0))
    # A doca, acesa.
    ret(img, 6, 5, 16, 1, VERMELHO_VIVO)
    # A tela: dois olhos abertos no escuro, o filme de terror em cartaz.
    ret(img, 8, 11, 12, 8, cor("#2b0a0a"))
    ret(img, 10, 14, 3, 2, VERMELHO_VIVO)
    ret(img, 15, 14, 3, 2, VERMELHO_VIVO)
    ret(img, 11, 14, 1, 2, VERMELHO)
    ret(img, 16, 14, 1, 2, VERMELHO)
    return img


def visor():
    img = Image.new("RGBA", (20, 7), (0, 0, 0, 0))
    # A caixa do visor, com a tira que prende na cabeça saindo dos lados.
    ret(img, 0, 2, 20, 2, CONTORNO)
    ret(img, 3, 0, 14, 7, CONTORNO)
    ret(img, 4, 1, 12, 5, VINHO_CLARO)
    ret(img, 4, 5, 12, 1, VINHO_ESCURO)
    # As duas lentes.
    ret(img, 5, 2, 4, 3, LENTE)
    ret(img, 11, 2, 4, 3, LENTE)
    ret(img, 5, 2, 1, 1, LENTE_BRILHO)
    ret(img, 11, 2, 1, 1, LENTE_BRILHO)
    return img


if __name__ == "__main__":
    os.makedirs(PASTA_OBJETOS, exist_ok=True)
    pedestal().save(os.path.join(PASTA_OBJETOS, "cabine_vr.png"))
    luz().save(os.path.join(PASTA_OBJETOS, "cabine_vr_luz.png"))
    visor().save(os.path.join(PASTA_OBJETOS, "visor_cinema.png"))
    print("salvo em", os.path.relpath(PASTA_OBJETOS, PASTA_PROJETO))
