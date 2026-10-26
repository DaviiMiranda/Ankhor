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
#   robos_referencia.png            todos os robôs de frente, 3/4, lado e costas
#   assets/modelagem/personagens/<robo>.blend
#
# <robo> = sentinela, rastreador, ronda, enxame ou cacador;
# <vista> = lado, frente ou costas.
#
# Por que uma tira só dos olhos? O labirinto é quase todo escuro: no Godot,
# o corpo do robô recebe a luz da cena (fica quase preto no escuro), mas os
# olhos são desenhados por cima SEM luz (material "unshaded"). É isso que
# faz o jogador ver dois pontos vermelhos se mexendo no escuro antes de ver
# o robô. Para separar os olhos não precisamos de outro render: o passe de
# ID já diz qual material está em cada pixel (comum.renderizar_vista
# devolve esse índice), então basta copiar os pixels do material "olho".
#
# Os dois tipos (docs/historia/personagens/robos.md):
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
#   RONDA — 1,7 m, atarracado, carcaça de plástico bege encardido (o bege
#   dos computadores dos anos 80, a obsessão do Carlos). A cabeça é um
#   monitor de tubo: a tela escura mostra dois olhos, e em cima gira uma
#   sirene. Carrega um cassetete. É o robô da PATRULHA PROGRAMADA: marcha
#   duro, sempre pela mesma rota, e bipa antes de virar.
#
#   ENXAME — unidade pequena (0,55 m), um carrapato de metal com seis patas
#   finas, dois olhos e pinças. Sozinha não assusta; o perigo é andar em
#   grupo. Anda em TRIPÉ: três patas no chão (frente e trás de um lado, a
#   do meio do outro) enquanto as outras três avançam, como um inseto.
#
#   CAÇADOR — o PERSEGUIDOR PERSISTENTE. Pesado, curvado como um gorila,
#   anda apoiado nos punhos: braços compridos e grossos na frente, pernas
#   curtas atrás. A cabeça fica baixa, entre os ombros, com um visor de
#   dois olhos; nas costas, dois escapamentos. Anda como quadrúpede, com
#   braço e perna opostos juntos.
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
# para a frente; o Rastreador é baixo e comprido; a Ronda é da altura de
# uma pessoa; o Enxame é pequeno; o Caçador é largo e comprido.
QUADRO = {"sentinela": (72, 72), "rastreador": (64, 40), "ronda": (56, 56),
          "enxame": (40, 24), "cacador": (64, 48)}
QUADRO_REF = {"sentinela": (150, 170), "rastreador": (150, 90), "ronda": (150, 150),
              "enxame": (110, 60), "cacador": (150, 120)}


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


def girar_x(parado, nome, graus_x):
    """Soma 'graus_x' à rotação em X que a junta tinha parada."""
    rot, _ = parado[nome]
    bpy.data.objects[nome].rotation_euler = (rot[0] + math.radians(graus_x), rot[1], rot[2])


# ---------------------------------------------------------------------------
# Ronda (patrulha programada)
# ---------------------------------------------------------------------------

def materiais_ronda():
    m = c.Materiais()
    return m, {
        # Plástico bege de computador antigo, encardido: destoa do cinza dos
        # outros robôs e conta que foi o Carlos (anos 80) que montou.
        "carcaca": m.novo("carcaca", "#9a8e74", aspereza=0.7),
        "metal": m.novo("metal", "#555b63", aspereza=0.5),
        "metal_escuro": m.novo("metal_escuro", "#30343a", aspereza=0.6),
        "cabo": m.novo("cabo", "#24252a"),
        "tela": m.novo("tela", "#0f1712", "plano"),
        "botao": m.novo("botao", "#c79a34", "plano"),
        # A sirene usa o mesmo material dos olhos: entra na tira dos olhos e
        # aparece no escuro, girando em cima da cabeça.
        "olho": m.novo("olho", "#ff3d2e", "brilho"),
    }


def perna_ronda(nome, lado, mt, quadril):
    """Perna curta e grossa. Coxa 0,31 + canela 0,30 + pé: o quadril fica
    a 0,66 m do chão."""
    junta = c.pivo(f"{nome}Quadril", (0.12 * lado, 0, 0), quadril)
    c.membro(f"{nome}Coxa", 0.075, 0.065, 0.31, mt["metal_escuro"], junta)
    joelho = c.pivo(f"{nome}Joelho", (0, 0, -0.31), junta)
    c.caixa(f"{nome}Joelheira", (0.13, 0.08, 0.12), (0, -0.05, 0), mt["carcaca"], joelho, bisel=0.015)
    c.membro(f"{nome}Canela", 0.07, 0.06, 0.30, mt["metal"], joelho)
    tornozelo = c.pivo(f"{nome}Tornozelo", (0, 0, -0.30), joelho)
    c.caixa(f"{nome}Pe", (0.15, 0.24, 0.07), (0, -0.04, -0.015), mt["carcaca"], tornozelo, bisel=0.015)


def braco_ronda(nome, lado, mt, tronco, cassetete):
    ombro = c.pivo(f"{nome}Ombro", (0.30 * lado, 0, 0.50), tronco, (-4, 0, 0))
    c.esfera(f"{nome}Ombreira", 0.09, (0, 0, 0), mt["carcaca"], ombro, escala=(1.1, 1.0, 0.9))
    c.membro(f"{nome}Braco", 0.05, 0.045, 0.26, mt["metal"], ombro)
    cotovelo = c.pivo(f"{nome}Cotovelo", (0, 0, -0.26), ombro, (-20, 0, 0))
    c.membro(f"{nome}Antebraco", 0.065, 0.055, 0.24, mt["carcaca"], cotovelo)
    pulso = c.pivo(f"{nome}Pulso", (0, 0, -0.24), cotovelo)
    c.caixa(f"{nome}Mao", (0.08, 0.09, 0.08), (0, 0, -0.04), mt["metal_escuro"], pulso)
    if cassetete:
        # Girado 120° em X, o cilindro aponta para baixo e para a frente.
        c.cone(f"{nome}Cassetete", 0.022, 0.022, 0.42, (0, -0.14, -0.12), mt["cabo"], pulso, (120, 0, 0), lados=6)


def montar_ronda(mt):
    raiz = c.pivo("Ronda")
    quadril = c.pivo("Quadril", (0, 0, 0.66), raiz)
    perna_ronda("PernaDir", -1, mt, quadril)
    perna_ronda("PernaEsq", +1, mt, quadril)

    tronco = c.pivo("Tronco", (0, 0, 0), quadril, (4, 0, 0))
    c.caixa("Bacia", (0.32, 0.22, 0.12), (0, 0, 0.02), mt["metal_escuro"], tronco, bisel=0.02)
    c.cone("Cintura", 0.10, 0.12, 0.14, (0, 0, 0.12), mt["cabo"], tronco, lados=6)
    c.caixa("Peito", (0.50, 0.32, 0.40), (0, 0, 0.38), mt["carcaca"], tronco, bisel=0.03)
    # Painel no peito: quatro botões amarelos e uma grade de ventilação.
    c.caixa("Painel", (0.30, 0.02, 0.15), (0, -0.165, 0.40), mt["metal_escuro"], tronco)
    for i, x in enumerate((-0.09, -0.03, 0.03, 0.09)):
        c.caixa(f"Botao{i}", (0.035, 0.02, 0.035), (x, -0.178, 0.43), mt["botao"], tronco)
    for i, z in enumerate((0.30, 0.34)):
        c.caixa(f"Grade{i}", (0.26, 0.02, 0.015), (0, -0.172, z), mt["cabo"], tronco)
    # Nas costas, a bateria.
    c.caixa("Bateria", (0.36, 0.14, 0.30), (0, 0.22, 0.40), mt["metal"], tronco, bisel=0.02)
    braco_ronda("BracoDir", -1, mt, tronco, True)
    braco_ronda("BracoEsq", +1, mt, tronco, False)

    pescoco = c.pivo("Pescoco", (0, 0, 0.58), tronco, (-4, 0, 0))
    c.cone("PescocoCabo", 0.06, 0.06, 0.08, (0, 0, 0.04), mt["cabo"], pescoco, lados=6)
    cabeca = c.pivo("Cabeca", (0, 0, 0.08), pescoco)
    # Monitor de tubo: a caixa da frente e, atrás, o tubo que afina (um
    # tronco de cone deitado: girado -90° em X, a base larga fica na frente).
    c.caixa("Monitor", (0.38, 0.30, 0.28), (0, -0.02, 0.14), mt["carcaca"], cabeca, bisel=0.025)
    c.cone("Tubo", 0.13, 0.07, 0.16, (0, 0.18, 0.14), mt["carcaca"], cabeca, (-90, 0, 0), lados=8)
    c.caixa("Tela", (0.30, 0.02, 0.21), (0, -0.17, 0.14), mt["tela"], cabeca)
    for lado in (-1, 1):
        c.caixa(f"Olho{lado}", (0.07, 0.02, 0.05), (0.075 * lado, -0.182, 0.16), mt["olho"], cabeca)
    c.cone("SireneBase", 0.05, 0.05, 0.03, (0, 0, 0.295), mt["metal_escuro"], cabeca, lados=8)
    c.cone("Sirene", 0.045, 0.035, 0.06, (0, 0, 0.34), mt["olho"], cabeca, lados=8)
    c.cone("Antena", 0.016, 0.010, 0.30, (0.14, 0.08, 0.42), mt["cabo"], cabeca, (0, 10, 0), lados=4)
    return raiz


def pose_andar_ronda(parado, fase):
    """Marcha dura: passo curto, braço oposto à perna (o braço direito vai
    junto com a perna esquerda) e a cabeça parada, sem balanço nenhum. A
    falta de balanço é o que faz parecer uma máquina cumprindo ordem."""
    for perna, desloc in (("PernaDir", 0), ("PernaEsq", 180)):
        phi = math.radians(fase + desloc)
        coxa = -18 * math.sin(phi)
        joelho = 32 * max(0.0, math.cos(phi)) ** 1.5
        girar_x(parado, f"{perna}Quadril", coxa)
        girar_x(parado, f"{perna}Joelho", joelho)
        girar_x(parado, f"{perna}Tornozelo", -coxa - joelho)
    for braco, desloc in (("BracoDir", 0), ("BracoEsq", 180)):
        phi = math.radians(fase + desloc)
        girar_x(parado, f"{braco}Ombro", 14 * math.sin(phi))
    _, pos = parado["Quadril"]
    descida = 0.03 * math.sin(math.radians(fase)) ** 2
    bpy.data.objects["Quadril"].location = (pos[0], pos[1], pos[2] - descida)


# ---------------------------------------------------------------------------
# Enxame (unidades em grupo)
# ---------------------------------------------------------------------------

def materiais_enxame():
    m = c.Materiais()
    return m, {
        "carapaca": m.novo("carapaca", "#46504a", aspereza=0.45),
        "metal_escuro": m.novo("metal_escuro", "#2c3033", aspereza=0.6),
        "ferrugem": m.novo("ferrugem", "#7a4a32"),
        "cabo": m.novo("cabo", "#202226"),
        "olho": m.novo("olho", "#ff4532", "brilho"),
    }


# As seis patas: (nome, lado, posição de frente para trás). lado = +1 para
# o lado +X e -1 para o -X; posição = -1 na frente, 0 no meio, +1 atrás.
PATAS_ENXAME = (("PataE1", 1, -1), ("PataE2", 1, 0), ("PataE3", 1, 1),
                ("PataD1", -1, -1), ("PataD2", -1, 0), ("PataD3", -1, 1))
# Os dois tripés: cada um tem a pata da frente e a de trás de um lado e a
# do meio do outro. Um tripé apoia enquanto o outro avança.
TRIPE_A = ("PataE1", "PataD2", "PataE3")


def giro_pata_enxame(lado, posicao):
    """Para onde a pata aponta, em graus em torno de Z. A pata é montada
    apontando para +X; girar φ leva (1, 0) a (cos φ, sen φ). No lado +X,
    -40° inclina a pata da frente para -Y (a frente); no lado -X a conta é
    espelhada: 180° menos o mesmo ângulo."""
    if lado > 0:
        return 40 * posicao
    return 180 - 40 * posicao


def pata_enxame(nome, lado, posicao, mt, corpo):
    """Pata de inseto: o fêmur sobe para fora (girado -120° em Y, aponta
    para +X e para cima) e a tíbia desce até o chão (100° de volta: fica a
    -20° da vertical, abrindo um pouco para fora)."""
    base = c.pivo(f"{nome}Base", (0.12 * lado, 0.11 * posicao, -0.02), corpo,
                  (0, 0, giro_pata_enxame(lado, posicao)))
    femur = c.pivo(f"{nome}Femur", (0, 0, 0), base, (0, -120, 0))
    c.esfera(f"{nome}Junta", 0.035, (0, 0, 0), mt["ferrugem"], femur, seg=6, aneis=4)
    c.membro(f"{nome}Coxa", 0.025, 0.02, 0.20, mt["metal_escuro"], femur, lados=4)
    joelho = c.pivo(f"{nome}Joelho", (0, 0, -0.20), femur, (0, 100, 0))
    c.membro(f"{nome}Canela", 0.02, 0.006, 0.40, mt["cabo"], joelho, lados=4)


def montar_enxame(mt):
    raiz = c.pivo("Enxame")
    corpo = c.pivo("Corpo", (0, 0, 0.30), raiz)
    c.esfera("Carapaca", 0.20, (0, 0.02, 0.03), mt["carapaca"], corpo, escala=(0.9, 1.15, 0.55), seg=10, aneis=6)
    c.caixa("Ventre", (0.22, 0.30, 0.08), (0, 0.02, -0.06), mt["metal_escuro"], corpo, bisel=0.015)
    c.caixa("Espinha", (0.04, 0.30, 0.03), (0, 0.03, 0.13), mt["ferrugem"], corpo)
    c.cone("Antena", 0.008, 0.003, 0.20, (0, 0.18, 0.18), mt["cabo"], corpo, (-30, 0, 0), lados=4)
    for nome, lado, posicao in PATAS_ENXAME:
        pata_enxame(nome, lado, posicao, mt, corpo)

    cabeca = c.pivo("Cabeca", (0, -0.22, 0.0), corpo)
    c.esfera("Cranio", 0.09, (0, 0, 0), mt["metal_escuro"], cabeca, escala=(1.1, 0.9, 0.8), seg=8, aneis=5)
    for lado in (-1, 1):
        c.esfera(f"Olho{lado}", 0.032, (0.045 * lado, -0.07, 0.02), mt["olho"], cabeca, seg=6, aneis=4)
        # Pinças: girado 100° em X, o cone aponta para a frente e um pouco
        # para baixo, com a ponta fina na frente.
        c.cone(f"Pinca{lado}", 0.02, 0.0, 0.10, (0.04 * lado, -0.10, -0.05), mt["ferrugem"], cabeca,
               (100, 0, -15 * lado), lados=4)
    return raiz


def pose_andar_enxame(parado, fase):
    """Marcha em tripé. Cada pata faz um ciclo: avança (gira em Z para a
    frente) com o fêmur levantado e volta com ele no chão, empurrando o
    corpo. O avanço é 14°·sen(φ); a pata está subindo enquanto a derivada
    cos(φ) é positiva, então o levantamento é 14°·max(0, cos φ). Os dois
    tripés estão meio ciclo defasados. O corpo sobe duas vezes por ciclo,
    uma a cada troca de tripé."""
    for nome, lado, _ in PATAS_ENXAME:
        phi = math.radians(fase + (0 if nome in TRIPE_A else 180))
        rot, _ = parado[f"{nome}Base"]
        avanco = math.radians(14 * math.sin(phi))
        bpy.data.objects[f"{nome}Base"].rotation_euler = (rot[0], rot[1], rot[2] - lado * avanco)
        rot, _ = parado[f"{nome}Femur"]
        levanta = math.radians(14 * max(0.0, math.cos(phi)))
        bpy.data.objects[f"{nome}Femur"].rotation_euler = (rot[0], rot[1] - levanta, rot[2])
    _, pos = parado["Corpo"]
    subida = 0.012 * abs(math.sin(math.radians(fase)))
    bpy.data.objects["Corpo"].location = (pos[0], pos[1], pos[2] + subida)


# ---------------------------------------------------------------------------
# Caçador (perseguidor persistente)
# ---------------------------------------------------------------------------

INCLINACAO_CACADOR = 55   # graus que o tronco se inclina para a frente


def materiais_cacador():
    m = c.Materiais()
    return m, {
        "metal": m.novo("metal", "#4c525a", aspereza=0.5),
        "metal_escuro": m.novo("metal_escuro", "#2b2e34", aspereza=0.6),
        "bronze": m.novo("bronze", "#6a4c33"),
        "cabo": m.novo("cabo", "#232429"),
        "lente": m.novo("lente", "#140d10", "plano"),
        "olho": m.novo("olho", "#ff3a2c", "brilho"),
    }


def perna_cacador(nome, lado, mt, corpo):
    """Perna traseira curta. Coxa para a frente (-20°), canela para trás
    (+25° no mundo) e o pé reto: 0,34·cos 20° + 0,36·cos 25° + pé ≈ 0,70 m,
    a altura do quadril."""
    junta = c.pivo(f"{nome}Quadril", (0.17 * lado, 0.04, 0), corpo, (-20, 0, 0))
    c.esfera(f"{nome}Junta", 0.08, (0, 0, 0), mt["bronze"], junta)
    c.membro(f"{nome}Coxa", 0.085, 0.06, 0.34, mt["metal"], junta)
    joelho = c.pivo(f"{nome}Joelho", (0, 0, -0.34), junta, (45, 0, 0))
    c.membro(f"{nome}Canela", 0.06, 0.045, 0.36, mt["metal_escuro"], joelho)
    tornozelo = c.pivo(f"{nome}Tornozelo", (0, 0, -0.36), joelho, (-25, 0, 0))
    c.caixa(f"{nome}Pe", (0.13, 0.24, 0.07), (0, -0.05, -0.02), mt["metal_escuro"], tornozelo, bisel=0.015)


def braco_cacador(nome, lado, mt, tronco):
    """Braço da frente, que serve de pata. O ombro desfaz a inclinação do
    tronco (-55°) e ainda joga o braço 8° para a frente. Ombro a ~1 m do
    chão; braço 0,48 + antebraço 0,42 + punho alcançam o chão."""
    ombro = c.pivo(f"{nome}Ombro", (0.34 * lado, 0, 0.52), tronco, (-INCLINACAO_CACADOR - 8, 0, 0))
    c.esfera(f"{nome}Junta", 0.11, (0, 0, 0), mt["bronze"], ombro)
    c.membro(f"{nome}Braco", 0.085, 0.07, 0.48, mt["metal"], ombro)
    cotovelo = c.pivo(f"{nome}Cotovelo", (0, 0, -0.48), ombro, (14, 0, 0))
    c.esfera(f"{nome}Cotoveleira", 0.07, (0, 0, 0), mt["metal_escuro"], cotovelo)
    c.membro(f"{nome}Antebraco", 0.09, 0.075, 0.42, mt["metal_escuro"], cotovelo)
    pulso = c.pivo(f"{nome}Pulso", (0, 0, -0.42), cotovelo, (-6, 0, 0))
    c.caixa(f"{nome}Punho", (0.16, 0.18, 0.12), (0, -0.02, -0.06), mt["metal"], pulso, bisel=0.02)
    for i, x in enumerate((-0.05, 0.0, 0.05)):
        c.caixa(f"{nome}Dedo{i}", (0.04, 0.05, 0.06), (x, -0.12, -0.08), mt["bronze"], pulso)


def montar_cacador(mt):
    raiz = c.pivo("Cacador")
    corpo = c.pivo("Corpo", (0, 0.18, 0.70), raiz)
    perna_cacador("PernaDir", -1, mt, corpo)
    perna_cacador("PernaEsq", +1, mt, corpo)
    c.caixa("Bacia", (0.38, 0.24, 0.16), (0, 0.02, 0.0), mt["metal_escuro"], corpo, bisel=0.02)

    tronco = c.pivo("Tronco", (0, 0, 0.04), corpo, (INCLINACAO_CACADOR, 0, 0))
    c.cone("Coluna", 0.08, 0.10, 0.26, (0, 0.02, 0.15), mt["cabo"], tronco, lados=6)
    c.caixa("Peito", (0.60, 0.40, 0.34), (0, 0, 0.44), mt["metal"], tronco, bisel=0.035)
    c.caixa("Couraca", (0.46, 0.04, 0.24), (0, -0.21, 0.44), mt["bronze"], tronco)
    # Escapamentos nas costas. O +Y do tronco aponta para cima e para trás;
    # girando -(55 + 10)° em X o cano fica quase em pé no mundo (-10°).
    for i, x in enumerate((-0.14, 0.14)):
        c.cone(f"Escape{i}", 0.05, 0.04, 0.26, (x, 0.22, 0.52), mt["metal_escuro"], tronco,
               (-INCLINACAO_CACADOR - 10, 0, 0), lados=6)
    braco_cacador("BracoDir", -1, mt, tronco)
    braco_cacador("BracoEsq", +1, mt, tronco)

    # Cabeça baixa, na frente do peito e entre os ombros; o pivô desfaz a
    # inclinação para ela olhar reto para a frente.
    cabeca = c.pivo("Cabeca", (0, -0.24, 0.50), tronco, (-INCLINACAO_CACADOR + 5, 0, 0))
    c.caixa("Cranio", (0.24, 0.26, 0.19), (0, -0.04, 0.0), mt["metal_escuro"], cabeca, bisel=0.02)
    c.caixa("Visor", (0.20, 0.03, 0.06), (0, -0.175, 0.02), mt["lente"], cabeca)
    for lado in (-1, 1):
        c.caixa(f"Olho{lado}", (0.05, 0.02, 0.035), (0.055 * lado, -0.19, 0.02), mt["olho"], cabeca)
    c.caixa("Mandibula", (0.20, 0.16, 0.06), (0, -0.08, -0.11), mt["metal"], cabeca, (10, 0, 0))
    return raiz


def pose_andar_cacador(parado, fase):
    """Andar de gorila: braço e perna OPOSTOS se movem juntos (braço
    esquerdo com perna direita). O punho levanta dobrando o cotovelo
    enquanto avança. O tronco balança para os lados (giro em Y) uma vez
    por ciclo: o peso passa de um braço para o outro."""
    for perna, desloc in (("PernaDir", 0), ("PernaEsq", 180)):
        phi = math.radians(fase + desloc)
        coxa = -20 * math.sin(phi)
        joelho = 30 * max(0.0, math.cos(phi))
        girar_x(parado, f"{perna}Quadril", coxa)
        girar_x(parado, f"{perna}Joelho", joelho)
        girar_x(parado, f"{perna}Tornozelo", -coxa - joelho)
    for braco, desloc in (("BracoEsq", 0), ("BracoDir", 180)):
        phi = math.radians(fase + desloc)
        girar_x(parado, f"{braco}Ombro", -16 * math.sin(phi))
        girar_x(parado, f"{braco}Cotovelo", 18 * max(0.0, math.cos(phi)))
    _, pos = parado["Corpo"]
    subida = 0.025 * abs(math.sin(math.radians(fase)))
    bpy.data.objects["Corpo"].location = (pos[0], pos[1], pos[2] + subida)
    rot, _ = parado["Tronco"]
    bpy.data.objects["Tronco"].rotation_euler = (rot[0], rot[1] + math.radians(4 * math.sin(math.radians(fase))), rot[2])


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


ROBOS = (
    ("sentinela", materiais_sentinela, montar_sentinela, pose_andar_sentinela),
    ("rastreador", materiais_rastreador, montar_rastreador, pose_andar_rastreador),
    ("ronda", materiais_ronda, montar_ronda, pose_andar_ronda),
    ("enxame", materiais_enxame, montar_enxame, pose_andar_enxame),
    ("cacador", materiais_cacador, montar_cacador, pose_andar_cacador),
)


def main():
    """Sem argumentos, gera todos os robôs e a folha de referência. Para
    gerar só alguns (mais rápido, sem refazer a folha), passe os nomes
    depois de '--':  blender -b ... --python gerar_robos.py -- ronda enxame"""
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    pedidos = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    referencias = []
    for nome, materiais, montar, pose in ROBOS:
        if pedidos and nome not in pedidos:
            continue
        referencias.append(renderizar_robo(nome, materiais, montar, pose))
    if not pedidos:
        folha = c.montar_folha(referencias)
        c.salvar_png(folha, os.path.join(PASTA_SAIDA, "robos_referencia.png"))
    print("[robos] pronto")


main()
