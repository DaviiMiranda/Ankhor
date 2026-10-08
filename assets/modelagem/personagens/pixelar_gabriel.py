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
# em pixel art feita à mão) e (4) refazer o contorno de 1 pixel. As vistas
# que não existem na referência (costas e 3/4) e as animações saem das
# vistas que existem, pelos métodos explicados em cada função.

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


def figura_reduzida(nome, caixa, altura=ALTURA_PX):
    rgb = abrir_rgb(nome, caixa)
    rgb, m = aparar(rgb, mascara_figura(rgb))
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
# 6. Vista de frente em camadas, e as costas
# ---------------------------------------------------------------------------
# Linhas do corpo no quadro (iguais na frente, nas costas e no 3/4):
LINHA_QUEIXO = 28     # até aqui é cabeça
LINHA_BAINHA = 63     # última linha do moletom
LINHA_VIRILHA = 73    # daqui para baixo as pernas são separadas
LINHA_JOELHO = 85
LINHA_TORNOZELO = 99  # daqui para baixo é o tênis


def camadas_frente(F, paleta):
    ys, xs = np.mgrid[0:QUADRO[1], 0:QUADRO[0]]
    azul = eh_azul(paleta, F)
    zona_mao = (ys >= LINHA_BAINHA + 1) & (ys <= LINHA_VIRILHA) & ~azul
    mao_e = so(F, zona_mao & (xs <= CENTRO_X - 6))
    mao_d = so(F, zona_mao & (xs >= CENTRO_X + 7))
    mao = (mao_e >= 0) | (mao_d >= 0)
    perna = (F >= 0) & ~mao & ((ys > LINHA_BAINHA) | ((ys >= LINHA_BAINHA - 2) & azul))
    pernas = so(F, perna)
    # O pedaço de calça que a mão tapava: preenchido, para quando a mão sair.
    atras_mao = (mao_e >= 0) | (mao_d >= 0)
    contorno_calca = atras_mao & (xs > CENTRO_X - 10) & (xs < CENTRO_X + 11)
    pernas = preencher(np.where(contorno_calca, 0, pernas), contorno_calca, paleta) \
        if contorno_calca.any() else pernas
    corpo = so(F, ~perna & ~atras_mao)
    return {
        "corpo": corpo,
        "perna_e": so(pernas, xs <= CENTRO_X),
        "perna_d": so(pernas, xs > CENTRO_X),
        "mao_e": mao_e,
        "mao_d": mao_d,
    }


def montar_frente(c):
    return compor(c["perna_e"], c["perna_d"], c["corpo"], c["mao_e"], c["mao_d"])


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
# 7. Vistas de 3/4 (giro de cilindro)
# ---------------------------------------------------------------------------
# A referência só tem frente e lado. Para o 3/4, cada linha do corpo vira a
# fatia de um cilindro de seção elíptica: a meia-largura a vem da frente e a
# meia-profundidade b vem do lado. Um ponto da fatia, no ângulo t (t = 0 é
# o meio da frente, t = -90° é o lado direito dele), fica em
#     X = a·sen t   (para o lado da tela)      Z = b·cos t   (para a câmera)
# Girando o corpo de θ (35° no 3/4), o ponto vai para
#     X' = X·cos θ + Z·sen θ = R·sen(t + α),   R = √((a cos θ)² + (b sen θ)²),
#                                              α = atan2(b sen θ, a cos θ)
# Então, para cada coluna X' da saída, t = asen(X'/R) − α, e a cor vem:
#   da frente, na coluna a·sen t, se o ponto está na metade da frente;
#   do lado,   na coluna b·cos t, se está no lado direito dele (t < −90°).
# Para as costas (θ = 145°) é igual, com a textura das costas no lugar da
# frente (lá a coluna é −a·sen t, porque a imagem das costas é espelhada).
# Pernas e mãos não são cilindros: são camadas que só mudam de lugar (o
# centro de cada uma passa pela mesma conta, na linha do quadril).

def extensao(spr):
    h = spr.shape[0]
    meia, centro, ok = np.zeros(h), np.zeros(h), np.zeros(h, bool)
    for y in range(h):
        xs = np.where(spr[y] >= 0)[0]
        if len(xs):
            meia[y] = (xs.max() - xs.min() + 1) / 2
            centro[y] = (xs.max() + xs.min() + 1) / 2
            ok[y] = True
    return meia, centro, ok


def suavizar(v, ok, raio=2):
    out = v.copy()
    for y in range(len(v)):
        if ok[y]:
            viz = [k for k in range(y - raio, y + raio + 1) if 0 <= k < len(v) and ok[k]]
            out[y] = np.mean(v[viz])
    return out


class Cilindro:
    def __init__(self, textura, lado, graus, de_costas):
        self.th = np.radians(graus)
        self.de_costas = de_costas
        self.a, self.cf, self.okf = extensao(textura)
        self.b, self.cs, self.oks = extensao(lado)
        self.a = suavizar(self.a, self.okf)
        self.b = suavizar(self.b, self.oks)
        self.ref_f = CENTRO_X + 0.5
        self.ref_s = np.median(self.cs[LINHA_JOELHO:LINHA_TORNOZELO])
        # Sinal da coluna da textura: na frente X = a·sen t; nas costas a
        # imagem está espelhada, X = −a·sen t.
        self.sinal = -1 if de_costas else 1

    def linha(self, y):
        A = self.a[y] if self.okf[y] else self.b[y]
        B = self.b[y] if self.oks[y] else self.a[y]
        Cf = self.cf[y] if self.okf[y] else self.ref_f
        Cs = self.cs[y] if self.oks[y] else self.ref_s
        R = np.hypot(A * np.cos(self.th), B * np.sin(self.th))
        al = np.arctan2(B * np.sin(self.th), A * np.cos(self.th))
        centro = CENTRO_X + 0.5 + (Cf - self.ref_f) * self.sinal * np.cos(self.th) \
            + (Cs - self.ref_s) * np.sin(self.th)
        return A, B, Cf, Cs, R, al, centro

    def x_saida(self, y, x_textura):
        A, B, Cf, Cs, R, al, centro = self.linha(y)
        s = np.clip(self.sinal * (x_textura + 0.5 - Cf) / max(A, 1), -1, 1)
        t = np.arcsin(s)
        return centro + R * np.sin(t + al), -A * np.sin(t) * np.sin(self.th) + B * np.cos(t) * np.cos(self.th)

    def girar_linhas(self, textura, lado, y0, y1):
        out = vazio()
        for y in range(y0, y1):
            if not (self.okf[y] or self.oks[y]):
                continue
            A, B, Cf, Cs, R, al, centro = self.linha(y)
            for x in range(QUADRO[0]):
                u = (x + 0.5 - centro) / max(R, 1e-3)
                if abs(u) >= 1:
                    continue
                t = np.arcsin(u) - al
                if self.de_costas:
                    usa_textura = np.cos(t) < 0 or not self.oks[y]
                else:
                    usa_textura = t > -np.pi / 2 or not self.oks[y]
                if usa_textura and self.okf[y]:
                    xi = int(np.floor(Cf + self.sinal * (A - 1.2) * np.sin(t)))
                    fonte = textura
                elif self.oks[y]:
                    xi = int(np.floor(Cs + (B - 1.2) * np.cos(t)))
                    fonte = lado
                else:
                    continue
                if 0 <= xi < QUADRO[0]:
                    out[y, x] = fonte[y, xi]
        # A amostra fica 1 pixel para dentro (sem o contorno da textura,
        # que viraria uma linha suja no meio do corpo); o contorno é
        # refeito depois, na borda nova.
        return out


def virar_cabeca(spr, desloc):
    # A cabeça não passa pelo cilindro (no perfil, a profundidade dela
    # inclui o nariz e o cabelo de trás, e o rosto sairia espremido). Ela
    # mantém a silhueta da frente, e só o miolo anda: o meio do rosto vai
    # desloc pixels para o lado em que ele olha, o lado de lá encolhe e o
    # de cá estica (aparece mais orelha e cabelo). É o que o olho lê como
    # "virou a cabeça".
    out = vazio()
    c = CENTRO_X + 0.5
    for y in range(LINHA_QUEIXO + 1):
        xs = np.where(spr[y] >= 0)[0]
        if not len(xs):
            continue
        esq, dir_ = xs.min(), xs.max() + 1.0
        meio = c + desloc
        for x in range(xs.min(), xs.max() + 1):
            xc = x + 0.5
            if xc < meio:
                src = esq + (xc - esq) * (c - esq) / (meio - esq)
            else:
                src = c + (xc - meio) * (dir_ - c) / (dir_ - meio)
            out[y, x] = spr[y, min(max(int(np.floor(src)), xs.min()), xs.max())]
    return out


def vista_girada(camadas, lado, graus, de_costas):
    textura = camadas["corpo"]
    cil = Cilindro(textura, lado, graus, de_costas)
    corpo = cil.girar_linhas(textura, lado, LINHA_QUEIXO + 1, LINHA_BAINHA + 1)
    cabeca = virar_cabeca(textura, -2 if de_costas else 2)
    corpo = compor(corpo, mover(cabeca, 1, 0))
    novas = {"corpo": corpo}
    profundidade = {}
    for nome in ("perna_e", "perna_d", "mao_e", "mao_d"):
        spr = camadas[nome]
        ys, xs = np.where(spr >= 0)
        y_ref = LINHA_BAINHA - 2
        x_novo, z = cil.x_saida(y_ref, xs.mean())
        novas[nome] = mover(spr, int(round(x_novo - 0.5 - xs.mean())), 0)
        profundidade[nome] = z
    novas["ordem_pernas"] = sorted(("perna_e", "perna_d"), key=lambda n: profundidade[n])
    novas["ordem_maos"] = sorted(("mao_e", "mao_d"), key=lambda n: profundidade[n])
    return novas


def montar(c):
    ordem_p = c.get("ordem_pernas", ("perna_e", "perna_d"))
    ordem_m = c.get("ordem_maos", ("mao_e", "mao_d"))
    return compor(c[ordem_p[0]], c[ordem_p[1]], c["corpo"], c[ordem_m[0]], c[ordem_m[1]])


# ---------------------------------------------------------------------------
# 8. Vista de lado em camadas (boneco recortado)
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
LEVANTA_PE = 5      # quanto o pé sobe na vista de frente, em pixels
DESCE_CORPO = 2     # quanto o corpo desce com as pernas abertas
BALANCO = 1         # quanto o corpo balança para os lados, de frente


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
    quadro = compor(meio, braco_perto)
    return contorno_final(assentar(quadro), paleta, contorno)


def inclinar(perna, desloc):
    # A perna anda para o lado a partir da virilha: nada no quadril (que
    # fica preso ao corpo), o deslocamento inteiro do joelho para baixo.
    out = vazio()
    for y in range(QUADRO[1]):
        k = np.clip((y - (LINHA_VIRILHA - 6)) / (LINHA_JOELHO - LINHA_VIRILHA + 6), 0, 1)
        dx = int(round(desloc * k))
        linha = perna[y]
        if dx > 0:
            out[y, dx:] = linha[:-dx]
        elif dx < 0:
            out[y, :dx] = linha[-dx:]
        else:
            out[y] = linha
    return out


def quadro_andar_frente(c, fase, paleta, contorno, passo_lateral=0):
    # De frente (e de costas, e de 3/4) a perna não gira: a que vem para a
    # frente no ar encolhe (o pé sobe LEVANTA_PE pixels, dobrando o
    # joelho), e o corpo desce e balança para o lado do pé que está no chão.
    # No 3/4 a perna também anda passo_lateral pixels para o lado.
    phi = np.radians(fase)
    desce = int(round(DESCE_CORPO * np.sin(phi) ** 2))
    balanca = int(round(BALANCO * np.sin(phi)))
    novas = dict(c)
    for nome, desloc in (("perna_e", 0), ("perna_d", 180)):
        p_ = np.radians(fase + desloc)
        sobe = int(round(LEVANTA_PE * max(0.0, np.cos(p_)) ** 1.5))
        perna = remapear_linhas(c[nome], [
            (LINHA_BAINHA - 8, LINHA_BAINHA - 8 + desce),
            (LINHA_JOELHO - 4, LINHA_JOELHO - 4 + desce),
            (LINHA_TORNOZELO, LINHA_TORNOZELO - sobe),
            (QUADRO[1] - 1, QUADRO[1] - 1 - sobe)])
        novas[nome] = inclinar(perna, passo_lateral * np.sin(p_))
    for nome in ("corpo", "mao_e", "mao_d"):
        novas[nome] = mover(c[nome], balanca, desce)
    quadro = montar(novas)
    return contorno_final(quadro, paleta, contorno)


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
    lado = figura_reduzida("vistas.webp", RECORTE_LADO)
    paleta = paleta_de([frente, lado], MAX_CORES)
    contorno = tabela_escura(paleta, 0.42)
    sombra = tabela_escura(paleta, 0.72)

    F = no_quadro(contornar(indexar(*frente, paleta), paleta))
    L = no_quadro(contornar(indexar(*lado, paleta), paleta))
    B = criar_costas(F, paleta)

    c_frente = camadas_frente(F, paleta)
    c_costas = camadas_frente(B, paleta)
    c_3q = vista_girada(c_frente, L, 35, False)
    c_3qc = vista_girada(c_costas, L, 145, True)
    c_lado = camadas_lado(L, paleta)
    pecas = pecas_da_perna(c_lado["pernas"])

    vistas = {
        "lado": L,
        "frente": F,
        "tres_quartos": contorno_final(montar(c_3q), paleta, contorno),
        "costas": contorno_final(B, paleta, contorno),
        "tres_quartos_costas": contorno_final(montar(c_3qc), paleta, contorno),
    }
    fases_andar = [360 * q / QUADROS_ANDAR for q in range(QUADROS_ANDAR)]
    andar = {
        "lado": [quadro_andar_lado(c_lado, pecas, f, paleta, sombra, contorno) for f in fases_andar],
        "frente": [quadro_andar_frente(c_frente, f, paleta, contorno) for f in fases_andar],
        "tres_quartos": [quadro_andar_frente(c_3q, f, paleta, contorno, 2) for f in fases_andar],
        "costas": [quadro_andar_frente(c_costas, f, paleta, contorno) for f in fases_andar],
        "tres_quartos_costas": [quadro_andar_frente(c_3qc, f, paleta, contorno, 2)
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
