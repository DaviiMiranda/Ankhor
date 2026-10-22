# gerar_marcas_faroleiros.py — desenha as MARCAS DOS FAROLEIROS pintadas à
# mão nas paredes (Enredo Principal, seção 2.4), para pôr em cima de qualquer
# peça de parede como um Sprite2D.
#
# Como rodar (Python 3 + numpy):
#
#   python assets/modelagem/cenario/gerar_marcas_faroleiros.py
#
# O que sai (em assets/sprites/cenario/objetos/):
#   marca_farol_inteiro.png  o farol com os três raios: lugar seguro, ou
#                            esconderijo antigo dos Faroleiros
#   marca_farol_apagado.png  o farol sem raios, com um traço atravessado:
#                            farol apagado, lugar perdido, perigo
#
# O SÍMBOLO (a regra do Enredo, na grade de 9 x 12 px)
#   - a torre: trapézio alto e estreito, mais largo na base (3 px no topo,
#     5 na base);
#   - a lanterna: quadrado de 3 x 3 em cima da torre, com o ponto no centro;
#   - três raios de 3 px saindo da lanterna para cima, em leque.
# Aqui cada pixel do símbolo vira 2 x 2 (18 x 24), para ler de longe, e a
# tinta escorre um pouco embaixo: foi pintado à mão e às pressas. A cor é o
# âmbar, a luz quente de uma chama (onde aparece âmbar, passou um Faroleiro).
# A variante com os raios riscados em vermelho (a traição do Carlos) é uma
# peça de parede do D-Tec: dtec_farol_riscado, em gerar_dtec.py.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")

_spec = importlib.util.spec_from_file_location("gerar_bunker", os.path.join(PASTA_SCRIPT, "gerar_bunker.py"))
bunker = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bunker)
bib = bunker.kit.bib
Imagem, RAMPAS = bib.Imagem, bib.RAMPAS

RAMPAS["ambar"] = bib.hexa("#2a1704", "#4a2a08", "#7a4510", "#a8641a", "#d48a2a", "#f2b04a")

ESCALA = 2
X0, Y0 = 2, 1
RAIOS = [(0, 0), (1, 1), (2, 2), (4, 0), (4, 1), (4, 2), (8, 0), (7, 1), (6, 2)]
LANTERNA = [(cx, cy) for cx in range(3, 6) for cy in range(3, 6) if (cx, cy) != (4, 4)]
TORRE = [(cx, 6 + linha) for linha in range(6)
         for cx in (range(3, 6) if linha < 3 else range(2, 7))]


def _celula(img, cx, cy):
    return img.ret(X0 + cx * ESCALA, Y0 + cy * ESCALA, X0 + (cx + 1) * ESCALA, Y0 + (cy + 1) * ESCALA)


def _farol(com_raios):
    img = Imagem(22, 32)
    grupos = [(LANTERNA, 0.92), (TORRE, 0.55)]
    if com_raios:
        grupos.insert(0, (RAIOS, 0.88))
    for celulas, tom in grupos:
        for (cx, cy) in celulas:
            img.pintar(_celula(img, cx, cy), "ambar", tom)
    img.pintar(_celula(img, 4, 4), "ambar", 0.12)
    img.pintar(img.ret(X0 + 6, 25, X0 + 7, 30) | img.ret(X0 + 11, 25, X0 + 12, 28), "ambar", 0.4)
    return img


def marca_farol_inteiro():
    return _farol(True)


def marca_farol_apagado():
    """Sem raios e com um traço atravessado: a luz apagou."""
    img = _farol(False)
    img.pintar(img.linha(X0 - 1, Y0 + 20, X0 + 19, Y0 + 2, 0.7), "ambar", 0.8)
    return img


MARCAS = {
    "marca_farol_inteiro": marca_farol_inteiro,
    "marca_farol_apagado": marca_farol_apagado,
}


def main():
    for nome, f in MARCAS.items():
        f().salvar(f"{nome}.png", PASTA_OBJETOS)


if __name__ == "__main__":
    main()
