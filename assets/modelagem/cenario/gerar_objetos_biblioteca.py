# gerar_objetos_biblioteca.py — desenha por código, pixel a pixel, os
# objetos e itens dos sistemas da fase da Biblioteca (docs/fases/biblioteca.md).
# São placeholders: pequenos, legíveis e na paleta fria do jogo, até a arte
# final ficar pronta.
#
# Como rodar (Python 3 + Pillow):
#   python assets/modelagem/cenario/gerar_objetos_biblioteca.py
#
# O que sai:
#   assets/sprites/itens/chave_manutencao.png        ícone 16 x 16 do inventário
#   assets/sprites/itens/chave_manutencao_chao.png   a chave caída (9 x 4)
#   assets/sprites/itens/disquete_clarice.png        ícone 16 x 16
#   assets/sprites/itens/disquete_clarice_chao.png   o disquete na mesa (7 x 4)
#   assets/sprites/cenario/objetos/quadro_energia.png       caixa de disjuntores na parede
#   assets/sprites/cenario/objetos/quadro_chaves.png        quadro de chaves com um gancho vazio
#   assets/sprites/cenario/objetos/telefone.png             telefone bege de mesa
#   assets/sprites/cenario/objetos/painel_codigo.png        teclado da grade, apagado
#   assets/sprites/cenario/objetos/painel_codigo_aceso.png  o mesmo, com energia
#   assets/sprites/cenario/objetos/grade_aco.png            a grade de aço da ala leste
#   assets/sprites/cenario/objetos/tabuas_porta.png         tábuas da porta barrada
#
# A grade e as tábuas têm o tamanho da abertura da porta de parede_porta.png
# (40 x 66 px, que começa em x = 20 e y = 46 do azulejo de 80 x 112): no
# Godot, ficam por cima da porta, no mesmo lugar.
#
# Como cada desenho é feito: começa com uma imagem transparente e pinta
# retângulos (ret) e pixels (px) com cores de uma paleta curta. O volume vem
# de duas regras da pixel art: a borda de cima e da esquerda é mais clara
# (a luz vem do alto, da esquerda) e a de baixo e da direita é mais escura.

import os

from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")


def cor(hexa):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


CONTORNO = cor("#16161c")
METAL_ESCURO = cor("#3a3f48")
METAL = cor("#5e6670")
METAL_CLARO = cor("#8d96a1")
LATAO = cor("#9c7d3a")
LATAO_CLARO = cor("#c9a85a")
LATAO_ESCURO = cor("#5a451d")
MADEIRA = cor("#6b4a30")
MADEIRA_CLARA = cor("#8a6440")
MADEIRA_ESCURA = cor("#43301f")
BEGE = cor("#cfc5a9")
BEGE_ESCURO = cor("#9e9479")
AZUL = cor("#3d5fa8")
AZUL_ESCURO = cor("#25386a")
ETIQUETA = cor("#e4dccb")
CANETA = cor("#c63f8c")
VERMELHO = cor("#c2453a")
VERDE_LED = cor("#7cf09a")
APAGADO = cor("#2a2e36")
AMARELO = cor("#d6b43a")


class Desenho:
    def __init__(self, largura, altura):
        self.img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
        self.p = self.img.load()

    def px(self, x, y, c):
        if 0 <= x < self.img.width and 0 <= y < self.img.height:
            self.p[x, y] = c

    def ret(self, x0, y0, x1, y1, c):
        """Retângulo cheio de (x0, y0) até (x1, y1), inclusive."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def caixa(self, x0, y0, x1, y1, meio, claro, escuro):
        """Retângulo com volume: miolo, borda clara em cima e à esquerda,
        escura embaixo e à direita, e contorno em volta."""
        self.ret(x0, y0, x1, y1, CONTORNO)
        self.ret(x0 + 1, y0 + 1, x1 - 1, y1 - 1, meio)
        self.ret(x0 + 1, y0 + 1, x1 - 1, y0 + 1, claro)
        self.ret(x0 + 1, y0 + 1, x0 + 1, y1 - 1, claro)
        self.ret(x0 + 1, y1 - 1, x1 - 1, y1 - 1, escuro)
        self.ret(x1 - 1, y0 + 1, x1 - 1, y1 - 1, escuro)

    def salvar(self, pasta, nome):
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, nome)
        self.img.save(caminho)
        print("  salvo:", os.path.relpath(caminho, PASTA_PROJETO))


def chave(d, x, y):
    """Chave de latão deitada: a argola (um anel 4 x 4), a haste e os dentes."""
    d.ret(x, y, x + 3, y + 3, LATAO)
    d.px(x + 1, y + 1, (0, 0, 0, 0))
    d.px(x + 2, y + 1, (0, 0, 0, 0))
    d.px(x + 1, y + 2, (0, 0, 0, 0))
    d.px(x + 2, y + 2, (0, 0, 0, 0))
    d.px(x, y, LATAO_CLARO)
    d.ret(x + 4, y + 1, x + 9, y + 2, LATAO)
    d.ret(x + 4, y + 1, x + 9, y + 1, LATAO_CLARO)
    d.px(x + 7, y + 3, LATAO_ESCURO)
    d.px(x + 9, y + 3, LATAO_ESCURO)


def chave_manutencao():
    icone = Desenho(16, 16)
    chave(icone, 2, 6)
    # Etiqueta de papel presa na argola: "MANUT."
    icone.ret(1, 10, 6, 14, ETIQUETA)
    icone.ret(2, 12, 5, 12, AZUL_ESCURO)
    icone.ret(1, 14, 6, 14, BEGE_ESCURO)
    icone.salvar(PASTA_ITENS, "chave_manutencao.png")
    chao = Desenho(10, 4)
    chave(chao, 0, 0)
    chao.salvar(PASTA_ITENS, "chave_manutencao_chao.png")


def disquete(d, x0, y0, tamanho):
    """Disquete de 3,5": corpo azul, o obturador de metal em cima e a
    etiqueta branca embaixo, com a letra da Clarice em rosa."""
    x1, y1 = x0 + tamanho - 1, y0 + tamanho - 1
    d.caixa(x0, y0, x1, y1, AZUL, cor("#5a7cc4"), AZUL_ESCURO)
    meio = (x0 + x1) // 2
    d.ret(meio - tamanho // 5, y0 + 1, meio + tamanho // 5, y0 + tamanho // 3, METAL_CLARO)
    d.ret(x0 + 2, y1 - tamanho // 3, x1 - 2, y1 - 1, ETIQUETA)
    if tamanho >= 12:
        d.ret(x0 + 3, y1 - tamanho // 3 + 1, x1 - 4, y1 - tamanho // 3 + 1, CANETA)


def disquete_clarice():
    icone = Desenho(16, 16)
    disquete(icone, 1, 1, 14)
    icone.salvar(PASTA_ITENS, "disquete_clarice.png")
    chao = Desenho(7, 4)
    chao.ret(0, 0, 6, 3, AZUL)
    chao.ret(0, 0, 6, 0, cor("#5a7cc4"))
    chao.ret(2, 0, 4, 1, METAL_CLARO)
    chao.ret(1, 3, 5, 3, ETIQUETA)
    chao.salvar(PASTA_ITENS, "disquete_clarice_chao.png")


def quadro_energia():
    """Caixa de disjuntores de metal: a porta aberta mostra quatro alavancas
    pretas em fila, com um aviso amarelo de perigo em cima."""
    d = Desenho(24, 32)
    d.caixa(0, 0, 23, 31, METAL, METAL_CLARO, METAL_ESCURO)
    d.ret(3, 3, 20, 7, AMARELO)
    for x in (5, 9, 13, 17):
        d.px(x, 5, CONTORNO)
    d.ret(3, 10, 20, 27, METAL_ESCURO)
    for i in range(4):
        x = 4 + i * 4
        d.ret(x, 14, x + 2, 23, CONTORNO)
        d.ret(x, 20, x + 2, 22, METAL_CLARO)
    d.salvar(PASTA_OBJETOS, "quadro_energia.png")


def quadro_chaves():
    """Quadro de madeira com seis ganchos. Cinco têm chave; o quarto está
    vazio, com a etiqueta embaixo (a pista de que a chave foi devolvida)."""
    d = Desenho(30, 20)
    d.caixa(0, 0, 29, 19, MADEIRA, MADEIRA_CLARA, MADEIRA_ESCURA)
    for i in range(6):
        x = 3 + i * 4
        d.px(x + 1, 4, METAL_CLARO)
        d.ret(x, 15, x + 2, 16, ETIQUETA)
        if i == 3:
            continue
        d.ret(x + 1, 5, x + 1, 11, LATAO)
        d.ret(x, 9, x + 2, 11, LATAO)
        d.px(x + 1, 10, MADEIRA_ESCURA)
    d.ret(15, 15, 17, 16, VERMELHO)
    d.salvar(PASTA_OBJETOS, "quadro_chaves.png")


def telefone():
    """Telefone de mesa bege, com o fone deitado no gancho (o mesmo modelo
    do telefone da estação da Clarice, no bunker)."""
    d = Desenho(14, 9)
    d.caixa(1, 3, 12, 8, BEGE, ETIQUETA, BEGE_ESCURO)
    d.ret(0, 1, 13, 3, BEGE_ESCURO)
    d.ret(1, 1, 12, 1, BEGE)
    d.ret(0, 0, 2, 2, BEGE_ESCURO)
    d.ret(11, 0, 13, 2, BEGE_ESCURO)
    for x in (4, 6, 8):
        d.px(x, 5, BEGE_ESCURO)
        d.px(x + 1, 6, BEGE_ESCURO)
    d.salvar(PASTA_OBJETOS, "telefone.png")


def painel_codigo(aceso):
    """Teclado de parede: uma telinha em cima (verde com energia, escura
    sem) e uma grade de 3 x 4 teclas."""
    d = Desenho(11, 16)
    d.caixa(0, 0, 10, 15, METAL, METAL_CLARO, METAL_ESCURO)
    d.ret(2, 2, 8, 4, VERDE_LED if aceso else APAGADO)
    for linha in range(4):
        for coluna in range(3):
            d.px(2 + coluna * 3, 6 + linha * 2, METAL_CLARO if aceso else METAL_ESCURO)
    d.px(9, 14, VERDE_LED if aceso else VERMELHO)
    d.salvar(PASTA_OBJETOS, "painel_codigo_aceso.png" if aceso else "painel_codigo.png")


def grade_aco():
    """Grade de segurança de enrolar, do tamanho da abertura da porta (40 x
    66): faixas horizontais de aço, cada uma com a borda de cima clara e a
    de baixo escura, e a barra de baixo mais grossa com duas travas."""
    d = Desenho(40, 66)
    for y in range(0, 60, 4):
        d.ret(0, y, 39, y + 3, METAL)
        d.ret(0, y, 39, y, METAL_CLARO)
        d.ret(0, y + 3, 39, y + 3, METAL_ESCURO)
    d.caixa(0, 59, 39, 65, METAL_ESCURO, METAL, CONTORNO)
    d.ret(6, 61, 9, 63, AMARELO)
    d.ret(30, 61, 33, 63, AMARELO)
    d.salvar(PASTA_OBJETOS, "grade_aco.png")


def tabuas_porta():
    """Tábuas pregadas atravessadas na porta (vistas de fora: quem barrou
    foi por dentro, mas as tábuas da reforma antiga ficaram)."""
    d = Desenho(40, 66)
    for y0, inclinacao in ((10, 4), (28, -3), (46, 5)):
        for x in range(40):
            y = y0 + (x * inclinacao) // 40
            d.ret(x, y, x, y + 5, MADEIRA)
            d.px(x, y, MADEIRA_CLARA)
            d.px(x, y + 5, MADEIRA_ESCURA)
        d.px(3, y0 + 2, METAL_CLARO)
        d.px(36, y0 + 2 + (36 * inclinacao) // 40, METAL_CLARO)
    d.salvar(PASTA_OBJETOS, "tabuas_porta.png")


if __name__ == "__main__":
    print("Gerando os objetos da Biblioteca:")
    chave_manutencao()
    disquete_clarice()
    quadro_energia()
    quadro_chaves()
    telefone()
    painel_codigo(False)
    painel_codigo(True)
    grade_aco()
    tabuas_porta()
