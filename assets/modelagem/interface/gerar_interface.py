# gerar_interface.py — desenha, por código, os ÍCONES DOS ITENS e as peças
# da INTERFACE (inventário e espaços de gadget), no mesmo estilo da
# Biblioteca: mesma paleta, mesmo dithering, mesmo contorno escuro.
#
# Como rodar (Python 3 + numpy, igual ao gerar_biblioteca.py):
#
#   python assets/modelagem/interface/gerar_interface.py
#
# O que sai:
#   assets/sprites/itens/<item>.png                16 x 16 px: ícone do item (inventário)
#   assets/sprites/itens/<item>_chao.png           o item caído no chão, na escala do
#                                                  cenário (1 px ≈ 3,6 cm: uma lanterna tem ~6 px)
#   assets/sprites/itens/lanterna_mao.png          14 x 8 px: a lanterna na mão do Gabriel (resolução dobrada)
#   assets/sprites/interface/espaco.png            20 x 20 px: um espaço vazio da grade
#   assets/sprites/interface/espaco_selecionado.png  o mesmo, com a borda acesa
#   assets/sprites/interface/painel.png            24 x 24 px: fundo das janelas, em
#                                                  "9 fatias" (NinePatchRect no Godot)
#   assets/sprites/interface/papel_<estilo>.png    248 x 156 px: a folha onde se lê um
#                                                  documento (tela de leitura e caderno)
#
# Os papéis não são "9 fatias": cada um é desenhado já no tamanho em que
# aparece, porque as pautas e o quadriculado precisam cair exatamente
# embaixo das linhas de texto. A fonte Ark Pixel no tamanho 10 tem 14 px de
# altura (11 acima da linha de base, com espaço para os acentos, e 3 abaixo)
# e o tema do jogo não põe espaço extra entre as linhas: uma linha de texto
# a cada 14 px. O texto começa em y = TOPO_TEXTO, então a pauta da linha i
# fica em TOPO_TEXTO + 13 + 14 * i (na última fileira das letras que
# descem, como g e p).
# Se mudar essas medidas aqui, mude também em cenas/interface/tela_documento.tscn.
#
# Este script IMPORTA as funções do gerar_biblioteca.py (paleta, pintar com
# dithering, contorno...), como o gerar_kit.py faz. Assim um ícone novo sai
# automaticamente com as mesmas cores do cenário.
#
# Painel em "9 fatias": a imagem é dividida em 3 x 3 pedaços. Os 4 cantos
# ficam do tamanho original, as 4 bordas esticam só num sentido e o meio
# estica nos dois. Assim uma imagem pequena vira uma janela de qualquer
# tamanho sem deformar a moldura. No Godot, o NinePatchRect faz isso: as
# margens (patch_margin) dizem onde cortar — aqui, 6 px de cada lado.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")
PASTA_INTERFACE = os.path.join(PASTA_PROJETO, "assets", "sprites", "interface")

# Importa o gerar_biblioteca.py como um módulo (sem rodar o main dele).
_spec = importlib.util.spec_from_file_location(
    "gerar_biblioteca",
    os.path.join(PASTA_PROJETO, "assets", "modelagem", "salas", "biblioteca", "gerar_biblioteca.py"))
bib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bib)

Imagem, RAMPAS, CONTORNO, ruido = bib.Imagem, bib.RAMPAS, bib.CONTORNO, bib.ruido

TAMANHO_ICONE = 16
TAMANHO_ESPACO = 20
TAMANHO_PAINEL = 24
MARGEM_PAINEL = 6       # patch_margin do NinePatchRect (mude lá se mudar aqui)

# Cores da lanterna, tiradas da imagem detalhada dela
# (assets/sprites/itens/lanterna_detalhe.png): carcaça de alumínio anodizado
# azul-acinzentado escuro, com reflexos de aço claros, botão vermelho,
# lente com o miolo quente e uma alça de pulso de nylon preto.
ACO = bib.hexa("#0e1118", "#1a202b", "#2a3342", "#3e4a5e", "#5c6b82", "#8d9bb2", "#c4cedd")
VERMELHO_BOTAO = bib.hexa("#4a1208", "#8a2214", "#d03a22", "#ee6a44")
NYLON = bib.hexa("#08090c", "#11141a", "#1c2029", "#2a303c")

# Cores do rádio, tiradas da imagem detalhada dele
# (assets/sprites/itens/radio_detalhe.png): carcaça de plástico verde-oliva
# com a quina de cima quase menta, detalhes em laranja (anel da antena, aro do
# botão de falar, botão de emergência), tela de LCD verde e borracha cinza
# escura na antena, na grade do alto-falante e no para-choque de baixo.
OLIVA_RADIO = bib.hexa("#141a12", "#242e20", "#3a4630", "#535f3f", "#6c7852", "#8a9a6c", "#b5cba8")
LARANJA_RADIO = bib.hexa("#4a1d08", "#8c3c12", "#d16b23", "#f59a51")
LCD_RADIO = bib.hexa("#1f2e1c", "#3e5a38", "#6c8f65", "#9ed591")
BORRACHA_RADIO = bib.hexa("#121316", "#1f2024", "#2c2c34", "#3c3e45", "#52565a", "#6f7875")
TECLA_RADIO = bib.hexa("#5e636e", "#9298a6", "#c2ccd6")

# A lâmpada da cápsula de clarão (clarao_detalhe.png), uma bolha de vidro
# azul-clara, e a tela acesa do notebook (notebook_detalhe.png), branco-azulada.
# A pedra (pedra_detalhe.png): cinza-pedra neutro, claro e quente em cima,
# azulado e escuro nas sombras.
PEDRA_CINZA = bib.hexa("#1c1c26", "#38383f", "#5a5a60", "#807d7a", "#a89f98", "#cbbfae", "#ece0cc")
LAMPADA_CLARAO = bib.hexa("#2a5fb0", "#4d8fe0", "#86c3f5", "#c8ecff", "#f2fbff")
TELA_NOTEBOOK = bib.hexa("#4f5d6e", "#7f8fa3", "#aebdd0", "#cfdbe8", "#e4edf5")


# ---------------------------------------------------------------------------
# Ícones dos itens
# ---------------------------------------------------------------------------


def lanterna():
    """A lanterna do Gabriel, a mesma da imagem detalhada
    (lanterna_detalhe.png) e a que ele leva na mão (lanterna_mao): corpo
    cilíndrico de aço azulado, deitado, com a cabeça larga e a lente redonda à
    esquerda (aro escuro, miolo quente), o botão vermelho em cima, a pegada
    xadrez no meio e a alça de pulso de nylon preto fazendo um laço embaixo.
    Não tem luz acesa no ícone: se ela está ligada, o espaço de gadget mostra."""
    img = Imagem(TAMANHO_ICONE, TAMANHO_ICONE)
    X, Y = img.X, img.Y
    img.pintar(img.caminho([(13, 9), (14, 12), (11, 14), (8, 13), (8, 10)], 0.55), NYLON, 0.6)
    img.pintar(img.ret(6, 5, 14, 10), ACO, 0.5 - 0.3 * (Y - 5) / 5 + 0.25 * (Y == 5))
    img.pintar(img.ret(9, 5, 13, 10) & ((X + Y) % 2 == 0), ACO, 0.12)
    img.pintar(img.ret(13, 5, 15, 10), ACO, 0.6 - 0.35 * (Y - 5) / 5)
    img.pintar(img.ret(2, 4, 7, 11), ACO, 0.55 - 0.3 * (Y - 4) / 6 + 0.2 * (Y == 4))
    img.pintar(img.ret(7, 4, 8, 11), ACO, 0.8)
    img.pintar(img.ret(7, 3, 10, 5), VERMELHO_BOTAO, 0.9)
    img.pintar(img.ret(7, 4, 10, 5), VERMELHO_BOTAO, 0.4)
    img.pintar(img.ret(1, 5, 3, 10), "metal", 0.15)
    img.pintar(img.ret(1, 5, 3, 10) & ~((X == 1) & ((Y == 5) | (Y == 9))), "lampada", 0.7)
    img.pintar(img.ret(1, 6, 2, 9), "lampada", 1.0)
    img.contornar(CONTORNO)
    return img


def lanterna_chao():
    """A mesma lanterna caída no chão, na escala do cenário: um pouco maior
    que a da mão (7 x 4 px contra 6 x 3) porque aqui o contorno e o corpo
    aparecem inteiros. Um corpo de aço azulado com o botão vermelho e a lente
    acesa na ponta direita."""
    img = Imagem(7, 4)
    img.pintar(img.ret(1, 1, 5, 2), ACO, 0.65)
    img.pintar(img.ret(1, 2, 5, 3), ACO, 0.3)
    img.pintar(img.ret(2, 1, 3, 2), VERMELHO_BOTAO, 0.9)
    img.pintar(img.ret(5, 1, 6, 3), "lampada", 0.85)
    img.contornar(CONTORNO)
    return img


def lanterna_mao():
    """A lanterna como o Gabriel a segura: 14 x 8 px, em resolução dobrada (o
    jogo mostra com escala 0,5, então ocupa 7 x 4 px no mundo, com o contorno,
    e o corpo tem ~6 x 3, uns 20 cm na escala do personagem, 1 px ~ 3,6 cm).
    Corpo cilíndrico de aço azulado à esquerda, a cabeça mais larga e a lente
    na ponta direita, com o botão vermelho em cima. Está apontada para a
    direita, com a pegada (o ponto de x = 5) no meio do corpo: o jogo põe esse
    ponto na mão do Gabriel e gira e espelha o sprite conforme a direção da
    mira (scripts/itens/lanterna.gd)."""
    img = Imagem(14, 8)
    Y = img.Y
    img.pintar(img.ret(2, 3, 9, 6), ACO, 0.55 - 0.3 * (Y - 3) / 3 + 0.2 * (Y == 3))
    img.pintar(img.ret(9, 2, 12, 7), ACO, 0.6 - 0.3 * (Y - 2) / 5 + 0.2 * (Y == 2))
    img.pintar(img.ret(5, 2, 7, 3), VERMELHO_BOTAO, 0.85)
    img.pintar(img.ret(12, 3, 13, 6), "lampada", 0.9)
    img.contornar(CONTORNO)
    return img


def pilha():
    """Pilha grande (tipo D): corpo cilíndrico com a faixa de cor da
    marca, o polo positivo em cima e o reflexo de metal."""
    img = Imagem(TAMANHO_ICONE, TAMANHO_ICONE)
    X, Y = img.X, img.Y
    corpo = img.ret(5, 3, 11, 15)
    img.pintar(corpo, "metal", 0.2 + 0.25 * (1 - (X - 5) / 6))
    img.pintar(img.ret(5, 7, 11, 11), "ferrugem", 0.55 + 0.2 * (1 - (X - 5) / 6))   # faixa da marca
    img.pintar(img.ret(7, 1, 9, 3), "metal", 0.6)                                  # polo +
    img.pintar(img.ret(6, 4, 7, 14), "ceu", 0.5)                                   # reflexo
    img.contornar(CONTORNO)
    return img


def pilha_chao():
    """A pilha deitada no chão: 3 px de corpo, a faixa e o polo."""
    img = Imagem(7, 4)
    img.pintar(img.ret(0, 0, 6, 3), "metal", 0.35)
    img.pintar(img.ret(2, 0, 4, 3), "ferrugem", 0.6)
    img.pintar(img.ret(6, 1, 7, 2), "metal", 0.6)
    img.contornar(CONTORNO)
    return img


def radio():
    """O rádio portátil do grupo (um HT da segurança, de 2008), o mesmo da
    imagem detalhada (radio_detalhe.png): carcaça verde-oliva com a quina da
    esquerda clara, antena de borracha com anel laranja, o botão de volume em
    cima, o botão de falar (PTT) na lateral com aro laranja, a tela de LCD
    verde, a grade do alto-falante e a fileira de teclas embaixo (duas cinza
    e a de emergência laranja)."""
    img = Imagem(TAMANHO_ICONE, TAMANHO_ICONE)
    X, Y = img.X, img.Y
    fino = ruido(img.w, img.h, 2, 2, 11)
    # Antena: bastão de 2 px, com o anel laranja perto da ponta e o colar na base.
    img.pintar(img.ret(5, 0, 7, 6), BORRACHA_RADIO, 0.3 + 0.25 * (X == 5))
    img.pintar(img.ret(5, 1, 7, 2), LARANJA_RADIO, 0.7)
    img.pintar(img.ret(5, 5, 7, 6), LARANJA_RADIO, 0.55)
    # Botão de volume em cima, à direita.
    img.pintar(img.ret(9, 3, 13, 5), OLIVA_RADIO, 0.18 + 0.15 * (Y == 3))
    # Carcaça: a lateral esquerda (2 px) e a frente, de cantos cortados.
    corpo = img.poligono([(3, 6), (4, 5), (13, 5), (14, 6), (14, 14), (13, 15), (4, 15), (3, 14)])
    img.pintar(corpo, OLIVA_RADIO, 0.5 + 0.06 * fino)
    img.pintar(corpo & (X < 5), OLIVA_RADIO, 0.36 + 0.06 * fino)
    img.pintar(corpo & (Y == 5) & (X > 4), OLIVA_RADIO, 0.72)
    img.pintar(img.ret(5, 5, 6, 14), OLIVA_RADIO, 1.0)
    # Botão de falar (PTT) na lateral, com aro laranja.
    img.pintar(img.ret(2, 7, 4, 11), LARANJA_RADIO, 0.6)
    img.pintar(img.ret(3, 8, 4, 10), BORRACHA_RADIO, 0.35)
    # Tela de LCD: verde, com uma linha de números ("CH 08") mais escura.
    img.pintar(img.ret(7, 6, 13, 9), LCD_RADIO, 0.75)
    img.pintar(img.ret(8, 7, 12, 8) & (X != 10), LCD_RADIO, 0.3)
    # Grade do alto-falante: fendas horizontais na borracha escura.
    img.pintar(img.ret(7, 10, 13, 13), BORRACHA_RADIO, 0.2 + 0.25 * (Y % 2 == 1))
    # Teclas: duas cinza e a de emergência laranja.
    img.pintar(img.ret(7, 13, 8, 14) | img.ret(9, 13, 10, 14), TECLA_RADIO, 0.6)
    img.pintar(img.ret(11, 13, 13, 14), LARANJA_RADIO, 0.85)
    # Para-choque de borracha embaixo.
    img.pintar(corpo & (Y == 14), BORRACHA_RADIO, 0.25)
    img.contornar(CONTORNO)
    return img


def radio_chao():
    """O mesmo rádio caído no chão, na escala do cenário: um HT tem uns
    20 cm, então ~6 px de corpo mais a antena. Carcaça oliva com a quina
    clara, tela verde, a grade escura e o ponto laranja da tecla."""
    img = Imagem(7, 11)
    img.pintar(img.ret(1, 0, 2, 4), BORRACHA_RADIO, 0.35)
    img.pintar(img.ret(1, 1, 2, 2), LARANJA_RADIO, 0.7)
    corpo = img.ret(1, 3, 6, 10)
    img.pintar(corpo, OLIVA_RADIO, 0.45)
    img.pintar(img.ret(1, 3, 2, 9), OLIVA_RADIO, 0.85)
    img.pintar(img.ret(2, 4, 5, 5), LCD_RADIO, 0.8)
    img.pintar(img.ret(2, 6, 5, 8), BORRACHA_RADIO, 0.2 + 0.2 * (img.Y == 7))
    img.pintar(img.ret(4, 8, 5, 9), LARANJA_RADIO, 0.8)
    img.pintar(img.ret(1, 9, 6, 10), BORRACHA_RADIO, 0.25)
    img.contornar(CONTORNO)
    return img


def clarao():
    """Cápsula de clarão (clarao_detalhe.png): cilindro de aço escuro
    deitado, com a ponta de trás frisada e enferrujada, o anel de cobre
    parafusado, uma braçadeira no meio e, na frente, a coroa dentada que
    segura a lâmpada: uma bolha de vidro azul-clara."""
    img = Imagem(TAMANHO_ICONE, TAMANHO_ICONE)
    X, Y = img.X, img.Y
    img.pintar(img.ret(1, 5, 12, 12), "metal", 0.12 + 0.35 * (Y == 6) + 0.1 * (Y == 7))
    img.pintar(img.ret(1, 5, 4, 12) & (Y % 2 == 1), "metal", 0.02)
    img.pintar(img.ret(1, 5, 4, 12) & (Y % 2 == 0), "ferrugem", 0.45)
    img.pintar(img.ret(4, 5, 6, 12), "ferrugem", 0.75 + 0.2 * (Y == 5))
    img.pintar(img.ret(8, 5, 9, 12), "metal", 0.45)
    img.pintar(img.ret(10, 4, 12, 13), "metal", 0.2 + 0.3 * (X == 10))
    img.pintar(img.ret(11, 4, 12, 13) & (Y % 2 == 0), "metal", 0.0)
    img.pintar(img.elipse(13.0, 8.5, 2.6, 3.6) & (X >= 12), LAMPADA_CLARAO, 0.55)
    img.pintar(img.elipse(13.6, 7.6, 1.2, 1.4) & (X >= 12), LAMPADA_CLARAO, 1.0)
    img.contornar(CONTORNO)
    return img


def clarao_chao():
    """A cápsula no chão: o corpo escuro com o anel de cobre e a lâmpada
    azul-clara na ponta."""
    img = Imagem(7, 4)
    img.pintar(img.ret(0, 0, 5, 3), "metal", 0.15)
    img.pintar(img.ret(1, 0, 2, 3), "ferrugem", 0.75)
    img.pintar(img.ret(5, 0, 7, 3), LAMPADA_CLARAO, 0.8)
    img.contornar(CONTORNO)
    return img


def pedra():
    """A pedra (pedra_detalhe.png): um pedaço de pedra cinza arredondado, do
    tamanho da mão, com o topo claro e quente (a luz vem de cima, da
    esquerda) e o lado direito e a base em sombra azulada."""
    img = Imagem(TAMANHO_ICONE, TAMANHO_ICONE)
    X, Y = img.X, img.Y
    corpo = img.poligono([(2, 11), (3, 7), (6, 4), (10, 3), (13, 6), (14, 10), (13, 13), (4, 13)])
    luz = 0.85 - 0.5 * (Y - 3) / 10 - 0.3 * (X - 2) / 12
    img.pintar(corpo, PEDRA_CINZA, luz + 0.1 * ruido(img.w, img.h, 2, 2, 7))
    img.pintar(img.ret(4, 5, 8, 6) & corpo, PEDRA_CINZA, 1.0)
    img.contornar(CONTORNO)
    return img


def pedra_chao():
    """Três pedrinhas juntas no chão (cada monte vale uma pedra no inventário)."""
    img = Imagem(9, 4)
    for x0, topo in ((0, 1), (3, 0), (6, 2)):
        img.pintar(img.ret(x0, topo, x0 + 3, 4), PEDRA_CINZA, 0.45)
        img.pintar(img.ret(x0, topo, x0 + 2, topo + 1), PEDRA_CINZA, 0.95)
        img.pintar(img.ret(x0 + 2, topo + 1, x0 + 3, 4), PEDRA_CINZA, 0.2)
    img.contornar(CONTORNO)
    return img


def notebook():
    """Notebook de campo (notebook_detalhe.png): carcaça robusta de plástico
    cinza-chumbo com cantoneiras nas quinas e manchas de ferrugem, a tela
    branco-azulada acesa com a barra verde e os blocos de dados, as
    dobradiças cor de ferrugem e a base grossa com o teclado escuro."""
    img = Imagem(TAMANHO_ICONE, TAMANHO_ICONE)
    X, Y = img.X, img.Y
    fino = ruido(img.w, img.h, 2, 2, 23)
    img.pintar(img.ret(2, 1, 14, 10), "metal", 0.18 + 0.08 * fino)
    img.pintar(img.ret(2, 1, 4, 3) | img.ret(12, 1, 14, 3), "metal", 0.4)
    img.pintar(img.ret(3, 2, 13, 9), TELA_NOTEBOOK, 0.75 + 0.2 * (Y < 4))
    img.pintar(img.ret(4, 3, 9, 4), "verde", 0.85)
    img.pintar(img.ret(4, 6, 12, 7) & (X % 3 == 1), TELA_NOTEBOOK, 0.35)
    img.pintar(img.ret(4, 10, 6, 11) | img.ret(10, 10, 12, 11), "ferrugem", 0.45)
    img.pintar(img.ret(1, 11, 15, 15), "metal", 0.2 + 0.08 * fino)
    img.pintar(img.ret(3, 11, 13, 13) & ((X + Y) % 2 == 0), "metal", 0.04)
    img.pintar(img.ret(1, 14, 15, 15), "metal", 0.1)
    img.pintar(img.ret(13, 13, 14, 14), "verde", 0.95)
    img.pintar(img.ret(2, 13, 3, 14), "ferrugem", 0.4)
    img.contornar(CONTORNO)
    return img


def notebook_chao():
    """O notebook fechado no chão: uma placa grossa cinza-chumbo, com as
    dobradiças cor de ferrugem e o LED verde aceso."""
    img = Imagem(9, 3)
    img.pintar(img.ret(0, 0, 9, 3), "metal", 0.22)
    img.pintar(img.ret(1, 0, 3, 1) | img.ret(6, 0, 8, 1), "ferrugem", 0.45)
    img.pintar(img.ret(7, 1, 8, 2), "verde", 0.95)
    img.contornar(CONTORNO)
    return img


# Nome do arquivo -> função que desenha. Um item novo entra aqui.
ICONES = {
    "lanterna": lanterna,
    "lanterna_chao": lanterna_chao,
    "lanterna_mao": lanterna_mao,
    "pilha": pilha,
    "pilha_chao": pilha_chao,
    "radio": radio,
    "radio_chao": radio_chao,
    "clarao": clarao,
    "clarao_chao": clarao_chao,
    "pedra": pedra,
    "pedra_chao": pedra_chao,
    "notebook": notebook,
    "notebook_chao": notebook_chao,
}


# ---------------------------------------------------------------------------
# Papéis (tela de leitura de documentos e caderno do Gabriel)
# ---------------------------------------------------------------------------

LARGURA_PAPEL = 248
ALTURA_PAPEL = 156
TOPO_TITULO = 6         # onde começa o título (1 linha)
TOPO_TEXTO = 22         # onde começa o texto
PASSO_LINHA = 14        # altura da linha da fonte Ark Pixel 10
LINHAS_TEXTO = 8        # linhas por página
MARGEM_TEXTO = 14       # x onde começa o texto

# Os papéis são as únicas coisas CLARAS do jogo: precisam ser lidos. Por
# isso têm rampas próprias, mais claras que a rampa "papel" do cenário
# (que é papel de mil anos, quase marrom).
PERGAMINHO = bib.hexa("#4a3419", "#6b4f27", "#8c6d3a", "#a8894f", "#c0a266", "#d2b87e", "#dfca94")
PAPEL_CLARO = bib.hexa("#7d7868", "#9f9985", "#bdb69e", "#d3cbb2", "#e2dbc4", "#ece6d2")
AZUL_PAUTA = bib.hexa("#9aabc4")[0]
VERMELHO_MARGEM = bib.hexa("#c07a70")[0]
CINZA_GRADE = bib.hexa("#c9c6b8")[0]
TINTA_MARROM = bib.hexa("#3a2210")[0]


def pautas():
    """Os y das pautas: uma embaixo do título e uma embaixo de cada linha
    de texto."""
    return [TOPO_TITULO + 13] + [TOPO_TEXTO + 13 + PASSO_LINHA * i for i in range(LINHAS_TEXTO)]


def borda_rasgada(img, forca, semente):
    """Máscara da folha com as bordas irregulares. Para cada lado, um ruído
    diz quantos pixels "comer" naquela altura (ou coluna): de 0 a 'forca'.
    Borda de papel velho nunca é reta."""
    w, h = img.w, img.h
    r = ruido(w, h, 5, 5, semente)
    esq = np.floor(forca * r[:, 0])[:, None]
    dir_ = np.floor(forca * r[:, w // 2])[:, None]
    cima = np.floor(forca * r[h // 2, :])[None, :]
    baixo = np.floor(forca * r[h // 3, :])[None, :]
    X, Y = img.X, img.Y
    return (X >= esq) & (X < w - dir_) & (Y >= cima) & (Y < h - baixo)


def perto_da_borda(folha, passos):
    """Quantos passos de 'encolher' a folha até o pixel sumir: 0 na borda,
    'passos' no miolo. Serve para escurecer as bordas (papel velho amarela
    e suja primeiro nas pontas)."""
    dist = np.zeros(folha.shape)
    m = folha.copy()
    for i in range(passos):
        p = np.pad(m, 1)
        m = m & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
        dist += m
    return dist / passos


def papel_pergaminho():
    """O diário do Baltazar (1750): pergaminho amarelado, bordas comidas e
    escuras, manchas de umidade. No canto de baixo, o esboço a pena que ele
    fez do robô: a cabeça, o olho de vidro e duas linhas saindo do olho, o
    "cone" do que o robô enxerga (docs/historia/personagens/robos.md: a visão dos
    robôs é um cone, calculado por produto escalar)."""
    img = Imagem(LARGURA_PAPEL, ALTURA_PAPEL)
    X, Y = img.X, img.Y
    folha = borda_rasgada(img, 4, 21)
    manchas = ruido(img.w, img.h, 30, 24, 22)
    fino = ruido(img.w, img.h, 2, 2, 23)
    borda = perto_da_borda(folha, 10)
    v = 0.62 + 0.14 * manchas + 0.04 * fino - 0.45 * (1 - borda)
    # Duas manchas de umidade: círculos um pouco mais escuros.
    for (cx, cy, r) in ((168, 30, 14), (40, 120, 10)):
        v = v - 0.12 * img.elipse(cx, cy, r, r * 0.8)
    img.pintar(folha, PERGAMINHO, v)
    img.contornar(PERGAMINHO[0])
    # Esboço do robô (tinta marrom, traço de 1 px).
    tinta = np.zeros(folha.shape, dtype=bool)
    cabeca = img.elipse(26, 145, 9, 7) & ~img.elipse(26, 145, 8, 6)
    olho = img.elipse(29, 144, 3, 3) & ~img.elipse(29, 144, 2, 2)
    tinta |= cabeca | olho | img.ret(29, 144, 30, 145)
    tinta |= img.linha(32, 143, 62, 137) | img.linha(32, 145, 62, 153)
    tinta |= img.linha(19, 151, 17, 154) | img.linha(33, 151, 35, 154)
    img.cor(tinta & folha, TINTA_MARROM)
    return img


def papel_caderno_clarice():
    """O bilhete da Clarice (1990): folha de fichário, com os furos do lado,
    pautas azuis, a margem vermelha e um adesivo de estrela no canto. Em
    cima, o pedaço de fita adesiva que a prendia na tela do terminal."""
    img = Imagem(LARGURA_PAPEL, ALTURA_PAPEL)
    X, Y = img.X, img.Y
    folha = img.ret(0, 0, img.w, img.h)
    fino = ruido(img.w, img.h, 2, 2, 31)
    manchas = ruido(img.w, img.h, 40, 30, 32)
    borda = perto_da_borda(folha, 6)
    img.pintar(folha, PAPEL_CLARO, 0.82 + 0.08 * manchas + 0.03 * fino - 0.3 * (1 - borda))
    for y in pautas():
        img.cor(img.ret(0, y, img.w, y + 1) & ~img.ret(0, 0, 10, img.h), AZUL_PAUTA)
    img.cor(img.ret(10, 0, 11, img.h), VERMELHO_MARGEM)
    # Furos do fichário: três círculos vazados na esquerda.
    for cy in (30, 78, 126):
        img.apagar(img.elipse(5, cy, 2.5, 2.5))
    # Fita adesiva no alto, meio transparente (tom mais claro e amarelado).
    meio = LARGURA_PAPEL // 2
    fita = img.poligono([(meio - 17, 0), (meio + 17, 0), (meio + 16, 7), (meio - 16, 8)])
    img.pintar(fita, bib.hexa("#d8d0a8", "#e6dfbd", "#f0ead0"), 0.5 + 0.3 * fino)
    # Adesivo de estrela no canto de cima (cor forte: é de 1990).
    estrela = []
    for i in range(10):
        ang = np.pi / 2 + i * np.pi / 5
        r = 7 if i % 2 == 0 else 3
        estrela.append((LARGURA_PAPEL - 16 + r * np.cos(ang), 12 - r * np.sin(ang)))
    adesivo = img.poligono(estrela)
    img.pintar(adesivo, bib.hexa("#7a2a55", "#b0417a", "#d9669c", "#f19bc0"), 0.55 + 0.3 * (Y < 11))
    img.contornar(PAPEL_CLARO[0])
    return img


def papel_caderno_gabriel():
    """O caderno do Gabriel (2026): folha quadriculada de caderno de
    faculdade, com a espiral em cima. O quadriculado é bem fraco, para não
    brigar com o texto."""
    img = Imagem(LARGURA_PAPEL, ALTURA_PAPEL)
    X, Y = img.X, img.Y
    folha = img.ret(0, 3, img.w, img.h)
    fino = ruido(img.w, img.h, 2, 2, 41)
    manchas = ruido(img.w, img.h, 40, 30, 42)
    borda = perto_da_borda(folha, 6)
    img.pintar(folha, PAPEL_CLARO, 0.85 + 0.06 * manchas + 0.03 * fino - 0.25 * (1 - borda))
    grade = folha & (((X % 6) == 0) | (((Y - 4) % 6) == 0)) & (Y > 5)
    img.cor(grade, CINZA_GRADE)
    # Espiral: furos redondos no alto e os aros de metal passando por eles.
    for x in range(8, img.w - 4, 8):
        img.apagar(img.elipse(x, 5, 1.6, 1.6))
        img.pintar(img.ret(x - 1, 0, x + 1, 5), "metal", 0.55)
    img.contornar(PAPEL_CLARO[0])
    return img


PAPEIS = {
    "papel_pergaminho": papel_pergaminho,
    "papel_caderno_clarice": papel_caderno_clarice,
    "papel_caderno_gabriel": papel_caderno_gabriel,
}


# ---------------------------------------------------------------------------
# Peças da interface
# ---------------------------------------------------------------------------


def espaco(aceso=False):
    """Um espaço da grade do inventário: um nicho escavado no concreto.
    A borda de cima e da esquerda fica escura e a de baixo e da direita
    clara (é o "chanfro para dentro": parece fundo, como uma prateleira).
    Aceso = selecionado: a borda vira a cor do sol, a mesma dos raios que
    entram pelo teto."""
    n = TAMANHO_ESPACO
    img = Imagem(n, n)
    fino = ruido(n, n, 2, 2, 3)
    tudo = img.ret(0, 0, n, n)
    img.pintar(tudo, "concreto", 0.32 + 0.08 * fino)
    dentro = img.ret(2, 2, n - 2, n - 2)
    img.cor(dentro, RAMPAS["concreto"][0])
    # Chanfro: sombra em cima/esquerda, luz embaixo/direita (1 px cada).
    img.pintar(img.ret(1, 1, n - 1, 2) | img.ret(1, 1, 2, n - 1), "concreto", 0.12)
    img.pintar(img.ret(1, n - 2, n - 1, n - 1) | img.ret(n - 2, 1, n - 1, n - 1), "concreto", 0.55)
    if aceso:
        borda = tudo & ~img.ret(1, 1, n - 1, n - 1)
        img.pintar(borda, "sol", 0.72)
        img.pintar(img.ret(1, 1, n - 1, 2) | img.ret(1, 1, 2, n - 1), "sol", 0.35)
    else:
        img.cor(tudo & ~img.ret(1, 1, n - 1, n - 1), CONTORNO)
    return img


def painel():
    """Fundo das janelas (inventário): concreto escuro e manchado, com uma
    moldura de 2 px (contorno quase preto + fio claro por dentro).
    Os cantos são cortados em diagonal, como uma placa gasta."""
    n = TAMANHO_PAINEL
    img = Imagem(n, n)
    fino = ruido(n, n, 2, 2, 5)
    manchas = ruido(n, n, 6, 6, 6)
    tudo = img.poligono([(1, 0), (n - 1, 0), (n, 1), (n, n - 1), (n - 1, n), (1, n), (0, n - 1), (0, 1)])
    img.pintar(tudo, "concreto", 0.14 + 0.08 * manchas + 0.05 * fino)
    borda = tudo & ~img.ret(1, 1, n - 1, n - 1)
    img.cor(borda, CONTORNO)
    fio = img.ret(1, 1, n - 1, n - 1) & ~img.ret(2, 2, n - 2, n - 2)
    img.pintar(fio, "concreto", 0.42 + 0.1 * fino)
    return img


def coracao(cheio):
    """Um coração da vida do Gabriel (HUD): 9 x 8 px. Cheio é vermelho com
    um brilho de 1 px; vazio é só o contorno escuro com o miolo apagado.
    Desenhado como duas elipses (os lóbulos) e um triângulo (a ponta)."""
    img = Imagem(9, 8)
    forma = img.elipse(2.5, 2.5, 2.5, 2.4) | img.elipse(6.5, 2.5, 2.5, 2.4) | \
        img.poligono([(0.2, 3.2), (8.8, 3.2), (4.5, 8.0)])
    vermelho = bib.hexa("#2a0d10", "#5e1519", "#9c2327", "#d23c35", "#f07a62")
    if cheio:
        img.pintar(forma, vermelho, 0.55 + 0.3 * (img.Y < 3))
        img.cor(img.ret(2, 1, 3, 2), vermelho[4])
    else:
        img.pintar(forma, vermelho, 0.08)
    img.contornar(CONTORNO)
    return img


def main():
    print("Gerando ícones e interface")
    for nome, funcao in ICONES.items():
        funcao().salvar(f"{nome}.png", PASTA_ITENS)
    espaco().salvar("espaco.png", PASTA_INTERFACE)
    espaco(aceso=True).salvar("espaco_selecionado.png", PASTA_INTERFACE)
    painel().salvar("painel.png", PASTA_INTERFACE)
    coracao(True).salvar("coracao_cheio.png", PASTA_INTERFACE)
    coracao(False).salvar("coracao_vazio.png", PASTA_INTERFACE)
    for nome, funcao in PAPEIS.items():
        funcao().salvar(f"{nome}.png", PASTA_INTERFACE)


if __name__ == "__main__":
    main()
