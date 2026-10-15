# gerar_objetos_menu.py — desenha os objetos discretos que ficam por cima da
# arte do menu principal e lembram personagens da história.
#
# Como rodar (precisa de Python com Pillow):
#
#   python assets/modelagem/menu/gerar_objetos_menu.py
#
# Sai, em assets/sprites/menu/:
#   menu_anel_gabriel.png   o anel da avó do Gabriel, gasto, deitado na mesa
#   menu_oculos_zane.png    os óculos de 2123 do Zane, na estante do fundo
#   menu_farol_postit.png   o símbolo dos Faroleiros, rabiscado no post-it
#
# Por que objetos separados, e não pintados na menu_cena.png? Assim a arte
# original não muda: cada objeto é um Sprite2D na cena do menu, fácil de mover,
# trocar ou tirar enquanto o grupo testa.
#
# Escala: a menu_cena.png tem 1280×720 e aparece com escala 0,25 (320×180, a
# resolução do jogo). Os objetos são desenhados pixel a pixel na resolução do
# jogo e ampliados 4× sem suavizar (vizinho mais próximo). Na cena eles também
# usam escala 0,25, então cada pixel desenhado aqui vira exatamente 1 pixel do
# jogo, do mesmo tamanho dos "pixels" da pintura.
#
# Como o desenho funciona: cada objeto é uma grade de letras, uma letra por
# pixel. Cada letra aponta para uma cor da paleta; "." é transparente.

import os

from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_SAIDA = os.path.join(PASTA_PROJETO, "assets", "sprites", "menu")
AMPLIACAO = 4

# A cena do menu é escura e azulada, com a luminária quente à direita. As cores
# são todas apagadas para o objeto não saltar aos olhos: é para quem procura.

# Anel do Gabriel: ouro velho, gasto. Visto de cima e um pouco de lado, então
# vira uma elipse. A luz da luminária vem da direita, por isso o brilho fica no
# lado direito do aro. O lado esquerdo, na sombra, não pode ser escuro demais:
# sobre a madeira escura ele sumia e o anel parecia um "C". O ouro da sombra
# fica só um pouco mais escuro que o ouro gasto, e o aro inteiro aparece.
PALETA_ANEL = {
    "e": (150, 112, 60, 255),    # ouro na sombra
    "o": (178, 138, 74, 255),    # ouro gasto
    "c": (204, 168, 98, 255),    # ouro claro, virado para a luz
    "b": (244, 224, 168, 255),   # o único ponto de brilho
    "s": (30, 18, 12, 110),      # sombra do anel na madeira
}
ANEL = [
    "..eooc...",
    ".e....cb.",
    "e......c.",
    ".e....oc.",
    "..eeoo.s.",
    "...sss...",
]

# Óculos do Zane: a ficha dele não tem óculos; são um objeto de 2123 que
# combina com o visual dele. Uma lente só, contínua, de ponta a ponta (como um
# visor), com armação grafite, a linha de luz ciano dos implantes dele e um
# detalhe amarelo-ácido na dobradiça, a cor de identificação do Zane.
# Estão em pé, de frente, na prateleira do meio da estante do fundo, na frente
# das lombadas dos livros (as hastes dobradas ficam escondidas atrás da lente).
# A estante é escura, por isso a armação é um grafite mais claro que o da
# sombra das prateleiras, e a linha ciano é o que chama o olho de quem procura.
PALETA_OCULOS = {
    "f": (62, 68, 84, 255),      # armação grafite
    "g": (96, 104, 122, 255),    # armação com reflexo
    "l": (18, 32, 44, 255),      # lente escura
    "r": (50, 100, 120, 255),    # reflexo frio na lente
    "c": (70, 170, 186, 255),    # linha de luz ciano
    "C": (146, 228, 238, 255),   # ponto mais aceso da luz
    "a": (170, 182, 42, 255),    # amarelo-ácido, na dobradiça
    "s": (6, 8, 14, 140),        # sombra na prateleira
}
OCULOS = [
    ".gffffffffffffffffa.",
    "fcccccCccccccccccccf",
    "fllllrrllllllllrrllf",
    "fllllllll..llllllllf",
    ".flllllf....flllllf.",
    "..ffff........ffff..",
    "..ssss........ssss..",
]


# Símbolo dos Faroleiros (Enredo Principal, seção 2.4), rabiscado a caneta no
# post-it colado na moldura do monitor. O post-it da pintura já tem rabiscos de
# "texto"; o desenho cobre só o meio dele com um pedaço do mesmo papel, e os
# rabiscos das bordas continuam aparecendo.
# A referência é a pintura do símbolo feita pelo Davi (tinta clara sobre fundo
# preto). No post-it as cores se invertem: tinta escura sobre papel claro.
# Por isso a lanterna vira um quadrado de tinta com um ponto de papel no meio.
# De cima para baixo: os três raios em leque, a lanterna, um vão, a torre em
# trapézio com a portinha embaixo.
PALETA_POSTIT = {
    "k": (62, 42, 28, 255),      # tinta de caneta, a mesma dos rabiscos da pintura
    "K": (84, 62, 46, 255),      # tinta mais fraca, onde a caneta falhou
    "p": (114, 92, 76, 255),     # papel do post-it
}
PAPEL_POSTIT = ((114, 92, 76, 255), (108, 86, 71, 255))
POSTIT = [
    ".k...k...k.",
    "..K..k..K..",
    "...........",
    "....kkk....",
    "....kpk....",
    "....kkk....",
    "...........",
    "....kkk....",
    "....kkk....",
    "...kkkkk...",
    "...kkKkk...",
    "..kkkkkkk..",
]


def cor_do_papel(x, y, papel):
    # Um granulado leve, para o remendo não ficar liso demais perto da pintura:
    # 1 pixel em cada 5 sai num tom um pouco mais escuro, num padrão espalhado.
    return papel[1] if (x * 7 + y * 3) % 5 == 0 else papel[0]


def encosta_na_tinta(grade, x, y):
    # O papel só é pintado em volta da tinta (nos 8 vizinhos de cada pixel de
    # tinta). Assim o remendo não vira um retângulo, e os rabiscos da pintura
    # continuam aparecendo no resto do post-it.
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            vy, vx = y + dy, x + dx
            if 0 <= vy < len(grade) and 0 <= vx < len(grade[vy]) and grade[vy][vx] in "kK":
                return True
    return False


def desenhar(grade, paleta, papel=None):
    altura = len(grade)
    largura = max(len(linha) for linha in grade)
    imagem = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    for y, linha in enumerate(grade):
        for x, letra in enumerate(linha):
            if letra != ".":
                imagem.putpixel((x, y), paleta[letra])
            elif papel and encosta_na_tinta(grade, x, y):
                imagem.putpixel((x, y), cor_do_papel(x, y, papel))
    return imagem.resize((largura * AMPLIACAO, altura * AMPLIACAO), Image.NEAREST)


def salvar(imagem, nome):
    caminho = os.path.join(PASTA_SAIDA, nome)
    imagem.save(caminho)
    print("salvo:", os.path.relpath(caminho, PASTA_PROJETO), imagem.size)


if __name__ == "__main__":
    salvar(desenhar(ANEL, PALETA_ANEL), "menu_anel_gabriel.png")
    salvar(desenhar(OCULOS, PALETA_OCULOS), "menu_oculos_zane.png")
    salvar(desenhar(POSTIT, PALETA_POSTIT, PAPEL_POSTIT), "menu_farol_postit.png")
