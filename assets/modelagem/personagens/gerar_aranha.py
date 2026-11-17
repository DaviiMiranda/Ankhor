# gerar_aranha.py — recorta o desenho da ARANHA 07 e gera os dois sprites do
# robô do apagão (docs/mecanicas/aranha_do_apagao.md).
#
# O desenho (aranha_referencia/aranha_07.webp, 1254 x 1254) é de frente, num
# fundo quase preto. As partes escuras do robô (juntas, pernas de trás, o
# miolo do corpo) têm a mesma cor do fundo, então uma máscara por cor
# estilhaça o robô. A saída é uma máscara em três passos:
#
#   1. PEÇAS CLARAS: pixels com luminância acima de LIMIAR_CLARO ou com o
#      vermelho do olho. A luminância é a média ponderada dos canais,
#      L = 0,30 R + 0,59 G + 0,11 B, a mesma de uma TV em preto e branco.
#      Componentes pequenos (menos de MINIMO_DA_PECA pixels) são descartados:
#      são poeira de ferrugem do fundo, não pedaço do robô.
#   2. CASCO: as peças claras são engordadas em RAIO_DO_CASCO pixels (uma
#      dilatação) e fechadas (dilatação seguida de erosão), o que cobre as
#      partes escuras entre elas. O robô só aparece no escuro, então esse
#      miolo escuro some na penumbra e não faz falta de contorno nítido.
#   3. BORDA: o casco ganha uma borda esfumada (desfoque gaussiano de
#      DESFOQUE_DA_BORDA pixels), para não aparecer uma caixa recortada.
#
# Os OLHOS saem separados (o vermelho vivo do desenho: R alto, G e B baixos),
# num segundo PNG do mesmo tamanho. No jogo ele é desenhado sem luz, sempre
# aceso, como os olhos dos outros robôs (cenas/personagens/robo_*.tscn).
#
# Como rodar (Python 3 + numpy + scipy + pillow):
#
#   python assets/modelagem/personagens/gerar_aranha.py
#
# O que sai (em assets/sprites/personagens/robos/):
#   aranha.png         o corpo, LARGURA_FINAL de largura (resolução dobrada,
#                      como os humanos: no jogo vai com escala 0,5)
#   aranha_olhos.png   só os olhos, do mesmo tamanho e no mesmo lugar
# E imprime a posição do olho central, para pôr a luz dele na cena.

import os

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
ORIGEM = os.path.join(PASTA_SCRIPT, "aranha_referencia", "aranha_07.webp")
SAIDA = os.path.join(PASTA_PROJETO, "assets", "sprites", "personagens", "robos")

LIMIAR_CLARO = 38
MINIMO_DA_PECA = 400
RAIO_DO_CASCO = 34
DESFOQUE_DA_BORDA = 7.0
LARGURA_FINAL = 176
MARGEM = 8


def vermelho_vivo(a):
    return (a[..., 0] > 190) & (a[..., 1] < 110) & (a[..., 2] < 110)


def pecas_claras(a):
    luminancia = a[..., 0] * 0.30 + a[..., 1] * 0.59 + a[..., 2] * 0.11
    mascara = ndi.binary_opening(luminancia > LIMIAR_CLARO, iterations=1) | vermelho_vivo(a)
    rotulos, quantos = ndi.label(mascara)
    tamanhos = ndi.sum(mascara, rotulos, range(1, quantos + 1))
    grandes = [i + 1 for i, t in enumerate(tamanhos) if t >= MINIMO_DA_PECA]
    return np.isin(rotulos, grandes)


def casco(pecas):
    esfera = ndi.generate_binary_structure(2, 1)
    cheio = ndi.binary_dilation(pecas, structure=esfera, iterations=RAIO_DO_CASCO)
    fechado = ndi.binary_erosion(cheio, structure=esfera, iterations=RAIO_DO_CASCO // 2)
    return ndi.binary_fill_holes(fechado | pecas)


def main():
    a = np.array(Image.open(ORIGEM).convert("RGB")).astype(float)
    mascara = casco(pecas_claras(a))
    alfa = np.clip(ndi.gaussian_filter(mascara.astype(float), DESFOQUE_DA_BORDA) * 1.25, 0.0, 1.0)
    alfa[mascara] = 1.0

    ys, xs = np.nonzero(alfa > 0.02)
    x0, x1 = max(xs.min() - MARGEM, 0), min(xs.max() + MARGEM, a.shape[1] - 1)
    y0, y1 = max(ys.min() - MARGEM, 0), min(ys.max() + MARGEM, a.shape[0] - 1)
    caixa = (slice(y0, y1 + 1), slice(x0, x1 + 1))
    largura = LARGURA_FINAL
    altura = round((y1 - y0 + 1) * largura / (x1 - x0 + 1))

    corpo = np.dstack([a[caixa], alfa[caixa] * 255.0]).astype(np.uint8)
    corpo_img = Image.fromarray(corpo, "RGBA").resize((largura, altura), Image.LANCZOS)

    olhos_mascara = ndi.binary_dilation(vermelho_vivo(a), iterations=3)
    olhos_alfa = ndi.gaussian_filter(olhos_mascara.astype(float), 1.5)
    olhos_alfa = np.clip(olhos_alfa * 1.3, 0.0, 1.0)
    olhos_cor = np.clip(a * 1.35, 0, 255)
    olhos = np.dstack([olhos_cor[caixa], olhos_alfa[caixa] * 255.0]).astype(np.uint8)
    olhos_img = Image.fromarray(olhos, "RGBA").resize((largura, altura), Image.LANCZOS)

    os.makedirs(SAIDA, exist_ok=True)
    corpo_img.save(os.path.join(SAIDA, "aranha.png"))
    olhos_img.save(os.path.join(SAIDA, "aranha_olhos.png"))

    vivos = vermelho_vivo(a)
    vivos[:, : x0] = False
    ys_olho, xs_olho = np.nonzero(vivos[caixa])
    pesos = a[caixa][..., 0][vivos[caixa]]
    centro = np.array([(xs_olho * pesos).sum(), (ys_olho * pesos).sum()]) / pesos.sum()
    fator = largura / (x1 - x0 + 1)
    print(f"aranha.png e aranha_olhos.png: {largura} x {altura}")
    print(f"centro do olhar (px do sprite): ({centro[0] * fator:.1f}, {centro[1] * fator:.1f})")
    print(f"pé: o centro de baixo do sprite, ({largura / 2:.0f}, {altura})")


if __name__ == "__main__":
    main()
