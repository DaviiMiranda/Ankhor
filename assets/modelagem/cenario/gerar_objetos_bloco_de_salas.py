# gerar_objetos_bloco_de_salas.py — desenha por código, pixel a pixel, os
# objetos e itens dos puzzles do Bloco de salas (docs/fases/bloco_de_salas.md).
# Mesmo estilo e mesma paleta do gerar_objetos_biblioteca.py, que é
# importado como módulo (cores, a classe Desenho e a chave de latão).
#
# Como rodar (Python 3 + Pillow):
#   python assets/modelagem/cenario/gerar_objetos_bloco_de_salas.py
#
# O que sai:
#   assets/sprites/itens/molho_de_chaves.png (+ _chao)  o molho de chaves da Clarice
#   assets/sprites/itens/chave_grade.png (+ _chao)     a chave da fita azul (grade da escada)
#   assets/sprites/itens/chave_deposito.png (+ _chao)  a chave do depósito (sala 206)
#   assets/sprites/itens/alicate.png (+ _chao)         o alicate corta-corrente
#   assets/sprites/cenario/objetos/claviculario.png    armário de chaves com cadeado de segredo
#   assets/sprites/cenario/objetos/grade_escada.png    grade de aço do vão da escada, com cadeado
#   assets/sprites/cenario/objetos/corrente_porta.png  corrente e cadeado na porta corta-fogo
#   assets/sprites/cenario/objetos/buraco_chao.png     o buraco no chão da sala 204
#   assets/sprites/cenario/objetos/sirene.png          a sirene vermelha do corredor do térreo
#   assets/sprites/cenario/objetos/caixas_queda.png    o monte de caixas e espuma embaixo do buraco, na 104
#
# Medidas que precisam bater com o kit (gerar_kit.py):
#   - a grade da escada cobre o vão de parede_escada_sobe.png: 53 x 82 px,
#     de x = 14 e y = 30 do azulejo de 80 x 112;
#   - a corrente cobre a abertura de parede_porta.png: 40 x 66 px, de x = 20
#     e y = 46 (o mesmo lugar das tábuas e da grade da Biblioteca).

import importlib.util
import math
import os

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))

_spec = importlib.util.spec_from_file_location(
    "gerar_objetos_biblioteca", os.path.join(PASTA_SCRIPT, "gerar_objetos_biblioteca.py"))
ob = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ob)

Desenho, chave, cor = ob.Desenho, ob.chave, ob.cor
PASTA_ITENS, PASTA_OBJETOS = ob.PASTA_ITENS, ob.PASTA_OBJETOS
CONTORNO, METAL_ESCURO, METAL, METAL_CLARO = ob.CONTORNO, ob.METAL_ESCURO, ob.METAL, ob.METAL_CLARO
LATAO, LATAO_CLARO, LATAO_ESCURO = ob.LATAO, ob.LATAO_CLARO, ob.LATAO_ESCURO
MADEIRA, MADEIRA_CLARA, MADEIRA_ESCURA = ob.MADEIRA, ob.MADEIRA_CLARA, ob.MADEIRA_ESCURA
AZUL, AZUL_ESCURO, ETIQUETA, BEGE_ESCURO = ob.AZUL, ob.AZUL_ESCURO, ob.ETIQUETA, ob.BEGE_ESCURO
VERMELHO, AMARELO = ob.VERMELHO, ob.AMARELO
VERMELHO_ESCURO = cor("#7a2620")
VERMELHO_CLARO = cor("#ff7a5c")
BURACO = cor("#0b0b10")
ENTULHO = cor("#5b5f66")
ENTULHO_CLARO = cor("#80868f")
PAPELAO = cor("#8a6a44")
PAPELAO_CLARO = cor("#a8865a")
PAPELAO_ESCURO = cor("#5e4630")
FITA = cor("#b9a67a")
ESPUMA = cor("#6e5a7a")
ESPUMA_CLARA = cor("#8e7a9a")
ESPUMA_ESCURA = cor("#463a50")
TRANSPARENTE = (0, 0, 0, 0)


def argola(d, cx, cy, raio, c):
    """Anel de arame: os pixels cuja distância ao centro arredonda para o raio."""
    for y in range(cy - raio - 1, cy + raio + 2):
        for x in range(cx - raio - 1, cx + raio + 2):
            if round(math.hypot(x - cx, y - cy)) == raio:
                d.px(x, y, c)


def chave_pendurada(d, x, y, comprimento, c, claro, escuro):
    """Chave de pé, pendurada pela argola: a cabeça 3 x 3 em cima, a haste
    descendo e dois dentes para a direita no fim."""
    d.ret(x - 1, y, x + 1, y + 2, c)
    d.px(x, y + 1, TRANSPARENTE)
    d.px(x - 1, y, claro)
    d.ret(x, y + 3, x, y + 3 + comprimento, c)
    d.px(x + 1, y + 1 + comprimento, escuro)
    d.px(x + 1, y + 3 + comprimento, escuro)


def molho_de_chaves():
    """O molho de chaves do vigia: uma argola grande de arame e cinco chaves
    penduradas, de tamanhos diferentes. Uma delas tem um pedaço de fita azul
    na cabeça (a da grade da escada)."""
    icone = Desenho(16, 16)
    argola(icone, 8, 4, 3, METAL_CLARO)
    for x, comprimento, c in ((3, 6, LATAO), (6, 8, METAL), (9, 7, LATAO), (12, 5, METAL), (14, 6, LATAO)):
        chave_pendurada(icone, x, 7, comprimento, c, LATAO_CLARO if c == LATAO else METAL_CLARO,
                        LATAO_ESCURO if c == LATAO else METAL_ESCURO)
    icone.ret(8, 7, 10, 9, AZUL)
    icone.px(9, 8, TRANSPARENTE)
    icone.salvar(PASTA_ITENS, "molho_de_chaves.png")
    chao = Desenho(10, 5)
    argola(chao, 2, 2, 2, METAL_CLARO)
    chao.ret(4, 2, 9, 2, LATAO)
    chao.ret(4, 4, 8, 4, METAL)
    chao.px(6, 3, AZUL)
    chao.salvar(PASTA_ITENS, "molho_de_chaves_chao.png")


def chave_grade():
    """A chave da grade da escada, tirada do molho: chave de latão com uma
    volta de fita isolante azul na argola, para achar no escuro."""
    icone = Desenho(16, 16)
    chave(icone, 2, 6)
    icone.ret(1, 5, 4, 10, AZUL)
    icone.ret(1, 5, 4, 5, cor("#5b80c8"))
    icone.ret(1, 10, 4, 10, AZUL_ESCURO)
    icone.ret(2, 7, 3, 8, TRANSPARENTE)
    icone.salvar(PASTA_ITENS, "chave_grade.png")
    chao = Desenho(10, 4)
    chave(chao, 0, 0)
    chao.ret(0, 0, 1, 3, AZUL)
    chao.salvar(PASTA_ITENS, "chave_grade_chao.png")


def chave_deposito():
    """A chave do depósito, do claviculário da sala dos professores: chave
    de ferro (mais escura que as de latão) com a etiqueta de papel 206."""
    icone = Desenho(16, 16)
    chave(icone, 2, 4)
    for x in range(2, 12):
        for y in range(4, 8):
            if icone.p[x, y] == LATAO:
                icone.px(x, y, METAL)
            elif icone.p[x, y] == LATAO_CLARO:
                icone.px(x, y, METAL_CLARO)
            elif icone.p[x, y] == LATAO_ESCURO:
                icone.px(x, y, METAL_ESCURO)
    icone.ret(1, 9, 9, 14, ETIQUETA)
    icone.ret(1, 14, 9, 14, BEGE_ESCURO)
    icone.ret(2, 11, 8, 11, VERMELHO)
    icone.ret(2, 12, 6, 12, VERMELHO_ESCURO)
    icone.px(2, 8, METAL_CLARO)
    icone.salvar(PASTA_ITENS, "chave_deposito.png")
    chao = Desenho(10, 5)
    chave(chao, 0, 0)
    chao.ret(0, 3, 3, 4, ETIQUETA)
    chao.salvar(PASTA_ITENS, "chave_deposito_chao.png")


def alicate():
    """Alicate corta-corrente (corta-vergalhão): dois cabos compridos com
    as pontas de borracha vermelha e, na outra ponta, a mandíbula curta de
    aço que morde a corrente. Desenhado na diagonal, como numa caixa de
    ferramentas."""
    icone = Desenho(16, 16)
    for i in range(9):
        icone.ret(3 + i, 12 - i, 4 + i, 12 - i, METAL_CLARO)
        icone.ret(5 + i, 13 - i, 6 + i, 13 - i, METAL)
    icone.ret(0, 11, 3, 13, VERMELHO)
    icone.ret(0, 11, 2, 11, VERMELHO_CLARO)
    icone.ret(2, 13, 5, 15, VERMELHO_ESCURO)
    icone.ret(11, 1, 15, 4, METAL_ESCURO)
    icone.ret(11, 1, 14, 1, METAL_CLARO)
    icone.ret(13, 0, 15, 0, METAL_ESCURO)
    icone.px(14, 2, CONTORNO)
    icone.px(13, 3, CONTORNO)
    icone.salvar(PASTA_ITENS, "alicate.png")
    chao = Desenho(14, 4)
    chao.ret(0, 1, 2, 2, VERMELHO)
    chao.ret(3, 1, 10, 1, METAL_CLARO)
    chao.ret(3, 2, 10, 2, METAL)
    chao.ret(11, 0, 13, 3, METAL_ESCURO)
    chao.ret(0, 3, 2, 3, VERMELHO_ESCURO)
    chao.salvar(PASTA_ITENS, "alicate_chao.png")


def claviculario():
    """Claviculário (armário de chaves) de parede: caixa de madeira com a
    porta fechada, a placa CHAVES e um cadeado de latão com três rodinhas
    de número na frente (o cadeado de segredo)."""
    d = Desenho(20, 24)
    d.caixa(0, 0, 19, 23, MADEIRA, MADEIRA_CLARA, MADEIRA_ESCURA)
    d.ret(2, 2, 17, 21, MADEIRA_ESCURA)
    d.ret(3, 3, 16, 20, MADEIRA)
    d.ret(5, 4, 14, 6, ETIQUETA)
    d.ret(6, 5, 13, 5, BEGE_ESCURO)
    d.ret(15, 11, 16, 13, METAL_CLARO)
    d.caixa(7, 12, 14, 20, LATAO, LATAO_CLARO, LATAO_ESCURO)
    argola(d, 10, 11, 2, METAL_CLARO)
    for x in (8, 10, 12):
        d.ret(x, 15, x + 1, 17, CONTORNO)
        d.px(x, 16, ETIQUETA)
    d.salvar(PASTA_OBJETOS, "claviculario.png")


def grade_escada():
    """Grade de aço de enrolar no vão da escada do térreo (53 x 82, o
    tamanho do vão de parede_escada_sobe.png): faixas horizontais como as
    da grade da Biblioteca, a barra de baixo mais grossa e um cadeado de
    latão preso numa argola no chão."""
    d = Desenho(53, 82)
    for y in range(0, 74, 4):
        d.ret(0, y, 52, y + 3, METAL)
        d.ret(0, y, 52, y, METAL_CLARO)
        d.ret(0, y + 3, 52, y + 3, METAL_ESCURO)
    d.caixa(0, 74, 52, 81, METAL_ESCURO, METAL, CONTORNO)
    argola(d, 26, 76, 2, METAL_CLARO)
    d.caixa(23, 77, 29, 81, LATAO, LATAO_CLARO, LATAO_ESCURO)
    d.ret(6, 76, 9, 78, AMARELO)
    d.ret(43, 76, 46, 78, AMARELO)
    d.salvar(PASTA_OBJETOS, "grade_escada.png")


def corrente_porta():
    """Corrente grossa atravessada na porta corta-fogo (40 x 66, a abertura
    de parede_porta.png), presa nos batentes, com um cadeado grande no meio.
    Cada elo é um anelzinho; os elos alternam entre de frente (anel) e de
    lado (traço), como uma corrente de verdade."""
    d = Desenho(40, 66)
    for y_base, inclinacao in ((28, 6), (40, -6)):
        for i in range(13):
            x = i * 3
            y = y_base + (i * inclinacao) // 13
            if i % 2 == 0:
                d.ret(x, y - 1, x + 3, y + 1, METAL_CLARO)
                d.px(x + 1, y, TRANSPARENTE)
                d.px(x + 2, y, TRANSPARENTE)
                d.ret(x, y + 1, x + 3, y + 1, METAL_ESCURO)
            else:
                d.ret(x, y, x + 3, y, METAL)
                d.ret(x, y + 1, x + 3, y + 1, METAL_ESCURO)
    d.caixa(15, 34, 24, 44, LATAO, LATAO_CLARO, LATAO_ESCURO)
    argola(d, 19, 33, 3, METAL_CLARO)
    d.ret(19, 38, 20, 40, CONTORNO)
    d.salvar(PASTA_OBJETOS, "corrente_porta.png")


def buraco_chao():
    """O buraco no chão da sala 204, visto de cima e de lado (a mesma
    perspectiva do chão): uma elipse preta achatada, a borda de baixo
    mostrando a grossura da laje, e cacos de concreto em volta."""
    d = Desenho(34, 14)
    cx, cy, rx, ry = 17, 6, 15, 5
    for y in range(14):
        for x in range(34):
            dentro = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if dentro <= 1.0:
                d.px(x, y, BURACO)
            elif dentro <= 1.45:
                d.px(x, y, ENTULHO if y >= cy else ENTULHO_CLARO)
    for x in range(5, 30):
        if ((x - cx) / rx) ** 2 <= 0.8:
            d.px(x, cy + ry - 1, METAL_ESCURO)
    for x, y in ((1, 7), (4, 11), (30, 3), (32, 8), (12, 12), (25, 12)):
        d.ret(x, y, x + 1, y + 1, ENTULHO_CLARO)
    d.salvar(PASTA_OBJETOS, "buraco_chao.png")


def sirene():
    """A sirene de alarme da parede do corredor: uma cúpula vermelha numa
    base de metal presa num suporte. O brilho vem de uma luz do Godot que
    pisca quando ela toca."""
    d = Desenho(11, 9)
    d.ret(4, 0, 6, 1, METAL_ESCURO)
    d.ret(2, 2, 8, 6, VERMELHO)
    d.ret(1, 4, 9, 6, VERMELHO)
    d.ret(3, 2, 7, 2, VERMELHO_CLARO)
    d.px(3, 3, VERMELHO_CLARO)
    d.ret(1, 6, 9, 6, VERMELHO_ESCURO)
    d.caixa(0, 6, 10, 8, METAL, METAL_CLARO, METAL_ESCURO)
    d.salvar(PASTA_OBJETOS, "sirene.png")


def caixas_queda():
    """O monte macio embaixo do buraco, na sala 104: caixas de papelão
    amassadas e os assentos de espuma de cadeiras velhas, empilhados. É
    onde o Gabriel cai quando desce pelo buraco da 204, e por isso a queda
    faz um baque abafado, e não um estalo. O pé (o ponto que encosta no
    chão) fica no meio da borda de baixo: offset = Vector2(-21, -21)."""
    d = Desenho(42, 22)
    d.caixa(1, 9, 15, 21, PAPELAO, PAPELAO_CLARO, PAPELAO_ESCURO)
    d.ret(2, 14, 14, 14, PAPELAO_ESCURO)
    d.caixa(25, 11, 40, 21, PAPELAO, PAPELAO_CLARO, PAPELAO_ESCURO)
    d.ret(31, 12, 33, 20, FITA)
    d.caixa(8, 2, 22, 11, PAPELAO_CLARO, ETIQUETA, PAPELAO)
    d.ret(9, 6, 21, 6, PAPELAO_ESCURO)
    d.caixa(13, 12, 30, 19, ESPUMA, ESPUMA_CLARA, ESPUMA_ESCURA)
    d.caixa(16, 16, 34, 21, ESPUMA_ESCURA, ESPUMA, CONTORNO)
    for x, y in ((18, 13), (24, 14), (27, 17), (20, 18)):
        d.px(x, y, ESPUMA_CLARA)
    d.salvar(PASTA_OBJETOS, "caixas_queda.png")


if __name__ == "__main__":
    print("Gerando os objetos do Bloco de salas:")
    molho_de_chaves()
    chave_grade()
    chave_deposito()
    alicate()
    claviculario()
    grade_escada()
    corrente_porta()
    buraco_chao()
    sirene()
    caixas_queda()
