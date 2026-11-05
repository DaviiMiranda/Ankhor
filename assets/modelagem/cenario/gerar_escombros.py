# gerar_escombros.py — desenha por código as peças variadas de escombro, para
# uma sala com desabamento não virar o mesmo sprite carimbado várias vezes.
# Usa a paleta e as ferramentas do gerar_biblioteca.py, importado como módulo
# (o main dele não roda), então combina com o entulho.png original.
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/cenario/gerar_escombros.py
#
# O que sai em assets/sprites/cenario/objetos/ (pé = o ponto que encosta no
# chão, usado no offset do Sprite2D):
#   entulho_monte.png       96 x 48  o monte grande de um desabamento
#   entulho_laje.png        56 x 30  um pedaço de laje tombado, com vergalhões
#   entulho_baixo.png       44 x 16  um montinho de terra e pedra
#   entulho_pedras_a.png    20 x 10  uma pedra grande e um caco (sem colisão)
#   entulho_pedras_b.png    28 x 10  lascas chatas e um ferro solto (sem colisão)
#   entulho_pedras_c.png    30 x 10  três cacos de tamanhos diferentes (sem colisão)
#
# E, em assets/sprites/cenario/chao/, manchas de terra para o chão, por baixo
# dos objetos, com a borda irregular e sem emenda de azulejo:
#   terra_mancha_grande.png 220 x 150
#   terra_mancha_media.png  130 x 70
#   terra_mancha_pequena.png 70 x 34
#
# A forma das manchas: um pixel entra quando
#     ruído(x, y) > d(x, y)
# onde d é a distância normalizada até o centro da elipse (0 no centro, 1 na
# beirada). Perto do centro quase todo pixel passa; perto da beirada só os
# picos do ruído passam, e a borda vira um recorte irregular, com ilhotas.
# É a mesma ideia de um mapa de altura cortado por um nível de água.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")
PASTA_CHAO = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "chao")

_spec = importlib.util.spec_from_file_location(
    "gerar_biblioteca",
    os.path.join(PASTA_PROJETO, "assets", "modelagem", "salas", "biblioteca", "gerar_biblioteca.py"))
bib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bib)

Imagem, ruido, musgo_por_cima = bib.Imagem, bib.ruido, bib.musgo_por_cima


def bloco(img, pontos, tom, semente, lado_sombra=None):
    """Um pedaço de concreto: a máscara do polígono, a textura de ruído, a face
    de cima mais clara (pixels sem nada do mesmo bloco logo acima) e, se pedido,
    o lado direito mais escuro a partir de x = lado_sombra."""
    m = img.poligono(pontos)
    fino = ruido(img.w, img.h, 2, 2, semente)
    valor = tom + 0.12 * fino
    if lado_sombra is not None:
        valor = valor - 0.14 * (img.X > lado_sombra)
    img.pintar(m, "concreto", valor)
    cima = m & ~np.roll(m, 2, axis=0)
    img.pintar(cima, "concreto", tom + 0.22, achatar=False)


def vergalhao(img, pontos):
    """Ferro de construção: uma linha fina, reta ou dobrada, com um ponto de
    luz na ponta para não sumir no escuro."""
    img.pintar(img.caminho(pontos, 0.6), "ferrugem", 0.6)
    x, y = pontos[-1]
    img.pintar(img.ret(int(x), int(y), int(x) + 1, int(y) + 1), "ferrugem", 1.0, achatar=False)


def saia_de_terra(img, cx, base, rx, ry, semente):
    """A terra que escorreu e se acumulou no pé da pilha."""
    d = np.hypot((img.X + 0.5 - cx) / rx, (img.Y + 0.5 - base) / ry)
    m = (ruido(img.w, img.h, 4, 3, semente) * 0.45 + 0.65 > d) & (img.Y < base + 1)
    img.pintar(m, "areia", 0.34 + 0.3 * ruido(img.w, img.h, 3, 2, semente + 1))


def so_a_maior_parte(img):
    """Apaga os pixels soltos: percorre a parte opaca em largura (BFS, com os 8
    vizinhos, porque um vergalhão na diagonal só encosta pelos cantos) a partir
    de cada pixel ainda não visitado e mantém só o maior pedaço. Sem isso, o
    ruído da terra deixa caquinhos flutuando em volta do contorno."""
    opaco = img.opaco()
    visto = np.zeros(opaco.shape, dtype=bool)
    maior = []
    for inicio in zip(*np.nonzero(opaco)):
        if visto[inicio]:
            continue
        visto[inicio] = True
        pedaco = [inicio]
        for y, x in pedaco:
            vizinhos = [(y + dy, x + dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1)]
            for viz in vizinhos:
                if 0 <= viz[0] < img.h and 0 <= viz[1] < img.w and opaco[viz] and not visto[viz]:
                    visto[viz] = True
                    pedaco.append(viz)
        if len(pedaco) > len(maior):
            maior = pedaco
    manter = np.zeros(opaco.shape, dtype=bool)
    for ponto in maior:
        manter[ponto] = True
    img.apagar(opaco & ~manter)


def entulho_monte():
    """O monte de um desabamento: terra na base, blocos de tamanhos diferentes
    empilhados sem ordem e uma placa de laje enfiada em pé no topo."""
    img = Imagem(96, 48)
    saia_de_terra(img, 48, 47, 47, 26, 201)
    bloco(img, [(38, 30), (46, 5), (55, 2), (60, 8), (54, 32)], 0.5, 202, 52)
    bloco(img, [(8, 46), (11, 32), (24, 24), (36, 30), (34, 46)], 0.44, 203, 26)
    bloco(img, [(60, 46), (58, 30), (70, 22), (84, 30), (90, 46)], 0.4, 204, 74)
    bloco(img, [(26, 34), (31, 20), (45, 16), (56, 24), (52, 38)], 0.56, 205, 44)
    bloco(img, [(50, 38), (56, 26), (67, 28), (70, 40), (60, 44)], 0.48, 206, 62)
    bloco(img, [(28, 47), (33, 38), (46, 36), (54, 41), (50, 47)], 0.6, 207, 45)
    bloco(img, [(70, 47), (73, 41), (81, 40), (85, 47)], 0.52, 208, 79)
    bloco(img, [(3, 47), (6, 42), (13, 41), (16, 47)], 0.5, 209, 11)
    saia_de_terra(img, 48, 47, 44, 7, 210)
    vergalhao(img, [(47, 8), (41, 2)])
    vergalhao(img, [(58, 8), (66, 4), (69, 9)])
    vergalhao(img, [(26, 24), (19, 15)])
    vergalhao(img, [(78, 28), (86, 22)])
    so_a_maior_parte(img)
    musgo_por_cima(img, 0.28, 211)
    img.contornar()
    return img


def entulho_laje():
    """Um pedaço de laje tombado: uma placa inclinada com a face de baixo à
    mostra e a ponta quebrada, de onde saem os vergalhões."""
    img = Imagem(56, 30)
    saia_de_terra(img, 24, 29, 24, 8, 221)
    face = [(4, 28), (32, 6), (47, 9), (39, 16), (37, 29)]
    bloco(img, face, 0.52, 222, 30)
    img.pintar(img.poligono([(37, 29), (39, 16), (47, 9), (50, 13), (47, 29)]), "concreto",
               0.26 + 0.1 * ruido(img.w, img.h, 2, 2, 223))
    img.pintar(img.caminho([(12, 26), (32, 11)], 0.5), "concreto", 0.3)
    img.pintar(img.caminho([(21, 28), (35, 18)], 0.5), "concreto", 0.32)
    bloco(img, [(39, 29), (42, 23), (49, 23), (53, 29)], 0.48, 224, 47)
    vergalhao(img, [(45, 10), (52, 3)])
    vergalhao(img, [(38, 8), (41, 1), (46, 1)])
    so_a_maior_parte(img)
    musgo_por_cima(img, 0.22, 225)
    img.contornar()
    return img


def entulho_baixo():
    """Um montinho baixo: mais terra do que pedra, sem vergalhão no alto. Não
    tem o desenho de nenhuma das peças altas, então quebra o ritmo entre elas."""
    img = Imagem(44, 16)
    saia_de_terra(img, 22, 15, 21, 12, 231)
    bloco(img, [(7, 14), (10, 8), (18, 7), (20, 14)], 0.46, 232, 15)
    bloco(img, [(22, 15), (25, 10), (33, 11), (36, 15)], 0.54, 233, 31)
    vergalhao(img, [(34, 11), (39, 7)])
    so_a_maior_parte(img)
    musgo_por_cima(img, 0.2, 234)
    img.contornar()
    return img


def entulho_pedras_a():
    """Uma pedra grande, quebrada na diagonal, e um caco ao lado."""
    img = Imagem(20, 10)
    bloco(img, [(1, 9), (2, 5), (6, 1), (12, 2), (13, 9)], 0.5, 241, 8)
    bloco(img, [(14, 9), (15, 6), (18, 7), (19, 9)], 0.42, 242, 17)
    img.contornar()
    return img


def entulho_pedras_b():
    """Duas lascas chatas de laje, compridas, e um pedaço de vergalhão solto."""
    img = Imagem(28, 10)
    bloco(img, [(1, 7), (4, 4), (13, 5), (12, 7)], 0.54, 243, 9)
    bloco(img, [(12, 9), (15, 7), (24, 6), (26, 9)], 0.44, 244, 21)
    img.pintar(img.caminho([(3, 9), (9, 8)], 0.5), "ferrugem", 0.6)
    img.contornar()
    return img


def entulho_pedras_c():
    """Três cacos angulosos, um de cada tamanho, sem ficarem alinhados."""
    img = Imagem(30, 10)
    bloco(img, [(1, 5), (2, 2), (7, 1), (8, 5)], 0.46, 245, 5)
    bloco(img, [(10, 9), (11, 4), (16, 3), (20, 5), (21, 9)], 0.55, 246, 16)
    bloco(img, [(24, 8), (25, 6), (28, 6), (28, 8)], 0.4, 247, 27)
    img.contornar()
    return img


def terra_mancha(largura, altura, semente):
    """Mancha de terra para o chão (ver a conta no topo do arquivo)."""
    img = Imagem(largura, altura)
    cx, cy = largura / 2.0, altura / 2.0
    d = np.hypot((img.X + 0.5 - cx) / cx, (img.Y + 0.5 - cy) / cy)
    grosso = ruido(largura, altura, 18, 11, semente)
    miudo = ruido(largura, altura, 5, 3, semente + 1)
    m = (0.72 * grosso + 0.46 * miudo) > d + 0.12
    tom = 0.12 + 0.3 * ruido(largura, altura, 6, 4, semente + 2) + 0.14 * (1 - d)
    img.pintar(m, "areia", tom)
    return img


def main():
    print("Gerando as peças de escombro:")
    entulho_monte().salvar("entulho_monte.png", PASTA_OBJETOS)
    entulho_laje().salvar("entulho_laje.png", PASTA_OBJETOS)
    entulho_baixo().salvar("entulho_baixo.png", PASTA_OBJETOS)
    entulho_pedras_a().salvar("entulho_pedras_a.png", PASTA_OBJETOS)
    entulho_pedras_b().salvar("entulho_pedras_b.png", PASTA_OBJETOS)
    entulho_pedras_c().salvar("entulho_pedras_c.png", PASTA_OBJETOS)
    terra_mancha(220, 150, 301).salvar("terra_mancha_grande.png", PASTA_CHAO)
    terra_mancha(130, 70, 311).salvar("terra_mancha_media.png", PASTA_CHAO)
    terra_mancha(70, 34, 321).salvar("terra_mancha_pequena.png", PASTA_CHAO)


if __name__ == "__main__":
    main()
