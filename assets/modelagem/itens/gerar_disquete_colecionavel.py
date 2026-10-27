# gerar_disquete_colecionavel.py — desenha os sprites do DISQUETE COLORIDO, o
# colecionável do Bloco de salas (docs/mecanicas/colecionaveis.md).
#
# Como rodar (Python 3 + Pillow):
#
#   python assets/modelagem/itens/gerar_disquete_colecionavel.py
#
# O que sai (em assets/sprites/itens/):
#   disquete_colecionavel.png        16 x 16, o ícone (a tela "Novo item")
#   disquete_colecionavel_chao.png   o disquete no chão, pequeno, como os outros
#                                    itens (o pé é o meio da borda de baixo)
#
# O DESENHO é um disquete de 3,5" PRETO (para não se confundir com o azul das
# senhas da Biblioteca) com os dois adesivos da Clarice, o rosa e o amarelo
# (assets/sprites/personagens/clarice/visual.md). Corpo de canto cortado em
# cima à direita, o obturador de metal com a janelinha escura e a etiqueta de
# papel embaixo, com os adesivos e uma linha de caneta.

import os

from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")

CORES = {
    "o": "#14141a",
    "b": "#30303c",
    "B": "#4c4c5e",
    "m": "#b4b4b4",
    "M": "#e4e4e4",
    "k": "#848484",
    "w": "#f4f2e0",
    "l": "#c4c6c2",
    "p": "#ff6fb0",
    "y": "#ffd23f",
}

CHAO = [
    "BBBBBBBb",
    "bbmmmkbb",
    "bbmmmkbb",
    "bpppyyyb",
    "bwwwwwwb",
]


def hexa(codigo):
    return tuple(int(codigo[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def retangulo(grade, x0, y0, x1, y1, letra):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            grade[y][x] = letra


def icone():
    grade = [[None] * 16 for _ in range(16)]
    retangulo(grade, 1, 1, 14, 14, "o")
    retangulo(grade, 2, 2, 13, 13, "b")
    retangulo(grade, 2, 2, 13, 2, "B")
    retangulo(grade, 2, 2, 2, 13, "B")
    grade[1][14] = None
    grade[1][13] = None
    grade[2][14] = None
    grade[2][13] = "o"
    grade[1][12] = "o"
    retangulo(grade, 5, 2, 10, 6, "m")
    retangulo(grade, 5, 2, 6, 6, "M")
    retangulo(grade, 5, 6, 10, 6, "k")
    retangulo(grade, 9, 3, 10, 5, "o")
    retangulo(grade, 3, 9, 12, 13, "w")
    retangulo(grade, 3, 9, 5, 10, "p")
    retangulo(grade, 10, 9, 12, 10, "y")
    retangulo(grade, 4, 12, 11, 12, "l")
    return grade


def salvar(grade, nome):
    altura, largura = len(grade), len(grade[0])
    img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    for y in range(altura):
        for x in range(largura):
            letra = grade[y][x]
            if letra is not None and letra != ".":
                img.putpixel((x, y), hexa(CORES[letra]))
    caminho = os.path.join(PASTA_ITENS, nome)
    img.save(caminho)
    print("salvo", caminho)


def main():
    salvar(icone(), "disquete_colecionavel.png")
    salvar(CHAO, "disquete_colecionavel_chao.png")


if __name__ == "__main__":
    main()
