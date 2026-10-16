# gerar_praca_base.py — a base comum dos geradores da PRAÇA DE ALIMENTAÇÃO
# do Centro de Convivência (docs/fases/centro_de_convivencia.md):
#   - as rampas de cor novas (cerâmica, grafite, inox, os neons);
#   - a geometria da praça, que é um ARCO (a planta desenhada pelo Davi);
#   - ferramentas: texto em pixel (fonte Galmuri), brilho de neon e catálogo.
#
# Quem usa esta base:
#   gerar_praca.py        o fundo da praça (cúpula, fachadas em arco, piso)
#   gerar_restaurantes.py os fundos dos restaurantes e da passarela, os
#                         objetos e os letreiros
#   gerar_porta_restaurante.py  a porta de vidro dos restaurantes
#   montar_convivencia.py (em assets/modelagem/salas/centro_de_convivencia/)
#                         lê a mesma geometria para colocar portas e paredes
#
# Este arquivo não gera nada sozinho.
#
# ---------------------------------------------------------------------------
# A GEOMETRIA DO ARCO
# ---------------------------------------------------------------------------
#
# A planta do mapa é um semicírculo com a entrada no meio de cima e as lojas
# na curva. Numa sala de vista lateral, "cima" da planta é o FUNDO da sala
# (a parede de trás) e a curva vira uma parede de trás que DESCE para os
# lados: no meio ela fica longe (junto ao topo), nas pontas fica perto.
#
# A sala tem 25 colunas de 80 px. Em cada coluna c, a parede encosta no chão
# na altura y_base(c). Usamos a equação da elipse:
#
#     u = (x_centro - metade) / metade            (de -1 a 1)
#     y_base = 112 + H * (1 - raiz(1 - (k * u)^2))
#
# No meio (u = 0) dá 112, como em qualquer sala; para as pontas (u -> 1) a
# curva fica quase vertical, como o arco da planta. O k < 1 corta o arco
# antes da vertical. Arredondamos para múltiplos de 16 px: o piso é feito de
# placas de 16 px de altura, e assim as fileiras de uma coluna continuam as
# da vizinha, sem emenda.

import importlib.util
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_PRACA = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "praca")
FONTE_PIXEL = os.path.join(PASTA_PROJETO, "assets", "fontes", "galmuri_7.ttf")
CATALOGO = os.environ.get("CATALOGO", "")

_spec = importlib.util.spec_from_file_location("gerar_dtec", os.path.join(PASTA_SCRIPT, "gerar_dtec.py"))
dtec = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dtec)
kit = dtec.kit
bib = kit.bib

Imagem, RAMPAS, SOMBRA, dilatar = bib.Imagem, bib.RAMPAS, bib.SOMBRA, bib.dilatar
ruido = bib.ruido
ruido_ciclico = kit.ruido_ciclico
hexa = bib.hexa

PECA = 80
Y_PAREDE = 112
ALTURA_PAREDE = 112

COLUNAS_PRACA = 25
LARGURA_PRACA = COLUNAS_PRACA * PECA
ALTURA_PRACA = 560
ARCO_ALTURA = 420
ARCO_CORTE = 0.97
COLUNA_ENTRADA = COLUNAS_PRACA // 2

LOJAS_PRACA = {
    "loja_1": 7,
    "loja_2": 3,
    "loja_3": 17,
    "loja_4": 21,
}

# O SEGUNDO ANDAR (o mezanino): um anel em volta do vazio da praça, na mesma
# curva do arco. Em vista lateral ele é uma faixa de LARGURA_BALCAO px de
# profundidade que acompanha a parede de trás: da parede (y_base) até a beirada
# da laje (y_frente), onde fica o corrimão. Abaixo da beirada é o vazio do andar
# de baixo, que não aparece.
ANDAR2_LARGURA = LARGURA_PRACA
ANDAR2_ALTURA = 640
LARGURA_BALCAO = 112
ESPESSURA_LAJE = 14

LOJAS_ANDAR2 = {
    "grafica": 2,
    "loja_uni": 7,
    "cinema": 22,
}
COLUNA_ESCADA_MEZANINO = COLUNA_ENTRADA
COLUNA_ESCADA_PRACA = 14
COLUNA_ESCADA_INTERDITADA = 10


def y_frente(coluna):
    """Altura da beirada da laje do mezanino na coluna (onde fica o corrimão)."""
    return y_base(coluna) + LARGURA_BALCAO


def y_base(coluna):
    """Altura em que a parede da coluna encosta no chão (ver o cabeçalho)."""
    x_centro = coluna * PECA + PECA / 2
    u = (x_centro - LARGURA_PRACA / 2) / (LARGURA_PRACA / 2)
    y = Y_PAREDE + ARCO_ALTURA * (1.0 - math.sqrt(1.0 - (ARCO_CORTE * u) ** 2))
    return max(Y_PAREDE, int(round(y / 16.0)) * 16)


# ---------------------------------------------------------------------------
# Rampas de cor
# ---------------------------------------------------------------------------

RAMPAS.update({
    "grafite": hexa("#0b0e12", "#12161c", "#1b2028", "#262d37", "#343d4a", "#465263", "#5c6a7d", "#7a8a9e"),
    "ceramica": hexa("#1c2024", "#2b3035", "#3d4349", "#535a61", "#6d757c", "#8a9298", "#a9b0b5", "#c9cfd2"),
    "inox": hexa("#12151a", "#1e2329", "#2d343c", "#414a54", "#58636f", "#76828e", "#9aa6b0", "#c3ccd3"),
    "laje": hexa("#0a0d10", "#10151a", "#181e24", "#222a31", "#2d3740", "#3a4651", "#4b5965", "#5f6e7b"),
    "neon_ambar": hexa("#2a1604", "#5a2f08", "#a05a10", "#e08a1c", "#ffb23a", "#ffd98a", "#fff2cf"),
    "neon_magenta": hexa("#2a0a22", "#5c1648", "#9c2275", "#d83aa5", "#ff6ad0", "#ffa8e8", "#ffe0f6"),
    "neon_verde": hexa("#06241a", "#0d4a34", "#167a58", "#22b07c", "#4ee0a2", "#9ff5cc", "#e0fff2"),
    "neon_vermelho": hexa("#2b0a0a", "#5e1414", "#a32020", "#e03a2a", "#ff6a4a", "#ffa68a", "#ffe0d4"),
    "neon_violeta": hexa("#1a0c2e", "#34165c", "#5a2a9c", "#8a46d8", "#b27aff", "#d6b2ff", "#f2e6ff"),
    "bioluz": hexa("#06201e", "#0b3a35", "#13594f", "#1f8070", "#34b08e", "#6ee0b0"),
    "gelo": hexa("#16222c", "#223646", "#34536a", "#4f7a94", "#7aa8c0", "#acd2e2", "#dcf0f8"),
    "madeira_fut": hexa("#150f0b", "#241812", "#38271c", "#4f382a", "#6b4d3a", "#8a6650", "#a9846a"),
    "tijolo": hexa("#1d0f0c", "#2e1712", "#44221a", "#5d3024", "#7a4231", "#98573f"),
    "azulejo_branco": hexa("#22262a", "#343a40", "#4b535a", "#667078", "#848f97", "#a3adb3", "#c4ccd0"),
    "verde_agua": hexa("#0d2220", "#143432", "#1d4a46", "#2a625c", "#3b7d75", "#52a095", "#7bc4b6"),
    "xadrez_claro": hexa("#0e1c1d", "#162a2c", "#20403f", "#2d5a56", "#3f7a72", "#5fa095"),
    "xadrez_escuro": hexa("#060d0f", "#0b1618", "#112224", "#183033", "#21433f", "#2c5650"),
    "couro": hexa("#150a12", "#241020", "#3a1a34", "#53244a", "#6e3062", "#8a3f7c"),
    "neon_azul": hexa("#04122e", "#0a2a66", "#1450b8", "#2a7af0", "#5aa2ff", "#a6ceff", "#e2f0ff"),
    "neon_limao": hexa("#1c2204", "#3b4a08", "#6e8a10", "#a8cc1c", "#d4f23c", "#ecff8a", "#f9ffd0"),
    "carpete": hexa("#070e1e", "#0d1a35", "#152a52", "#1e3d72", "#2b5290", "#3a68ae"),
    "veludo": hexa("#14060c", "#260a16", "#3d1022", "#5a1830", "#7a2240", "#9a3052"),
    "papel_branco": hexa("#2a2d33", "#444850", "#646a72", "#868d95", "#a9b0b6", "#c9ced2", "#e6e9eb"),
    "concreto_fut": hexa("#101214", "#1b1e21", "#292d31", "#393e43", "#4c525a", "#626971"),
})

NEON = {
    "ciano": "ciano",
    "ambar": "neon_ambar",
    "magenta": "neon_magenta",
    "verde": "neon_verde",
    "vermelho": "neon_vermelho",
    "violeta": "neon_violeta",
    "azul": "neon_azul",
    "limao": "neon_limao",
}

# Cada restaurante tem a sua cor de neon: é o que o jogador usa para se
# orientar na praça sem ler o nome.
COR_LOJA = {
    "loja_1": "ambar",
    "loja_2": "verde",
    "loja_3": "vermelho",
    "loja_4": "magenta",
    "grafica": "limao",
    "loja_uni": "azul",
    "cinema": "violeta",
}

NOME_LOJA = {
    "loja_1": "TAPIOCA ORBITAL",
    "loja_2": "SELF NEBULOSA",
    "loja_3": "PIZZARIA QUASAR",
    "loja_4": "CHURRASCO SOLAR",
    "grafica": "GRÁFICA QUÂNTICA",
    "loja_uni": "LOJA UNIVERSITÁRIA",
    "cinema": "CINE ANDRÔMEDA",
}


# ---------------------------------------------------------------------------
# O que brilha (camada emissiva)
# ---------------------------------------------------------------------------
#
# O Godot escurece a sala inteira com o CanvasModulate (a "escuridão"), e isso
# vale até para o que é desenhado "sem luz". Para os neons e as vitrines
# brilharem no escuro, cada fundo ganha uma SEGUNDA imagem só com os pixels que
# brilham, que o Godot põe por cima com a cor multiplicada por 1 / escuridão
# (assim o produto com o CanvasModulate devolve a cor original, como se o pixel
# emitisse luz própria).
#
# Quais pixels brilham? Os que têm EXATAMENTE a cor de um tom claro de uma rampa
# de neon (as rampas do pintar() só têm essas cores, então a comparação é
# exata): do tom 2 em diante nos neons e no ciano, do tom 3 na bioluz, e os
# LEDs.

TONS_QUE_BRILHAM = (("neon_ambar", 2), ("neon_magenta", 2), ("neon_verde", 2), ("neon_vermelho", 2),
                    ("neon_violeta", 2), ("neon_azul", 2), ("neon_limao", 2), ("ciano", 2), ("bioluz", 3))
LEDS = ("#6cf28e", "#ffc24a", "#ff5a3a", "#8cf2ff")


def _empacotar(cores):
    return [(int(c[0]) << 16) | (int(c[1]) << 8) | int(c[2]) for c in cores]


def mascara_emissiva(px, excluir=()):
    """Máscara dos pixels de 'px' (altura x largura x 4) que brilham, menos
    os retângulos (x0, y0, x1, y1) de 'excluir' (as portas, que se mexem)."""
    alvo = []
    for nome, desde in TONS_QUE_BRILHAM:
        alvo += _empacotar(RAMPAS[nome][desde:])
    alvo += _empacotar(hexa(*LEDS))
    rgb = (px[..., 0].astype(np.uint32) << 16) | (px[..., 1].astype(np.uint32) << 8) | px[..., 2].astype(np.uint32)
    mascara = np.isin(rgb, np.array(alvo, dtype=np.uint32)) & (px[..., 3] > 0)
    for (x0, y0, x1, y1) in excluir:
        mascara[max(y0, 0):y1, max(x0, 0):x1] = False
    return mascara


def camada_emissiva(img, excluir=()):
    """Uma Imagem do mesmo tamanho com só os pixels que brilham."""
    luz = Imagem(img.w, img.h)
    m = mascara_emissiva(img.px, excluir)
    luz.px[m] = img.px[m]
    return luz


# ---------------------------------------------------------------------------
# Ferramentas
# ---------------------------------------------------------------------------


def texto_em_pixel(texto, tamanho=8):
    """Máscara (bool) do texto, desenhado com a fonte Galmuri sem suavização.
    No tamanho 8 a letra maiúscula tem 7 px de altura; no 16, o dobro."""
    fonte = ImageFont.truetype(FONTE_PIXEL, tamanho)
    caixa = fonte.getbbox(texto)
    largura, altura = caixa[2] - caixa[0] + 2, caixa[3] - caixa[1] + 2
    imagem = Image.new("1", (largura, altura), 0)
    desenho = ImageDraw.Draw(imagem)
    desenho.fontmode = "1"
    desenho.text((1 - caixa[0], 1 - caixa[1]), texto, font=fonte, fill=1)
    return np.array(imagem)


def escrever(img, x, y, texto, rampa, valor, tamanho=8, achatar=False):
    """Escreve o texto com o canto superior esquerdo em (x, y)."""
    mascara = texto_em_pixel(texto, tamanho)
    h, w = mascara.shape
    cheia = np.zeros((img.h, img.w), dtype=bool)
    y0, x0 = max(y, 0), max(x, 0)
    y1, x1 = min(y + h, img.h), min(x + w, img.w)
    if y0 >= y1 or x0 >= x1:
        return cheia
    cheia[y0:y1, x0:x1] = mascara[y0 - y:y1 - y, x0 - x:x1 - x]
    img.pintar(cheia, rampa, valor, achatar=achatar)
    return cheia


def largura_do_texto(texto, tamanho=8):
    return texto_em_pixel(texto, tamanho).shape[1]


def brilho(img, fonte, rampa, raio=4, forca=0.55, so_vazio=False):
    """Brilho de neon em volta de uma máscara: anéis de 1 px que se afastam
    da fonte, cada um mais escuro que o anterior. Cada anel é desenhado com
    dithering (pintar), então o brilho vira um pontilhado que some aos poucos.
    'so_vazio' deixa o brilho só onde ainda não há nada desenhado."""
    anterior = fonte
    for k in range(1, raio + 1):
        anel = dilatar(anterior)
        faixa = anel & ~anterior
        if so_vazio:
            faixa &= ~img.opaco()
        valor = forca * (1.0 - (k - 1) / raio) ** 1.6
        img.pintar(faixa, rampa, valor, achatar=False)
        anterior = anel


def gradiente_vertical(img, mascara, rampa, topo, base, y0, y1):
    """Pinta a máscara com um degradê de cima (valor 'topo') para baixo
    (valor 'base') entre as linhas y0 e y1."""
    t = np.clip((img.Y - y0) / max(y1 - y0, 1), 0.0, 1.0)
    img.pintar(mascara, rampa, topo + (base - topo) * t)


def colar_recorte(destino, origem, x, y):
    """Cola a Imagem 'origem' em 'destino' com o canto em (x, y), mantendo
    o que for opaco (como Imagem.colar, mas aceita cantos fora da tela)."""
    destino.colar(origem, x, y)


def salvar(img, nome, subpasta=""):
    pasta = os.path.join(PASTA_PRACA, subpasta) if subpasta else PASTA_PRACA
    os.makedirs(pasta, exist_ok=True)
    img.salvar(nome, pasta)


def catalogo(pecas, colunas, escala=2):
    return kit.catalogo(pecas, colunas, None, escala)


def salvar_catalogo(nome, pecas, colunas, escala=2):
    if not CATALOGO:
        return
    pasta = PASTA_SCRIPT if CATALOGO == "1" else CATALOGO
    os.makedirs(pasta, exist_ok=True)
    bib.salvar_png(os.path.join(pasta, f"{nome}.png"), catalogo(pecas, colunas, escala))
    print("  catálogo:", f"{nome}.png (não commitar)")
