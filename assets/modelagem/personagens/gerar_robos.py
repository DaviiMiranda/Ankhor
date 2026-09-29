# gerar_robos.py — modela os dois tipos de ROBÔ no Blender, por código, e
# renderiza as tiras de caminhada (lado, frente e costas) e uma folha de
# referência. Mesmo pipeline do Gabriel (comum.py): dois passes (luz e ID),
# rampas de 4 tons, contorno seletivo e paleta fixa.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_robos.py
#
# O que sai (em assets/sprites/personagens/robos/):
#   <robo>_andar_<vista>.png        caminhada: 8 quadros lado a lado
#   <robo>_andar_<vista>_olhos.png  os mesmos quadros, só com os pixels dos
#                                   olhos (o resto transparente)
#   robos_referencia.png            os dois robôs de frente, 3/4, lado e costas
#   assets/modelagem/personagens/sentinela.blend e rastreador.blend
#
# <robo> = sentinela ou rastreador; <vista> = lado, frente ou costas.
#
# Por que uma tira só dos olhos? O labirinto é quase todo escuro: no Godot,
# o corpo do robô recebe a luz da cena (fica quase preto no escuro), mas os
# olhos são desenhados por cima SEM luz (material "unshaded"). É isso que
# faz o jogador ver dois pontos vermelhos se mexendo no escuro antes de ver
# o robô. Para separar os olhos não precisamos de outro render: o passe de
# ID já diz qual material está em cada pixel (comum.renderizar_vista
# devolve esse índice), então basta copiar os pixels do material "olho".
#
# Os dois tipos (docs/personagens/robos.md):
#
#   SENTINELA — 2,1 m, alta, magra e curvada para a frente, braços longos
#   que quase arrastam no chão, garras de três dedos. A cabeça é um globo
#   com UM olho grande: a lente é o sensor óptico (o ponto fraco que o
#   Baltazar desenhou no diário). Anda devagar e enxerga longe, num cone.
#
#   RASTREADOR — quadrúpede baixo (0,8 m), comprido, como um cão feito de
#   placas e cabos. Três olhos pequenos, espinhos nas costas e duas antenas
#   parabólicas no lugar das orelhas: é o robô que OUVE. Rápido, enxerga
#   pouco. Anda num trote: patas em diagonal se movem juntas.
#
# O que dá medo aqui é a silhueta: proporções erradas para uma pessoa
# (braços compridos demais, cabeça para a frente do corpo) e um bicho que
# parece cachorro mas tem antena no lugar da orelha.

import math
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as c  # noqa: E402
import numpy as np  # noqa: E402
import bpy  # noqa: E402

PASTA_SAIDA = os.path.join(c.PASTA_SPRITES, "robos")
VISTAS = (("lado", 90), ("frente", 0), ("costas", 180))
QUADROS_ANDAR = 8
MAX_CORES = 24

# Quadros (largura, altura) em px. A Sentinela passa dos 2 m e se inclina
# para a frente; o Rastreador é baixo e comprido.
QUADRO = {"sentinela": (72, 72), "rastreador": (64, 40)}
QUADRO_REF = {"sentinela": (150, 170), "rastreador": (150, 90)}


# ---------------------------------------------------------------------------
# Sentinela
# ---------------------------------------------------------------------------

def materiais_sentinela():
    m = c.Materiais()
    return m, {
        "metal": m.novo("metal", "#5b626b", aspereza=0.5),
        "metal_escuro": m.novo("metal_escuro", "#353940", aspereza=0.6),
        "ferrugem": m.novo("ferrugem", "#7b5037"),
        "cabo": m.novo("cabo", "#26272d"),
        "lente": m.novo("lente", "#150d11", "plano"),
        "olho": m.novo("olho", "#ff4032", "brilho"),
    }


def perna_sentinela(nome, lado, mt, quadril):
    junta = c.pivo(f"{nome}Quadril", (0.13 * lado, 0, 0), quadril, (-6, 0, 0))
    c.membro(f"{nome}Coxa", 0.075, 0.055, 0.55, mt["metal_escuro"], junta)
    joelho = c.pivo(f"{nome}Joelho", (0, 0, -0.55), junta, (14, 0, 0))
    c.esfera(f"{nome}Rotula", 0.07, (0, 0, 0), mt["ferrugem"], joelho)
    c.membro(f"{nome}Canela", 0.055, 0.04, 0.57, mt["metal"], joelho)
    tornozelo = c.pivo(f"{nome}Tornozelo", (0, 0, -0.57), joelho, (-8, 0, 0))
    c.caixa(f"{nome}Pe", (0.12, 0.30, 0.05), (0, -0.07, -0.02), mt["metal_escuro"], tornozelo)
    for i, x in enumerate((-0.04, 0.0, 0.04)):
        c.caixa(f"{nome}Unha{i}", (0.02, 0.08, 0.03), (x, -0.25, -0.03), mt["ferrugem"], tornozelo, (15, 0, 0))


def braco_sentinela(nome, lado, mt, tronco):
    # O tronco está inclinado 32° para a frente; o ombro desfaz parte disso
    # para o braço pender quase na vertical, à frente do corpo.
    ombro = c.pivo(f"{nome}Ombro", (0.30 * lado, 0, 0.55), tronco, (-24, 8 * lado, 0))
    c.esfera(f"{nome}Junta", 0.08, (0, 0, 0), mt["ferrugem"], ombro)
    c.membro(f"{nome}Braco", 0.055, 0.045, 0.55, mt["metal"], ombro)
    cotovelo = c.pivo(f"{nome}Cotovelo", (0, 0, -0.55), ombro, (-12, 0, 0))
    c.membro(f"{nome}Antebraco", 0.045, 0.035, 0.58, mt["metal_escuro"], cotovelo)
    pulso = c.pivo(f"{nome}Pulso", (0, 0, -0.58), cotovelo, (0, 0, 0))
    c.caixa(f"{nome}Mao", (0.08, 0.06, 0.08), (0, 0, -0.03), mt["metal"], pulso)
    # Três dedos finos e compridos, levemente abertos: garras.
    for i, (x, giro) in enumerate(((-0.03, -10), (0.0, 0), (0.03, 10))):
        dedo = c.pivo(f"{nome}Dedo{i}", (x, 0, -0.07), pulso, (-12, giro, 0))
        c.membro(f"{nome}Garra{i}", 0.014, 0.006, 0.22, mt["cabo"], dedo, lados=4)


def montar_sentinela(mt):
    raiz = c.pivo("Sentinela")
    quadril = c.pivo("Quadril", (0, 0, 1.13), raiz)
    perna_sentinela("PernaDir", -1, mt, quadril)
    perna_sentinela("PernaEsq", +1, mt, quadril)

    tronco = c.pivo("Tronco", (0, 0, 0), quadril, (32, 0, 0))
    c.caixa("Bacia", (0.32, 0.18, 0.14), (0, 0, 0.0), mt["metal_escuro"], tronco, bisel=0.02)
    c.cone("Coluna", 0.05, 0.05, 0.25, (0, 0.03, 0.18), mt["cabo"], tronco, lados=6)
    # Caixa torácica: um tronco de cone oco por dentro não aparece em 2 m;
    # o que se lê são as "costelas" (faixas de ferrugem) sobre o metal.
    c.cone("Torax", 0.19, 0.30, 0.42, (0, 0, 0.50), mt["metal"], tronco, lados=8, achatar=0.62)
    for i, z in enumerate((0.38, 0.48, 0.58)):
        c.cone(f"Costela{i}", 0.25 + 0.06 * i, 0.25 + 0.06 * i, 0.03, (0, -0.01, z), mt["ferrugem"],
               tronco, lados=8, achatar=0.64)
    # Nas costas, o gerador: uma caixa com aletas.
    c.caixa("Gerador", (0.30, 0.16, 0.30), (0, 0.20, 0.52), mt["metal_escuro"], tronco, bisel=0.02)
    for i, z in enumerate((0.42, 0.50, 0.58)):
        c.caixa(f"Aleta{i}", (0.32, 0.03, 0.02), (0, 0.29, z), mt["cabo"], tronco)
    braco_sentinela("BracoDir", -1, mt, tronco)
    braco_sentinela("BracoEsq", +1, mt, tronco)

    # Pescoço de cabos, esticado para a frente; a cabeça volta a olhar reto.
    pescoco = c.pivo("Pescoco", (0, -0.02, 0.72), tronco, (22, 0, 0))
    c.membro("PescocoCabo", 0.045, 0.045, 0.20, mt["cabo"], pescoco)
    pescoco.rotation_euler[0] += math.radians(180)
    cabeca = c.pivo("Cabeca", (0, 0, -0.24), pescoco, (180 - 60, 0, 0))
    c.esfera("Cranio", 0.17, (0, 0, 0), mt["metal"], cabeca, escala=(1.0, 1.05, 0.92), seg=10, aneis=6)
    c.caixa("Queixo", (0.16, 0.10, 0.06), (0, -0.07, -0.13), mt["metal_escuro"], cabeca)
    # O olho: aro, lente escura e a pupila que brilha.
    c.cone("Aro", 0.105, 0.105, 0.05, (0, -0.15, 0.01), mt["ferrugem"], cabeca, (90, 0, 0), lados=10)
    c.cone("Lente", 0.085, 0.085, 0.05, (0, -0.17, 0.01), mt["lente"], cabeca, (90, 0, 0), lados=10)
    c.cone("Olho", 0.042, 0.042, 0.04, (0, -0.19, 0.01), mt["olho"], cabeca, (90, 0, 0), lados=8)
    for lado in (-1, 1):
        c.cone(f"Antena{lado}", 0.012, 0.006, 0.22, (0.09 * lado, 0.05, 0.22), mt["cabo"], cabeca,
               (-20, 18 * lado, 0), lados=4)
    return raiz


def pose_andar_sentinela(parado, fase):
    """Passo lento e pesado. As pernas seguem a onda seno (como no Gabriel),
    os braços balançam pouco e ATRASADOS (são pesados e soltos) e a cabeça
    fica quase parada: é isso que dá o ar de máquina que mira."""
    def girar(nome, graus_x):
        rot, _ = parado[nome]
        bpy.data.objects[nome].rotation_euler = (rot[0] + math.radians(graus_x), rot[1], rot[2])

    for perna, desloc in (("PernaDir", 0), ("PernaEsq", 180)):
        phi = math.radians(fase + desloc)
        coxa = -18 * math.sin(phi)
        joelho = 38 * max(0.0, math.cos(phi)) ** 1.5
        girar(f"{perna}Quadril", coxa)
        girar(f"{perna}Joelho", joelho)
        girar(f"{perna}Tornozelo", -coxa - joelho)
    for braco, desloc in (("BracoDir", 0), ("BracoEsq", 180)):
        phi = math.radians(fase + desloc - 50)
        girar(f"{braco}Ombro", 9 * math.sin(phi))
        girar(f"{braco}Cotovelo", -6 * max(0.0, math.sin(phi)))
    _, pos = parado["Quadril"]
    descida = 0.037 * math.sin(math.radians(fase)) ** 2
    bpy.data.objects["Quadril"].location = (pos[0], pos[1], pos[2] - descida)


# ---------------------------------------------------------------------------
# Rastreador
# ---------------------------------------------------------------------------

def materiais_rastreador():
    m = c.Materiais()
    return m, {
        "metal": m.novo("metal", "#4d535c", aspereza=0.5),
        "metal_escuro": m.novo("metal_escuro", "#2d3036", aspereza=0.6),
        "placa": m.novo("placa", "#6e3a2c"),
        "cabo": m.novo("cabo", "#222328"),
        "dente": m.novo("dente", "#a8a293", "plano"),
        "olho": m.novo("olho", "#ff4a2a", "brilho"),
    }


def pata(nome, x, y, mt, corpo):
    """Pata de cão de metal: coxa, canela voltada para trás e um pé. O
    corpo fica a 0,55 m; coxa 0,30 + canela 0,30 com as dobras dá o chão."""
    junta = c.pivo(f"{nome}Ombro", (x, y, -0.02), corpo, (-18, 0, 0))
    c.esfera(f"{nome}Junta", 0.06, (0, 0, 0), mt["placa"], junta)
    c.membro(f"{nome}Coxa", 0.055, 0.04, 0.30, mt["metal"], junta)
    joelho = c.pivo(f"{nome}Joelho", (0, 0, -0.30), junta, (40, 0, 0))
    c.membro(f"{nome}Canela", 0.04, 0.03, 0.31, mt["metal_escuro"], joelho)
    pe = c.pivo(f"{nome}Pe", (0, 0, -0.31), joelho, (-22, 0, 0))
    c.caixa(f"{nome}Garra", (0.08, 0.13, 0.03), (0, -0.04, -0.01), mt["cabo"], pe)


def montar_rastreador(mt):
    raiz = c.pivo("Rastreador")
    corpo = c.pivo("Corpo", (0, 0, 0.56), raiz)
    # Corpo em três placas ao longo do eixo Y (a frente é -Y).
    c.caixa("Torax", (0.34, 0.42, 0.24), (0, -0.20, 0.02), mt["metal"], corpo, (-6, 0, 0), bisel=0.03)
    c.caixa("Cintura", (0.20, 0.20, 0.14), (0, 0.10, 0.0), mt["cabo"], corpo)
    c.caixa("Abdomen", (0.30, 0.40, 0.20), (0, 0.36, 0.02), mt["metal"], corpo, (6, 0, 0), bisel=0.03)
    for i, y in enumerate((-0.32, -0.16, 0.30, 0.44)):
        c.caixa(f"Placa{i}", (0.30, 0.10, 0.03), (0, y, 0.15), mt["placa"], corpo)
    # Espinhos nas costas: cones finos, inclinados para trás.
    for i, y in enumerate((-0.28, -0.12, 0.26, 0.40)):
        c.cone(f"Espinho{i}", 0.035, 0.0, 0.16, (0, y, 0.22), mt["metal_escuro"], corpo, (-25, 0, 0), lados=4)
    # Rabo: três gomos de cabo caindo.
    rabo = c.pivo("Rabo", (0, 0.56, 0.05), corpo, (-120, 0, 0))
    c.membro("RaboCabo", 0.03, 0.02, 0.35, mt["cabo"], rabo, lados=4)

    for nome, x, y in (("PataFE", 0.15, -0.30), ("PataFD", -0.15, -0.30),
                       ("PataTE", 0.14, 0.40), ("PataTD", -0.14, 0.40)):
        pata(nome, x, y, mt, corpo)

    # Cabeça baixa e comprida, projetada para a frente.
    pescoco = c.pivo("Pescoco", (0, -0.42, 0.02), corpo, (14, 0, 0))
    c.caixa("PescocoCabo", (0.10, 0.14, 0.10), (0, -0.05, 0), mt["cabo"], pescoco)
    cabeca = c.pivo("Cabeca", (0, -0.14, -0.02), pescoco, (-6, 0, 0))
    c.caixa("Cranio", (0.20, 0.30, 0.14), (0, -0.12, 0.03), mt["metal"], cabeca, bisel=0.02)
    c.caixa("Focinho", (0.14, 0.14, 0.08), (0, -0.32, 0.0), mt["metal_escuro"], cabeca, bisel=0.015)
    c.caixa("Mandibula", (0.14, 0.26, 0.05), (0, -0.20, -0.08), mt["metal_escuro"], cabeca, (8, 0, 0))
    for i, x in enumerate((-0.05, -0.017, 0.017, 0.05)):
        c.caixa(f"Dente{i}", (0.018, 0.02, 0.035), (x, -0.31, -0.06), mt["dente"], cabeca)
    # Três olhos pequenos, em triângulo, na frente do crânio.
    for i, (x, z) in enumerate(((-0.05, 0.06), (0.05, 0.06), (0.0, 0.03))):
        c.esfera(f"Olho{i}", 0.025, (x, -0.27, z), mt["olho"], cabeca, seg=6, aneis=4)
    # Antenas parabólicas no lugar das orelhas: é o robô que ouve.
    for lado in (-1, 1):
        haste = c.pivo(f"Haste{lado}", (0.08 * lado, -0.06, 0.09), cabeca, (-15, 0, 28 * lado))
        c.membro(f"HasteCabo{lado}", 0.012, 0.012, 0.14, mt["cabo"], haste, lados=4)
        haste.rotation_euler[0] += math.radians(180)
        c.cone(f"Parabolica{lado}", 0.075, 0.02, 0.035, (0, 0, -0.15), mt["metal_escuro"], haste,
               (0, 90 * lado, 0), lados=8)
    return raiz


def pose_andar_rastreador(parado, fase):
    """Trote: as patas em diagonal se movem juntas (frente-esquerda com
    trás-direita, e o outro par meio ciclo depois). O corpo sobe e desce
    duas vezes por ciclo, e a cabeça balança um pouco, farejando."""
    def girar(nome, graus_x):
        rot, _ = parado[nome]
        bpy.data.objects[nome].rotation_euler = (rot[0] + math.radians(graus_x), rot[1], rot[2])

    for pata, desloc in (("PataFE", 0), ("PataTD", 0), ("PataFD", 180), ("PataTE", 180)):
        phi = math.radians(fase + desloc)
        coxa = -24 * math.sin(phi)
        joelho = 30 * max(0.0, math.cos(phi))
        girar(f"{pata}Ombro", coxa)
        girar(f"{pata}Joelho", joelho)
        girar(f"{pata}Pe", -coxa - joelho)
    _, pos = parado["Corpo"]
    subida = 0.03 * abs(math.sin(math.radians(fase)))
    bpy.data.objects["Corpo"].location = (pos[0], pos[1], pos[2] + subida)
    girar("Cabeca", 5 * math.sin(math.radians(2 * fase)))


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def guardar_pose():
    return {o.name: (tuple(o.rotation_euler), tuple(o.location))
            for o in bpy.data.objects if o.type == 'EMPTY'}


def restaurar_pose(pose):
    for nome, (rot, pos) in pose.items():
        bpy.data.objects[nome].rotation_euler = rot
        bpy.data.objects[nome].location = pos


def indice_do(materiais, nome):
    return [n for n, _, _, _ in materiais.lista].index(nome)


def renderizar_robo(nome, criar_materiais, montar, pose_andar):
    """Monta um robô, renderiza as tiras de caminhada (corpo e olhos) e as
    vistas de referência. Devolve as vistas de referência já na paleta."""
    c.cena_vazia()
    materiais, mt = criar_materiais()
    c.usar_colecao(nome.capitalize())
    raiz = montar(mt)
    cam = c.criar_camera()
    c.criar_luzes()
    olho = indice_do(materiais, "olho")
    quadro = QUADRO[nome]

    parado = guardar_pose()
    corpos = {v: [] for v, _ in VISTAS}
    olhos = {v: [] for v, _ in VISTAS}
    for q in range(QUADROS_ANDAR):
        pose_andar(parado, 360 * q / QUADROS_ANDAR)
        for vista, angulo in VISTAS:
            img, ind, _ = c.renderizar_vista(cam, raiz, materiais, angulo, quadro, c.PX_POR_M_JOGO, c.PE_JOGO_PX)
            corpos[vista].append(c.contorno(img, ind, materiais))
            so_olhos = np.zeros_like(img)
            so_olhos[ind == olho] = img[ind == olho]
            olhos[vista].append(so_olhos)
        print(f"[{nome}] andar: quadro {q + 1}/{QUADROS_ANDAR}")
    restaurar_pose(parado)
    linhas = corpos["lado"][0][..., 3].any(axis=1).nonzero()[0]
    print(f"[{nome}] altura no sprite: {linhas[-1] - linhas[0] + 1} px")

    referencia = []
    for angulo in (0, 35, 90, 180):
        img, ind, _ = c.renderizar_vista(cam, raiz, materiais, angulo, QUADRO_REF[nome], c.PX_POR_M_REF, c.PE_REF_PX)
        referencia.append(c.contorno(img, ind, materiais))

    todas = [q for v in corpos.values() for q in v]
    convertidas, paleta = c.unificar_paleta(todas + referencia, materiais, MAX_CORES)
    i = 0
    for vista, _ in VISTAS:
        tira = np.concatenate(convertidas[i:i + QUADROS_ANDAR], axis=1)
        c.salvar_png(tira, os.path.join(PASTA_SAIDA, f"{nome}_andar_{vista}.png"))
        c.salvar_png(np.concatenate(olhos[vista], axis=1),
                     os.path.join(PASTA_SAIDA, f"{nome}_andar_{vista}_olhos.png"))
        i += QUADROS_ANDAR
    c.salvar_blend(os.path.join(c.PASTA_SCRIPT, f"{nome}.blend"), raiz)
    return convertidas[i:]


def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    ref_sentinela = renderizar_robo("sentinela", materiais_sentinela, montar_sentinela, pose_andar_sentinela)
    ref_rastreador = renderizar_robo("rastreador", materiais_rastreador, montar_rastreador, pose_andar_rastreador)
    folha = c.montar_folha([ref_sentinela, ref_rastreador])
    c.salvar_png(folha, os.path.join(PASTA_SAIDA, "robos_referencia.png"))
    print("[robos] pronto")


main()
