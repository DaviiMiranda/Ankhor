# gerar_arma_impulso.py — desenha em pixel art o ícone (16 x 16) e o sprite
# do chão da arma de impulso, o gadget que fica no cofre do cinema.
#
# Como rodar (Python 3 + Pillow):
#   python assets/modelagem/itens/gerar_arma_impulso.py
#
# Gera:
#   assets/sprites/itens/arma_impulso.png        ícone da mochila, 16 x 16
#   assets/sprites/itens/arma_impulso_chao.png   sprite do chão, 11 x 6
#
# O desenho é uma pistola curta e quadrada: carcaça de aço azulado, cabo
# escuro e um bocal em anel com o núcleo ciano aceso (a cor do impulso, a
# mesma da onda no jogo). Cada pixel é pintado pelo seu caractere da grade.

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
    "..kkkkkkkkkk....",
    ".kmllllllllmkkk.",
    ".kmmmmmmmmmkcwk.",
    ".kddddmmmmmkwck.",
    ".kkkkdmmmmmkcwk.",
    "....kdmkkkkkkkk.",
    "....kdmk........",
    "....kddk........",
    "....kdok........",
    "....kdok........",
    "....kkkk........",
    "................",
    "................",
]

CHAO = [
    "..kkkkkkk..",
    ".kmllllmkkk",
    ".kmmmmmkcwk",
    ".kddmmmkwck",
    "..kdmkkkkk.",
    "..kkkk.....",
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
