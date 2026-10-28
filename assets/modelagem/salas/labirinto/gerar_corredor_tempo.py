# gerar_corredor_tempo.py — gera os objetos do Corredor do Tempo que ainda
# não existiam no jogo (o resto reaproveita a vitrola, o relógio de pêndulo
# e as paredes da sala dos anos 80 do Bunker).
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/salas/labirinto/gerar_corredor_tempo.py
#
# O que sai, em assets/sprites/cenario/objetos/:
#   maquina_aneis.png    36 x 44: um gabinete de metal com três anéis
#                        concêntricos no painel e a trava vermelha em cima
#   quadro_filme_1.png   22 x 30: quadro da coleção do Carlos, De Volta para o
#   quadro_filme_2.png   Futuro partes I, II e III. Desenhos próprios (não são
#   quadro_filme_3.png   os cartazes): I, a torre do relógio com o raio e o
#                        rastro de fogo no asfalto; II, a cidade de 2015 ao
#                        anoitecer com um skate voador; III, a locomotiva no
#                        deserto de 1885 ao pôr do sol. Embaixo, o número da
#                        parte em algarismos romanos.
#
# Mesma paleta e ferramentas (Imagem, RAMPAS, pontilhado de Bayer) do
# gerar_biblioteca.py.
#
# - ANÉIS: cada anel é a coroa r_dentro <= r <= r_fora, com r a distância
#   ao centro (hypot). A fenda é a fatia em que o ângulo atan2(dy, dx) fica
#   a menos de meia largura do ângulo da fenda; a diferença de ângulos é
#   tirada pelo arco tangente de (sen, cos) para dar a volta certa em ±pi.
# - CÉUS DOS QUADROS: degradê vertical, o valor da rampa caindo com y
#   (0,75 - 0,6 · y/altura); o pontilhado de Bayer do pintar() faz a
#   transição entre as cores sem faixas.
# - ALGARISMOS: cada "I" é uma barra de 1 x 4 px; "II" e "III" põem as
#   barras lado a lado com 1 px de folga, centradas no quadro.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")

_spec = importlib.util.spec_from_file_location(
    "gerar_biblioteca",
    os.path.join(PASTA_PROJETO, "assets", "modelagem", "salas", "biblioteca", "gerar_biblioteca.py"))
bib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bib)
Imagem, RAMPAS = bib.Imagem, bib.RAMPAS

LARANJA = bib.hexa("#2a1206", "#5a2a0c", "#9a4a14", "#d8742a", "#f2a24e")
CREME = bib.hexa("#4a4436", "#8a8268", "#c8bea0", "#ece2c6")
VERMELHO = bib.hexa("#1e0a0a", "#4a1212", "#7e1c1a", "#c0392b")
NOITE = bib.hexa("#07091a", "#0f1430", "#1a2250", "#2c3874")
ANOITECER = bib.hexa("#1a0a24", "#3a1248", "#6a1e6a", "#b0367e", "#f06aa0")
POR_DO_SOL = bib.hexa("#3a1408", "#7a2c0c", "#c2541a", "#ec8a2e", "#f8c46a")
AMARELO = bib.hexa("#f8e45a")[0]
FOGO = bib.hexa("#f08a24")[0]
CIANO = bib.hexa("#6ae8f0")[0]
ROSA = bib.hexa("#ff7ab8")[0]
SOMBRA = bib.hexa("#120a10")[0]

LARGURA_QUADRO, ALTURA_QUADRO = 22, 30
FAIXA = 25


def maquina_aneis():
    img = Imagem(36, 44)
    X, Y = img.X, img.Y
    img.pintar(img.ret(2, 6, 34, 44), "metal", 0.42 - 0.2 * (Y / 44))
    img.pintar(img.ret(2, 6, 34, 7), "metal", 0.7)
    img.pintar(img.ret(4, 40, 32, 44), "metal", 0.12)
    cx, cy = 18.0, 22.0
    r = np.hypot(X + 0.5 - cx, Y + 0.5 - cy)
    img.pintar(r <= 13.5, "metal", 0.06)
    angulo = np.arctan2(Y + 0.5 - cy, X + 0.5 - cx)
    for (dentro, fora), fenda, valor in (((10.5, 12.5), 0.6, 0.65), ((7.0, 9.0), 2.4, 0.55), ((3.5, 5.5), -1.9, 0.6)):
        diferenca = np.abs(np.arctan2(np.sin(angulo - fenda), np.cos(angulo - fenda)))
        coroa = (r >= dentro) & (r <= fora) & (diferenca > 0.35)
        img.pintar(coroa, LARANJA, valor)
    img.cor(img.ret(16, 2, 20, 8), VERMELHO[3])
    img.cor(img.ret(17, 8, 19, 10), VERMELHO[2])
    img.cor(img.ret(6, 36, 9, 38), bib.hexa("#7cf09a")[0])
    img.cor(img.ret(27, 36, 30, 38), VERMELHO[3])
    return img


def moldura(img, ceu):
    """Moldura de madeira de 1 px, o céu em degradê e a faixa de baixo."""
    Y = img.Y
    img.pintar(img.ret(0, 0, LARGURA_QUADRO, ALTURA_QUADRO), "madeira", 0.55)
    img.pintar(img.ret(1, 1, LARGURA_QUADRO - 1, FAIXA), ceu, 0.75 - 0.6 * Y / ALTURA_QUADRO)


def numero_da_parte(img, parte):
    img.cor(img.ret(1, FAIXA, LARGURA_QUADRO - 1, ALTURA_QUADRO - 1), SOMBRA)
    largura = 2 * parte - 1
    x0 = (LARGURA_QUADRO - largura) // 2
    for i in range(parte):
        img.cor(img.ret(x0 + 2 * i, FAIXA + 1, x0 + 2 * i + 1, FAIXA + 4), CREME[3])


def quadro_parte_1():
    img = Imagem(LARGURA_QUADRO, ALTURA_QUADRO)
    moldura(img, NOITE)
    img.pintar(img.ret(1, 20, 21, FAIXA), "concreto", 0.25)
    img.cor(img.linha(1.5, 24.5, 10, 20.5, 0.4), FOGO)
    img.cor(img.linha(6.5, 24.5, 14, 20.5, 0.4), FOGO)
    img.pintar(img.ret(8, 10, 15, 20), "concreto", 0.62 - 0.3 * img.Y / ALTURA_QUADRO)
    img.pintar(img.poligono([(7, 10), (11.5, 5), (16, 10)]), "concreto", 0.4)
    img.cor(img.elipse(11.5, 13.5, 2.3, 2.3), CREME[3])
    img.cor(img.linha(11.5, 13.5, 11.5, 12, 0.4), SOMBRA)
    img.cor(img.linha(11.5, 13.5, 12.7, 13.5, 0.4), SOMBRA)
    img.cor(img.caminho([(18, 1), (15.5, 4), (17.5, 5), (14, 9)], 0.45), AMARELO)
    return img


def quadro_parte_2():
    img = Imagem(LARGURA_QUADRO, ALTURA_QUADRO)
    moldura(img, ANOITECER)
    for x0, x1, topo in ((1, 4, 15), (4, 8, 11), (8, 11, 17), (11, 15, 9), (15, 18, 14), (18, 21, 12)):
        img.cor(img.ret(x0, topo, x1, FAIXA), SOMBRA)
        for y in range(topo + 2, FAIXA - 1, 3):
            img.cor(img.ret(x0 + 1, y, x0 + 2, y + 1), CIANO)
    img.cor(img.ret(5, 6, 16, 8), ROSA)
    img.cor(img.ret(6, 8, 7, 9), CIANO)
    img.cor(img.ret(14, 8, 15, 9), CIANO)
    img.cor(img.ret(4, 7, 5, 8), ROSA)
    img.cor(img.ret(16, 6, 17, 7), ROSA)
    return img


def quadro_parte_3():
    img = Imagem(LARGURA_QUADRO, ALTURA_QUADRO)
    moldura(img, POR_DO_SOL)
    img.cor(img.elipse(15, 13, 3.2, 3.2), bib.hexa("#fde7a0")[0])
    img.cor(img.poligono([(1, 17), (3, 12), (7, 12), (9, 17)]), bib.hexa("#4a1c10")[0])
    img.cor(img.poligono([(13, 17), (15, 14), (19, 14), (21, 17)]), bib.hexa("#4a1c10")[0])
    img.pintar(img.ret(1, 17, 21, FAIXA), "areia", 0.85 - 0.3 * (img.Y - 17) / 8)
    img.cor(img.ret(1, 22, 21, 23), SOMBRA)
    img.cor(img.ret(6, 17, 14, 21), SOMBRA)
    img.cor(img.ret(12, 14, 17, 21), SOMBRA)
    img.cor(img.ret(7, 14, 9, 17), SOMBRA)
    img.cor(img.poligono([(3, 22), (6, 18), (6, 22)]), SOMBRA)
    img.pintar(img.elipse(8, 11.5, 1.8, 1.4) | img.elipse(6, 8.5, 1.6, 1.3) | img.elipse(4, 5.5, 1.4, 1.1), CREME, 0.35)
    return img


def main():
    print("Gerando os objetos do Corredor do Tempo")
    maquina_aneis().salvar("maquina_aneis.png", PASTA_OBJETOS)
    for parte, desenho in enumerate((quadro_parte_1, quadro_parte_2, quadro_parte_3), start=1):
        img = desenho()
        numero_da_parte(img, parte)
        img.salvar(f"quadro_filme_{parte}.png", PASTA_OBJETOS)


if __name__ == "__main__":
    main()
