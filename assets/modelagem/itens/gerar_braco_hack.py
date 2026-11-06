# gerar_braco_hack.py — desenha os ícones do implante de hack do Zane (o braço de metal que
# se estende na direção de um robô): o ícone da mochila (16 x 16) e o sprite do chão (9 x 4).
#
# Como rodar (Python 3 + Pillow):
#
#   python assets/modelagem/itens/gerar_braco_hack.py
#
# Cada caractere do desenho é um pixel; o mapa de cores está em PALETA.

import os

from PIL import Image

PASTA = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sprites", "itens"))

PALETA = {
    ".": (0, 0, 0, 0),
    "k": (23, 25, 30, 255),
    "m": (142, 151, 163, 255),
    "d": (74, 80, 91, 255),
    "c": (61, 242, 210, 255),
    "w": (217, 255, 246, 255),
}

ICONE = [
    "................",
    "................",
    "...........c..c.",
    "..........c.cc..",
    "..kkkkkkkkkk.c..",
    ".kmmmmmmmmmmkc.c",
    ".kdcdcdcdmmmkwc.",
    ".kmmmmmmmmmmkc.c",
    "..kkkkkkkkkkk.c.",
    "...kddk..kmk.c..",
    "...kddk..kkk....",
    "................",
    "................",
    "................",
    "................",
    "................",
]

CHAO = [
    ".kkkkkkk.",
    "kmdcdcmmk",
    ".kkkkkkk.",
    "..c...c..",
]


def desenhar(linhas, nome):
    imagem = Image.new("RGBA", (len(linhas[0]), len(linhas)))
    for y, linha in enumerate(linhas):
        for x, letra in enumerate(linha):
            imagem.putpixel((x, y), PALETA[letra])
    imagem.save(os.path.join(PASTA, nome))
    print("escrito", nome)


desenhar(ICONE, "braco_hack.png")
desenhar(CHAO, "braco_hack_chao.png")
