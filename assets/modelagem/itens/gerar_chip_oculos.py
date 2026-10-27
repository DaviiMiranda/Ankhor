# gerar_chip_oculos.py — desenha os sprites do CHIP HEXAGONAL, o colecionável
# do Bunker (docs/mecanicas/colecionaveis.md).
#
# Como rodar (Python 3 + Pillow):
#
#   python assets/modelagem/itens/gerar_chip_oculos.py
#
# O que sai (em assets/sprites/itens/):
#   chip_oculos.png        16 x 16, o ícone (a tela "Novo item")
#   chip_oculos_chao.png   o chip no chão, pequeno, como os outros itens (o pé
#                          é o meio da borda de baixo)
#
# O DESENHO é um chip em forma de HEXÁGONO (o mesmo hexágono do peito da
# jaqueta do Zane, assets/sprites/personagens/zane/visual.md), de corpo escuro
# azul-esverdeado, borda e trilha em CIANO-VERDE (a cor da interface
# holográfica dele) e um ponto de luz no meio. O hexágono é de topo reto: um
# pixel está dentro dele quando |dy| <= altura e |dx| + |dy| / raiz(3) <= raio.

import math
import os

from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")

CORES = {
    "o": "#06161a",
    "b": "#12302e",
    "t": "#1f4f4a",
    "c": "#3fe0c0",
    "l": "#b8fff0",
}

RAIZ_DE_TRES = math.sqrt(3)


def hexa(codigo):
    return tuple(int(codigo[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def dentro(dx, dy, raio):
    return abs(dy) <= raio * RAIZ_DE_TRES / 2 and abs(dx) + abs(dy) / RAIZ_DE_TRES <= raio


def hexagono(largura, altura, raio, com_trilha):
    cx, cy = (largura - 1) / 2, (altura - 1) / 2
    grade = [[None] * largura for _ in range(altura)]
    for y in range(altura):
        for x in range(largura):
            dx, dy = x - cx, y - cy
            if not dentro(dx, dy, raio):
                continue
            if not dentro(dx, dy, raio - 1.3):
                grade[y][x] = "c"
            else:
                grade[y][x] = "t" if dy < 0 else "b"
    if com_trilha:
        for x in range(int(cx) - 3, int(cx) + 4):
            if grade[int(cy)][x] is not None:
                grade[int(cy)][x] = "c"
        grade[int(cy)][int(cx)] = "l"
        grade[int(cy)][int(cx) + 1] = "l"
    else:
        grade[int(cy)][int(cx)] = "l"
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
    icone = hexagono(16, 16, 6.6, True)
    contorno(icone)
    salvar(icone, "chip_oculos.png")
    salvar(hexagono(7, 6, 3.4, False), "chip_oculos_chao.png")


if __name__ == "__main__":
    main()
