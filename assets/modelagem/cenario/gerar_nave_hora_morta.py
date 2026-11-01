# gerar_nave_hora_morta.py — desenha por código as texturas da nave de Hora Morta,
# o filme de terror da Sala VR (docs/mecanicas/hora_morta.md): metal gasto, chapas,
# grades e a porta do fim do corredor, num visual mais realista que o resto do jogo.
#
# Cada textura nasce de um mapa de altura. A cor sai dele (sulcos escuros, bordas
# gastas) e o mapa de normais também: a normal de cada pixel vem da inclinação da
# altura, e é isso que faz a luz parecer pegar nos rebites e nas emendas.
#
# Como rodar (Python 3, Pillow e NumPy):
#   python assets/modelagem/cenario/gerar_nave_hora_morta.py
#
# O que sai, em assets/sprites/cenario/hora_morta/ (os *_n.png são os mapas de normais):
#   painel_nave      painéis de aço com emendas, rebites, riscos e sujeira escorrida
#   chao_chapa       chapa de piso com relevo em losangos
#   chao_grade       grade de metal do piso, com buracos escuros
#   teto_dutos       forro escuro atrás dos canos do teto
#   porta_nave       a porta inteira, com faixas de perigo e visor (não repete)
#   faixa_perigo     faixa amarela e preta

import os

import numpy as np
from PIL import Image, ImageDraw

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_SAIDA = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "hora_morta")

TAMANHO = 512
ACO = np.array([116.0, 126.0, 128.0])


def ruido(tamanho, escala, semente, esticar_y=1.0):
    # Ruído periódico: filtra números aleatórios no domínio de Fourier. A transformada
    # é periódica por definição, então a borda direita continua na esquerda, e a
    # textura repete sem emenda. Cortar as frequências altas deixa as manchas maiores.
    gerador = np.random.default_rng(semente)
    espectro = np.fft.fft2(gerador.normal(size=(tamanho, tamanho)))
    fy = np.fft.fftfreq(tamanho)[:, None] * esticar_y
    fx = np.fft.fftfreq(tamanho)[None, :]
    frequencia = np.sqrt(fx * fx + fy * fy) * escala
    campo = np.real(np.fft.ifft2(espectro / (1.0 + frequencia ** 3)))
    return (campo - campo.min()) / (campo.max() - campo.min())


def normais(altura, forca):
    # A inclinação vem da diferença entre vizinhos (com volta nas bordas). O vetor
    # (-dx, -dy, 1) normalizado aponta para fora da superfície e vira RGB em 0..255.
    dx = np.roll(altura, -1, axis=1) - np.roll(altura, 1, axis=1)
    dy = np.roll(altura, -1, axis=0) - np.roll(altura, 1, axis=0)
    nx, ny = -dx * forca, dy * forca
    comprimento = np.sqrt(nx * nx + ny * ny + 1.0)
    canais = np.stack((nx / comprimento, ny / comprimento, 1.0 / comprimento), axis=-1)
    return ((canais * 0.5 + 0.5) * 255.0).astype(np.uint8)


def salvar(nome, cor, altura=None, forca=6.0):
    imagem = np.clip(cor, 0.0, 255.0).astype(np.uint8)
    Image.fromarray(imagem, "RGB").save(os.path.join(PASTA_SAIDA, nome + ".png"))
    if altura is not None:
        Image.fromarray(normais(altura, forca), "RGB").save(os.path.join(PASTA_SAIDA, nome + "_n.png"))


def riscos(tamanho, quantos, semente):
    # Linhas finas e claras em ângulos parecidos, como metal arranhado pelo uso.
    gerador = np.random.default_rng(semente)
    camada = Image.new("L", (tamanho, tamanho), 0)
    traco = ImageDraw.Draw(camada)
    for _ in range(quantos):
        x, y = gerador.integers(0, tamanho, 2)
        angulo = gerador.normal(1.2, 0.35)
        comprimento = gerador.integers(15, 90)
        fim = (x + np.cos(angulo) * comprimento, y + np.sin(angulo) * comprimento)
        traco.line([(x, y), fim], fill=int(gerador.integers(40, 170)))
    return np.asarray(camada, dtype=float) / 255.0


def painel_nave():
    n = TAMANHO
    sujeira = ruido(n, 40.0, 11)
    escorrido = ruido(n, 60.0, 12, esticar_y=0.35)
    risco = riscos(n, 110, 13) * 0.45
    altura = np.ones((n, n)) * 0.6 + ruido(n, 6.0, 14) * 0.012 - risco * 0.015

    emenda = np.zeros((n, n))
    tinta = np.ones((n, n))
    gerador = np.random.default_rng(15)
    cortes_y = [0, 182, 356]
    for indice, y0 in enumerate(cortes_y):
        y1 = cortes_y[indice + 1] if indice + 1 < len(cortes_y) else n
        cortes_x = [0, 256] if indice != 1 else [0, 150, 340]
        for j, x0 in enumerate(cortes_x):
            x1 = cortes_x[j + 1] if j + 1 < len(cortes_x) else n
            tinta[y0:y1, x0:x1] = gerador.uniform(0.86, 1.08)
            emenda[y0:y0 + 3, x0:x1] = 1.0
            emenda[y0:y1, x0:x0 + 3] = 1.0
            for ry in (y0 + 13, y1 - 13):
                for rx in range(x0 + 13, x1 - 8, 46):
                    yy, xx = np.ogrid[:n, :n]
                    rebite = (yy - ry) ** 2 + (xx - rx) ** 2 <= 9
                    altura[rebite] += 0.11
                    tinta[rebite] *= 1.2

    altura -= emenda * 0.42
    desgaste = np.roll(emenda, 3, axis=0) + np.roll(emenda, 3, axis=1)
    cor = ACO[None, None, :] * tinta[:, :, None]
    cor *= (0.62 + 0.6 * sujeira)[:, :, None]
    cor *= (0.76 + 0.34 * escorrido)[:, :, None]
    cor += (risco * 60.0)[:, :, None]
    cor += (desgaste * 34.0)[:, :, None]
    cor *= (1.0 - emenda * 0.78)[:, :, None]
    ferrugem = np.clip(sujeira * escorrido - 0.4, 0.0, 1.0)[:, :, None] * np.array([60.0, 18.0, -14.0])
    salvar("painel_nave", cor + ferrugem, altura)


def chao_chapa():
    n = TAMANHO
    yy, xx = np.mgrid[:n, :n]
    passo = n / 16.0
    celula_x = (xx + yy) / passo
    celula_y = (xx - yy) / passo
    # Dois conjuntos de losangos, em tabuleiro, com a ponta virada para lados opostos.
    u, v = celula_x % 1.0 - 0.5, celula_y % 1.0 - 0.5
    par = (np.floor(celula_x) + np.floor(celula_y)) % 2 == 0
    losango = np.where(par, np.exp(-((u / 0.34) ** 2 + (v / 0.09) ** 2)), np.exp(-((u / 0.09) ** 2 + (v / 0.34) ** 2)))
    sujeira = ruido(n, 50.0, 21)
    risco = riscos(n, 220, 22)
    altura = 0.5 + losango * 0.32 + ruido(n, 6.0, 23) * 0.02
    cor = np.array([98.0, 102.0, 104.0])[None, None, :] * (0.48 + 0.72 * sujeira)[:, :, None]
    cor += (losango * 46.0 * sujeira)[:, :, None]
    cor += (risco * 44.0)[:, :, None]
    salvar("chao_chapa", cor, altura)


def chao_grade():
    n = TAMANHO
    yy, xx = np.mgrid[:n, :n]
    passo_x, passo_y = 32.0, 12.0
    linha = (yy // passo_y).astype(int)
    deslocado = xx + (linha % 2) * passo_x / 2.0
    fenda = ((deslocado % passo_x) < passo_x - 8.0) & ((yy % passo_y) < passo_y - 5.0)
    sujeira = ruido(n, 40.0, 31)
    altura = np.where(fenda, 0.05, 0.8) + ruido(n, 6.0, 32) * 0.02
    cor = np.array([92.0, 96.0, 98.0])[None, None, :] * (0.55 + 0.6 * sujeira)[:, :, None]
    cor = np.where(fenda[:, :, None], np.array([7.0, 8.0, 10.0]), cor)
    salvar("chao_grade", cor, altura, forca=3.0)


def teto_dutos():
    n = TAMANHO
    sujeira = ruido(n, 30.0, 41)
    altura = np.ones((n, n)) * 0.5
    altura[:, 120:128] -= 0.3
    altura[:, 380:388] -= 0.3
    altura[250:256, :] -= 0.3
    cor = np.array([42.0, 46.0, 50.0])[None, None, :] * (0.5 + 0.7 * sujeira)[:, :, None]
    cor *= (0.25 + 1.5 * altura)[:, :, None]
    salvar("teto_dutos", cor, altura)


def listras(largura, altura, deslocamento=0):
    grade_y, grade_x = np.mgrid[:altura, :largura]
    faixa = ((grade_x + grade_y + deslocamento) // 18) % 2 == 0
    cor = np.where(faixa[:, :, None], np.array([196.0, 150.0, 32.0]), np.array([22.0, 22.0, 24.0]))
    return cor


def faixa_perigo():
    n = TAMANHO // 2
    cor = np.tile(listras(n, n)[None], (1, 1, 1, 1))[0]
    sujeira = ruido(n, 18.0, 51)
    salvar("faixa_perigo", cor * (0.55 + 0.6 * sujeira)[:, :, None])


def porta_nave():
    # A porta é desenhada inteira, então usa a mesma base de metal e leva por cima as
    # peças: moldura, faixas, visor e placas. A altura acompanha cada peça.
    largura, altura_px = 512, 716
    n = max(largura, altura_px)
    sujeira = ruido(n, 40.0, 61)[:altura_px, :largura]
    escorrido = ruido(n, 60.0, 62, esticar_y=0.12)[:altura_px, :largura]
    risco = riscos(n, 200, 63)[:altura_px, :largura]
    base = np.array([112.0, 122.0, 124.0])[None, None, :] * (0.6 + 0.62 * sujeira)[:, :, None]
    base *= (0.76 + 0.34 * escorrido)[:, :, None]
    base += (risco * 54.0)[:, :, None]

    cor = base.copy()
    altura = Image.new("L", (largura, altura_px), 120)
    relevo = ImageDraw.Draw(altura)
    mascara = Image.new("L", (largura, altura_px), 0)
    sombra = ImageDraw.Draw(mascara)

    # Moldura octogonal: a porta recua em relação ao batente.
    canto = 62
    octogono = [(canto, 34), (largura - canto, 34), (largura - 34, canto), (largura - 34, altura_px - canto),
                (largura - canto, altura_px - 34), (canto, altura_px - 34), (34, altura_px - canto), (34, canto)]
    relevo.polygon(octogono, fill=90)
    sombra.line(octogono + octogono[:1], fill=210, width=7)

    paineis = [(70, 74, 232, 290), (278, 74, 442, 290), (70, 330, 232, 642), (278, 460, 442, 642)]
    for caixa in paineis:
        relevo.rounded_rectangle(caixa, 16, fill=146)
        sombra.rounded_rectangle(caixa, 16, outline=170, width=4)
    sombra.line([(256, 40), (256, altura_px - 40)], fill=240, width=5)

    sombra_arr = np.asarray(mascara, dtype=float)[:, :, None] / 255.0
    cor *= 1.0 - sombra_arr * 0.82

    # Visor da porta: vidro escuro com um reflexo na diagonal.
    grade_y, grade_x = np.mgrid[:altura_px, :largura]
    visor = (grade_x > 300) & (grade_x < 420) & (grade_y > 110) & (grade_y < 250)
    reflexo = (((grade_x - grade_y) % 120) < 16) & visor
    cor[visor] = np.array([24.0, 30.0, 36.0])
    cor[reflexo] = np.array([74.0, 88.0, 98.0])

    # Faixas de perigo: em cima, embaixo e nas laterais do batente.
    for y0, y1, x0, x1 in ((0, 26, 90, 422), (altura_px - 26, altura_px, 90, 422), (90, altura_px - 90, 0, 22),
                           (90, altura_px - 90, largura - 22, largura)):
        cor[y0:y1, x0:x1] = listras(x1 - x0, y1 - y0) * (0.65 + 0.5 * sujeira[y0:y1, x0:x1])[:, :, None]

    # Placas de aviso, para quebrar o metal liso.
    for x0, y0, x1, y1 in ((110, 150, 190, 230), (316, 520, 402, 594)):
        cor[y0:y1, x0:x1] = listras(x1 - x0, y1 - y0, 6) * 0.9

    altura_arr = np.asarray(altura, dtype=float) / 255.0
    salvar("porta_nave", cor, altura_arr, forca=4.0)


def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    painel_nave()
    chao_chapa()
    chao_grade()
    teto_dutos()
    faixa_perigo()
    porta_nave()


if __name__ == "__main__":
    main()
