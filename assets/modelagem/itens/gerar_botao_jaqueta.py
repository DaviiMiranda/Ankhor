# gerar_botao_jaqueta.py — desenha os sprites do BOTÃO DA JAQUETA, o
# colecionável do Centro de Convivência (docs/mecanicas/colecionaveis.md).
#
# Como rodar (Python 3 + Pillow):
#
#   python assets/modelagem/itens/gerar_botao_jaqueta.py
#
# O que sai (em assets/sprites/itens/):
#   botao_jaqueta.png        16 x 16, o ícone (a tela "Novo item")
#   botao_jaqueta_chao.png   o botão no chão, pequeno, como os outros itens
#                            (o pé é o meio da borda de baixo)
#
# O DESENHO é um botão redondo de couro marrom-caramelo, a cor da jaqueta da
# Diana (assets/sprites/personagens/diana/visual.md), com aro dourado (a
# fivela do cinto dela é dourada) e quatro furos. O sombreado vem de uma luz
# no canto de cima à esquerda: cada pixel do disco é mais claro ou mais escuro
# conforme a posição dele em relação ao centro.

import math
import os

from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")

CORES = {
    "o": "#2a1606",
    "e": "#7a4a18",
    "m": "#b8742c",
    "c": "#d8944a",
    "a": "#a8801f",
    "g": "#e8c050",
    "f": "#3a2208",
}


def hexa(codigo):
    return tuple(int(codigo[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def disco(tamanho, raio, furos, aro=True):
    centro = (tamanho - 1) / 2
    grade = [[None] * tamanho for _ in range(tamanho)]
    for y in range(tamanho):
        for x in range(tamanho):
            dx, dy = x - centro, y - centro
            distancia = math.hypot(dx, dy)
            if distancia > raio:
                continue
            luz = (-dx - dy) / (2 * raio)
            if aro and distancia >= raio - 1.2:
                grade[y][x] = "g" if luz > -0.1 else "a"
            else:
                grade[y][x] = "c" if luz > 0.45 else ("m" if luz > -0.55 else "e")
    for fx, fy in furos:
        grade[fy][fx] = "f"
    return grade


def contorno(grade):
    altura, largura = len(grade), len(grade[0])
    novos = []
    for y in range(altura):
        for x in range(largura):
            if grade[y][x] is not None:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                vx, vy = x + dx, y + dy
                if 0 <= vx < largura and 0 <= vy < altura and grade[vy][vx] not in (None, "o"):
                    novos.append((x, y))
                    break
    for x, y in novos:
        grade[y][x] = "o"


def salvar(grade, nome):
    altura, largura = len(grade), len(grade[0])
    img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    for y in range(altura):
        for x in range(largura):
            if grade[y][x] is not None:
                img.putpixel((x, y), hexa(CORES[grade[y][x]]))
    caminho = os.path.join(PASTA_ITENS, nome)
    img.save(caminho)
    print("salvo", caminho)


def main():
    icone = disco(16, 6.3, [(6, 6), (9, 6), (6, 9), (9, 9)])
    contorno(icone)
    salvar(icone, "botao_jaqueta.png")
    chao = disco(6, 2.6, [(2, 2)], aro=False)
    salvar(chao, "botao_jaqueta_chao.png")


if __name__ == "__main__":
    main()
