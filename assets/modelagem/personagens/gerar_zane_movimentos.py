# gerar_zane_movimentos.py — anima o Zane correndo e estendendo o braço para
# hackear um robô, nas cinco vistas de jogo, e mede onde fica a mão que segura
# a lanterna em todos os quadros dele (parado, andando, correndo e hackeando).
#
# Como rodar (sem abrir a janela do Blender; precisa do gerar_zane.py ao lado):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_zane_movimentos.py
#
# Para testar uma vista só (mais rápido), passe o nome dela depois de --:
#
#   blender -b --factory-startup --python .../gerar_zane_movimentos.py -- lado
#
# O que sai:
#   assets/sprites/personagens/zane/zane_correr_<vista>.png   48 quadros de 96 x 112
#   assets/sprites/personagens/zane/zane_hack_<vista>.png     12 quadros de 96 x 112
#   scripts/personagens/maos_do_zane.gd                       as tabelas de mãos (MAOS,
#       MAOS_CORRENDO e MAOS_HACK), do mesmo jeito das do Gabriel
#
# ---------------------------------------------------------------------------
# A CORRIDA
# ---------------------------------------------------------------------------
#
# A mesma ideia da corrida do Gabriel (gerar_gabriel_correr.py), com a mesma fase φ
# da caminhada, mas com QUATRO vezes os quadros da caminhada (48 contra 12): cada
# quadro avança 7,5° e os pés se cruzam nos quadros 0 e 24. Como o jogo troca de
# tira no mesmo ponto do ciclo (quadro = fase · 48 / 12), não há salto. Mais quadros
# deixam o movimento fluido, porque cada pose difere pouco da vizinha.
#
#   coxa      = C0 - C · sen(φ) - E · max(0, -cos φ)^1,5
#   joelho    = J0 + J · max(0, cos φ)^1,2 + F · max(0, -cos φ)^1,5
#   ombro     = A · sen(φ), ao contrário da perna do mesmo lado
#   cotovelo  = -(B + D · (1 - sen(φ - ATRASO)) / 2)
#
# A diferença está na postura. O Gabriel corre curvado (tronco 13° para a frente).
# O Zane corre ereto: o tronco só inclina 5° por cima da pose parada, que já é um
# pouco para trás (-2°), e a cabeça desfaz a inclinação para o queixo continuar
# erguido. O passo é largo e saltado (coxa e joelho maiores e mais tempo no ar,
# VOO maior), do jeito elétrico dele, e o braço de metal balança como o outro.
#
# A altura do quadril sai da perna mais esticada, h = L1·cos(a) + L2·cos(a + b) + SOLA,
# suavizada só com a média e a onda na frequência dos passos (série de Fourier),
# como no Gabriel: o corpo não dá tranco a cada passo.
#
# ---------------------------------------------------------------------------
# O BRAÇO DE HACK
# ---------------------------------------------------------------------------
#
# Poses-chave (ângulos em graus somados à pose parada; ângulo negativo em X leva o
# braço para a frente e para cima): o braço de metal sobe do lado do corpo até ficar
# esticado na horizontal, apontando para a frente, o outro braço recua para
# equilibrar e o tronco se inclina um pouco. Os quadros entre as chaves saem de
# Catmull-Rom (ver gerar_gabriel_mochila.py). No jogo a tira toca até o fim, o último
# quadro fica parado enquanto o minigame está aberto, e depois ela toca ao contrário.
#
# ---------------------------------------------------------------------------
# AS MÃOS
# ---------------------------------------------------------------------------
#
# A lanterna fica na mão que está mais à direita do quadro na pose parada, em cada
# vista, e essa mesma mão é seguida pelo modelo 3D em todos os quadros:
#
#   px = u · largura         py = (1 - v) · altura
#
# onde (u, v) é a posição do ponto no enquadramento (world_to_camera_view). Na tira
# de hack a mão é sempre a do braço de metal, que é a que se estende.

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

_fonte = open(os.path.join(PASTA_SCRIPT, "gerar_zane.py"), encoding="utf-8").read()
_fonte = _fonte.rsplit("\nmain()", 1)[0]
gz = {"__file__": os.path.join(PASTA_SCRIPT, "gerar_zane.py"), "__name__": "gerar_zane"}
exec(compile(_fonte, "gerar_zane.py", "exec"), gz)

PASTA_ZANE = os.path.join(c.PASTA_SPRITES, "zane")
SAIDA_TABELA = os.path.join(c.PASTA_PROJETO, "scripts", "personagens", "maos_do_zane.gd")

QUADROS_CORRER = 48
QUADROS_HACK = 12
BRACO_DE_HACK = "BracoDir"

COXA_MEIO, COXA, COXA_APOIO = -9, 38, 22
JOELHO_BASE, JOELHO_AR, JOELHO_APOIO = 12, 86, 34
JOELHO_REPOUSO = 2.5
OMBRO, COTOVELO, COTOVELO_FRENTE, ATRASO_COTOVELO = 40, 62, 22, 35
INCLINACAO_TRONCO, TORCAO_TRONCO = 5, 4
CABECA_LEVANTA, CABECA_DESTORCE = -6, 3
PE_NO_AR = 30
COXA_M, CANELA_M, SOLA_M = 0.43, 0.37, 0.122
VOO_M = 0.026

# (ombro do braço de metal, cotovelo dele, ombro do outro, cotovelo do outro, tronco, cabeça)
POSES_HACK = [
    (0,   0,   0,   0,   0, 0),
    (-30, -62, 4,  -8,   2, 0),
    (-68, -38, 10, -14,  4, -2),
    (-92, -10, 14, -18,  5, -4),
    (-98, -3,  16, -20,  6, -5),
]


def paleta_do_zane():
    cores = set()
    for vista, _ in c.VISTAS_JOGO:
        img = c._ler_png(os.path.join(PASTA_ZANE, f"zane_andar_{vista}.png"))
        cores |= {tuple(p) for p in np.round(img[img[..., 3] > 0][:, :3] * 255).astype(int)}
    return sorted(cores)


def girar(parado, nome, x=0.0, z=0.0):
    rot, _ = parado[nome]
    bpy.data.objects[nome].rotation_euler = (rot[0] + math.radians(x), rot[1], rot[2] + math.radians(z))


def girar_absoluto(parado, nome, x):
    rot, _ = parado[nome]
    bpy.data.objects[nome].rotation_euler = (math.radians(x), rot[1], rot[2])


def altura_da_perna(a_graus, b_graus):
    a = math.radians(a_graus)
    return COXA_M * math.cos(a) + CANELA_M * math.cos(a + math.radians(b_graus)) + SOLA_M


def angulos_da_perna(fase):
    phi = math.radians(fase)
    no_ar = max(0.0, math.cos(phi))
    no_apoio = max(0.0, -math.cos(phi))
    coxa = COXA_MEIO - COXA * math.sin(phi) - COXA_APOIO * no_apoio ** 1.5
    joelho = JOELHO_REPOUSO + JOELHO_BASE + JOELHO_AR * no_ar ** 1.2 + JOELHO_APOIO * no_apoio ** 1.5
    return coxa, joelho, no_ar


def altura_crua(fase):
    alturas = [altura_da_perna(*angulos_da_perna(fase + desloc)[:2]) for desloc in (0, 180)]
    return max(alturas) + VOO_M * math.sin(math.radians(2 * fase)) ** 2


def onda_do_quadril(amostras=720):
    fases = [360 * i / amostras for i in range(amostras)]
    alturas = [altura_crua(fase) for fase in fases]
    media = sum(alturas) / amostras
    a = 2 * sum(h * math.cos(math.radians(2 * f)) for h, f in zip(alturas, fases)) / amostras
    b = 2 * sum(h * math.sin(math.radians(2 * f)) for h, f in zip(alturas, fases)) / amostras
    return media, a, b


ONDA_QUADRIL = onda_do_quadril()


def altura_suave(fase):
    media, a, b = ONDA_QUADRIL
    dobro = math.radians(2 * fase)
    return media + a * math.cos(dobro) + b * math.sin(dobro)


def pose_correr(parado, fase):
    c.restaurar_pose(parado)
    for perna, desloc in (("PernaDir", 0), ("PernaEsq", 180)):
        coxa, joelho, no_ar = angulos_da_perna(fase + desloc)
        girar_absoluto(parado, f"{perna}Quadril", coxa)
        girar_absoluto(parado, f"{perna}Joelho", joelho)
        girar_absoluto(parado, f"{perna}Tornozelo", -coxa - joelho + PE_NO_AR * no_ar)
    for braco, desloc in (("BracoDir", 0), ("BracoEsq", 180)):
        seno = math.sin(math.radians(fase + desloc))
        atrasado = math.sin(math.radians(fase + desloc - ATRASO_COTOVELO))
        girar(parado, f"{braco}Ombro", OMBRO * seno)
        girar(parado, f"{braco}Cotovelo", -(COTOVELO + COTOVELO_FRENTE * (1 - atrasado) / 2))
    seno = math.sin(math.radians(fase))
    girar(parado, "Tronco", INCLINACAO_TRONCO, -TORCAO_TRONCO * seno)
    girar(parado, "Cabeca", CABECA_LEVANTA, CABECA_DESTORCE * seno)
    _, pos = parado["Quadril"]
    bpy.data.objects["Quadril"].location = (pos[0], pos[1], altura_suave(fase))
    bpy.context.view_layer.update()


def catmull_rom(p0, p1, p2, p3, t):
    return 0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                  + (3 * p1 - p0 - 3 * p2 + p3) * t ** 3)


def pose_do_quadro_de_hack(quadro):
    ultima = len(POSES_HACK) - 1
    posicao = quadro / (QUADROS_HACK - 1) * ultima
    i = min(int(posicao), ultima - 1)
    t = posicao - i
    vizinhas = [POSES_HACK[max(i - 1, 0)], POSES_HACK[i], POSES_HACK[i + 1], POSES_HACK[min(i + 2, ultima)]]
    return [catmull_rom(*(v[campo] for v in vizinhas), t) for campo in range(6)]


def pose_hack(parado, quadro):
    ombro_m, cotovelo_m, ombro_o, cotovelo_o, tronco, cabeca = pose_do_quadro_de_hack(quadro)
    c.restaurar_pose(parado)
    girar(parado, "BracoDirOmbro", ombro_m)
    girar(parado, "BracoDirCotovelo", cotovelo_m)
    girar(parado, "BracoEsqOmbro", ombro_o)
    girar(parado, "BracoEsqCotovelo", cotovelo_o)
    girar(parado, "Tronco", tronco)
    girar(parado, "Cabeca", cabeca)
    bpy.context.view_layer.update()


def para_pixel(cam, ponto):
    cena = bpy.context.scene
    u, v, _ = world_to_camera_view(cena, cam, ponto)
    return u * cena.render.resolution_x, (1.0 - v) * cena.render.resolution_y


def posicao_da_mao(cam, braco):
    return para_pixel(cam, bpy.data.objects[f"{braco}Mao"].matrix_world.translation)


def renderizar(cam, raiz, materiais, angulo):
    return c.renderizar_vista(cam, raiz, materiais, angulo, c.QUADRO_JOGO_2X, c.PX_POR_M_JOGO_2X, c.PE_JOGO_2X)


def braco_da_lanterna(cam, raiz, materiais, angulo):
    renderizar(cam, raiz, materiais, angulo)
    bpy.context.view_layer.update()
    return max(("BracoDir", "BracoEsq"), key=lambda braco: posicao_da_mao(cam, braco)[0])


def vistas_pedidas():
    argumentos = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return [v for v in c.VISTAS_JOGO if not argumentos or v[0] in argumentos]


def medir(cam, raiz, materiais, angulo, braco, parado, pose, quadros):
    pontos = []
    for q in range(quadros):
        c.restaurar_pose(parado)
        pose(q)
        bpy.context.view_layer.update()
        renderizar(cam, raiz, materiais, angulo)
        bpy.context.view_layer.update()
        pontos.append(posicao_da_mao(cam, braco))
    return pontos


def formatar(pontos):
    return "[" + ", ".join("Vector2(%.1f, %.1f)" % p for p in pontos) + "]"


def main():
    c.DETALHE = gz["DETALHE"]
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = gz["criar_materiais"]()
    c.usar_colecao("Zane")
    raiz = gz["montar"](mt)
    c.achatar_sombra("Rosto")
    gz["expressao"]("normal")
    gz["esconder_boca"]()
    cam = c.criar_camera()
    c.criar_luzes()
    parado = c.guardar_pose()
    paleta = paleta_do_zane()
    folga = max(abs(altura_crua(f) - altura_suave(f)) for f in range(360))
    print(f"[zane] pé longe do chão, no máximo: {folga * c.PX_POR_M_JOGO_2X:.1f} px")

    maos = {}
    correndo = {}
    hackeando = {}
    for vista, angulo in vistas_pedidas():
        braco = braco_da_lanterna(cam, raiz, materiais, angulo)
        print(f"[zane] {vista}: mão da lanterna = {braco}")

        quadros_correr = []
        pontos_correr = []
        for q in range(QUADROS_CORRER):
            pose_correr(parado, 360 * q / QUADROS_CORRER)
            img, ind, _ = renderizar(cam, raiz, materiais, angulo)
            quadros_correr.append(c.contorno(img, ind, materiais))
            bpy.context.view_layer.update()
            pontos_correr.append(posicao_da_mao(cam, braco))
        c.restaurar_pose(parado)
        tira = np.concatenate(c.aplicar_paleta(quadros_correr, paleta), axis=1)
        c.salvar_png(tira, os.path.join(PASTA_ZANE, f"zane_correr_{vista}.png"))
        correndo[vista] = pontos_correr
        print(f"[zane] {vista}: corrida pronta")

        quadros_hack = []
        pontos_hack = []
        for q in range(QUADROS_HACK):
            pose_hack(parado, q)
            img, ind, _ = renderizar(cam, raiz, materiais, angulo)
            quadros_hack.append(c.contorno(img, ind, materiais))
            bpy.context.view_layer.update()
            pontos_hack.append(posicao_da_mao(cam, BRACO_DE_HACK))
        c.restaurar_pose(parado)
        tira = np.concatenate(c.aplicar_paleta(quadros_hack, paleta), axis=1)
        c.salvar_png(tira, os.path.join(PASTA_ZANE, f"zane_hack_{vista}.png"))
        hackeando[vista] = pontos_hack
        print(f"[zane] {vista}: hack pronto")

        maos[vista] = {
            "imovel": medir(cam, raiz, materiais, angulo, braco, parado, lambda q: None, 1),
            "parado": medir(cam, raiz, materiais, angulo, braco, parado,
                            lambda q: c.pose_parado(parado, 360 * q / c.QUADROS_PARADO, **gz["RESPIRAR"]),
                            c.QUADROS_PARADO),
            "andar": medir(cam, raiz, materiais, angulo, braco, parado,
                           lambda q: c.pose_andar(parado, 360 * q / c.QUADROS_ANDAR, **gz["PASSO"]),
                           c.QUADROS_ANDAR),
        }
        c.restaurar_pose(parado)

    linhas = ["const MAOS := {"]
    for vista, tiras in maos.items():
        linhas.append(f'\t"{vista}": {{')
        for nome, pontos in tiras.items():
            linhas.append(f'\t\t"{nome}": {formatar(pontos)},')
        linhas.append("\t},")
    linhas.append("}")
    linhas.append("")
    linhas.append("const MAOS_CORRENDO := {")
    for vista, pontos in correndo.items():
        linhas.append(f'\t"{vista}": {formatar(pontos)},')
    linhas.append("}")
    linhas.append("")
    linhas.append("const MAOS_HACK := {")
    for vista, pontos in hackeando.items():
        linhas.append(f'\t"{vista}": {formatar(pontos)},')
    linhas.append("}")
    if len(maos) == len(c.VISTAS_JOGO):
        with open(SAIDA_TABELA, "w", encoding="utf-8", newline="\n") as arq:
            arq.write("\n".join(linhas) + "\n")
        print("[zane] tabela de mãos gravada")
    else:
        print("[zane] só algumas vistas: a tabela de mãos não foi gravada")
    print("[zane] pronto")


main()
