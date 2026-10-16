# gerar_convivencia.py — desenha os assets procedurais do Centro de Convivência:
#   - kit de cenário em assets/sprites/cenario/convivencia/ (mesas redondas de
#     concreto com raízes, balcões da cantina, cacos de vidro, holofotes,
#     comporta da rampa);
#   - item-chave Célula de Energia (ícone 16x16, sprite de chão e imagem de
#     detalhe 128x128 em assets/sprites/itens/).
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
PASTA_CONV = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "convivencia")
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


def gerar_mesa_concreto():
    """Mesa redonda de concreto tradicional do Centro de Convivência,
    coberta parcialmente por raízes e musgo (56 x 36 px)."""
    d = Desenho(56, 36)
    # Sombra e base central
    d.ret(22, 18, 33, 33, CONCRETO_ESCURO)
    d.ret(24, 18, 31, 32, CONCRETO)
    # Bancos laterais de concreto
    d.caixa(2, 20, 14, 30, CONCRETO, CONCRETO_CLARO, CONCRETO_ESCURO)
    d.caixa(41, 20, 53, 30, CONCRETO, CONCRETO_CLARO, CONCRETO_ESCURO)
    # Tampo redondo (elipse em perspectiva)
    for y in range(6, 22):
        for x in range(8, 48):
            nx = (x - 28) / 19.0
            ny = (y - 13) / 7.0
            dist = nx * nx + ny * ny
            if dist <= 1.0:
                if dist > 0.82 or y >= 19:
                    d.px(x, y, CONCRETO_ESCURO)
                elif y <= 9 and nx < 0.3:
                    d.px(x, y, CONCRETO_CLARO)
                else:
                    d.px(x, y, CONCRETO)
    # Raízes e musgo subindo pelo pé e tampo
    for i in range(14):
        rx = 18 + i
        ry = 33 - int(i * 1.3)
        d.ret(rx, ry, rx + 2, ry + 2, RAIZ if i % 2 == 0 else RAIZ_ESCURA)
    d.ret(14, 9, 25, 13, MUSGO)
    d.ret(16, 10, 22, 12, MUSGO_CLARO)
    d.salvar(PASTA_CONV, "mesa_concreto.png")


def gerar_balcao_cantina():
    """Balcão de aço inoxidável manchado da cantina (96 x 40 px)."""
    d = Desenho(96, 40)
    d.caixa(0, 6, 95, 38, ACO, ACO_CLARO, ACO_ESCURO)
    # Tampo superior de inox
    d.ret(1, 7, 94, 13, ACO_CLARO)
    d.ret(1, 14, 94, 15, CONTORNO)
    # Painéis frontais e manchas de ferrugem/tempo
    for x in (24, 48, 72):
        d.ret(x, 15, x + 1, 37, ACO_ESCURO)
    d.ret(10, 22, 18, 28, RAIZ_ESCURA)
    d.ret(54, 25, 65, 33, MUSGO_ESCURO)
    # Estufa de salgados quebrada em cima do balcão
    d.caixa(64, 0, 88, 8, ACO_ESCURO, ACO_CLARO, CONTORNO)
    d.ret(66, 2, 86, 6, VIDRO)
    d.px(70, 4, CONTORNO)
    d.px(71, 5, CONTORNO)
    d.salvar(PASTA_CONV, "balcao_cantina.png")


def gerar_cacos_vidro():
    """Tapete de cacos de louça e vidro estilhaçado no chão (64 x 28 px)."""
    d = Desenho(64, 28)
    rng = np.random.default_rng(42)
    for _ in range(55):
        x = int(rng.integers(2, 60))
        y = int(rng.integers(2, 25))
        c = VIDRO_CLARO if rng.random() > 0.4 else VIDRO
        d.px(x, y, c)
        d.px(x + 1, y, c)
        if rng.random() > 0.5:
            d.px(x, y + 1, ACO_CLARO)
    d.salvar(PASTA_CONV, "cacos_vidro.png")


def gerar_comporta_rampa():
    """Comporta pesada de contenção da rampa do subsolo (48 x 68 px)."""
    d = Desenho(48, 68)
    d.caixa(0, 0, 47, 67, ACO_ESCURO, ACO, CONTORNO)
    for y in range(8, 60, 10):
        d.ret(3, y, 44, y + 5, ACO)
        d.ret(3, y, 44, y + 1, ACO_CLARO)
    # Faixa de alerta amarela e preta na base
    for x in range(4, 44, 6):
        d.ret(x, 58, x + 2, 64, AMARELO)
        d.ret(x + 3, 58, x + 5, 64, CONTORNO)
    # Luz indicadora vermelha (comporta travada)
    d.ret(21, 3, 26, 6, VERMELHO)
    d.salvar(PASTA_CONV, "comporta_rampa.png")


def main():
    os.makedirs(PASTA_CONV, exist_ok=True)
    gerar_celula_energia()
    gerar_mesa_concreto()
    gerar_balcao_cantina()
    gerar_cacos_vidro()
    gerar_comporta_rampa()
    print("Assets do Centro de Convivencia gerados com sucesso.")


if __name__ == "__main__":
    main()
