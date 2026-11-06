# gerar_escritorio.py — desenha, por código, o KIT DO ESCRITÓRIO: a ala
# administrativa escondida no fim do Labirinto, que o Zane atravessa para
# chegar à câmara selada (docs/fases/labirinto.md, seção 5.1). Uma recepção
# com cadeiras de espera e três salas: o arquivo, a sala de reuniões e a sala
# de segurança.
#
# Mesmo estilo e mesmas medidas do kit do bunker (gerar_bunker.py) e das
# salas antigas (gerar_salas_antigas.py), que este script importa: paleta,
# dithering, contorno, peças de 80 x 112 de parede, 128 px de chão e
# 128 x 64 de chão de fundo.
#
# Como rodar (Python 3 + numpy):
#
#   python assets/modelagem/cenario/gerar_escritorio.py
#
# O que sai (em assets/sprites/cenario/escritorio/):
#   paredes/<peça>.png    80 x 112: um pedaço da parede do fundo
#   paredes/pilar_escritorio.png  16 x 112: o canto da sala
#   paredes/escritorio_lateral.png 16 x 64: a parede do lado, vista de cima
#   chao/<peça>.png       128 x 68 o chão de perto; <peça>_fundo.png 128 x 64
#   objetos/<objeto>.png  os móveis (y-sort); o "pé" de cada um sai no terminal
#   porta/<porta>_abrir_NN.png  os quadros da folha da porta abrindo
#   porta/lampada_trava.png     a lâmpada verde da porta restrita (acesa)
# Com CATALOGO=1 monta folhas com todas as peças nesta pasta. Não commitar.
#
# ---------------------------------------------------------------------------
# O VISUAL DO ESCRITÓRIO
# ---------------------------------------------------------------------------
#
# O bunker é concreto, aço e verde-oliva. O escritório é o contrário: parece
# um lugar de trabalho comum, de um prédio dos anos 80, só que abandonado e
# no escuro, mil anos depois. O que conta isso:
#   - FORRO de placas: a grade de alumínio em T e as placas de fibra, com
#     furinhos. Aqui e ali falta uma placa e aparece o vão escuro com cabos;
#   - parede pintada de CREME em cima e LAMBRI de madeira até a cintura,
#     com a moldura de madeira (o "bate-cadeira") separando os dois;
#   - carpete AZUL-ACINZENTADO de escritório nas salas e PISO VINÍLICO em
#     xadrez bege e marrom na recepção;
#   - os móveis em bege de computador, madeira e plástico MOSTARDA (as
#     cadeiras de espera), as telas de tubo com o brilho verde;
#   - a luz: painéis fluorescentes no forro (as PointLight2D ficam nas
#     cenas, em cima das peças escritorio_luminaria).
#
# O piso vinílico segue a perspectiva do chão: as fileiras de lajotas são as
# mesmas do chão da Biblioteca (bib.FILEIRAS), cada vez mais altas para
# baixo, e as colunas têm 16 px. O xadrez é ((x // 16) + fileira) % 2.
# No chão de fundo, as fileiras têm 16 px e começam 8 px antes (a faixa de
# y 0 a 8 continua a fileira que a peça de perto corta em y = 180), então a
# paridade do xadrez continua a mesma na emenda.
#
# Tudo encaixa sem emenda pelo mesmo truque do kit: ruído cíclico (a grade de
# números sorteados dá a volta na largura da peça) e juntas na coluna 0.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "escritorio")
CATALOGO = os.environ.get("CATALOGO", "")

_spec = importlib.util.spec_from_file_location("gerar_salas_antigas", os.path.join(PASTA_SCRIPT, "gerar_salas_antigas.py"))
antigas = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(antigas)
bunker = antigas.bunker
kit = bunker.kit
bib = kit.bib

Imagem, RAMPAS, SOMBRA, dilatar = bib.Imagem, bib.RAMPAS, bib.SOMBRA, bib.dilatar
ciclico = kit.ruido_ciclico
ciclico_2d = kit.ruido_ciclico_2d
L = 80
Y_CHAO = kit.Y_CHAO
ALTURA = kit.ALTURA
LUZ = kit.LUZ

RAMPAS.update({
    "creme": bib.hexa("#2b271f", "#443e30", "#5f5744", "#7c7259", "#998d6f", "#b3a684", "#cabd99"),
    "teto": bib.hexa("#2c2c29", "#43423d", "#5c5a53", "#76736a", "#8f8b80", "#a6a296"),
    "carpete_azul": bib.hexa("#0d1119", "#141b27", "#1c2636", "#253246", "#2f3f56", "#3b4d66"),
    "mostarda": bib.hexa("#261b05", "#43310a", "#644a10", "#876418", "#a77d22", "#c39831"),
    "bege_pc": bib.hexa("#2f2b23", "#4a4438", "#666050", "#837b68", "#9e9680", "#b7ae95"),
    "tela": bib.hexa("#07120c", "#0c2016", "#123222", "#1b4a31", "#2a6a45", "#46925f"),
    "caneta_azul": bib.hexa("#0c1430", "#16245a", "#253a86"),
})
LED_VERDE = bunker.LED_VERDE
LED_VERMELHO = bunker.LED_VERMELHO
LAMPADA_APAGADA = bib.hexa("#4a1210")[0]
LAMPADA_ACESA = bib.hexa("#8cff9c")[0]

# Porta das salas: o vão vai de XA a XB e começa em YA (em cima fica a placa
# com o nome da sala, um Label na cena). A folha é um AnimatedSprite2D por
# cima da peça, em (0, YA), com QUADROS_PORTA quadros de abrir.
XA, XB, YA = 22, 58, 44
QUADROS_PORTA = 12


# ---------------------------------------------------------------------------
# Paredes
# ---------------------------------------------------------------------------


def forro(img, semente):
    """O forro de placas: a grade de alumínio em T (a cada 40 px e na borda
    de baixo) e as placas com furinhos. Algumas sementes tiram uma placa e
    deixam o vão escuro, com um cabo caindo."""
    X, Y = img.X, img.Y
    fino = ciclico(L, Y_CHAO, 2, 2, 600)
    furos = ((X * 7 + Y * 13) % 11 == 0)
    placa = img.ret(0, 0, L, 17)
    img.pintar(placa, "teto", 0.42 + 0.06 * fino - 0.08 * furos - 0.25 * np.clip((6 - Y) / 6, 0, 1))
    img.pintar(img.ret(0, 16, L, 18) | (placa & (X % 40 == 0)), "teto", 0.62 + 0.15 * (Y == 16))
    if semente % 4 == 1:
        x0 = 44
        img.pintar(img.ret(x0, 0, x0 + 35, 16), "concreto", 0.03 + 0.03 * fino)
        img.pintar(img.caminho([(x0 + 8, 2), (x0 + 11, 12), (x0 + 9, 24)], 0.6), "aco", 0.2)
        img.pintar(img.caminho([(x0 + 22, 3), (x0 + 24, 14)], 0.6), "vermelho", 0.3)
    img.cor(img.ret(0, 18, L, 19), SOMBRA)


def parede_base(semente=0):
    img = Imagem(L, Y_CHAO)
    X, Y = img.X, img.Y
    forro(img, semente)
    fino = ciclico(L, Y_CHAO, 2, 2, 601)
    manchas = ciclico(L, Y_CHAO, 40, 20, 602 + semente)
    escorrido = ciclico(L, Y_CHAO, 4, 40, 603 + semente)
    pintura = img.ret(0, 19, L, 63)
    v = 0.5 + 0.1 * manchas + 0.04 * fino - 0.1 * (escorrido > 0.8) - 0.18 * np.clip((30 - Y) / 11, 0, 1)
    img.pintar(pintura, "creme", v * LUZ / 0.7)
    img.pintar(img.ret(0, 62, L, 66), "nogueira", 0.62 + 0.25 * (Y == 62) - 0.25 * (Y == 65))
    lambri = img.ret(0, 66, L, 100)
    veio = ciclico(L, Y_CHAO, 10, 3, 604)
    img.pintar(lambri, "nogueira", 0.42 + 0.1 * veio + 0.04 * fino - 0.2 * (X % 10 == 0) + 0.08 * (X % 10 == 1))
    img.pintar(img.ret(0, 100, L, Y_CHAO), "nogueira", 0.2 + 0.2 * (Y == 100) + 0.04 * fino)
    img.pintar(img.ret(0, 100, L, Y_CHAO) & (ciclico(L, Y_CHAO, 8, 2, 605) > 0.8), "nogueira", 0.08)
    img.v, img.fino, img.manchas = v, fino, manchas
    return img


def placa_da_porta(img, x0, x1, y0=28):
    """A plaquinha de latão em cima da porta: o nome da sala entra por cima,
    no Godot (Label), como no bunker."""
    img.pintar(img.ret(x0, y0, x1, y0 + 10), "dourado", 0.32)
    img.pintar(img.ret(x0, y0, x1, y0 + 1), "dourado", 0.6)
    img.pintar(img.ret(x0, y0 + 9, x1, y0 + 10), "dourado", 0.15)


def batente(img):
    """O batente de madeira da porta e o vão escuro (a folha fica por cima)."""
    X, Y = img.X, img.Y
    img.pintar(img.ret(XA - 4, YA - 4, XB + 4, Y_CHAO), "nogueira", 0.55 + 0.2 * (Y == YA - 4) + 0.1 * (X == XA - 4))
    vao = img.ret(XA, YA, XB, Y_CHAO)
    img.pintar(vao, "concreto", 0.02 + 0.05 * (Y - YA) / (Y_CHAO - YA))
    img.cor(img.ret(XA, YA, XB, YA + 2), SOMBRA)


def escritorio_lisa():
    return parede_base()


def escritorio_forro_aberto():
    return parede_base(1)


def escritorio_luminaria():
    """Painel fluorescente embutido no forro: a moldura e o difusor em
    quadradinhos (a "colmeia"). Na cena, uma luz fria que pisca."""
    img = parede_base(2)
    X, Y = img.X, img.Y
    img.pintar(img.ret(12, 2, 68, 16), "teto", 0.7)
    difusor = img.ret(14, 4, 66, 14)
    img.pintar(difusor, "fluorescente", 0.75 + 0.25 * ((X % 4 != 0) & (Y % 4 != 0)))
    img.pintar(difusor & (X > 50) & (Y > 9), "fluorescente", 0.3)
    return img


def escritorio_porta():
    img = parede_base(3)
    batente(img)
    placa_da_porta(img, 24, 56)
    return img


def escritorio_porta_restrita():
    """A porta do fundo da recepção: folha de aço com a faixa vermelha, o
    leitor de cartão do lado e a caixinha com as TRÊS LÂMPADAS em cima, uma
    por sala. Desenhadas apagadas; as acesas são sprites na cena."""
    img = parede_base(4)
    X, Y = img.X, img.Y
    img.pintar(img.ret(XA - 4, YA - 4, XB + 4, Y_CHAO), "aco", 0.4 + 0.2 * (Y == YA - 4))
    vao = img.ret(XA, YA, XB, Y_CHAO)
    img.pintar(vao, "concreto", 0.02 + 0.05 * (Y - YA) / (Y_CHAO - YA))
    img.cor(img.ret(XA, YA, XB, YA + 2), SOMBRA)
    img.pintar(img.ret(26, 26, 54, 38), "aco", 0.25 + 0.2 * (Y == 26))
    for x in (31, 40, 49):
        img.cor(img.elipse(x, 32, 2.6, 2.6), LAMPADA_APAGADA)
        img.pintar(img.ret(x - 1, 30, x, 31), "vermelho", 0.6)
    img.pintar(img.ret(62, 70, 68, 80), "aco", 0.2 + 0.2 * (X == 62))
    img.pintar(img.ret(63, 72, 67, 73), "aco", 0.05)
    img.cor(img.ret(64, 77, 66, 78), LED_VERMELHO)
    return img


def escritorio_duto():
    """A boca do duto de serviço no pé da parede, sem a grade: é por aí que
    o Zane sai. Lá dentro, a chapa do duto some no escuro em perspectiva
    (as bordas convergem para o fundo). A grade está encostada do lado."""
    img = parede_base(5)
    X, Y = img.X, img.Y
    img.pintar(img.ret(8, 68, 54, 100), "aco", 0.5 + 0.2 * (Y == 68) - 0.15 * (X == 53))
    boca = img.ret(11, 71, 51, 100)
    img.pintar(boca, "aco", 0.2)
    fundo = img.ret(21, 78, 41, 94)
    img.pintar(fundo, "concreto", 0.01)
    for (a, b) in (((11, 71), (21, 78)), ((51, 71), (41, 78)), ((11, 100), (21, 94)), ((51, 100), (41, 94))):
        img.pintar(img.linha(a[0], a[1], b[0], b[1], 0.6), "aco", 0.4)
    img.pintar(boca & ~fundo & (X > 40), "aco", 0.1)
    img.pintar(boca & ~fundo & (Y > 93), "aco", 0.32)
    tampa = img.poligono([(56, 74), (72, 72), (74, 100), (58, 100)])
    img.pintar(tampa, "aco", 0.45)
    for k in range(6):
        img.pintar(tampa & (np.abs(Y - (77 + 4 * k)) < 0.6), "aco", 0.15)
    return img


def digito(img, x, y, d, cor, s=1):
    """Um número de sete segmentos (a, b, c, d, e, f, g), cada segmento com
    3s de comprimento e s de espessura."""
    seg = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd",
           "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcfgd"}[d]
    c = 3 * s
    pos = {"a": (x + s, y, x + s + c, y + s), "g": (x + s, y + c + s, x + s + c, y + c + 2 * s),
           "d": (x + s, y + 2 * c + 2 * s, x + s + c, y + 2 * c + 3 * s),
           "f": (x, y + s, x + s, y + c + s), "b": (x + c + s, y + s, x + c + 2 * s, y + c + s),
           "e": (x, y + c + 2 * s, x + s, y + 2 * c + 2 * s), "c": (x + c + s, y + c + 2 * s, x + c + 2 * s, y + 2 * c + 2 * s)}
    for nome in seg:
        img.cor(img.ret(*pos[nome]), cor)


def escritorio_senhas():
    """O painel de senhas da recepção: a caixa preta com os números
    vermelhos parados em 019 e, embaixo, o rolo de senhas de papel."""
    img = parede_base(6)
    X, Y = img.X, img.Y
    img.pintar(img.ret(18, 26, 62, 46), "aco", 0.1 + 0.15 * (Y == 26))
    img.pintar(img.ret(21, 29, 59, 43), "aco", 0.03)
    vermelho = bib.hexa("#ff4a32")[0]
    for i, d in enumerate("019"):
        digito(img, 28 + i * 9, 31, d, vermelho)
    img.pintar(img.ret(34, 72, 46, 84), "vermelho", 0.45 + 0.2 * (Y == 72))
    img.pintar(img.ret(37, 84, 43, 92), "branco", 0.8)
    img.pintar(img.ret(37, 92, 43, 93), "branco", 0.4)
    return img


def escritorio_quadro_avisos():
    """Quadro de cortiça com folhas presas por tachinhas: circulares, uma
    escala de plantão e um bilhete arrancado pela metade."""
    img = parede_base(7)
    X, Y = img.X, img.Y
    img.pintar(img.ret(10, 26, 70, 60), "nogueira", 0.55)
    cortica = img.ret(12, 28, 68, 58)
    img.pintar(cortica, "areia", 0.45 + 0.12 * ((X * 5 + Y * 3) % 7 < 2))
    for (x0, y0, x1, y1, tom) in ((15, 31, 29, 49, 0.8), (32, 30, 46, 41, 0.72), (49, 33, 65, 55, 0.78), (32, 44, 44, 56, 0.66)):
        img.pintar(img.ret(x0, y0, x1, y1), "branco", tom)
        for y in range(y0 + 3, y1 - 1, 3):
            img.pintar(img.ret(x0 + 2, y, x1 - 2 - (y % 5), y + 1), "aco", 0.35)
        img.pintar(img.elipse((x0 + x1) / 2, y0 + 1, 1.3, 1.3), "vermelho", 0.8)
    return img


def escritorio_janela():
    """Janela interna com a persiana de lâminas. Algumas lâminas tortas
    deixam ver o escuro do outro lado."""
    img = parede_base(8)
    X, Y = img.X, img.Y
    img.pintar(img.ret(12, 24, 68, 62), "aco", 0.5 + 0.2 * (Y == 24))
    vidro = img.ret(14, 26, 66, 60)
    img.pintar(vidro, "vidro", 0.12)
    laminas = vidro & ((Y - 26) % 3 != 2)
    torta = (np.abs((X - 40) * 0.25 - (Y - 44)) < 1.2) & (X > 30) & (X < 52)
    img.pintar(laminas & ~torta, "bege_pc", 0.55 + 0.15 * ((Y - 26) % 3 == 0))
    img.pintar(img.ret(14, 26, 66, 28), "bege_pc", 0.7)
    img.pintar(img.ret(60, 28, 61, 58), "branco", 0.5)
    return img


def escritorio_relogio():
    """Relógio de parede parado e um certificado emoldurado."""
    img = parede_base(9)
    X, Y = img.X, img.Y
    img.pintar(img.elipse(26, 38, 10, 10), "aco", 0.3)
    mostrador = img.elipse(26, 38, 8.5, 8.5)
    img.pintar(mostrador, "branco", 0.82)
    for a in np.arange(0, 2 * np.pi, np.pi / 6):
        img.pintar(img.elipse(26 + 7 * np.cos(a), 38 + 7 * np.sin(a), 0.6, 0.6), "aco", 0.1)
    img.pintar(img.linha(26, 38, 22, 35, 0.6) | img.linha(26, 38, 29, 31, 0.5), "aco", 0.05)
    img.pintar(img.ret(44, 28, 70, 50), "dourado", 0.5)
    img.pintar(img.ret(46, 30, 68, 48), "branco", 0.76)
    for y in (34, 38, 41):
        img.pintar(img.ret(50, y, 64, y + 1), "aco", 0.4)
    img.pintar(img.elipse(62, 45, 2, 2), "vermelho", 0.6)
    return img


def escritorio_poster():
    """Pôster de filme de 1985: a silhueta de um carro esportivo com as
    portas abertas para cima, rastro de fogo e a grade de neon atrás."""
    img = parede_base(10)
    X, Y = img.X, img.Y
    img.pintar(img.ret(20, 22, 60, 64), "aco", 0.15)
    tela = img.ret(22, 24, 58, 62)
    img.pintar(tela, "vinho", 0.15 + 0.35 * np.clip((Y - 24) / 30, 0, 1))
    img.pintar(tela & ((Y - 40) % 4 == 0) & (Y > 44), "laranja80", 0.6)
    img.pintar(tela & ((X - 40) % 6 == 0) & (Y > 46), "laranja80", 0.45)
    carro = img.poligono([(26, 52), (30, 47), (38, 45), (48, 46), (55, 50), (55, 53), (26, 54)])
    img.pintar(carro, "aco", 0.45 + 0.2 * (Y < 48))
    img.pintar(img.linha(33, 46, 30, 40, 0.6) | img.linha(43, 45, 46, 39, 0.6), "aco", 0.55)
    img.pintar(img.elipse(31, 54, 2, 2) | img.elipse(50, 54, 2, 2), "aco", 0.05)
    img.pintar(img.linha(25, 52, 22, 51, 0.7) | img.linha(25, 54, 22, 55, 0.7), "laranja80", 0.95)
    img.pintar(img.ret(26, 27, 54, 31), "dourado", 0.75)
    return img


def escritorio_arquivo_parede():
    """Parede inteira de gavetas de arquivo, com as etiquetas e os puxadores.
    Uma gaveta ficou aberta, com as pastas para fora."""
    img = parede_base(11)
    X, Y = img.X, img.Y
    img.pintar(img.ret(4, 24, 76, 100), "bege_pc", 0.35)
    for col in range(3):
        for fila in range(5):
            x0, y0 = 6 + col * 23, 26 + fila * 15
            gaveta = img.ret(x0, y0, x0 + 22, y0 + 14)
            img.pintar(gaveta, "bege_pc", 0.55 + 0.15 * (Y == y0) - 0.15 * (X == x0 + 21))
            img.pintar(img.ret(x0 + 7, y0 + 3, x0 + 15, y0 + 6), "branco", 0.7)
            img.pintar(img.ret(x0 + 8, y0 + 9, x0 + 14, y0 + 11), "aco", 0.5)
    img.pintar(img.ret(29, 56, 51, 70), "bege_pc", 0.45)
    for k, x in enumerate(range(31, 49, 3)):
        img.pintar(img.ret(x, 52 - (k % 3), x + 2, 58), ("areia", "branco", "laranja80")[k % 3], 0.6)
    return img


def escritorio_quadro_branco():
    """O quadro branco da sala de reuniões: caixas e setas de caneta azul,
    uma data e, de caneta VERMELHA (a cor do Carlos), um número circulado.
    O texto inteiro aparece em jogo pelo aviso "Ler o quadro"."""
    img = parede_base(12)
    X, Y = img.X, img.Y
    img.pintar(img.ret(6, 24, 74, 64), "aco", 0.55 + 0.2 * (Y == 24))
    quadro = img.ret(8, 26, 72, 62)
    img.pintar(quadro, "branco", 0.86 - 0.1 * (ciclico(L, Y_CHAO, 16, 8, 620) > 0.75))
    for (x0, y0, x1, y1) in ((12, 30, 26, 38), (34, 30, 48, 38), (12, 44, 26, 52)):
        img.pintar(img.ret(x0, y0, x1, y1) & ~img.ret(x0 + 1, y0 + 1, x1 - 1, y1 - 1), "caneta_azul", 0.6)
    img.pintar(img.linha(26, 34, 34, 34, 0.5) | img.linha(19, 38, 19, 44, 0.5), "caneta_azul", 0.6)
    for x in range(14, 24, 2):
        img.pintar(img.ret(x, 33, x + 1, 35), "caneta_azul", 0.4)
    vermelho = bib.hexa("#c8302a")[0]
    for i, d in enumerate("1985"):
        digito(img, 40 + i * 6, 46, d, vermelho)
    img.cor((np.abs(((X + 0.5 - 51.5) / 15) ** 2 + ((Y + 0.5 - 50) / 7) ** 2 - 1) < 0.14) & quadro, vermelho)
    img.pintar(img.ret(20, 62, 60, 64), "aco", 0.4)
    img.pintar(img.ret(26, 61, 32, 62), "caneta_azul", 0.6)
    img.cor(img.ret(36, 61, 42, 62), vermelho)
    return img


def escritorio_monitores():
    """Painel de monitores de tubo da segurança: seis telas com as câmeras
    do subsolo, em verde, e uma só com chuvisco."""
    img = parede_base(13)
    X, Y = img.X, img.Y
    img.pintar(img.ret(4, 22, 76, 92), "aco", 0.2 + 0.15 * (Y == 22))
    rng = np.random.default_rng(630)
    for fila in range(2):
        for col in range(3):
            x0, y0 = 7 + col * 23, 25 + fila * 33
            img.pintar(img.ret(x0, y0, x0 + 21, y0 + 30), "bege_pc", 0.4 + 0.15 * (Y == y0))
            tela = img.ret(x0 + 2, y0 + 2, x0 + 19, y0 + 22)
            if (fila, col) == (1, 2):
                chuvisco = rng.random(tela.shape) < 0.5
                img.pintar(tela, "aco", 0.15 + 0.5 * chuvisco)
            else:
                img.pintar(tela, "tela", 0.35 + 0.15 * ((Y % 2) == 0))
                corredor = img.poligono([(x0 + 6, y0 + 22), (x0 + 9, y0 + 8), (x0 + 12, y0 + 8), (x0 + 15, y0 + 22)])
                img.pintar(tela & corredor, "tela", 0.6)
                if (fila + col) % 2 == 0:
                    img.pintar(tela & img.elipse(x0 + 10.5, y0 + 13, 1.5, 3), "tela", 0.05)
            img.cor(img.ret(x0 + 16, y0 + 25, x0 + 18, y0 + 27), LED_VERDE)
    return img


def escritorio_painel():
    """Quadro de força bege do escritório, com o aviso de choque."""
    img = parede_base(14)
    X, Y = img.X, img.Y
    img.pintar(img.ret(20, 28, 60, 84), "bege_pc", 0.5 + 0.15 * (Y == 28) - 0.12 * (X == 59))
    img.pintar(img.ret(24, 34, 52, 78), "bege_pc", 0.32)
    img.pintar(img.poligono([(56, 36), (52, 43), (60, 43)]), "amarelo", 0.85)
    img.pintar(img.ret(54, 60, 57, 64), "aco", 0.6)
    for x in (26, 34, 42):
        img.pintar(img.ret(x, 17, x + 2, 28), "bege_pc", 0.35)
    return img


def pilar_escritorio():
    """A quina da sala: um pilar pintado de creme, com a cantoneira de
    madeira e o mesmo lambri e rodapé da parede."""
    img = Imagem(16, Y_CHAO)
    X, Y = img.X, img.Y
    fino = ciclico(16, Y_CHAO, 2, 2, 640)
    img.pintar(img.ret(0, 0, 16, 19), "teto", 0.3 + 0.05 * fino)
    img.pintar(img.ret(0, 19, 16, 66), "creme", 0.38 + 0.05 * fino + 0.12 * (X < 3))
    img.pintar(img.ret(0, 62, 16, 66), "nogueira", 0.6)
    img.pintar(img.ret(0, 66, 16, 100), "nogueira", 0.38 + 0.08 * (X < 3))
    img.pintar(img.ret(0, 100, 16, Y_CHAO), "nogueira", 0.2)
    img.pintar(img.ret(13, 19, 16, Y_CHAO), "nogueira", 0.25)
    return img


def escritorio_lateral():
    """A parede do lado vista de cima: o topo da parede creme com a
    moldura de madeira e a face na sombra."""
    img = Imagem(16, kit.ALTURA_FUNDO)
    X, Y = img.X, img.Y
    fino = ciclico_2d(img.w, img.h, 2, 2, 650)
    img.pintar(img.ret(0, 0, 9, img.h), "teto", 0.38 + 0.05 * fino)
    img.pintar(img.ret(7, 0, 9, img.h), "nogueira", 0.55)
    img.pintar(img.ret(9, 0, 13, img.h), "creme", 0.28 + 0.05 * fino)
    img.cor(img.ret(13, 0, 16, img.h) & ((X + Y) % 2 == 0), SOMBRA)
    img.cor(img.ret(13, 0, 14, img.h), SOMBRA)
    return img


PAREDES = {
    "escritorio_lisa": escritorio_lisa,
    "escritorio_forro_aberto": escritorio_forro_aberto,
    "escritorio_luminaria": escritorio_luminaria,
    "escritorio_porta": escritorio_porta,
    "escritorio_porta_restrita": escritorio_porta_restrita,
    "escritorio_duto": escritorio_duto,
    "escritorio_senhas": escritorio_senhas,
    "escritorio_quadro_avisos": escritorio_quadro_avisos,
    "escritorio_janela": escritorio_janela,
    "escritorio_relogio": escritorio_relogio,
    "escritorio_poster": escritorio_poster,
    "escritorio_arquivo_parede": escritorio_arquivo_parede,
    "escritorio_quadro_branco": escritorio_quadro_branco,
    "escritorio_monitores": escritorio_monitores,
    "escritorio_painel": escritorio_painel,
    "pilar_escritorio": pilar_escritorio,
}


# ---------------------------------------------------------------------------
# Portas: a folha abrindo
# ---------------------------------------------------------------------------
#
# A folha gira em volta da dobradiça (à esquerda, em XA) e entra na sala do
# outro lado. Vista de frente, uma folha de largura W girada de um ângulo θ
# aparece com largura W · cos θ (a projeção). O ângulo vai de 0 a 85 graus
# seguindo (1 - cos(π t)) / 2, que começa e termina devagar. Quanto mais
# girada, mais escura: a face pega menos luz (o fator é o próprio cos θ).


def folha_madeira(img, x0, largura, sombra):
    X, Y = img.X, img.Y
    h = Y_CHAO - YA
    folha = img.ret(x0, 0, x0 + largura, h)
    img.pintar(folha, "nogueira", (0.5 + 0.06 * ((X - x0) % 6 == 0)) * sombra + 0.05)
    if largura > 8:
        for (ya, yb) in ((6, 30), (36, 62)):
            almofada = img.ret(x0 + 3, ya, x0 + largura - 3, yb)
            img.pintar(almofada & ~img.ret(x0 + 4, ya + 1, x0 + largura - 4, yb - 1), "nogueira", 0.25 * sombra)
        img.pintar(img.ret(x0 + largura - 5, 34, x0 + largura - 2, 36), "dourado", 0.75 * sombra + 0.1)


def folha_aco(img, x0, largura, sombra):
    X, Y = img.X, img.Y
    h = Y_CHAO - YA
    img.pintar(img.ret(x0, 0, x0 + largura, h), "aco", (0.34 + 0.06 * ((Y % 14) == 0)) * sombra + 0.05)
    img.pintar(img.ret(x0, 28, x0 + largura, 34), "vermelho", 0.55 * sombra + 0.05)
    if largura > 10:
        img.pintar(img.ret(x0 + largura - 6, 38, x0 + largura - 3, 46), "aco", 0.6 * sombra)


def quadros_da_porta(desenhar):
    quadros = []
    largura_vao = XB - XA
    for i in range(QUADROS_PORTA):
        t = i / (QUADROS_PORTA - 1)
        angulo = np.radians(85) * (1 - np.cos(np.pi * t)) / 2
        cosseno = np.cos(angulo)
        img = Imagem(L, Y_CHAO - YA)
        largura = max(2, int(round(largura_vao * cosseno)))
        desenhar(img, XA, largura, 0.45 + 0.55 * cosseno)
        if i > 0:
            img.cor(img.ret(XA + largura, 0, XA + largura + 1, img.h), SOMBRA)
        quadros.append(img)
    return quadros


def quadros_porta_restrita():
    """A porta de aço desliza para dentro da parede, para a direita: a
    folha anda e é cortada na borda XB do vão."""
    quadros = []
    largura_vao = XB - XA
    for i in range(QUADROS_PORTA):
        t = i / (QUADROS_PORTA - 1)
        deslocamento = int(round(largura_vao * (1 - np.cos(np.pi * t)) / 2))
        img = Imagem(L, Y_CHAO - YA)
        folha_aco(img, XA + deslocamento, largura_vao, 1.0)
        img.apagar(img.X >= XB)
        quadros.append(img)
    return quadros


def lampada_trava():
    img = Imagem(7, 7)
    img.cor(img.elipse(3.5, 3.5, 2.8, 2.8), LAMPADA_ACESA)
    img.cor(img.ret(2, 2, 3, 3), bib.hexa("#eaffee")[0])
    return img


def gravar_quadros(nome, quadros, pasta):
    for i, q in enumerate(quadros):
        q.salvar(f"{nome}_abrir_{i:02d}.png", pasta)
    res = f"res://assets/sprites/cenario/escritorio/porta"
    linhas = ['[gd_resource type="SpriteFrames" format=3]', ""]
    for i in range(len(quadros)):
        linhas.append(f'[ext_resource type="Texture2D" path="{res}/{nome}_abrir_{i:02d}.png" id="{i + 1}"]')
    linhas += ["", "[resource]", "animations = [{", '"frames": [{']
    linhas.append("}, {\n".join(f'"duration": 1.0,\n"texture": ExtResource("{i + 1}")' for i in range(len(quadros))) + "\n}],")
    linhas += ['"loop": false,', '"name": &"abrir",', '"speed": 15.0', "}]", ""]
    with open(os.path.join(pasta, f"{nome}_quadros.tres"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(linhas))


# ---------------------------------------------------------------------------
# Chão
# ---------------------------------------------------------------------------


def fileira_de(Y):
    return np.searchsorted(np.array(bib.FILEIRAS), Y, side="right") - 1


FILEIRA_DA_EMENDA = int(fileira_de(np.array([179]))[0])


def piso_vinilico():
    """Lajotas de vinil em xadrez de dois beges, gastas no meio."""
    img = Imagem(128, ALTURA)
    X, Y = img.X, img.Y
    chao = img.ret(0, Y_CHAO, 128, ALTURA)
    fino = ciclico(128, ALTURA, 2, 2, 660)
    manchas = ciclico(128, ALTURA, 32, 10, 661)
    fileira = fileira_de(Y)
    xadrez = ((X // 16) + fileira) % 2 == 0
    perto = np.clip((Y - Y_CHAO) / 20, 0, 1)
    img.pintar(chao & xadrez, "bege80", (0.42 + 0.1 * manchas + 0.04 * fino) * (0.75 + 0.25 * perto))
    img.pintar(chao & ~xadrez, "bege80", (0.27 + 0.08 * manchas + 0.04 * fino) * (0.75 + 0.25 * perto))
    juntas = np.isin(Y, bib.FILEIRAS) | (X % 16 == 0)
    img.pintar(chao & juntas & (Y > Y_CHAO + 1), "marrom80", 0.2, achatar=False)
    img.cor(img.ret(0, Y_CHAO, 128, Y_CHAO + 1), SOMBRA)
    return img


def piso_vinilico_fundo():
    img = Imagem(128, kit.ALTURA_FUNDO)
    X, Y = img.X, img.Y
    fino = ciclico_2d(img.w, img.h, 2, 2, 660)
    manchas = ciclico_2d(img.w, img.h, 32, 16, 661)
    fileira = (Y + 8) // 16 + FILEIRA_DA_EMENDA
    xadrez = ((X // 16) + fileira) % 2 == 0
    tudo = img.ret(0, 0, img.w, img.h)
    img.pintar(tudo & xadrez, "bege80", 0.42 + 0.1 * manchas + 0.04 * fino)
    img.pintar(tudo & ~xadrez, "bege80", 0.27 + 0.08 * manchas + 0.04 * fino)
    img.pintar(tudo & (((Y + 8) % 16 == 0) | (X % 16 == 0)), "marrom80", 0.2, achatar=False)
    return img


def carpete_azul():
    """Carpete de escritório: o laço miúdo em diagonal, manchas de café e o
    caminho mais claro onde todo mundo pisava."""
    img = Imagem(128, ALTURA)
    X, Y = img.X, img.Y
    chao = img.ret(0, Y_CHAO, 128, ALTURA)
    fino = ciclico(128, ALTURA, 2, 2, 670)
    manchas = ciclico(128, ALTURA, 32, 10, 671)
    cafe = ciclico(128, ALTURA, 16, 6, 672) > 0.88
    perto = np.clip((Y - Y_CHAO) / 20, 0, 1)
    img.pintar(chao, "carpete_azul", (0.45 + 0.1 * manchas + 0.06 * fino + 0.08 * ((X + 2 * Y) % 5 == 0) - 0.18 * cafe) * (0.7 + 0.3 * perto))
    img.cor(img.ret(0, Y_CHAO, 128, Y_CHAO + 1), SOMBRA)
    return img


def carpete_azul_fundo():
    img = Imagem(128, kit.ALTURA_FUNDO)
    X, Y = img.X, img.Y
    fino = ciclico_2d(img.w, img.h, 2, 2, 670)
    manchas = ciclico_2d(img.w, img.h, 32, 16, 671)
    cafe = ciclico_2d(img.w, img.h, 16, 8, 672) > 0.88
    img.pintar(img.ret(0, 0, img.w, img.h), "carpete_azul",
               0.45 + 0.1 * manchas + 0.06 * fino + 0.08 * ((X + 2 * Y) % 5 == 0) - 0.18 * cafe)
    return img


CHAOS = {"piso_vinilico": piso_vinilico, "carpete_azul": carpete_azul}
CHAOS_FUNDO = {"piso_vinilico_fundo": piso_vinilico_fundo, "carpete_azul_fundo": carpete_azul_fundo}


# ---------------------------------------------------------------------------
# Objetos: cada função devolve (imagem, x_do_pé, y_do_pé). A PEGADA é o
# retângulo de colisão no chão (largura, altura), em px, e BARREIRA diz se o
# móvel também tapa a visão dos robôs e o caminho deles (camada 8).
# ---------------------------------------------------------------------------


def assento(img, x0, quebrado=False):
    """Uma cadeira de espera de plástico mostarda, vista de frente: o
    encosto arredondado em cima e o assento embaixo."""
    X, Y = img.X, img.Y
    if not quebrado:
        encosto = img.ret(x0, 3, x0 + 18, 15) & ~(img.ret(x0, 3, x0 + 2, 5) | img.ret(x0 + 16, 3, x0 + 18, 5))
        img.pintar(encosto, "mostarda", 0.5 + 0.2 * (Y < 5) - 0.15 * (X > x0 + 15))
        img.pintar(img.ret(x0 + 4, 7, x0 + 14, 8), "mostarda", 0.35)
    else:
        caco = img.poligono([(x0, 9), (x0 + 7, 6), (x0 + 11, 10), (x0 + 18, 8), (x0 + 18, 15), (x0, 15)])
        img.pintar(caco, "mostarda", 0.45)
        img.pintar(img.ret(x0 + 8, 6, x0 + 10, 15), "aco", 0.4)
    img.pintar(img.ret(x0 - 1, 15, x0 + 19, 21), "mostarda", 0.6 + 0.25 * (Y == 15) - 0.2 * (Y == 20))


def cadeiras_espera(quebrada=False):
    """Longarina de três cadeiras de espera presas numa viga de aço."""
    img = Imagem(66, 30)
    for i, x0 in enumerate((3, 24, 45)):
        assento(img, x0, quebrada and i == 1)
    img.pintar(img.ret(2, 21, 64, 24), "aco", 0.45 + 0.2 * (img.Y == 21))
    for x in (6, 58):
        img.pintar(img.ret(x, 24, x + 2, 28), "aco", 0.35)
        img.pintar(img.ret(x - 3, 28, x + 5, 29), "aco", 0.3)
    img.contornar()
    return img, 33, 28


def cadeiras_espera_quebrada():
    return cadeiras_espera(True)


def balcao_recepcao():
    """O balcão da recepção: frente de lambri, o tampo alto de fórmica, a
    sineta, o telefone e as costas do monitor de tubo."""
    img = Imagem(112, 48)
    X, Y = img.X, img.Y
    frente = img.ret(2, 20, 110, 46)
    img.pintar(frente, "nogueira", 0.42 + 0.06 * (X % 8 == 1) - 0.18 * (X % 8 == 0) - 0.15 * (Y > 43))
    img.pintar(img.ret(0, 14, 112, 20), "bege80", 0.62 + 0.2 * (Y == 14) - 0.2 * (Y == 19))
    img.pintar(img.ret(40, 26, 72, 33), "dourado", 0.45 + 0.2 * (Y == 26))
    img.pintar(img.ret(44, 29, 68, 30), "dourado", 0.2)
    img.pintar(img.ret(70, 0, 96, 14), "bege_pc", 0.45 + 0.15 * (Y == 0) - 0.15 * (X > 92))
    img.pintar(img.ret(76, 3, 90, 9), "bege_pc", 0.3)
    img.pintar(img.elipse(26, 12, 4, 2.5) & (Y < 13), "dourado", 0.7 + 0.2 * (X < 25))
    img.pintar(img.ret(25, 9, 27, 10), "dourado", 0.9)
    img.pintar(img.ret(46, 8, 60, 14), "bege_pc", 0.25)
    img.pintar(img.ret(44, 6, 62, 9), "bege_pc", 0.35 + 0.2 * (Y == 6))
    img.pintar(img.caminho([(60, 10), (64, 13), (68, 12)], 0.5), "aco", 0.2)
    img.pintar(img.ret(8, 10, 20, 14), "branco", 0.7)
    img.contornar()
    return img, 56, 46


def bebedouro():
    """Bebedouro de galão: o garrafão azulado vazio por cima e o gabinete."""
    img = Imagem(18, 46)
    X, Y = img.X, img.Y
    img.pintar(img.elipse(9, 9, 6.5, 8) | img.ret(6, 15, 12, 19), "vidro", 0.55 + 0.3 * (X < 6) * (Y < 12))
    img.pintar(img.ret(3, 19, 15, 44), "bege_pc", 0.55 + 0.15 * (X == 3) - 0.15 * (X == 14))
    img.pintar(img.ret(5, 24, 13, 30), "bege_pc", 0.25)
    img.pintar(img.ret(6, 25, 8, 27), "caneta_azul", 0.9)
    img.pintar(img.ret(10, 25, 12, 27), "vermelho", 0.7)
    img.pintar(img.ret(4, 43, 14, 45), "aco", 0.3)
    img.contornar()
    return img, 9, 44


def planta_seca():
    """Vaso de planta de escritório que ninguém regou por mil anos: talos
    secos, folhas caídas e terra rachada."""
    img = Imagem(24, 42)
    X, Y = img.X, img.Y
    img.pintar(img.poligono([(4, 28), (20, 28), (18, 40), (6, 40)]), "laranja80", 0.35 + 0.15 * (X < 8))
    img.pintar(img.ret(3, 26, 21, 29), "laranja80", 0.5)
    for (pontos, tom) in (([(12, 27), (11, 14), (7, 4)], 0.35), ([(12, 27), (14, 12), (19, 6)], 0.4),
                          ([(12, 27), (12, 18), (9, 12)], 0.3), ([(12, 27), (16, 20), (21, 17)], 0.35)):
        img.pintar(img.caminho(pontos, 0.6), "marrom80", tom)
    for (x, y) in ((6, 5), (19, 7), (9, 13), (21, 18), (14, 11)):
        img.pintar(img.elipse(x, y + 1, 2, 1), "areia", 0.5)
    img.contornar()
    return img, 12, 40


def mesa_centro():
    """Mesinha baixa de espera com as revistas espalhadas."""
    img = Imagem(42, 18)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 6, 40, 10), "nogueira", 0.5 + 0.25 * (Y == 6))
    img.pintar(img.ret(4, 10, 6, 17) | img.ret(36, 10, 38, 17), "nogueira", 0.3)
    for (x0, rampa) in ((7, "vermelho"), (16, "caneta_azul"), (27, "laranja80")):
        img.pintar(img.ret(x0, 3 + (x0 % 2), x0 + 8, 7), rampa, 0.6 + 0.2 * (Y == 3))
    img.contornar()
    return img, 21, 16


def arquivo_aco(aberto=False):
    """Arquivo de aço de quatro gavetas, bege de escritório. No aberto, a
    gaveta de cima saiu e as pastas aparecem."""
    img = Imagem(26, 50)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 4, 24, 48), "bege_pc", 0.4 + 0.15 * (X == 2) - 0.12 * (X == 23))
    img.pintar(img.ret(2, 4, 24, 5), "bege_pc", 0.65)
    for k in range(4):
        y0 = 6 + k * 10 + (3 if aberto and k == 0 else 0)
        img.pintar(img.ret(3, y0, 23, y0 + 9), "bege_pc", 0.55 + 0.15 * (Y == y0) - 0.15 * (Y == y0 + 8))
        img.pintar(img.ret(9, y0 + 2, 17, y0 + 4), "branco", 0.72)
        img.pintar(img.ret(10, y0 + 5, 16, y0 + 7), "aco", 0.55)
    if aberto:
        for k, x in enumerate(range(5, 21, 3)):
            img.pintar(img.ret(x, 2 + (k % 2), x + 2, 9), ("areia", "branco", "laranja80")[k % 3], 0.65)
    img.pintar(img.ret(2, 46, 24, 48), "aco", 0.2)
    img.contornar()
    return img, 13, 48


def arquivo_aco_aberto():
    return arquivo_aco(True)


def mesa_escritorio():
    """Mesa de trabalho: monitor de tubo com o cursor verde ainda piscando,
    teclado, pilha de papel, caneca e o gaveteiro."""
    img = Imagem(62, 42)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 20, 60, 24), "nogueira", 0.55 + 0.25 * (Y == 20))
    img.pintar(img.ret(4, 24, 40, 36), "nogueira", 0.3)
    img.pintar(img.ret(42, 24, 58, 40), "nogueira", 0.42 + 0.12 * (X == 42))
    for y in (27, 32, 37):
        img.pintar(img.ret(44, y, 56, y + 1), "nogueira", 0.2)
        img.pintar(img.ret(48, y + 2, 52, y + 3), "dourado", 0.6)
    img.pintar(img.ret(4, 36, 6, 40), "nogueira", 0.3)
    img.pintar(img.ret(12, 2, 36, 18), "bege_pc", 0.5 + 0.15 * (Y == 2) - 0.15 * (X > 33))
    tela = img.ret(15, 4, 33, 14)
    img.pintar(tela, "tela", 0.22 + 0.1 * ((Y % 2) == 0))
    img.pintar(img.ret(17, 6, 19, 8), "tela", 0.95)
    img.pintar(img.ret(18, 18, 30, 20), "bege_pc", 0.4)
    img.pintar(img.ret(14, 19, 34, 21), "bege_pc", 0.55)
    img.pintar(img.ret(40, 14, 52, 20), "branco", 0.7 + 0.1 * ((Y % 2) == 0))
    img.pintar(img.ret(54, 15, 58, 20), "vermelho", 0.5 + 0.2 * (X == 54))
    img.contornar()
    return img, 31, 40


def cadeira_escritorio():
    """Cadeira giratória de tecido escuro, com o pistão e a base em estrela."""
    img = Imagem(22, 32)
    X, Y = img.X, img.Y
    img.pintar(img.ret(5, 2, 17, 15) & ~(img.ret(5, 2, 6, 3) | img.ret(16, 2, 17, 3)), "carpete_azul", 0.35 + 0.15 * (Y < 4))
    img.pintar(img.ret(3, 15, 19, 20), "carpete_azul", 0.45 + 0.2 * (Y == 15))
    img.pintar(img.ret(10, 20, 12, 26), "aco", 0.4)
    img.pintar(img.linha(11, 26, 3, 29, 0.7) | img.linha(11, 26, 19, 29, 0.7) | img.linha(11, 26, 11, 30, 0.7), "aco", 0.3)
    for x in (3, 11, 19):
        img.pintar(img.elipse(x, 30, 1.5, 1.2), "aco", 0.1)
    img.contornar()
    return img, 11, 30


def mesa_reuniao():
    """A mesa comprida da sala de reuniões, com as pastas abertas, uma
    jarra d'água e os copos virados."""
    img = Imagem(124, 34)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 10, 122, 19), "nogueira", 0.48 + 0.08 * ciclico(124, 34, 4, 2, 680) + 0.2 * (Y == 10))
    img.pintar(img.ret(2, 19, 122, 22), "nogueira", 0.25)
    for x in (8, 112):
        img.pintar(img.ret(x, 22, x + 4, 32), "nogueira", 0.3)
    img.pintar(img.ret(50, 22, 74, 30), "nogueira", 0.2)
    for x0 in (14, 40, 78, 100):
        img.pintar(img.ret(x0, 12, x0 + 12, 16), "branco", 0.72 + 0.1 * (X == x0 + 6))
    img.pintar(img.ret(62, 2, 68, 12), "vidro", 0.6 + 0.25 * (X == 63))
    img.pintar(img.ret(63, 6, 67, 11), "vidro", 0.35)
    for x in (56, 72):
        img.pintar(img.ret(x, 8, x + 3, 12), "vidro", 0.75)
    img.contornar()
    return img, 62, 32


def copiadora():
    """Copiadora bege de escritório, com uma folha atolada para fora."""
    img = Imagem(42, 44)
    X, Y = img.X, img.Y
    img.pintar(img.ret(3, 12, 39, 42), "bege_pc", 0.5 + 0.15 * (X == 3) - 0.15 * (X == 38))
    img.pintar(img.ret(2, 6, 40, 12), "bege_pc", 0.65 + 0.15 * (Y == 6))
    img.pintar(img.ret(6, 15, 24, 19), "aco", 0.25)
    img.cor(img.ret(28, 16, 30, 18), LED_VERMELHO)
    img.pintar(img.ret(32, 15, 36, 19), "aco", 0.5)
    for y in (24, 31):
        img.pintar(img.ret(5, y, 37, y + 6), "bege_pc", 0.4 + 0.12 * (Y == y))
        img.pintar(img.ret(18, y + 2, 24, y + 3), "aco", 0.4)
    img.pintar(img.poligono([(40, 20), (41, 17), (42, 22), (40, 26)]), "branco", 0.8)
    img.pintar(img.ret(10, 2, 30, 6), "branco", 0.72)
    img.contornar()
    return img, 21, 42


def console_seguranca():
    """A mesa do vigia: três monitores de câmera em cima, o teclado, a
    garrafa térmica e o caderno de ocorrências."""
    img = Imagem(80, 46)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 26, 78, 30), "aco", 0.45 + 0.25 * (Y == 26))
    img.pintar(img.ret(4, 30, 76, 44), "aco", 0.22 + 0.1 * (X == 4))
    for x in (10, 38, 66):
        img.pintar(img.ret(x, 33, x + 4, 35), "aco", 0.5)
    for k, x0 in enumerate((6, 29, 52)):
        img.pintar(img.ret(x0, 4, x0 + 22, 24), "bege_pc", 0.45 + 0.15 * (Y == 4) - 0.12 * (X == x0 + 21))
        tela = img.ret(x0 + 2, 6, x0 + 20, 20)
        img.pintar(tela, "tela", 0.4 + 0.12 * ((Y % 2) == 0))
        if k == 1:
            for x in range(x0 + 4, x0 + 18, 5):
                img.pintar(img.ret(x, 14, x + 3, 17), "tela", 0.75)
        else:
            img.pintar(tela & img.poligono([(x0 + 7, 20), (x0 + 10, 9), (x0 + 12, 9), (x0 + 15, 20)]), "tela", 0.7)
    img.pintar(img.ret(26, 23, 52, 26), "bege_pc", 0.55)
    img.pintar(img.ret(4, 18, 6, 26), "vermelho", 0.45 + 0.2 * (X == 4))
    img.pintar(img.ret(58, 22, 72, 26), "laranja80", 0.45)
    img.contornar()
    return img, 40, 44


def lixeira():
    img = Imagem(14, 16)
    X, Y = img.X, img.Y
    img.pintar(img.poligono([(2, 4), (12, 4), (11, 15), (3, 15)]) & ((X + Y) % 3 != 0), "aco", 0.35)
    img.pintar(img.ret(2, 4, 12, 5), "aco", 0.55)
    img.pintar(img.elipse(6, 3, 2.5, 2) | img.elipse(9, 2, 2, 2), "branco", 0.7)
    img.contornar()
    return img, 7, 15


def caixas_papel():
    """Caixas-arquivo de papelão empilhadas, com as etiquetas escritas à
    mão e a tampa de uma delas aberta."""
    img = Imagem(36, 28)
    X, Y = img.X, img.Y
    for (x0, y0, x1, y1) in ((2, 14, 18, 27), (18, 14, 34, 27), (8, 2, 26, 14)):
        img.pintar(img.ret(x0, y0, x1, y1), "areia", 0.5 + 0.15 * (Y == y0) - 0.12 * (X == x1 - 1))
        img.pintar(img.ret(x0 + 4, y0 + 4, x1 - 4, y0 + 8), "branco", 0.72)
        img.pintar(img.ret(x0 + 5, y0 + 5, x1 - 6, y0 + 6), "caneta_azul", 0.5)
    img.pintar(img.poligono([(26, 2), (32, 0), (32, 4), (26, 6)]), "areia", 0.35)
    img.contornar()
    return img, 18, 27


OBJETOS = {
    "cadeiras_espera": (cadeiras_espera, (62, 6), True),
    "cadeiras_espera_quebrada": (cadeiras_espera_quebrada, (62, 6), True),
    "balcao_recepcao": (balcao_recepcao, (108, 10), True),
    "bebedouro": (bebedouro, (12, 4), False),
    "planta_seca": (planta_seca, (14, 4), False),
    "mesa_centro": (mesa_centro, (38, 5), False),
    "arquivo_aco": (arquivo_aco, (24, 6), True),
    "arquivo_aco_aberto": (arquivo_aco_aberto, (24, 6), True),
    "mesa_escritorio": (mesa_escritorio, (58, 8), True),
    "cadeira_escritorio": (cadeira_escritorio, (12, 4), False),
    "mesa_reuniao": (mesa_reuniao, (120, 10), True),
    "copiadora": (copiadora, (38, 8), True),
    "console_seguranca": (console_seguranca, (76, 8), True),
    "lixeira": (lixeira, (8, 3), False),
    "caixas_papel": (caixas_papel, (32, 6), True),
}


def main():
    print("Gerando o kit do escritório em", os.path.relpath(PASTA, PASTA_PROJETO))
    for sub in ("paredes", "chao", "objetos", "porta"):
        os.makedirs(os.path.join(PASTA, sub), exist_ok=True)
    paredes = {nome: f() for nome, f in PAREDES.items()}
    for nome, img in paredes.items():
        img.salvar(f"{nome}.png", os.path.join(PASTA, "paredes"))
    escritorio_lateral().salvar("escritorio_lateral.png", os.path.join(PASTA, "paredes"))
    chaos = {}
    for nome, f in CHAOS.items():
        img = f()
        img.px = img.px[Y_CHAO:].copy()
        img.h = img.px.shape[0]
        img.salvar(f"{nome}.png", os.path.join(PASTA, "chao"))
        chaos[nome] = img
    for nome, f in CHAOS_FUNDO.items():
        img = f()
        img.salvar(f"{nome}.png", os.path.join(PASTA, "chao"))
        chaos[nome] = img
    objetos = {}
    for nome, (f, pegada, barreira) in OBJETOS.items():
        img, px, py = f()
        img.salvar(f"{nome}.png", os.path.join(PASTA, "objetos"))
        print(f"    {nome}: pé em ({px}, {py}) -> offset = Vector2({-px}, {-py}), pegada {pegada}, barreira {barreira}")
        objetos[nome] = img
    pasta_porta = os.path.join(PASTA, "porta")
    gravar_quadros("porta_escritorio", quadros_da_porta(folha_madeira), pasta_porta)
    gravar_quadros("porta_restrita", quadros_porta_restrita(), pasta_porta)
    lampada_trava().salvar("lampada_trava.png", pasta_porta)
    if not CATALOGO:
        return
    pasta = PASTA_SCRIPT if CATALOGO == "1" else CATALOGO
    os.makedirs(pasta, exist_ok=True)
    for nome, pecas, colunas in (("escritorio_paredes", list(paredes.items()), 6),
                                 ("escritorio_chao", list(chaos.items()), 2),
                                 ("escritorio_objetos", list(objetos.items()), 5)):
        bib.salvar_png(os.path.join(pasta, f"{nome}.png"), kit.catalogo(pecas, colunas, None))
        print("  catálogo:", f"{nome}.png (não commitar)")


if __name__ == "__main__":
    main()
