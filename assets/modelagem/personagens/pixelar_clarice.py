# pixelar_clarice.py — transforma as artes de referência da Clarice em
# sprites de jogo (pixel art no tamanho do jogo, paleta fechada), do mesmo
# jeito que o pixelar_gabriel.py faz com o Gabriel. As ferramentas (recorte,
# redução, paleta por k-médias, contorno) são as do pixelar_gabriel.py.
#
# Como rodar (só precisa de Python 3 com Pillow e NumPy, sem Blender):
#
#   python assets/modelagem/personagens/pixelar_clarice.py
#
# Entrada (assets/modelagem/personagens/clarice_referencia/):
#   expressoes.png      cinco rostos: neutro, raiva, triste, vergonha e feliz
#   andar_frente.webp   oito poses andando de frente (duas fileiras de quatro)
#   andar_costas.webp   oito poses andando de costas
#   andar_lado.webp     quatro poses andando para a direita (em cima) e
#                       quatro para a esquerda (embaixo)
#   andar_diagonal.webp em cima, de novo as quatro poses de lado (não são
#                       usadas: não são 3/4); embaixo, 3/4 de costas
#                       andando para a esquerda (a primeira é a pose de
#                       perfil da folha de lado e fica de fora)
#
# Saída (assets/sprites/personagens/clarice/), nos mesmos nomes e tamanhos
# que o gerar_clarice.py usava, para as cenas do Godot não mudarem:
#   clarice_<vista>.png           96 x 112, parada, vistas frente, costas, lado
#                                 e tres_quartos_costas
#   clarice_andar_<vista>.png     caminhada, 12 quadros de 96 x 112 lado a lado
#   clarice_parado_<vista>.png    respiração, 8 quadros de 96 x 112
#   clarice_retrato_<nome>.png    80 x 80, para a caixa de diálogo
#   clarice_referencia.png        folha com o que sai daqui, para conferir
#
# O 3/4 de frente ainda não tem referência: continua saindo do
# gerar_clarice.py (Blender), e este script não mexe nele. O 3/4 de costas
# vem virado para a esquerda e é espelhado (no jogo, todos os sprites olham
# para a direita e o Godot espelha para a esquerda).
#
# De lado o jogo só usa a Clarice andando para a direita: para a esquerda,
# o Godot espelha o sprite (flip_h). Então só entram as quatro poses de
# cima da folha de lado; as de baixo (para a esquerda) são outro desenho, e
# misturá-las mudaria o cabelo e o walkman de um quadro para o outro.
#
# Consistência entre as poses: a jaqueta tem a mesma largura nas poses de
# frente e de costas, mas a cabeça, o tronco e as pernas não saíram do
# mesmo tamanho (na fileira de baixo a cabeça é ~4% maior, o tronco ~5%
# menor e as pernas ~8% maiores). Então:
#   1. cada pose é cortada em três trechos (do alto do cabelo à faixa roxa
#      do peito, da faixa à barra da jaqueta, da barra ao pé), e cada trecho
#      é esticado para a média das poses (frente e costas juntas; de lado,
#      as quatro poses de lado); depois todas são reduzidas pela mesma
#      escala;
#   2. todas as vistas usam a mesma paleta de 40 cores;
#   3. as poses são alinhadas pela cabeça (de frente e de costas pelo meio
#      dela, de lado pela ponta do rosto) e o pé vai para a linha do chão;
#   4. a cabeça da pose parada é colada em todos os quadros da mesma vista
#      (o coque e o rabo de cavalo mudavam de forma de uma pose para outra).
#
# Caminhada de frente e de costas: só a fileira de baixo de cada folha é
# um ciclo de verdade (pé esquerdo à frente, passagem, pé direito à frente,
# passagem). Na fileira de cima o pé direito fica à frente nas quatro poses
# e as pernas quase não mexem; ela só serve para a pose parada.
#
# Caminhada de lado: nas poses desenhadas os dois passos são o mesmo desenho
# (a mesma perna à frente, os braços no mesmo lugar), e a caminhada parecia
# pular com uma perna só. Então ela é um boneco recortado, como a do Gabriel
# (seção 4): as peças saem da pose de passo aberto e giram nas juntas.
#
# 3/4 de costas: só há três poses desenhadas. Entre uma pose de passo aberto
# e a pose de passagem (pernas juntas) entram dois quadros gerados, com as
# pernas fechando aos poucos (função pernas_fechando).

import os
import sys

import numpy as np
from PIL import Image, ImageDraw

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA_SCRIPT)
import pixelar_gabriel as base  # noqa: E402

PASTA_REF = os.path.join(PASTA_SCRIPT, "clarice_referencia")
PASTA_SAIDA = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "sprites",
                                            "personagens", "clarice"))

QUADRO = base.QUADRO
LINHA_PE = base.LINHA_PE
CENTRO_X = base.CENTRO_X
QUADROS_ANDAR = base.QUADROS_ANDAR
QUADROS_PARADO = base.QUADROS_PARADO
TAM_RETRATO = base.TAM_RETRATO
MAX_CORES = 40
MAX_CORES_RETRATO = 48

# Altura da Clarice no sprite, do alto do coque ao pé: 1,62 m do couro
# cabeludo ao pé (90 px na escala do Gabriel, que tem 1,75 m e 97 px sem o
# volume do cabelo) e o coque por cima.
ALTURA_PX = 95

# Cada folha de caminhada é uma grade de 2 fileiras x 4 colunas.
FOLHA_LINHAS = ((0, 383), (383, 765))
FOLHA_COLUNAS = ((0, 256), (256, 512), (512, 768), (768, 1024))

# Arquivo de cada vista, as células (fileira, coluna) que entram, na ordem
# do ciclo, e se a pose é espelhada. De lado, só a fileira de cima (a que
# anda para a direita): as de baixo são outro desenho, e misturá-las mudaria
# o cabelo e o walkman de um quadro para o outro.
TODAS = [(f, c) for f in range(2) for c in range(4)]
FOLHAS = {
    "frente": ("andar_frente.webp", TODAS, False),
    "costas": ("andar_costas.webp", TODAS, False),
    "lado": ("andar_lado.webp", [(0, 0), (0, 1), (0, 2), (0, 3)], False),
    "tres_quartos_costas": ("andar_diagonal.webp", [(1, 1), (1, 2), (1, 3)], True),
}
# Vistas alinhadas pela ponta do rosto (as outras, pelo meio da cabeça).
DE_LADO = ("lado", "tres_quartos_costas")
# Vistas que dividem o mesmo tamanho de cabeça, tronco e pernas.
GRUPOS = (("frente", "costas"), ("lado",), ("tres_quartos_costas",))

# O ciclo de 12 quadros de cada vista. Um número é a pose desenhada (na
# ordem de FOLHAS); um par (pose, k) é um quadro gerado a partir da pose de
# passo aberto, com as pernas fechadas até a fração k da abertura.
# De frente e de costas: as quatro poses da fileira de baixo (4 a 7), três
# quadros cada, como a frente e as costas do Gabriel.
# No 3/4 de costas: passo (0), o outro passo (1) e uma só passagem (2), que
# vale para os dois lados.
# De lado o ciclo sai do boneco (BONECO_LADO), não daqui.
ABRE, FECHA = 0.65, 0.3
CICLO = {
    "frente": [4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7],
    "costas": [4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7],
    "tres_quartos_costas": [0, (0, ABRE), (0, FECHA), 2, (1, FECHA), (1, ABRE),
                            1, (1, ABRE), (1, FECHA), 2, (0, FECHA), (0, ABRE)],
}

# Pose usada como "parada" (a de pernas mais juntas, escolhida olhando a
# folha) em cada folha. De lado a parada é o boneco com os membros retos.
POSE_PARADA = {"frente": 2, "costas": 3, "lado": 0, "tres_quartos_costas": 2}

# O boneco de lado sai da pose de passo aberto (DIR 1, a pose 0 da folha de
# lado), em coordenadas do quadro de 96 x 112:
#   braco_perto  o braço do lado da câmera, que nessa pose vai para trás e
#                é desenhado por cima do tronco (da jaqueta até a mão)
#   braco_longe  o antebraço do outro lado, que aparece na frente do corpo
#   ombro        onde o braço gira
#   costas_x     do braço de perto, só o que fica à direita desta coluna (e
#                acima da barra da jaqueta) estava cobrindo o tronco; esse
#                buraco é preenchido com as cores de volta
# A perna é a da frente dessa pose (inteira e reta). O outro braço e a outra
# perna são cópias mais escuras das mesmas peças, desenhadas atrás do corpo.
BONECO_LADO = {
    "pose": 0,
    "braco_perto": [(40, 45), (46, 45), (46, 52), (45, 61), (40, 63), (39, 69), (38, 76),
                    (28, 76), (29, 66), (32, 58), (34, 51)],
    "braco_longe": [(57, 56), (61, 56), (67, 62), (72, 66), (71, 75), (61, 75), (57, 64)],
    "ombro": (43.0, 48.0),
    "costas_x": 42,
}
# Amplitudes da caminhada de lado, em graus, como no pixelar_gabriel.py
# (COXA, JOELHO, BRACO): a coxa da pose desenhada está a ~20° da vertical.
COXA, JOELHO, BRACO = 22.0, 30.0, 20.0

RETRATOS = {
    "normal": 0,
    "seria": 1,
    "triste": 2,
    "envergonhada": 3,
    "sorrindo": 4,
}


# ---------------------------------------------------------------------------
# 1. Recorte
# ---------------------------------------------------------------------------

def abrir_rgb(nome, caixa):
    img = Image.open(os.path.join(PASTA_REF, nome)).convert("RGB").crop(caixa)
    return np.asarray(img).astype(np.float32)


def roxo(rgb, mascara):
    # A faixa roxa da jaqueta (e as munhequeiras, também roxas).
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    return mascara & (b > 140) & (r > 90) & (g < 90) & (b > r + 25)


def so_a_figura(mascara, semente):
    # As folhas têm texto ("FRAME 1", "NEUTRO"...) no canto. O texto não
    # encosta na figura, então ficam só os pixels ligados à semente (um
    # ponto que com certeza é da figura), por inundação.
    img = Image.fromarray(mascara.astype(np.uint8) * 255).copy()
    ImageDraw.floodfill(img, (int(semente[0]), int(semente[1])), 128, thresh=0)
    return np.asarray(img) == 128


def faixa_do_peito(rgb, mascara):
    # A primeira linha (de cima para baixo) com bastante roxo é o topo da
    # faixa do peito; o centro dela, na horizontal, é o centro do corpo.
    linhas = np.where(roxo(rgb, mascara).sum(axis=1) >= 12)[0]
    topo = int(linhas.min())
    xs = np.where(roxo(rgb, mascara)[topo:topo + 6].any(axis=0))[0]
    return topo, (xs.min() + xs.max() + 1) / 2


def recortar_pose(nome, caixa, espelhar=False):
    rgb = abrir_rgb(nome, caixa)
    if espelhar:
        rgb = rgb[:, ::-1].copy()
    m = base.mascara_figura(rgb)
    topo, centro = faixa_do_peito(rgb, m)
    m = so_a_figura(m, (centro, topo + 2))
    return base.aparar(rgb, m)


# ---------------------------------------------------------------------------
# 2. Caminhadas
# ---------------------------------------------------------------------------

def jeans(rgb, m):
    # O azul-marinho da calça: mais azul que verde, verde e vermelho quase
    # iguais (o verde-azulado escuro da jaqueta tem bem mais verde) e escuro.
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    return m & (b > g + 8) & (np.abs(g - r) < 20) & (lum > 38) & (lum < 100)


def bainha(rgb, m, centro, peito, de_lado):
    # Onde a jaqueta acaba e começam as pernas.
    # De frente e de costas: a última linha com roxo no meio do corpo (a
    # barra da jaqueta). Só o meio: as munhequeiras, também roxas, ficam dos
    # lados.
    # De lado e no 3/4 a barra roxa quase não aparece no meio do corpo, e
    # essa conta pegava a faixa do peito ou uma munhequeira. Ali vale a linha
    # de cima da calça: a primeira, bem abaixo do peito, com bastante jeans.
    if de_lado:
        cont = jeans(rgb, m).sum(axis=1)
        return next(y for y in range(peito + 40, m.shape[0]) if cont[y] >= 15) - 1
    c = int(centro)
    linhas = np.where(roxo(rgb, m)[:, c - 15:c + 15].sum(axis=1) >= 10)[0]
    return int(linhas.max())


def marcos(rgb, m, de_lado):
    # Onde começa cada trecho do corpo, de cima para baixo: alto do cabelo,
    # faixa do peito, barra da jaqueta e sola do pé.
    peito, centro = faixa_do_peito(rgb, m)
    return [0, peito, bainha(rgb, m, centro, peito, de_lado), m.shape[0] - 1], centro


def esticar_trechos(rgb, m, de, para):
    # Estica ou encolhe cada trecho na vertical (cabeça, tronco, pernas)
    # para o tamanho de "para", escolhendo para cada linha nova a linha
    # original correspondente (conta linear dentro de cada trecho).
    ys = np.arange(int(round(para[-1])) + 1)
    origem = np.clip(np.round(np.interp(ys, para, de)).astype(int), 0, m.shape[0] - 1)
    return rgb[origem], m[origem]


def coluna_da_cabeca(mm, peito, de_lado):
    # A coluna que alinha as poses: a cabeça quase não sai do lugar quando
    # ela anda (os braços e as pernas, sim). Vale a faixa do rosto, entre
    # 45% e 80% da altura do cabelo ao peito (acima fica o coque, abaixo o
    # pescoço e a gola). De frente e de costas é o meio dessa faixa; de lado,
    # a ponta do rosto (o rabo de cavalo balança atrás).
    faixa = mm[int(0.45 * peito):int(0.8 * peito)]
    xs = np.where(faixa.any(axis=0))[0]
    return xs.max() + 1 if de_lado else (xs.min() + xs.max() + 1) / 2


def reduzir_pose(rgb, m, padrao, escala, de_lado):
    # Cada trecho do corpo vai para o tamanho padrão (a média das poses) e
    # a pose inteira é reduzida pela mesma escala, igual para todas.
    de, _ = marcos(rgb, m, de_lado)
    rgb, m = esticar_trechos(rgb, m, de, padrao)
    largura = max(1, round(m.shape[1] * escala))
    altura = max(1, round(m.shape[0] * escala))
    cor, mm = base.reduzir(rgb, m, largura, altura)
    xs = np.where(mm.any(axis=0))[0]
    meio = (xs.min() + xs.max() + 1) / 2
    return cor, mm, coluna_da_cabeca(mm, padrao[1] * escala, de_lado), meio


def alinhar(poses):
    # A cabeça de todas as poses vai para a mesma coluna. Qual coluna: a que
    # deixa o corpo, em média, centrado em CENTRO_X (de lado, a ponta do
    # rosto fica à frente do meio do corpo).
    desvio = np.mean([cabeca - meio for _, _, cabeca, meio in poses])
    return [(cor, mm, cabeca - desvio) for cor, mm, cabeca, _ in poses]


def no_quadro(spr, centro):
    # Põe o "centro" da pose na coluna CENTRO_X e o pé mais baixo no chão.
    quadro = base.vazio()
    ys, xs = np.where(spr >= 0)
    x0 = int(round(CENTRO_X + 0.5 - centro))
    y0 = LINHA_PE - ys.max()
    ok = (ys + y0 >= 0) & (ys + y0 < QUADRO[1]) & (xs + x0 >= 0) & (xs + x0 < QUADRO[0])
    quadro[ys[ok] + y0, xs[ok] + x0] = spr[ys[ok], xs[ok]]
    return quadro


def recortar_folha(nome, celulas, espelhar):
    caixas = [(FOLHA_COLUNAS[c][0], FOLHA_LINHAS[f][0], FOLHA_COLUNAS[c][1], FOLHA_LINHAS[f][1])
              for f, c in celulas]
    return [recortar_pose(nome, caixa, espelhar) for caixa in caixas]


def reduzir_folhas():
    # O tamanho padrão de cada trecho é a média das poses do grupo (frente
    # e costas juntas): assim as duas caminhadas têm a mesma cabeça, o mesmo
    # tronco e as mesmas pernas. A escala é a mesma para todas as vistas (as
    # folhas foram desenhadas no mesmo tamanho) e sai do primeiro grupo.
    folhas = {vista: recortar_folha(*FOLHAS[vista]) for vista in FOLHAS}
    escala = None
    reduzidas = {}
    for grupo in GRUPOS:
        padrao = np.mean([marcos(rgb, m, vista in DE_LADO)[0]
                          for vista in grupo for rgb, m in folhas[vista]], axis=0)
        if escala is None:
            escala = (ALTURA_PX - 1) / padrao[-1]
        for vista in grupo:
            reduzidas[vista] = alinhar([reduzir_pose(rgb, m, padrao, escala, vista in DE_LADO)
                                        for rgb, m in folhas[vista]])
    return reduzidas


# ---------------------------------------------------------------------------
# 3. Quadros intermediários
# ---------------------------------------------------------------------------
# Do passo aberto à passagem, cada perna gira no quadril até ficar quase em
# pé. Na pose de passo aberto as duas pernas estão separadas abaixo da
# virilha (um "V" de cabeça para baixo): ali cada uma é uma peça (os pixels
# ligados entre si). Entre o quadril (logo abaixo das mãos) e a virilha as
# duas ainda são um bloco só, que é dividido por uma reta do meio do quadril
# até o ponto onde as pernas se separam. Cada perna inteira gira em volta do
# quadril, com o mesmo giro de pixel art do Gabriel (base.girar,
# RotSprite), até o ângulo dela ficar k vezes o que era:
#   ângulo da perna = ângulo do quadril até o tornozelo, medido da vertical
#   giro            = (k - 1) * ângulo da perna
# O tênis não gira (ficaria inclinado): ele anda junto com o tornozelo. A
# perna de trás é desenhada primeiro, a da frente por cima, com uma linha de
# contorno onde as duas se encostam. Por baixo de tudo vai a metade de cima
# do bloco do quadril, na posição original: girada, a perna se descola um
# pixel do quadril em alguns pontos, e esse remendo tapa o buraco sem
# aparecer no resto. Com as pernas mais em pé, o pé desce:
# o quadro inteiro sobe até o pé voltar à linha do chão, e é esse o sobe e
# desce da caminhada (o corpo fica mais alto na passagem).
# O tronco, os braços e a cabeça continuam os da pose desenhada.

ALTURA_TENIS = 7


def eh_de_cima(paleta):
    # Cores que não são da calça nem do contorno: pele, jaqueta (verde-
    # azulado, roxo) e o branco do punho. Servem para achar onde acabam as
    # mãos: dali para baixo só há pernas.
    r, g, b = (paleta[:, i].astype(int) for i in range(3))
    lum = base.luminancia(paleta)
    return (r > b + 15) | (g > r + 40) | ((b > g + 40) & (r > g + 15)) | (lum > 150)


def trechos(linha):
    # Os pedaços contínuos de pixels de uma linha: [(início, fim), ...].
    cheio = np.concatenate([[False], linha >= 0, [False]])
    bordas = np.flatnonzero(cheio[1:] != cheio[:-1])
    return list(zip(bordas[::2], bordas[1::2]))


def virilha(spr, de_cima):
    # A primeira linha, abaixo das mãos, de onde para baixo as pernas são
    # dois pedaços separados até o tênis.
    cima = (spr >= 0) & de_cima[np.maximum(spr, 0)]
    topo = max(y for y in range(55, LINHA_PE - 10) if cima[y].any()) + 1
    for y in range(LINHA_PE - ALTURA_TENIS, topo - 1, -1):
        if len(trechos(spr[y])) < 2:
            return y + 1, topo
    return topo, topo


def pecas(mascara):
    # Grupos de pixels ligados entre si (em cima, embaixo e dos lados), do
    # maior para o menor, achados por inundação a partir de cada pixel.
    restante = mascara.copy()
    grupos = []
    while restante.any():
        y, x = np.argwhere(restante)[0]
        img = Image.fromarray(restante.astype(np.uint8) * 255).copy()
        ImageDraw.floodfill(img, (int(x), int(y)), 128, thresh=0)
        grupo = np.asarray(img) == 128
        grupos.append(grupo)
        restante &= ~grupo
    return sorted(grupos, key=lambda g: -g.sum())


def dividir_pernas(spr, linha, topo):
    # As duas pernas inteiras, do quadril ao tênis: abaixo da virilha, as
    # duas peças; entre o quadril e a virilha, cada lado da reta que vai do
    # meio do quadril até o vão entre as pernas.
    ys, xs = np.mgrid[0:QUADRO[1], 0:QUADRO[0]]
    abaixo = pecas((spr >= 0) & (ys >= linha))[:2]
    if len(abaixo) < 2:
        return None
    cols = np.where(spr[topo] >= 0)[0]
    quadril = ((cols.min() + cols.max() + 1) / 2, float(topo))
    a, b = trechos(spr[linha])[:2]
    vao = (a[1] + b[0]) / 2
    reta = quadril[0] + (vao - quadril[0]) * (ys - topo) / max(1, linha - topo)
    bloco = (spr >= 0) & (ys >= topo) & (ys < linha)
    pernas = []
    for peca in abaixo:
        lado_direito = xs[peca].mean() > vao
        metade = bloco & ((xs >= reta) if lado_direito else (xs < reta))
        pernas.append(peca | metade)
    return pernas, quadril


def pernas_fechando(spr, k, de_cima, paleta, contorno):
    linha, topo = virilha(spr, de_cima)
    divididas = dividir_pernas(spr, linha, topo)
    if divididas is None:
        return spr
    pernas, quadril = divididas
    ys = np.arange(QUADRO[1])[:, None]
    corpo = np.where(pernas[0] | pernas[1], -1, spr)
    remendo = base.so(spr, (pernas[0] | pernas[1]) & (ys < (topo + linha) // 2 + 1))
    novas = []
    for perna in pernas:
        fundo = np.where(perna.any(axis=1))[0].max()
        tenis = perna & (ys > fundo - ALTURA_TENIS)
        canela = perna & ~tenis
        yt = np.where(canela.any(axis=1))[0].max()
        xt = np.where(canela[yt])[0]
        tornozelo = ((xt.min() + xt.max() + 1) / 2, float(yt))
        giro = (k - 1) * base.angulo(quadril, tornozelo)
        girada = base.girar(base.so(spr, canela), giro, quadril)
        novo = base.ponto_girado(tornozelo, giro, quadril, quadril)
        pe = base.mover(base.so(spr, tenis), int(round(novo[0] - tornozelo[0])),
                        int(round(novo[1] - tornozelo[1])))
        novas.append((tornozelo[0], base.compor(girada, pe)))
    novas.sort(key=lambda t: t[0])
    tras, frente = novas[0][1], novas[1][1]
    frente = base.separar_contorno(frente, tras, contorno, paleta)
    return base.assentar(base.compor(remendo, tras, corpo, frente))


# ---------------------------------------------------------------------------
# 4. Boneco de lado
# ---------------------------------------------------------------------------
# Como a caminhada de lado do Gabriel: o braço gira no ombro, a coxa no
# quadril e a canela no joelho, e o tênis vai junto com o tornozelo. Um
# ciclo são dois passos; a fase φ vai de 0 a 360° em 12 quadros:
#   coxa   = COXA · sen φ              a perna balança (positivo = frente);
#                                      a outra perna usa φ + 180°
#   joelho = JOELHO · máx(0, cos φ)^1,5  dobra só enquanto a perna vem para a
#                                      frente no ar
#   braço  = −BRACO · sen φ            ao contrário da perna do mesmo lado
# As peças vêm desenhadas num ângulo (a perna a ~20° para a frente, o braço
# ~20° para trás); cada uma gira a diferença entre o ângulo que precisa ter
# e o ângulo em que foi desenhada. Depois de montar o quadro, o boneco desce
# até o pé mais baixo encostar no chão: é o sobe e desce da caminhada.

class BonecoLado:
    def __init__(self, pose, paleta, contorno):
        cfg = BONECO_LADO
        ys, xs = np.mgrid[0:QUADRO[1], 0:QUADRO[0]]
        cheio = pose >= 0
        perto = base.mascara_poligono(cfg["braco_perto"]) & cheio
        longe = base.mascara_poligono(cfg["braco_longe"]) & cheio
        self.braco = base.so(pose, perto)
        self.ombro = cfg["ombro"]
        sem_bracos = np.where(perto | longe, -1, pose)
        _, bainha = linhas_do_corpo(pose, paleta)
        buraco = perto & (xs >= cfg["costas_x"]) & (ys <= bainha)
        sem_bracos = base.preencher(np.where(buraco, 0, sem_bracos), buraco, paleta)
        de_cima = eh_de_cima(paleta)
        linha, topo = virilha(sem_bracos, de_cima)
        pernas, self.quadril = dividir_pernas(sem_bracos, linha, topo)
        self.corpo = np.where(pernas[0] | pernas[1], -1, sem_bracos)
        frente = max(pernas, key=lambda m: np.where(m)[1].mean())
        self.pecas_perna(base.so(sem_bracos, frente))
        yb, xb = np.where(self.braco >= 0)
        mao = yb >= yb.max() - 6
        self.ang_braco = base.angulo(self.ombro, (xb[mao].mean(), yb[mao].mean()))
        self.paleta = paleta
        self.contorno = contorno
        self.sombra = base.tabela_escura(paleta, 0.72)

    def pecas_perna(self, perna):
        # Coxa, canela e tênis, com o joelho no meio do caminho entre o
        # quadril e o tornozelo.
        ys = np.arange(QUADRO[1])[:, None]
        linhas = np.where((perna >= 0).any(axis=1))[0]
        fundo = linhas.max()
        tenis = (perna >= 0) & (ys > fundo - ALTURA_TENIS)
        yt = fundo - ALTURA_TENIS
        xt = np.where(perna[yt] >= 0)[0]
        self.tornozelo = ((xt.min() + xt.max() + 1) / 2, float(yt))
        yj = int(round((self.quadril[1] + yt) / 2))
        xj = np.where(perna[yj] >= 0)[0]
        self.joelho = ((xj.min() + xj.max() + 1) / 2, float(yj))
        self.coxa = np.where(ys <= yj + 1, perna, -1)
        self.canela = np.where((ys >= yj - 1) & ~tenis, perna, -1)
        self.tenis = np.where(tenis, perna, -1)
        self.ang_perna = base.angulo(self.quadril, self.tornozelo)

    def perna(self, coxa, joelho):
        a1 = coxa - self.ang_perna
        a2 = a1 - joelho
        j = base.ponto_girado(self.joelho, a1, self.quadril, self.quadril)
        t = base.ponto_girado(self.tornozelo, a2, self.joelho, j)
        return base.compor(base.girar(self.coxa, a1, self.quadril),
                           base.girar(self.canela, a2, self.joelho, j),
                           base.mover(self.tenis, int(round(t[0] - self.tornozelo[0])),
                                      int(round(t[1] - self.tornozelo[1]))))

    def braco_em(self, graus):
        return base.girar(self.braco, graus - self.ang_braco, self.ombro)

    def quadro(self, fase, andando=True):
        pernas, bracos = [], []
        for desloc in (0, 180):
            phi = np.radians(fase + desloc)
            if andando:
                pernas.append(self.perna(COXA * np.sin(phi),
                                         JOELHO * max(0.0, np.cos(phi)) ** 1.5))
                bracos.append(self.braco_em(-BRACO * np.sin(phi)))
            else:
                pernas.append(self.perna(0.0, 0.0))
                bracos.append(self.braco_em(0.0))
        perna_perto, perna_longe = pernas
        braco_perto, braco_longe = bracos
        fundo = base.compor(base.escurecer(braco_longe, self.sombra),
                            base.escurecer(perna_longe, self.sombra))
        perna_perto = base.separar_contorno(perna_perto, fundo, self.contorno, self.paleta)
        meio = base.compor(fundo, perna_perto, self.corpo)
        braco_perto = base.separar_contorno(braco_perto, meio, self.contorno, self.paleta)
        q = base.limpar_migalhas(base.compor(meio, braco_perto))
        return base.contorno_final(base.assentar(q), self.paleta, self.contorno)


def montar_ciclo(quadros, ciclo, paleta, contorno):
    de_cima = eh_de_cima(paleta)
    saida = []
    for passo in ciclo:
        if isinstance(passo, tuple):
            pose, k = passo
            q = pernas_fechando(quadros[pose], k, de_cima, paleta, contorno)
            saida.append(base.contorno_final(base.limpar_migalhas(q), paleta, contorno))
        else:
            saida.append(quadros[passo])
    return saida


# ---------------------------------------------------------------------------
# 5. Respiração
# ---------------------------------------------------------------------------
# A mesma conta do Gabriel (pixelar_gabriel.py, quadro_parado): o peito sobe
# até 2 pixels e a cabeça vai junto, 60° atrasada; as pernas não mexem. As
# linhas do corpo saem da própria figura: o queixo fica 7 px acima da faixa
# do peito, e a bainha da jaqueta é a última linha com roxo no meio do corpo.

SUBIDA = 2.0


def linhas_do_corpo(spr, paleta):
    cor = paleta[np.maximum(spr, 0)].astype(np.float32)
    eh_roxo = roxo(cor, spr >= 0)
    meio = eh_roxo[:, CENTRO_X - 6:CENTRO_X + 7].sum(axis=1)
    linhas = np.where(meio >= 6)[0]
    return int(linhas.min()) - 7, int(linhas.max())


def mesma_cabeca(quadro, molde, queixo):
    # A cabeça muda um pouco de uma pose desenhada para outra (o coque de
    # frente muda de forma, o rabo de cavalo de costas pula de lugar). Como
    # todas as poses já estão alinhadas pela faixa do peito e com os trechos
    # do corpo do mesmo tamanho, a cabeça da pose parada (tudo até a linha
    # do queixo) é colada em todos os quadros, sempre no mesmo lugar.
    out = quadro.copy()
    out[:queixo + 1] = molde[:queixo + 1]
    return out


def quadro_parado(spr, fase, queixo, bainha):
    phi = np.radians(fase)
    peito = round(SUBIDA * (1 - np.cos(phi)) / 2)
    cabeca = round(SUBIDA * (1 - np.cos(phi - np.radians(60))) / 2) if fase else 0
    meio_peito = (queixo + bainha) // 2
    return base.remapear_linhas(spr, [
        (0, -cabeca), (queixo - 2, queixo - 2 - cabeca),
        (queixo + 2, queixo + 2 - peito), (meio_peito, meio_peito - peito),
        (bainha - 4, bainha - 4), (QUADRO[1] - 1, QUADRO[1] - 1)])


# ---------------------------------------------------------------------------
# 6. Retratos da caixa de diálogo
# ---------------------------------------------------------------------------
# A folha de expressões tem cinco rostos lado a lado, cada um numa faixa de
# 1/5 da largura, com o nome escrito no canto. Cada rosto é recortado,
# reduzido até 80 px de altura e centrado num quadro de 80 x 80. Os cinco
# usam a mesma paleta, para a pele e a jaqueta não mudarem de cor entre uma
# fala e outra.

def retratos():
    img = Image.open(os.path.join(PASTA_REF, "expressoes.png")).convert("RGB")
    largura_faixa = img.width / 5
    figuras = {}
    for nome, i in RETRATOS.items():
        caixa = (round(i * largura_faixa), 0, round((i + 1) * largura_faixa), img.height)
        rgb = abrir_rgb("expressoes.png", caixa)
        m = base.mascara_figura(rgb)
        m = so_a_figura(m, (rgb.shape[1] / 2, rgb.shape[0] - 3))
        rgb, m = base.aparar(rgb, m)
        largura = max(1, round(m.shape[1] * TAM_RETRATO / m.shape[0]))
        figuras[nome] = base.reduzir(rgb, m, min(largura, TAM_RETRATO), TAM_RETRATO)
    paleta = base.paleta_de(list(figuras.values()), MAX_CORES_RETRATO)
    saida = {}
    for nome, (cor, m) in figuras.items():
        spr = base.contornar(base.indexar(cor, m, paleta), paleta)
        quadro = np.full((TAM_RETRATO, TAM_RETRATO), -1, np.int32)
        x0 = (TAM_RETRATO - spr.shape[1]) // 2
        quadro[:, x0:x0 + spr.shape[1]] = spr
        saida[nome] = base.para_rgba(quadro, paleta)
    return saida


# ---------------------------------------------------------------------------
# 7. Tudo junto
# ---------------------------------------------------------------------------

def salvar(rgba, nome):
    Image.fromarray(rgba, "RGBA").save(os.path.join(PASTA_SAIDA, nome))


def folha_referencia(vistas, andar, retratos_rgba, paleta):
    # Para conferir: as vistas paradas, as caminhadas e os retratos.
    margem = 8
    largura = margem + QUADROS_ANDAR * QUADRO[0] + margem
    linha_retratos = margem + (len(andar) + 1) * (QUADRO[1] + margem)
    altura = linha_retratos + TAM_RETRATO + margem
    folha = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    for i, spr in enumerate(vistas.values()):
        folha.alpha_composite(Image.fromarray(base.para_rgba(spr, paleta)),
                              (margem + i * (QUADRO[0] + margem), margem))
    for j, quadros in enumerate(andar.values()):
        for i, spr in enumerate(quadros):
            folha.alpha_composite(Image.fromarray(base.para_rgba(spr, paleta)),
                                  (margem + i * QUADRO[0], margem + (j + 1) * (QUADRO[1] + margem)))
    for i, rgba in enumerate(retratos_rgba.values()):
        folha.alpha_composite(Image.fromarray(rgba),
                              (margem + i * (TAM_RETRATO + margem), linha_retratos))
    return folha


def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    folhas = reduzir_folhas()
    paleta = base.paleta_de([(cor, m) for poses in folhas.values() for cor, m, _ in poses],
                            MAX_CORES)
    contorno = base.tabela_escura(paleta, 0.42)

    vistas, andar = {}, {}
    for vista, poses in folhas.items():
        quadros = [base.contorno_final(no_quadro(base.contornar(base.indexar(cor, m, paleta),
                                                                paleta), centro),
                                       paleta, contorno)
                   for cor, m, centro in poses]
        parada = quadros[POSE_PARADA[vista]]
        queixo, _ = linhas_do_corpo(parada, paleta)
        quadros = [base.contorno_final(mesma_cabeca(q, parada, queixo), paleta, contorno)
                   for q in quadros]
        if vista == "lado":
            boneco = BonecoLado(quadros[BONECO_LADO["pose"]], paleta, contorno)
            vistas[vista] = boneco.quadro(0, andando=False)
            andar[vista] = [boneco.quadro(360 * q / QUADROS_ANDAR) for q in range(QUADROS_ANDAR)]
        else:
            vistas[vista] = parada
            andar[vista] = montar_ciclo(quadros, CICLO[vista], paleta, contorno)

    fases_parado = [360 * q / QUADROS_PARADO for q in range(QUADROS_PARADO)]
    for vista, spr in vistas.items():
        salvar(base.para_rgba(spr, paleta), f"clarice_{vista}.png")
        salvar(np.concatenate([base.para_rgba(q, paleta) for q in andar[vista]], axis=1),
               f"clarice_andar_{vista}.png")
        queixo, bainha = linhas_do_corpo(spr, paleta)
        parado = [base.contorno_final(quadro_parado(spr, f, queixo, bainha), paleta, contorno)
                  for f in fases_parado]
        salvar(np.concatenate([base.para_rgba(q, paleta) for q in parado], axis=1),
               f"clarice_parado_{vista}.png")
        print(f"{vista}: parada, {QUADROS_ANDAR} quadros andando, {QUADROS_PARADO} respirando")

    rets = retratos()
    for nome, rgba in rets.items():
        salvar(rgba, f"clarice_retrato_{nome}.png")
        print(f"retrato {nome}")
    folha_referencia(vistas, andar, rets, paleta).save(
        os.path.join(PASTA_SAIDA, "clarice_referencia.png"))
    print(f"paleta dos sprites: {len(np.unique(paleta, axis=0))} cores")


if __name__ == "__main__":
    main()
