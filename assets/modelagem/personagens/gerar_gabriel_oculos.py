# gerar_gabriel_oculos.py — anima o Gabriel pegando os óculos do Zane da máquina
# de salvar e pondo no rosto (docs/mecanicas/sala_segura.md).
#
# Como rodar (sem abrir a janela do Blender; precisa do gerar_gabriel.py ao lado):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_gabriel_oculos.py
#
# O que sai:
#   assets/sprites/personagens/gabriel/gabriel_oculos_lado.png
#       12 quadros de 96 x 112 lado a lado (o mesmo tamanho dos outros sprites do
#       Gabriel), de lado, olhando para a direita, na mesma paleta dele.
#   scripts/personagens/quadros_oculos_gabriel.gd
#       a tabela que o jogo lê: em cada quadro, onde os óculos estão (em pixels
#       do quadro) e em que fase: "pedestal" (ainda na máquina), "mao" ou "rosto".
#
# A animação toca para a frente para PÔR os óculos e de trás para a frente para
# TIRAR: o gesto é o mesmo ao contrário (levar à cara, soltar a mão; levar a
# mão à cara, pegar, devolver ao pedestal). Por isso é uma tira só.
#
# ---------------------------------------------------------------------------
# A ANIMAÇÃO
# ---------------------------------------------------------------------------
#
# Cada quadro é uma pose: os ângulos (em graus, somados à pose parada dele) do
# braço da câmera (BracoDir, o que aparece de lado), do tronco e da cabeça.
# Girar em torno do eixo X com ângulo NEGATIVO leva o braço para a frente e
# para cima (a mesma convenção do comum.py). Os quadros:
#
#    0 parado             3 mão nos óculos (pega)      7 óculos no rosto
#    1 inclina e estende  4-6 levanta o braço           8 ajusta (puxa a armação)
#    2 braço quase lá     (óculos na mão)               9-11 solta a mão e relaxa
#
# Os óculos NÃO são desenhados aqui: no Blender eles não teriam a paleta do
# jogo. O que sai é a POSIÇÃO deles em cada quadro, e o Godot desenha o sprite
# do Zane (menu_oculos_zane.png) nesse ponto.
#
# A posição vem da câmera ortográfica: um ponto 3D (x, y, z) vira o pixel
#
#     px = u · largura         py = (1 - v) · altura
#
# onde (u, v) é a posição do ponto no enquadramento, de 0 a 1 (a função
# world_to_camera_view do Blender faz essa conta). O ponto é o centro da mão
# (objeto BracoDirMao) enquanto a mão carrega, e o meio dos olhos quando já
# estão no rosto.

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
from mathutils import Vector  # noqa: E402

# Reaproveita as funções do gerar_gabriel.py sem rodar o main() dele.
_fonte = open(os.path.join(PASTA_SCRIPT, "gerar_gabriel.py"), encoding="utf-8").read()
_fonte = _fonte.rsplit("\nmain()", 1)[0]
gg = {"__file__": os.path.join(PASTA_SCRIPT, "gerar_gabriel.py"), "__name__": "gerar_gabriel"}
exec(compile(_fonte, "gerar_gabriel.py", "exec"), gg)

PASTA_SPRITES_GABRIEL = os.path.join(c.PASTA_SPRITES, "gabriel")
SAIDA_TIRA = os.path.join(PASTA_SPRITES_GABRIEL, "gabriel_oculos_lado.png")
SAIDA_TABELA = os.path.join(c.PASTA_PROJETO, "scripts", "personagens", "quadros_oculos_gabriel.gd")
SPRITE_REFERENCIA = os.path.join(PASTA_SPRITES_GABRIEL, "gabriel_lado.png")

# (ombro, cotovelo, tronco, cabeça, fase dos óculos) de cada quadro.
POSES = [
    (0,   0,    0,  0, "pedestal"),
    (-22, -4,   6,  0, "pedestal"),
    (-34, -8,  12,  0, "pedestal"),
    (-38, -10, 14,  0, "mao"),
    (-42, -50,  8,  0, "mao"),
    (-48, -92,  4, -2, "mao"),
    (-54, -122, 2, -4, "mao"),
    (-58, -138, 0, -5, "rosto"),
    (-56, -146, 0, -5, "rosto"),
    (-42, -84,  0, -3, "rosto"),
    (-20, -30,  0, -2, "rosto"),
    (-4,  -6,   0, -2, "rosto"),
]
AVANCO_OCULOS_NO_ROSTO_PX = 0.5   # os óculos ficam um pouco à frente dos olhos
DESCIDA_OCULOS_NO_ROSTO_PX = 1.5  # e um pouco abaixo: a armação cobre os olhos, não a testa


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
    tabela = []
    for i, (ombro, cotovelo, tronco, cabeca, fase) in enumerate(POSES):
        aplicar_pose(parado, ombro, cotovelo, tronco, cabeca)
        img, ind, _ = c.renderizar_vista(cam, raiz, materiais, 90, c.QUADRO_JOGO_2X, c.PX_POR_M_JOGO_2X, c.PE_JOGO_2X)
        quadros.append(c.contorno(img, ind, materiais))
        if fase == "rosto":
            olhos = [bpy.data.objects[f"Olho{lado}"].matrix_world.translation for lado in (-1, 1)]
            x, y = para_pixel(cam, (olhos[0] + olhos[1]) / 2)
            x += AVANCO_OCULOS_NO_ROSTO_PX
            y += DESCIDA_OCULOS_NO_ROSTO_PX
        else:
            x, y = para_pixel(cam, bpy.data.objects["BracoDirMao"].matrix_world.translation)
        tabela.append((x, y, fase))
        print(f"[oculos] quadro {i + 1}/{len(POSES)}: {fase} em ({x:.1f}, {y:.1f})")

    paleta = paleta_do_gabriel()
    tira = np.concatenate(c.aplicar_paleta(quadros, paleta), axis=1)
    c.salvar_png(tira, SAIDA_TIRA)

    linhas = ["const QUADROS := ["]
    for x, y, fase in tabela:
        linhas.append('\t{"ponto": Vector2(%.1f, %.1f), "fase": "%s"},' % (x, y, fase))
    linhas.append("]")
    with open(SAIDA_TABELA, "w", encoding="utf-8", newline="\n") as arq:
        arq.write("\n".join(linhas) + "\n")
    print("[oculos] pronto")


main()
