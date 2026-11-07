# gerar_gabriel_arma.py — o Gabriel de lado com a arma de pulso no antebraço.
#
# Como rodar (sem abrir a janela do Blender; precisa do gerar_gabriel.py ao lado):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_gabriel_arma.py
#
# O que sai:
#   assets/sprites/personagens/gabriel/gabriel_arma_lado.png
#       3 quadros de 96 x 112 lado a lado (o mesmo tamanho dos outros sprites do
#       Gabriel), de lado, olhando para a direita, na paleta dele:
#         0 normal   braço caído, arma apagada
#         1 mirando  braço estendido, luzes da arma acesas
#         2 atirando braço estendido, rajada ciano no bocal
#   scripts/personagens/quadros_arma_gabriel.gd
#       onde está o bocal da arma em cada quadro (em pixels do quadro), para o
#       jogo desenhar a onda de impulso saindo dali.
#
# A arma NÃO é modelada no Blender (não teria a paleta do jogo): é pixel art
# desenhada aqui, no mesmo estilo do ícone do item, e colada por cima do braço.
# O Blender só diz onde o cotovelo e a mão estão em cada pose:
#
#     px = u · largura         py = (1 - v) · altura
#
# (a função world_to_camera_view faz a conta). O antebraço é o segmento
# cotovelo -> mão. A arma é desenhada com o bocal para a direita e girada de 90
# em 90 graus (sem perda), então só serve para antebraço na horizontal ou na
# vertical: as poses abaixo respeitam isso.

import math
import os
import sys

sys.dont_write_bytecode = True
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA_SCRIPT)
import comum as c  # noqa: E402
import numpy as np  # noqa: E402
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402

_fonte = open(os.path.join(PASTA_SCRIPT, "gerar_gabriel.py"), encoding="utf-8").read()
_fonte = _fonte.rsplit("\nmain()", 1)[0]
gg = {"__file__": os.path.join(PASTA_SCRIPT, "gerar_gabriel.py"), "__name__": "gerar_gabriel"}
exec(compile(_fonte, "gerar_gabriel.py", "exec"), gg)

PASTA_SPRITES_GABRIEL = os.path.join(c.PASTA_SPRITES, "gabriel")
SAIDA_TIRA = os.path.join(PASTA_SPRITES_GABRIEL, "gabriel_arma_lado.png")
SAIDA_TABELA = os.path.join(c.PASTA_PROJETO, "scripts", "personagens", "quadros_arma_gabriel.gd")
SPRITE_REFERENCIA = os.path.join(PASTA_SPRITES_GABRIEL, "gabriel_lado.png")

# (ombro, cotovelo, tronco, cabeça, luzes da arma, rajada) de cada quadro.
POSES = [
    (0,   0, 0, 0, "apagada", False),
    (-88, 0, 5, -2, "acesa", False),
    (-88, 0, 7, -2, "acesa", True),
]


PALETA_ARMA = {
    ".": None,
    "k": (14, 18, 26),
    "d": (38, 48, 64),
    "m": (70, 88, 112),
    "l": (120, 144, 170),
    "c": (90, 235, 255),
    "w": (215, 252, 255),
}
CIANO_APAGADO = (34, 96, 112)
BRANCO_APAGADO = (70, 150, 165)

# A arma de lado, bocal para a direita: 20 colunas x 9 linhas. O cano fica em
# cima (linhas 0 a 3), a braçadeira abraça o antebraço (linhas 3 a 8, colunas
# 2 a 13) e a mão fica livre à direita dela, por baixo do cano.
ARMA = [
    ".....kkkkkkkkkkkkkkk",
    ".....kllllllllllllck",
    ".....kmmmmmmmmmmmkwk",
    "..kkkkkkkkkkkkkkkkck",
    "..klllllllllllk.....",
    "..kmmmcccmmmmk......",
    "..kddddddddddk......",
    "..kdccdccdccdk......",
    "..kkkkkkkkkkkk......",
]
CENTRO_DO_CORPO = (7.5, 6.0)
BOCAL = (19.5, 2.0)


def arma_em_pixels(luzes):
    altura, largura = len(ARMA), len(ARMA[0])
    img = np.zeros((altura, largura, 4), dtype=np.float32)
    for y, linha in enumerate(ARMA):
        for x, ch in enumerate(linha):
            cor = PALETA_ARMA[ch]
            if cor is None:
                continue
            if luzes == "apagada" and ch == "c":
                cor = CIANO_APAGADO
            if luzes == "apagada" and ch == "w":
                cor = BRANCO_APAGADO
            img[y, x] = (cor[0] / 255, cor[1] / 255, cor[2] / 255, 1.0)
    return img


def colar(quadro, arma, x0, y0):
    for y in range(arma.shape[0]):
        for x in range(arma.shape[1]):
            if arma[y, x, 3] > 0 and 0 <= y0 + y < quadro.shape[0] and 0 <= x0 + x < quadro.shape[1]:
                quadro[y0 + y, x0 + x] = arma[y, x]


def desenhar_rajada(quadro, bx, by):
    ciano = (90 / 255, 235 / 255, 255 / 255, 1.0)
    branco = (215 / 255, 252 / 255, 1.0, 1.0)
    for y in range(quadro.shape[0]):
        for x in range(quadro.shape[1]):
            dx, dy = x + 0.5 - bx, y + 0.5 - by
            dist = math.hypot(dx, dy)
            ang = math.degrees(math.atan2(dy, dx)) if dist > 0 else 0.0
            if dist <= 1.6:
                quadro[y, x] = branco
            elif dist <= 4.6 and abs(ang) <= 50 and (x + y) % 2 == 0:
                quadro[y, x] = ciano
            elif abs(dist - 3.2) < 0.55 and abs(ang) <= 28:
                quadro[y, x] = branco


def paleta_do_gabriel():
    img = c._ler_png(SPRITE_REFERENCIA)
    cores = {tuple(p) for p in np.round(img[img[..., 3] > 0][:, :3] * 255).astype(int)}
    return sorted(cores)


def girar(parado, nome, graus_x):
    rot, _ = parado[nome]
    bpy.data.objects[nome].rotation_euler = (rot[0] + math.radians(graus_x), rot[1], rot[2])


def aplicar_pose(parado, ombro, cotovelo, tronco, cabeca):
    c.restaurar_pose(parado)
    girar(parado, "BracoDirOmbro", ombro)
    girar(parado, "BracoDirCotovelo", cotovelo)
    girar(parado, "Tronco", tronco)
    girar(parado, "Cabeca", cabeca)
    bpy.context.view_layer.update()


def para_pixel(cam, ponto):
    cena = bpy.context.scene
    u, v, _ = world_to_camera_view(cena, cam, ponto)
    return u * cena.render.resolution_x, (1.0 - v) * cena.render.resolution_y


def main():
    c.DETALHE = gg["DETALHE"]
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = gg["criar_materiais"]()
    c.usar_colecao("Gabriel")
    raiz = gg["montar"](mt)
    c.achatar_sombra("Rosto")
    bpy.data.objects["Boca"].hide_render = True
    bpy.data.objects["BocaAberta"].hide_render = True
    cam = c.criar_camera()
    c.criar_luzes()
    parado = c.guardar_pose()

    quadros = []
    pontos = []
    for i, (ombro, cotovelo, tronco, cabeca, luzes, rajada) in enumerate(POSES):
        aplicar_pose(parado, ombro, cotovelo, tronco, cabeca)
        img, ind, _ = c.renderizar_vista(cam, raiz, materiais, 90, c.QUADRO_JOGO_2X, c.PX_POR_M_JOGO_2X, c.PE_JOGO_2X)
        quadros.append(c.contorno(img, ind, materiais))
        cotovelo_px = para_pixel(cam, bpy.data.objects["BracoDirCotovelo"].matrix_world.translation)
        mao_px = para_pixel(cam, bpy.data.objects["BracoDirMao"].matrix_world.translation)
        pontos.append((cotovelo_px, mao_px))
        print(f"[arma] quadro {i + 1}/{len(POSES)}: cotovelo {cotovelo_px} mao {mao_px}")

    paleta = paleta_do_gabriel()
    quadros = c.aplicar_paleta(quadros, paleta)

    tabela = []
    for i, ((cotovelo_px, mao_px), (_, _, _, _, luzes, com_rajada)) in enumerate(zip(pontos, POSES)):
        arma = arma_em_pixels(luzes)
        meio = ((cotovelo_px[0] + mao_px[0]) / 2, (cotovelo_px[1] + mao_px[1]) / 2)
        bocal = BOCAL
        if i == 0:
            arma = np.rot90(arma, k=-1)
            altura = len(ARMA)
            bocal = (altura - BOCAL[1], BOCAL[0])
            centro = (altura - CENTRO_DO_CORPO[1], CENTRO_DO_CORPO[0])
        else:
            centro = CENTRO_DO_CORPO
        x0 = int(round(meio[0] - centro[0]))
        y0 = int(round(meio[1] - centro[1]))
        colar(quadros[i], arma, x0, y0)
        bx, by = x0 + bocal[0], y0 + bocal[1]
        if com_rajada:
            desenhar_rajada(quadros[i], bx + 0.5, by)
        tabela.append((bx, by))

    tira = np.concatenate(quadros, axis=1)
    c.salvar_png(tira, SAIDA_TIRA)

    linhas = ["const QUADROS := ["]
    for bx, by in tabela:
        linhas.append("\tVector2(%.1f, %.1f)," % (bx, by))
    linhas.append("]")
    with open(SAIDA_TABELA, "w", encoding="utf-8", newline="\n") as arq:
        arq.write("\n".join(linhas) + "\n")
    print("[arma] pronto")


main()
