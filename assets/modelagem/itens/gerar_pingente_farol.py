# gerar_pingente_farol.py — desenha os sprites do PINGENTE DE FAROL, o
# colecionável da Biblioteca (docs/mecanicas/colecionaveis.md).
#
# Como rodar (Python 3 + Pillow):
#
#   python assets/modelagem/itens/gerar_pingente_farol.py
#
# O que sai (em assets/sprites/itens/):
#   pingente_farol.png        16 x 16, o ícone (a tela "Novo item")
#   pingente_farol_chao.png   o pingente deitado no chão, pequeno, como os
#                             outros itens (o pé é o meio da borda de baixo)
#
# O DESENHO é o símbolo dos Faroleiros (Enredo Principal, seção 2.4) na grade
# de 9 x 12 células: a torre (trapézio, 3 células no topo e 5 na base), a
# lanterna (3 x 3, com o ponto no centro) e os três raios em leque. Aqui cada
# célula é 1 pixel. O ponto do centro da lanterna, que no símbolo pintado na
# parede é um furo, vira o brilho da chama. A cor é o âmbar dos Faroleiros
# (mesma rampa de gerar_marcas_faroleiros.py).

import os

from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")

CORES = {
    "o": "#2a1704",
    "e": "#4a2a08",
    "d": "#7a4510",
    "t": "#a8641a",
    "r": "#d48a2a",
    "l": "#f2b04a",
    "g": "#fff2b8",
}

RAIOS = [(0, 0), (1, 1), (2, 2), (4, 0), (4, 1), (4, 2), (8, 0), (7, 1), (6, 2)]
LANTERNA = [(cx, cy) for cx in range(3, 6) for cy in range(3, 6)]
TORRE = [(cx, 6 + linha) for linha in range(6)
         for cx in (range(3, 6) if linha < 3 else range(2, 7))]

CHAO = [
    "r.........",
    ".rlllttdd.",
    "rrlgltttdd",
    ".rlllttdd.",
    "r.........",
]


def hexa(codigo):
    return tuple(int(codigo[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def contorno(grade, largura, altura):
    """Pinta de escuro todo pixel vazio que encosta num pixel desenhado."""
    for y in range(altura):
        for x in range(largura):
            if grade[y][x] is not None:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                vx, vy = x + dx, y + dy
                if 0 <= vx < largura and 0 <= vy < altura and grade[vy][vx] not in (None, "o"):
                    grade[y][x] = "o"
                    break


def icone():
    largura, altura = 16, 16
    x0, y0 = 3, 2
    grade = [[None] * largura for _ in range(altura)]
    for cx, cy in RAIOS:
        grade[y0 + cy][x0 + cx] = "r"
    for cx, cy in LANTERNA:
        grade[y0 + cy][x0 + cx] = "l"
    grade[y0 + 4][x0 + 4] = "g"
    for cx, cy in TORRE:
        lado = "t" if cx <= 4 else "d"
        grade[y0 + cy][x0 + cx] = lado
    for cx in range(2, 7):
        grade[y0 + 11][x0 + cx] = "e"
    contorno(grade, largura, altura)
    return grade


def chao():
    altura, largura = len(CHAO), len(CHAO[0])
    grade = [[None if c == "." else c for c in linha] for linha in CHAO]
    return grade, largura, altura


def salvar(grade, largura, altura, nome):
    img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    for y in range(altura):
        for x in range(largura):
            letra = grade[y][x]
            if letra is not None:
                img.putpixel((x, y), hexa(CORES[letra]))
    caminho = os.path.join(PASTA_ITENS, nome)
    img.save(caminho)
    print("salvo", caminho)


def main():
    salvar(icone(), 16, 16, "pingente_farol.png")
    grade, largura, altura = chao()
    salvar(grade, largura, altura, "pingente_farol_chao.png")


if __name__ == "__main__":
    main()
