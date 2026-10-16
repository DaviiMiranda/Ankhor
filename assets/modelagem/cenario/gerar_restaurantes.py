# gerar_restaurantes.py — desenha, por código, os LETREIROS e os FUNDOS dos
# restaurantes do Centro de Convivência (docs/fases/centro_de_convivencia.md):
# a passarela, os quatro restaurantes e a câmara fria.
#
# Como rodar (Python 3 + numpy + Pillow):
#
#   python assets/modelagem/cenario/gerar_restaurantes.py
#
# O que sai (em assets/sprites/cenario/praca/):
#   letreiros/letreiro_<loja>.png         o letreiro apagado (com o texto escuro)
#   letreiros/letreiro_<loja>_aceso.png   só os pixels que acendem (o neon e o
#                                         brilho), para por cima do apagado,
#                                         sem receber a luz do Godot (SemLuz)
#   fundo_<sala>.png                      a parede e o piso da sala numa imagem só
# Com CATALOGO=1 monta folhas com as peças. Não commitar.
#
# ---------------------------------------------------------------------------
# O VISUAL DOS RESTAURANTES
# ---------------------------------------------------------------------------
#
# Cada restaurante tem a sua COR de neon (a mesma da vitrine na praça) e o seu
# jeito de ser, para não parecerem a mesma sala repetida:
#   TAPIOCA ORBITAL  (âmbar)    cafeteria de madeira clara e azulejo branco,
#                               com a chapa de tapioca acesa: a sala segura;
#   SELF NEBULOSA    (verde)    restaurante de bufê em tons de verde-água,
#                               piso de xadrez brilhante e uma câmara fria
#                               nos fundos;
#   CÂMARA FRIA      (ciano)    aço, gelo e névoa: onde está a célula de energia;
#   PIZZARIA QUASAR  (vermelho) tijolo vermelho, bancadas de aço e um forno de
#                               plasma, com o quadro elétrico da cozinha;
#   CHURRASCO SOLAR  (magenta)  bar escuro de luz magenta, a grelha solar e o
#                               elevador de carga que desce para o Bunker.
#
# Como na praça, o fundo de cada sala é uma imagem única (parede de 112 px em
# cima, piso embaixo); portas, letreiros e objetos entram por cima, no Godot.

import math
import os

import numpy as np

import gerar_praca_base as base

Imagem, RAMPAS, SOMBRA, dilatar = base.Imagem, base.RAMPAS, base.SOMBRA, base.dilatar
ruido = base.ruido
ciclico = base.ruido_ciclico
kit = base.kit
L = base.PECA
H = base.ALTURA_PAREDE
LUZ = 0.78



def espelho(img):
    nova = Imagem(img.w, img.h)
    nova.px = img.px[:, ::-1].copy()
    return nova


# ---------------------------------------------------------------------------
# Letreiros
# ---------------------------------------------------------------------------


def letreiro(texto, cor, largura=240, altura=28, tamanho=16, pes=True):
    """O letreiro de neon: caixa de grafite com moldura de neon, o nome em
    letras de 16 px e dois enfeites nas pontas. Devolve (apagado, aceso).

    O APAGADO é a caixa com o neon quase sem luz. O ACESO só tem os pixels
    que brilham: a moldura, as letras e o brilho em volta delas, que é
    pintado com o dithering de anéis (base.brilho) e vira um pontilhado que
    some aos poucos. O Godot põe o aceso por cima, sem receber luz, quando
    a energia volta (marca convivencia_energia)."""
    rampa = base.NEON[cor]
    apagado = Imagem(largura, altura + (4 if pes else 0))
    aceso = Imagem(largura, altura + (4 if pes else 0))
    for img in (apagado, aceso):
        img.fino = ciclico(largura, img.h, 2, 2, 900)
    X, Y = apagado.X, apagado.Y
    caixa = apagado.ret(0, 0, largura, altura)
    apagado.pintar(caixa, "grafite", 0.16 + 0.05 * apagado.fino + 0.2 * (Y == 0) + 0.1 * (X == 0) - 0.06 * (X == largura - 1))
    apagado.pintar(apagado.ret(0, altura - 2, largura, altura), "grafite", 0.07)
    if pes:
        for x in (largura // 6, largura - largura // 6 - 6):
            apagado.pintar(apagado.ret(x, altura, x + 6, altura + 4), "inox", 0.3 + 0.15 * (X == x))
    moldura = apagado.ret(3, 3, largura - 3, altura - 3) & ~apagado.ret(4, 4, largura - 4, altura - 4)
    apagado.pintar(moldura, rampa, 0.14, achatar=False)
    largura_texto = base.largura_do_texto(texto, tamanho)
    x_texto = (largura - largura_texto) // 2
    linhas_texto = np.where(base.texto_em_pixel(texto, tamanho).any(axis=1))[0]
    y_texto = altura // 2 + 8 - 1 - int(linhas_texto[-1])
    mascara = base.escrever(apagado, x_texto, y_texto, texto, rampa, 0.16, tamanho)
    # Enfeites: um losango de cada lado do nome.
    losangos = np.zeros((apagado.h, largura), dtype=bool)
    for cx in (12, largura - 13):
        losangos |= (np.abs(X + 0.5 - cx) + np.abs(Y + 0.5 - altura / 2.0)) < 5
    apagado.pintar(losangos, rampa, 0.14, achatar=False)
    # O aceso: moldura, letras e losangos com o brilho em volta.
    aceso.pintar(moldura, rampa, 0.86, achatar=False)
    aceso.pintar(mascara, rampa, 0.94, achatar=False)
    aceso.pintar(losangos, rampa, 0.82, achatar=False)
    base.brilho(aceso, mascara | losangos, rampa, raio=3, forca=0.5)
    base.brilho(aceso, moldura, rampa, raio=2, forca=0.35, so_vazio=True)
    return apagado, aceso


def letreiros():
    saida = {}
    for loja in ("loja_1", "loja_2", "loja_3", "loja_4"):
        saida[f"letreiro_{loja}"] = letreiro(base.NOME_LOJA[loja], base.COR_LOJA[loja])
    saida["letreiro_entrada"] = letreiro("CENTRO DE CONVIVÊNCIA", "ciano", 400, 28, 16, pes=False)
    return saida


def main():
    import gerar_interiores as interiores
    print("Gerando os restaurantes em", os.path.relpath(base.PASTA_PRACA, base.PASTA_PROJETO))
    fundos = []
    for nome in interiores.SALAS:
        fundo, luz = interiores.montar_fundo(nome)
        base.salvar(fundo, f"fundo_{nome}.png")
        base.salvar(luz, f"fundo_{nome}_luz.png")
        fundos.append((f"fundo_{nome}", fundo))
    base.salvar_catalogo("praca_fundos", fundos, 2, 1)
    amostra = []
    for nome, (apagado, aceso) in letreiros().items():
        base.salvar(apagado, f"{nome}.png", "letreiros")
        base.salvar(aceso, f"{nome}_aceso.png", "letreiros")
        visto = Imagem(apagado.w, apagado.h)
        visto.colar(apagado, 0, 0)
        visto.colar(aceso, 0, 0)
        amostra += [(nome, apagado), (nome + "_ac", visto)]
    base.salvar_catalogo("praca_letreiros", amostra, 2, 2)


if __name__ == "__main__":
    main()
