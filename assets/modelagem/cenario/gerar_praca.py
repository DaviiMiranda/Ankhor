# gerar_praca.py — desenha, por código, o FUNDO DA PRAÇA DE ALIMENTAÇÃO do
# Centro de Convivência (docs/fases/centro_de_convivencia.md): a cúpula de
# vidro, as fachadas dos restaurantes em ARCO e o piso de placas.
#
# Como rodar (Python 3 + numpy + Pillow):
#
#   python assets/modelagem/cenario/gerar_praca.py
#
# O que sai (em assets/sprites/cenario/praca/):
#   fundo_praca.png            2000 x 560 px: a cúpula, as fachadas e o piso,
#                              tudo numa imagem só, porque a sala tem formato
#                              de arco e cada coluna de parede está numa
#                              altura (ver a geometria em gerar_praca_base.py)
#   fundo_praca_luz.png        2000 x 560 px: só os pixels que brilham (neon,
#                              vitrines, frisos), que viram a luz da praça
#                              (ver gerar_praca_base.py)
# Com CATALOGO=1 monta uma folha com as peças. Não commitar.
#
# ---------------------------------------------------------------------------
# O VISUAL DA PRAÇA
# ---------------------------------------------------------------------------
#
# É o Centro de Convivência em 3026: uma praça de alimentação sob uma
# CÚPULA DE VIDRO, de noite. Os painéis de vidro quebraram em vários pontos
# e o céu entra. As fachadas dos restaurantes são de cerâmica clara e grafite,
# com vitrines, toldos e letreiros de neon, cada restaurante de uma cor
# (âmbar, verde, vermelho, magenta). O piso é de placas de pedra escura com
# frisos de luz apagados; no meio, um emblema de anéis. Mato e raízes
# estão voltando pelas frestas: a natureza reconquista a praça.
#
# O fundo é UMA imagem só (e não peças de 80 px) porque o arco muda a altura
# de cada coluna de parede: o piso de uma coluna começa onde a parede dela
# acaba, e uma imagem única garante que as placas, o mato e as rachaduras
# passem de uma coluna para outra sem emenda.

import math
import os

import numpy as np

import gerar_praca_base as base

Imagem, RAMPAS, SOMBRA, dilatar = base.Imagem, base.RAMPAS, base.SOMBRA, base.dilatar
kit = base.kit
ruido = base.ruido
hexa = base.hexa
PECA, Y_PAREDE = base.PECA, base.Y_PAREDE
L = PECA
H = base.ALTURA_PAREDE
LUZ = 0.78


# ---------------------------------------------------------------------------
# Peças de fachada (80 x 112)
# ---------------------------------------------------------------------------


def fachada_base(semente=0):
    """Painéis de cerâmica clara de 40 px com cantos chanfrados, o beiral
    escuro em cima (com o friso de luz apagado) e o rodapé de grafite com
    respiros embaixo. Sujeira escorrendo do beiral e um pouco de mato."""
    img = Imagem(L, H)
    X, Y = img.X, img.Y
    fino = base.ruido_ciclico(L, H, 2, 2, 500 + semente)
    manchas = base.ruido_ciclico(L, H, 40, 16, 501 + semente)
    escorrido = base.ruido_ciclico(L, H, 4, 56, 502 + semente)
    corpo = img.ret(0, 12, L, 100)
    v = (0.50 + 0.2 * manchas + 0.05 * fino - 0.2 * (escorrido > 0.68)) * LUZ
    v -= 0.2 * np.clip((30 - Y) / 18, 0, 1)
    img.pintar(corpo, "ceramica", v)
    # Juntas dos painéis (a cada 40 px) com chanfro claro do lado esquerdo.
    junta = corpo & ((X % 40) == 0)
    img.pintar(junta, "ceramica", v - 0.3, achatar=False)
    img.pintar(corpo & ((X % 40) == 1), "ceramica", v + 0.14, achatar=False)
    img.pintar(corpo & ((X % 40) == 39), "ceramica", v - 0.14, achatar=False)
    # Faixa horizontal de emenda no meio.
    img.pintar(img.ret(0, 60, L, 61), "ceramica", 0.2, achatar=False)
    img.pintar(img.ret(0, 61, L, 62), "ceramica", 0.62 * LUZ, achatar=False)
    # Beiral: grafite com o friso de luz (apagado, azul-escuro) no meio.
    img.pintar(img.ret(0, 0, L, 12), "grafite", 0.32 + 0.1 * fino + 0.14 * (Y == 11))
    img.pintar(img.ret(0, 5, L, 7), "grafite", 0.12)
    img.pintar(img.ret(2, 5, L - 2, 6), "ciano", 0.12, achatar=False)
    # Rodapé de grafite com respiros.
    img.pintar(img.ret(0, 100, L, H), "grafite", 0.26 + 0.08 * fino + 0.14 * (Y == 100))
    for x in range(8, L - 8, 14):
        img.pintar(img.ret(x, 104, x + 8, 109), "grafite", 0.08)
        for y in (105, 107):
            img.pintar(img.ret(x + 1, y, x + 7, y + 1), "grafite", 0.34, achatar=False)
    img.v, img.fino, img.manchas = v, fino, manchas
    return img


def musgo_na_base(img, semente, forca=0.5):
    """Musgo subindo do rodapé, em manchas."""
    rng = np.random.default_rng(semente)
    n = base.ruido_ciclico(L, H, 5, 6, 520 + semente)
    sobe = np.clip((img.Y - 70) / 30, 0, 1) * forca
    mancha = (n + sobe > 0.78) & img.ret(0, 70, L, 100)
    img.pintar(mancha, "verde", 0.3 + 0.4 * img.fino)
    img.pintar(dilatar(mancha) & (img.fino > 0.7) & img.ret(0, 70, L, 100), "verde", 0.6)
    for _ in range(3):
        x0 = int(rng.integers(6, L - 6))
        cipo = img.caminho([(x0 + 2 * math.sin(k * 0.9), 100 - k * 9) for k in range(5)], 0.6)
        img.pintar(cipo & img.ret(0, 50, L, 100), "verde", 0.35 + 0.3 * img.fino)


def rachadura_fachada(img, x_ini, semente):
    base.kit.rachadura(img, x_ini, semente)


def fachada_lisa(semente=0):
    img = fachada_base(semente)
    musgo_na_base(img, semente)
    return img


def fachada_rachada(semente=1):
    img = fachada_base(semente)
    rachadura_fachada(img, 24, 530 + semente)
    rachadura_fachada(img, 58, 531 + semente)
    musgo_na_base(img, semente, 0.7)
    return img


def moldura_neon(img, x0, y0, x1, y1, rampa, valor=0.7, espessura=1):
    """Moldura de neon retangular (o contorno do retângulo)."""
    fora = img.ret(x0, y0, x1, y1)
    dentro = img.ret(x0 + espessura, y0 + espessura, x1 - espessura, y1 - espessura)
    img.pintar(fora & ~dentro, rampa, valor, achatar=False)


def fachada_cartaz(cor="ciano", semente=2):
    """Cartaz holográfico de propaganda: moldura de aço, fundo escuro e
    formas abstratas de comida (um círculo, uma onda e uma faixa) na cor
    do neon. A luz de verdade vem do Godot; aqui só o desenho."""
    img = fachada_base(semente)
    X, Y = img.X, img.Y
    rampa = base.NEON.get(cor, cor)
    img.pintar(img.ret(14, 20, 66, 90), "inox", 0.4 + 0.2 * (Y == 20) + 0.1 * (X == 14))
    tela = img.ret(17, 23, 63, 87)
    img.pintar(tela, "grafite", 0.06 + 0.05 * (Y % 3 == 0))
    img.pintar(img.elipse(40, 46, 13, 13) & tela, rampa, 0.42 + 0.3 * ((X - 40) < 0))
    img.pintar(img.elipse(40, 46, 9, 9) & tela, rampa, 0.18)
    onda = (np.abs(Y + 0.5 - (68 + 4 * np.sin((X - 20) / 3.3))) < 1.2) & (X > 19) & (X < 61)
    img.pintar(onda, rampa, 0.7, achatar=False)
    img.pintar(img.ret(22, 77, 58, 80), rampa, 0.35)
    img.pintar(img.ret(22, 82, 46, 84), rampa, 0.28)
    moldura_neon(img, 17, 23, 63, 87, rampa, 0.38)
    musgo_na_base(img, semente, 0.3)
    return img


def fachada_planta(semente=3):
    """Floreira de pedra com plantas que brilham (bioluminescência) e
    folhagem caindo pela parede."""
    img = fachada_base(semente)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(540 + semente)
    img.pintar(img.ret(10, 82, 70, 100), "grafite", 0.34 + 0.14 * (Y == 82))
    img.pintar(img.ret(10, 82, 11, 100), "grafite", 0.55)
    img.pintar(img.ret(12, 84, 68, 99), "laje", 0.28)
    for k in range(9):
        x0 = 16 + k * 6 + int(rng.integers(-1, 2))
        topo = 52 + int(rng.integers(0, 22))
        talo = img.caminho([(x0, 86), (x0 + rng.uniform(-3, 3), (86 + topo) / 2), (x0 + rng.uniform(-5, 5), topo)], 0.7)
        img.pintar(talo, "verde", 0.4 + 0.2 * rng.random())
        folha = img.elipse(x0 + rng.uniform(-4, 4), topo, rng.uniform(3, 6), rng.uniform(2, 4))
        img.pintar(folha, "bioluz", 0.55 + 0.35 * rng.random())
        img.pintar(img.ret(int(x0), topo - 1, int(x0) + 1, topo), "bioluz", 1.0, achatar=False)
    for x0 in (20, 52):
        cipo = img.caminho([(x0 + 2 * math.sin(k * 0.8), 12 + k * 8) for k in range(7)], 0.6)
        img.pintar(cipo & img.ret(0, 12, L, 82), "verde", 0.3 + 0.3 * img.fino)
    return img


def fachada_canos(semente=4):
    """Canos e eletrodutos expostos, com uma válvula e uma caixa de ligação
    de que sai um facho de faíscas apagado."""
    img = fachada_base(semente)
    X, Y = img.X, img.Y
    for (y0, rampa, esp) in ((26, "inox", 3), (36, "ciano", 2), (46, "inox", 4)):
        cano = img.ret(0, y0, L, y0 + esp)
        img.pintar(cano, rampa, 0.34 + 0.34 * (Y == y0) - 0.12 * (Y == y0 + esp - 1))
        for x in range(6, L, 22):
            img.pintar(img.ret(x, y0 - 1, x + 3, y0 + esp + 1), "inox", 0.62)
    img.pintar(img.ret(46, 24, 60, 56), "inox", 0.28 + 0.2 * (Y == 24))
    img.pintar(img.ret(48, 28, 58, 40), "grafite", 0.08)
    img.cor(img.ret(52, 31, 54, 33), base.hexa("#ff5a3a")[0])
    img.pintar(img.elipse(20, 66, 6, 6), "inox", 0.5 + 0.2 * ((X < 20) & (Y < 66)))
    img.pintar(img.elipse(20, 66, 3, 3), "neon_vermelho", 0.45)
    img.pintar(img.ret(18, 56, 22, 62), "inox", 0.4)
    musgo_na_base(img, semente, 0.5)
    return img


def fachada_painel_solar(semente=5):
    """Painéis de luz da fachada: uma grade de quadrados de vidro leitoso,
    alguns apagados, outros trincados."""
    img = fachada_base(semente)
    X, Y = img.X, img.Y
    rng = np.random.default_rng(550 + semente)
    img.pintar(img.ret(8, 20, 72, 92), "inox", 0.3 + 0.2 * (Y == 20))
    for gy in range(3):
        for gx in range(4):
            x0, y0 = 11 + gx * 15, 23 + gy * 22
            vidro = img.ret(x0, y0, x0 + 13, y0 + 20)
            acesa = rng.random() < 0.18
            img.pintar(vidro, "ciano" if acesa else "gelo", (0.4 if acesa else 0.22) + 0.1 * rng.random())
            img.pintar(vidro & ((X - x0) + (Y - y0) % 11 == 3), "gelo", 0.7, achatar=False)
            if rng.random() < 0.25:
                img.pintar(img.caminho([(x0 + 2, y0 + 1), (x0 + 6, y0 + 9), (x0 + 5, y0 + 18)], 0.5), "grafite", 0.05)
    musgo_na_base(img, semente, 0.4)
    return img


def fachada_nicho(semente=8):
    """Nicho de manutenção: um vão fundo e escuro na fachada, onde cabe uma
    pessoa em pé. As laterais mostram a espessura da parede, o fundo é quase
    preto (um friso de luz ciano apagado no teto) e trepadeiras caem da borda.
    É onde o Gabriel se esconde dos robôs (NichoEsconderijo no Godot)."""
    img = Imagem(L, H)
    X, Y = img.X, img.Y
    img = fachada_base(semente)
    X, Y = img.X, img.Y
    vao = img.ret(18, 26, 62, 112)
    img.pintar(img.ret(14, 22, 66, 112), "ceramica", 0.5 + 0.2 * (Y == 22) + 0.1 * (X == 14))
    prof = np.clip((Y - 26) / 86.0, 0, 1)
    img.pintar(vao, "grafite", 0.04 + 0.05 * prof)
    img.pintar(img.ret(18, 26, 24, 112), "grafite", 0.16 - 0.1 * (X - 18) / 6.0, achatar=False)
    img.pintar(img.ret(56, 26, 62, 112), "grafite", 0.03, achatar=False)
    img.pintar(img.ret(20, 28, 60, 29), "ciano", 0.16, achatar=False)
    img.pintar(img.ret(18, 26, 62, 30), "grafite", 0.02, achatar=False)
    img.pintar(img.ret(30, 90, 50, 112) & (ruido(L, H, 4, 4, 570) > 0.6), "grafite", 0.1, achatar=False)
    for x0 in (20, 54):
        cipo = img.caminho([(x0 + 2 * math.sin(k * 0.9), 22 + k * 7) for k in range(7)], 0.7)
        img.pintar(cipo, "verde", 0.3 + 0.3 * img.fino)
    img.pintar(img.ret(14, 100, 66, 104), "grafite", 0.2)
    return img


# Cor do vidro e do interior de cada restaurante (a vitrine mostra um pouco
# do que há lá dentro): é o que dá identidade à fachada.
def fachada_vitrine(cor="ambar", variante=0, semente=6):
    """Vitrine larga: moldura de aço, vidro escuro com o interior aceso na cor
    do restaurante (luminárias penduradas, uma mesa e um balcão ao fundo),
    reflexo em diagonal, o toldo listrado em cima e o balcão externo."""
    img = fachada_base(semente + variante)
    X, Y = img.X, img.Y
    rampa = base.NEON.get(cor, cor)
    rng = np.random.default_rng(560 + variante)
    # Moldura e vidro.
    img.pintar(img.ret(6, 24, 74, 100), "inox", 0.42 + 0.2 * (Y == 24) + 0.1 * (X == 6) - 0.1 * (X == 73))
    vidro = img.ret(9, 27, 71, 97)
    img.pintar(vidro, "grafite", 0.08)
    # Luz do interior: degradê do teto (mais claro) para o chão.
    prof = np.clip((Y - 27) / 70.0, 0, 1)
    img.pintar(vidro, rampa, 0.14 + 0.2 * (1 - prof) + 0.04 * img.fino)
    # Luminárias penduradas.
    for x in (22, 40, 58):
        img.pintar(img.ret(x, 27, x + 1, 36), "inox", 0.3)
        img.pintar(img.elipse(x + 0.5, 38, 4, 3) & vidro, rampa, 0.95, achatar=False)
        img.pintar(img.ret(x - 6, 36, x + 7, 52) & ((X + Y) % 2 == 0) & vidro, rampa, 0.28 + 0.05 * (x % 3))
    # Balcão ao fundo e mesa com cadeiras (silhuetas escuras).
    img.pintar(img.ret(9, 76, 71, 84) & vidro, "grafite", 0.14 + 0.1 * (Y == 76))
    img.pintar(img.ret(11, 76, 69, 77) & vidro, rampa, 0.5, achatar=False)
    img.pintar(img.ret(14, 86, 34, 90) & vidro, "grafite", 0.05)
    img.pintar(img.ret(18, 90, 20, 97) | img.ret(30, 90, 32, 97), "grafite", 0.05)
    img.pintar(img.ret(46, 84, 62, 88) & vidro, "grafite", 0.05)
    if variante % 2:
        img.pintar(img.elipse(54, 70, 3, 4) & vidro, "grafite", 0.04)
        img.pintar(img.ret(51, 73, 58, 84) & vidro, "grafite", 0.04)
    # Reflexo do vidro em diagonal.
    reflexo = vidro & ((np.abs((X - Y) + 36) < 2) | (np.abs((X - Y) + 22) < 1))
    img.pintar(reflexo, "gelo", 0.55, achatar=False)
    # Toldo listrado (a cor do restaurante e grafite), com franja.
    toldo = img.ret(4, 14, 76, 26)
    listra = ((X // 6) % 2) == 0
    img.pintar(toldo & listra, rampa, 0.46)
    img.pintar(toldo & ~listra, "grafite", 0.2)
    img.pintar(img.ret(4, 14, 76, 15), "inox", 0.6)
    img.pintar(img.ret(4, 24, 76, 26) & ((X % 6) < 4), "grafite", 0.1)
    img.pintar(img.ret(4, 25, 76, 26), rampa, 0.18)
    # Soleira de aço.
    img.pintar(img.ret(4, 97, 76, 101), "inox", 0.5 + 0.2 * (Y == 97))
    musgo_na_base(img, semente + variante, 0.3)
    return img


def espelho(img):
    """A peça virada da esquerda para a direita (as vitrines, que ladeiam a
    porta dos dois lados, ficam simétricas sem desenhar duas vezes)."""
    nova = Imagem(img.w, img.h)
    nova.px = img.px[:, ::-1].copy()
    return nova


def misturar(img, mascara, rgb, alfa):
    """Mistura a cor 'rgb' por cima do que já está desenhado, com opacidade
    'alfa' (0 a 1): é o vidro tingido da cúpula por cima do céu."""
    a = np.broadcast_to(np.asarray(alfa, dtype=float), mascara.shape)[mascara][:, None]
    atual = img.px[mascara][:, :3].astype(float)
    img.px[mascara, :3] = np.clip(atual * (1 - a) + np.asarray(rgb, dtype=float) * a, 0, 255).astype(np.uint8)
    img.px[mascara, 3] = 255


def escurecer(img, mascara, quanto):
    a = np.broadcast_to(np.asarray(quanto, dtype=float), mascara.shape)[mascara][:, None]
    img.px[mascara, :3] = (img.px[mascara][:, :3].astype(float) * (1 - a)).astype(np.uint8)


# ---------------------------------------------------------------------------
# A cúpula de vidro
# ---------------------------------------------------------------------------


def cupula(largura, altura, semente=800):
    """O céu da noite visto por uma cúpula de vidro quebrada.

    As nervuras da cúpula saem de um ponto F bem abaixo da imagem (o centro
    da praça, lá embaixo): cada pixel tem um ângulo (theta) e uma distância
    (r) até F. Uma nervura radial é onde o ângulo está perto de um múltiplo
    de 6 graus (a largura em pixels é |theta - theta_k| * r, que cresce com
    r: por isso as nervuras ficam mais afastadas nas pontas). Os anéis são
    onde r está perto de um múltiplo de 64. Cada retângulo curvo entre duas
    nervuras e dois anéis é um VIDRO, e o sorteio decide se ele ainda está
    inteiro, quebrado (céu aberto) ou coberto de cipó."""
    img = Imagem(largura, altura)
    X, Y = img.X, img.Y
    tudo = img.ret(0, 0, largura, altura)
    noite = np.array(kit.NOITE)
    v = 0.04 + 0.8 * (Y / float(altura)) ** 1.3 + 0.07 * base.ruido_ciclico(largura, altura, 40, 20, semente)
    indice = np.clip(np.floor(v * len(noite) + img.limiar), 0, len(noite) - 1).astype(int)
    img.px[tudo] = noite[indice][tudo]
    rng = np.random.default_rng(semente)
    for _ in range(320):
        ex, ey = int(rng.integers(0, largura)), int(rng.integers(0, altura))
        img.px[ey, ex] = kit.ESTRELA[int(rng.integers(0, 3)) if rng.random() < 0.3 else 0]
    # A lua, atrás do vidro (só aparece onde a fachada deixa o céu à mostra).
    cx, cy = 1795, 92
    dist = np.sqrt((X + 0.5 - cx) ** 2 + (Y + 0.5 - cy) ** 2)
    img.pintar((dist > 22) & (dist < 40), RAMPAS["gelo"], 0.28 * (1 - (dist - 22) / 18.0), achatar=False)
    img.pintar(dist <= 22, RAMPAS["gelo"], 0.86 - 0.12 * ((X - cx) > 6) - 0.1 * ((Y - cy) > 8)
               + 0.06 * base.ruido_ciclico(largura, altura, 4, 4, semente + 1))
    img.pintar(img.elipse(cx - 7, cy - 4, 4, 3), RAMPAS["gelo"], 0.55, achatar=False)
    img.pintar(img.elipse(cx + 6, cy + 7, 3, 2), RAMPAS["gelo"], 0.5, achatar=False)
    # Geometria das nervuras e dos anéis.
    fx, fy = largura / 2.0, altura + 330.0
    dx, dy = X + 0.5 - fx, Y + 0.5 - fy
    r = np.sqrt(dx * dx + dy * dy)
    theta = np.degrees(np.arctan2(dx, -dy))
    passo_angulo, passo_anel = 6.0, 64.0
    k = np.round(theta / passo_angulo)
    sd_nervura = (theta - k * passo_angulo) * np.pi / 180.0 * r
    n = np.round(r / passo_anel)
    sd_anel = r - n * passo_anel
    principal = (k.astype(int) % 4) == 0
    nervura = np.abs(sd_nervura) < np.where(principal, 2.6, 1.6)
    anel = np.abs(sd_anel) < np.where((n.astype(int) % 3) == 0, 2.6, 1.6)
    # O vidro: sorteio por painel (k, n).
    chave = (k.astype(int) * 131 + n.astype(int) * 17 + 7) % 997
    sorteio = ((chave * 2654435761) % 1000) / 1000.0
    fora_da_estrutura = ~(nervura | anel)
    inteiro = fora_da_estrutura & (sorteio > 0.34)
    quebrado = fora_da_estrutura & (sorteio <= 0.34)
    misturar(img, inteiro, (90, 130, 170), 0.16 + 0.05 * (((X + Y) // 3) % 2))
    reflexo = inteiro & (((np.abs((X - Y) % 37 - 6) < 1.2)) | (np.abs((X - Y) % 53 - 20) < 0.8))
    misturar(img, reflexo, (210, 235, 255), 0.30)
    # Cacos de vidro grudados nas nervuras dos painéis quebrados.
    dist_borda = np.minimum(np.abs(sd_nervura), np.abs(sd_anel))
    ruido_caco = base.ruido_ciclico(largura, altura, 8, 8, semente + 2)
    cacos = quebrado & (dist_borda < 3 + 9 * ruido_caco)
    img.pintar(cacos, RAMPAS["gelo"], 0.16 + 0.26 * ruido_caco, achatar=False)
    # Cipós descendo das nervuras principais.
    nuvem = base.ruido_ciclico(largura, altura, 8, 40, semente + 3)
    cipo = fora_da_estrutura & (dist_borda < 14) & (nuvem > 0.72) & (Y > 20)
    img.pintar(cipo, RAMPAS["verde"], 0.3 + 0.35 * base.ruido_ciclico(largura, altura, 2, 2, semente + 4))
    # A estrutura de aço: realce do lado de onde vem a luz (esquerda), sombra do outro.
    estrutura = nervura | anel
    brilho_lado = np.where(nervura, sd_nervura < -0.4, sd_anel < -0.4)
    img.pintar(estrutura, RAMPAS["inox"], 0.30 + 0.16 * brilho_lado + 0.06 * base.ruido_ciclico(largura, altura, 2, 2, semente + 5))
    # Luzinhas de balizamento nas nervuras principais (apagadas: azul bem escuro).
    luz = nervura & principal & (np.abs(((r % 28) - 14)) < 1.2)
    img.pintar(luz, RAMPAS["ciano"], 0.18, achatar=False)
    return img


# ---------------------------------------------------------------------------
# O piso
# ---------------------------------------------------------------------------

LAJE_L, LAJE_A = 40, 16


def mapa_y_base(largura):
    colunas = np.array([base.y_base(c) for c in range(base.COLUNAS_PRACA)])
    return colunas[np.minimum(np.arange(largura) // PECA, base.COLUNAS_PRACA - 1)]


def piso(largura, altura):
    """Placas de pedra escura de 40 x 16 px, em fileiras que se alternam
    (a fileira de baixo começa 20 px adiante), como tijolos. As fileiras e
    as placas são contadas a partir de y = 0 e x = 0 da sala inteira, e não
    de cada coluna: por isso uma coluna continua a vizinha sem emenda, mesmo
    com a parede de cada uma acabando numa altura diferente."""
    img = Imagem(largura, altura)
    X, Y = img.X, img.Y
    ybase = mapa_y_base(largura)[None, :] * np.ones((altura, 1), dtype=int)
    chao = Y >= ybase
    fileira = Y // LAJE_A
    desloc = LAJE_L // 2 * (fileira % 2)
    placa = (X + desloc) // LAJE_L
    sorteio = np.random.default_rng(610).random((fileira.max() + 2, largura // LAJE_L + 3))
    tom = sorteio[fileira, placa]
    fino = base.ruido_ciclico(largura, altura, 2, 2, 611)
    manchas = ruido(largura, altura, 60, 30, 612)
    sujeira = np.clip((Y - ybase) / 22.0, 0, 1)
    valor = (0.34 + 0.22 * tom + 0.16 * manchas + 0.05 * fino) * LUZ - 0.24 * (1 - sujeira)
    img.pintar(chao, "laje", valor)
    junta = chao & (((Y % LAJE_A) == 0) | (((X + desloc) % LAJE_L) == 0))
    img.pintar(junta, "laje", valor - 0.22, achatar=False)
    realce = chao & ((Y % LAJE_A) == 1) & (((X + desloc) % LAJE_L) != 0)
    img.pintar(realce, "laje", valor + 0.09, achatar=False)
    img.cor(chao & (Y == ybase), SOMBRA)
    img.chao, img.ybase, img.fino, img.manchas = chao, ybase, fino, manchas
    return img


def musgo_no_piso(img, semente=620):
    """Manchas de musgo (com plantinhas que brilham) crescendo mais perto das
    paredes, e as folhas secas que o vento trouxe."""
    rng = np.random.default_rng(semente)
    perto = np.clip(1.0 - (img.Y - img.ybase) / 160.0, 0, 1)
    n = ruido(img.w, img.h, 36, 18, semente)
    moita = img.chao & (n + 0.28 * perto > 0.9)
    img.pintar(moita, "verde", 0.28 + 0.4 * img.fino)
    img.pintar(dilatar(moita) & ~moita & img.chao & (img.fino > 0.66), "verde", 0.5)
    pontos = moita & (rng.random((img.h, img.w)) > 0.985)
    img.pintar(pontos, "bioluz", 1.0, achatar=False)
    for _ in range(140):
        x, y = int(rng.integers(2, img.w - 3)), int(rng.integers(120, img.h - 3))
        if img.chao[y, x]:
            rampa = "areia" if rng.random() < 0.6 else "ferrugem"
            img.pintar(img.ret(x, y, x + 2, y + 1), rampa, 0.35 + 0.35 * rng.random())


def rachaduras_no_piso(img, quantas=22, semente=630):
    rng = np.random.default_rng(semente)
    for _ in range(quantas):
        x, y = float(rng.integers(20, img.w - 20)), float(rng.integers(150, img.h - 10))
        angulo = rng.uniform(0, 2 * np.pi)
        pontos = [(x, y)]
        for _ in range(int(rng.integers(5, 11))):
            angulo += rng.uniform(-0.7, 0.7)
            x += np.cos(angulo) * rng.uniform(4, 9)
            y += np.sin(angulo) * rng.uniform(2, 5)
            pontos.append((x, y))
        risco = img.caminho(pontos, 0.5) & img.chao
        img.cor(risco, RAMPAS["laje"][0])
        img.pintar(np.roll(risco, 1, axis=0) & ~risco & img.chao, "laje", 0.52, achatar=False)


def emblema_central(img, cx, cy, rx, ry):
    """O emblema do piso: anéis de pedra clara com friso de luz (apagado), 16
    raios e um disco no meio, onde fica o holograma. Em cada pixel medimos a
    distância normalizada d = raiz(((x - cx)/rx)^2 + ((y - cy)/ry)^2): d = 1
    é a borda da elipse externa, e as faixas são intervalos de d."""
    X, Y = img.X, img.Y
    nx, ny = (X + 0.5 - cx) / rx, (Y + 0.5 - cy) / ry
    d = np.sqrt(nx * nx + ny * ny)
    ang = np.arctan2(ny, nx)
    raios = np.abs(np.sin(8 * ang)) < 0.07
    fino = img.fino
    img.pintar((d <= 1.0) & (d > 0.80) & img.chao, "laje", 0.62 + 0.1 * fino)
    img.pintar((d <= 0.80) & (d > 0.56) & img.chao, "laje", 0.40 + 0.1 * fino)
    img.pintar((d <= 0.56) & (d > 0.22) & img.chao, "laje", 0.54 + 0.1 * fino)
    img.pintar((d <= 0.22) & img.chao, "laje", 0.30)
    img.pintar((d <= 0.80) & (d > 0.22) & raios & img.chao, "laje", 0.30, achatar=False)
    for a, b, v in ((1.0, 0.985, 0.62), (0.80, 0.785, 0.5), (0.56, 0.545, 0.5), (0.22, 0.205, 0.55)):
        faixa = (d <= a) & (d > b) & img.chao
        img.pintar(faixa, "ciano", v * 0.5, achatar=False)
    img.pintar((d <= 0.2) & img.chao & (((X + Y) % 3) == 0), "ciano", 0.28, achatar=False)
    img.pintar((d <= 0.08) & img.chao, "ciano", 0.3)


def trilha_ate_a_porta(img, de, para, largura_de, largura_para, rampa):
    """Uma faixa de piso mais clara, ligando o emblema a uma porta, com uma
    linha tracejada de luz no meio (na cor do restaurante). A faixa é um
    trapézio: larga perto da porta (largura_de) e mais estreita no emblema."""
    (x0, y0), (x1, y1) = de, para
    meio = img.linha(x0, y0, x1, y1, 0.6)
    pontos = [(x0 - largura_de / 2, y0), (x0 + largura_de / 2, y0), (x1 + largura_para / 2, y1), (x1 - largura_para / 2, y1)]
    faixa = img.poligono(pontos) & img.chao
    img.pintar(faixa, "laje", 0.74 + 0.1 * img.fino)
    img.pintar(faixa & ((img.Y % LAJE_A) == 0), "laje", 0.42, achatar=False)
    interior = img.poligono([(x0 - largura_de / 2 + 3, y0), (x0 + largura_de / 2 - 3, y0),
                             (x1 + largura_para / 2 - 2, y1), (x1 - largura_para / 2 + 2, y1)])
    img.pintar(faixa & ~interior, rampa, 0.22, achatar=False)
    tracejado = meio & (((img.X + img.Y) // 5) % 2 == 0) & img.chao
    img.pintar(tracejado, rampa, 0.36, achatar=False)


def cantos_em_degrau(canvas):
    """Onde uma coluna de parede é mais baixa (mais perto) que a vizinha, a
    ponta da fachada aparece de lado: vira uma quina de cerâmica, e o piso do
    vizinho ganha uma sombra rente a ela."""
    for c in range(base.COLUNAS_PRACA - 1):
        a, b = base.y_base(c), base.y_base(c + 1)
        if a == b:
            continue
        baixo = c if a > b else c + 1
        yb_baixo, yb_alto = max(a, b), min(a, b)
        x_quina = (c + 1) * PECA
        lado = -1 if baixo == c else 1
        x_ini = x_quina - 3 if lado < 0 else x_quina
        quina = canvas.ret(x_ini, yb_baixo - H, x_ini + 3, yb_baixo)
        canvas.pintar(quina, "ceramica", 0.32 + 0.1 * ((canvas.X - x_ini) == (0 if lado > 0 else 2)))
        canvas.pintar(quina & (canvas.Y == yb_baixo - 1), "grafite", 0.2)
        x_s = x_quina - 10 if lado > 0 else x_quina
        sombra = canvas.ret(x_s, yb_alto, x_s + 10, yb_baixo)
        gradiente = np.clip(1.0 - np.abs(canvas.X - x_quina) / 10.0, 0, 1)
        escurecer(canvas, sombra, 0.55 * gradiente)


# ---------------------------------------------------------------------------
# A praça montada
# ---------------------------------------------------------------------------

# Qual peça de fachada vai em cada uma das 25 colunas. (peça, True) = peça espelhada.
SEQUENCIA = [
    "fachada_canos", "fachada_cartaz_ciano", "vitrine_loja_2", "PORTA:loja_2", ("vitrine_loja_2", True),
    "fachada_nicho", "vitrine_loja_1", "PORTA:loja_1", ("vitrine_loja_1", True), "fachada_planta",
    "ESCADA:interditada", "fachada_lisa_b", "PORTA:entrada", ("fachada_lisa_b", True),
    "ESCADA:sobe", ("fachada_planta", True), "vitrine_loja_3", "PORTA:loja_3",
    ("vitrine_loja_3", True), ("fachada_nicho", True), "vitrine_loja_4", "PORTA:loja_4",
    ("vitrine_loja_4", True), "fachada_cartaz_ambar", "fachada_rachada",
]


def peca_da_coluna(coluna, pecas, porta_modulo):
    item = SEQUENCIA[coluna]
    espelhar = False
    if isinstance(item, tuple):
        item, espelhar = item
    if item.startswith("ESCADA:"):
        import gerar_andar2
        if item.endswith("interditada"):
            return gerar_andar2.escada(fachada_base(10), "sobe", "FECHADA", interditada=True)
        return gerar_andar2.escada(fachada_base(14), "sobe", "MEZANINO")
    if item.startswith("PORTA:"):
        quem = item.split(":")[1]
        cor = "ciano" if quem == "entrada" else base.COR_LOJA[quem]
        return porta_modulo.peca_de_parede(fachada_base(11 + coluna), cor)
    peca = pecas[item]
    return espelho(peca) if espelhar else peca


def fundo_praca():
    import gerar_porta_restaurante as porta
    pecas = {nome: f() for nome, f in PECAS.items()}
    largura, altura = base.LARGURA_PRACA, base.ALTURA_PRACA
    tela = Imagem(largura, altura)
    tela.colar(cupula(largura, 280), 0, 0)
    for c in range(base.COLUNAS_PRACA):
        tela.colar(peca_da_coluna(c, pecas, porta), c * PECA, base.y_base(c) - H)
    chao = piso(largura, altura)
    musgo_no_piso(chao)
    rachaduras_no_piso(chao)
    cx, cy = largura // 2, 396
    emblema_central(chao, cx, cy, 300, 118)
    for loja, coluna in base.LOJAS_PRACA.items():
        x_porta = coluna * PECA + 41
        y_porta = base.y_base(coluna) + 12
        ponto = (cx + (x_porta - cx) * 0.55, cy + (y_porta - cy) * 0.55)
        trilha_ate_a_porta(chao, (x_porta, y_porta + 4), ponto, 40, 24, base.NEON[base.COR_LOJA[loja]])
    trilha_ate_a_porta(chao, (cx + 1, base.y_base(base.COLUNA_ENTRADA) + 16), (cx, cy - 118), 46, 30, base.NEON["ciano"])
    x_escada = base.COLUNA_ESCADA_PRACA * PECA + 41
    y_escada = base.y_base(base.COLUNA_ESCADA_PRACA) + 16
    ponto = (cx + (x_escada - cx) * 0.55, cy + (y_escada - cy) * 0.55)
    trilha_ate_a_porta(chao, (x_escada, y_escada), ponto, 40, 24, base.NEON["ciano"])
    cheio = chao.chao
    tela.px[cheio] = chao.px[cheio]
    cantos_em_degrau(tela)
    portas = [(c * PECA + 10, base.y_base(c) - H + 24, c * PECA + 70, base.y_base(c)) for c in list(base.LOJAS_PRACA.values()) + [base.COLUNA_ENTRADA]]
    return tela, base.camada_emissiva(tela, portas)


PECAS = {
    "fachada_lisa_a": lambda: fachada_lisa(0),
    "fachada_lisa_b": lambda: fachada_lisa(7),
    "fachada_rachada": fachada_rachada,
    "fachada_cartaz_ciano": lambda: fachada_cartaz("ciano"),
    "fachada_cartaz_ambar": lambda: fachada_cartaz("ambar", 9),
    "fachada_planta": fachada_planta,
    "fachada_canos": fachada_canos,
    "fachada_painel_solar": fachada_painel_solar,
    "fachada_nicho": fachada_nicho,
    "vitrine_loja_1": lambda: fachada_vitrine("ambar", 0),
    "vitrine_loja_2": lambda: fachada_vitrine("verde", 1),
    "vitrine_loja_3": lambda: fachada_vitrine("vermelho", 2),
    "vitrine_loja_4": lambda: fachada_vitrine("magenta", 3),
}


def main():
    print("Gerando as fachadas da praça em", os.path.relpath(base.PASTA_PRACA, base.PASTA_PROJETO))
    pecas = {nome: f() for nome, f in PECAS.items()}
    base.salvar_catalogo("praca_fachadas", list(pecas.items()), 6)
    tela, luz = fundo_praca()
    base.salvar(tela, "fundo_praca.png")
    base.salvar(luz, "fundo_praca_luz.png")


if __name__ == "__main__":
    main()
