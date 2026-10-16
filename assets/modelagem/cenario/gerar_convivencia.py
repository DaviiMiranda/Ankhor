# gerar_convivencia.py — desenha o item-chave do Centro de Convivência, a
# Célula de Energia (ícone 16x16, sprite de chão e imagem de detalhe 128x128
# em assets/sprites/itens/).
#
# O cenário da fase (a praça de alimentação, os restaurantes, a porta de vidro
# e os objetos) é desenhado por gerar_praca.py, gerar_restaurantes.py,
# gerar_porta_restaurante.py e gerar_praca_objetos.py.
#
# Como rodar:
#   python assets/modelagem/cenario/gerar_convivencia.py

import importlib.util
import math
import os

import numpy as np
from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")

_spec = importlib.util.spec_from_file_location(
    "gerar_objetos_biblioteca", os.path.join(PASTA_SCRIPT, "gerar_objetos_biblioteca.py"))
ob = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ob)

Desenho, cor = ob.Desenho, ob.cor

CONTORNO = cor("#0d0f12")
CONCRETO_ESCURO = cor("#2a2d32")
CONCRETO = cor("#42474f")
CONCRETO_CLARO = cor("#5c636e")
RAIZ_ESCURA = cor("#2b1d14")
RAIZ = cor("#473223")
RAIZ_CLARA = cor("#634733")
MUSGO_ESCURO = cor("#1d331e")
MUSGO = cor("#2f5230")
MUSGO_CLARO = cor("#487544")
ACO_ESCURO = cor("#252a30")
ACO = cor("#464f59")
ACO_CLARO = cor("#707d8c")
CIANO_ESCURO = cor("#0e4d59")
CIANO = cor("#24b0c7")
CIANO_CLARO = cor("#8cf2ff")
VIDRO_CLARO = cor("#a8d8e6")
VIDRO = cor("#6899a8")
AMARELO = cor("#e6b82e")
VERMELHO = cor("#d93829")


def gerar_celula_energia():
    """Desenha o ícone (16x16), o sprite de chão (12x8) e o detalhe (128x128)
    da Célula de Energia de Alta Densidade."""
    os.makedirs(PASTA_ITENS, exist_ok=True)
    icone = Desenho(16, 16)
    icone.caixa(3, 1, 12, 14, ACO, ACO_CLARO, ACO_ESCURO)
    icone.ret(5, 0, 10, 1, ACO_CLARO)
    icone.ret(5, 4, 10, 11, CIANO_ESCURO)
    icone.ret(6, 5, 9, 10, CIANO)
    icone.ret(7, 6, 8, 9, CIANO_CLARO)
    icone.ret(4, 7, 11, 8, ACO_ESCURO)
    icone.px(4, 2, AMARELO)
    icone.px(11, 2, AMARELO)
    icone.salvar(PASTA_ITENS, "celula_energia.png")

    chao = Desenho(12, 7)
    chao.caixa(0, 1, 11, 6, ACO, ACO_CLARO, ACO_ESCURO)
    chao.ret(3, 2, 8, 5, CIANO)
    chao.ret(4, 3, 7, 4, CIANO_CLARO)
    chao.ret(5, 1, 6, 6, ACO_ESCURO)
    chao.salvar(PASTA_ITENS, "celula_energia_chao.png")

    # Imagem de detalhe 128x128 para a tela de item novo e Examinar
    det = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    pix = det.load()
    for y in range(16, 112):
        for x in range(32, 96):
            # Cilindro metálico com núcleo luminoso ciano
            dx = (x - 64) / 32.0
            if abs(dx) > 1.0:
                continue
            sombra = math.cos(dx * 1.3)
            eh_tampa = y < 28 or y > 98 or (58 <= y <= 66)
            eh_borda = abs(x - 64) > 26
            if eh_tampa or eh_borda:
                base = (int(45 + 45 * sombra), int(52 + 52 * sombra), int(62 + 60 * sombra), 255)
                if 20 <= y <= 24 and (38 <= x <= 46 or 82 <= x <= 90):
                    base = (230, 184, 46, 255)
            else:
                pulso = max(0.0, 1.0 - abs(dx) * 1.1)
                r = int(20 + 120 * (pulso ** 2))
                g = int(140 + 110 * pulso)
                b = int(180 + 75 * pulso)
                base = (min(255, r), min(255, g), min(255, b), 255)
            if x in (32, 95) or y in (16, 111):
                base = CONTORNO
            pix[x, y] = base
    det.save(os.path.join(PASTA_ITENS, "celula_energia_detalhe.png"))


def main():
    gerar_celula_energia()
    print("Célula de Energia gerada com sucesso.")


if __name__ == "__main__":
    main()
