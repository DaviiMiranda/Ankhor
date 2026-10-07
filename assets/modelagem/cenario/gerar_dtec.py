# gerar_dtec.py — desenha, por código, o KIT DO DTEC: as peças de parede,
# de chão e os objetos do laboratório de tecnologia (docs/fases/dtec.md).
# Mesmo estilo e mesmas medidas do kit do bunker (gerar_bunker.py), que este
# script importa: paleta, dithering, contorno, peças de 80 px de parede e
# 128 px de chão.
#
# Como rodar (Python 3 + numpy):
#
#   python assets/modelagem/cenario/gerar_dtec.py
#
# O que sai (em assets/sprites/cenario/dtec/):
#   paredes/<peça>.png   80 x 112 px: um pedaço da parede do fundo (encaixa lado a lado)
#   paredes/pilar_dtec.png  16 x 112 px: a coluna das pontas
#   paredes/dtec_lateral.png  16 x 64 px: a parede do lado da sala funda
#   chao/<peça>.png      128 x 68 px: um pedaço do chão
#   chao/<peça>_fundo.png  128 x 64 px: o chão da parte sul das salas fundas
#   objetos/<objeto>.png objetos que o Gabriel contorna (y-sort); o "pé" de
#                        cada um sai no terminal, como no gerar_bunker.py
# Com CATALOGO=1 monta folhas com o nome de cada peça nesta pasta. Não commitar.
#
# ---------------------------------------------------------------------------
# O VISUAL DO DTEC
# ---------------------------------------------------------------------------
#
# O DTEC é um departamento de tecnologia: laboratórios, servidores e, no
# meio, a sala de uma máquina grande. Foi fechado e lacrado, por isso está
# mais inteiro que a Biblioteca; mas são mil anos de poeira. O que conta isso:
#   - parede clara de LABORATÓRIO: painel cinza em cima e AZULEJO branco
#     embaixo (grade de 10 px), com a FAIXA AZUL do DTEC entre os dois;
#     alguns azulejos caíram (onde o ruído passa do limite) e a poeira
#     escurece a parte de cima;
#   - no teto, o DUTO de ventilação de aço com rebites e grelhas;
#   - vidro e aço: janelas de laboratório, bancadas, racks;
#   - a natureza entrando pelas rachaduras (poucas folhas verdes);
#   - a máquina do salão central: um anel enorme em pé em volta de um
#     núcleo CIANO que brilha. O brilho de verdade vem das PointLight2D da
#     cena; aqui só pintamos os pixels mais claros da rampa "ciano".
#
# Tudo encaixa sem emenda pelo mesmo truque do kit: ruído cíclico (a grade
# de números sorteados dá a volta na largura da peça) e juntas na coluna 0.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_DTEC = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "dtec")
CATALOGO = os.environ.get("CATALOGO", "")

_spec = importlib.util.spec_from_file_location("gerar_bunker", os.path.join(PASTA_SCRIPT, "gerar_bunker.py"))
bunker = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bunker)
kit = bunker.kit
bib = kit.bib

Imagem, RAMPAS, SOMBRA, dilatar = bib.Imagem, bib.RAMPAS, bib.SOMBRA, bib.dilatar
ciclico = kit.ruido_ciclico
ruido = bib.ruido
listras = bunker.listras
L = 80                 # largura da peça de parede
Y_CHAO = kit.Y_CHAO    # 112
ALTURA = kit.ALTURA    # 180
LUZ = kit.LUZ

# Rampas novas do DTEC (do mais escuro ao mais claro). Entram no mesmo
# dicionário de rampas, então o pintar() já sabe usar.
RAMPAS.update({
    "azulejo": bib.hexa("#1a1d21", "#262a2f", "#353a40", "#464c52", "#5a6067", "#70777d", "#888f94", "#a3a9ac"),
    "dtec": bib.hexa("#0b1626", "#12233b", "#1a3352", "#24466c", "#2f5a88", "#3d71a6"),
    "epoxi": bib.hexa("#15181a", "#1f2326", "#2a2f32", "#363c3f", "#444a4d", "#53595b", "#646a6b"),
    "ciano": bib.hexa("#0d3a44", "#13606e", "#1b8c9b", "#2bbccb", "#62e3ee", "#b6fbff", "#effeff"),
    "tela_verde": bib.hexa("#0b1a10", "#12301a", "#1d4d29", "#2d7a3e", "#4fb865", "#98f0a8"),
})
LED_VERDE, LED_VERMELHO, LED_AMBAR = bunker.LED_VERDE, bunker.LED_VERMELHO, bunker.LED_AMBAR
LED_AZUL = bib.hexa("#7fd8ff")[0]

# ---------------------------------------------------------------------------
# Paredes
# ---------------------------------------------------------------------------


def parede_base(semente=0):
    img = Imagem(L, Y_CHAO)
    X, Y = img.X, img.Y
    fino = ciclico(L, Y_CHAO, 2, 2, 300)
    manchas = ciclico(L, Y_CHAO, 40, 16, 301 + semente)
    poeira = ciclico(L, Y_CHAO, 8, 40, 302 + semente)
    # Painel de cima: cinza, mais escuro perto do teto (poeira e sombra do duto).
    painel = img.ret(0, 20, L, 56)
    v = (0.42 + 0.14 * manchas + 0.05 * fino - 0.1 * (poeira > 0.7)) * LUZ - 0.14 * np.clip((34 - Y) / 14, 0, 1)
    img.pintar(painel, "azulejo", v)
    img.pintar(painel & ((X == 0) | (X == 40)), "azulejo", v - 0.18, achatar=False)
    # Faixa azul do DTEC, com um filete claro em cima.
    img.pintar(img.ret(0, 56, L, 61), "dtec", 0.62 + 0.08 * fino)
    img.pintar(img.ret(0, 56, L, 57), "dtec", 0.95)
    # Azulejos de 10 px: rejunte escuro e, onde o ruído passa do limite,
    # azulejo que caiu (aparece o reboco escuro com a borda quebrada).
    azulejos = img.ret(0, 61, L, 100)
    caiu = (ciclico(L, Y_CHAO, 10, 4, 303 + semente) > 0.9) & azulejos
    caiu &= ((X % 10) != 0) & (((Y - 61) % 10) != 0)
    img.pintar(azulejos, "azulejo", (0.66 + 0.1 * manchas + 0.04 * fino) * LUZ)
    rejunte = azulejos & (((X % 10) == 0) | (((Y - 61) % 10) == 0))
    img.pintar(rejunte, "azulejo", 0.24, achatar=False)
    img.pintar(caiu, "concreto", 0.18 + 0.06 * fino)
    img.pintar(dilatar(caiu) & ~caiu & azulejos & ~rejunte, "azulejo", 0.36, achatar=False)
    # Rodapé de aço escovado.
    img.pintar(img.ret(0, 100, L, Y_CHAO), "aco", 0.2 + 0.05 * fino + 0.18 * (Y == 100))
    # Laje do teto e o duto de ventilação com rebites e grelha.
    img.pintar(img.ret(0, 0, L, 10), "concreto", 0.08 + 0.05 * fino + 0.1 * (Y == 9))
    img.pintar(img.ret(0, 10, L, 20), "aco", 0.36 + 0.22 * (Y == 10) - 0.14 * (Y == 19))
    img.pintar(img.ret(0, 10, L, 20) & (X == 0), "aco", 0.15, achatar=False)
    for x in (6, 34, 46, 74):
        img.pintar(img.ret(x, 12, x + 1, 13) | img.ret(x, 17, x + 1, 18), "aco", 0.7)
    for x in range(14, 27, 2):
        img.pintar(img.ret(x, 13, x + 1, 18), "aco", 0.12)
    img.v, img.fino, img.manchas = v, fino, manchas
    return img


def plaquinha(img, x0, x1, y0=28):
    """Placa azul em cima da porta: o nome da sala entra por cima, no Godot
    (Label), para cada porta ter o seu sem desenhar uma peça nova."""
    img.pintar(img.ret(x0, y0, x1, y0 + 9), "dtec", 0.25)
    img.pintar(img.ret(x0, y0, x1, y0 + 1), "dtec", 0.6)
    for x in (x0 + 1, x1 - 2):
        img.pintar(img.ret(x, y0 + 4, x + 1, y0 + 5), "aco", 0.7)


def batente(img, xa, xb, ya):
    """Batente de aço fino, com o leitor de cartão do lado direito."""
    img.pintar(img.ret(xa - 3, ya - 3, xb + 3, Y_CHAO), "aco", 0.42 + 0.05 * img.fino)
    img.pintar(img.ret(xa - 3, ya - 3, xb + 3, ya - 2), "aco", 0.68)
    img.pintar(img.ret(xa - 3, ya - 3, xa - 2, Y_CHAO), "aco", 0.6)


def leitor(img, x, y, led):
    """Leitor de cartão com teclado: caixinha escura, teclas e o LED."""
    img.pintar(img.ret(x, y, x + 6, y + 10), "aco", 0.14)
    img.pintar(img.ret(x, y, x + 6, y + 1), "aco", 0.5)
    for yy in (y + 4, y + 6, y + 8):
        img.pintar(img.ret(x + 1, yy, x + 5, yy + 1) & ((img.X % 2) == 1), "aco", 0.55)
    img.cor(img.ret(x + 2, y + 2, x + 4, y + 3), led)


def folha_fechada(img, xa, xb, ya):
    """Duas folhas de porta de correr fechadas, com visor de vidro fosco e a
    faixa azul do DTEC atravessando."""
    meio = (xa + xb) // 2
    folha = img.ret(xa, ya, xb, Y_CHAO)
    img.pintar(folha, "azulejo", 0.5 + 0.06 * img.manchas)
    img.pintar(img.ret(meio, ya, meio + 1, Y_CHAO), "aco", 0.15)
    for x0 in (xa + 4, meio + 4):
        img.pintar(img.ret(x0, ya + 6, x0 + 13, ya + 26), "vidro", 0.35 + 0.15 * ((img.X + img.Y) % 9 == 0))
    img.pintar(img.ret(xa, ya + 34, xb, ya + 38), "dtec", 0.6)


def dtec_lisa():
    return parede_base()


def dtec_rachada():
    """Rachadura grande, azulejos caídos em cascata e mato entrando pela
    fresta: mil anos de abandono mesmo num prédio lacrado."""
    img = parede_base(1)
    X, Y = img.X, img.Y
    kit.rachadura(img, 34, 310)
    kit.rachadura(img, 50, 311)
    buraco = (np.abs(X - 42 - 3 * np.sin(Y / 6)) < 9 - np.abs(Y - 80) / 4) & (Y > 64) & (Y < 98)
    img.pintar(buraco, "concreto", 0.12 + 0.06 * img.fino)
    img.pintar(dilatar(buraco) & ~buraco & (Y > 61) & (Y < 100), "azulejo", 0.3, achatar=False)
    for (cx, cy) in ((38, 70), (44, 66), (47, 74), (36, 79), (42, 84), (49, 81)):
        img.pintar(img.elipse(cx, cy, 2.5, 1.6), "verde", 0.55 + 0.25 * (img.Y < cy))
    img.pintar(img.caminho([(42, 98), (41, 88), (43, 78), (42, 68)], 0.5), "verde", 0.35)
    return img


def dtec_luminaria():
    """Painel de luz fluorescente embutido no forro, embaixo do duto. No
    Godot, uma PointLight2D fria que pisca (LuzTremula)."""
    img = parede_base(2)
    img.pintar(img.ret(12, 20, 68, 25), "aco", 0.4 + 0.2 * (img.Y == 20))
    img.pintar(img.ret(14, 21, 66, 24), "fluorescente", 0.85)
    img.pintar(img.ret(14, 22, 66, 23), "fluorescente", 1.0)
    for x in range(20, 64, 8):
        img.pintar(img.ret(x, 21, x + 1, 24), "aco", 0.35)
    return img


def dtec_porta():
    """Porta de correr aberta: as folhas entraram na parede e sobrou o vão
    escuro. O leitor de cartão está com o LED verde (liberada)."""
    img = parede_base(3)
    xa, xb, ya = 20, 62, 44
    batente(img, xa, xb, ya)
    vao = img.ret(xa, ya, xb, Y_CHAO)
    prof = (img.Y - ya) / (Y_CHAO - ya)
    img.pintar(vao, "concreto", 0.04 + 0.08 * prof)
    img.cor(img.ret(xa, ya, xb, ya + 2), SOMBRA)
    plaquinha(img, 24, 58)
    leitor(img, 67, 66, LED_VERDE)
    return img


def dtec_porta_trancada():
    """Porta fechada e TRANCADA: o leitor está com o LED vermelho. É a porta
    que o notebook consegue hackear (Porta.trancada no Godot)."""
    img = parede_base(4)
    xa, xb, ya = 20, 62, 44
    batente(img, xa, xb, ya)
    folha_fechada(img, xa, xb, ya)
    plaquinha(img, 24, 58)
    leitor(img, 67, 66, LED_VERMELHO)
    img.pintar(img.ret(xa + 15, ya + 42, xb - 15, ya + 50), "vermelho", 0.45)
    img.pintar(img.ret(xa + 16, ya + 43, xb - 16, ya + 49), "vermelho", 0.65)
    return img


def dtec_porta_lacrada():
    """Porta fechada e LACRADA de vez: fita amarela e preta em X, placa de
    acesso restrito e o leitor apagado. É a porta das salas que nunca abrem
    (Porta.bloqueada no Godot)."""
    img = parede_base(5)
    X, Y = img.X, img.Y
    xa, xb, ya = 20, 62, 44
    batente(img, xa, xb, ya)
    folha_fechada(img, xa, xb, ya)
    plaquinha(img, 24, 58)
    for (a, b) in (((16, 50), (66, 104)), ((66, 50), (16, 104))):
        fita = img.linha(a[0], a[1], b[0], b[1], 1.6)
        listra = ((X + Y) // 3) % 2 == 0
        img.pintar(fita & listra, "amarelo", 0.8)
        img.pintar(fita & ~listra, "aco", 0.05)
    img.pintar(img.ret(29, 60, 53, 70), "vermelho", 0.55)
    img.pintar(img.ret(30, 61, 52, 69), "branco", 0.85)
    img.pintar(img.ret(32, 64, 50, 66), "vermelho", 0.6)
    leitor(img, 67, 66, bib.hexa("#2a2c30")[0])
    return img


def dtec_porta_central():
    """A entrada do salão da máquina: porta larga aberta, faixas de perigo
    no batente e a luz ciano da máquina vazando do vão."""
    img = parede_base(6)
    X, Y = img.X, img.Y
    xa, xb, ya = 14, 66, 38
    img.pintar(img.ret(xa - 5, ya - 5, xb + 5, Y_CHAO), "aco", 0.4 + 0.05 * img.fino)
    listras(img, img.ret(xa - 5, ya - 5, xb + 5, ya - 1) | img.ret(xa - 5, ya - 1, xa - 1, Y_CHAO)
            | img.ret(xb + 1, ya - 1, xb + 5, Y_CHAO), 3)
    vao = img.ret(xa, ya, xb, Y_CHAO)
    prof = (Y - ya) / (Y_CHAO - ya)
    brilho = np.clip(1 - np.abs(X - 40) / 26, 0, 1) * np.clip((Y - ya) / 30, 0, 1)
    img.pintar(vao, "ciano", 0.05 + 0.32 * brilho * (1 - 0.4 * prof))
    img.cor(img.ret(xa, ya, xb, ya + 2), SOMBRA)
    img.pintar(img.ret(xa, Y_CHAO - 3, xb, Y_CHAO), "ciano", 0.55)
    plaquinha(img, 22, 58, 26)
    return img


def dtec_vidro():
    """Janela de laboratório: vidro escuro com bancadas e equipamentos lá
    dentro, um monitor ainda aceso e o reflexo em diagonal."""
    img = parede_base(7)
    X, Y = img.X, img.Y
    img.pintar(img.ret(6, 26, 74, 84), "aco", 0.48 + 0.2 * (Y == 26))
    vidro = img.ret(9, 29, 71, 81)
    img.pintar(vidro, "vidro", 0.18 + 0.2 * (Y - 29) / 52)
    img.pintar(img.ret(12, 62, 68, 65) & vidro, "vidro", 0.45)
    img.pintar(img.ret(14, 65, 16, 81) | img.ret(64, 65, 66, 81), "vidro", 0.08)
    img.pintar(img.ret(20, 50, 32, 61), "vidro", 0.05)
    img.pintar(img.ret(21, 51, 31, 59), "tela_verde", 0.45 + 0.2 * ((Y % 3) == 0))
    for x in (42, 48, 52):
        img.pintar(img.ret(x, 54, x + 3, 62), "vidro", 0.55)
    img.pintar(img.ret(56, 40, 66, 62), "vidro", 0.1)
    for y in range(43, 60, 4):
        img.cor(img.ret(58, y, 59, y + 1), LED_VERDE if y % 8 else LED_AMBAR)
    reflexo = vidro & ((np.abs((X - Y) + 2) < 2) | (np.abs((X - Y) + 16) < 1))
    img.pintar(reflexo, "vidro", 0.95, achatar=False)
    img.pintar(img.ret(6, 84, 74, 87), "aco", 0.6)
    return img


def dtec_quadro():
    """Quadro branco com o que sobrou da última aula: um grafo (nós e
    arestas), uma onda e contas apagadas pela metade."""
    img = parede_base(8)
    X, Y = img.X, img.Y
    img.pintar(img.ret(5, 27, 75, 77), "aco", 0.55 + 0.15 * (Y == 27))
    quadro = img.ret(7, 29, 73, 75)
    img.pintar(quadro, "azulejo", 0.86 - 0.12 * ruido(L, Y_CHAO, 12, 8, 320) - 0.08 * ((X + 2 * Y) % 11 == 0))
    nos = [(16, 38), (30, 34), (26, 50), (42, 44), (18, 62)]
    for a, b in ((0, 1), (1, 2), (0, 2), (2, 3), (1, 3), (2, 4)):
        img.pintar(img.linha(*nos[a], *nos[b], 0.5), "dtec", 0.55)
    for (x, y) in nos:
        img.pintar(img.elipse(x, y, 2.4, 2.4), "vermelho", 0.6)
    onda = (np.abs(Y + 0.5 - (58 + 5 * np.sin((X - 46) / 3.2))) < 0.7) & (X > 46) & (X < 70)
    img.pintar(onda, "vermelho", 0.5)
    for y in (34, 38, 42):
        img.pintar(img.ret(50, y, 50 + (y * 7) % 18, y + 1) & ((X % 3) != 0), "dtec", 0.35)
    img.pintar(img.ret(10, 75, 70, 77), "aco", 0.45)
    img.pintar(img.ret(20, 74, 26, 75) | img.ret(30, 74, 34, 75), "vermelho", 0.5)
    return img


def dtec_painel():
    """Painel de controle na parede: telinhas verdes, chaves, mostradores e
    fileiras de LEDs."""
    img = parede_base(9)
    X, Y = img.X, img.Y
    img.pintar(img.ret(10, 30, 70, 90), "aco", 0.3 + 0.1 * (Y == 30) + 0.04 * img.fino)
    img.pintar(img.ret(10, 30, 11, 90), "aco", 0.5)
    for x0 in (14, 42):
        img.pintar(img.ret(x0, 34, x0 + 24, 50), "aco", 0.08)
        img.pintar(img.ret(x0 + 1, 35, x0 + 23, 49), "tela_verde", 0.3 + 0.25 * ((Y % 3) == 0))
    onda = (np.abs(Y + 0.5 - (42 + 4 * np.sin(X / 2.5))) < 0.6) & (X > 15) & (X < 37)
    img.pintar(onda, "tela_verde", 0.95, achatar=False)
    for k, x in enumerate(range(44, 64, 3)):
        img.pintar(img.ret(x, 47 - (k * 5) % 10, x + 2, 48), "tela_verde", 0.9)
    for (cx, cy) in ((20, 62), (34, 62)):
        img.pintar(img.elipse(cx, cy, 5, 5), "branco", 0.7)
        img.pintar(img.linha(cx, cy, cx + 3, cy - 2, 0.5), "vermelho", 0.7)
    for x in range(44, 66, 4):
        img.pintar(img.ret(x, 58, x + 2, 66), "aco", 0.6)
        img.pintar(img.ret(x, 58 + (x % 3) * 2, x + 2, 61 + (x % 3) * 2), "branco", 0.8)
    for x in range(14, 66, 3):
        img.cor(img.ret(x, 76, x + 1, 77), (LED_VERDE, LED_AMBAR, LED_AZUL)[(x // 3) % 3])
        img.cor(img.ret(x, 81, x + 1, 82), LED_VERDE if (x * 7) % 5 else LED_VERMELHO)
    return img


def dtec_armario():
    """Armário de parede com portas de vidro: pastas, caixas de peças e
    manuais encadernados."""
    img = parede_base(10)
    X, Y = img.X, img.Y
    img.pintar(img.ret(6, 24, 74, 58), "azulejo", 0.6 + 0.12 * (Y == 24))
    img.pintar(img.ret(8, 26, 72, 56), "azulejo", 0.22)
    rng = np.random.default_rng(330)
    for y0 in (27, 42):
        img.pintar(img.ret(8, y0 + 13, 72, y0 + 15), "azulejo", 0.55)
        x = 9
        while x < 70:
            larg = int(rng.integers(2, 5))
            alt = int(rng.integers(8, 13))
            rampa = ("dtec", "vermelho", "amarelo", "branco", "tinta")[int(rng.integers(0, 5))]
            img.pintar(img.ret(x, y0 + 13 - alt, x + larg, y0 + 13), rampa, 0.4 + 0.2 * (X == x))
            x += larg + int(rng.integers(0, 3))
    img.pintar(img.ret(39, 24, 41, 58), "azulejo", 0.6)
    reflexo = img.ret(8, 26, 72, 56) & (np.abs((X - Y) % 20 - 4) < 1)
    img.pintar(reflexo, "vidro", 0.85, achatar=False)
    return img


def dtec_cartaz():
    """Mural de avisos: o triângulo amarelo de risco elétrico, uma folha de
    escala de horários e papéis presos com tachinhas."""
    img = parede_base(11)
    X, Y = img.X, img.Y
    img.pintar(img.ret(8, 28, 46, 70), "madeira", 0.4 + 0.08 * img.fino)
    for (x0, y0, x1, y1) in ((11, 31, 25, 47), (27, 33, 43, 45), (13, 50, 29, 67), (31, 48, 44, 66)):
        img.pintar(img.ret(x0, y0, x1, y1), "papel", 0.75)
        for yy in range(y0 + 3, y1 - 2, 3):
            img.pintar(img.ret(x0 + 2, yy, x1 - 2, yy + 1) & ((X % 4) != 0), "papel", 0.3)
        img.pintar(img.ret((x0 + x1) // 2, y0, (x0 + x1) // 2 + 1, y0 + 1), "vermelho", 0.7)
    tri = img.poligono([(62, 32), (73, 52), (51, 52)])
    img.pintar(tri, "amarelo", 0.8)
    img.pintar(tri & ~img.poligono([(62, 36), (70, 50), (54, 50)]), "aco", 0.05)
    img.pintar(img.caminho([(63, 38), (60, 44), (64, 44), (61, 50)], 0.6), "aco", 0.05)
    return img


def dtec_terminal():
    """Terminal de parede ainda ligado: tela ciano com linhas de texto e a
    prateleira do teclado."""
    img = parede_base(12)
    X, Y = img.X, img.Y
    img.pintar(img.ret(22, 32, 58, 62), "aco", 0.3 + 0.2 * (Y == 32))
    img.pintar(img.ret(25, 35, 55, 58), "ciano", 0.12)
    for k, y in enumerate(range(38, 56, 3)):
        larg = (11, 24, 17, 27, 9, 20)[k % 6]
        img.pintar(img.ret(27, y, 27 + larg, y + 1) & ((X % 5) != 3), "ciano", 0.75)
    img.pintar(img.ret(27, 53, 29, 55), "ciano", 0.95)
    img.pintar(img.ret(18, 66, 62, 70), "aco", 0.45 + 0.2 * (Y == 66))
    img.pintar(img.ret(22, 67, 58, 69) & ((X % 3) != 0), "azulejo", 0.7)
    img.pintar(img.ret(38, 62, 42, 66), "aco", 0.25)
    return img


def dtec_extintor():
    """Extintor vermelho no suporte, a placa de emergência e o hidrante de
    mangueira enrolada."""
    img = parede_base(13)
    X, Y = img.X, img.Y
    img.pintar(img.ret(16, 66, 26, 92), "vermelho", 0.6 + 0.25 * (X == 17))
    img.pintar(img.ret(18, 61, 24, 66), "aco", 0.4)
    img.pintar(img.caminho([(24, 62), (28, 64), (27, 76)], 0.6), "aco", 0.2)
    img.pintar(img.ret(14, 44, 28, 56), "vermelho", 0.45)
    img.pintar(img.ret(19, 47, 23, 53), "branco", 0.85)
    img.pintar(img.ret(40, 46, 70, 88), "vermelho", 0.38 + 0.1 * (Y == 46))
    img.pintar(img.ret(42, 48, 68, 86), "vidro", 0.2)
    mangueira = img.elipse(55, 67, 10, 10) & ~img.elipse(55, 67, 4, 4)
    img.pintar(mangueira, "branco", 0.5 + 0.2 * (((X + Y) % 4) < 2))
    return img


def dtec_canos():
    """Linhas de gás do laboratório: três canos coloridos (azul, amarelo e
    verde) com registros, que encaixam de uma peça para a outra."""
    img = parede_base(14)
    X, Y = img.X, img.Y
    for (ya, rampa) in ((26, "dtec"), (31, "amarelo"), (36, "tela_verde")):
        img.pintar(img.ret(0, ya, L, ya + 3), rampa, 0.5 + 0.3 * (Y == ya))
        for xf in (0, 40):
            img.pintar(img.ret(xf, ya - 1, xf + 2, ya + 4), "aco", 0.55)
    img.pintar(img.ret(58, 39, 61, 92), "amarelo", 0.45 + 0.3 * (X == 58))
    img.pintar(img.ret(55, 70, 64, 73), "aco", 0.4)
    img.pintar(img.elipse(59.5, 66, 4, 4) & ~img.elipse(59.5, 66, 2, 2), "vermelho", 0.65)
    img.pintar(img.ret(52, 90, 67, 96), "aco", 0.3)
    return img


def dtec_tela_grande():
    """Telão da sala de controle: o gráfico da máquina (uma onda que cresce)
    e o esquema do anel em volta do núcleo."""
    img = parede_base(15)
    X, Y = img.X, img.Y
    img.pintar(img.ret(4, 26, 76, 76), "aco", 0.15 + 0.15 * (Y == 26))
    tela = img.ret(6, 28, 74, 74)
    img.pintar(tela, "ciano", 0.08 + 0.05 * ((Y % 3) == 0))
    img.pintar(tela & (((X - 6) % 10 == 0) | ((Y - 28) % 10 == 0)), "ciano", 0.2, achatar=False)
    amp = 2 + (X - 6) / 8
    onda = (np.abs(Y + 0.5 - (44 - amp * np.sin((X - 6) / 2.2))) < 0.7) & (X > 6) & (X < 44)
    img.pintar(onda, "ciano", 0.85, achatar=False)
    anel = img.elipse(60, 50, 10, 13) & ~img.elipse(60, 50, 8, 11)
    img.pintar(anel, "ciano", 0.7)
    img.pintar(img.elipse(60, 50, 3, 3), "ciano", 1.0)
    for y in (62, 66, 70):
        img.pintar(img.ret(10, y, 10 + (y * 5) % 28, y + 1) & ((X % 4) != 0), "ciano", 0.5)
    return img


PAREDES = {
    "dtec_lisa": dtec_lisa,
    "dtec_rachada": dtec_rachada,
    "dtec_luminaria": dtec_luminaria,
    "dtec_porta": dtec_porta,
    "dtec_porta_trancada": dtec_porta_trancada,
    "dtec_porta_lacrada": dtec_porta_lacrada,
    "dtec_porta_central": dtec_porta_central,
    "dtec_vidro": dtec_vidro,
    "dtec_quadro": dtec_quadro,
    "dtec_painel": dtec_painel,
    "dtec_armario": dtec_armario,
    "dtec_cartaz": dtec_cartaz,
    "dtec_terminal": dtec_terminal,
    "dtec_extintor": dtec_extintor,
    "dtec_canos": dtec_canos,
    "dtec_tela_grande": dtec_tela_grande,
}


def pilar_dtec():
    """Coluna branca das pontas da sala, com a faixa azul e o rodapé de aço."""
    img = Imagem(16, Y_CHAO)
    X, Y = img.X, img.Y
    img.pintar(img.ret(0, 10, 16, Y_CHAO), "azulejo", 0.55 + 0.05 * ciclico(16, Y_CHAO, 2, 2, 340))
    img.pintar(img.ret(0, 10, 3, Y_CHAO), "azulejo", 0.75)
    img.pintar(img.ret(12, 10, 16, Y_CHAO), "azulejo", 0.35)
    img.pintar(img.ret(0, 0, 16, 10), "concreto", 0.12)
    img.pintar(img.ret(0, 56, 16, 61), "dtec", 0.62)
    img.pintar(img.ret(0, 100, 16, Y_CHAO), "aco", 0.25)
    return img


def dtec_lateral():
    """A parede do lado, vista de cima: o topo da parede de azulejo com o
    filete azul e a face escura virada para a sala. Para o lado esquerdo; o
    direito é a mesma peça espelhada."""
    img = Imagem(16, kit.ALTURA_FUNDO)
    X, Y = img.X, img.Y
    fino = kit.ruido_ciclico_2d(img.w, img.h, 2, 2, 350)
    img.pintar(img.ret(0, 0, 9, img.h), "azulejo", 0.5 + 0.06 * fino)
    img.pintar(img.ret(7, 0, 9, img.h), "dtec", 0.55)
    img.pintar(img.ret(9, 0, 13, img.h), "azulejo", 0.28 + 0.05 * fino)
    img.cor(img.ret(13, 0, 16, img.h) & ((X + Y) % 2 == 0), SOMBRA)
    img.cor(img.ret(13, 0, 14, img.h), SOMBRA)
    return img


# ---------------------------------------------------------------------------
# Chão
# ---------------------------------------------------------------------------


def chao_base(semente=0):
    """Piso de epóxi cinza-claro em placas de 32 px que seguem a perspectiva
    (as fileiras da Biblioteca, de duas em duas), com poeira acumulada rente
    à parede e marcas de arrasto."""
    img = Imagem(128, ALTURA)
    X, Y = img.X, img.Y
    chao = img.ret(0, Y_CHAO, 128, ALTURA)
    fino = ciclico(128, ALTURA, 2, 2, 360)
    manchas = ciclico(128, ALTURA, 32, 10, 361 + semente)
    poeira = np.clip((126 - Y) / 14, 0, 1)
    valor = (0.5 + 0.12 * manchas + 0.05 * fino) * LUZ - 0.18 * poeira
    img.pintar(chao, "epoxi", valor)
    juntas = np.zeros(chao.shape, dtype=bool)
    for ya in bib.FILEIRAS[2::2]:
        juntas |= Y == ya
    juntas |= (X % 32 == 0) & (Y > Y_CHAO + 2)
    img.pintar(chao & juntas, "epoxi", valor - 0.16, achatar=False)
    img.cor(img.ret(0, Y_CHAO, 128, Y_CHAO + 1), SOMBRA)
    img.chao, img.fino, img.manchas = chao, fino, manchas
    return img


def chao_dtec():
    img = chao_base()
    arrasto = (np.abs(img.Y - 150 - 0.08 * img.X) < 1) & (img.X > 20) & (img.X < 90)
    img.pintar(arrasto, "epoxi", 0.25, achatar=False)
    return img


def chao_dtec_cabos():
    """Feixe de cabos atravessando o chão (do lado de uma máquina para o
    outro), com a canaleta de borracha."""
    img = chao_base(1)
    X, Y = img.X, img.Y
    img.pintar(img.ret(0, 140, 128, 150), "aco", 0.12 + 0.05 * img.fino)
    for k, (rampa, tom) in enumerate((("aco", 0.3), ("vermelho", 0.35), ("dtec", 0.45), ("aco", 0.5))):
        ys = 142 + 2 * k + 1.2 * np.sin(2 * np.pi * (X + 9 * k) / 64)
        img.pintar((np.abs(Y + 0.5 - ys) < 0.8) & img.chao, rampa, tom, achatar=False)
    return img


def chao_dtec_elevado():
    """Piso elevado da sala dos servidores: placas perfuradas para o ar frio
    subir, uma fileira de furos em cada placa."""
    img = chao_base(2)
    X, Y = img.X, img.Y
    placa = img.ret(0, 118, 128, ALTURA)
    img.pintar(placa, "aco", 0.42 + 0.05 * img.manchas)
    for i in range(len(bib.FILEIRAS) - 1):
        ya, yb = bib.FILEIRAS[i], bib.FILEIRAS[i + 1]
        if yb <= 118:
            continue
        faixa = (Y >= ya) & (Y < yb)
        furos = faixa & ((X % 4) == 1) & ((Y % 3) == 1) & ((X % 32) > 4) & ((X % 32) < 28)
        img.pintar(furos & placa, "aco", 0.1)
        img.pintar(faixa & (Y == ya) & placa, "aco", 0.65)
    img.pintar(placa & (X % 32 == 0), "aco", 0.65)
    return img


def chao_dtec_faixa():
    """Faixa de perigo pintada no chão, em volta da máquina."""
    img = chao_base(3)
    faixa = img.ret(0, 124, 128, 140)
    listras(img, faixa, 6, 1, 0.65)
    return img


def fundo_base(semente=0):
    """Epóxi do fundo, com juntas a cada 32 px: y local 8 continua a junta
    da peça normal, e 64 = 2 x 32 faz a peça repetir para baixo."""
    img = Imagem(128, kit.ALTURA_FUNDO)
    X, Y = img.X, img.Y
    fino = kit.ruido_ciclico_2d(img.w, img.h, 2, 2, 360)
    manchas = kit.ruido_ciclico_2d(img.w, img.h, 32, 16, 361 + semente)
    valor = (0.5 + 0.12 * manchas + 0.05 * fino) * LUZ
    tudo = img.ret(0, 0, img.w, img.h)
    img.pintar(tudo, "epoxi", valor)
    juntas = ((Y % 32) == 8) | (X % 32 == 0)
    img.pintar(tudo & juntas, "epoxi", valor - 0.16, achatar=False)
    img.chao, img.fino, img.manchas = tudo, fino, manchas
    return img


def chao_dtec_fundo():
    return fundo_base()


def chao_dtec_elevado_fundo():
    img = fundo_base(2)
    X, Y = img.X, img.Y
    img.pintar(img.chao, "aco", 0.42 + 0.05 * img.manchas)
    furos = ((X % 4) == 1) & ((Y % 3) == 1) & ((X % 32) > 4) & ((X % 32) < 28) & ((Y % 32) > 10) & ((Y % 32) < 30)
    img.pintar(furos, "aco", 0.1)
    img.pintar(((Y % 32) == 8) | (X % 32 == 0), "aco", 0.65)
    return img


def chao_dtec_cabos_fundo():
    """Cabos soltos no chão do fundo, serpenteando (a peça repete para baixo:
    o seno usa o período da altura da peça)."""
    img = fundo_base(1)
    X, Y = img.X, img.Y
    for k, (rampa, tom) in enumerate((("aco", 0.3), ("vermelho", 0.35), ("dtec", 0.45))):
        xs = 40 + 30 * k + 6 * np.sin(2 * np.pi * (Y + 11 * k) / img.h)
        img.pintar(np.abs(X + 0.5 - xs) < 0.9, rampa, tom, achatar=False)
    return img


def chao_dtec_faixa_fundo():
    img = fundo_base(3)
    faixa = img.ret(0, 24, 128, 40)
    listras(img, faixa, 6, 1, 0.65)
    return img


CHAOS = {
    "chao_dtec": chao_dtec,
    "chao_dtec_cabos": chao_dtec_cabos,
    "chao_dtec_elevado": chao_dtec_elevado,
    "chao_dtec_faixa": chao_dtec_faixa,
}

CHAOS_FUNDO = {
    "chao_dtec_fundo": chao_dtec_fundo,
    "chao_dtec_elevado_fundo": chao_dtec_elevado_fundo,
    "chao_dtec_cabos_fundo": chao_dtec_cabos_fundo,
    "chao_dtec_faixa_fundo": chao_dtec_faixa_fundo,
}

# ---------------------------------------------------------------------------
# Objetos: cada função devolve (imagem, x_do_pé, y_do_pé), como no bunker.
# A PEGADA é o retângulo de colisão no chão (largura, altura), em px.
# ---------------------------------------------------------------------------


def bancada_lab():
    """Bancada de laboratório: tampo branco, gaveteiros, um microscópio,
    béqueres com líquido colorido e um monitor apagado."""
    img = Imagem(72, 40)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 18, 70, 22), "azulejo", 0.75 + 0.2 * (Y == 18))
    img.pintar(img.ret(4, 22, 68, 38), "azulejo", 0.42)
    for x0 in (6, 38):
        img.pintar(img.ret(x0, 24, x0 + 28, 37), "azulejo", 0.5 + 0.15 * (Y == 24))
        for y in (28, 33):
            img.pintar(img.ret(x0 + 11, y, x0 + 17, y + 1), "aco", 0.7)
    img.pintar(img.ret(8, 6, 12, 18) | img.ret(6, 14, 16, 18) | img.ret(10, 3, 16, 7), "aco", 0.4 + 0.2 * (X == 8))
    img.pintar(img.ret(14, 7, 18, 9), "aco", 0.65)
    for (x, alt, rampa) in ((24, 7, "dtec"), (29, 5, "vermelho"), (33, 8, "tela_verde")):
        img.pintar(img.ret(x, 18 - alt, x + 4, 18), "vidro", 0.6)
        img.pintar(img.ret(x, 18 - alt // 2, x + 4, 18), rampa, 0.6)
    img.pintar(img.ret(46, 2, 66, 15), "aco", 0.2)
    img.pintar(img.ret(48, 4, 64, 13), "vidro", 0.15 + 0.25 * ((X - Y) % 9 == 0))
    img.pintar(img.ret(54, 15, 58, 18), "aco", 0.3)
    img.contornar()
    return img, 36, 38


def bancada_eletronica():
    """Bancada de eletrônica: osciloscópio com a onda verde, estação de
    solda, placas de circuito e um carretel de fio."""
    img = Imagem(72, 40)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 18, 70, 22), "madeira", 0.45 + 0.2 * (Y == 18))
    img.pintar(img.ret(4, 22, 7, 38) | img.ret(65, 22, 68, 38), "aco", 0.35)
    img.pintar(img.ret(7, 30, 65, 32), "aco", 0.3)
    img.pintar(img.ret(6, 3, 30, 18), "aco", 0.32 + 0.2 * (Y == 3))
    img.pintar(img.ret(8, 5, 22, 15), "tela_verde", 0.25)
    onda = (np.abs(Y + 0.5 - (10 + 3 * np.sin((X - 8) / 1.8))) < 0.6) & (X > 8) & (X < 22)
    img.pintar(onda, "tela_verde", 0.95, achatar=False)
    for y in (6, 10, 14):
        img.pintar(img.elipse(26, y + 0.5, 1.5, 1.5), "branco", 0.6)
    img.pintar(img.ret(34, 12, 44, 18), "aco", 0.25)
    img.cor(img.ret(36, 14, 37, 15), LED_VERMELHO)
    img.pintar(img.caminho([(42, 12), (46, 6), (50, 9)], 0.6), "aco", 0.5)
    for (x0, y0) in ((50, 14), (57, 15)):
        img.pintar(img.ret(x0, y0, x0 + 8, y0 + 4), "tela_verde", 0.35)
        img.cor(img.ret(x0 + 2, y0 + 1, x0 + 4, y0 + 2), RAMPAS["aco"][6])
    img.pintar(img.elipse(64, 14, 3.5, 3.5), "vermelho", 0.55)
    img.pintar(img.elipse(64, 14, 1.2, 1.2), "aco", 0.4)
    img.contornar()
    return img, 36, 38


def mesa_computador():
    """Mesa com um computador de 3026: monitor fino ainda aceso (fraco),
    teclado e uma caneca."""
    img = Imagem(52, 36)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 16, 50, 19), "azulejo", 0.6 + 0.2 * (Y == 16))
    img.pintar(img.ret(4, 19, 7, 34) | img.ret(45, 19, 48, 34), "aco", 0.35)
    img.pintar(img.ret(30, 19, 45, 30), "azulejo", 0.4)
    img.pintar(img.ret(12, 1, 36, 14), "aco", 0.15)
    img.pintar(img.ret(13, 2, 35, 13), "ciano", 0.15 + 0.1 * ((Y % 3) == 0))
    for y in (4, 7, 10):
        img.pintar(img.ret(15, y, 15 + (y * 3) % 17, y + 1), "ciano", 0.45)
    img.pintar(img.ret(23, 14, 25, 16), "aco", 0.3)
    img.pintar(img.ret(14, 15, 34, 16) & ((X % 2) == 0), "aco", 0.6)
    img.pintar(img.ret(40, 11, 44, 16), "vermelho", 0.5)
    img.contornar()
    return img, 26, 34


def cadeira_escritorio():
    """Cadeira de rodinhas, com o encosto alto."""
    img = Imagem(18, 26)
    X, Y = img.X, img.Y
    img.pintar(img.ret(4, 1, 14, 13), "dtec", 0.3 + 0.15 * (X == 4))
    img.pintar(img.ret(3, 13, 15, 16), "dtec", 0.4)
    img.pintar(img.ret(8, 16, 10, 22), "aco", 0.4)
    img.pintar(img.ret(2, 22, 16, 23), "aco", 0.35)
    for x in (2, 9, 15):
        img.pintar(img.ret(x, 23, x + 2, 25), "aco", 0.15)
    img.contornar()
    return img, 9, 24


def rack_dtec():
    """Rack de servidores alto, com a porta de grade e os LEDs piscando
    (no Godot não pisca; a luz verde vem de uma PointLight2D)."""
    img = Imagem(26, 56)
    X, Y = img.X, img.Y
    img.pintar(img.ret(1, 1, 25, 55), "aco", 0.18 + 0.2 * (X == 1) + 0.15 * (Y == 1))
    img.pintar(img.ret(3, 4, 23, 52), "aco", 0.08)
    for y in range(5, 51, 5):
        img.pintar(img.ret(4, y, 22, y + 4), "aco", 0.25 + 0.1 * (Y == y))
        for x in range(6, 20, 3):
            if (x * 5 + y) % 7 < 4:
                img.cor(img.ret(x, y + 1, x + 1, y + 2), (LED_VERDE, LED_AZUL, LED_AMBAR)[(x + y) % 3])
    grade = img.ret(3, 4, 23, 52) & (((X + Y) % 4) == 0)
    img.pintar(grade, "aco", 0.35, achatar=False)
    img.pintar(img.ret(2, 53, 24, 55), "aco", 0.3)
    img.contornar()
    return img, 13, 54


def armario_quimico():
    """Armário de reagentes com portas de vidro: frascos coloridos nas
    prateleiras e o losango de produto inflamável."""
    img = Imagem(36, 54)
    X, Y = img.X, img.Y
    img.pintar(img.ret(1, 1, 35, 53), "azulejo", 0.55 + 0.2 * (X == 1))
    img.pintar(img.ret(3, 4, 33, 40), "vidro", 0.2)
    for y0 in (14, 26, 38):
        img.pintar(img.ret(3, y0, 33, y0 + 2), "azulejo", 0.7)
        for k, x in enumerate(range(5, 31, 5)):
            rampa = ("vermelho", "dtec", "amarelo", "tela_verde", "branco", "ciano")[(k + y0) % 6]
            alt = 5 + (k * 3 + y0) % 5
            img.pintar(img.ret(x, y0 - alt, x + 3, y0), "vidro", 0.55)
            img.pintar(img.ret(x, y0 - alt // 2, x + 3, y0), rampa, 0.6)
    img.pintar(img.ret(17, 4, 19, 40), "azulejo", 0.55)
    reflexo = img.ret(3, 4, 33, 40) & (np.abs((X - Y) % 16 - 3) < 1)
    img.pintar(reflexo, "vidro", 0.9, achatar=False)
    img.pintar(img.ret(3, 42, 33, 52), "azulejo", 0.42)
    losango = np.abs(X - 18) + np.abs(Y - 47) < 5
    img.pintar(losango, "vermelho", 0.6)
    img.contornar()
    return img, 18, 52


def capela():
    """Capela de exaustão: um gabinete alto com o vidro de correr meio
    aberto, a lâmpada interna e o duto subindo."""
    img = Imagem(50, 64)
    X, Y = img.X, img.Y
    img.pintar(img.ret(20, 0, 30, 8), "aco", 0.35 + 0.2 * (X == 20))
    img.pintar(img.ret(2, 8, 48, 62), "azulejo", 0.58 + 0.2 * (X == 2) + 0.1 * (Y == 8))
    img.pintar(img.ret(6, 14, 44, 40), "azulejo", 0.2)
    img.pintar(img.ret(6, 14, 44, 16), "fluorescente", 0.85)
    img.pintar(img.ret(6, 16, 44, 30), "vidro", 0.35 + 0.15 * ((X - Y) % 11 == 0))
    img.pintar(img.ret(6, 30, 44, 31), "aco", 0.6)
    img.pintar(img.ret(12, 34, 16, 40), "vidro", 0.6)
    img.pintar(img.ret(12, 37, 16, 40), "tela_verde", 0.6)
    img.pintar(img.ret(6, 40, 44, 43), "azulejo", 0.75)
    img.pintar(img.ret(6, 45, 44, 60), "azulejo", 0.45)
    img.pintar(img.ret(24, 50, 26, 52), "aco", 0.7)
    img.contornar()
    return img, 25, 62


def cilindros():
    """Três cilindros de gás presos por corrente: verde, azul e cinza."""
    img = Imagem(28, 48)
    X, Y = img.X, img.Y
    for k, (x0, rampa) in enumerate(((2, "tela_verde"), (10, "dtec"), (18, "aco"))):
        img.pintar(img.ret(x0, 8 + k % 2 * 2, x0 + 8, 46), rampa, 0.45 + 0.25 * (X == x0 + 1))
        img.pintar(img.elipse(x0 + 4, 9 + k % 2 * 2, 4, 3), rampa, 0.55)
        img.pintar(img.ret(x0 + 3, 3 + k % 2 * 2, x0 + 5, 8 + k % 2 * 2), "aco", 0.6)
    img.pintar(img.caminho([(1, 24), (14, 26), (27, 24)], 0.6) & ((X % 3) != 0), "aco", 0.65)
    img.contornar()
    return img, 14, 46


def braco_robotico():
    """Braço robótico industrial amarelo na base, parado no meio de um
    movimento, com a garra aberta."""
    img = Imagem(46, 52)
    X, Y = img.X, img.Y
    img.pintar(img.ret(6, 42, 30, 50), "aco", 0.3 + 0.2 * (Y == 42))
    img.pintar(img.ret(12, 34, 24, 42), "amarelo", 0.5 + 0.2 * (X == 12))
    img.pintar(img.linha(18, 36, 14, 16, 3.2), "amarelo", 0.55)
    img.pintar(img.elipse(14, 16, 4, 4), "aco", 0.4)
    img.pintar(img.linha(14, 16, 36, 10, 2.6), "amarelo", 0.62)
    img.pintar(img.elipse(36, 10, 3, 3), "aco", 0.45)
    img.pintar(img.caminho([(36, 10), (42, 6), (44, 9)], 0.8), "aco", 0.55)
    img.pintar(img.caminho([(36, 10), (42, 14), (44, 11)], 0.8), "aco", 0.55)
    img.pintar(img.caminho([(24, 38), (32, 44), (40, 49)], 0.6), "aco", 0.2)
    img.contornar()
    return img, 18, 50


def robo_desmontado():
    """Mesa de manutenção com um robô aberto: a cabeça com o olho apagado,
    o tronco sem tampa e fios saindo. Ninguém sabe se ele ainda liga."""
    img = Imagem(64, 38)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 20, 62, 24), "aco", 0.42 + 0.2 * (Y == 20))
    img.pintar(img.ret(5, 24, 8, 36) | img.ret(56, 24, 59, 36), "aco", 0.32)
    img.pintar(img.ret(14, 8, 38, 20), "metal", 0.45 + 0.15 * (Y == 8))
    img.pintar(img.ret(18, 11, 34, 19), "metal", 0.15)
    for x in range(19, 34, 3):
        img.pintar(img.ret(x, 12, x + 2, 18), "tela_verde", 0.25 + 0.2 * (x % 2))
    img.pintar(img.caminho([(26, 18), (30, 23), (34, 26)], 0.6), "vermelho", 0.5)
    img.pintar(img.caminho([(22, 18), (20, 24), (16, 30)], 0.6), "dtec", 0.55)
    img.pintar(img.elipse(48, 13, 8, 7), "metal", 0.5 + 0.2 * (Y < 11))
    img.pintar(img.elipse(50, 13, 3, 2), "vermelho", 0.15)
    img.pintar(img.ret(40, 18, 46, 20), "metal", 0.35)
    img.pintar(img.ret(6, 15, 12, 20), "metal", 0.35)
    img.contornar()
    return img, 32, 36


def console():
    """Console da sala de controle, inclinado: duas telas, teclados e
    fileiras de botões."""
    img = Imagem(64, 36)
    X, Y = img.X, img.Y
    img.pintar(img.poligono([(2, 18), (62, 18), (58, 34), (6, 34)]), "aco", 0.3 + 0.12 * (Y == 18))
    img.pintar(img.poligono([(4, 8), (60, 8), (62, 18), (2, 18)]), "aco", 0.42)
    for x0 in (8, 36):
        img.pintar(img.ret(x0, 0, x0 + 20, 9), "aco", 0.15)
        img.pintar(img.ret(x0 + 1, 1, x0 + 19, 8), "ciano", 0.2 + 0.1 * ((Y % 2) == 0))
        img.pintar(img.ret(x0 + 3, 4, x0 + 3 + (x0 % 11), 5), "ciano", 0.75)
    for x in range(6, 58, 3):
        img.cor(img.ret(x, 12, x + 2, 13), (LED_VERDE, LED_AMBAR, LED_AZUL, LED_VERMELHO)[(x // 3) % 4])
        img.pintar(img.ret(x, 15, x + 2, 16), "branco", 0.55)
    img.contornar()
    return img, 32, 34


def planta():
    """Um vaso de escritório onde a planta não morreu: cresceu mil anos e
    tomou o canto (a natureza entrando no prédio lacrado)."""
    img = Imagem(30, 40)
    X, Y = img.X, img.Y
    img.pintar(img.poligono([(9, 28), (21, 28), (19, 38), (11, 38)]), "dtec", 0.4 + 0.2 * (X < 12))
    rng = np.random.default_rng(370)
    for _ in range(26):
        cx, cy = rng.uniform(4, 26), rng.uniform(2, 26)
        img.pintar(img.elipse(cx, cy, rng.uniform(2, 4), rng.uniform(1.2, 2)), "verde", 0.4 + 0.3 * rng.random())
    img.pintar(img.caminho([(15, 28), (14, 18), (10, 10)], 0.5) | img.caminho([(15, 28), (19, 14)], 0.5), "casca", 0.4)
    img.contornar()
    return img, 15, 38


def balcao_recepcao():
    """Balcão da recepção do DTEC: frente azul com o nome em relevo (o texto
    entra no Godot, se precisar), tampo claro e um monitor."""
    img = Imagem(100, 38)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 10, 98, 14), "azulejo", 0.75 + 0.2 * (Y == 10))
    img.pintar(img.ret(4, 14, 96, 36), "dtec", 0.35 + 0.08 * ruido(100, 38, 10, 6, 380))
    img.pintar(img.ret(4, 22, 96, 24), "dtec", 0.75)
    for x in range(10, 92, 20):
        img.pintar(img.ret(x, 26, x + 12, 33), "dtec", 0.22)
    img.pintar(img.ret(64, 0, 84, 10), "aco", 0.15)
    img.pintar(img.ret(65, 1, 83, 9), "vidro", 0.2)
    img.pintar(img.ret(20, 7, 34, 10), "papel", 0.6)
    img.contornar()
    return img, 50, 36


def catraca():
    """Catraca de entrada: hoje é peça de museu. A haste ficou travada."""
    img = Imagem(26, 30)
    X, Y = img.X, img.Y
    img.pintar(img.ret(4, 6, 16, 28), "aco", 0.4 + 0.25 * (X == 4) + 0.1 * (Y == 6))
    img.pintar(img.ret(6, 9, 14, 13), "vidro", 0.3)
    img.cor(img.ret(9, 10, 11, 12), LED_VERMELHO)
    for (a, b) in (((16, 14), (25, 12)), ((16, 16), (24, 20)), ((16, 18), (20, 26))):
        img.pintar(img.linha(a[0], a[1], b[0], b[1], 0.8), "aco", 0.65)
    img.contornar()
    return img, 10, 28


def maquina():
    """A MÁQUINA do salão central: uma plataforma em degraus, duas torres com
    bobinas de cobre, um anel enorme em pé e, no meio do anel, o núcleo
    ciano brilhando, com arcos de energia saltando até o anel.

    O anel é a diferença de duas elipses (de fora menos de dentro). Para
    dar volume, o tom de cada pixel do anel depende do ângulo em volta do
    centro: atan2(dy, dx) dá o ângulo, e o cosseno do ângulo menos 135°
    (luz vindo de cima à esquerda) clareia um lado e escurece o outro.

    O núcleo é uma esfera: o tom cai do centro para a borda (1 - d²), e
    os arcos de energia são passeios aleatórios do núcleo até o anel."""
    W, H = 176, 156
    img = Imagem(W, H)
    X, Y = img.X, img.Y
    cx, cy = 88, 66
    # Plataforma em três degraus, com faixa de perigo na borda de cima.
    for k, (x0, x1, y0) in enumerate(((10, 166, 138), (22, 154, 128), (34, 142, 120))):
        degrau = img.ret(x0, y0, x1, y0 + 10 if k else H - 2)
        img.pintar(degrau, "aco", 0.3 + 0.1 * k + 0.25 * (Y == y0))
        listras(img, img.ret(x0, y0, x1, y0 + 2), 4)
    # Duas torres com bobinas de cobre (faixas alternadas) e luz no topo.
    for tx in (30, 134):
        img.pintar(img.ret(tx, 22, tx + 12, 122), "aco", 0.32 + 0.22 * (X == tx) - 0.1 * (X == tx + 11))
        for y in range(30, 116, 6):
            img.pintar(img.ret(tx - 2, y, tx + 14, y + 3), "ferrugem", 0.6 + 0.2 * (Y == y))
        img.pintar(img.ret(tx - 3, 16, tx + 15, 22), "aco", 0.5)
        img.pintar(img.elipse(tx + 6, 13, 5, 4), "ciano", 0.8)
    # O anel em pé.
    dx, dy = X + 0.5 - cx, Y + 0.5 - cy
    anel = img.elipse(cx, cy, 52, 58) & ~img.elipse(cx, cy, 40, 46)
    angulo = np.arctan2(dy, dx)
    volume = 0.5 + 0.3 * np.cos(angulo - np.radians(-135))
    img.pintar(anel, "aco", volume)
    trilha = img.elipse(cx, cy, 47, 53) & ~img.elipse(cx, cy, 45, 51)
    img.pintar(trilha, "ciano", 0.55 + 0.25 * ((np.degrees(angulo) // 15) % 2))
    for graus in range(0, 360, 45):
        a = np.radians(graus)
        bx, by = cx + 49 * np.cos(a), cy + 55 * np.sin(a)
        img.pintar(img.elipse(bx, by, 4, 4), "aco", 0.7)
    # Suporte do anel até a plataforma.
    img.pintar(img.poligono([(cx - 14, 118), (cx + 14, 118), (cx + 6, 120), (cx - 6, 120)]), "aco", 0.5)
    img.pintar(img.ret(cx - 6, 108, cx + 6, 120), "aco", 0.4)
    # O núcleo: esfera ciano, mais clara no centro, com um halo pontilhado.
    d2 = (dx / 18) ** 2 + (dy / 18) ** 2
    halo = (d2 <= 1.8) & (d2 > 1.0) & (((X + Y) % 2) == 0)
    img.pintar(halo, "ciano", 0.45)
    nucleo = d2 <= 1.0
    img.pintar(nucleo, "ciano", 0.55 + 0.45 * (1 - d2) + 0.15 * ((dx < 0) & (dy < 0)))
    # Arcos de energia: passeios aleatórios do núcleo até o anel.
    rng = np.random.default_rng(390)
    for graus in (20, 150, 250, 320):
        a = np.radians(graus)
        pontos = []
        for t in np.linspace(0.0, 1.0, 7):
            r = 16 + t * 28
            pontos.append((cx + r * np.cos(a) + rng.uniform(-3, 3), cy + r * 1.1 * np.sin(a) + rng.uniform(-3, 3)))
        img.pintar(img.caminho(pontos, 0.6), "ciano", 0.95, achatar=False)
    # Cabos grossos descendo das torres para o chão.
    for (x0, x1) in ((36, 12), (140, 164)):
        img.pintar(img.caminho([(x0, 118), ((x0 + x1) / 2, 140), (x1, 152)], 1.4), "aco", 0.2)
    img.contornar()
    return img, 88, 154


def caixas_lab():
    """Caixas de equipamento com tampa: as cinzas de aço e uma azul do DTEC."""
    img = Imagem(44, 30)
    X, Y = img.X, img.Y
    for (x0, y0, x1, y1, rampa) in ((2, 12, 24, 28, "aco"), (22, 16, 42, 28, "dtec"), (6, 2, 22, 12, "aco")):
        img.pintar(img.ret(x0, y0, x1, y1), rampa, 0.35 + 0.25 * (Y == y0) + 0.1 * (X == x0))
        img.pintar(img.ret(x0, y0 + 3, x1, y0 + 4), rampa, 0.2)
        img.pintar(img.ret((x0 + x1) // 2 - 2, y0 + 5, (x0 + x1) // 2 + 2, y0 + 7), "aco", 0.7)
    img.contornar()
    return img, 22, 28


OBJETOS = {
    "bancada_lab": (bancada_lab, (66, 6)),
    "bancada_eletronica": (bancada_eletronica, (66, 6)),
    "mesa_computador": (mesa_computador, (46, 5)),
    "cadeira_escritorio": (cadeira_escritorio, (12, 3)),
    "rack_dtec": (rack_dtec, (24, 5)),
    "armario_quimico": (armario_quimico, (34, 5)),
    "capela": (capela, (46, 5)),
    "cilindros": (cilindros, (26, 5)),
    "braco_robotico": (braco_robotico, (26, 5)),
    "robo_desmontado": (robo_desmontado, (60, 5)),
    "console": (console, (58, 5)),
    "planta": (planta, (14, 4)),
    "balcao_recepcao": (balcao_recepcao, (96, 6)),
    "catraca": (catraca, (14, 4)),
    "maquina": (maquina, (150, 22)),
    "caixas_lab": (caixas_lab, (40, 5)),
}


def main():
    print("Gerando o kit do DTEC em", os.path.relpath(PASTA_DTEC, PASTA_PROJETO))
    paredes = {nome: f() for nome, f in PAREDES.items()}
    paredes["pilar_dtec"] = pilar_dtec()
    for nome, img in paredes.items():
        img.salvar(f"{nome}.png", os.path.join(PASTA_DTEC, "paredes"))
    chaos = {}
    for nome, f in CHAOS.items():
        img = f()
        img.px = img.px[Y_CHAO:].copy()
        img.h = img.px.shape[0]
        img.salvar(f"{nome}.png", os.path.join(PASTA_DTEC, "chao"))
        chaos[nome] = img
    for nome, f in CHAOS_FUNDO.items():
        f().salvar(f"{nome}.png", os.path.join(PASTA_DTEC, "chao"))
    dtec_lateral().salvar("dtec_lateral.png", os.path.join(PASTA_DTEC, "paredes"))
    objetos = {}
    for nome, (f, pegada) in OBJETOS.items():
        img, px, py = f()
        img.salvar(f"{nome}.png", os.path.join(PASTA_DTEC, "objetos"))
        print(f"    {nome}: pé em ({px}, {py}) -> offset = Vector2({-px}, {-py}), pegada {pegada}")
        objetos[nome] = img
    if not CATALOGO:
        return
    pasta = PASTA_SCRIPT if CATALOGO == "1" else CATALOGO
    os.makedirs(pasta, exist_ok=True)
    for nome, pecas, colunas in (("dtec_paredes", list(paredes.items()), 5),
                                 ("dtec_chao", list(chaos.items()), 4),
                                 ("dtec_objetos", list(objetos.items()), 4)):
        bib.salvar_png(os.path.join(pasta, f"{nome}.png"), kit.catalogo(pecas, colunas, None))
        print("  catálogo:", f"{nome}.png (não commitar)")


if __name__ == "__main__":
    main()
