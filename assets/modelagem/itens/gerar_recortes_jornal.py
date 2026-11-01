# gerar_recortes_jornal.py — desenha as IMAGENS dos três RECORTES DE JORNAL e o
# ícone do colecionável (docs/mecanicas/colecionaveis.md, "Recortes de jornal").
#
# Como rodar (Python 3 + Pillow + numpy):
#
#   python assets/modelagem/itens/gerar_recortes_jornal.py
#
# O que sai:
#   assets/sprites/interface/recorte_1.png ... recorte_3.png   220 x 74, a "foto" de cada
#                                                              recorte (tela de leitura)
#   assets/sprites/itens/recorte_jornal.png                    16 x 16, o ícone ("Novo item")
#   assets/sprites/itens/recorte_jornal_chao.png               o recorte caído no chão
#
# COMO A FOTO É FEITA. Cada cena é desenhada primeiro em TONS DE CINZA (0 a 1,
# onde 0 é a tinta e 1 é o papel), com formas simples. Depois o cinza vira
# poucas cores por DITHERING ORDENADO: compara-se o tom de cada pixel com uma
# matriz de limiares de Bayer 4 x 4 repetida na imagem. Se o tom passa do
# limiar o pixel clareia um degrau, senão fica no degrau de baixo. Isso dá o
# pontilhado de foto de jornal antigo com só 4 tons por imagem.
#
#   limiar(x, y) = (Bayer[y mod 4][x mod 4] + 0,5) / 16
#   degrau       = piso(tom * (n - 1) + limiar - 0,5)      (n = número de tons)
#
# As fotos 1 e 2 usam tinta e papel de jornal; a 3 usa o âmbar dos Faroleiros
# (docs/historia/História_Completa.md, seção 2.4): onde aparece âmbar, passou
# um Faroleiro.

import os

import numpy as np
from PIL import Image, ImageDraw

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_INTERFACE = os.path.join(PASTA_PROJETO, "assets", "sprites", "interface")
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")

LARGURA = 220
ALTURA = 74

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])

PALETA_JORNAL = ["#211f1b", "#5f5a4e", "#a09879", "#d9d1b5"]
PALETA_AMBAR = ["#150f0a", "#4a2a10", "#c97a1c", "#ffd98a"]
CIANO = "#5ee0ec"


def cor(hexa):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4))


def pontilhar(tons, paleta):
    """tons: matriz de 0 a 1. Devolve a imagem RGB com os tons trocados por
    degraus da paleta, com o limiar de Bayer decidindo cada pixel."""
    altura, largura = tons.shape
    n = len(paleta)
    limiar = (BAYER[np.arange(altura)[:, None] % 4, np.arange(largura)[None, :] % 4] + 0.5) / 16.0
    degrau = np.floor(np.clip(tons, 0, 1) * (n - 1) + limiar - 0.5 + 0.5)
    degrau = np.clip(degrau, 0, n - 1).astype(int)
    cores = np.array([cor(c) for c in paleta], dtype=np.uint8)
    return Image.fromarray(cores[degrau], "RGB")


def tela():
    """Uma tela cinza (modo L, 0 a 255) e a caneta dela."""
    imagem = Image.new("L", (LARGURA, ALTURA), 255)
    return imagem, ImageDraw.Draw(imagem)


def tons(imagem):
    return np.asarray(imagem, dtype=float) / 255.0


def pessoa(d, x, chao, altura, tom, cabeca=None):
    """Silhueta: cabeça redonda e corpo em trapézio, com o pé em 'chao'."""
    r = max(2, altura // 6)
    topo_corpo = chao - altura + 2 * r
    d.ellipse((x - r, chao - altura, x + r, chao - altura + 2 * r), fill=tom)
    d.polygon([(x - r - 1, chao), (x + r + 1, chao), (x + r, topo_corpo), (x - r, topo_corpo)], fill=tom)


def cena_conflito():
    """Uma avenida entre dois prédios de fachada cega: de um lado e do outro,
    uma multidão de silhuetas; no meio, uma faixa vazia. Do lado direito, as
    cabeças têm um ponto claro (o implante). Faixas de protesto nos dois lados."""
    imagem, d = tela()
    for y in range(0, 36):
        d.line((0, y, LARGURA, y), fill=int(235 - y * 1.6))
    rng = np.random.default_rng(7)
    x = 0
    while x < LARGURA:
        w = int(rng.integers(14, 26))
        h = int(rng.integers(20, 44))
        d.rectangle((x, 40 - h, x + w, 40), fill=int(rng.integers(90, 140)))
        for jy in range(40 - h + 4, 38, 6):
            for jx in range(x + 3, x + w - 2, 5):
                d.point((jx, jy), fill=200)
        x += w + 2
    d.rectangle((0, 40, LARGURA, ALTURA), fill=215)
    d.polygon([(95, 40), (125, 40), (140, ALTURA), (80, ALTURA)], fill=240)
    for yy in range(46, ALTURA, 8):
        d.line((108, yy, 112, yy), fill=150)
    luz = []
    for lado, (ini, fim) in enumerate(((6, 90), (130, 214))):
        x = ini
        while x < fim:
            chao = int(rng.integers(62, 72))
            altura = int(rng.integers(20, 30))
            pessoa(d, x, chao, altura, int(rng.integers(20, 60)))
            if lado == 1 and rng.random() < 0.45:
                luz.append((x + 2, chao - altura + 2))
            x += int(rng.integers(6, 10))
    for x0, x1 in ((24, 46), (150, 176)):
        d.line((x0, 34, x0, 56), fill=40)
        d.line((x1, 34, x1, 56), fill=40)
        d.rectangle((x0, 34, x1, 42), fill=235, outline=40)
        d.line((x0 + 3, 38, x1 - 3, 38), fill=60)
    return imagem, luz


def cena_plataforma():
    """Uma plataforma de embarque quase vazia: a nave enorme à direita, com a
    rampa baixada; uma fila curta de silhuetas com mala subindo; bancos vazios
    à esquerda. O céu é claro e a plataforma, escura."""
    imagem, d = tela()
    for y in range(0, 50):
        d.line((0, y, LARGURA, y), fill=int(250 - y * 1.1))
    d.ellipse((118, -46, 270, 62), fill=70)
    d.ellipse((126, -40, 262, 56), fill=95)
    for k in range(9):
        d.ellipse((140 + k * 9, 34 - abs(k - 4), 144 + k * 9, 38 - abs(k - 4)), fill=240)
    d.rectangle((120, 44, 146, 56), fill=40)
    d.rectangle((122, 46, 144, 56), fill=225)
    d.rectangle((0, 54, LARGURA, ALTURA), fill=60)
    d.rectangle((0, 54, LARGURA, 57), fill=150)
    d.polygon([(98, 57), (124, 57), (130, 52), (124, 52)], fill=140)
    d.line((98, 57, 124, 52), fill=140)
    for xb in (14, 46):
        d.rectangle((xb, 60, xb + 22, 62), fill=150)
        d.line((xb + 2, 62, xb + 2, 68), fill=150)
        d.line((xb + 20, 62, xb + 20, 68), fill=150)
        d.line((xb, 55, xb + 22, 55), fill=150)
    d.line((86, 40, 86, 60), fill=20)
    d.rectangle((78, 38, 94, 44), fill=235, outline=20)
    for k, x in enumerate((100, 110, 119, 127, 134, 140)):
        chao = 62 + (k % 2) * 2 - k // 2
        pessoa(d, x, chao + 6, 16, 235)
        d.rectangle((x + 3, chao + 1, x + 6, chao + 6), fill=235)
    return imagem


def cena_lanterna():
    """Uma roda de gente em volta de uma lanterna, de noite: poucas silhuetas
    sentadas (cabeça, ombros, um banco), a luz âmbar subindo da lanterna e,
    na parede do fundo, o farol dos Faroleiros rabiscado (torre, lanterna e
    três raios)."""
    imagem, d = tela()
    d.rectangle((0, 0, LARGURA, ALTURA), fill=18)
    cx, cy = 110, 56
    luz = np.zeros((ALTURA, LARGURA))
    ys, xs = np.mgrid[0:ALTURA, 0:LARGURA]
    dist = np.hypot((xs - cx) / 1.6, ys - cy)
    luz = np.clip(1.0 - dist / 62.0, 0, 1) ** 1.6
    d.rectangle((0, 60, LARGURA, ALTURA), fill=14)
    base = tons(imagem)
    t = np.clip(base * 0.1 + luz * 0.95, 0, 1)
    pronta = Image.fromarray((t * 255).astype(np.uint8), "L")
    d = ImageDraw.Draw(pronta)
    fx, fy = 188, 30
    d.polygon([(fx - 6, fy + 28), (fx + 6, fy + 28), (fx + 3, fy + 8), (fx - 3, fy + 8)], fill=170)
    d.rectangle((fx - 3, fy + 2, fx + 3, fy + 8), fill=235)
    for dx in (-14, 0, 14):
        d.line((fx, fy, fx + dx, fy - 14), fill=215, width=2)
    d.rectangle((cx - 3, 54, cx + 3, 60), fill=250)
    d.rectangle((cx - 2, 51, cx + 2, 53), fill=250)
    for k, x in enumerate((60, 80, 140, 160, 186, 32)):
        chao = 70 - (k % 2) * 2
        tom = 8
        d.ellipse((x - 5, chao - 24, x + 5, chao - 14), fill=tom)
        d.polygon([(x - 9, chao), (x + 9, chao), (x + 7, chao - 14), (x - 7, chao - 14)], fill=tom)
    d.ellipse((cx - 5, 61, cx + 5, 71), fill=8)
    return pronta


def icone(paleta):
    """16 x 16: um recorte de jornal dobrado ao meio, borda rasgada, com um
    bloco de 'foto' e linhas de texto."""
    linhas = [
        "................",
        "..oooooooooo....",
        ".opppppppppoo...",
        ".opqqqqqqpppo...",
        ".opqqqqqqpppo...",
        ".opqqqqqqpppo...",
        ".opppppppppppo..",
        ".oplllllllpppo..",
        ".opppppppppppo..",
        ".oplllllllllpo..",
        ".opppppppppppo..",
        ".oplllllpppppo..",
        ".opppppppppppo..",
        "..oooooooooooo..",
        "................",
        "................",
    ]
    cores = {"o": "#2a2722", "p": "#d9d1b5", "q": "#7a735d", "l": "#8f8869", ".": None}
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for y, linha in enumerate(linhas):
        for x, c in enumerate(linha):
            if cores[c]:
                img.putpixel((x, y), cor(cores[c]) + (255,))
    return img


def chao():
    """O recorte caído: um retângulo pequeno e torto, pé no meio da borda de baixo."""
    linhas = [
        "..oooooooo.",
        ".opppppqqpo",
        ".opllllqqpo",
        ".opppppppoo",
        ".opllllllpo",
        "..oooooooo.",
    ]
    cores = {"o": "#2a2722", "p": "#d9d1b5", "q": "#7a735d", "l": "#8f8869"}
    img = Image.new("RGBA", (11, 6), (0, 0, 0, 0))
    for y, linha in enumerate(linhas):
        for x, c in enumerate(linha):
            if c in cores:
                img.putpixel((x, y), cor(cores[c]) + (255,))
    return img


def main():
    os.makedirs(PASTA_INTERFACE, exist_ok=True)
    os.makedirs(PASTA_ITENS, exist_ok=True)

    conflito, pontos = cena_conflito()
    foto = pontilhar(tons(conflito), PALETA_JORNAL)
    for (x, y) in pontos:
        foto.putpixel((x, y), cor(CIANO))
    foto.save(os.path.join(PASTA_INTERFACE, "recorte_1.png"))

    pontilhar(tons(cena_plataforma()), PALETA_JORNAL).save(os.path.join(PASTA_INTERFACE, "recorte_2.png"))
    pontilhar(tons(cena_lanterna()), PALETA_AMBAR).save(os.path.join(PASTA_INTERFACE, "recorte_3.png"))

    icone(PALETA_JORNAL).save(os.path.join(PASTA_ITENS, "recorte_jornal.png"))
    chao().save(os.path.join(PASTA_ITENS, "recorte_jornal_chao.png"))
    print("Recortes salvos em", PASTA_INTERFACE, "e", PASTA_ITENS)


main()
