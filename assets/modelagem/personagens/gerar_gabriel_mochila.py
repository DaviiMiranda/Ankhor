# gerar_gabriel_mochila.py — anima o Gabriel tirando a mochila de um ombro,
# trazendo-a para a frente da barriga e abrindo, para a tela do inventário
# (docs/mecanicas/itens_e_inventario.md).
#
# Como rodar (sem abrir a janela do Blender; precisa do gerar_gabriel.py ao lado):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_gabriel_mochila.py
#
# Para testar uma vista só (mais rápido), passe o nome dela depois de --:
#
#   blender -b --factory-startup --python .../gerar_gabriel_mochila.py -- lado
#
# O que sai (24 quadros de 96 x 112 lado a lado, na paleta dele):
#   assets/sprites/personagens/gabriel/gabriel_mochila_lado.png
#   assets/sprites/personagens/gabriel/gabriel_mochila_frente.png
#   assets/sprites/personagens/gabriel/gabriel_mochila_tres_quartos.png
#   assets/sprites/personagens/gabriel/gabriel_mochila_costas.png
#   assets/sprites/personagens/gabriel/gabriel_mochila_tres_quartos_costas.png
#
# A animação toca para a frente ao ABRIR o inventário e de trás para a frente
# ao FECHAR: o gesto é o mesmo ao contrário. Por isso é uma tira só por vista.
#
# ---------------------------------------------------------------------------
# A ANIMAÇÃO
# ---------------------------------------------------------------------------
#
# Cada pose-chave guarda os ângulos (em graus, somados à pose parada dele) dos
# dois braços, do tronco e da cabeça, mais o ângulo da mochila em volta do corpo.
# Girar em torno do eixo X com ângulo NEGATIVO leva o braço para a frente e para
# cima (a mesma convenção do comum.py). As poses-chave:
#
#    0 parado (igual ao sprite parado)     5-6 a mochila passa pelo lado do corpo
#    1-2 a mão direita sobe até a alça     7 a mochila chega à barriga
#    3 a alça sai do ombro                 8 a outra mão segura, a cabeça abaixa
#    4 a mochila começa a girar            9-11 a mão vai ao zíper e o puxa
#
# Os quadros entre as poses-chave saem da interpolação de Catmull-Rom. Entre as
# chaves p1 e p2, com t de 0 a 1 e os vizinhos p0 e p3:
#
#     p(t) = 0,5 · [ 2·p1 + (p2 - p0)·t + (2·p0 - 5·p1 + 4·p2 - p3)·t²
#                    + (3·p1 - p0 - 3·p2 + p3)·t³ ]
#
# A curva passa exatamente pelas chaves, e a velocidade em cada chave é a mesma
# dos dois lados, (p2 - p0) / 2. Por isso o movimento não para e recomeça a cada
# pose, como aconteceria numa interpolação linear. O quadro 0 continua igual à
# pose parada, e o último é a última chave. Como a curva pode passar um pouco das
# chaves, θ é limitado a 0°-180°.
#
# O trajeto da mochila é um círculo em volta do eixo vertical do corpo, com
# ângulo θ de 0° (nas costas) a 180° (na barriga):
#
#     x = -R(θ) · sen θ        y = R(θ) · cos θ        giro = θ
#
# O raio não é constante porque o corpo não é um cilindro: de costas ou de
# frente, 0,205 m basta para encostar no moletom; de lado, ela precisa passar por
# fora do braço. A onda sen θ faz o raio crescer só no meio do caminho:
#
#     R(θ) = 0,205 + folga · sen θ
#
# O sinal de x põe a passagem no lado direito do corpo (x negativo), o da alça
# que saiu, e é o lado que a câmera vê na vista "lado". Como a alça esquerda
# continua no ombro, a mochila gira pendurada nela.

import math
import os
import sys

sys.dont_write_bytecode = True
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA_SCRIPT)
import comum as c  # noqa: E402
import numpy as np  # noqa: E402
import bpy  # noqa: E402

# Reaproveita as funções do gerar_gabriel.py sem rodar o main() dele.
_fonte = open(os.path.join(PASTA_SCRIPT, "gerar_gabriel.py"), encoding="utf-8").read()
_fonte = _fonte.rsplit("\nmain()", 1)[0]
gg = {"__file__": os.path.join(PASTA_SCRIPT, "gerar_gabriel.py"), "__name__": "gerar_gabriel"}
exec(compile(_fonte, "gerar_gabriel.py", "exec"), gg)

PASTA_SPRITES_GABRIEL = os.path.join(c.PASTA_SPRITES, "gabriel")

PECAS_DA_MOCHILA = ("Mochila", "MochilaBolso", "MochilaZiper", "MochilaAlca")
PECAS_DA_ALCA_QUE_SAI = ("Alca-1Cima", "Alca-1Frente", "Fivela-1")

FOLGA_DO_LADO = 0.19    # quanto ela se afasta ao passar por fora do braço
DESCIDA_NA_BARRIGA = 0.07  # na frente ela fica mais baixa: pende da alça

# (ombro dir, cotovelo dir, ombro esq, cotovelo esq, tronco, cabeça, θ da mochila, alça solta)
QUADROS = 24
POSES = [
    (0,   0,    0,   0,    0,  0,   0, False),
    (-12, -78,  0,   0,    1,  0,   0, False),
    (-14, -132, 0,   0,    2,  0,   0, False),
    (2,   -112, 0,   0,    3,  1,  18, True),
    (10,  -64, -6,  -18,   4,  2,  58, True),
    (12,  -36, -14, -40,   5,  4, 100, True),
    (2,   -36, -22, -58,   6,  7, 142, True),
    (-14, -48, -28, -66,   7, 10, 180, True),
    (-24, -58, -32, -72,   8, 14, 180, True),
    (-30, -70, -32, -72,   9, 17, 180, True),
    (-38, -88, -32, -72,   9, 18, 180, True),
    (-29, -64, -33, -74,   9, 18, 180, True),
]


def catmull_rom(p0, p1, p2, p3, t):
    return 0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                  + (3 * p1 - p0 - 3 * p2 + p3) * t ** 3)


def pose_do_quadro(quadro):
    """A pose de um quadro da tira, entre duas poses-chave. Nas pontas da lista,
    a chave vizinha que falta é a própria ponta."""
    ultima = len(POSES) - 1
    posicao = quadro / (QUADROS - 1) * ultima
    i = min(int(posicao), ultima - 1)
    t = posicao - i
    vizinhas = [POSES[max(i - 1, 0)], POSES[i], POSES[i + 1], POSES[min(i + 2, ultima)]]
    angulos = [catmull_rom(*(v[campo] for v in vizinhas), t) for campo in range(7)]
    angulos[6] = min(max(angulos[6], 0.0), 180.0)
    alca_solta = POSES[i + 1][7] if t >= 0.5 else POSES[i][7]
    return (*angulos, alca_solta)


def paleta_do_gabriel():
    # A mesma leitura dos outros geradores: as cores que as tiras dele já usam.
    cores = set()
    for vista, _ in c.VISTAS_JOGO:
        img = c._ler_png(os.path.join(PASTA_SPRITES_GABRIEL, f"gabriel_{vista}.png"))
        cores |= {tuple(p) for p in np.round(img[img[..., 3] > 0][:, :3] * 255).astype(int)}
    return sorted(cores)


def preparar_pivo_da_mochila():
    """Junta as peças da mochila num pivô no centro do tronco. Com o pivô na
    origem do tronco e sem rotação, as peças não saem do lugar ao trocar de pai."""
    tronco = bpy.data.objects["Tronco"]
    pivo = c.pivo("MochilaPivo", (0, 0, 0), tronco)
    for nome in PECAS_DA_MOCHILA:
        bpy.data.objects[nome].parent = pivo
    return pivo


def girar(parado, nome, graus_x):
    rot, _ = parado[nome]
    bpy.data.objects[nome].rotation_euler = (rot[0] + math.radians(graus_x), rot[1], rot[2])


def posicionar_mochila(pivo, theta_graus):
    # Rodar o pivô em Z já leva as peças em círculo de raio 0,205 m. O que falta
    # somar é só o afastamento (folga · sen θ), na mesma direção radial.
    theta = math.radians(theta_graus)
    folga = FOLGA_DO_LADO * math.sin(theta)
    pivo.rotation_euler = (0, 0, theta)
    pivo.location = (-folga * math.sin(theta), folga * math.cos(theta),
                     -DESCIDA_NA_BARRIGA * (1 - math.cos(theta)) / 2)


def aplicar_pose(parado, pivo, pose):
    ombro_d, cotovelo_d, ombro_e, cotovelo_e, tronco, cabeca, theta, alca_solta = pose
    c.restaurar_pose(parado)
    girar(parado, "BracoDirOmbro", ombro_d)
    girar(parado, "BracoDirCotovelo", cotovelo_d)
    girar(parado, "BracoEsqOmbro", ombro_e)
    girar(parado, "BracoEsqCotovelo", cotovelo_e)
    girar(parado, "Tronco", tronco)
    girar(parado, "Cabeca", cabeca)
    posicionar_mochila(pivo, theta)
    for nome in PECAS_DA_ALCA_QUE_SAI:
        bpy.data.objects[nome].hide_render = alca_solta
    bpy.context.view_layer.update()


def vistas_pedidas():
    argumentos = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return [v for v in c.VISTAS_JOGO if not argumentos or v[0] in argumentos]


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
    pivo = preparar_pivo_da_mochila()
    parado = c.guardar_pose()

    paleta = paleta_do_gabriel()
    for vista, angulo in vistas_pedidas():
        quadros = []
        for i in range(QUADROS):
            aplicar_pose(parado, pivo, pose_do_quadro(i))
            img, ind, _ = c.renderizar_vista(cam, raiz, materiais, angulo, c.QUADRO_JOGO_2X, c.PX_POR_M_JOGO_2X, c.PE_JOGO_2X)
            quadros.append(c.contorno(img, ind, materiais))
            print(f"[mochila] {vista}: quadro {i + 1}/{QUADROS}")
        tira = np.concatenate(c.aplicar_paleta(quadros, paleta), axis=1)
        c.salvar_png(tira, os.path.join(PASTA_SPRITES_GABRIEL, f"gabriel_mochila_{vista}.png"))
    print("[mochila] pronto")


main()
