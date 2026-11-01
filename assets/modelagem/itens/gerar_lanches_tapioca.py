# gerar_lanches_tapioca.py — desenha os ícones dos 5 LANCHES do puzzle da
# estufa da Tapioca Orbital (docs/fases/centro_de_convivencia.md, seção 8.6).
#
# Como rodar (Python 3 + Pillow):
#
#   python assets/modelagem/itens/gerar_lanches_tapioca.py
#
# O que sai (em assets/sprites/itens/), todos com 24 x 24 px:
#   lanche_pastel.png, lanche_omelete.png, lanche_bolo.png,
#   lanche_torrada.png e lanche_cuscuz.png
#
# O DESENHO usa formas simples e depois um contorno: todo pixel vazio que
# encosta num pixel pintado (nas 4 direções) vira a cor escura. Como o
# contorno é sempre o mesmo, os cinco lanches parecem da mesma família.

import os

from PIL import Image, ImageDraw

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")

TAMANHO = 24
CONTORNO = (34, 20, 18, 255)
PRATO = (190, 200, 210, 255)
PRATO_SOMBRA = (130, 142, 158, 255)


def tela():
    imagem = Image.new("RGBA", (TAMANHO, TAMANHO), (0, 0, 0, 0))
    return imagem, ImageDraw.Draw(imagem)


def prato(desenho):
    desenho.rectangle((2, 18, 21, 19), fill=PRATO)
    desenho.rectangle((4, 20, 19, 20), fill=PRATO_SOMBRA)


def contornar(imagem):
    pixels = imagem.load()
    bordas = []
    for y in range(TAMANHO):
        for x in range(TAMANHO):
            if pixels[x, y][3] != 0:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                vx, vy = x + dx, y + dy
                if 0 <= vx < TAMANHO and 0 <= vy < TAMANHO and pixels[vx, vy][3] != 0 and pixels[vx, vy] != CONTORNO:
                    bordas.append((x, y))
                    break
    for ponto in bordas:
        pixels[ponto] = CONTORNO
    return imagem


def pastel():
    imagem, d = tela()
    d.polygon([(3, 16), (20, 16), (20, 8), (3, 8)], fill=(214, 156, 62, 255))
    d.rectangle((3, 8, 20, 9), fill=(240, 196, 96, 255))
    d.rectangle((3, 15, 20, 16), fill=(166, 108, 36, 255))
    for x in range(4, 20, 3):
        d.point((x, 12), fill=(166, 108, 36, 255))
        d.point((x + 1, 11), fill=(240, 196, 96, 255))
    return contornar(imagem)


def omelete():
    imagem, d = tela()
    prato(d)
    # Dobrada ao meio e achatada, para não parecer o cuscuz, que é alto.
    d.rectangle((2, 12, 21, 17), fill=(240, 206, 76, 255))
    d.rectangle((4, 10, 19, 11), fill=(240, 206, 76, 255))
    d.rectangle((3, 16, 20, 17), fill=(198, 156, 50, 255))
    d.line((4, 13, 19, 13), fill=(255, 232, 130, 255))
    for x, y in ((6, 11), (11, 11), (16, 11), (8, 15), (14, 15)):
        d.point((x, y), fill=(84, 150, 62, 255))
        d.point((x + 1, y), fill=(196, 62, 44, 255))
    return contornar(imagem)


def bolo():
    imagem, d = tela()
    prato(d)
    d.rectangle((5, 9, 18, 17), fill=(134, 82, 44, 255))
    d.rectangle((5, 12, 18, 13), fill=(236, 214, 170, 255))
    d.rectangle((5, 7, 18, 8), fill=(244, 236, 220, 255))
    d.point((7, 9), fill=(244, 236, 220, 255))
    d.point((12, 9), fill=(244, 236, 220, 255))
    d.rectangle((16, 9, 16, 10), fill=(244, 236, 220, 255))
    return contornar(imagem)


def torrada():
    imagem, d = tela()
    d.rectangle((6, 9, 17, 19), fill=(168, 104, 48, 255))
    d.rectangle((4, 5, 19, 9), fill=(168, 104, 48, 255))
    d.rectangle((7, 10, 16, 18), fill=(228, 176, 96, 255))
    d.rectangle((5, 6, 18, 9), fill=(228, 176, 96, 255))
    d.rectangle((9, 7, 13, 9), fill=(198, 138, 66, 255))
    d.rectangle((10, 13, 14, 15), fill=(198, 138, 66, 255))
    return contornar(imagem)


def cuscuz():
    imagem, d = tela()
    prato(d)
    d.pieslice((4, 6, 19, 32), 180, 360, fill=(244, 196, 54, 255))
    d.rectangle((4, 17, 19, 17), fill=(204, 150, 36, 255))
    for x, y in ((9, 9), (13, 10), (7, 13), (11, 13), (15, 14), (10, 16), (6, 16), (16, 11)):
        d.point((x, y), fill=(255, 226, 120, 255))
    return contornar(imagem)


LANCHES = {
    "pastel": pastel,
    "omelete": omelete,
    "bolo": bolo,
    "torrada": torrada,
    "cuscuz": cuscuz,
}


def main():
    for nome, desenhar in LANCHES.items():
        caminho = os.path.join(PASTA_ITENS, f"lanche_{nome}.png")
        desenhar().save(caminho)
        print(caminho)


if __name__ == "__main__":
    main()
