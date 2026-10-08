# pixelar_gabriel.py — transforma as artes de referência do Gabriel em
# sprites de jogo de verdade (pixel art no tamanho do jogo, paleta fechada)
# e monta, a partir delas, as vistas e as animações que faltam.
#
# Como rodar (só precisa de Python 3 com Pillow e NumPy, sem Blender):
#
#   python assets/modelagem/personagens/pixelar_gabriel.py
#
# Entrada (assets/modelagem/personagens/gabriel_referencia/):
#   frente.png       o Gabriel de frente, em alta resolução
#   vistas.webp      de lado (para a direita), de frente e de lado (para a esquerda)
#   expressoes.webp  cinco rostos: normal, bravo, preocupado, surpreso e envergonhado
#   andar_diagonal.webp  um passo de 3/4 de frente e um de 3/4 de costas (duas vezes cada)
#   andar_frente.webp    quatro poses andando de frente
#   andar_costas.webp    quatro poses andando de costas
#
# Saída (assets/sprites/personagens/gabriel/), nos mesmos nomes e tamanhos
# que o gerar_gabriel.py usava, para a cena do Godot não mudar:
#   gabriel_<vista>.png           96 x 112, vistas lado, frente, tres_quartos,
#                                 costas e tres_quartos_costas
#   gabriel_andar_<vista>.png     caminhada, 12 quadros de 96 x 112 lado a lado
#   gabriel_parado_<vista>.png    respiração, 8 quadros de 96 x 112
#   gabriel_retrato_<nome>.png    80 x 80, para a caixa de diálogo
#   gabriel_referencia.png        folha com tudo, para conferir
#
# Por que um script e não só "salvar a imagem menor": as referências são
# desenhos em "pixel art falsa" (cada pixel do desenho ocupa ~4 a 5 pixels
# da imagem, sem grade exata, com cores misturadas nas bordas). Para virar
# sprite precisa: (1) recortar do fundo, (2) reduzir para a altura do
# jogo, (3) fechar a paleta (poucas cores, iguais em todos os sprites, como
# em pixel art feita à mão) e (4) refazer o contorno de 1 pixel. As costas
# (que não existem na referência) e as animações saem das vistas que
# existem, pelos métodos explicados em cada função.

import os

import numpy as np
from PIL import Image, ImageDraw

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_REF = os.path.join(PASTA_SCRIPT, "gabriel_referencia")
PASTA_SAIDA = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "sprites",
                                            "personagens", "gabriel"))

# Quadro de cada sprite: o mesmo de todos os personagens em pé (comum.py).
# O Gabriel ocupa da linha 8 à linha 106 (99 px de altura, 1,75 m), o pé
# sempre na mesma linha, e o centro do corpo na coluna 47.
QUADRO = (96, 112)
ALTURA_PX = 99
LINHA_PE = 106
CENTRO_X = 47
QUADROS_ANDAR = 12
QUADROS_PARADO = 8
TAM_RETRATO = 80
MAX_CORES = 40          # paleta dos sprites (todas as vistas e animações)
MAX_CORES_RETRATO = 48  # paleta dos retratos (o rosto grande pede mais tons)

# Recortes das referências (x0, y0, x1, y1), em pixels da imagem original.
RECORTE_FRENTE = (0, 0, 419, 1024)
RECORTE_LADO = (40, 0, 260, 572)
# Na referência de lado a cabeça saiu maior que na de frente (do cabelo ao
# queixo, 21 px contra 18). Ela é encolhida para 85%, presa no pescoço,
# antes de reduzir o desenho; o corpo cresce um pouco para a altura total
# continuar 99 px, igual às outras vistas.
ESCALA_CABECA_LADO = 0.85
QUEIXO_LADO = 21 / 99   # onde a cabeça acaba, em fração da altura da figura
RETRATOS = {
    "normal": (20, 14, 240, 251),
    "bravo": (276, 14, 496, 251),
    "preocupado": (533, 14, 751, 251),
    "surpreso": (785, 14, 1003, 251),
    "envergonhado": (145, 308, 367, 550),
}


# ---------------------------------------------------------------------------
# 1. Recorte e redução
# ---------------------------------------------------------------------------

def abrir_rgb(nome, caixa):
    img = Image.open(os.path.join(PASTA_REF, nome)).convert("RGB").crop(caixa)
    return np.asarray(img).astype(np.float32)


def mascara_figura(rgb, tolerancia=22):
    # O fundo é um cinza quase liso. Fundo é o que tem a cor dele E está
    # ligado à borda da imagem (inundação a partir de um canto). Assim os
    # cordões do capuz, que são cinza claro mas ficam dentro da figura, não
    # viram buraco.
    # A cor do fundo vem da faixa de cima e dos cantos de cima (embaixo o
    # recorte pode cortar a figura, como o moletom nos retratos).
    borda = np.concatenate([rgb[:4].reshape(-1, 3), rgb[:, :4].reshape(-1, 3),
                            rgb[:, -4:].reshape(-1, 3)])
    fundo = np.median(borda, axis=0)
    parece_fundo = np.abs(rgb - fundo).max(axis=2) <= tolerancia
    h, w = parece_fundo.shape
    img = Image.new("L", (w + 2, h + 2), 255)
    img.paste(Image.fromarray(parece_fundo.astype(np.uint8) * 255), (1, 1))
    ImageDraw.floodfill(img, (0, 0), 128, thresh=0)
    figura = np.asarray(img)[1:-1, 1:-1] != 128
    # A inundação passa pela moldura em volta da imagem; a figura que
    # encosta na borda de baixo continua inteira.
    return figura


def aparar(rgb, mascara):
    ys, xs = np.where(mascara)
    return (rgb[ys.min():ys.max() + 1, xs.min():xs.max() + 1],
            mascara[ys.min():ys.max() + 1, xs.min():xs.max() + 1])


def espalhar_cor(rgb, mascara, passos=6):
    # Pinta o fundo com a cor da borda da figura antes de reduzir: senão o
    # cinza do fundo entra na média e o contorno sai desbotado.
    rgb = rgb.copy()
    m = mascara.copy()
    for _ in range(passos):
        soma = np.zeros_like(rgb)
        cont = np.zeros(m.shape, np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sm = np.roll(m, (dy, dx), (0, 1))
            soma += np.roll(rgb * m[..., None], (dy, dx), (0, 1))
            cont += sm
        novo = (~m) & (cont > 0)
        rgb[novo] = soma[novo] / cont[novo][:, None]
        m = m | novo
    return rgb


def reduzir(rgb, mascara, largura, altura):
    # Cor com Lanczos (preserva o contraste dos detalhes pequenos, como
    # olho e boca) e transparência com média simples (caixa): o pixel fica
    # opaco se mais da metade dele era figura.
    rgb = espalhar_cor(rgb, mascara)
    canais = [np.asarray(Image.fromarray(rgb[..., c]).resize((largura, altura), Image.LANCZOS))
              for c in range(3)]
    alfa = np.asarray(Image.fromarray(mascara.astype(np.float32)).resize(
        (largura, altura), Image.BOX))
    cor = np.clip(np.dstack(canais), 0, 255)
    return cor, alfa > 0.5


def encolher_cabeca(rgb, mascara, fracao_queixo, escala, escala_x=None):
    # Corta a figura na altura do queixo, encolhe a parte de cima e cola de
    # volta com o meio do pescoço no mesmo lugar. escala_x, se vier, é a
    # escala da largura (senão, a mesma da altura).
    corte = int(round(mascara.shape[0] * fracao_queixo))
    cab_rgb, cab_m = rgb[:corte], mascara[:corte]
    xs = np.where(cab_m[-3:].any(axis=0))[0]
    pescoco = (xs.min() + xs.max() + 1) / 2
    cab_rgb = espalhar_cor(cab_rgb, cab_m)
    escala_x = escala if escala_x is None else escala_x
    w = max(1, round(cab_m.shape[1] * escala_x))
    h = max(1, round(corte * escala))
    nova_cor = np.dstack([np.asarray(Image.fromarray(cab_rgb[..., c]).resize((w, h), Image.LANCZOS))
                          for c in range(3)])
    nova_m = np.asarray(Image.fromarray(cab_m.astype(np.float32)).resize((w, h), Image.BOX)) > 0.5
    x0 = int(round(pescoco - pescoco * escala_x))
    # Cabeça mais larga que antes pode passar da borda esquerda: o corpo
    # anda para a direita o tanto que falta.
    folga = max(0, -x0)
    x0 += folga
    corpo_rgb, corpo_m = rgb[corte:], mascara[corte:]
    largura = max(corpo_m.shape[1] + folga, x0 + w)
    out_rgb = np.zeros((h + corpo_m.shape[0], largura, 3), np.float32)
    out_m = np.zeros((h + corpo_m.shape[0], largura), bool)
    out_rgb[h:, folga:folga + corpo_m.shape[1]] = corpo_rgb
    out_m[h:, folga:folga + corpo_m.shape[1]] = corpo_m
    regiao = (slice(0, h), slice(x0, x0 + w))
    out_rgb[regiao] = np.where(nova_m[..., None], nova_cor, out_rgb[regiao])
    out_m[regiao] |= nova_m
    return aparar(out_rgb, out_m)


def figura_reduzida(nome, caixa, altura=ALTURA_PX, cabeca=None):
    rgb = abrir_rgb(nome, caixa)
    rgb, m = aparar(rgb, mascara_figura(rgb))
    if cabeca is not None:
        rgb, m = encolher_cabeca(rgb, m, *cabeca)
    largura = max(1, round(m.shape[1] * altura / m.shape[0]))
    return reduzir(rgb, m, largura, altura)


# ---------------------------------------------------------------------------
# 2. Paleta (k-médias no espaço de cor Lab)
# ---------------------------------------------------------------------------
# Pixel art feita à mão usa poucas cores, repetidas em todo o personagem.
# O k-médias acha as K cores que melhor representam todos os pixels: começa
# com K cores, junta cada pixel à cor mais próxima e troca cada cor pela
# média do seu grupo, até parar de mudar. A distância é medida em Lab, onde
# a diferença entre dois números é parecida com a diferença que o olho vê.

def srgb_para_lab(rgb):
    c = rgb / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124, 0.3576, 0.1805],
                  [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]])
    xyz = c @ m.T / np.array([0.9505, 1.0, 1.089])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16,
                     500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], axis=-1)


def k_medias(cores, k, iteracoes=30, semente=7):
    lab = srgb_para_lab(cores)
    rng = np.random.default_rng(semente)
    # Começo "k-means++": cada centro novo é sorteado longe dos que já
    # existem, para os tons raros (olho, boca, cordão) ganharem uma cor.
    centros = [lab[rng.integers(len(lab))]]
    for _ in range(k - 1):
        d = np.min([((lab - c) ** 2).sum(1) for c in centros], axis=0)
        centros.append(lab[rng.choice(len(lab), p=d / d.sum())])
    centros = np.array(centros)
    for _ in range(iteracoes):
        grupo = np.argmin(((lab[:, None] - centros[None]) ** 2).sum(2), axis=1)
        for i in range(k):
            if np.any(grupo == i):
                centros[i] = lab[grupo == i].mean(0)
    grupo = np.argmin(((lab[:, None] - centros[None]) ** 2).sum(2), axis=1)
    paleta = np.array([cores[grupo == i].mean(0) if np.any(grupo == i) else cores[0]
                       for i in range(k)])
    return np.round(paleta).astype(np.uint8)


def paleta_de(imagens, k):
    cores = np.concatenate([cor[m] for cor, m in imagens])
    if len(cores) > 40000:
        cores = cores[np.random.default_rng(3).choice(len(cores), 40000, replace=False)]
    return k_medias(cores, k)


def indices_na_paleta(cor, paleta):
    lab = srgb_para_lab(cor.reshape(-1, 3).astype(np.float32))
    pal = srgb_para_lab(paleta.astype(np.float32))
    idx = np.argmin(((lab[:, None] - pal[None]) ** 2).sum(2), axis=1)
    return idx.reshape(cor.shape[:2])


# ---------------------------------------------------------------------------
# 3. Sprite indexado: cada pixel guarda o número da cor na paleta (-1 vazio)
# ---------------------------------------------------------------------------

def indexar(cor, mascara, paleta):
    idx = indices_na_paleta(cor, paleta)
    return np.where(mascara, idx, -1)


def mais_escura(paleta, i, fator=0.42):
    # A cor da paleta mais perto do tom i escurecido: o contorno de cada
    # parte fica num tom escuro da própria parte (vinho no moletom, azul
    # fundo na calça, marrom no cabelo), como na referência.
    alvo = paleta[i].astype(np.float32) * fator
    return int(indices_na_paleta(alvo[None, None], paleta)[0, 0])


def contornar(spr, paleta):
    # Contorno de 1 pixel: todo pixel da figura que encosta no vazio
    # (em cima, embaixo ou dos lados) vira o tom escuro da sua cor.
    cheio = spr >= 0
    borda = np.zeros_like(cheio)
    pad = np.pad(cheio, 1, constant_values=False)
    for dy, dx in ((0, 1), (2, 1), (1, 0), (1, 2)):
        borda |= ~pad[dy:dy + cheio.shape[0], dx:dx + cheio.shape[1]]
    borda &= cheio
    escuras = {}
    out = spr.copy()
    for y, x in zip(*np.where(borda)):
        i = spr[y, x]
        if i not in escuras:
            escuras[i] = mais_escura(paleta, i)
        out[y, x] = escuras[i]
    return out


def no_quadro(spr, centro_x=CENTRO_X, linha_pe=LINHA_PE):
    quadro = np.full((QUADRO[1], QUADRO[0]), -1, np.int32)
    h, w = spr.shape
    x0 = centro_x - w // 2
    y0 = linha_pe + 1 - h
    quadro[y0:y0 + h, x0:x0 + w] = spr
    return quadro


def para_rgba(spr, paleta):
    out = np.zeros(spr.shape + (4,), np.uint8)
    cheio = spr >= 0
    out[cheio, :3] = paleta[spr[cheio]]
    out[cheio, 3] = 255
    return out


def salvar(rgba, nome):
    Image.fromarray(rgba, "RGBA").save(os.path.join(PASTA_SAIDA, nome))


# ---------------------------------------------------------------------------
# 4. Ferramentas de sprite indexado
# ---------------------------------------------------------------------------

def vazio():
    return np.full((QUADRO[1], QUADRO[0]), -1, np.int32)


def perto(paleta, rgb):
    # A cor da paleta mais perto de uma cor qualquer (para pintar detalhes
    # novos, como o capuz das costas, sempre com cores que já existem).
    return int(indices_na_paleta(np.array(rgb, np.float32)[None, None], paleta)[0, 0])


def eh_azul(paleta, spr):
    cor = paleta[np.maximum(spr, 0)].astype(int)
    return (spr >= 0) & (cor[..., 2] > cor[..., 0] + 15)


def luminancia(paleta):
    return paleta.astype(np.float32) @ np.array([0.299, 0.587, 0.114])


def compor(*camadas):
    # Desenha as camadas em ordem: a última fica por cima.
    out = vazio()
    for c in camadas:
        out = np.where(c >= 0, c, out)
    return out


def so(spr, mascara):
    return np.where(mascara & (spr >= 0), spr, -1)


def mover(spr, dx, dy):
    out = vazio()
    h, w = spr.shape
    ys, xs = np.where(spr >= 0)
    ys2, xs2 = ys + dy, xs + dx
    ok = (ys2 >= 0) & (ys2 < h) & (xs2 >= 0) & (xs2 < w)
    out[ys2[ok], xs2[ok]] = spr[ys[ok], xs[ok]]
    return out


def espelhar(spr):
    # Espelha em volta da coluna do centro (CENTRO_X continua no meio).
    out = vazio()
    ys, xs = np.where(spr >= 0)
    xs2 = 2 * CENTRO_X - xs
    ok = (xs2 >= 0) & (xs2 < spr.shape[1])
    out[ys[ok], xs2[ok]] = spr[ys[ok], xs[ok]]
    return out


def preencher(spr, buraco, paleta, evitar_escuras=True):
    # Tapa um buraco com as cores de volta: cada pixel do buraco vira a cor
    # mais comum entre os vizinhos já pintados, de fora para dentro. Serve
    # para apagar o braço do tronco (quando ele balança, aparece o moletom
    # que estava atrás) e a mão da calça.
    spr = spr.copy()
    lum = luminancia(paleta)
    falta = buraco.copy()
    spr[falta] = -1
    while falta.any():
        mudou = False
        for y, x in zip(*np.where(falta)):
            viz = [spr[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                   if (dy or dx) and 0 <= y + dy < spr.shape[0] and 0 <= x + dx < spr.shape[1]
                   and not falta[y + dy, x + dx] and spr[y + dy, x + dx] >= 0]
            if evitar_escuras:
                claras = [v for v in viz if lum[v] > 45]
                viz = claras or viz
            if viz:
                vals, conts = np.unique(viz, return_counts=True)
                spr[y, x] = vals[np.argmax(conts)]
                falta[y, x] = False
                mudou = True
        if not mudou:
            break
    return spr


def tabela_escura(paleta, fator):
    return np.array([perto(paleta, paleta[i].astype(np.float32) * fator)
                     for i in range(len(paleta))])


def escurecer(spr, tabela):
    return np.where(spr >= 0, tabela[np.maximum(spr, 0)], -1)


def contorno_final(spr, paleta, tabela):
    # Igual ao contornar(), mas não escurece o que já é escuro: pode ser
    # chamado de novo depois de montar um quadro de animação, para fechar o
    # contorno onde as camadas se separaram (perna que abriu, braço que
    # saiu da frente do corpo).
    lum = luminancia(paleta)
    cheio = spr >= 0
    pad = np.pad(cheio, 1, constant_values=False)
    borda = np.zeros_like(cheio)
    for dy, dx in ((0, 1), (2, 1), (1, 0), (1, 2)):
        borda |= ~pad[dy:dy + cheio.shape[0], dx:dx + cheio.shape[1]]
    borda &= cheio
    out = spr.copy()
    alvo = borda & (lum[np.maximum(spr, 0)] > 70)
    out[alvo] = tabela[spr[alvo]]
    return out


def limpar_migalhas(spr, minimo=8):
    # Tira os pedacinhos soltos (menos de "minimo" pixels ligados entre si)
    # que sobram quando uma peça gira e deixa para trás um canto do desenho
    # antigo. Cada grupo de pixels vizinhos (em cima, embaixo e dos lados) é
    # achado por uma busca em largura a partir de um pixel ainda não visto.
    cheio = spr >= 0
    visto = np.zeros_like(cheio)
    out = spr.copy()
    h, w = spr.shape
    for y0, x0 in zip(*np.where(cheio)):
        if visto[y0, x0]:
            continue
        grupo = [(y0, x0)]
        visto[y0, x0] = True
        i = 0
        while i < len(grupo):
            y, x = grupo[i]
            i += 1
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < h and 0 <= xx < w and cheio[yy, xx] and not visto[yy, xx]:
                    visto[yy, xx] = True
                    grupo.append((yy, xx))
        if len(grupo) < minimo:
            for y, x in grupo:
                out[y, x] = -1
    return out


def separar_contorno(spr, sobre, tabela, paleta):
    # Linha escura onde uma camada da frente encosta numa camada de trás
    # (a perna da frente sobre a de trás): sem ela, as duas viram um borrão.
    lum = luminancia(paleta)
    cheio = spr >= 0
    out = spr.copy()
    for y, x in zip(*np.where(cheio)):
        for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < spr.shape[0] and 0 <= xx < spr.shape[1]:
                if not cheio[yy, xx] and sobre[yy, xx] >= 0 and lum[spr[y, x]] > 70:
                    out[y, x] = tabela[spr[y, x]]
                    break
    return out


# ---------------------------------------------------------------------------
# 5. Girar um pedaço de pixel art (RotSprite simplificado)
# ---------------------------------------------------------------------------
# Girar pixel art direto deixa a linha serrilhada e some com pixels. O
# truque do RotSprite: aumentar a imagem 4 vezes com o Scale2x (que
# arredonda as diagonais em vez de fazer escadinha), girar a imagem grande
# pegando o pixel mais próximo, e voltar ao tamanho original pegando um
# pixel de cada bloco de 4 x 4.
#
# Scale2x: cada pixel P vira 4. Olhando os vizinhos de cima (A), da
# esquerda (C), da direita (B) e de baixo (D), o canto de cima à esquerda
# vira C se C == A (e A != B, C != D); senão fica P. Os outros três cantos
# seguem a mesma regra girada.

def scale2x(spr):
    p = np.pad(spr, 1, mode="edge")
    P = p[1:-1, 1:-1]
    A, D = p[:-2, 1:-1], p[2:, 1:-1]
    C, B = p[1:-1, :-2], p[1:-1, 2:]
    out = np.repeat(np.repeat(P, 2, 0), 2, 1)
    base = (A != D) & (C != B)
    out[0::2, 0::2] = np.where(base & (C == A), C, P)
    out[0::2, 1::2] = np.where(base & (A == B), B, P)
    out[1::2, 0::2] = np.where(base & (D == C), C, P)
    out[1::2, 1::2] = np.where(base & (B == D), D, P)
    return out


def girar(spr, graus, pivo, destino=None):
    # Gira em volta do pivô (x, y) e põe o pivô no ponto destino. Ângulo
    # positivo leva a ponta de baixo para a frente (para a direita).
    if destino is None:
        destino = pivo
    grande = scale2x(scale2x(spr))
    a = np.radians(graus)
    h, w = spr.shape
    ys, xs = np.mgrid[0:h * 4, 0:w * 4]
    # Inverso da rotação: para cada pixel de saída, de onde ele veio.
    dx = (xs + 0.5) / 4 - destino[0]
    dy = (ys + 0.5) / 4 - destino[1]
    sx = dx * np.cos(a) - dy * np.sin(a) + pivo[0]
    sy = dx * np.sin(a) + dy * np.cos(a) + pivo[1]
    gx = np.floor(sx * 4).astype(int)
    gy = np.floor(sy * 4).astype(int)
    ok = (gx >= 0) & (gx < w * 4) & (gy >= 0) & (gy < h * 4)
    girado = np.full((h * 4, w * 4), -1, np.int32)
    girado[ok] = grande[gy[ok], gx[ok]]
    return girado[1::4, 1::4]


def ponto_girado(pt, graus, pivo, destino):
    a = np.radians(graus)
    dx, dy = pt[0] - pivo[0], pt[1] - pivo[1]
    return (destino[0] + dx * np.cos(a) + dy * np.sin(a),
            destino[1] - dx * np.sin(a) + dy * np.cos(a))


def remapear_linhas(spr, pontos, x0=0, x1=None):
    # Estica ou encolhe na vertical, entre as colunas x0 e x1. pontos é a
    # lista (linha de origem, linha de destino); entre eles a conta é linear.
    # Para cada linha de destino, procura de qual linha de origem ela vem.
    if x1 is None:
        x1 = spr.shape[1]
    out = spr.copy()
    out[:, x0:x1] = -1
    origem = np.array([o for o, _ in pontos], np.float32)
    dest = np.array([d for _, d in pontos], np.float32)
    for yd in range(spr.shape[0]):
        if yd < dest[0] or yd > dest[-1]:
            continue
        ys = int(round(np.interp(yd, dest, origem)))
        if 0 <= ys < spr.shape[0]:
            out[yd, x0:x1] = spr[ys, x0:x1]
    return out


# ---------------------------------------------------------------------------
# 6. As costas
# ---------------------------------------------------------------------------
# Linhas do corpo no quadro (iguais em todas as vistas):
LINHA_QUEIXO = 28     # até aqui é cabeça
LINHA_BAINHA = 63     # última linha do moletom
LINHA_VIRILHA = 73    # daqui para baixo as pernas são separadas
LINHA_JOELHO = 85
LINHA_TORNOZELO = 99  # daqui para baixo é o tênis


def capuz_das_costas(paleta):
    # O capuz caído nas costas: uma gota arredondada que sai da gola e
    # desce até o meio das costas, com contorno vinho, o vermelho do
    # moletom por dentro, uma costura no meio e a sombra que ele faz embaixo.
    base = perto(paleta, (230, 30, 36))
    meio = perto(paleta, (200, 25, 40))
    borda = perto(paleta, (106, 13, 42))
    sombra = perto(paleta, (147, 17, 43))
    luz = perto(paleta, (240, 32, 36))
    topo, fundo, meia_larg = 26, 42, 8.5
    capuz = vazio()
    for y in range(topo, fundo + 2):
        v = (y - topo) / (fundo - topo)
        w = meia_larg * np.sqrt(max(0.0, 1 - max(0.0, v - 0.2) ** 2 / 0.8 ** 2))
        for x in range(int(CENTRO_X - w), int(CENTRO_X + w) + 1):
            capuz[y, x] = base
    dentro = capuz >= 0
    pad = np.pad(dentro, 1)
    em_volta = ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
    capuz[dentro & em_volta] = borda
    for y in range(topo + 2, fundo - 2):
        if capuz[y, CENTRO_X] == base:
            capuz[y, CENTRO_X] = meio
    for y in range(topo + 2, fundo - 1):
        for x in range(CENTRO_X + 3, CENTRO_X + 9):
            if capuz[y, x] == base:
                capuz[y, x] = meio
    for y in range(topo + 1, topo + 6):
        for x in range(CENTRO_X - 6, CENTRO_X - 2):
            if capuz[y, x] == base:
                capuz[y, x] = luz
    sombra_spr = vazio()
    for x in range(QUADRO[0]):
        col = np.where(dentro[:, x])[0]
        if len(col):
            sombra_spr[col.max() + 1:col.max() + 3, x] = sombra
    return capuz, sombra_spr


def criar_costas(F, paleta):
    # As costas não estão na referência. Partem da frente espelhada (o lado
    # direito dele passa para o outro lado da tela) e trocam o que só existe
    # na frente: o rosto vira cabelo e nuca, os cordões e o bolso somem, o
    # capuz aparece caído nas costas e a calça ganha os bolsos de trás.
    B = espelhar(F)
    ys, xs = np.mgrid[0:QUADRO[1], 0:QUADRO[0]]
    cab_escuro = perto(paleta, (54, 27, 39))
    cab_medio = perto(paleta, (77, 40, 42))
    cab_claro = perto(paleta, (101, 54, 44))
    cab_brilho = perto(paleta, (131, 74, 53))
    nuca = perto(paleta, (182, 113, 100))
    nuca_sombra = perto(paleta, (132, 95, 95))
    # Cabeça: o rosto vira cabelo. As mechas saem do redemoinho (no alto
    # da cabeça) e descem abrindo em leque: um pixel é risco escuro entre
    # mechas quando o ângulo dele, visto do redemoinho, cai perto de uma
    # das linhas do leque. Em cima fica o brilho; embaixo, o cabelo escurece
    # e afina até a nuca, e abaixo dela aparece o pescoço.
    redemoinho = (CENTRO_X + 1, 9)
    for y in range(11, LINHA_QUEIXO + 1):
        linha = np.where(F[y] >= 0)[0]
        if not len(linha):
            continue
        for x in range(linha.min() + 1, linha.max()):
            dx, dy = x - redemoinho[0], y - redemoinho[1]
            if y <= 21 or (y == 22 and abs(dx) <= 4):
                ang = np.degrees(np.arctan2(dx, dy + 2))
                risco = abs(((ang + 90) / 26) % 1 - 0.5) > 0.38
                dist = np.hypot(dx, dy)
                if risco and dist > 3:
                    cor = cab_escuro
                elif y <= 13 and dx < 2:
                    cor = cab_brilho
                elif y <= 16:
                    cor = cab_claro
                elif y <= 19:
                    cor = cab_medio
                else:
                    cor = cab_escuro if abs(dx) > 2 else cab_medio
                B[y, x] = cor
            elif abs(x - CENTRO_X) <= 3:
                B[y, x] = nuca_sombra if y <= 23 else nuca
            elif y <= 24:
                B[y, x] = -1
    # Tronco: sem cordões nem bolso, só o vermelho do moletom.
    base = perto(paleta, (230, 30, 36))
    meio = perto(paleta, (208, 27, 39))
    for y in range(LINHA_QUEIXO + 2, 57):
        for x in range(CENTRO_X - 6, CENTRO_X + 7):
            if B[y, x] >= 0:
                B[y, x] = meio if abs(x - CENTRO_X) == 6 else base
    capuz, sombra = capuz_das_costas(paleta)
    B = np.where((sombra >= 0) & (B >= 0) & (capuz < 0) & (ys < 57), sombra, B)
    B = np.where(capuz >= 0, capuz, B)
    # Calça: costura do meio e os dois bolsos de trás.
    costura = perto(paleta, (10, 50, 104))
    for y in range(LINHA_BAINHA, LINHA_VIRILHA):
        if B[y, CENTRO_X] >= 0 and eh_azul(paleta, B[y:y + 1, CENTRO_X:CENTRO_X + 1])[0, 0]:
            B[y, CENTRO_X] = costura
    for x0 in (CENTRO_X - 8, CENTRO_X + 2):
        for x in range(x0, x0 + 7):
            B[LINHA_BAINHA + 3, x] = costura
        for y in range(LINHA_BAINHA + 3, LINHA_BAINHA + 8):
            B[y, x0] = costura
            B[y, x0 + 6] = costura
        for x in range(x0, x0 + 7):
            B[LINHA_BAINHA + 8 + (1 if x0 + 2 <= x <= x0 + 4 else 0), x] = costura
    return B


# ---------------------------------------------------------------------------
# 7. Vista de lado em camadas (boneco recortado)
# ---------------------------------------------------------------------------
# Para andar de lado, o sprite parado é recortado em peças que giram nas
# juntas, como um boneco de papel com tachinhas: o braço gira no ombro, a
# coxa no quadril, a canela no joelho e o pé no tornozelo. A perna e o
# braço do lado de lá são cópias mais escuras das peças, desenhadas atrás
# do corpo. Onde o braço e a mão tapavam o corpo e a calça, as cores são
# preenchidas (função preencher), para aparecer moletom quando o braço sai.

BRACO_LADO = [(42, 32), (50, 32), (51, 45), (52, 58), (54, 64), (55, 76),
              (45, 76), (44, 64), (42, 50)]
OMBRO_LADO = (46.5, 34.0)
QUADRIL_LADO = (47.0, 67.0)


def mascara_poligono(pontos):
    img = Image.new("L", (QUADRO[0], QUADRO[1]), 0)
    ImageDraw.Draw(img).polygon(pontos, fill=255)
    return np.asarray(img) > 0


def camadas_lado(L, paleta):
    ys, xs = np.mgrid[0:QUADRO[1], 0:QUADRO[0]]
    azul = eh_azul(paleta, L)
    # Abaixo da bainha, do braço só fica a mão: a pele e a borda dela (o
    # resto ali é contorno da calça).
    cor = paleta[np.maximum(L, 0)].astype(int)
    pele = (L >= 0) & (cor[..., 0] > 140) & (cor[..., 1] > 80) & (cor[..., 0] > cor[..., 2] + 30)
    pad = np.pad(pele, 1)
    perto_pele = pele.copy()
    for dy in (0, 1, 2):
        for dx in (0, 1, 2):
            perto_pele |= pad[dy:dy + pele.shape[0], dx:dx + pele.shape[1]]
    braco = mascara_poligono(BRACO_LADO) & (L >= 0) &         ((ys <= LINHA_BAINHA + 3) & ~azul | (ys <= LINHA_BAINHA) | (perto_pele & ~azul))
    perna = (L >= 0) & ~braco & ((ys > LINHA_BAINHA) | ((ys >= LINHA_BAINHA - 2) & azul))
    corpo = so(L, ~perna & ~braco)
    # Tapa o buraco do braço no corpo e o da mão na calça.
    # Atrás do braço é o lado do moletom: vermelho de base, e a bainha
    # continua com as cores da bainha de volta.
    buraco_corpo = braco & (ys <= LINHA_BAINHA)
    corpo = np.where(buraco_corpo, perto(paleta, (230, 30, 36)), corpo)
    bainha = buraco_corpo & (ys >= LINHA_BAINHA - 4)
    corpo = preencher(corpo, bainha, paleta, evitar_escuras=False)
    pernas = so(L, perna)
    buraco_perna = braco & (ys > LINHA_BAINHA)
    pernas = preencher(np.where(buraco_perna, 0, pernas), buraco_perna, paleta)
    # A calça continua por baixo da bainha até o quadril: quando a coxa
    # gira, não abre um buraco entre o moletom e a perna.
    for y in range(LINHA_BAINHA - 6, LINHA_BAINHA + 1):
        linha = pernas[LINHA_BAINHA + 2]
        pernas[y] = np.where(pernas[y] >= 0, pernas[y], linha)
    return {"corpo": corpo, "braco": so(L, braco), "pernas": pernas}


def pecas_da_perna(pernas):
    # Coxa, canela e pé, cada um com a junta de cima (onde ele gira).
    ys = np.arange(QUADRO[1])[:, None]
    def centro_linha(y):
        xs = np.where(pernas[y] >= 0)[0]
        return (xs.min() + xs.max() + 1) / 2
    joelho = (centro_linha(LINHA_JOELHO), float(LINHA_JOELHO))
    tornozelo = (centro_linha(LINHA_TORNOZELO - 2), float(LINHA_TORNOZELO))
    coxa = np.where(ys <= LINHA_JOELHO + 1, pernas, -1)
    canela = np.where((ys >= LINHA_JOELHO - 1) & (ys <= LINHA_TORNOZELO), pernas, -1)
    pe = np.where(ys >= LINHA_TORNOZELO, pernas, -1)
    return coxa, canela, pe, joelho, tornozelo


# ---------------------------------------------------------------------------
# 8. Vistas de 3/4 (boneco recortado a partir da pose de passo)
# ---------------------------------------------------------------------------
# A referência andar_diagonal.webp tem o Gabriel dando um passo de 3/4 de
# frente e de 3/4 de costas. De cada pose saem o corpo (cabeça e tronco) e
# os dois braços, que giram no ombro como na vista de lado. As pernas da
# pose vêm dobradas e com o tênis de trás apontando para trás, e giradas
# ficavam tortas; então as pernas do 3/4 são as mesmas peças da vista de
# lado (coxa, canela e tênis, que já aponta para a frente), presas nos dois
# quadris da pose.
#
# Na diagonal o passo aparece mais curto que de lado (o corpo está virado
# para a câmera), então os ângulos da caminhada de lado são multiplicados
# por PASSO_3Q. E o pé que vai à frente fica PASSO_Y pixels mais baixo na
# tela no 3/4 de frente (ele anda na direção da câmera) e mais alto no de
# costas (anda para longe).
#
# "perto" é o lado do corpo virado para a câmera (desenhado na frente do
# corpo); "longe", o outro (desenhado atrás). Na referência o braço que
# vai à frente é o do mesmo lado da perna que vai à frente; no boneco cada
# braço balança ao contrário da perna do seu lado, como numa caminhada.

PASSO_3Q = 0.6
PASSO_Y = 3.0
BRACO_3Q = 12.0
ESCALA_POSE = 55 / 306   # do alto do cabelo à bainha: 306 px na referência, 55 no sprite
# Como na vista de lado, a cabeça da pose saiu maior que a da frente (do
# cabelo ao queixo, 22 px contra 19): encolhe para 87%, presa no pescoço.
ESCALA_CABECA_3Q = 0.87

POSES_3Q = {
    "tres_quartos": {
        "caixa": (30, 0, 256, 572),
        "queixo": 0.23,
        "sentido": 1,
        "cabelo": [(35, 7), (58, 7), (58, 14), (44, 15), (43, 22), (34, 22)],
        "braco_perto": [(28, 36), (38, 33), (38, 46), (37, 58), (35, 64), (38, 74), (27, 74),
                        (27, 50)],
        "braco_longe": [(53, 34), (58, 36), (62, 50), (64, 57), (71, 58), (71, 71), (59, 71),
                        (57, 62), (54, 50)],
        "ombro_perto": (34.5, 37.0), "ombro_longe": (56.0, 38.0),
        "quadril_perto": (42.0, 68.0), "quadril_longe": (49.0, 68.0),
    },
    "tres_quartos_costas": {
        "caixa": (540, 0, 775, 572),
        "queixo": 0.22,
        "sentido": -1,
        "cabelo": None,
        "braco_longe": [(28, 36), (37, 34), (38, 46), (37, 58), (35, 64), (38, 72), (27, 72),
                        (27, 50)],
        "braco_perto": [(53, 33), (58, 35), (61, 48), (63, 60), (67, 61), (67, 72), (55, 72),
                        (56, 62), (53, 48)],
        "ombro_longe": (34.5, 37.0), "ombro_perto": (56.0, 37.0),
        "quadril_perto": (50.0, 68.0), "quadril_longe": (43.0, 68.0),
    },
}


def angulo(de, ate):
    # Graus a partir da vertical; positivo = a ponta vai para a direita
    # (para a frente, nos dois 3/4).
    return float(np.degrees(np.arctan2(ate[0] - de[0], ate[1] - de[1])))


def pose_de_referencia(caixa, queixo, paleta):
    rgb = abrir_rgb("andar_diagonal.webp", caixa)
    rgb, m = aparar(rgb, mascara_figura(rgb))
    rgb, m = encolher_cabeca(rgb, m, queixo, ESCALA_CABECA_3Q)
    cor, mm = reduzir(rgb, m, round(m.shape[1] * ESCALA_POSE), round(m.shape[0] * ESCALA_POSE))
    return no_quadro(contornar(indexar(cor, mm, paleta), paleta))


def pintar_cabelo(spr, poligono, paleta):
    # Na pose de 3/4 de frente o cabelo saiu loiro (a referência variou).
    # Os pixels da área do cabelo voltam para os quatro castanhos do
    # Gabriel pela claridade: o quarto mais escuro vira o castanho mais
    # escuro, e assim por diante. O contorno (bem escuro) fica como está.
    if poligono is None:
        return spr
    rampa = np.array([perto(paleta, c) for c in
                      ((54, 27, 39), (77, 40, 42), (101, 54, 44), (131, 74, 53))])
    lum = luminancia(paleta)
    area = mascara_poligono(poligono) & (spr >= 0)
    area &= lum[np.maximum(spr, 0)] > 45
    if not area.any():
        return spr
    valores = lum[spr[area]]
    cortes = np.quantile(valores, [0.25, 0.55, 0.85])
    out = spr.copy()
    out[area] = rampa[np.searchsorted(cortes, valores)]
    return out


class Boneco3q:
    def __init__(self, cfg, paleta, pecas_lado):
        P = pintar_cabelo(pose_de_referencia(cfg["caixa"], cfg["queixo"], paleta),
                          cfg["cabelo"], paleta)
        self.sentido = cfg["sentido"]
        self.pecas = pecas_lado
        ys, xs = np.mgrid[0:QUADRO[1], 0:QUADRO[0]]
        azul = eh_azul(paleta, P)
        cor = paleta[np.maximum(P, 0)].astype(int)
        pele = (P >= 0) & (cor[..., 0] > 140) & (cor[..., 1] > 80) & (cor[..., 0] > cor[..., 2] + 30)
        pad = np.pad(pele, 1)
        perto_pele = pele.copy()
        for dy in (0, 1, 2):
            for dx in (0, 1, 2):
                perto_pele |= pad[dy:dy + pele.shape[0], dx:dx + pele.shape[1]]
        self.bracos = {}
        ocupado = np.zeros(P.shape, bool)
        for lado in ("perto", "longe"):
            m = mascara_poligono(cfg["braco_" + lado]) & (P >= 0) & ~azul & \
                ((ys <= LINHA_BAINHA) | perto_pele)
            self.bracos[lado] = so(P, m)
            ocupado |= m
        self.quadril = {lado: cfg["quadril_" + lado] for lado in ("perto", "longe")}
        # O assento da calça, logo abaixo da bainha, fica parado atrás das
        # pernas: quando elas se abrem, não aparece buraco entre as coxas.
        x_min = min(q[0] for q in self.quadril.values()) - 6
        x_max = max(q[0] for q in self.quadril.values()) + 6
        self.assento = so(P, azul & ~ocupado & (ys >= LINHA_BAINHA - 2) & (ys <= LINHA_BAINHA + 5)
                          & (xs >= x_min) & (xs <= x_max))
        # O corpo acaba na bainha e não guarda nada da área dos braços:
        # restos da mão e do punho ficariam boiando quando o braço balança.
        area_bracos = mascara_poligono(cfg["braco_perto"]) | mascara_poligono(cfg["braco_longe"])
        self.corpo = so(P, ~ocupado & ~azul & ~area_bracos & (ys <= LINHA_BAINHA + 1))
        self.ombro = {lado: cfg["ombro_" + lado] for lado in ("perto", "longe")}
        self.ang_braco = {}
        for lado, b in self.bracos.items():
            yb, xb = np.where(b >= 0)
            mao = yb >= yb.max() - 6
            self.ang_braco[lado] = angulo(self.ombro[lado], (xb[mao].mean(), yb[mao].mean()))

    def perna(self, lado, fase, andando):
        if andando:
            p_ = np.radians(fase)
            coxa = PASSO_3Q * COXA * np.sin(p_)
            joelho = PASSO_3Q * JOELHO * max(0.0, np.cos(p_)) ** 1.5
            desce = int(round(self.sentido * PASSO_Y * np.sin(p_)))
        else:
            coxa = joelho = 0.0
            desce = 0
        return mover(perna_lado(self.pecas, coxa, joelho, self.quadril[lado]), 0, desce)

    def quadro(self, fase, paleta, sombra, contorno, andando=True):
        partes = {}
        for lado, desloc in (("perto", 0), ("longe", 180)):
            braco = -BRACO_3Q * np.sin(np.radians(fase + desloc)) if andando else 0.0
            partes["perna_" + lado] = self.perna(lado, fase + desloc, andando)
            partes["braco_" + lado] = girar(self.bracos[lado], braco - self.ang_braco[lado],
                                            self.ombro[lado])
        longe = compor(partes["braco_longe"], escurecer(partes["perna_longe"], sombra))
        perna_perto = separar_contorno(partes["perna_perto"], longe, contorno, paleta)
        meio = compor(longe, self.assento, perna_perto, self.corpo)
        braco_perto = separar_contorno(partes["braco_perto"], meio, contorno, paleta)
        quadro = limpar_migalhas(compor(meio, braco_perto))
        return contorno_final(assentar(quadro), paleta, contorno)


# ---------------------------------------------------------------------------
# 9. Animações
# ---------------------------------------------------------------------------
# Caminhada: um ciclo são DOIS passos, e a fase φ vai de 0 a 360 graus
# (12 quadros, 30° cada). É a mesma conta do comum.py, que os outros
# personagens usam no Blender:
#   coxa   = COXA · sen φ                a perna balança (positivo = frente);
#                                        a outra perna usa φ + 180°
#   joelho = JOELHO · máx(0, cos φ)^1,5   dobra só enquanto a perna vem para a
#                                        frente no ar
#   braço  = −BRACO · sen φ              ao contrário da perna do mesmo lado
# O "sobe e desce" sai sozinho: depois de montar o quadro, o boneco desce
# até o pé mais baixo encostar na linha do chão.

COXA, JOELHO, BRACO = 22.0, 55.0, 16.0


def assentar(spr):
    linhas = np.where((spr >= 0).any(axis=1))[0]
    return mover(spr, 0, LINHA_PE - linhas.max())


def perna_lado(pecas, coxa_graus, joelho_graus, quadril):
    coxa, canela, pe, joelho, tornozelo = pecas
    a1 = coxa_graus
    a2 = coxa_graus - joelho_graus
    j = ponto_girado(joelho, a1, QUADRIL_LADO, quadril)
    t = ponto_girado(tornozelo, a2, joelho, j)
    return compor(girar(coxa, a1, QUADRIL_LADO, quadril),
                  girar(canela, a2, joelho, j),
                  mover(pe, int(round(t[0] - tornozelo[0])), int(round(t[1] - tornozelo[1]))))


def quadro_andar_lado(c, pecas, fase, paleta, escura, contorno):
    phi = np.radians(fase)
    pernas = []
    for desloc in (0, 180):
        p_ = np.radians(fase + desloc)
        pernas.append(perna_lado(pecas, COXA * np.sin(p_),
                                 JOELHO * max(0.0, np.cos(p_)) ** 1.5, QUADRIL_LADO))
    perto_, longe = pernas
    longe = escurecer(longe, escura)
    braco_perto = girar(c["braco"], -BRACO * np.sin(phi), OMBRO_LADO)
    braco_longe = escurecer(girar(c["braco"], BRACO * np.sin(phi), OMBRO_LADO), escura)
    fundo = compor(braco_longe, longe)
    perto_ = separar_contorno(perto_, fundo, contorno, paleta)
    meio = compor(fundo, perto_, c["corpo"])
    braco_perto = separar_contorno(braco_perto, meio, contorno, paleta)
    quadro = limpar_migalhas(compor(meio, braco_perto))
    return contorno_final(assentar(quadro), paleta, contorno)


# Parado: o peito sobe até 2 pixels ao puxar o ar e a cabeça vai junto,
# 60° atrasada (primeiro o peito, depois a cabeça), como no comum.py:
#   peito  = 2 · (1 − cos φ) / 2
#   cabeça = 2 · (1 − cos(φ − 60°)) / 2
# As pernas não mexem: o moletom estica entre o peito e a bainha.
SUBIDA = 2.0


def quadro_parado(spr, fase):
    phi = np.radians(fase)
    # Em pixels inteiros: meio pixel faria a conta repetir ou pular uma
    # linha no meio do rosto, e a cabeça sairia deformada.
    peito = round(SUBIDA * (1 - np.cos(phi)) / 2)
    cabeca = round(SUBIDA * (1 - np.cos(phi - np.radians(60))) / 2) if fase else 0
    return remapear_linhas(spr, [
        (0, -cabeca), (LINHA_QUEIXO - 2, LINHA_QUEIXO - 2 - cabeca),
        (LINHA_QUEIXO + 2, LINHA_QUEIXO + 2 - peito), (40, 40 - peito),
        (LINHA_BAINHA - 4, LINHA_BAINHA - 4), (QUADRO[1] - 1, QUADRO[1] - 1)])


# ---------------------------------------------------------------------------
# 9. Caminhada de frente e de costas (quatro poses desenhadas)
# ---------------------------------------------------------------------------
# andar_frente.webp e andar_costas.webp têm o Gabriel andando de frente e de
# costas em quatro poses: pé no chão, passando, o outro pé no chão,
# passando. Cada pose é recortada e reduzida como as outras referências e
# fica 3 dos 12 quadros do ciclo. O corpo é centrado pelo peito (não pelo
# desenho inteiro, que muda de largura com os braços) e o pé mais baixo vai
# para a linha do chão; assim o sobe e desce do desenho continua.
#
# Nas poses de frente a cabeça e o peito saíram maiores que no Gabriel
# parado (cabeça 23 px contra 19, peito 35 contra 31): o corpo estreita
# para 92% e a cabeça encolhe para 85% na altura e 95% na largura.
#
# O cabelo das poses de frente saiu loiro, e a calça das de costas mais
# cinza. As duas partes são repintadas com as cores do Gabriel parado
# (função repintar).

POSES_ANDAR = {
    "frente": {"arquivo": "andar_frente.webp",
               "colunas": [(30, 245), (250, 470), (584, 800), (797, 1015)],
               "largura": 0.92, "cabeca": (0.22, 0.85, 0.95)},
    "costas": {"arquivo": "andar_costas.webp",
               "colunas": [(28, 245), (250, 470), (584, 800), (797, 1016)],
               "largura": 1.0, "cabeca": None},
}
ESCALA_ANDAR = 55 / 304   # do alto do cabelo à bainha: 304 px na referência, 55 no sprite


def hsv(cor):
    # Matiz (0 a 360), saturação e brilho (0 a 1) de cada pixel.
    c = cor / 255.0
    mx, mn = c.max(axis=-1), c.min(axis=-1)
    delta = np.maximum(mx - mn, 1e-6)
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    h = np.where(mx == r, ((g - b) / delta) % 6,
                 np.where(mx == g, (b - r) / delta + 2, (r - g) / delta + 4)) * 60
    return h, np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0), mx


def material(cor, mascara, qual, de_costas=False):
    # Onde está cada material numa figura em cores (antes da paleta).
    #   calça: abaixo do moletom, mais azul que vermelho e com alguma cor
    #          (saturação acima de 0,22): o tênis cinza e o contorno quase
    #          preto ficam de fora, o jeans acinzentado das costas entra.
    #   cabelo: na cabeça (acima do capuz), sem o vermelho do capuz e sem o
    #          contorno. De costas é a cabeça toda, menos a pele (orelha e
    #          nuca, mais claras). De frente a cor não separa o cabelo loiro
    #          da pele, então vale a posição: os 40% de cima da cabeça, e os
    #          lados (fora do miolo do rosto) até 60% da altura.
    r, g, b = cor[..., 0], cor[..., 1], cor[..., 2]
    vermelho = mascara & (r > 150) & (g < 70)
    linhas_vermelhas = np.where(vermelho.sum(axis=1) >= 4)[0]
    capuz, bainha = linhas_vermelhas.min(), linhas_vermelhas.max()
    ys, xs = np.mgrid[0:mascara.shape[0], 0:mascara.shape[1]]
    h, sat, v = hsv(cor)
    if qual == "calca":
        return mascara & (ys > bainha - 3) & (b > r + 12) & (sat > 0.22) & (v > 0.25)
    cabeca = mascara & (ys < capuz) & (v >= 0.2) & ~vermelho
    if de_costas:
        return cabeca & (v < 0.88) & ((h < 45) | (h > 350)) & (ys < capuz - 2)
    topo = np.where(cabeca.any(axis=1))[0].min()
    altura = capuz - topo
    cabelo = cabeca & (ys < topo + 0.4 * altura)
    for y in range(int(topo + 0.4 * altura), int(topo + 0.6 * altura)):
        cols = np.where(cabeca[y])[0]
        if len(cols):
            largura = cols.max() - cols.min() + 1
            miolo = (xs[y] >= cols.min() + 0.2 * largura) & (xs[y] <= cols.max() - 0.2 * largura)
            cabelo[y] = cabeca[y] & ~miolo
    return cabelo


def repintar(spr, cor, mascara, molde, paleta):
    # Troca as cores de uma parte pelas do Gabriel parado, casando claro com
    # claro: cada pixel vira o tom do molde com a claridade mais perto da
    # dele, depois de esticar as claridades da pose para terem a mesma
    # média e o mesmo espalhamento (desvio-padrão) das do molde.
    if not mascara.any():
        return spr
    lum = luminancia(paleta)
    tons = np.unique(molde)
    alvo = lum[molde]
    origem = cor[mascara].astype(np.float32) @ np.array([0.299, 0.587, 0.114])
    z = (origem - origem.mean()) / max(origem.std(), 1e-3)
    # 0,7: um pouco menos de contraste que o molde, para os vincos da
    # calça desenhada não virarem manchas escuras.
    desejada = alvo.mean() + 0.7 * z * alvo.std()
    escolhido = tons[np.argmin(np.abs(lum[tons][None, :] - desejada[:, None]), axis=1)]
    out = spr.copy()
    out[mascara] = escolhido
    return out


def no_quadro_pelo_peito(spr):
    # Centra pelo peito (a linha 20 px abaixo do topo) e põe o pé no chão.
    linhas = np.where((spr >= 0).any(axis=1))[0]
    xs = np.where(spr[linhas.min() + 20] >= 0)[0]
    centro = (xs.min() + xs.max() + 1) / 2
    quadro = vazio()
    h, w = spr.shape
    x0 = int(round(CENTRO_X + 0.5 - centro))
    y0 = LINHA_PE - linhas.max()
    ys_, xs_ = np.where(spr >= 0)
    ok = (ys_ + y0 >= 0) & (ys_ + y0 < QUADRO[1]) & (xs_ + x0 >= 0) & (xs_ + x0 < QUADRO[0])
    quadro[ys_[ok] + y0, xs_[ok] + x0] = spr[ys_[ok], xs_[ok]]
    return quadro


def moldes_do_parado(frente_cor, frente_m, F_reduzido, paleta):
    # Os tons de calça e de cabelo que o Gabriel parado usa. Na calça, só
    # os azuis de verdade (sem o cinza-azulado do contorno e das sombras).
    moldes = {qual: F_reduzido[material(frente_cor, frente_m, qual) & (F_reduzido >= 0)]
              for qual in ("calca", "cabelo")}
    cor = paleta[moldes["calca"]].astype(int)
    moldes["calca"] = moldes["calca"][cor[:, 2] > cor[:, 0] + 40]
    return moldes


def ciclo_desenhado(cfg, paleta, moldes, contorno):
    poses = []
    for x0, x1 in cfg["colunas"]:
        rgb = abrir_rgb(cfg["arquivo"], (x0, 0, x1, 572))
        rgb, m = aparar(rgb, mascara_figura(rgb))
        if cfg["cabeca"]:
            queixo, escala, escala_x = cfg["cabeca"]
            rgb, m = encolher_cabeca(rgb, m, queixo, escala, escala_x / cfg["largura"])
        cor, mm = reduzir(rgb, m, round(m.shape[1] * ESCALA_ANDAR * cfg["largura"]),
                          round(m.shape[0] * ESCALA_ANDAR))
        spr = indexar(cor, mm, paleta)
        de_costas = cfg["arquivo"] == "andar_costas.webp"
        for qual in ("calca", "cabelo"):
            spr = repintar(spr, cor, material(cor, mm, qual, de_costas), moldes[qual], paleta)
        spr = contorno_final(no_quadro_pelo_peito(contornar(spr, paleta)), paleta, contorno)
        poses.append(spr)
    por_pose = QUADROS_ANDAR // len(poses)
    return [pose for pose in poses for _ in range(por_pose)]


# ---------------------------------------------------------------------------
# 10. Retratos da caixa de diálogo
# ---------------------------------------------------------------------------
# Cada rosto da folha de expressões é recortado, reduzido até 80 px de
# altura (cabelo até o ombro) e centrado num quadro de 80 x 80. Os cinco
# usam a mesma paleta, para a pele e o moletom não mudarem de cor entre
# uma fala e outra.

def retratos():
    figuras = {}
    for nome, caixa in RETRATOS.items():
        rgb = abrir_rgb("expressoes.webp", caixa)
        rgb, m = aparar(rgb, mascara_figura(rgb))
        largura = max(1, round(m.shape[1] * TAM_RETRATO / m.shape[0]))
        figuras[nome] = reduzir(rgb, m, min(largura, TAM_RETRATO), TAM_RETRATO)
    paleta = paleta_de(list(figuras.values()), MAX_CORES_RETRATO)
    saida = {}
    for nome, (cor, m) in figuras.items():
        spr = contornar(indexar(cor, m, paleta), paleta)
        quadro = np.full((TAM_RETRATO, TAM_RETRATO), -1, np.int32)
        x0 = (TAM_RETRATO - spr.shape[1]) // 2
        quadro[:, x0:x0 + spr.shape[1]] = spr
        saida[nome] = para_rgba(quadro, paleta)
    return saida


# ---------------------------------------------------------------------------
# 11. Tudo junto
# ---------------------------------------------------------------------------

def folha_referencia(vistas, retratos_rgba, paleta):
    # Folha para conferir: as cinco vistas em cima (em 2x) e os retratos embaixo.
    margem = 8
    largura = margem + len(vistas) * (QUADRO[0] + margem)
    altura = margem + QUADRO[1] + margem + TAM_RETRATO + margem
    folha = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    for i, spr in enumerate(vistas.values()):
        folha.alpha_composite(Image.fromarray(para_rgba(spr, paleta)),
                              (margem + i * (QUADRO[0] + margem), margem))
    for i, rgba in enumerate(retratos_rgba.values()):
        folha.alpha_composite(Image.fromarray(rgba),
                              (margem + i * (TAM_RETRATO + margem), 2 * margem + QUADRO[1]))
    return folha


def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    frente = figura_reduzida("frente.png", RECORTE_FRENTE)
    lado = figura_reduzida("vistas.webp", RECORTE_LADO,
                           cabeca=(QUEIXO_LADO, ESCALA_CABECA_LADO))
    paleta = paleta_de([frente, lado], MAX_CORES)
    contorno = tabela_escura(paleta, 0.42)
    sombra = tabela_escura(paleta, 0.72)

    F_solto = indexar(*frente, paleta)
    F = no_quadro(contornar(F_solto, paleta))
    moldes = moldes_do_parado(frente[0], frente[1], F_solto, paleta)
    L = no_quadro(contornar(indexar(*lado, paleta), paleta))
    B = criar_costas(F, paleta)

    c_lado = camadas_lado(L, paleta)
    pecas = pecas_da_perna(c_lado["pernas"])
    boneco_3q = Boneco3q(POSES_3Q["tres_quartos"], paleta, pecas)
    boneco_3qc = Boneco3q(POSES_3Q["tres_quartos_costas"], paleta, pecas)

    vistas = {
        "lado": L,
        "frente": F,
        "tres_quartos": boneco_3q.quadro(0, paleta, sombra, contorno, andando=False),
        "costas": contorno_final(B, paleta, contorno),
        "tres_quartos_costas": boneco_3qc.quadro(0, paleta, sombra, contorno, andando=False),
    }
    fases_andar = [360 * q / QUADROS_ANDAR for q in range(QUADROS_ANDAR)]
    andar = {
        "lado": [quadro_andar_lado(c_lado, pecas, f, paleta, sombra, contorno) for f in fases_andar],
        "frente": ciclo_desenhado(POSES_ANDAR["frente"], paleta, moldes, contorno),
        "tres_quartos": [boneco_3q.quadro(f, paleta, sombra, contorno) for f in fases_andar],
        "costas": ciclo_desenhado(POSES_ANDAR["costas"], paleta, moldes, contorno),
        "tres_quartos_costas": [boneco_3qc.quadro(f, paleta, sombra, contorno)
                                for f in fases_andar],
    }
    fases_parado = [360 * q / QUADROS_PARADO for q in range(QUADROS_PARADO)]
    for vista, spr in vistas.items():
        salvar(para_rgba(spr, paleta), f"gabriel_{vista}.png")
        tira = np.concatenate([para_rgba(q, paleta) for q in andar[vista]], axis=1)
        salvar(tira, f"gabriel_andar_{vista}.png")
        parado = [contorno_final(quadro_parado(spr, f), paleta, contorno) for f in fases_parado]
        salvar(np.concatenate([para_rgba(q, paleta) for q in parado], axis=1),
               f"gabriel_parado_{vista}.png")
        print(f"{vista}: parado, {QUADROS_ANDAR} quadros andando, {QUADROS_PARADO} respirando")

    rets = retratos()
    for nome, rgba in rets.items():
        salvar(rgba, f"gabriel_retrato_{nome}.png")
        print(f"retrato {nome}")
    folha_referencia(vistas, rets, paleta).save(os.path.join(PASTA_SAIDA, "gabriel_referencia.png"))
    print(f"paleta dos sprites: {len(np.unique(paleta, axis=0))} cores")


if __name__ == "__main__":
    main()
