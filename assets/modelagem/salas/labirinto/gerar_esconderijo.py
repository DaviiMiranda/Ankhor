# gerar_esconderijo.py — gera a ARTE do esconderijo do Baltazar no Labirinto:
# a parede falsa que só a lanterna revela e a bagunça de quem vive ali.
#
# Como rodar (Python 3 + numpy):
#
#   python assets/modelagem/salas/labirinto/gerar_esconderijo.py
#
# O que sai:
#   assets/sprites/salas/labirinto/painel_solto.png      64 x 40  as marcas da parede falsa
#   assets/sprites/salas/labirinto/painel_encostado.png  22 x 44  o painel tirado do lugar
#   assets/sprites/cenario/objetos/ninho_baltazar.png    58 x 20  a cama de panos no chão
#   assets/sprites/cenario/objetos/altar_baltazar.png    26 x 38  caixa com velas e uma cruz de vergalhão
#   assets/sprites/cenario/objetos/chapa_estrelas.png    46 x 36  chapa de metal com estrelas riscadas
#   assets/sprites/cenario/objetos/velas_no_chao.png     16 x 12  tocos de vela numa poça de cera
# Com PREVIA=<pasta>, também salva previa_esconderijo.png nessa pasta (não commitar).
#
# ---------------------------------------------------------------------------
# A PAREDE FALSA: UM DESENHO QUE SÓ APARECE NA LUZ
# ---------------------------------------------------------------------------
#
# A entrada do esconderijo é um painel de concreto solto no meio da parede.
# No Godot, os dois blocos da parede falsa são desenhados como qualquer
# parede (topo e frente), e o painel_solto.png vai POR CIMA da frente. Ele é
# quase todo transparente: só tem as emendas do painel e os riscos que o
# Baltazar fez com uma pedra. A opacidade dele no jogo é a força da
# lanterna naquele ponto (ver scripts/sistemas/parede_falsa.gd), então sem
# o feixe apontado a parede parece igual às outras.
#
# Os riscos são o Cruzeiro do Sul, a constelação que um rapaz do Ceará de
# 1750 conhecia de olhar o céu, e uma cruz pequena: o Baltazar marcou a
# porta do único lugar onde se sente seguro com as duas coisas em que
# confia. As estrelas do Cruzeiro estão nas posições aproximadas do céu
# (Gacrux em cima, Acrux embaixo, Mimosa e Delta dos lados e a Intrometida
# entre Acrux e Delta), cada uma riscada como um "+" de 3 px.
#
# As emendas usam o mesmo truque de luz das paredes do Labirinto: luz de
# cima, então a emenda de cima é uma linha escura e a quina de baixo de
# cada emenda é um pixel mais claro (a borda que a luz pega).

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")
PASTA_SALA = os.path.join(PASTA_PROJETO, "assets", "sprites", "salas", "labirinto")
PREVIA = os.environ.get("PREVIA", "")

_spec = importlib.util.spec_from_file_location(
    "gerar_biblioteca",
    os.path.join(PASTA_PROJETO, "assets", "modelagem", "salas", "biblioteca", "gerar_biblioteca.py"))
bib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bib)
Imagem, salvar_png, ruido = bib.Imagem, bib.salvar_png, bib.ruido

BLOCO = 32
ALTURA_PAREDE = 40

# Vinho, a cor do Baltazar (ver docs/historia/personagens/baltazar.md, seção 6).
VINHO = bib.hexa("#1e0a10", "#3a1220", "#5c1e30", "#7e2c40", "#a04458")

# O Cruzeiro do Sul no painel: (x, y) de cada estrela e o tamanho do "+".
CRUZEIRO = {
    "gacrux": (24, 10, 1),
    "acrux": (25, 29, 1),
    "mimosa": (32, 18, 1),
    "delta": (17, 20, 1),
    "intrometida": (22, 25, 0),
}


def estrela(img, x, y, braco, rampa="concreto", valor=0.85):
    """Uma estrela riscada: um '+' com 'braco' px para cada lado (0 = um
    pixel só)."""
    img.pintar(img.ret(x - braco, y, x + braco + 1, y + 1), rampa, valor)
    img.pintar(img.ret(x, y - braco, x + 1, y + braco + 1), rampa, valor)


def painel_solto():
    """As marcas da parede falsa, para ir por cima da frente da parede.
    O painel ocupa x de 7 a 57 e desce até o chão. Fora das marcas, tudo
    transparente."""
    img = Imagem(2 * BLOCO, ALTURA_PAREDE)
    x0, x1, y0 = 7, 57, 3
    img.pintar(img.ret(x0, y0, x1, y0 + 1), "concreto", 0.03)                  # emenda de cima
    img.pintar(img.ret(x0, y0 + 1, x1, y0 + 2), "concreto", 0.5)               # quina que pega luz
    img.pintar(img.ret(x0, y0, x0 + 1, ALTURA_PAREDE), "concreto", 0.03)       # emenda da esquerda
    img.pintar(img.ret(x1 - 2, y0, x1, ALTURA_PAREDE), "concreto", 0.0)        # fresta da direita
    img.pintar(img.ret(x1, y0, x1 + 1, ALTURA_PAREDE), "concreto", 0.45)
    for y in (17, 21, 25):                                                     # onde os dedos puxam
        img.pintar(img.ret(x1 - 5, y, x1 - 2, y + 2), "concreto", 0.08)
    for (a, b) in (((10, 38), (20, 36)), ((30, 38), (44, 37)), ((47, 39), (55, 37))):
        img.pintar(img.linha(a[0], a[1], b[0], b[1], 0.5), "concreto", 0.55)   # arrastado no chão
    gx, gy, _ = CRUZEIRO["gacrux"]
    ax, ay, _ = CRUZEIRO["acrux"]
    mx, my, _ = CRUZEIRO["mimosa"]
    dx, dy, _ = CRUZEIRO["delta"]
    img.pintar(img.linha(gx + 0.5, gy + 0.5, ax + 0.5, ay + 0.5, 0.45), "concreto", 0.6)
    img.pintar(img.linha(dx + 0.5, dy + 0.5, mx + 0.5, my + 0.5, 0.45), "concreto", 0.6)
    for x, y, braco in CRUZEIRO.values():
        estrela(img, x, y, braco)
    img.pintar(img.ret(44, 9, 45, 21), "concreto", 0.8)                        # a cruz
    img.pintar(img.ret(41, 12, 48, 13), "concreto", 0.8)
    return img


def painel_encostado():
    """O painel tirado da parede, encostado no corredor ao lado da
    passagem: uma laje fina de concreto inclinada, com as mesmas marcas."""
    img = Imagem(22, 44)
    fino = ruido(img.w, img.h, 2, 2, 610)
    laje = img.poligono([(5, 2), (19, 0), (21, 44), (2, 44)])
    img.pintar(laje, "concreto", 0.32 + 0.06 * fino - 0.12 * (img.Y / 44))
    img.pintar(laje & img.ret(0, 0, 22, 4), "concreto", 0.55)
    img.pintar(laje & (img.X >= 19), "concreto", 0.14)
    estrela(img, 9, 12, 1)
    estrela(img, 14, 18, 1)
    img.pintar(img.linha(9.5, 12.5, 10.5, 25.5, 0.45), "concreto", 0.6)
    estrela(img, 10, 26, 1)
    img.pintar(img.ret(0, 42, 22, 44) & ~laje, "concreto", 0.02)
    img.contornar()
    return img, 11, 43


def ninho():
    """A cama do Baltazar: panos verdes das divisórias das cabines da
    Biblioteca, um cobertor cor de vinho dobrado e uma trouxa de linho
    servindo de travesseiro. Dobras em linhas escuras."""
    img = Imagem(58, 20)
    fino = ruido(img.w, img.h, 3, 2, 620)
    img.pintar(img.elipse(29, 16, 28, 4), "concreto", 0.02)                    # sombra no chão
    base = img.elipse(28, 13, 26, 6)
    img.pintar(base, "tecido", 0.35 + 0.2 * fino + 0.15 * (img.Y < 11))
    cobertor = img.poligono([(4, 15), (10, 7), (30, 6), (34, 16), (20, 18)])
    img.pintar(cobertor, VINHO, 0.45 + 0.25 * fino - 0.2 * (img.Y > 14))
    for (a, b) in (((12, 9), (16, 15)), ((21, 8), (24, 15)), ((28, 8), (31, 14))):
        img.pintar(img.linha(a[0], a[1], b[0], b[1], 0.5) & cobertor, VINHO, 0.1)
    trouxa = img.elipse(46, 10, 9, 4.5)
    img.pintar(trouxa, "papel", 0.45 + 0.3 * (img.Y < 9))
    img.pintar(img.linha(40, 11, 52, 9, 0.45) & trouxa, "papel", 0.2)
    img.contornar()
    return img, 29, 18


def altar():
    """Um altar feito com o que achou: uma caixa de metal, três velas de
    alturas diferentes com a cera escorrendo pela borda e, atrás, uma cruz
    de dois vergalhões amarrados com uma fita vinho (a fita do cabelo dele
    tem a mesma cor). A luz das velas vem de uma PointLight2D no Godot."""
    img = Imagem(26, 38)
    X, Y = img.X, img.Y
    img.pintar(img.linha(13, 2, 13, 26, 0.7), "ferrugem", 0.5 + 0.2 * (X == 13))
    img.pintar(img.linha(7, 9, 19, 9, 0.7), "ferrugem", 0.55)
    img.pintar(img.ret(12, 8, 15, 11), VINHO, 0.75)
    img.pintar(img.linha(14, 11, 16, 15, 0.45), VINHO, 0.6)
    caixa = img.ret(2, 25, 24, 38)
    img.pintar(caixa, "metal", 0.28 - 0.1 * ((Y - 25) / 13))
    img.pintar(img.ret(2, 25, 24, 27), "metal", 0.5)
    img.pintar(img.ret(5, 30, 21, 31), "metal", 0.12)
    for x, altura in ((5, 6), (11, 10), (18, 4)):
        topo = 25 - altura
        img.pintar(img.ret(x, topo, x + 3, 25), "papel", 0.75 + 0.2 * (X == x))
        img.pintar(img.ret(x + 1, topo - 3, x + 2, topo - 1), "lampada", 0.7)
        img.pintar(img.ret(x + 1, topo - 1, x + 2, topo), "lampada", 1.0)
        img.pintar(img.ret(x, 25, x + 1, 25 + 2 + altura % 3), "papel", 0.7)  # cera escorrida
    img.contornar()
    return img, 13, 37


def chapa_estrelas():
    """Uma chapa de metal encostada na parede, riscada a carvão e giz com o
    céu que o Baltazar lembra: duas constelações ligadas por linhas, a lua
    crescente e um círculo com raios (a luz que ele seguiu)."""
    img = Imagem(46, 36)
    X, Y = img.X, img.Y
    fino = ruido(img.w, img.h, 3, 3, 630)
    chapa = img.poligono([(4, 1), (42, 2), (44, 35), (2, 35)])
    img.pintar(chapa, "metal", 0.22 + 0.08 * fino)
    img.pintar(chapa & img.ret(0, 0, 46, 4), "metal", 0.42)
    for (x, y) in ((6, 4), (40, 5), (6, 31), (41, 31)):
        img.pintar(img.ret(x, y, x + 1, y + 1), "metal", 0.6)                 # rebites
    giz = [(9, 9), (14, 7), (19, 12), (16, 17), (11, 15)]
    img.pintar(img.caminho(giz + [giz[0]], 0.4), "papel", 0.55)
    for x, y in giz:
        estrela(img, x, y, 1, "papel", 0.95)
    outra = [(25, 24), (30, 21), (35, 25), (31, 29)]
    img.pintar(img.caminho(outra, 0.4), "papel", 0.55)
    for x, y in outra:
        estrela(img, x, y, 0, "papel", 0.95)
    lua = img.elipse(35, 10, 4.5, 4.5) & ~img.elipse(37, 9, 4, 4)
    img.pintar(lua, "papel", 0.9)
    sol = img.elipse(12, 27, 3, 3) & ~img.elipse(12, 27, 1.8, 1.8)
    img.pintar(sol, "papel", 0.85)
    for ang in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        x, y = 12 + 4.5 * np.cos(ang), 27 + 4.5 * np.sin(ang)
        img.pintar(img.ret(int(round(x)), int(round(y)), int(round(x)) + 1, int(round(y)) + 1), "papel", 0.7)
    img.pintar(img.ret(2, 34, 44, 36) & ~chapa, "concreto", 0.02)
    img.contornar()
    return img, 23, 35


def velas_no_chao():
    """Três tocos de vela numa poça de cera, no chão perto da cama."""
    img = Imagem(16, 12)
    X = img.X
    img.pintar(img.elipse(8, 10, 7, 2), "papel", 0.55)
    for x, altura in ((3, 4), (7, 6), (11, 3)):
        topo = 10 - altura
        img.pintar(img.ret(x, topo, x + 2, 10), "papel", 0.75 + 0.2 * (X == x))
        img.pintar(img.ret(x, topo - 2, x + 1, topo - 1), "lampada", 0.7)
        img.pintar(img.ret(x, topo - 1, x + 1, topo), "lampada", 1.0)
    img.contornar()
    return img, 8, 11


def main():
    print("Gerando o esconderijo do Baltazar")
    os.makedirs(PASTA_SALA, exist_ok=True)
    painel = painel_solto()
    painel.salvar("painel_solto.png", PASTA_SALA)
    encostado, ex, ey = painel_encostado()
    encostado.salvar("painel_encostado.png", PASTA_SALA)
    print(f"    painel_encostado: pé em ({ex}, {ey}) -> offset = Vector2({-ex}, {-ey})")
    objetos = {"ninho_baltazar": ninho(), "altar_baltazar": altar(),
               "chapa_estrelas": chapa_estrelas(), "velas_no_chao": velas_no_chao()}
    for nome, (img, px, py) in objetos.items():
        img.salvar(f"{nome}.png", PASTA_OBJETOS)
        print(f"    {nome}: pé em ({px}, {py}) -> offset = Vector2({-px}, {-py})")
    if PREVIA:
        frente = Imagem(2 * BLOCO, ALTURA_PAREDE)
        frente.pintar(frente.ret(0, 0, 2 * BLOCO, ALTURA_PAREDE), "concreto", 0.3)
        frente.colar(painel, 0, 0)
        imagens = [frente, encostado] + [img for img, _, _ in objetos.values()]
        largura = sum(i.w for i in imagens) + 4 * len(imagens)
        quadro = Imagem(largura, max(i.h for i in imagens))
        quadro.cor(quadro.ret(0, 0, quadro.w, quadro.h), [24, 24, 32, 255])
        x = 0
        for i in imagens:
            quadro.colar(i, x, quadro.h - i.h)
            x += i.w + 4
        salvar_png(os.path.join(PREVIA, "previa_esconderijo.png"), np.repeat(np.repeat(quadro.px, 4, 0), 4, 1))
        print("  prévia: previa_esconderijo.png (não commitar)")


if __name__ == "__main__":
    main()
