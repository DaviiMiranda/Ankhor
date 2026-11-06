# gerar_diana_sentada.py — a DIANA sentada numa cadeira de escritório, com o
# tornozelo torcido, para a Emergência do D-Tec (Enredo, Ato 4, "A chegada").
#
# Como rodar (sem abrir a janela do Blender; precisa do gerar_diana.py ao lado):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_diana_sentada.py
#
# O que sai:
#   assets/sprites/personagens/diana/diana_sentada.png
#       8 quadros de 96 x 112 lado a lado (a respiração), vista de 3/4, com a
#       cadeira no mesmo sprite (como a Clarice na estação dela).
#
# A POSE
#   A mesma de sentar da Clarice (gerar_clarice.py, sentar): quadril na
#   altura do assento (0,48 m), coxas a -88° (para a frente) e joelhos a +88°
#   (canelas para baixo). Com a perna da Diana (0,85 m do chão ao quadril), a
#   sola fica a uns 4 cm do chão: o pé encosta. A perna do tornozelo torcido
#   (a direita) vai esticada para a frente, com o joelho quase reto e o pé
#   apoiado no calcanhar. As mãos ficam no colo, a esquerda perto do joelho
#   machucado.
#
# A CADEIRA
#   A cadeira giratória da Clarice (gerar_clarice.py, montar_cadeira): cinco
#   patas, coluna de gás, assento a 0,39 m e encosto, em cinza-chumbo e metal.
#   As duas cores entram na paleta da Diana (unificar_paleta), que junta tons
#   quase iguais; o resto do corpo usa as mesmas cores dos outros sprites dela.
#
# A RESPIRAÇÃO
#   comum.pose_parado por cima da pose sentada: o tronco sobe 1 px ao puxar o
#   ar e a cabeça acompanha atrasada, em 8 quadros (comum.QUADROS_PARADO).

import os
import sys

sys.dont_write_bytecode = True
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA_SCRIPT)
import comum as c  # noqa: E402
import numpy as np  # noqa: E402
import bpy  # noqa: E402

ANGULO = 35                       # a vista de 3/4 dos sprites de jogo
CADEIRA_POS = (0.0, 0.22, 0.0)
ALTURA_DO_QUADRIL = 0.48


def carregar(arquivo):
    caminho = os.path.join(PASTA_SCRIPT, arquivo)
    fonte = open(caminho, encoding="utf-8").read().rsplit("\nmain()", 1)[0]
    modulo = {"__file__": caminho, "__name__": arquivo.replace(".py", "")}
    exec(compile(fonte, arquivo, "exec"), modulo)
    return modulo


def girar(nome, x=None, y=None, z=None):
    obj = bpy.data.objects[nome]
    rot = list(obj.rotation_euler)
    for i, valor in enumerate((x, y, z)):
        if valor is not None:
            rot[i] = np.radians(valor)
    obj.rotation_euler = rot


def montar_cadeira(mt):
    giro = c.pivo("Cadeira", CADEIRA_POS)
    for i in range(5):
        c.caixa(f"Pata{i}", (0.04, 0.3, 0.03), (0, 0, 0.04), mt["cadeira"], giro, (0, 0, i * 72), desloc=(0, 0.15, 0))
    c.cone("Coluna", 0.03, 0.03, 0.3, (0, 0, 0.2), mt["metal"], giro, lados=6)
    c.caixa("Assento", (0.46, 0.44, 0.08), (0, 0.0, 0.39), mt["cadeira"], giro, bisel=0.025)
    c.caixa("HasteEncosto", (0.05, 0.04, 0.3), (0, 0.24, 0.51), mt["metal"], giro)
    c.caixa("Encosto", (0.4, 0.07, 0.28), (0, 0.27, 0.72), mt["cadeira"], giro, (-6, 0, 0), bisel=0.03)
    return giro


def sentar_com_o_pe_machucado():
    bpy.data.objects["Quadril"].location = (0, 0.02, ALTURA_DO_QUADRIL)
    girar("PernaEsqQuadril", x=-88, y=6)
    girar("PernaEsqJoelho", x=88)
    girar("PernaEsqTornozelo", x=0)
    girar("PernaDirQuadril", x=-78, y=-6)
    girar("PernaDirJoelho", x=30)
    girar("PernaDirTornozelo", x=40)
    girar("Tronco", x=6)
    girar("Cabeca", x=8, z=-10)
    girar("BracoDirOmbro", x=-34, y=-8)
    girar("BracoDirCotovelo", x=-48)
    girar("BracoEsqOmbro", x=-46, y=10)
    girar("BracoEsqCotovelo", x=-40)


def main():
    g = carregar("gerar_diana.py")
    c.DETALHE = g["DETALHE"]
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = g["criar_materiais"]()
    mt["cadeira"] = materiais.novo("cadeira", "#3a3e48")
    mt["metal"] = materiais.novo("metal", "#8a919c")
    c.usar_colecao("DianaSentada")
    diana = g["montar"](mt)
    c.achatar_sombra("Rosto")
    g["expressao"](g["EXPRESSOES"][0])
    g["esconder_boca"]()
    cadeira = montar_cadeira(mt)
    cena = c.pivo("Cena")
    diana.parent = cena
    cadeira.parent = cena
    sentar_com_o_pe_machucado()
    cam = c.criar_camera()
    c.criar_luzes()
    sentada = c.guardar_pose()

    quadros = []
    for q in range(c.QUADROS_PARADO):
        c.pose_parado(sentada, 360 * q / c.QUADROS_PARADO)
        img, ind, _ = c.renderizar_vista(cam, cena, materiais, ANGULO, c.QUADRO_JOGO_2X, c.PX_POR_M_JOGO_2X, c.PE_JOGO_2X)
        quadros.append(c.contorno(img, ind, materiais))
        print(f"[diana sentada] quadro {q + 1}/{c.QUADROS_PARADO}")

    convertidas, _ = c.unificar_paleta(quadros, materiais, g["MAX_CORES"])
    saida = os.path.join(c.PASTA_SPRITES, "diana", "diana_sentada.png")
    c.salvar_png(np.concatenate(convertidas, axis=1), saida)
    print(f"[diana sentada] pronto: {saida}")


main()
