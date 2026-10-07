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


# ---------------------------------------------------------------------------
# Ícones dos itens
# ---------------------------------------------------------------------------


def lanterna():
    """A lanterna do Gabriel: uma lanterna de mão comum, de plástico preto,
    deitada na diagonal. Cabo com o botão de borracha, cabeça mais larga e
    a lente com a lâmpada (miolo claro, borda âmbar). Não tem luz acesa no
    ícone: se ela está ligada, o espaço de gadget mostra."""
    img = Imagem(TAMANHO_ICONE, TAMANHO_ICONE)
    X, Y = img.X, img.Y
    fino = ruido(img.w, img.h, 2, 2, 7)
    # Cabo: um bastão grosso da esquerda-baixo até o meio.
    cabo = img.linha(3, 13, 9, 7, 2.1)
    img.pintar(cabo, "metal", 0.16 + 0.16 * (X + Y < 16) + 0.05 * fino)
    img.pintar(img.linha(5, 10, 6, 9, 0.8), "ferrugem", 0.45)            # botão
    # Cabeça: mais larga, em volta da lente.
    cabeca = img.elipse(11, 5, 3.6, 3.6) | img.linha(8, 8, 11, 5, 2.6)
    img.pintar(cabeca, "metal", 0.22 + 0.2 * (Y < 4) + 0.05 * fino)
    lente = img.elipse(11.8, 4.2, 2.3, 2.3)
    img.pintar(lente, "sol", 0.35)
    img.pintar(img.elipse(12.2, 3.8, 1.1, 1.1), "sol", 0.9)
    img.contornar(CONTORNO)
    return img


def lanterna_chao():
    """A mesma lanterna caída no chão, na escala do cenário (~20 cm = 6 px)."""
    img = Imagem(10, 5)
    img.pintar(img.ret(0, 1, 6, 4), "metal", 0.25)
    img.pintar(img.ret(6, 0, 9, 5), "metal", 0.35)
    img.pintar(img.ret(8, 1, 9, 4), "sol", 0.7)
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
    """O rádio portátil que o Rafael usava na ronda (um HT de 2008): corpo
    de plástico preto, antena de borracha à esquerda, tela pequena de LCD
    esverdeado e a grade do alto-falante embaixo. O botão de falar (PTT)
    fica na lateral, em ferrugem."""
    img = Imagem(TAMANHO_ICONE, TAMANHO_ICONE)
    X, Y = img.X, img.Y
    fino = ruido(img.w, img.h, 2, 2, 11)
    # Antena: um bastão grosso de 2 px, mais claro na ponta.
    img.pintar(img.ret(4, 0, 6, 5), "metal", 0.18 + 0.2 * (Y == 0))
    # Corpo: retângulo de cantos cortados, mais claro na esquerda.
    corpo = img.poligono([(4, 5), (5, 4), (12, 4), (13, 5), (13, 15), (12, 16), (5, 16), (4, 15)])
    img.pintar(corpo, "metal", 0.12 + 0.18 * (1 - (X - 4) / 9) + 0.05 * fino)
    # Botão de falar na lateral esquerda.
    img.pintar(img.ret(3, 7, 4, 10), "ferrugem", 0.5)
    # Tela de LCD: verde apagado, com uma linha mais clara (os números).
    tela = img.ret(6, 6, 12, 9)
    img.pintar(tela, "verde", 0.55)
    img.pintar(img.ret(7, 7, 11, 8), "verde", 0.8)
    # Grade do alto-falante: pontos alternados, como furos.
    furos = img.ret(6, 11, 12, 15) & ((X + Y) % 2 == 0)
    img.pintar(furos, "metal", 0.02)
    # Brilho de 1 px na quina de cima do corpo.
    img.pintar(img.ret(5, 5, 7, 6), "metal", 0.7)
    img.contornar(CONTORNO)
    return img


def radio_chao():
    """O mesmo rádio caído no chão, na escala do cenário: um HT tem uns
    20 cm, então ~6 px de corpo mais a antena."""
    img = Imagem(7, 11)
    img.pintar(img.ret(1, 0, 2, 4), "metal", 0.3)
    corpo = img.ret(1, 3, 6, 10)
    img.pintar(corpo, "metal", 0.22)
    img.pintar(img.ret(2, 4, 5, 6), "verde", 0.6)
    img.pintar(img.ret(2, 7, 5, 9) & ((img.X + img.Y) % 2 == 0), "metal", 0.02)
    img.contornar(CONTORNO)
    return img


def clarao():
    """Cápsula de clarão: um cilindro curto de metal com a lente de vidro
    na ponta (a "cara" do flash) e o anel de ferrugem do gatilho."""
    img = Imagem(TAMANHO_ICONE, TAMANHO_ICONE)
    X = img.X
    img.pintar(img.ret(4, 5, 13, 11), "metal", 0.25 + 0.3 * (1 - (X - 4) / 9))
    img.pintar(img.ret(7, 5, 8, 11), "ferrugem", 0.6)
    img.pintar(img.elipse(12.5, 8, 2.5, 3.5), "ceu", 0.85)
    img.pintar(img.ret(5, 6, 7, 7), "metal", 0.8)
    img.contornar(CONTORNO)
    return img


def clarao_chao():
    """A cápsula no chão: 5 px de corpo e a lente clara na ponta."""
    img = Imagem(7, 4)
    img.pintar(img.ret(0, 0, 5, 3), "metal", 0.35)
    img.pintar(img.ret(5, 0, 7, 3), "ceu", 0.85)
    img.contornar(CONTORNO)
    return img


def pedra():
    """Um pedaço de concreto quebrado, do tamanho da mão: polígono
    irregular, mais claro em cima (a luz vem de cima)."""
    img = Imagem(TAMANHO_ICONE, TAMANHO_ICONE)
    Y = img.Y
    corpo = img.poligono([(4, 8), (7, 4), (11, 5), (13, 9), (11, 13), (5, 12)])
    img.pintar(corpo, "concreto", 0.75 - 0.4 * (Y - 4) / 9 + 0.1 * ruido(img.w, img.h, 2, 2, 7))
    img.contornar(CONTORNO)
    return img


def pedra_chao():
    """Três pedrinhas juntas no chão (cada monte vale uma pedra no inventário)."""
    img = Imagem(9, 4)
    for x0 in (0, 3, 6):
        img.pintar(img.ret(x0, 1, x0 + 3, 4), "concreto", 0.7)
    img.contornar(CONTORNO)
    return img


def notebook():
    """Notebook aberto de lado: a tampa com a tela azulada acesa e a base
    com o teclado (pontos escuros alternados)."""
    img = Imagem(TAMANHO_ICONE, TAMANHO_ICONE)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 2, 14, 10), "metal", 0.2)
    img.pintar(img.ret(3, 3, 13, 9), "ceu", 0.35 + 0.3 * (Y - 3) / 6)
    img.pintar(img.ret(4, 4, 9, 5), "verde", 0.9)
    img.pintar(img.ret(1, 11, 15, 14), "metal", 0.35)
    img.pintar(img.ret(2, 12, 14, 13) & ((X + Y) % 2 == 0), "metal", 0.05)
    img.contornar(CONTORNO)
    return img


def notebook_chao():
    """O notebook fechado no chão: uma placa fina com o LED aceso."""
    img = Imagem(9, 3)
    img.pintar(img.ret(0, 0, 9, 3), "metal", 0.3)
    img.pintar(img.ret(7, 1, 8, 2), "verde", 0.95)
    img.contornar(CONTORNO)
    return img


# Nome do arquivo -> função que desenha. Um item novo entra aqui.
ICONES = {
    "lanterna": lanterna,
    "lanterna_chao": lanterna_chao,
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
    """O bilhete da Clarice (1994): folha de fichário, com os furos do lado,
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
    # Adesivo de estrela no canto de cima (cor forte: é de 1994).
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
