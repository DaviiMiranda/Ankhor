# gerar_arma_impulso.py — desenha em pixel art o ícone (16 x 16) e o sprite
# do chão da arma de impulso, o gadget que fica no cofre do cinema.
#
# Como rodar (Python 3 + Pillow):
#   python assets/modelagem/itens/gerar_arma_impulso.py
#
# Gera:
#   assets/sprites/itens/arma_impulso.png        ícone da mochila, 16 x 16
#   assets/sprites/itens/arma_impulso_chao.png   sprite do chão, 14 x 7
#
# O desenho é a arma de pulso: um canhão curto de aço azulado preso ao
# antebraço, com o cano em cima, o tubo de baixo em anel e o núcleo ciano aceso
# no bocal (a cor do impulso, a mesma da onda no jogo). É o mesmo desenho da
# imagem detalhada (arma_impulso_detalhe.png) e do sprite do braço do Gabriel
# (gerar_gabriel_arma.py). Cada pixel é pintado pelo seu caractere da grade.

import os

from PIL import Image

PASTA_PROJETO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")

PALETA = {
    ".": (0, 0, 0, 0),
    "k": (14, 18, 26, 255),
    "d": (38, 48, 64, 255),
    "m": (70, 88, 112, 255),
    "l": (120, 144, 170, 255),
    "c": (90, 235, 255, 255),
    "w": (215, 252, 255, 255),
    "o": (230, 120, 40, 255),
}

ICONE = [
    "................",
    "................",
    "................",
    ".....kkkkkkkkkk.",
    ".....kllllllllck",
    ".kkkkkmmmmmmmmwk",
    "kllllllkkkkkkkck",
    "kmmccmmmmmmmmmkk",
    "kmmmmmmmkllllkdk",
    "kddddddkkmmmmmkk",
    "kdcdcdckkmcmmkdk",
    ".kdddddkkddddkkk",
    "..kkkkkkkkkkkkk.",
    "................",
    "................",
    "................",
]

CHAO = [
    "......kkkkkkkk",
    "...kkkklllllck",
    "..klllmmmmmmwk",
    ".kmmmmkkkkkkck",
    ".kdccdkkllllkk",
    ".kddddkkmcmmkk",
    "..kkkkkkkkkkk.",
]


def desenhar(grade, caminho):
    altura, largura = len(grade), len(grade[0])
    imagem = Image.new("RGBA", (largura, altura))
    for y, linha in enumerate(grade):
        assert len(linha) == largura, "linha %d com largura errada" % y
        for x, letra in enumerate(linha):
            imagem.putpixel((x, y), PALETA[letra])
    imagem.save(caminho)
    print("gerado:", caminho)


if __name__ == "__main__":
    desenhar(ICONE, os.path.join(PASTA_ITENS, "arma_impulso.png"))
    desenhar(CHAO, os.path.join(PASTA_ITENS, "arma_impulso_chao.png"))
