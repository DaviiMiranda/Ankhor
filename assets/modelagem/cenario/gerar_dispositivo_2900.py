# gerar_dispositivo_2900.py — desenha o DISPOSITIVO que cai no chão quando o
# Henrique some, no fim do Bunker (Enredo Principal, seção 8, Ato 3).
#
# Como rodar (Python 3 + numpy + Pillow):
#
#   python assets/modelagem/cenario/gerar_dispositivo_2900.py
#
# O que sai (em assets/sprites/cenario/objetos/):
#   dispositivo_2900.png       o aparelho no chão, 24 x 14 px, em 1x (cenário)
#   dispositivo_2900_luz.png   só os números acesos, para piscar por cima
#
# O QUE É (e o que não é)
#   O Enredo só decidiu que é um dispositivo com o número 2900 no visor. O que
#   ele é, de onde veio e o que o 2900 quer dizer está pendente (seção 10.3).
#   Por isso o desenho é neutro: uma caixinha de metal fosco com um visor, sem
#   marca, sem o vermelho do Carlos nem o âmbar dos Faroleiros. Os números são
#   ciano, a cor da tecnologia de 3026 (seção 2.4).
#
# OS NÚMEROS
#   Cada algarismo é uma grade de 3 x 5 px (fonte de sete segmentos
#   simplificada). Quatro algarismos com 1 px de folga entre eles ocupam
#   4 * 3 + 3 = 15 px, e cabem no visor de 17 px de largura. Os segmentos
#   apagados ficam num ciano escuro, como num visor de verdade.

import os

import numpy as np
from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")

LARGURA, ALTURA = 24, 14
NUMERO = "2900"

CONTORNO = (16, 19, 25, 255)
SOMBRA = (36, 42, 52, 255)
CORPO = (58, 66, 80, 255)
BRILHO = (92, 102, 118, 255)
VISOR = (5, 9, 12, 255)
APAGADO = (18, 52, 60, 255)
ACESO = (110, 240, 255, 255)
LED = (255, 210, 120, 255)

ALGARISMOS = {
    "0": ["111", "101", "101", "101", "111"],
    "2": ["111", "001", "111", "100", "111"],
    "9": ["111", "101", "111", "001", "111"],
    "8": ["111", "101", "111", "101", "111"],
}


def caixa(img):
    # Corpo com os cantos cortados (1 px) e contorno escuro.
    img[1:ALTURA - 1, 1:LARGURA - 1] = CORPO
    img[0, 1:LARGURA - 1] = CONTORNO
    img[ALTURA - 1, 1:LARGURA - 1] = CONTORNO
    img[1:ALTURA - 1, 0] = CONTORNO
    img[1:ALTURA - 1, LARGURA - 1] = CONTORNO
    # Luz de cima (borda clara) e sombra embaixo: o volume da caixa.
    img[1, 2:LARGURA - 2] = BRILHO
    img[ALTURA - 2, 1:LARGURA - 1] = SOMBRA
    img[ALTURA - 3, 1:LARGURA - 1] = SOMBRA
    # Dois parafusos e o LED do lado direito.
    img[ALTURA - 4, 2] = SOMBRA
    img[ALTURA - 4, LARGURA - 3] = SOMBRA
    img[2, LARGURA - 3] = LED


def visor(img, aceso):
    x0, y0 = 3, 3
    img[y0 - 1:y0 + 6, x0 - 1:x0 + 16] = VISOR
    for i, algarismo in enumerate(NUMERO):
        x = x0 + i * 4
        for linha, bits in enumerate(ALGARISMOS["8"]):
            for coluna, bit in enumerate(bits):
                if bit == "1":
                    img[y0 + linha, x + coluna] = APAGADO
        for linha, bits in enumerate(ALGARISMOS[algarismo]):
            for coluna, bit in enumerate(bits):
                if bit == "1":
                    img[y0 + linha, x + coluna] = aceso


def main():
    os.makedirs(PASTA_OBJETOS, exist_ok=True)
    img = np.zeros((ALTURA, LARGURA, 4), dtype=np.uint8)
    caixa(img)
    visor(img, ACESO)
    Image.fromarray(img, "RGBA").save(os.path.join(PASTA_OBJETOS, "dispositivo_2900.png"))

    # A camada de luz: só os segmentos acesos, sobre fundo transparente.
    luz = np.zeros((ALTURA, LARGURA, 4), dtype=np.uint8)
    referencia = np.zeros((ALTURA, LARGURA, 4), dtype=np.uint8)
    visor(referencia, ACESO)
    acesos = np.all(referencia == ACESO, axis=2)
    luz[acesos] = ACESO
    Image.fromarray(luz, "RGBA").save(os.path.join(PASTA_OBJETOS, "dispositivo_2900_luz.png"))
    print("  objeto: assets/sprites/cenario/objetos/dispositivo_2900.png (+ _luz)")


if __name__ == "__main__":
    main()
