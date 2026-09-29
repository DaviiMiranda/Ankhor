# gerar_antecessores.py — desenha, por código, os OBJETOS DE CENÁRIO que os
# antecessores (as pessoas puxadas pela fenda antes do Gabriel) deixaram na
# Biblioteca. Quem são e o que deixaram: docs/personagens/antecessores.md.
#
# Como rodar (Python 3 + numpy, igual ao gerar_biblioteca.py):
#
#   python assets/modelagem/cenario/gerar_antecessores.py
#
# O que sai (em assets/sprites/cenario/objetos/):
#   acampamento_baltazar.png  o canto onde o Baltazar (1750) viveu, entre as
#                             raízes da árvore: pano, diário, luneta, vela
#   robo_desmontado.png       um robô que o Baltazar desmontou peça por peça
#                             e deixou enfileirado, como num estudo
#   riscos_estrelas.png       mapas de estrelas riscados na casca da árvore
#                             (vai por cima do tronco, como filho da árvore)
#   terminal.png              terminal de 3026, apagado, com o bilhete da
#                             Clarice (1994) colado na tela
#
# Como o gerar_kit.py, este script IMPORTA as funções do gerar_biblioteca.py
# (paleta, dithering, contorno), então os objetos saem no mesmo estilo.
#
# Cada função devolve (imagem, x do pé, y do pé). O "pé" é o ponto que
# encosta no chão: no Godot, o offset do Sprite2D é -pé, e o y-sort usa a
# posição do nó (docs/visao_geral/estilo_artistico.md). O script imprime o
# offset de cada um.
#
# Escala: no cenário 1 px vale ~3,6 cm (o Gabriel tem 49 px de altura).

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")

# Importa o gerar_biblioteca.py como um módulo (sem rodar o main dele).
_spec = importlib.util.spec_from_file_location(
    "gerar_biblioteca",
    os.path.join(PASTA_PROJETO, "assets", "modelagem", "salas", "biblioteca", "gerar_biblioteca.py"))
bib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bib)

Imagem, RAMPAS, CONTORNO, SOMBRA, ruido = bib.Imagem, bib.RAMPAS, bib.CONTORNO, bib.SOMBRA, bib.ruido

# Latão da luneta: um dourado queimado, escuro (é metal de 1750 que passou
# séculos no escuro). Não existe na paleta da Biblioteca porque nada lá era
# de latão.
LATAO = bib.hexa("#1f170a", "#3a2c12", "#5a451d", "#7c6129", "#9c7d3a", "#bb9a52")
# Cera da vela: branco-amarelado apagado.
CERA = bib.hexa("#3e3a2e", "#5e5946", "#807960", "#a09878")


def sombra_no_chao(img, cx, cy, rx, ry):
    """Sombra de contato: uma elipse quase preta embaixo do objeto. Pintada
    primeiro, o objeto vai por cima."""
    img.cor(img.elipse(cx, cy, rx, ry), SOMBRA)


def acampamento_baltazar():
    """O canto do Baltazar entre as raízes. Da esquerda para a direita:
    o toco de vela numa pedra, o pano encerado com o diário em cima (couro
    escuro, com uma fita marcando a página) e a luneta de latão deitada,
    com a lente rachada virada para a câmera. Tudo baixo: são coisas no
    chão, o Gabriel passa por cima."""
    img = Imagem(48, 16)
    X, Y = img.X, img.Y
    fino = ruido(img.w, img.h, 2, 2, 301)
    base = 14
    sombra_no_chao(img, 24, base, 22, 2.5)
    # Pano encerado: um losango achatado, verde-oliva escuro e dobrado.
    pano = img.poligono([(12, base - 3), (22, base - 6), (36, base - 5), (34, base), (14, base + 1)])
    img.pintar(pano, "tecido", 0.35 + 0.25 * (Y < base - 3) + 0.08 * fino)
    img.pintar(img.linha(18, base - 4, 30, base - 1), "tecido", 0.1)       # dobra
    # Diário: um bloco de couro (madeira escura) com as páginas aparecendo.
    diario = img.ret(19, base - 8, 29, base - 4)
    img.pintar(diario, "madeira", 0.35 + 0.2 * (Y == base - 8))
    img.pintar(img.ret(20, base - 5, 28, base - 4), "papel", 0.75)         # páginas
    img.pintar(img.ret(26, base - 5, 27, base - 1), "livro_vermelho", 0.8)  # fita
    # Luneta de latão deitada, na diagonal, com a boca virada para a direita.
    corpo = img.linha(33, base - 2, 44, base - 5, 1.3)
    img.pintar(corpo, LATAO, 0.45 + 0.35 * (Y <= base - 4) + 0.1 * fino)
    img.pintar(img.linha(37, base - 4, 37, base - 1, 0.6), LATAO, 0.2)     # anel
    lente = img.elipse(45, base - 5, 1.6, 2.1)
    img.pintar(lente, "ceu", 0.45)
    img.cor(img.ret(45, base - 6, 46, base - 5), RAMPAS["ceu"][5])          # reflexo
    img.cor(img.ret(44, base - 4, 45, base - 3), CONTORNO)                 # a rachadura
    # Toco de vela sobre uma pedra chata, à esquerda.
    pedra = img.elipse(6, base - 1, 5, 2)
    img.pintar(pedra, "concreto", 0.4 + 0.2 * (Y < base - 1))
    vela = img.ret(5, base - 7, 8, base - 2)
    img.pintar(vela, CERA, 0.5 + 0.3 * (X == 5))
    img.pintar(img.ret(4, base - 3, 9, base - 2), CERA, 0.35)               # cera escorrida
    img.cor(img.ret(6, base - 9, 7, base - 7), CONTORNO)                   # pavio apagado
    img.contornar()
    return img, 24, base


def robo_desmontado():
    """Um robô aberto e desmontado, com as peças em fila no chão. Da
    esquerda para a direita: a cabeça com o OLHO (a lente do sensor óptico,
    o ponto fraco que o Baltazar desenhou no diário), duas placas da
    carcaça, um braço de dois gomos, uma engrenagem e três parafusos
    alinhados. É metal de 3026, frio, com ferrugem nas juntas."""
    img = Imagem(64, 14)
    X, Y = img.X, img.Y
    fino = ruido(img.w, img.h, 2, 2, 311)
    base = 12
    sombra_no_chao(img, 32, base, 31, 2)
    # Cabeça: meia-cúpula com a lente grande e apagada.
    cabeca = img.elipse(8, base - 3, 7, 6) & (Y <= base)
    img.pintar(cabeca, "metal", 0.35 + 0.3 * (X < 6) * (Y < base - 4) + 0.08 * fino)
    olho = img.elipse(10, base - 4, 3, 3)
    img.pintar(olho, "metal", 0.05)
    img.cor(img.ret(9, base - 6, 10, base - 5), RAMPAS["ceu"][3])           # vidro
    # Placas da carcaça, deitadas (planas, só a quina de cima clara).
    for x0, larg, tom in ((18, 8, 0.4), (28, 7, 0.32)):
        placa = img.ret(x0, base - 3, x0 + larg, base)
        img.pintar(placa, "metal", tom + 0.2 * (Y == base - 3) + 0.06 * fino)
        img.pintar(img.ret(x0 + 1, base - 2, x0 + 2, base - 1), "ferrugem", 0.5)
    # Braço: dois gomos com uma junta enferrujada no meio.
    braco = img.linha(38, base - 2, 44, base - 3, 1.2) | img.linha(45, base - 3, 50, base - 1, 1.1)
    img.pintar(braco, "metal", 0.45 + 0.1 * fino)
    img.pintar(img.elipse(44.5, base - 3, 1.5, 1.5), "ferrugem", 0.55)
    # Engrenagem: um círculo com dentes (pixels alternados na borda).
    ang = np.arctan2(Y + 0.5 - (base - 3), X + 0.5 - 55)
    dentes = (np.cos(ang * 8) > 0) & img.elipse(55, base - 3, 3.2, 3.2)
    engrenagem = img.elipse(55, base - 3, 2.4, 2.4) | dentes
    img.pintar(engrenagem & ~img.elipse(55, base - 3, 0.9, 0.9), "ferrugem", 0.45 + 0.2 * fino)
    # Parafusos em fila, bem arrumados: é isso que dá o ar de "estudo".
    for x in (59, 61, 63):
        img.pintar(img.ret(x - 1, base - 2, x, base), "metal", 0.6)
    img.contornar()
    return img, 32, base


def riscos_estrelas():
    """Mapas de estrelas riscados à faca na casca. O risco tira a casca e
    mostra a madeira clara por baixo. São três constelações: pontos
    (estrelas) ligados por traços finos, e um círculo com uma cruz, que é
    como um astrônomo de 1750 marcava a posição do norte.
    O fundo é transparente: este sprite vai por cima do tronco da árvore."""
    img = Imagem(18, 30)
    risco = np.zeros((img.h, img.w), dtype=bool)
    constelacoes = [
        [(2, 3), (6, 1), (10, 4), (8, 8)],
        [(12, 12), (15, 14), (14, 18), (10, 17)],
        [(3, 20), (6, 23), (4, 27)],
    ]
    estrelas = []
    for pontos in constelacoes:
        risco |= img.caminho(pontos, 0.45)
        estrelas += pontos
    risco |= img.elipse(4.5, 12.5, 3, 3) & ~img.elipse(4.5, 12.5, 2, 2)
    risco |= img.linha(4.5, 8.5, 4.5, 16.5, 0.45) | img.linha(0.5, 12.5, 8.5, 12.5, 0.45)
    # A madeira exposta é bem mais clara que a casca (areia clara), senão o
    # risco some no tronco escuro.
    img.pintar(risco, "areia", 0.7)
    for (x, y) in estrelas:
        img.cor(img.ret(x, y, x + 1, y + 1), RAMPAS["areia"][7])
    return img, 9, 29


def terminal():
    """Um terminal de 3026 da pesquisa da Âncora, apagado: um pedestal de
    metal com a tela inclinada no alto. A tela está escura e rachada, com
    o bilhete da Clarice colado por cima (uma folha clara com um pedaço de
    fita). Na frente, a fenda da unidade de disquete que a Clarice
    adaptou (docs/personagens/antecessores.md). Musgo sobe pelo pé."""
    img = Imagem(30, 46)
    X, Y = img.X, img.Y
    fino = ruido(img.w, img.h, 2, 2, 321)
    base = 44
    sombra_no_chao(img, 15, base, 13, 2)
    # Pé: coluna larga, mais clara à esquerda (a luz vem de lá).
    pe = img.poligono([(8, base), (9, 20), (21, 20), (22, base)])
    img.pintar(pe, "metal", 0.28 + 0.22 * (X < 12) + 0.06 * fino)
    img.pintar(img.ret(10, 24, 20, 25), "metal", 0.12)                     # emenda
    # Fenda do disquete com a luzinha apagada.
    img.pintar(img.ret(11, 28, 19, 30), "metal", 0.04)
    img.pintar(img.ret(17, 31, 19, 32), "ferrugem", 0.4)
    # Cabeça do terminal: um bloco inclinado para trás, com a tela.
    cabeca = img.poligono([(3, 4), (26, 1), (28, 20), (2, 21)])
    img.pintar(cabeca, "metal", 0.36 + 0.2 * (Y < 6) + 0.06 * fino)
    tela = img.poligono([(6, 6), (24, 4), (25, 17), (5, 18)])
    img.pintar(tela, "concreto", 0.06 + 0.06 * fino)
    img.pintar(img.linha(8, 16, 14, 9) | img.linha(14, 9, 16, 11), "metal", 0.4)  # rachadura
    # Bilhete da Clarice colado na tela, um pouco torto, com a fita.
    bilhete = img.poligono([(13, 8), (22, 7), (23, 16), (14, 17)])
    img.pintar(bilhete, "papel", 0.95)
    for y in (10, 12, 14):
        img.pintar(img.linha(15, y, 21, y - 0.5, 0.4), "livro_azul", 0.8)
    img.pintar(img.ret(16, 6, 20, 8), "areia", 0.85)
    # Musgo no pé.
    musgo = pe & (Y > base - 6) & (ruido(img.w, img.h, 3, 3, 322) > 0.45)
    img.pintar(musgo, "verde", 0.35 + 0.3 * fino)
    img.contornar()
    return img, 15, base


FUNCOES = {
    "acampamento_baltazar": acampamento_baltazar,
    "robo_desmontado": robo_desmontado,
    "riscos_estrelas": riscos_estrelas,
    "terminal": terminal,
}


def main():
    print("Gerando os objetos dos antecessores (offset do Sprite2D no Godot = -pé):")
    for nome, funcao in FUNCOES.items():
        img, px, py = funcao()
        img.salvar(f"{nome}.png", PASTA_OBJETOS)
        print(f"    {nome}: pé em ({px}, {py}) -> offset = Vector2({-px}, {-py})")


if __name__ == "__main__":
    main()
