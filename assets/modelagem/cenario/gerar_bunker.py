# gerar_bunker.py — desenha, por código, o KIT DO BUNKER: as peças de parede,
# de chão e os objetos do bunker de pesquisa embaixo do núcleo da Âncora
# (docs/fases/bunker.md). Mesmo estilo do kit de cenário (gerar_kit.py) e
# da Biblioteca, que este script importa: paleta, dithering, contorno.
#
# Como rodar (Python 3 + numpy):
#
#   python assets/modelagem/cenario/gerar_bunker.py
#
# O que sai (em assets/sprites/cenario/bunker/):
#   paredes/<peça>.png   80 x 112 px: um pedaço da parede do fundo (encaixa lado a lado)
#   paredes/pilar_bunker.png  16 x 112 px: a viga de aço das pontas
#   chao/<peça>.png      128 x 68 px: um pedaço do chão
#   objetos/<objeto>.png objetos que o Gabriel contorna (y-sort); o "pé" de
#                        cada um sai no terminal, como no gerar_biblioteca.py
# Com CATALOGO=1 monta folhas com o nome de cada peça (bunker_paredes.png,
# bunker_chao.png, bunker_objetos.png) nesta pasta. Não commitar.
#
# ---------------------------------------------------------------------------
# O VISUAL DO BUNKER
# ---------------------------------------------------------------------------
#
# A Biblioteca é ruína tomada pela natureza; o bunker é o contrário: fechado,
# seco, construído para durar. Mil anos depois ainda está de pé, mas gasto.
# O que conta isso:
#   - parede em duas faixas: concreto aparente em cima e TINTA verde-oliva
#     embaixo (a cor de instalação militar), descascando em manchas, com um
#     filete amarelo de sinalização entre as duas;
#   - no teto, uma ELETROCALHA de aço com cabos pendurados entre os
#     suportes. O cabo pendurado é uma CATENÁRIA; aqui usamos meio seno,
#     y = y0 + flecha · sen(π · x / vão), que é quase igual e é fácil;
#   - aço azulado (portas, vigas, canos) em vez de madeira;
#   - AMARELO E PRETO em faixas diagonais onde há perigo (portas, comporta,
#     degraus). A faixa diagonal é ((x + y) // largura) % 2: quando x + y
#     passa de um múltiplo da largura, a cor troca;
#   - luz: tubos fluorescentes frios que piscam e luzes de emergência
#     vermelhas (as PointLight2D ficam nas cenas, em cima das peças
#     bunker_luminaria e bunker_emergencia).
#
# Tudo encaixa sem emenda pelo mesmo truque do kit: ruído cíclico (a grade
# de números sorteados dá a volta na largura da peça) e juntas na coluna 0.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_BUNKER = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "bunker")
CATALOGO = os.environ.get("CATALOGO", "")

_spec = importlib.util.spec_from_file_location("gerar_kit", os.path.join(PASTA_SCRIPT, "gerar_kit.py"))
kit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kit)
bib = kit.bib

Imagem, RAMPAS, SOMBRA, CONTORNO, dilatar = bib.Imagem, bib.RAMPAS, bib.SOMBRA, bib.CONTORNO, bib.dilatar
ciclico = kit.ruido_ciclico
L = 80                 # largura da peça de parede
Y_CHAO = kit.Y_CHAO    # 112
ALTURA = kit.ALTURA    # 180
LUZ = kit.LUZ

# Rampas novas do bunker (do mais escuro ao mais claro). Entram no mesmo
# dicionário de rampas da Biblioteca, então o pintar() já sabe usar.
RAMPAS.update({
    "tinta": bib.hexa("#141a14", "#1c241c", "#263026", "#313d30", "#3e4b3b", "#4d5b48", "#5f6d57"),
    "aco": bib.hexa("#101318", "#181d24", "#222933", "#2e3642", "#3c4553", "#4d5767", "#63707f", "#7f8b98"),
    "amarelo": bib.hexa("#2a2208", "#4a3b0e", "#6f5812", "#977818", "#b8931f", "#d1ab2c"),
    "vermelho": bib.hexa("#1e0a0a", "#3a1110", "#5a1916", "#7c231d", "#9c3025", "#b8432f"),
    "branco": bib.hexa("#3a3a36", "#55554f", "#71716a", "#8d8c83", "#a6a498", "#bcb9aa"),
    "lona": bib.hexa("#16170f", "#222418", "#2f3221", "#3d412b", "#4d5236", "#5e6443"),
    "vidro": bib.hexa("#0b1216", "#101b21", "#16252d", "#1f3340", "#2c4756"),
    "fluorescente": bib.hexa("#8d9aa0", "#b9c6c9", "#dde8ea", "#f4fbfb"),
})
LED_VERDE = bib.hexa("#6cf28e")[0]
LED_VERMELHO = bib.hexa("#ff5a3a")[0]
LED_AMBAR = bib.hexa("#ffc24a")[0]


def listras(img, mascara, largura=4, inclinacao=1, tom=0.8):
    """Faixas de perigo amarelas e pretas na diagonal, dentro da máscara."""
    faixa = ((img.X + inclinacao * img.Y) // largura) % 2 == 0
    img.pintar(mascara & faixa, "amarelo", tom)
    img.pintar(mascara & ~faixa, "aco", 0.05)


# ---------------------------------------------------------------------------
# Paredes
# ---------------------------------------------------------------------------


def parede_base(semente=0):
    img = Imagem(L, Y_CHAO)
    X, Y = img.X, img.Y
    parede = img.ret(0, 0, L, Y_CHAO)
    manchas = ciclico(L, Y_CHAO, 40, 18, 200 + semente)
    fino = ciclico(L, Y_CHAO, 2, 2, 201)
    escorrido = ciclico(L, Y_CHAO, 4, 50, 202 + semente)
    v = (0.32 + 0.2 * manchas + 0.07 * fino - 0.14 * (escorrido > 0.72)) * LUZ
    v = v - 0.15 * np.clip((26 - Y) / 12, 0, 1)
    img.pintar(parede, "concreto", v)
    # Faixa pintada de verde-oliva, descascando (onde o ruído passa do
    # limite, a tinta caiu e aparece o concreto).
    tinta = img.ret(0, 58, L, 100)
    descascado = ciclico(L, Y_CHAO, 5, 4, 203 + semente) > 0.82
    img.pintar(tinta & ~descascado, "tinta", 0.46 + 0.1 * manchas + 0.05 * fino)
    img.pintar(tinta & descascado & dilatar(~descascado & tinta), "tinta", 0.15, achatar=False)
    img.pintar(img.ret(0, 56, L, 58), "amarelo", 0.5 + 0.1 * fino)
    img.pintar(img.ret(0, 58, L, 59), "tinta", 0.12)
    # Rodapé de concreto escuro, com marcas de bota.
    img.pintar(img.ret(0, 100, L, Y_CHAO), "concreto", 0.13 + 0.06 * fino + 0.1 * (Y == 100))
    # Laje do teto e a eletrocalha com os cabos pendurados.
    img.pintar(img.ret(0, 0, L, 10), "concreto", 0.08 + 0.05 * fino + 0.1 * (Y == 9))
    img.cor(img.ret(0, 10, L, 12), RAMPAS["concreto"][0])
    for xs in (0, 40):
        img.pintar(img.ret(xs + 2, 10, xs + 4, 15), "aco", 0.3)
    img.pintar(img.ret(0, 14, L, 17), "aco", 0.32 + 0.3 * (Y == 14))
    for k, (flecha, rampa, tom) in enumerate(((4, "aco", 0.12), (2.5, "vermelho", 0.3), (5.5, "aco", 0.08))):
        ys = 17.5 + k * 0.7 + flecha * np.sin(np.pi * ((X - 3) % 40) / 40)
        img.pintar((np.abs(Y + 0.5 - ys) < 0.6) & parede, rampa, tom, achatar=False)
    # Junta das placas (na coluna 0: disfarça a emenda) e parafusos.
    img.pintar(parede & (X == 0) & (Y > 20) & (Y < 100), "concreto", v - 0.2, achatar=False)
    for x in (8, 32, 48, 72):
        img.pintar(img.ret(x, 62, x + 1, 63), "aco", 0.7)
    img.v, img.fino, img.manchas = v, fino, manchas
    return img


def plaquinha(img, x0, x1, y0=28):
    """Placa de aço escura em cima da porta: o nome da sala entra por cima,
    no Godot (Label), para cada porta ter o seu sem desenhar uma peça nova."""
    img.pintar(img.ret(x0, y0, x1, y0 + 9), "aco", 0.12)
    img.pintar(img.ret(x0, y0, x1, y0 + 1), "aco", 0.4)
    for x in (x0 + 1, x1 - 2):
        img.pintar(img.ret(x, y0 + 4, x + 1, y0 + 5), "aco", 0.6)


def batente(img, xa, xb, ya):
    """Batente de aço grosso com faixas de perigo na parte de baixo."""
    img.pintar(img.ret(xa - 4, ya - 4, xb + 4, Y_CHAO), "aco", 0.36 + 0.06 * img.fino)
    img.pintar(img.ret(xa - 4, ya - 4, xb + 4, ya - 3), "aco", 0.6)
    img.pintar(img.ret(xa - 4, ya - 4, xa - 3, Y_CHAO), "aco", 0.55)
    listras(img, img.ret(xa - 4, Y_CHAO - 12, xa, Y_CHAO) | img.ret(xb, Y_CHAO - 12, xb + 4, Y_CHAO), 3)


def bunker_lisa():
    return parede_base()


def bunker_rachada():
    """Infiltração: rachadura grande, a mancha escura de água descendo do
    teto até a faixa pintada e ferrugem escorrendo de um vergalhão."""
    img = parede_base(1)
    X, Y = img.X, img.Y
    agua = (np.abs(X - 44 - 4 * np.sin(Y / 9)) < 7 - Y / 30) & (Y > 11) & (Y < 96)
    img.pintar(agua, "concreto", img.v * 0.55, achatar=False)
    kit.rachadura(img, 30, 210)
    kit.rachadura(img, 52, 211)
    img.pintar(img.linha(24, 40, 30, 36, 0.6), "ferrugem", 0.6)
    img.pintar((np.abs(X - 27) < 1) & (Y > 40) & (Y < 70), "ferrugem", 0.35, achatar=False)
    return img


def bunker_canos():
    """Dois canos horizontais (encaixam de uma peça para a outra: as
    flanges ficam em x = 0 e 40) e um cano que desce com um registro de
    volante vermelho."""
    img = parede_base(2)
    X, Y = img.X, img.Y
    for (ya, esp, tom) in ((22, 5, 0.45), (31, 3, 0.35)):
        cano = img.ret(0, ya, L, ya + esp)
        img.pintar(cano, "aco", tom + 0.25 * (Y == ya) - 0.15 * (Y == ya + esp - 1))
        for xf in (0, 40):
            img.pintar(img.ret(xf, ya - 1, xf + 3, ya + esp + 1), "aco", tom + 0.15)
    img.pintar(img.ret(60, 25, 64, 100), "aco", 0.38 + 0.25 * (X == 60))
    img.pintar(img.ret(58, 26, 66, 29), "aco", 0.55)
    volante = img.elipse(62, 70, 6, 6) & ~img.elipse(62, 70, 4, 4)
    img.pintar(volante, "vermelho", 0.7)
    img.pintar(img.linha(56, 70, 68, 70, 0.6) | img.linha(62, 64, 62, 76, 0.6), "vermelho", 0.55)
    img.pintar(img.ret(61, 69, 63, 71), "aco", 0.7)
    return img


def bunker_luminaria():
    """Luminária de tubo fluorescente presa na eletrocalha, com a grade de
    proteção. No Godot, uma PointLight2D fria que pisca (LuzTremula)."""
    img = parede_base(3)
    img.pintar(img.ret(14, 17, 66, 22), "aco", 0.3 + 0.2 * (img.Y == 17))
    img.pintar(img.ret(17, 22, 63, 25), "fluorescente", 0.9)
    img.pintar(img.ret(17, 23, 63, 24), "fluorescente", 1.0)
    for x in range(18, 63, 6):
        img.pintar(img.ret(x, 22, x + 1, 26), "aco", 0.2)
    img.pintar(img.ret(16, 25, 64, 26), "aco", 0.25)
    return img


def bunker_emergencia():
    """Giroflex de emergência vermelho numa caixa de aço, com a grade de
    arame em volta da cúpula (a luz vermelha fica na cena)."""
    img = parede_base(4)
    img.pintar(img.ret(34, 30, 46, 34), "aco", 0.35)
    cupula = img.elipse(40, 29, 5, 5) & (img.Y < 30)
    img.pintar(cupula, "vermelho", 0.8 + 0.2 * (img.X < 39))
    for x in (36, 40, 44):
        img.pintar(img.ret(x, 24, x + 1, 30), "aco", 0.25)
    img.pintar(img.ret(40, 17, 41, 30), "aco", 0.2)
    img.pintar(img.ret(24, 40, 56, 50), "vermelho", 0.35)
    img.pintar(img.ret(25, 41, 55, 49), "vermelho", 0.5)
    return img


def bunker_porta():
    """Porta de correr de aço, aberta: a folha entrou na parede e sobrou o
    vão escuro, com um pouco do corredor do outro lado."""
    img = parede_base(5)
    xa, xb, ya = 20, 62, 44
    batente(img, xa, xb, ya)
    vao = img.ret(xa, ya, xb, Y_CHAO)
    prof = (img.Y - ya) / (Y_CHAO - ya)
    img.pintar(vao, "concreto", 0.03 + 0.07 * prof)
    img.cor(img.ret(xa, ya, xb, ya + 2), SOMBRA)
    img.pintar(img.ret(xb - 5, ya, xb, Y_CHAO), "aco", 0.28 + 0.1 * (img.X == xb - 5))
    plaquinha(img, 24, 58)
    return img


def porta_fechada(img):
    xa, xb, ya = 20, 62, 44
    batente(img, xa, xb, ya)
    folha = img.ret(xa, ya, xb, Y_CHAO)
    img.pintar(folha, "aco", 0.3 + 0.08 * img.manchas + 0.12 * ((img.Y - ya) % 14 == 0))
    img.pintar(img.ret(xa + 13, ya + 6, xb - 13, ya + 16), "vidro", 0.3 + 0.4 * ((img.X + img.Y) % 7 == 0))
    img.pintar(img.ret(xa + 12, ya + 5, xb - 12, ya + 6), "aco", 0.55)
    img.pintar(img.ret(xb - 9, ya + 30, xb - 4, ya + 33), "aco", 0.65)
    plaquinha(img, 24, 58)
    return img


def bunker_porta_fechada():
    return porta_fechada(parede_base(6))


def bunker_porta_lacrada():
    """Porta fechada e LACRADA: corrente com cadeado e a fita de isolamento
    vermelha e branca em X. É a porta das salas que ainda não abrem."""
    img = porta_fechada(parede_base(7))
    X, Y = img.X, img.Y
    for (a, b) in (((16, 50), (66, 104)), ((66, 50), (16, 104))):
        fita = img.linha(a[0], a[1], b[0], b[1], 1.6)
        listra = ((X + Y) // 3) % 2 == 0
        img.pintar(fita & listra, "vermelho", 0.75)
        img.pintar(fita & ~listra, "branco", 0.9)
    corrente = img.caminho([(21, 78), (31, 83), (41, 80), (51, 83), (61, 78)], 0.7)
    img.pintar(corrente & ((X % 3) != 0), "ferrugem", 0.55)
    img.pintar(img.ret(38, 82, 44, 89), "amarelo", 0.55)
    img.pintar(img.elipse(41, 81.5, 2.5, 2.5) & ~img.elipse(41, 81.5, 1.2, 1.2) & (Y < 82), "aco", 0.6)
    return img


def bunker_comporta():
    """A comporta redonda do acesso ao núcleo: porta de cofre, com anéis,
    oito trancas em volta e o volante no meio. Sempre lacrada por enquanto."""
    img = parede_base(8)
    X, Y = img.X, img.Y
    cx, cy, r = 40, 68, 32
    moldura = img.elipse(cx, cy, r + 4, r + 4) & (Y < Y_CHAO)
    listras(img, moldura & ~img.elipse(cx, cy, r + 1, r + 1), 3)
    disco = img.elipse(cx, cy, r, r) & (Y < Y_CHAO)
    dist = np.sqrt((X + 0.5 - cx) ** 2 + (Y + 0.5 - cy) ** 2)
    img.pintar(disco, "aco", 0.38 - 0.12 * (dist / r) + 0.18 * (np.abs(dist - r * 0.72) < 0.8) - 0.1 * (X > cx + 8))
    for i in range(8):
        a = i * np.pi / 4
        bx, by = cx + np.cos(a) * (r - 4), cy + np.sin(a) * (r - 4)
        img.pintar(img.elipse(bx, by, 2.2, 2.2) & disco, "aco", 0.65)
    img.pintar(img.elipse(cx, cy, 9, 9) & ~img.elipse(cx, cy, 7, 7), "vermelho", 0.6)
    for a in (0, np.pi / 3, 2 * np.pi / 3):
        img.pintar(img.linha(cx - 8 * np.cos(a), cy - 8 * np.sin(a), cx + 8 * np.cos(a), cy + 8 * np.sin(a), 0.6), "vermelho", 0.5)
    img.pintar(img.elipse(cx, cy, 2.5, 2.5), "aco", 0.75)
    return img


def bunker_armarios():
    """Três armários de metal com as frestas de ventilação; o do meio ficou
    entreaberto (a fresta escura na borda)."""
    img = parede_base(9)
    X, Y = img.X, img.Y
    for i, x0 in enumerate((10, 30, 50)):
        porta = img.ret(x0, 34, x0 + 19, 100)
        img.pintar(porta, "tinta", 0.5 + 0.2 * (X == x0) - 0.15 * (X == x0 + 18))
        for y in range(40, 52, 3):
            img.pintar(img.ret(x0 + 5, y, x0 + 14, y + 1), "tinta", 0.1)
        img.pintar(img.ret(x0 + 14, 66, x0 + 16, 72), "aco", 0.6)
        img.pintar(img.ret(x0 + 5, 56, x0 + 14, 60), "branco", 0.5)
        if i == 1:
            img.cor(img.ret(x0 + 18, 34, x0 + 20, 100), SOMBRA)
    img.pintar(img.ret(9, 32, 71, 34), "tinta", 0.3)
    img.pintar(img.ret(9, 100, 71, 102), "tinta", 0.2)
    return img


def bunker_painel():
    """Quadro elétrico: a caixa cinza com os disjuntores, a placa de
    perigo (triângulo amarelo com o raio) e os conduítes subindo até a
    eletrocalha."""
    img = parede_base(10)
    X, Y = img.X, img.Y
    for x in (22, 30, 38):
        img.pintar(img.ret(x, 17, x + 2, 34), "aco", 0.3)
    caixa = img.ret(16, 34, 64, 86)
    img.pintar(caixa, "aco", 0.42 + 0.2 * (Y == 34) - 0.15 * (X == 63))
    img.pintar(img.ret(20, 40, 50, 80), "aco", 0.2)
    for fila in range(4):
        for col in range(5):
            x, y = 22 + col * 6, 42 + fila * 9
            img.pintar(img.ret(x, y, x + 4, y + 6), "branco", 0.4)
            img.pintar(img.ret(x + 1, y + (1 if (fila + col) % 3 else 3), x + 3, y + (3 if (fila + col) % 3 else 5)), "aco", 0.1)
    tri = img.poligono([(57, 42), (52, 52), (62, 52)])
    img.pintar(tri, "amarelo", 0.85)
    img.pintar(img.caminho([(58, 44), (56, 48), (58, 48), (56, 51)], 0.45), "aco", 0.05)
    img.cor(img.ret(54, 60, 56, 62), LED_VERMELHO)
    return img


def bunker_mapa():
    """Planta de evacuação emoldurada: as salas em linha escura, o "você
    está aqui" vermelho e as setas verdes de saída."""
    img = parede_base(11)
    X, Y = img.X, img.Y
    img.pintar(img.ret(12, 28, 68, 72), "aco", 0.3)
    papel = img.ret(14, 30, 66, 70)
    img.pintar(papel, "branco", 0.62 + 0.1 * img.manchas)
    for (x0, y0, x1, y1) in ((18, 36, 34, 48), (34, 36, 50, 48), (50, 36, 62, 48), (18, 52, 40, 66), (40, 52, 62, 66)):
        borda = img.ret(x0, y0, x1, y1) & ~img.ret(x0 + 1, y0 + 1, x1 - 1, y1 - 1)
        img.pintar(borda, "aco", 0.1)
    img.pintar(img.ret(18, 48, 62, 52), "branco", 0.45)
    img.pintar(img.elipse(30, 58, 1.8, 1.8), "vermelho", 0.8)
    for x in (44, 52):
        img.pintar(img.poligono([(x, 49), (x + 4, 50), (x, 51)]), "tinta", 0.9)
    img.pintar(img.ret(14, 30, 66, 33), "vermelho", 0.55)
    return img


def bunker_grafo():
    """A parede da Clarice: folhas de papel coladas com fita, com o GRAFO
    das rotas dos robôs desenhado a pincel atômico (nós são bolinhas, as
    arestas são as linhas entre eles), barbante vermelho ligando uma folha
    à outra e post-its rosa e amarelo. É a descoberta dela
    (docs/personagens/antecessores.md): as patrulhas formam um grafo."""
    img = parede_base(12)
    X, Y = img.X, img.Y
    folhas = ((6, 26, 34, 52), (38, 22, 70, 50), (10, 56, 40, 84), (44, 54, 74, 86))
    rng = np.random.default_rng(1994)
    nos_todos = []
    for (x0, y0, x1, y1) in folhas:
        img.pintar(img.ret(x0, y0, x1, y1), "branco", 0.72 + 0.08 * img.fino)
        img.pintar(img.ret(x0 + (x1 - x0) // 2 - 3, y0 - 1, x0 + (x1 - x0) // 2 + 3, y0 + 2), "amarelo", 0.4)
        nos = [(int(rng.integers(x0 + 3, x1 - 3)), int(rng.integers(y0 + 3, y1 - 3))) for _ in range(5)]
        for a, b in zip(nos, nos[1:] + nos[:1]):
            img.pintar(img.linha(a[0] + 0.5, a[1] + 0.5, b[0] + 0.5, b[1] + 0.5, 0.45), "aco", 0.08)
        for (x, y) in nos:
            img.pintar(img.elipse(x + 0.5, y + 0.5, 1.6, 1.6), "aco", 0.05)
        nos_todos.append(nos[0])
    for a, b in zip(nos_todos, nos_todos[1:]):
        img.pintar(img.linha(a[0] + 0.5, a[1] + 0.5, b[0] + 0.5, b[1] + 0.5, 0.45), "vermelho", 0.8, achatar=False)
    img.pintar(img.ret(28, 46, 35, 52), bib.hexa("#e5609f"), 0.5)
    img.pintar(img.ret(64, 26, 70, 32), bib.hexa("#f0d148"), 0.5)
    img.pintar(img.ret(12, 86, 20, 92), bib.hexa("#f0d148"), 0.5)
    return img


def bunker_vidro():
    """Janela de observação para a sala dos servidores: vidro escuro com o
    reflexo em diagonal e, lá dentro, os LEDs dos equipamentos."""
    img = parede_base(13)
    X, Y = img.X, img.Y
    img.pintar(img.ret(8, 28, 72, 74), "aco", 0.4 + 0.2 * (Y == 28))
    vidro = img.ret(11, 31, 69, 71)
    img.pintar(vidro, "vidro", 0.2 + 0.25 * (Y - 31) / 40)
    for x in range(16, 66, 10):
        img.pintar(img.ret(x, 36, x + 6, 71), "vidro", 0.08)
        for y in range(40, 68, 4):
            if (x * 3 + y) % 7 < 3:
                img.cor(img.ret(x + 1 + (y % 3), y, x + 2 + (y % 3), y + 1), LED_VERDE if (x + y) % 5 else LED_AMBAR)
    reflexo = vidro & ((np.abs((X - Y) - 4) < 2) | (np.abs((X - Y) + 10) < 1))
    img.pintar(reflexo, "vidro", 0.95, achatar=False)
    return img


def bunker_prateleiras():
    """Prateleiras de aço na parede, com latas, potes e caixas."""
    img = parede_base(14)
    rng = np.random.default_rng(140)
    for y in (46, 66, 86):
        img.pintar(img.ret(8, y, 72, y + 2), "aco", 0.45)
        img.pintar(img.ret(10, y + 2, 12, y + 6), "aco", 0.3)
        img.pintar(img.ret(68, y + 2, 70, y + 6), "aco", 0.3)
        x = 10
        while x < 66:
            tipo = rng.integers(0, 3)
            if tipo == 0:
                h = int(rng.integers(6, 10))
                img.pintar(img.ret(x, y - h, x + 5, y), "aco", 0.55 + 0.2 * (img.X == x))
                img.pintar(img.ret(x, y - h + 2, x + 5, y - h + 4), rng.choice(["vermelho", "amarelo", "tinta"]), 0.6)
                x += 6
            elif tipo == 1:
                h = int(rng.integers(8, 14))
                img.pintar(img.ret(x, y - h, x + 10, y), "madeira", 0.5)
                img.pintar(img.ret(x + 2, y - h + 3, x + 8, y - h + 5), "branco", 0.4)
                x += 11
            else:
                x += int(rng.integers(3, 8))
    return img


def bunker_remedios():
    """Armário de remédios da enfermaria: caixa branca com a cruz vermelha,
    portas de vidro e frascos atrás."""
    img = parede_base(15)
    X, Y = img.X, img.Y
    img.pintar(img.ret(18, 26, 62, 84), "branco", 0.62 + 0.15 * (Y == 26) - 0.15 * (X == 61))
    img.pintar(img.ret(21, 38, 39, 81), "vidro", 0.35)
    img.pintar(img.ret(41, 38, 59, 81), "vidro", 0.35)
    for y in (50, 64):
        img.pintar(img.ret(21, y, 59, y + 1), "branco", 0.4)
        for x in range(23, 58, 4):
            if (x + y) % 3:
                img.pintar(img.ret(x, y - 5, x + 2, y), "ferrugem", 0.6)
    img.pintar(img.ret(36, 28, 44, 36), "vermelho", 0.75)
    img.pintar(img.ret(38, 27, 42, 37), "vermelho", 0.75)
    img.pintar(img.ret(34, 29, 46, 35), "vermelho", 0.75)
    return img


def bunker_descontaminacao():
    """Área de descontaminação da entrada: chuveiros no cano do teto, a
    faixa de perigo e o ralo na parede."""
    img = parede_base(16)
    img.pintar(img.ret(0, 24, L, 28), "aco", 0.42 + 0.25 * (img.Y == 24))
    for x in (14, 40, 66):
        img.pintar(img.ret(x - 1, 28, x + 2, 34), "aco", 0.4)
        img.pintar(img.poligono([(x - 5, 38), (x + 6, 38), (x + 3, 34), (x - 2, 34)]), "aco", 0.55)
        for gota in range(3):
            img.pintar(img.ret(x - 3 + gota * 3, 42 + gota * 5, x - 2 + gota * 3, 44 + gota * 5), "vidro", 0.8)
    listras(img, img.ret(0, 50, L, 56), 4)
    img.pintar(img.ret(34, 90, 46, 98), "aco", 0.2)
    for x in range(35, 46, 2):
        img.pintar(img.ret(x, 91, x + 1, 97), "aco", 0.05)
    return img


def escada(sobe):
    """Vão com a escada de aço: degraus de chapa xadrez em perfil, o
    corrimão amarelo e o fundo escuro (para onde a escada vai)."""
    img = parede_base(17 if sobe else 18)
    X, Y = img.X, img.Y
    xa, xb, ya = 14, 66, 34
    batente(img, xa, xb, ya)
    vao = img.ret(xa, ya, xb, Y_CHAO)
    img.pintar(vao, "concreto", 0.02 + 0.04 * (Y - ya) / (Y_CHAO - ya))
    passo = ((X - xa) // 6) if sobe else ((xb - 1 - X) // 6)
    topo = Y_CHAO - 1 - 8 * (passo + 1) if sobe else ya + 10 + 8 * passo
    if sobe:
        massa = vao & (Y >= topo)
    else:
        massa = vao & (Y >= topo) & (Y < topo + 3)
    img.pintar(massa, "aco", 0.22 + 0.05 * img.fino)
    img.pintar(vao & (Y >= topo) & (Y < topo + 1), "aco", 0.6)
    borda = ((X - xa) % 6 == 0) if sobe else ((xb - 1 - X) % 6 == 0)
    if sobe:
        img.pintar(vao & borda & (Y >= topo), "aco", 0.08)
        corrimao = img.linha(xa + 1, Y_CHAO - 22, xb - 1, Y_CHAO - 22 - 8 * (xb - xa) / 6, 0.7)
    else:
        corrimao = img.linha(xb - 1, ya + 2, xa + 1, ya + 2 + 8 * (xb - xa) / 6, 0.7)
    img.pintar(corrimao & vao, "amarelo", 0.7)
    return img


def bunker_escada_sobe():
    return escada(True)


def bunker_escada_desce():
    return escada(False)


def pilar_bunker():
    """Viga de aço em I nas pontas da sala: alma escura, abas claras,
    parafusos e faixa de perigo embaixo."""
    img = Imagem(16, Y_CHAO)
    X, Y = img.X, img.Y
    img.pintar(img.ret(0, 0, 16, Y_CHAO), "aco", 0.22 + 0.05 * ciclico(16, Y_CHAO, 2, 2, 230))
    img.pintar(img.ret(0, 0, 3, Y_CHAO), "aco", 0.5)
    img.pintar(img.ret(13, 0, 16, Y_CHAO), "aco", 0.4)
    for y in range(20, 100, 16):
        img.pintar(img.ret(6, y, 7, y + 1) | img.ret(9, y, 10, y + 1), "aco", 0.7)
    listras(img, img.ret(0, 96, 16, Y_CHAO), 3)
    return img


PAREDES = {
    "bunker_lisa": bunker_lisa,
    "bunker_rachada": bunker_rachada,
    "bunker_canos": bunker_canos,
    "bunker_luminaria": bunker_luminaria,
    "bunker_emergencia": bunker_emergencia,
    "bunker_porta": bunker_porta,
    "bunker_porta_fechada": bunker_porta_fechada,
    "bunker_porta_lacrada": bunker_porta_lacrada,
    "bunker_comporta": bunker_comporta,
    "bunker_armarios": bunker_armarios,
    "bunker_painel": bunker_painel,
    "bunker_mapa": bunker_mapa,
    "bunker_grafo": bunker_grafo,
    "bunker_vidro": bunker_vidro,
    "bunker_prateleiras": bunker_prateleiras,
    "bunker_remedios": bunker_remedios,
    "bunker_descontaminacao": bunker_descontaminacao,
    "bunker_escada_sobe": bunker_escada_sobe,
    "bunker_escada_desce": bunker_escada_desce,
    "pilar_bunker": pilar_bunker,
}

# ---------------------------------------------------------------------------
# Chão
# ---------------------------------------------------------------------------


def chao_base(semente=0):
    """Piso de concreto liso pintado de cinza, com juntas de dilatação que
    seguem a perspectiva (as mesmas fileiras da Biblioteca, mas a cada três)
    e a faixa amarela de sinalização rente à parede."""
    img = Imagem(128, ALTURA)
    X, Y = img.X, img.Y
    chao = img.ret(0, Y_CHAO, 128, ALTURA)
    fino = ciclico(128, ALTURA, 2, 2, 240)
    manchas = ciclico(128, ALTURA, 32, 10, 241 + semente)
    oleo = ciclico(128, ALTURA, 16, 6, 242 + semente) > 0.82
    valor = (0.42 + 0.14 * manchas + 0.05 * fino - 0.12 * oleo) * LUZ - 0.2 * np.clip((122 - Y) / 10, 0, 1)
    img.pintar(chao, "piso", valor)
    juntas = np.zeros(chao.shape, dtype=bool)
    for ya in bib.FILEIRAS[3::3]:
        juntas |= Y == ya
    juntas |= (X % 64 == 0) & (Y > Y_CHAO + 2)
    img.pintar(chao & juntas, "piso", valor - 0.2, achatar=False)
    img.pintar(img.ret(0, 116, 128, 118), "amarelo", 0.42 + 0.08 * fino)
    img.cor(img.ret(0, Y_CHAO, 128, Y_CHAO + 1), SOMBRA)
    img.chao, img.fino, img.manchas = chao, fino, manchas
    return img


def chao_bunker():
    img = chao_base()
    img.pintar(img.ret(56, 150, 72, 156), "aco", 0.2)
    for x in range(57, 72, 2):
        img.pintar(img.ret(x, 151, x + 1, 155), "aco", 0.05)
    return img


def chao_bunker_grade():
    """Passarela de grade metálica: em cada fileira da perspectiva, furos
    em losango, maiores nas fileiras de baixo (mais perto)."""
    img = chao_base(1)
    X, Y = img.X, img.Y
    grade = img.ret(0, 122, 128, ALTURA)
    img.pintar(grade, "aco", 0.36 + 0.06 * img.manchas)
    for i in range(len(bib.FILEIRAS) - 1):
        ya, yb = bib.FILEIRAS[i], bib.FILEIRAS[i + 1]
        if yb <= 122:
            continue
        faixa = (Y >= ya) & (Y < yb)
        passo = max(3, (yb - ya) // 2 + 2)
        furo = faixa & ((np.abs((X % passo) - passo / 2) + np.abs(Y - (ya + yb) / 2) * 1.2) < passo / 2 - 1)
        img.pintar(furo & grade, "aco", 0.06)
        img.pintar(faixa & (Y == ya) & grade, "aco", 0.6)
    img.pintar(img.ret(0, 120, 128, 122), "aco", 0.5)
    return img


def chao_bunker_agua():
    """Concreto com água empoçada (vazamento do setor B): poças escuras com
    a borda úmida e o reflexo claro das luzes em riscos horizontais."""
    img = chao_base(2)
    X, Y = img.X, img.Y
    poca = (ciclico(128, ALTURA, 32, 8, 250) + 0.2 * img.fino > 0.68) & img.chao & (Y > 120)
    img.pintar(dilatar(poca) & ~poca & img.chao, "piso", 0.25)
    img.pintar(poca, "vidro", 0.25 + 0.15 * img.manchas)
    reflexo = poca & ((Y % 5) == 0) & (ciclico(128, ALTURA, 8, 2, 251) > 0.6)
    img.pintar(reflexo, "vidro", 0.9, achatar=False)
    return img


def chao_bunker_faixa():
    """Faixa de perigo pintada no chão, na frente de portas e da comporta."""
    img = chao_base(3)
    faixa = img.ret(0, 128, 128, 146)
    listras(img, faixa, 6, 1, 0.65)
    img.pintar(faixa & (img.manchas > 0.72), "piso", 0.35)
    return img


CHAOS = {
    "chao_bunker": chao_bunker,
    "chao_bunker_grade": chao_bunker_grade,
    "chao_bunker_agua": chao_bunker_agua,
    "chao_bunker_faixa": chao_bunker_faixa,
}

# ---------------------------------------------------------------------------
# Objetos: cada função devolve (imagem, x_do_pé, y_do_pé), como na Biblioteca.
# A PEGADA é o retângulo de colisão no chão (largura, altura), em px.
# ---------------------------------------------------------------------------


def beliche():
    """Beliche de aço com dois colchões de lona verde, travesseiros e um
    cobertor escorregando da cama de cima."""
    img = Imagem(62, 46)
    X, Y = img.X, img.Y
    for x in (3, 56):
        img.pintar(img.ret(x, 2, x + 3, 45), "aco", 0.45 + 0.2 * (X == x))
    for y in (14, 36):
        img.pintar(img.ret(3, y, 59, y + 3), "aco", 0.35)
        img.pintar(img.ret(6, y - 5, 56, y), "lona", 0.5 + 0.2 * (Y == y - 5))
        img.pintar(img.ret(7, y - 8, 17, y - 4), "branco", 0.55)
    img.pintar(img.ret(3, 2, 59, 4), "aco", 0.5)
    cobertor = img.poligono([(30, 9), (50, 9), (52, 26), (44, 30), (34, 22)])
    img.pintar(cobertor, "vermelho", 0.45 + 0.15 * (Y < 12))
    img.pintar(img.ret(52, 4, 55, 34), "aco", 0.25)
    for y in range(6, 34, 5):
        img.pintar(img.ret(52, y, 55, y + 1), "aco", 0.6)
    img.contornar()
    return img, 31, 44


def mesa_refeitorio():
    """Mesa comprida de aço com banco na frente, bandejas e latas vazias."""
    img = Imagem(98, 30)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 8, 96, 13), "aco", 0.45 + 0.25 * (Y == 8))
    img.pintar(img.ret(4, 13, 94, 15), "aco", 0.25)
    for x in (6, 88):
        img.pintar(img.ret(x, 15, x + 3, 26), "aco", 0.3)
    img.pintar(img.ret(10, 20, 88, 23), "aco", 0.4 + 0.2 * (Y == 20))
    for x in (14, 84):
        img.pintar(img.ret(x, 23, x + 2, 29), "aco", 0.25)
    for x in (16, 46, 70):
        img.pintar(img.ret(x, 5, x + 14, 8), "branco", 0.45)
    for x in (34, 38, 62):
        img.pintar(img.ret(x, 2, x + 3, 8), "aco", 0.6 + 0.2 * (X == x))
    img.contornar()
    return img, 49, 28


def maca():
    """Maca de enfermaria: colchão fino de lona clara num estrado de aço,
    com rodinhas e a cabeceira levantada."""
    img = Imagem(66, 28)
    X, Y = img.X, img.Y
    img.pintar(img.ret(4, 12, 62, 15), "aco", 0.45)
    img.pintar(img.ret(6, 8, 60, 12), "branco", 0.55 + 0.2 * (Y == 8))
    img.pintar(img.poligono([(6, 8), (8, 2), (20, 2), (18, 8)]), "branco", 0.62)
    img.pintar(img.ret(24, 7, 40, 9), "vermelho", 0.35)
    for x in (8, 56):
        img.pintar(img.ret(x, 15, x + 2, 24), "aco", 0.35)
        img.pintar(img.elipse(x + 1, 25, 2.2, 2.2), "aco", 0.15)
    img.contornar()
    return img, 33, 26


def suporte_soro():
    img = Imagem(14, 44)
    img.pintar(img.ret(6, 4, 8, 40), "aco", 0.55)
    img.pintar(img.ret(2, 4, 12, 5), "aco", 0.55)
    img.pintar(img.ret(2, 6, 6, 14), "vidro", 0.7)
    img.pintar(img.ret(3, 10, 5, 14), "vermelho", 0.4)
    img.pintar(img.ret(3, 14, 4, 26), "vidro", 0.6)
    img.pintar(img.ret(1, 40, 13, 42), "aco", 0.35)
    img.contornar()
    return img, 7, 42


def biombo():
    """Biombo de três folhas com pano claro, a do meio mais para trás."""
    img = Imagem(52, 40)
    X, Y = img.X, img.Y
    for i, x0 in enumerate((2, 18, 34)):
        dy = 2 if i == 1 else 0
        img.pintar(img.ret(x0, 2 + dy, x0 + 16, 34 + dy), "aco", 0.4)
        img.pintar(img.ret(x0 + 1, 4 + dy, x0 + 15, 32 + dy), "branco", 0.5 - 0.1 * (i == 1) + 0.1 * ((X - x0) % 4 == 0))
        img.pintar(img.ret(x0 + 1, 34 + dy, x0 + 3, 38), "aco", 0.3)
    img.contornar()
    return img, 26, 38


def gerador():
    """Gerador a diesel: o bloco do motor verde-oliva, o radiador com a
    grade, o escapamento subindo, os mostradores e a placa de perigo."""
    img = Imagem(84, 56)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 44, 82, 54), "aco", 0.25 + 0.2 * (Y == 44))
    img.pintar(img.ret(6, 18, 60, 44), "tinta", 0.5 + 0.2 * (Y == 18) - 0.15 * (X > 54))
    img.pintar(img.ret(60, 14, 80, 44), "aco", 0.35)
    for y in range(17, 42, 3):
        img.pintar(img.ret(62, y, 78, y + 1), "aco", 0.1)
    img.pintar(img.ret(14, 4, 19, 18), "aco", 0.4 + 0.2 * (X == 14))
    img.pintar(img.ret(12, 2, 21, 5), "aco", 0.3)
    for x in (24, 34):
        img.pintar(img.elipse(x, 27, 3.5, 3.5), "branco", 0.6)
        img.pintar(img.linha(x, 27, x + 2, 25, 0.4), "vermelho", 0.6)
    img.pintar(img.poligono([(47, 24), (43, 32), (51, 32)]), "amarelo", 0.85)
    img.pintar(img.ret(10, 36, 56, 38), "aco", 0.3)
    img.cor(img.ret(40, 26, 42, 28), LED_VERDE)
    img.contornar()
    return img, 42, 54


def tambor(cor="vermelho"):
    img = Imagem(18, 28)
    X, Y = img.X, img.Y
    corpo = img.ret(2, 3, 16, 27)
    img.pintar(corpo, cor, 0.35 + 0.35 * (1 - np.abs(X - 7) / 8))
    for y in (8, 20):
        img.pintar(img.ret(2, y, 16, y + 1), cor, 0.15)
    img.pintar(img.elipse(9, 3, 7, 2), cor, 0.7)
    img.pintar(img.elipse(11, 3, 1.5, 1), "aco", 0.1)
    img.contornar()
    return img, 9, 26


def tambor_verde():
    return tambor("tinta")


def caixas():
    """Pilha de caixotes de madeira com a marca pintada e uma caixa
    militar verde por cima."""
    img = Imagem(44, 38)
    X, Y = img.X, img.Y
    for (x0, y0, x1, y1) in ((2, 16, 22, 36), (22, 18, 42, 36)):
        bib.madeira(img, img.ret(x0, y0, x1, y1), 0.45, x0 + 300)
        img.pintar(img.ret(x0, y0, x1, y0 + 1) | img.ret(x0, y1 - 1, x1, y1), "madeira", 0.25)
        img.pintar(img.linha(x0, y0, x1, y1, 0.5) & img.ret(x0, y0, x1, y1), "madeira", 0.3)
    img.pintar(img.ret(8, 4, 34, 16), "tinta", 0.5 + 0.2 * (Y == 4))
    img.pintar(img.ret(12, 8, 30, 11), "amarelo", 0.4)
    img.pintar(img.ret(18, 2, 24, 4), "aco", 0.5)
    img.contornar()
    return img, 22, 36


def rack_servidor():
    """Rack de servidores: armário preto alto com as gavetas dos
    equipamentos e os LEDs verdes, âmbar e vermelhos piscando (na cena, uma
    luz fraca verde por cima dá o brilho)."""
    img = Imagem(26, 62)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 2, 24, 60), "aco", 0.14 + 0.1 * (X == 2))
    rng = np.random.default_rng(260)
    for y in range(6, 56, 5):
        img.pintar(img.ret(4, y, 22, y + 4), "aco", 0.25 + 0.1 * (Y == y))
        for x in range(6, 20, 3):
            if rng.random() < 0.55:
                img.cor(img.ret(x, y + 1, x + 1, y + 2), [LED_VERDE, LED_AMBAR, LED_VERDE, LED_VERMELHO][int(rng.integers(0, 4))])
    img.pintar(img.ret(2, 58, 24, 60), "aco", 0.3)
    img.contornar()
    return img, 13, 60


def colchao():
    """O canto da Clarice: colchão no chão, travesseiro, cobertor roxo (a
    cor da jaqueta dela) e um walkman em cima."""
    img = Imagem(58, 18)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 8, 56, 16), "lona", 0.45 + 0.2 * (Y == 8))
    img.pintar(img.ret(4, 4, 16, 10), "branco", 0.6)
    cobertor = img.poligono([(20, 6), (54, 7), (56, 15), (18, 15)])
    img.pintar(cobertor, bib.hexa("#2a1a3d", "#3d2758", "#553677", "#6a3e9e", "#8766b3"), 0.5 + 0.2 * (Y < 9))
    img.pintar(img.ret(40, 3, 46, 7), "branco", 0.4)
    img.pintar(img.caminho([(46, 5), (50, 4), (52, 6)], 0.5), "aco", 0.1)
    img.contornar()
    return img, 29, 16


def estante_metal():
    """Estante de aço solta, com caixas de papelão e rolos de cabo."""
    img = Imagem(50, 58)
    X, Y = img.X, img.Y
    for x in (3, 45):
        img.pintar(img.ret(x, 2, x + 2, 56), "aco", 0.45)
    rng = np.random.default_rng(270)
    for y in (16, 32, 48):
        img.pintar(img.ret(3, y, 47, y + 2), "aco", 0.4)
        x = 6
        while x < 42:
            w = int(rng.integers(7, 13))
            h = int(rng.integers(6, 12))
            if x + w > 44:
                break
            caixa = img.ret(x, y - h, x + w, y)
            sorteio = rng.random()
            if sorteio < 0.25:
                bib.madeira(img, caixa, 0.55, x + y)
            elif sorteio < 0.7:
                img.pintar(caixa, "areia", 0.55)
            x += w + 1
    img.pintar(img.elipse(20, 53, 6, 3) & ~img.elipse(20, 53, 3, 1.5), "aco", 0.2)
    img.contornar()
    return img, 25, 56


def latas():
    """Latas de comida vazias empilhadas: o que a Clarice come há meses."""
    img = Imagem(24, 14)
    X, Y = img.X, img.Y
    for (x, y) in ((2, 6), (8, 6), (14, 6), (5, 1), (11, 1)):
        img.pintar(img.ret(x, y, x + 6, y + 6), "aco", 0.5 + 0.25 * (X == x))
        img.pintar(img.ret(x, y + 2, x + 6, y + 4), "vermelho" if (x + y) % 2 else "amarelo", 0.5)
    img.pintar(img.poligono([(18, 12), (22, 10), (23, 13)]), "aco", 0.4)
    img.contornar()
    return img, 12, 12


def mesa_metal():
    """Mesa de aço do posto de guarda, com a luminária de braço, papéis
    e um rádio velho."""
    img = Imagem(58, 34)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 14, 56, 18), "aco", 0.45 + 0.25 * (Y == 14))
    img.pintar(img.ret(40, 18, 54, 32), "aco", 0.3)
    for y in (22, 27):
        img.pintar(img.ret(42, y, 52, y + 1), "aco", 0.55)
    img.pintar(img.ret(4, 18, 7, 32), "aco", 0.3)
    img.pintar(img.ret(10, 11, 26, 14), "branco", 0.55)
    img.pintar(img.ret(30, 8, 40, 14), "tinta", 0.45)
    img.pintar(img.ret(36, 3, 37, 8), "aco", 0.4)
    img.pintar(img.caminho([(48, 14), (46, 6), (52, 2)], 0.6), "aco", 0.4)
    img.pintar(img.poligono([(50, 1), (56, 3), (54, 6)]), "amarelo", 0.45)
    img.contornar()
    return img, 29, 32


OBJETOS = {
    "beliche": (beliche, (56, 6)),
    "mesa_refeitorio": (mesa_refeitorio, (90, 8)),
    "maca": (maca, (58, 5)),
    "suporte_soro": (suporte_soro, (8, 3)),
    "biombo": (biombo, (48, 4)),
    "gerador": (gerador, (78, 10)),
    "tambor": (tambor, (14, 5)),
    "tambor_verde": (tambor_verde, (14, 5)),
    "caixas": (caixas, (40, 6)),
    "rack_servidor": (rack_servidor, (22, 5)),
    "colchao": (colchao, (52, 6)),
    "estante_metal": (estante_metal, (46, 5)),
    "latas": (latas, (18, 4)),
    "mesa_metal": (mesa_metal, (52, 5)),
}


def main():
    print("Gerando o kit do bunker em", os.path.relpath(PASTA_BUNKER, PASTA_PROJETO))
    paredes = {nome: f() for nome, f in PAREDES.items()}
    for nome, img in paredes.items():
        img.salvar(f"{nome}.png", os.path.join(PASTA_BUNKER, "paredes"))
    chaos = {}
    for nome, f in CHAOS.items():
        img = f()
        img.px = img.px[Y_CHAO:].copy()
        img.h = img.px.shape[0]
        img.salvar(f"{nome}.png", os.path.join(PASTA_BUNKER, "chao"))
        chaos[nome] = img
    objetos = {}
    for nome, (f, pegada) in OBJETOS.items():
        img, px, py = f()
        img.salvar(f"{nome}.png", os.path.join(PASTA_BUNKER, "objetos"))
        print(f"    {nome}: pé em ({px}, {py}) -> offset = Vector2({-px}, {-py}), pegada {pegada}")
        objetos[nome] = img
    if not CATALOGO:
        return
    pasta = PASTA_SCRIPT if CATALOGO == "1" else CATALOGO
    os.makedirs(pasta, exist_ok=True)
    for nome, pecas, colunas in (("bunker_paredes", list(paredes.items()), 5),
                                 ("bunker_chao", list(chaos.items()), 4),
                                 ("bunker_objetos", list(objetos.items()), 5)):
        bib.salvar_png(os.path.join(pasta, f"{nome}.png"), kit.catalogo(pecas, colunas, None))
        print("  catálogo:", f"{nome}.png (não commitar)")


if __name__ == "__main__":
    main()
