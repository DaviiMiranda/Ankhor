# gerar_criatura_hora_morta.py — desenha por código a criatura de Hora Morta
# (docs/mecanicas/hora_morta.md). Ela é uma imagem do filme, não um bicho: uma
# silhueta preta, comprida, com um quadro de película queimado no lugar do rosto.
# As linhas riscadas e as fileiras deslocadas de cada quadro imitam película estragada.
#
# Como rodar (Python 3 + Pillow):
#   python assets/modelagem/personagens/gerar_criatura_hora_morta.py
#
# O que sai, em assets/sprites/personagens/criatura_hora_morta/:
#   criatura_andar.png   4 quadros de 64 x 128, um ao lado do outro

import os
import random

from PIL import Image, ImageDraw

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_SAIDA = os.path.join(PASTA_PROJETO, "assets", "sprites", "personagens", "criatura_hora_morta")

LARGURA, ALTURA = 64, 128
QUADROS = 4
PRETO = (7, 6, 9, 255)
QUEIMADO = (226, 214, 170, 255)
BRASA = (214, 92, 34, 255)
RISCO = (92, 88, 84, 255)

# Pontos de cada quadro: o pé e a mão que avançam trocam de lado a cada dois quadros.
POSES = (
    {"pe_esq": (20, 126), "pe_dir": (44, 126), "mao_esq": (10, 94), "mao_dir": (55, 102), "corpo": 0},
    {"pe_esq": (27, 126), "pe_dir": (38, 124), "mao_esq": (13, 98), "mao_dir": (52, 98), "corpo": -1},
    {"pe_esq": (44, 126), "pe_dir": (20, 126), "mao_esq": (9, 102), "mao_dir": (54, 94), "corpo": 0},
    {"pe_esq": (37, 124), "pe_dir": (27, 126), "mao_esq": (12, 98), "mao_dir": (51, 98), "corpo": 1},
)


def silhueta(pose):
    img = Image.new("RGBA", (LARGURA, ALTURA), (0, 0, 0, 0))
    traco = ImageDraw.Draw(img)
    meio = 32 + pose["corpo"]
    traco.polygon([(meio - 10, 28), (meio + 10, 28), (meio + 6, 70), (meio - 6, 70)], fill=PRETO)
    for ombro, cotovelo, mao in (
        ((meio - 10, 30), (meio - 18, 62), pose["mao_esq"]),
        ((meio + 10, 30), (meio + 18, 62), pose["mao_dir"]),
    ):
        traco.line([ombro, cotovelo, mao], fill=PRETO, width=3)
    for quadril, pe, joelho_x in (
        ((meio - 4, 68), pose["pe_esq"], -3),
        ((meio + 4, 68), pose["pe_dir"], 3),
    ):
        joelho = ((quadril[0] + pe[0]) // 2 + joelho_x, 96)
        traco.line([quadril, joelho, pe], fill=PRETO, width=4)
    traco.rectangle([meio - 2, 20, meio + 2, 30], fill=PRETO)
    return img, meio


def rosto(img, meio, sorteio):
    # O rosto é um quadro de filme que queimou: o buraco claro tem a borda irregular.
    traco = ImageDraw.Draw(img)
    traco.rectangle([meio - 9, 3, meio + 9, 22], fill=PRETO)
    for y in range(6, 20):
        for x in range(meio - 6, meio + 7):
            distancia = abs(x - meio) / 7 + abs(y - 13) / 8
            if distancia + sorteio.uniform(-0.2, 0.2) < 0.75:
                img.putpixel((x, y), QUEIMADO)
            elif distancia + sorteio.uniform(-0.2, 0.2) < 0.95:
                img.putpixel((x, y), BRASA)
    for y in (5, 10, 15, 20):
        img.putpixel((meio - 8, y), QUEIMADO)
        img.putpixel((meio + 8, y), QUEIMADO)


def riscar(img, sorteio):
    # Riscos verticais só aparecem onde já há corpo, para não sujar o fundo.
    for _ in range(sorteio.randint(3, 5)):
        x = sorteio.randrange(LARGURA)
        for y in range(ALTURA):
            if img.getpixel((x, y)) == PRETO and sorteio.random() < 0.7:
                img.putpixel((x, y), RISCO)


def rasgar(img, sorteio):
    # Desloca umas poucas fileiras para o lado, como película que pulou no projetor.
    copia = img.copy()
    for _ in range(sorteio.randint(4, 7)):
        y = sorteio.randrange(ALTURA)
        desvio = sorteio.choice((-3, -2, 2, 3))
        for altura in range(sorteio.randint(1, 3)):
            if y + altura >= ALTURA:
                break
            for x in range(LARGURA):
                img.putpixel((x, y + altura), copia.getpixel(((x + desvio) % LARGURA, y + altura)))


def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    folha = Image.new("RGBA", (LARGURA * QUADROS, ALTURA), (0, 0, 0, 0))
    for indice, pose in enumerate(POSES):
        sorteio = random.Random(700 + indice)
        img, meio = silhueta(pose)
        rosto(img, meio, sorteio)
        riscar(img, sorteio)
        rasgar(img, sorteio)
        folha.paste(img, (LARGURA * indice, 0))
    folha.save(os.path.join(PASTA_SAIDA, "criatura_andar.png"))


if __name__ == "__main__":
    main()
