# gerar_quadro_nave.py — desenha a GRAVURA DA NAVE, o quadro que aparece na
# parede do quarto do visor 3D quando o jogador junta os três recortes de
# jornal (docs/mecanicas/colecionaveis.md).
#
# Como rodar (Python 3 + Pillow + numpy):
#
#   python assets/modelagem/cenario/gerar_quadro_nave.py
#
# O que sai:
#   assets/sprites/cenario/visor/quadro_nave.png   192 x 120, em pixel art
#
# O DESENHO: uma nave imensa cruzando o escuro, de lado, apontada para a
# direita. Não diz de onde saiu nem para onde vai (os Homo sideralis e o
# destino deles são pendência da história). O ciano é a tecnologia de 3026
# (docs/historia/História_Completa.md, seção 2.4); o amarelo quente das
# janelas é o único sinal de gente a bordo.
#
# COMO FICA COM PROFUNDIDADE COM POUCOS TONS. O casco é um polígono comprido
# pintado em faixas horizontais: a luz vem de cima à direita (uma estrela fora
# do quadro), então cada faixa de baixo é mais escura que a de cima:
#
#   tom(y) = tom_do_topo - (y - y_topo) / altura_do_casco * contraste
#
# e depois o tom é quantizado em 5 degraus com dithering ordenado de Bayer 4x4
# (o mesmo de gerar_recortes_jornal.py). O rastro do motor é um gradiente que
# some com a distância, também pontilhado.

import os

import numpy as np
from PIL import Image, ImageDraw

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "visor", "quadro_nave.png")

LARGURA = 192
ALTURA = 120

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
CASCO = ["#0d1422", "#233049", "#3e5272", "#6a84a8", "#a9c0d8"]
FUNDO = ["#04060f", "#0a1030", "#1a1450", "#3a2470"]
CIANO = ["#0a3a48", "#12889c", "#5ee0ec", "#d8fbff"]


def cor(hexa):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4))


def limiar(altura, largura):
    return (BAYER[np.arange(altura)[:, None] % 4, np.arange(largura)[None, :] % 4] + 0.5) / 16.0


def pontilhar(tons, paleta):
    n = len(paleta)
    degrau = np.floor(np.clip(tons, 0, 1) * (n - 1) + limiar(*tons.shape))
    degrau = np.clip(degrau, 0, n - 1).astype(int)
    return np.array([cor(c) for c in paleta], dtype=np.uint8)[degrau]


def ruido(altura, largura, passo, semente):
    """Ruído suave: uma grade pequena de sorteios esticada com interpolação bilinear."""
    rng = np.random.default_rng(semente)
    pequeno = rng.random((altura // passo + 2, largura // passo + 2))
    grande = Image.fromarray((pequeno * 255).astype(np.uint8), "L").resize(
        (largura + 2 * passo, altura + 2 * passo), Image.BILINEAR)
    return np.asarray(grande, dtype=float)[:altura, :largura] / 255.0


def fundo():
    """Céu: azul-marinho com uma faixa de nebulosa roxa na diagonal e estrelas."""
    ys, xs = np.mgrid[0:ALTURA, 0:LARGURA]
    faixa = np.clip(1.0 - np.abs((ys - 0.45 * xs - 10) / 34.0), 0, 1)
    tons = 0.12 + 0.55 * faixa * (0.4 + 0.6 * ruido(ALTURA, LARGURA, 12, 3)) + 0.1 * ruido(ALTURA, LARGURA, 5, 4)
    imagem = pontilhar(tons, FUNDO)
    rng = np.random.default_rng(11)
    for _ in range(150):
        x, y = int(rng.integers(0, LARGURA)), int(rng.integers(0, ALTURA))
        imagem[y, x] = cor("#e8eeff") if rng.random() < 0.3 else cor("#7886b8")
    for _ in range(7):
        x, y = int(rng.integers(4, LARGURA - 4)), int(rng.integers(4, ALTURA - 4))
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            imagem[y + dy, x + dx] = cor("#ffffff")
    return imagem


def planeta(imagem):
    """Um planeta pequeno e minguante no canto de baixo à direita."""
    ys, xs = np.mgrid[0:ALTURA, 0:LARGURA]
    cx, cy, r = 168, 112, 26
    dentro = (xs - cx) ** 2 + (ys - cy) ** 2 < r * r
    sombra = (xs - cx - 12) ** 2 + (ys - cy + 10) ** 2 < (r - 2) ** 2
    tons = np.where(sombra, 0.1, 0.55 + 0.25 * ruido(ALTURA, LARGURA, 8, 9))
    pronto = pontilhar(tons, ["#0a0e1c", "#2a3a5c", "#4a6a88", "#7aa0a8"])
    imagem[dentro] = pronto[dentro]


def casco(imagem):
    """A nave: casco comprido em faixas, torre de comando em cima, fileiras de
    janelas acesas, três motores com rastro ciano à esquerda."""
    corpo = Image.new("L", (LARGURA, ALTURA), 0)
    d = ImageDraw.Draw(corpo)
    topo, base = 44, 78
    contorno = [(36, 54), (44, 46), (60, topo), (130, topo - 2), (160, 50), (182, 60),
                (160, 68), (130, base), (60, base + 2), (44, 72), (36, 66)]
    d.polygon(contorno, fill=255)
    d.polygon([(70, topo), (76, 30), (100, 26), (110, 34), (112, topo)], fill=255)
    d.rectangle((88, 18, 92, 28), fill=255)
    d.polygon([(64, base), (72, 92), (100, 92), (108, base)], fill=255)
    d.polygon([(118, topo - 2), (126, 36), (146, 38), (140, topo - 2)], fill=255)
    mascara = np.asarray(corpo) > 0
    ys, xs = np.mgrid[0:ALTURA, 0:LARGURA]
    tons = 0.95 - (ys - 20) / 80.0 * 0.85
    tons = tons - 0.12 * (ys % 6 == 0) + 0.06 * ruido(ALTURA, LARGURA, 3, 21)
    pronto = pontilhar(tons, CASCO)
    imagem[mascara] = pronto[mascara]
    contorno_escuro = mascara & ~np.pad(mascara, 1)[:-2, 1:-1] | mascara & ~np.pad(mascara, 1)[1:-1, :-2]
    imagem[contorno_escuro] = cor("#050810")
    for y in (56, 62, 68):
        for x in range(50, 170, 6):
            if mascara[y, x] and mascara[y, x + 2] and (x + y) % 12 != 0:
                imagem[y, x:x + 3] = cor("#ffd27a")
    for x in range(78, 106, 6):
        imagem[36, x:x + 3] = cor("#ffd27a")
    imagem[24, 89] = cor("#ff4a4a")
    for x in range(60, 150, 2):
        if mascara[topo + 6, x]:
            imagem[topo + 6, x] = cor("#16203a")
    return mascara


def motores(imagem):
    """Três bocais na popa e o rastro de luz saindo para a esquerda."""
    ys, xs = np.mgrid[0:ALTURA, 0:LARGURA]
    rastro = np.zeros((ALTURA, LARGURA))
    for yc in (52, 60, 68):
        comprimento = 34.0
        ao_longo = np.clip((36 - xs) / comprimento, 0, 1)
        espessura = 1.0 + 3.2 * (1.0 - ao_longo)
        dentro = (xs <= 36) & (np.abs(ys - yc) < espessura)
        rastro = np.maximum(rastro, np.where(dentro, (1.0 - ao_longo) ** 0.8, 0))
    luz = pontilhar(rastro, CIANO)
    mascara = rastro > 0.08
    imagem[mascara] = luz[mascara]
    for yc in (52, 60, 68):
        imagem[yc - 2:yc + 3, 35:37] = cor("#e8fdff")


def main():
    imagem = fundo()
    planeta(imagem)
    motores(imagem)
    casco(imagem)
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    Image.fromarray(imagem, "RGB").save(SAIDA)
    print("Quadro salvo em", SAIDA)


main()
