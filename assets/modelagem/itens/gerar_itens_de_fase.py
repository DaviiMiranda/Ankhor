# gerar_itens_de_fase.py — desenha, por código, os itens novos de cada fase
# (placeholders no estilo do jogo): walkman, módulo de pulso, mapa da Diana,
# máscara de gás, mais a portinhola da galeria e as caixas do nicho.
#
# Como rodar (Python 3 + Pillow):
#   python assets/modelagem/itens/gerar_itens_de_fase.py
#
# O que sai em assets/sprites/itens/:
#   <item>.png           16 x 16 px: ícone do inventário
#   <item>_chao.png      o item no chão, na escala do cenário
#   <item>_detalhe.png   imagem grande da tela de item novo
# e em assets/sprites/cenario/objetos/:
#   grade_galeria.png    a portinhola da galeria, com a marca de giz da Diana
#
# Cada item é uma lista de retângulos em coordenadas de 0 a 16. Multiplicar
# essas coordenadas por uma escala inteira dá o ícone (1x), o chão (arredondado
# para 12 px) e o detalhe (8x): é a mesma figura em três resoluções. No detalhe
# entra ainda um brilho no canto de cima de cada retângulo e um escurecimento
# no de baixo, a conta mais simples de luz de cima para baixo.

import os
import random

from PIL import Image, ImageDraw

PASTA = os.path.dirname(os.path.abspath(__file__))
PROJETO = os.path.normpath(os.path.join(PASTA, "..", "..", ".."))
ITENS = os.path.join(PROJETO, "assets", "sprites", "itens")
OBJETOS = os.path.join(PROJETO, "assets", "sprites", "cenario", "objetos")

CONTORNO = (18, 18, 24, 255)

# (x0, y0, x1, y1, cor): retângulos do fundo para a frente, em unidades de 1/16.
FIGURAS = {
    "walkman": [
        (2, 3, 14, 14, CONTORNO),
        (3, 4, 13, 13, (216, 120, 40, 255)),
        (4, 6, 12, 11, (40, 38, 46, 255)),
        (5, 7, 7, 10, (150, 148, 160, 255)),
        (9, 7, 11, 10, (150, 148, 160, 255)),
        (7, 8, 9, 9, (88, 84, 96, 255)),
        (4, 4, 6, 5, (240, 214, 90, 255)),
        (8, 4, 12, 5, (90, 60, 30, 255)),
        (3, 1, 5, 3, (90, 88, 98, 255)),
    ],
    "modulo_pulso": [
        (3, 4, 13, 12, CONTORNO),
        (4, 5, 12, 11, (46, 72, 84, 255)),
        (5, 6, 11, 10, (18, 30, 38, 255)),
        (7, 7, 9, 9, (120, 235, 255, 255)),
        (6, 6, 7, 7, (70, 170, 200, 255)),
        (9, 9, 10, 10, (70, 170, 200, 255)),
        (5, 2, 6, 4, (190, 196, 204, 255)),
        (10, 2, 11, 4, (190, 196, 204, 255)),
        (5, 12, 6, 14, (190, 196, 204, 255)),
        (10, 12, 11, 14, (190, 196, 204, 255)),
    ],
    "mapa_diana": [
        (2, 3, 14, 13, CONTORNO),
        (3, 4, 13, 12, (222, 206, 164, 255)),
        (4, 6, 12, 7, (120, 84, 52, 255)),
        (7, 7, 8, 10, (120, 84, 52, 255)),
        (10, 7, 11, 9, (120, 84, 52, 255)),
        (4, 9, 7, 10, (120, 84, 52, 255)),
        (11, 5, 12, 6, (200, 50, 40, 255)),
        (4, 10, 5, 11, (200, 50, 40, 255)),
    ],
    "mascara_gas": [
        (3, 3, 13, 12, CONTORNO),
        (4, 4, 12, 11, (72, 84, 62, 255)),
        (5, 5, 7, 7, (150, 200, 210, 255)),
        (9, 5, 11, 7, (150, 200, 210, 255)),
        (6, 8, 10, 13, CONTORNO),
        (7, 9, 9, 12, (120, 120, 112, 255)),
        (5, 14, 11, 15, (120, 120, 112, 255)),
        (7, 13, 9, 14, (72, 84, 62, 255)),
    ],
}


def desenhar(figura, escala, com_luz=False):
    tamanho = 16 * escala
    img = Image.new("RGBA", (tamanho, tamanho), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for (x0, y0, x1, y1, cor) in figura:
        d.rectangle([x0 * escala, y0 * escala, x1 * escala - 1, y1 * escala - 1], fill=cor)
        if com_luz and cor != CONTORNO:
            clara = tuple(min(255, int(c * 1.22)) for c in cor[:3]) + (255,)
            escura = tuple(int(c * 0.72) for c in cor[:3]) + (255,)
            d.rectangle([x0 * escala, y0 * escala, x1 * escala - 1, y0 * escala], fill=clara)
            d.rectangle([x0 * escala, y1 * escala - 1, x1 * escala - 1, y1 * escala - 1], fill=escura)
    return img


def chao(figura):
    """Reduz com vizinho mais próximo para 12 px e recorta o que sobra."""
    img = desenhar(figura, 1).resize((12, 12), Image.NEAREST)
    return img.crop(img.getbbox())


def detalhe_do_mapa():
    """O mapa à mão da Diana: um papel com as galerias de 1978 desenhadas por
    cima da planta da praça. A curva do arco é a mesma ideia da elipse da praça
    (docs/fases/centro_de_convivencia.md, seção 6), desenhada a mão livre."""
    sorteio = random.Random(1978)
    img = Image.new("RGBA", (144, 112), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    papel = (222, 206, 164, 255)
    tinta = (92, 62, 40, 255)
    giz = (200, 50, 40, 255)
    d.rectangle([0, 0, 143, 111], fill=CONTORNO)
    d.rectangle([1, 1, 142, 110], fill=papel)
    for _ in range(420):
        x, y = sorteio.randint(2, 141), sorteio.randint(2, 109)
        d.point((x, y), fill=(206, 188, 146, 255))
    d.arc([18, 8, 126, 96], 180, 360, fill=tinta)
    for (x, y, nome) in [(26, 42, 2), (52, 22, 1), (92, 22, 3), (118, 42, 4)]:
        d.rectangle([x - 6, y - 5, x + 6, y + 5], outline=tinta)
    d.line([(26, 48), (26, 84), (118, 84), (118, 48)], fill=giz, width=2)
    d.line([(92, 28), (92, 84)], fill=giz, width=2)
    for x in (26, 92, 118):
        d.line([(x - 3, 84 - 3), (x + 3, 84 + 3)], fill=giz)
        d.line([(x - 3, 84 + 3), (x + 3, 84 - 3)], fill=giz)
    return img


def grade_da_galeria():
    """Portinhola de chapa com grade, cabe numa parede de 112 px de altura. O X
    de giz vermelho é a marca que a Diana deixou: só aparece com o mapa."""
    img = Image.new("RGBA", (28, 36), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 27, 35], fill=CONTORNO)
    d.rectangle([1, 1, 26, 34], fill=(70, 72, 78, 255))
    d.rectangle([3, 3, 24, 32], fill=(14, 14, 18, 255))
    for x in range(5, 25, 4):
        d.line([(x, 3), (x, 32)], fill=(96, 98, 104, 255))
    d.line([(6, 8), (21, 27)], fill=(214, 60, 46, 255), width=2)
    d.line([(21, 8), (6, 27)], fill=(214, 60, 46, 255), width=2)
    return img


def main():
    os.makedirs(ITENS, exist_ok=True)
    for nome, figura in FIGURAS.items():
        desenhar(figura, 1).save(os.path.join(ITENS, f"{nome}.png"))
        chao(figura).save(os.path.join(ITENS, f"{nome}_chao.png"))
        if nome == "mapa_diana":
            detalhe_do_mapa().save(os.path.join(ITENS, f"{nome}_detalhe.png"))
        else:
            desenhar(figura, 8, True).save(os.path.join(ITENS, f"{nome}_detalhe.png"))
    grade_da_galeria().save(os.path.join(OBJETOS, "grade_galeria.png"))
    print("itens de fase gerados")


if __name__ == "__main__":
    main()
