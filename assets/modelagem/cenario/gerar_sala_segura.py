# gerar_sala_segura.py — desenha por código, pixel a pixel, a máquina de salvar
# da sala segura (docs/mecanicas/sala_segura.md). É um placeholder pequeno e
# legível, na paleta fria do jogo, até a arte final ficar pronta.
#
# Como rodar (Python 3 + Pillow):
#   python assets/modelagem/cenario/gerar_sala_segura.py
#
# O que sai, em assets/sprites/cenario/objetos/:
#   maquina_de_salvar.png        28 x 24, o pedestal de grafite com a telinha apagada
#   maquina_de_salvar_luz.png    28 x 24, só os pixels que acendem (tela e doca),
#                                para ir por cima do pedestal, sem sofrer a luz da sala
#
# Os óculos que ficam em cima são os do Zane (assets/sprites/menu/menu_oculos_zane.png,
# gerados por assets/modelagem/menu/gerar_objetos_menu.py): a cena os coloca sobre
# a doca com escala 0,25, o mesmo tamanho em que aparecem na estante do menu.
#
# Como cada desenho é feito: começa com uma imagem transparente e pinta
# retângulos (ret) e pixels (px) com cores de uma paleta curta. O volume vem
# de duas regras da pixel art: a borda de cima e da esquerda é mais clara
# (a luz vem do alto, da esquerda) e a de baixo e da direita é mais escura.

import os

from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")


def cor(hexa):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


CONTORNO = cor("#16161c")
GRAFITE_ESCURO = cor("#272b34")
GRAFITE = cor("#3a404c")
GRAFITE_CLARO = cor("#586070")
TELA = cor("#0f1c26")
CIANO = cor("#46aaba")
CIANO_VIVO = cor("#92e4ee")
AMARELO_ACIDO = cor("#aab62a")

LARGURA, ALTURA = 28, 24


def ret(img, x, y, largura, altura, c):
    for j in range(y, y + altura):
        for i in range(x, x + largura):
            img.putpixel((i, j), c)


def px(img, x, y, c):
    img.putpixel((x, y), c)


# O disquete de salvar, 6 x 6: o desenho que todo mundo reconhece. O vão escuro
# de cima é a aba metálica; o de baixo, o rótulo; o canto cortado é do disquete.
DISQUETE = [
    "#####.",
    "#...##",
    "#...##",
    "######",
    "#....#",
    "######",
]


def desenhar_disquete(img, x0, y0, c):
    for j, linha in enumerate(DISQUETE):
        for i, letra in enumerate(linha):
            if letra == "#":
                px(img, x0 + i, y0 + j, c)


def pedestal():
    img = Image.new("RGBA", (LARGURA, ALTURA), (0, 0, 0, 0))
    # Plinto (a base, mais larga e escura).
    ret(img, 1, 21, 26, 3, CONTORNO)
    ret(img, 2, 21, 24, 2, GRAFITE_ESCURO)
    ret(img, 2, 21, 24, 1, GRAFITE)
    # Corpo.
    ret(img, 3, 7, 22, 15, CONTORNO)
    ret(img, 4, 8, 20, 13, GRAFITE)
    ret(img, 4, 8, 1, 13, GRAFITE_CLARO)
    ret(img, 23, 8, 1, 13, GRAFITE_ESCURO)
    ret(img, 4, 20, 20, 1, GRAFITE_ESCURO)
    # Tampo, mais largo que o corpo, com o brilho da borda de cima.
    ret(img, 1, 4, 26, 4, CONTORNO)
    ret(img, 2, 5, 24, 2, GRAFITE_CLARO)
    ret(img, 2, 6, 24, 1, GRAFITE)
    ret(img, 2, 7, 24, 1, GRAFITE_ESCURO)
    # Doca dos óculos: uma canaleta escura no tampo (a luz de cima é a camada _luz).
    ret(img, 6, 5, 16, 1, GRAFITE_ESCURO)
    # Telinha embutida no corpo (12 x 8 de vidro).
    ret(img, 7, 10, 14, 10, CONTORNO)
    ret(img, 8, 11, 12, 8, TELA)
    # Detalhe amarelo-ácido: a cor do Zane, numa etiqueta no canto do corpo.
    ret(img, 4, 19, 3, 1, AMARELO_ACIDO)
    # Saída de ar, três frestas, do outro lado.
    for k in range(3):
        ret(img, 21, 19 - 2 * k, 2, 1, GRAFITE_ESCURO)
    return img


def luz():
    img = Image.new("RGBA", (LARGURA, ALTURA), (0, 0, 0, 0))
    # A doca, acesa.
    ret(img, 6, 5, 16, 1, CIANO_VIVO)
    # A tela: fundo ciano fraco, disquete e duas linhas de "texto".
    ret(img, 8, 11, 12, 8, cor("#14323f"))
    desenhar_disquete(img, 9, 12, CIANO_VIVO)
    ret(img, 16, 13, 3, 1, CIANO)
    ret(img, 16, 15, 3, 1, CIANO)
    return img


if __name__ == "__main__":
    os.makedirs(PASTA_OBJETOS, exist_ok=True)
    pedestal().save(os.path.join(PASTA_OBJETOS, "maquina_de_salvar.png"))
    luz().save(os.path.join(PASTA_OBJETOS, "maquina_de_salvar_luz.png"))
    print("salvo em", os.path.relpath(PASTA_OBJETOS, PASTA_PROJETO))
