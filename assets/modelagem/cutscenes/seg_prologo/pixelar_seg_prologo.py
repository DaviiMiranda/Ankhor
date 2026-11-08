# pixelar_seg_prologo.py — transforma as ilustrações de referência do prólogo
# em imagens do jogo (pixel art de 640 x 360, paleta fechada) para a cutscene
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
#   cena_01_alarme.png ... cena_08_pulso_fenda.png, 640 x 360 cada
#
# Resolução dobrada: a tela do jogo tem 320 x 180, mas as ilustrações saem
# com o dobro (640 x 360) e a cena do Godot as mostra com escala 0,5. Como o
# stretch do projeto é canvas_items, a imagem é desenhada na resolução da
# janela: ocupa a tela inteira do mesmo jeito, com o dobro de detalhe. É a
# mesma regra dos sprites dos personagens humanos (CLAUDE.md, docs/decisoes.md).
# As referências têm cerca de 600 "pixels de desenho" de largura; reduzir
# para 320 jogava fora metade deles (rostos e roupas viravam borrões).
#
# O que o script faz com cada ilustração:
#   1. Recorta para 16:9 exato. A referência tem 1376 x 768 (proporção
#      1,79), um pouco mais larga que a tela (1,78); corta-se o excesso
#      igualmente dos dois lados.
#   2. Reduz para 640 x 360 com filtro Lanczos. A referência é "pixel art
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
#
# Números e letras na ilustração (o visor do despertador da cena 1, o
# crachá) saem como o gerador de imagem desenhou. Confira depois de rodar:
# se um número sair errado, gere a ilustração de novo.

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

ESCALA = 2
LARGURA, ALTURA = 320 * ESCALA, 180 * ESCALA
CORES = 96
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

def pixelar(nome):
    imagem = Image.open(os.path.join(PASTA_REFERENCIA, nome + ".webp")).convert("RGB")
    rgb = reduzir(recortar_16_9(imagem))
    paleta, indices = fechar_paleta(rgb)
    resultado = paleta[indices]
    caminho = os.path.join(PASTA_SAIDA, nome + ".png")
    Image.fromarray(resultado).save(caminho)
    print("salvo", os.path.relpath(caminho, RAIZ))


if __name__ == "__main__":
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    for nome in CENAS:
        pixelar(nome)
