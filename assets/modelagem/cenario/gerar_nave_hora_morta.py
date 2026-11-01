# gerar_nave_hora_morta.py — desenha por código as texturas da nave de Hora Morta,
# o filme de terror da Sala VR (docs/mecanicas/hora_morta.md). São ladrilhos de
# 64 x 64: o script do casco repete cada um pelas paredes com projeção triplanar,
# então a borda da direita precisa continuar na da esquerda, e a de cima na de baixo.
#
# Como rodar (Python 3 + Pillow):
#   python assets/modelagem/cenario/gerar_nave_hora_morta.py
#
# O que sai, em assets/sprites/cenario/hora_morta/:
#   parede_nave.png   painéis de metal com rebites, manchas e riscos
#   chao_grade.png    grade de metal do piso
#   teto_nave.png     placas do teto com um duto passando
#   porta_nave.png    porta de correr com faixas de perigo

import os
import random

from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_SAIDA = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "hora_morta")

TAMANHO = 64


def cor(hexa):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def ret(img, x, y, largura, altura, c):
    for j in range(y, y + altura):
        for i in range(x, x + largura):
            img.putpixel((i % TAMANHO, j % TAMANHO), c)


def clarear(c, quanto):
    return tuple(max(0, min(255, canal + quanto)) for canal in c[:3]) + (255,)


def granular(img, sorteio, forca):
    # Muda cada pixel um pouco para o metal não parecer uma cor chapada.
    for y in range(TAMANHO):
        for x in range(TAMANHO):
            img.putpixel((x, y), clarear(img.getpixel((x, y)), sorteio.randint(-forca, forca)))


def manchas(img, sorteio, quantas, c):
    # Ferrugem e sujeira escorrendo: uma coluna de pixels que falha no caminho.
    for _ in range(quantas):
        x = sorteio.randrange(TAMANHO)
        y = sorteio.randrange(TAMANHO)
        for passo in range(sorteio.randint(6, 18)):
            if sorteio.random() < 0.8:
                img.putpixel((x, (y + passo) % TAMANHO), c)
            if sorteio.random() < 0.15:
                x = (x + sorteio.choice((-1, 1))) % TAMANHO


def parede():
    sorteio = random.Random(11)
    base = cor("#3f4752")
    img = Image.new("RGBA", (TAMANHO, TAMANHO), base)
    granular(img, sorteio, 4)
    manchas(img, sorteio, 7, cor("#3b3430"))
    for corte in (0, 32):
        ret(img, corte, 0, 1, TAMANHO, cor("#1b1f26"))
        ret(img, corte + 1, 0, 1, TAMANHO, clarear(base, 14))
    for corte in (0, 32):
        ret(img, 0, corte, TAMANHO, 1, cor("#1b1f26"))
        ret(img, 0, corte + 1, TAMANHO, 1, clarear(base, 14))
    for x in (5, 27, 37, 59):
        for y in (5, 27, 37, 59):
            img.putpixel((x, y), cor("#7c8794"))
            img.putpixel((x + 1, y + 1), cor("#20252c"))
    return img


def chao():
    sorteio = random.Random(23)
    img = Image.new("RGBA", (TAMANHO, TAMANHO), cor("#14171c"))
    for y in range(0, TAMANHO, 8):
        for x in range(0, TAMANHO, 8):
            ret(img, x, y, 7, 3, cor("#4b525c"))
            ret(img, x, y + 4, 3, 3, cor("#3a4049"))
            ret(img, x + 4, y + 4, 3, 3, cor("#3a4049"))
    granular(img, sorteio, 5)
    manchas(img, sorteio, 5, cor("#262019"))
    return img


def teto():
    sorteio = random.Random(37)
    base = cor("#2b3038")
    img = Image.new("RGBA", (TAMANHO, TAMANHO), base)
    granular(img, sorteio, 3)
    ret(img, 0, 0, TAMANHO, 1, cor("#13161b"))
    ret(img, 24, 0, 16, TAMANHO, cor("#3a4049"))
    ret(img, 24, 0, 1, TAMANHO, cor("#13161b"))
    ret(img, 39, 0, 1, TAMANHO, cor("#13161b"))
    for y in range(4, TAMANHO, 16):
        ret(img, 24, y, 16, 2, cor("#555d68"))
    return img


def porta():
    sorteio = random.Random(41)
    base = cor("#4a4f58")
    img = Image.new("RGBA", (TAMANHO, TAMANHO), base)
    granular(img, sorteio, 4)
    ret(img, 31, 0, 2, TAMANHO, cor("#101216"))
    for y in range(0, 10):
        for x in range(TAMANHO):
            faixa = (x + y) // 5 % 2 == 0
            img.putpixel((x, y + 27), cor("#b08a22") if faixa else cor("#1a1a1c"))
    manchas(img, sorteio, 5, cor("#3b3430"))
    return img


def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    for nome, desenho in (
        ("parede_nave", parede),
        ("chao_grade", chao),
        ("teto_nave", teto),
        ("porta_nave", porta),
    ):
        desenho().save(os.path.join(PASTA_SAIDA, nome + ".png"))


if __name__ == "__main__":
    main()
