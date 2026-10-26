# gerar_corredor_tempo.py — gera os dois objetos do Corredor do Tempo que
# ainda não existiam no jogo (o resto reaproveita a vitrola, o relógio de
# pêndulo e as paredes da sala dos anos 80 do Bunker).
#
# Como rodar (Python 3 + numpy):
#   python assets/modelagem/salas/labirinto/gerar_corredor_tempo.py
#
# O que sai, em assets/sprites/cenario/objetos/:
#   relogio_parede.png   22 x 22: relógio de cozinha dos anos 80, moldura
#                        laranja, para pendurar na parede da sala do relógio
#   maquina_aneis.png    36 x 44: um gabinete de metal com três anéis
#                        concêntricos no painel e a trava vermelha em cima
#
# Mesma paleta e ferramentas (Imagem, RAMPAS, pontilhado de Bayer) do
# gerar_biblioteca.py.
#
# - ANÉIS: cada anel é a coroa r_dentro <= r <= r_fora, com r a distância
#   ao centro (hypot). A fenda é a fatia em que o ângulo atan2(dy, dx) fica
#   a menos de meia largura do ângulo da fenda; a diferença de ângulos é
#   tirada pelo arco tangente de (sen, cos) para dar a volta certa em ±pi.
# - PONTEIROS: segmentos com espessura (Imagem.linha), marcando 10 para as 2,
#   a hora dos relógios de vitrine.

import importlib.util
import math
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


def relogio_parede():
    img = Imagem(22, 22)
    c = 11.0
    r = np.hypot(img.X + 0.5 - c, img.Y + 0.5 - c)
    img.pintar(r <= 10.5, LARANJA, 0.55 - 0.25 * (img.Y / 22))
    img.pintar(r <= 8.5, CREME, 0.85 - 0.3 * (img.Y / 22))
    for i in range(12):
        a = math.tau * i / 12
        x, y = c + 7.2 * math.cos(a), c + 7.2 * math.sin(a)
        img.cor(img.ret(int(x), int(y), int(x) + 1, int(y) + 1), CREME[0])
    img.cor(img.linha(c, c, c - 3.5, c - 2.0, 0.6), CREME[0])
    img.cor(img.linha(c, c, c + 4.5, c - 4.5, 0.5), CREME[0])
    img.cor(img.linha(c, c, c + 0.5, c + 6.5, 0.4), VERMELHO[3])
    img.cor(img.ret(10, 10, 12, 12), VERMELHO[2])
    return img


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


def main():
    print("Gerando os objetos do Corredor do Tempo")
    relogio_parede().salvar("relogio_parede.png", PASTA_OBJETOS)
    maquina_aneis().salvar("maquina_aneis.png", PASTA_OBJETOS)


if __name__ == "__main__":
    main()
