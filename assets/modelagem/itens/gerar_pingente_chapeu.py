# gerar_pingente_chapeu.py — desenha os sprites do PINGENTE DO CHAPÉU, o
# colecionável do Labirinto (docs/mecanicas/colecionaveis.md).
#
# Como rodar (Python 3 + Pillow):
#
#   python assets/modelagem/itens/gerar_pingente_chapeu.py
#
# O que sai (em assets/sprites/itens/):
#   pingente_chapeu.png        16 x 16, o ícone (a tela "Novo item")
#   pingente_chapeu_chao.png   o pingente deitado no chão, pequeno, como os
#                              outros itens (o pé é o meio da borda de baixo)
#
# O DESENHO é uma borla de enfeite de tricórnio: a argola de latão em cima, o
# colarinho, e o tufo de fios em VINHO (o tom do pau-brasil, a cor do Baltazar,
# assets/sprites/personagens/baltazar/visual.md) com a franja repartida
# embaixo.

import os

from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")

CORES = {
    "o": "#25080e",
    "a": "#7a4510",
    "b": "#c07a22",
    "c": "#f2c05a",
    "d": "#5e1420",
    "e": "#8f2434",
    "f": "#c0475a",
}

ICONE = [
    "................",
    "......cccc......",
    "......c..b......",
    "......c..b......",
    "......bbbb......",
    ".......aa.......",
    "......cccc......",
    ".....cbbbba.....",
    "......aaaa......",
    ".....deffed.....",
    "....deeffeed....",
    "....deeffeed....",
    "....deeffeed....",
    "....de.ee.ed....",
    "....d.e..e.d....",
    "................",
]

CHAO = [
    ".cc........",
    "c..cdeeeed.",
    "c..bdeffeed",
    "c..cdeeeed.",
    ".bb........",
]


def hexa(codigo):
    return tuple(int(codigo[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def para_grade(linhas):
    return [[None if c == "." else c for c in linha] for linha in linhas]


def contorno(grade):
    """Pinta de escuro todo pixel vazio que encosta num pixel desenhado."""
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
            letra = grade[y][x]
            if letra is not None:
                img.putpixel((x, y), hexa(CORES[letra]))
    caminho = os.path.join(PASTA_ITENS, nome)
    img.save(caminho)
    print("salvo", caminho)


def main():
    icone = para_grade(ICONE)
    contorno(icone)
    salvar(icone, "pingente_chapeu.png")
    salvar(para_grade(CHAO), "pingente_chapeu_chao.png")


if __name__ == "__main__":
    main()
