# gerar_gabriel_arma.py — o Gabriel mirando e atirando com a arma de pulso, nas
# cinco vistas do jogo (de lado, de frente, de costas e os dois três quartos).
#
# Como rodar (sem abrir a janela do Blender; precisa do gerar_gabriel.py ao lado):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_gabriel_arma.py
#
# O que sai:
#   assets/sprites/personagens/gabriel/gabriel_arma_<vista>.png
#       2 quadros de 96 x 112 lado a lado (o mesmo tamanho dos outros sprites do
#       Gabriel), um arquivo por vista, na paleta dele mais os tons da arma:
#         0 mirando   braço estendido para a frente, luzes da arma acesas
#         1 atirando  o mesmo, com a rajada de pulso no bocal
#       Para a esquerda, o Godot espelha o sprite (flip_h), como nos outros.
#   scripts/personagens/quadros_arma_gabriel.gd
#       BOCAIS[vista][quadro]: onde está o bocal da arma (em pixels do quadro),
#       para o jogo pôr o clarão do tiro ali.
#
# A arma é MODELADA no Blender (peças de caixa e cilindro presas ao antebraço),
# e não desenhada à mão em cada ângulo: assim ela gira junto com o corpo e sai
# certa em todas as vistas. Ela entra no mesmo pipeline do Gabriel: cada peça tem
# um material de 4 tons (sombra funda, sombra, luz, brilho) e as luzes ciano são
# materiais "planos" (cor chapada, sem sombra).
#
# O braço aponta sempre "para a frente do corpo". Como o Gabriel gira inteiro
# para olhar para a direção da mira (de lado, de frente, de costas...), a mesma
# pose serve nas cinco vistas: o que muda é o ângulo da câmera.
#
# O bocal: um ponto 3D (o objeto Bocal, na ponta do cano) vira o pixel
#
#     px = u · largura         py = (1 - v) · altura
#
# (a função world_to_camera_view do Blender faz a conta, como no
# gerar_gabriel_oculos.py). A direção do tiro na imagem é a reta do cotovelo ao
# bocal. De frente e de costas o braço aponta para a câmera ou para longe, essa
# reta quase some (menos de 4 px), e a rajada sai redonda, em todas as direções.

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
SAIDA_TABELA = os.path.join(c.PASTA_PROJETO, "scripts", "personagens", "quadros_arma_gabriel.gd")
SPRITE_REFERENCIA = os.path.join(PASTA_SPRITES_GABRIEL, "gabriel_lado.png")

# (ombro, cotovelo, tronco, cabeça, com rajada) de cada quadro. Girar em torno
# do eixo X com ângulo NEGATIVO leva o braço para a frente e para cima.
POSES = [
    (-88, 0, 5, -2, False),
    (-88, 0, 7, -2, True),
]

CIANO = (90, 235, 255)
BRANCO = (215, 252, 255)


def criar_arma(materiais):
    """A arma presa ao antebraço (o pivô BracoDirCotovelo). No sistema do
    antebraço o -Z é para a ponta da mão e o -Y é para cima quando o braço está
    estendido para a frente."""
    aco = materiais.novo("arma_aco", "#4a5d78")
    claro = materiais.novo("arma_aco_claro", "#7d93ad")
    escuro = materiais.novo("arma_aco_escuro", "#27303f")
    luz = materiais.novo("arma_luz", "#5aebff", "plano")
    cotovelo = bpy.data.objects["BracoDirCotovelo"]

    c.cone("ArmaBraco", 0.074, 0.074, 0.15, (0, 0, -0.135), aco, cotovelo, lados=8)
    c.cone("ArmaAnelA", 0.082, 0.082, 0.022, (0, 0, -0.07), escuro, cotovelo, lados=8)
    c.cone("ArmaAnelB", 0.082, 0.082, 0.022, (0, 0, -0.20), escuro, cotovelo, lados=8)
    c.caixa("ArmaPlaca", (0.05, 0.03, 0.17), (0, -0.075, -0.13), claro, cotovelo, bisel=0.006)
    c.cone("ArmaCano", 0.027, 0.027, 0.33, (0, -0.108, -0.225), aco, cotovelo, lados=8)
    c.cone("ArmaBocal", 0.036, 0.036, 0.035, (0, -0.108, -0.385), escuro, cotovelo, lados=8)
    c.cone("ArmaNucleo", 0.02, 0.02, 0.012, (0, -0.108, -0.405), luz, cotovelo, lados=8)
    c.caixa("ArmaFaixaCano", (0.012, 0.012, 0.18), (0, -0.138, -0.2), luz, cotovelo)
    for lado in (-1, 1):
        c.caixa(f"ArmaFaixa{lado}", (0.012, 0.012, 0.11), (0.078 * lado, 0, -0.135), luz, cotovelo)
    c.pivo("Bocal", (0, -0.108, -0.41), cotovelo)


def paleta_do_gabriel():
    img = c._ler_png(SPRITE_REFERENCIA)
    cores = {tuple(p) for p in np.round(img[img[..., 3] > 0][:, :3] * 255).astype(int)}
    return sorted(cores)


def paleta_da_arma(materiais):
    cores = set()
    for (nome, _, _, _), rampa in zip(materiais.lista, materiais.rampas()):
        if nome.startswith("arma_"):
            for tom in rampa:
                cores.add(tuple(int(round(v * 255)) for v in tom))
    cores.add(CIANO)
    cores.add(BRANCO)
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


def desenhar_rajada(quadro, bocal, direcao):
    """Rajada de pulso no bocal: núcleo branco, raios ciano e um arco. Com
    'direcao' (ângulo em graus no quadro) ela abre num leque de +-50 graus; com
    None sai redonda."""
    ciano = (*(v / 255 for v in CIANO), 1.0)
    branco = (*(v / 255 for v in BRANCO), 1.0)
    altura, largura = quadro.shape[:2]
    for y in range(altura):
        for x in range(largura):
            dx, dy = x + 0.5 - bocal[0], y + 0.5 - bocal[1]
            dist = math.hypot(dx, dy)
            desvio = 0.0 if direcao is None else abs((math.degrees(math.atan2(dy, dx)) - direcao + 180) % 360 - 180)
            if dist <= 1.6:
                quadro[y, x] = branco
            elif dist <= 4.6 and desvio <= 50 and (x + y) % 2 == 0:
                quadro[y, x] = ciano
            elif abs(dist - 3.2) < 0.55 and desvio <= 28:
                quadro[y, x] = branco


def main():
    c.DETALHE = gg["DETALHE"]
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = gg["criar_materiais"]()
    c.usar_colecao("Gabriel")
    raiz = gg["montar"](mt)
    criar_arma(materiais)
    c.achatar_sombra("Rosto")
    bpy.data.objects["Boca"].hide_render = True
    bpy.data.objects["BocaAberta"].hide_render = True
    cam = c.criar_camera()
    c.criar_luzes()
    parado = c.guardar_pose()
    paleta = paleta_do_gabriel() + paleta_da_arma(materiais)

    tabela = {}
    for vista, angulo in c.VISTAS_JOGO:
        quadros, bocais = [], []
        for ombro, cotovelo, tronco, cabeca, com_rajada in POSES:
            aplicar_pose(parado, ombro, cotovelo, tronco, cabeca)
            img, ind, _ = c.renderizar_vista(cam, raiz, materiais, angulo, c.QUADRO_JOGO_2X, c.PX_POR_M_JOGO_2X, c.PE_JOGO_2X)
            img = c.contorno(img, ind, materiais)
            img = c.aplicar_paleta([img], paleta)[0]
            ponta = para_pixel(cam, bpy.data.objects["Bocal"].matrix_world.translation)
            origem = para_pixel(cam, bpy.data.objects["BracoDirCotovelo"].matrix_world.translation)
            dx, dy = ponta[0] - origem[0], ponta[1] - origem[1]
            direcao = math.degrees(math.atan2(dy, dx)) if math.hypot(dx, dy) >= 4.0 else None
            if com_rajada:
                desenhar_rajada(img, ponta, direcao)
            quadros.append(img)
            bocais.append(ponta)
        c.salvar_png(np.concatenate(quadros, axis=1), os.path.join(PASTA_SPRITES_GABRIEL, f"gabriel_arma_{vista}.png"))
        tabela[vista] = bocais
        print(f"[arma] {vista}: bocal em {[(round(x, 1), round(y, 1)) for x, y in bocais]}")

    linhas = ["const BOCAIS := {"]
    for vista, bocais in tabela.items():
        pontos = ", ".join("Vector2(%.1f, %.1f)" % (x, y) for x, y in bocais)
        linhas.append(f'\t"{vista}": [{pontos}],')
    linhas.append("}")
    with open(SAIDA_TABELA, "w", encoding="utf-8", newline="\n") as arq:
        arq.write("\n".join(linhas) + "\n")
    print("[arma] pronto")


main()
