# gerar_salas_da_epoca.py — desenha, por código, as peças de três salinhas
# do Corredor do Tempo (Labirinto), cada uma com a cara de uma coisa dos anos
# 80 que o Carlos colecionava (docs/mecanicas/corredor_do_tempo.md):
#
#   - JOGOS: um fliperama no escuro. Parede roxa com dois tubos de neon
#     (magenta em cima, ciano embaixo), um cartaz com um alienígena de 8 bits
#     e o carpete preto com confete neon, aquele dos fliperamas e boliches.
#   - MICROS: um CPD (centro de processamento de dados) de escritório. Parede
#     bege-acinzentada com a faixa laranja de firma, um gabinete de fita
#     magnética embutido (os dois carretéis) e um painel de luzes. O chão é o
#     piso elevado do D-Tec, que já existe.
#   - TELEFONE: uma sala de casa. Lambri de madeira até o teto, a prateleira
#     com as listas telefônicas amarelas, o selo emoldurado do centenário do
#     telefone e o piso de taco. O orelhão e a mesinha com o telefone de disco.
#
# Mesmo estilo e mesmas medidas das salas antigas do bunker
# (gerar_salas_antigas.py), que este script importa: paleta, pontilhado,
# contorno, a laje de concreto por cima (alguém montou as salas dentro do
# subsolo), peças de 80 x 112 de parede e 128 x 68 de chão.
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/salas/labirinto/gerar_salas_da_epoca.py
#
# O que sai (em assets/sprites/cenario/labirinto/salas_da_epoca/):
#   paredes/<peça>.png   80 x 112
#   chao/<peça>.png      128 x 68
#   objetos/<objeto>.png os móveis (y-sort); o "pé" de cada um sai no terminal
#
# - CONFETE DO CARPETE: um "hash" por célula de 4 x 4 px,
#   h = frac(sen(12,9898·cx + 78,233·cy) · 43758,5453), sorteia se a célula
#   tem um pedacinho (h > 0,82) e de que cor (o resto de h em três faixas).
#   É o truque clássico de ruído em shader, sem precisar de gerador aleatório.
# - TACO: o piso é dividido em blocos de 16 x 6 px; em blocos alternados (como
#   um tabuleiro de xadrez) as tábuas correm em pé ou deitadas, e cada bloco
#   ganha um tom próprio pelo mesmo hash.
# - ORELHÃO: a cúpula é uma elipse, e a abertura da frente é outra elipse
#   menor, deslocada para baixo, recortada dela.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "..", ".."))
PASTA = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "labirinto", "salas_da_epoca")

_spec = importlib.util.spec_from_file_location(
    "gerar_salas_antigas", os.path.join(PASTA_PROJETO, "assets", "modelagem", "cenario", "gerar_salas_antigas.py"))
antigas = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(antigas)
kit, bib = antigas.kit, antigas.bib

Imagem, RAMPAS, SOMBRA = bib.Imagem, bib.RAMPAS, bib.SOMBRA
ciclico = kit.ruido_ciclico
L = antigas.L
Y_CHAO = antigas.Y_CHAO
ALTURA = antigas.ALTURA

RAMPAS.update({
    "roxo": bib.hexa("#0c0614", "#140a22", "#1e1032", "#2a1744", "#382058"),
    "magenta": bib.hexa("#3a0a2a", "#6e1452", "#b02a82", "#ec4fb4", "#ff9ad8"),
    "ciano": bib.hexa("#06262e", "#0c4a58", "#178a9c", "#34cfe0", "#a6f6ff"),
    "cpd": bib.hexa("#2e2c26", "#47443b", "#635f52", "#827d6c", "#a29c87", "#bdb7a0"),
    "lambri": bib.hexa("#1a0f07", "#2a180b", "#3c2311", "#4f2f17", "#653d1e", "#7c4c26"),
    "orelhao": bib.hexa("#3a1404", "#6a2606", "#a03c0a", "#d65a12", "#f2802a"),
    "tela_verde": bib.hexa("#041206", "#0a2a0e", "#14501a", "#2a8a30", "#6ae06e"),
})
AMARELO_LISTA = bib.hexa("#f2c62a")[0]
NEON_MAGENTA = bib.hexa("#ffd0f0")[0]
NEON_CIANO = bib.hexa("#e0ffff")[0]
VERDE_ALIEN = bib.hexa("#6ae06e")[0]


def hash2(a, b):
    v = np.sin(a * 12.9898 + b * 78.233) * 43758.5453
    return v - np.floor(v)


def porta_de(parede, rampa_moldura):
    """O vão de porta aberto, igual ao das salas antigas, no estilo de cada sala."""
    img = parede(3)
    X, Y = img.X, img.Y
    xa, xb, ya = 22, 58, 34
    img.pintar(img.ret(xa - 4, ya - 4, xb + 4, Y_CHAO), rampa_moldura, 0.55 + 0.15 * (Y == ya - 4))
    img.pintar(img.ret(xa, ya, xb, Y_CHAO), "concreto", 0.06 + 0.04 * ((Y % 6) == 0))
    img.pintar(img.ret(xa, Y_CHAO - 10, xb, Y_CHAO) & ((X + Y) % 3 == 0), "vermelho", 0.3)
    return img


# ---------------------------------------------------------------------------
# Jogos
# ---------------------------------------------------------------------------


def parede_jogos(semente=0):
    img = Imagem(L, Y_CHAO)
    Y = img.Y
    fino = antigas.laje_do_bunker(img, semente + 20)
    manchas = ciclico(L, Y_CHAO, 40, 20, 600 + semente)
    img.pintar(img.ret(0, 21, L, 100), "roxo", 0.45 + 0.08 * manchas + 0.04 * fino)
    for y0, rampa, nucleo in ((28, "magenta", NEON_MAGENTA), (92, "ciano", NEON_CIANO)):
        img.pintar(img.ret(0, y0 - 2, L, y0 + 4), rampa, 0.35 + 0.25 * (np.abs(Y - y0 - 1) < 2))
        img.cor(img.ret(0, y0, L, y0 + 2), nucleo)
    img.pintar(img.ret(0, 100, L, Y_CHAO), "roxo", 0.15 + 0.15 * (Y == 100))
    return img


def jogos_neon():
    return parede_jogos()


def jogos_cartaz():
    """Um cartaz de fliperama: o alienígena de 8 bits e a fileira de pontos."""
    img = parede_jogos(1)
    img.pintar(img.ret(22, 38, 58, 86), "magenta", 0.5)
    img.cor(img.ret(24, 40, 56, 84), SOMBRA)
    alien = ["..#.....#..",
             "...#...#...",
             "..#######..",
             ".##.###.##.",
             "###########",
             "#.#######.#",
             "#.#.....#.#",
             "...##.##..."]
    for j, linha in enumerate(alien):
        for i, c in enumerate(linha):
            if c == "#":
                img.cor(img.ret(29 + 2 * i, 46 + 2 * j, 31 + 2 * i, 48 + 2 * j), VERDE_ALIEN)
    for i in range(6):
        img.cor(img.ret(28 + 4 * i, 72, 30 + 4 * i, 74), bib.hexa("#f2c62a")[0])
    img.pintar(img.ret(26, 77, 54, 80), "ciano", 0.7)
    return img


def jogos_porta():
    return porta_de(parede_jogos, "magenta")


def carpete_fliperama():
    img = Imagem(128, ALTURA)
    X, Y = img.X, img.Y
    chao = img.ret(0, Y_CHAO, 128, ALTURA)
    fino = ciclico(128, ALTURA, 2, 2, 610)
    img.pintar(chao, "roxo", 0.12 + 0.06 * fino)
    cx, cy = X // 4, (Y - Y_CHAO) // 4
    h = hash2(cx, cy)
    dentro = ((X % 4) < 2) & (((Y - Y_CHAO) % 4) < 2)
    for k, rampa in enumerate(("magenta", "ciano", "amarelo")):
        tom = (h > 0.82) & (np.floor((h - 0.82) / 0.06) == k)
        img.pintar(chao & dentro & tom, rampa, 0.7, achatar=False)
    img.cor(img.ret(0, Y_CHAO, 128, Y_CHAO + 1), SOMBRA)
    return img


def mesa_genius():
    """Um pedestal preto com o Genius em cima: quatro quadrantes coloridos."""
    img = Imagem(28, 34)
    X, Y = img.X, img.Y
    img.pintar(img.ret(6, 12, 22, 32), "roxo", 0.3 + 0.1 * (X == 6))
    img.pintar(img.ret(4, 10, 24, 13), "roxo", 0.5)
    cx, cy = 14.0, 7.0
    disco = img.elipse(cx, cy, 10, 4.5)
    img.cor(disco, bib.hexa("#141414")[0])
    dx, dy = X + 0.5 - cx, Y + 0.5 - cy
    cores = {(False, False): "#2ec24a", (True, False): "#e0303a", (False, True): "#f0c828", (True, True): "#2a6ae0"}
    for (direita, baixo), cor in cores.items():
        quadrante = img.elipse(cx, cy, 8.5, 3.6) & ((dx > 0.5) == direita) & ((dy > 0.3) == baixo)
        quadrante &= (np.abs(dx) > 0.5) & (np.abs(dy) > 0.3)
        img.cor(quadrante, bib.hexa(cor)[0])
    img.cor(img.elipse(cx, cy, 3, 1.4), bib.hexa("#141414")[0])
    img.contornar()
    return img, 14, 32


# ---------------------------------------------------------------------------
# Micros (CPD)
# ---------------------------------------------------------------------------


def parede_cpd(semente=0):
    img = Imagem(L, Y_CHAO)
    Y = img.Y
    fino = antigas.laje_do_bunker(img, semente + 30)
    manchas = ciclico(L, Y_CHAO, 40, 20, 620 + semente)
    img.pintar(img.ret(0, 21, L, 100), "cpd", 0.62 + 0.06 * manchas + 0.04 * fino)
    img.pintar(img.ret(0, 58, L, 61), "laranja80", 0.65 + 0.1 * (Y == 58))
    img.pintar(img.ret(0, 100, L, Y_CHAO), "aco", 0.3 + 0.15 * (Y == 100))
    return img


def micros_lisa():
    return parede_cpd()


def micros_fitas():
    """Gabinete de fita magnética embutido: dois carretéis atrás do vidro."""
    img = parede_cpd(1)
    X, Y = img.X, img.Y
    img.pintar(img.ret(14, 24, 66, 100), "cpd", 0.82 + 0.08 * (X == 14))
    img.pintar(img.ret(18, 28, 62, 66), "vidro", 0.3 + 0.1 * ((X + Y) % 5 == 0))
    for cx in (29, 51):
        img.pintar(img.elipse(cx, 44, 9, 9), "aco", 0.2)
        img.pintar(img.elipse(cx, 44, 6, 6), "marrom80", 0.35)
        img.pintar(img.elipse(cx, 44, 2, 2), "aco", 0.7)
    img.pintar(img.ret(18, 70, 62, 76), "aco", 0.35)
    for i, rampa in enumerate(("vermelho", "amarelo", "tela_verde", "amarelo", "vermelho")):
        img.pintar(img.ret(22 + 8 * i, 72, 25 + 8 * i, 74), rampa, 0.9)
    img.pintar(img.ret(18, 80, 62, 96), "cpd", 0.55 + 0.1 * ((Y % 4) == 0))
    return img


def micros_painel():
    """Painel de luzes do computador grande e uma tela verde de terminal."""
    img = parede_cpd(2)
    X, Y = img.X, img.Y
    img.pintar(img.ret(10, 30, 70, 56), "aco", 0.3 + 0.1 * (Y == 30))
    for j in range(3):
        for i in range(10):
            aceso = hash2(i, j) > 0.45
            img.pintar(img.ret(14 + 6 * i, 34 + 7 * j, 17 + 6 * i, 37 + 7 * j), "vermelho" if aceso else "aco", 0.85 if aceso else 0.2)
    img.pintar(img.ret(26, 66, 54, 92), "cpd", 0.8)
    img.pintar(img.ret(29, 69, 51, 85), "tela_verde", 0.25 + 0.15 * ((Y % 3) == 0))
    for k in range(4):
        img.pintar(img.ret(31, 71 + 3 * k, 31 + 4 + 3 * ((k * 7) % 5), 72 + 3 * k), "tela_verde", 0.9)
    return img


def micros_porta():
    return porta_de(parede_cpd, "aco")


# ---------------------------------------------------------------------------
# Telefone
# ---------------------------------------------------------------------------


def parede_lambri(semente=0):
    img = Imagem(L, Y_CHAO)
    X, Y = img.X, img.Y
    fino = antigas.laje_do_bunker(img, semente + 40)
    veio = ciclico(L, Y_CHAO, 8, 16, 640 + semente)
    tabua = hash2(X // 8, semente)
    img.pintar(img.ret(0, 21, L, 100), "lambri", 0.45 + 0.1 * veio + 0.08 * tabua + 0.03 * fino)
    img.pintar(img.ret(0, 21, L, 100) & ((X % 8) == 0), "lambri", 0.15, achatar=False)
    img.pintar(img.ret(0, 100, L, Y_CHAO), "lambri", 0.25 + 0.2 * (Y == 100))
    return img


def telefone_lambri():
    return parede_lambri()


def telefone_listas():
    """Prateleira com as listas telefônicas amarelas e a agenda."""
    img = parede_lambri(1)
    Y = img.Y
    img.pintar(img.ret(12, 62, 68, 66), "lambri", 0.75 + 0.1 * (Y == 62))
    for i, (largura, altura) in enumerate(((7, 22), (6, 20), (8, 23), (5, 18), (7, 21))):
        x0 = 16 + sum(w + 1 for w, _ in ((7, 22), (6, 20), (8, 23), (5, 18), (7, 21))[:i])
        img.cor(img.ret(x0, 62 - altura, x0 + largura, 62), AMARELO_LISTA)
        img.pintar(img.ret(x0, 62 - altura + 3, x0 + largura, 62 - altura + 5), "marrom80", 0.4)
    img.pintar(img.ret(56, 48, 66, 62), "vinho", 0.5)
    return img


def telefone_selo():
    """O selo do centenário do telefone, emoldurado: um telefone de manivela."""
    img = parede_lambri(2)
    X, Y = img.X, img.Y
    img.pintar(img.ret(26, 34, 54, 70), "dourado", 0.55 + 0.15 * ((X == 26) | (Y == 34)))
    papel = img.ret(29, 37, 51, 67)
    img.pintar(papel, "bege80", 0.9)
    picote = papel & ((X == 29) | (X == 50) | (Y == 37) | (Y == 66)) & (((X + Y) % 2) == 0)
    img.pintar(picote, "lambri", 0.5, achatar=False)
    img.pintar(img.ret(32, 40, 48, 60), "ciano", 0.3)
    img.pintar(img.ret(36, 47, 44, 57), "nogueira", 0.4)
    img.pintar(img.ret(37, 44, 43, 47), "aco", 0.5)
    img.pintar(img.linha(44, 50, 47, 48, 0.5), "aco", 0.6)
    img.pintar(img.ret(32, 61, 48, 64), "vermelho", 0.6)
    return img


def telefone_porta():
    return porta_de(parede_lambri, "lambri")


def taco():
    img = Imagem(128, ALTURA)
    X, Y = img.X, img.Y
    chao = img.ret(0, Y_CHAO, 128, ALTURA)
    yy = Y - Y_CHAO
    bx, by = X // 16, yy // 6
    deitado = ((bx + by) % 2) == 0
    tom = hash2(bx, by)
    img.pintar(chao, "nogueira", 0.42 + 0.14 * tom)
    linhas = np.where(deitado, (yy % 2) == 0, (X % 4) == 0)
    img.pintar(chao & linhas, "nogueira", 0.25, achatar=False)
    img.pintar(chao & (((X % 16) == 0) | ((yy % 6) == 0)), "nogueira", 0.12, achatar=False)
    img.cor(img.ret(0, Y_CHAO, 128, Y_CHAO + 1), SOMBRA)
    return img


def orelhao():
    """O orelhão: a cúpula laranja, o telefone lá dentro e o poste."""
    img = Imagem(34, 70)
    X, Y = img.X, img.Y
    img.pintar(img.ret(15, 36, 19, 68), "aco", 0.45 + 0.15 * (X == 15))
    img.pintar(img.elipse(17, 68, 7, 2), "aco", 0.3)
    cupula = img.elipse(17, 20, 16, 19)
    abertura = img.elipse(17, 26, 11, 14)
    img.pintar(cupula & ~abertura, "orelhao", 0.75 - 0.3 * (Y / 40))
    img.pintar(cupula & abertura, "orelhao", 0.12)
    img.pintar(img.ret(12, 16, 22, 30), "aco", 0.5)
    img.pintar(img.ret(14, 18, 20, 24), "aco", 0.25)
    img.pintar(img.ret(11, 14, 14, 26), "aco", 0.7)
    img.contornar()
    return img, 17, 68


def mesa_telefone():
    """Aparador de madeira com o telefone de disco vermelho."""
    img = Imagem(30, 34)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 14, 28, 18), "lambri", 0.7 + 0.15 * (Y == 14))
    img.pintar(img.ret(4, 18, 7, 32) | img.ret(23, 18, 26, 32), "lambri", 0.5)
    img.pintar(img.ret(5, 26, 25, 28), "lambri", 0.4)
    img.pintar(img.poligono([(8, 14), (10, 7), (20, 7), (22, 14)]), "vermelho", 0.75)
    img.pintar(img.elipse(15, 11, 3.2, 2.4), "bege80", 0.85)
    img.pintar(img.elipse(15, 11, 1, 0.8), "vermelho", 0.6)
    img.pintar(img.ret(7, 4, 23, 7), "vermelho", 0.85 + 0.1 * (Y == 4))
    img.pintar(img.ret(6, 5, 9, 8) | img.ret(21, 5, 24, 8), "vermelho", 0.6)
    img.contornar()
    return img, 15, 32


PAREDES = {
    "jogos_neon": jogos_neon,
    "jogos_cartaz": jogos_cartaz,
    "jogos_porta": jogos_porta,
    "micros_lisa": micros_lisa,
    "micros_fitas": micros_fitas,
    "micros_painel": micros_painel,
    "micros_porta": micros_porta,
    "telefone_lambri": telefone_lambri,
    "telefone_listas": telefone_listas,
    "telefone_selo": telefone_selo,
    "telefone_porta": telefone_porta,
}
CHAOS = {"carpete_fliperama": carpete_fliperama, "taco": taco}
OBJETOS = {
    "mesa_genius": (mesa_genius, (16, 5)),
    "orelhao": (orelhao, (14, 4)),
    "mesa_telefone": (mesa_telefone, (26, 5)),
}


def main():
    print("Gerando as salas da época em", os.path.relpath(PASTA, PASTA_PROJETO))
    for nome, f in PAREDES.items():
        f().salvar(f"{nome}.png", os.path.join(PASTA, "paredes"))
    for nome, f in CHAOS.items():
        img = f()
        img.px = img.px[Y_CHAO:].copy()
        img.h = img.px.shape[0]
        img.salvar(f"{nome}.png", os.path.join(PASTA, "chao"))
    for nome, (f, pegada) in OBJETOS.items():
        img, px, py = f()
        img.salvar(f"{nome}.png", os.path.join(PASTA, "objetos"))
        print(f"    {nome}: pé em ({px}, {py}) -> offset = Vector2({-px}, {-py}), pegada {pegada}")


if __name__ == "__main__":
    main()
