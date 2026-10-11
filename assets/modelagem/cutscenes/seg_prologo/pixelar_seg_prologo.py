# pixelar_seg_prologo.py — transforma as ilustrações de referência do prólogo
# em imagens do jogo (pixel art de 320 x 180, paleta fechada) para a cutscene
# "seg_prologo" (docs/historia/roteiro/cutscenes/seg_prologo.md).
#
# Como rodar (só precisa de Python 3 com Pillow e NumPy):
#
#   python assets/modelagem/cutscenes/seg_prologo/pixelar_seg_prologo.py
#
# Entrada (assets/modelagem/cutscenes/seg_prologo/referencia/):
#   cena_01_alarme.webp ... cena_08_pulso_fenda.webp
#   Ilustrações geradas fora do Godot, guardadas pela metade do tamanho
#   original (1376 x 768) para não pesar no repositório.
#
# Saída (assets/sprites/cutscenes/seg_prologo/), com os nomes do roteiro:
#   cena_01_alarme.png ... cena_08_pulso_fenda.png, 320 x 180 cada
#
# O que o script faz com cada ilustração:
#   1. Recorta para 16:9 exato. A referência tem 1376 x 768 (proporção
#      1,79), um pouco mais larga que a tela (1,78); corta-se o excesso
#      igualmente dos dois lados.
#   2. Reduz para 320 x 180 com filtro Lanczos. A referência é "pixel art
#      falsa" (cada pixel do desenho ocupa vários pixels da imagem, sem grade
#      exata); a média ponderada do Lanczos junta esses blocos sem criar
#      serrilhado.
#   3. Fecha a paleta em CORES cores com k-médias no espaço Lab (o mesmo
#      método do pixelar_gabriel.py). No Lab a distância entre duas cores
#      acompanha a diferença que o olho percebe, então a paleta guarda os tons
#      que importam (o vermelho do moletom, a luz da fenda) em vez de gastar
#      cores em degradês quase iguais. Cada pixel vira a cor da paleta mais
#      próxima, sem pontilhado: é o que deixa a imagem com cara de pixel art.
#      Cada cena tem a própria paleta, porque a luz muda muito de uma para
#      outra (madrugada azul, sol, fluorescente, fenda violeta).
#   4. Na cena 1, redesenha o visor do despertador marcando 06:15 (o gerador
#      de imagem não acerta números), em dígitos de 7 segmentos, e o
#      reflexo dele no tampo do criado-mudo.

import os
import sys

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "assets", "modelagem", "personagens"))

from pixelar_gabriel import indices_na_paleta, k_medias  # noqa: E402

PASTA_REFERENCIA = os.path.join(AQUI, "referencia")
PASTA_SAIDA = os.path.join(RAIZ, "assets", "sprites", "cutscenes", "seg_prologo")

LARGURA, ALTURA = 320, 180
CORES = 48
AMOSTRA_PALETA = 40000

CENAS = [
    "cena_01_alarme",
    "cena_02_quarto",
    "cena_03_trajeto",
    "cena_04_campus_vivo",
    "cena_05_sala_aula",
    "cena_06_biblioteca_externa",
    "cena_07_cabine_noite",
    "cena_08_pulso_fenda",
]


# ---------------------------------------------------------------------------
# 1 e 2. Recorte 16:9 e redução
# ---------------------------------------------------------------------------

def recortar_16_9(imagem):
    largura, altura = imagem.size
    largura_util = round(altura * LARGURA / ALTURA)
    x0 = (largura - largura_util) // 2
    return imagem.crop((x0, 0, x0 + largura_util, altura))


def reduzir(imagem):
    pequena = imagem.resize((LARGURA, ALTURA), Image.LANCZOS)
    return np.asarray(pequena).astype(np.float32).clip(0, 255)


# ---------------------------------------------------------------------------
# 3. Paleta fechada
# ---------------------------------------------------------------------------

def fechar_paleta(rgb):
    cores = rgb.reshape(-1, 3)
    # Uma amostra fixa (semente 3) basta para o k-médias e deixa o
    # resultado igual toda vez que o script roda.
    escolha = np.random.default_rng(3).choice(
        len(cores), min(AMOSTRA_PALETA, len(cores)), replace=False)
    paleta = k_medias(cores[escolha], CORES, iteracoes=20)
    return paleta, indices_na_paleta(rgb, paleta)


# ---------------------------------------------------------------------------
# 4. O despertador da cena 1
# ---------------------------------------------------------------------------

# Cada dígito de 7 segmentos é uma combinação destes segmentos:
#    a
#  f   b
#    g
#  e   c
#    d
SEGMENTOS = {
    "0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc",
    "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg",
}

# Área do visor que recebe os dígitos novos (em pixels da imagem de
# 320 x 180), medida sobre a imagem reduzida: cobre os dígitos errados que o
# gerador desenhou.
VISOR = (181, 100, 228, 124)
DIGITO_L, DIGITO_A, TRACO = 8, 18, 2

# O reflexo do visor no tampo do criado-mudo: o gerador também desenhou ali
# os números errados. A área é apagada com a cor do tampo e recebe os
# dígitos novos de cabeça para baixo, apagados, até a quina da mesa
# (linha 151), que corta o reflexo.
REFLEXO = (184, 136, 228, 151)
REFLEXO_TOPO = 140
REFLEXO_FORCA = 0.3


def desenhar_digito(img, x, y, digito, cor):
    meio = y + (DIGITO_A - TRACO) // 2
    base = y + DIGITO_A - TRACO
    direita = x + DIGITO_L - TRACO
    metade = DIGITO_A // 2
    retangulos = {
        "a": (x, y, DIGITO_L, TRACO),
        "g": (x, meio, DIGITO_L, TRACO),
        "d": (x, base, DIGITO_L, TRACO),
        "f": (x, y, TRACO, metade),
        "b": (direita, y, TRACO, metade),
        "e": (x, meio, TRACO, DIGITO_A - (meio - y)),
        "c": (direita, meio, TRACO, DIGITO_A - (meio - y)),
    }
    for s in SEGMENTOS[digito]:
        rx, ry, rl, ra = retangulos[s]
        img[ry:ry + ra, rx:rx + rl] = cor


def escrever(img, x, y, texto, cor):
    for caractere in texto:
        if caractere == ":":
            img[y + 4:y + 4 + TRACO, x:x + TRACO] = cor
            img[y + DIGITO_A - 6:y + DIGITO_A - 6 + TRACO, x:x + TRACO] = cor
            x += TRACO + 2
        else:
            desenhar_digito(img, x, y, caractere, cor)
            x += DIGITO_L + 2


def cor_mais_comum(area):
    cores, contagem = np.unique(area.reshape(-1, 3), axis=0, return_counts=True)
    return cores[np.argmax(contagem)]


def desenhar_relogio(img, paleta, texto="06:15"):
    x0, y0, x1, y1 = VISOR
    area = img[y0:y1, x0:x1].reshape(-1, 3).astype(int)
    # O fundo do visor é o tom mais escuro da área; a cor dos dígitos é o
    # vermelho mais forte (maior R em relação a G e B), o mesmo do desenho.
    fundo = area[np.argmin(area.sum(1))]
    vermelho = area[np.argmax(area[:, 0] * 2 - area[:, 1] - area[:, 2])]
    img[y0:y1, x0:x1] = fundo
    y_digito = y0 + (y1 - y0 - DIGITO_A) // 2
    escrever(img, x0 + 2, y_digito, texto, vermelho)
    desenhar_reflexo(img, paleta, x0, y_digito, x1, vermelho)


def desenhar_reflexo(img, paleta, x0, y_digito, x1, vermelho):
    rx0, ry0, rx1, ry1 = REFLEXO
    mesa = cor_mais_comum(img[ry0:ry1, rx0:rx1])
    img[ry0:ry1, rx0:rx1] = mesa
    # O reflexo é uma mistura do vermelho com a cor do tampo, levada para a
    # cor mais próxima da paleta para não criar uma cor nova na imagem.
    mistura = mesa * (1 - REFLEXO_FORCA) + vermelho * REFLEXO_FORCA
    tom = paleta[indices_na_paleta(mistura.reshape(1, 1, 3).astype(np.float32), paleta)[0, 0]]
    digitos = img[y_digito:y_digito + DIGITO_A, x0:x1]
    acesos = np.all(digitos == vermelho, axis=-1)[::-1]
    for linha in range(DIGITO_A):
        y = REFLEXO_TOPO + linha
        if y >= ry1:
            break
        img[y, x0:x1][acesos[linha]] = tom


# ---------------------------------------------------------------------------

def pixelar(nome):
    imagem = Image.open(os.path.join(PASTA_REFERENCIA, nome + ".webp")).convert("RGB")
    rgb = reduzir(recortar_16_9(imagem))
    paleta, indices = fechar_paleta(rgb)
    resultado = paleta[indices]
    if nome == "cena_01_alarme":
        desenhar_relogio(resultado, paleta)
    caminho = os.path.join(PASTA_SAIDA, nome + ".png")
    Image.fromarray(resultado).save(caminho)
    print("salvo", os.path.relpath(caminho, RAIZ))


if __name__ == "__main__":
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    for nome in CENAS:
        pixelar(nome)
