# gerar_diana.py — modela a Diana (1978) no Blender, por código, e renderiza
# os mesmos sprites do Gabriel: as cinco vistas de jogo, a caminhada e a
# respiração em cada uma e a folha de referência.
#
# ATENÇÃO: os retratos da Diana (normal, assustada, dramatica, ansiosa,
# irritada, determinada e aliviada) vêm do pixelar_retratos.py, a partir da
# folha desenhada em diana_referencia/expressoes.jpg. Este script só
# renderiza os retratos do Blender para a folha de referência e NÃO grava os
# diana_retrato_<expressão>.png.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_diana.py
#
# O que sai (em assets/sprites/personagens/diana/), com os tamanhos do Gabriel:
#   diana_<vista>.png             96 x 112 (resolução dobrada: o Godot mostra
#                                 com escala 0,5), vistas lado, frente,
#                                 tres_quartos, costas e tres_quartos_costas
#   diana_andar_<vista>.png       caminhada: 12 quadros de 96 x 112 lado a lado
#   diana_parado_<vista>.png      parada respirando: 8 quadros
#   diana_referencia.png          frente, 3/4, lado e costas, e os retratos
#                                 (os do Blender, não os do jogo)
#   assets/modelagem/personagens/diana.blend   o modelo, para abrir e mexer
#
# Quem é (docs/historia/personagens/diana.md): estudante de arquitetura e
# estagiária na obra do campus em 1978, com uns 20 anos. Dramática, ansiosa,
# impulsiva e intensa; fala rápido e exagerado. O visual segue o desenho que
# a equipe fez dela (diana_referencia/andar.jpg e expressoes.jpg):
#   - anos 70 de verdade: cabelo castanho-claro volumoso e repicado, com as
#     pontas viradas para fora, óculos grandes de armação laranja com lentes
#     alaranjadas e argolas douradas;
#   - jaqueta marrom-caramelo de gola larga, com bolsos no peito e no
#     quadril e os punhos dobrados, aberta sobre uma camiseta listrada de
#     amarelo, laranja e creme, com um cinto preto;
#   - calça jeans boca de sino e botas de plataforma marrons;
#   - postura de quem está sempre pronta para o pior: ombros um pouco
#     altos, cotovelos dobrados e um passo curto e rápido.
#
# Modelagem: só primitivas, com DETALHE 3 e sombreamento suave, como o
# Gabriel e a Clarice (ver comum.py). O esqueleto tem as mesmas juntas do
# Gabriel, então a caminhada e a respiração são as do comum.py (item 7).

import math
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as c  # noqa: E402
import bpy  # noqa: E402

MAX_CORES = 48
DETALHE = 3

# Passo curto e rápido, com o braço balançando: a ansiedade dela.
PASSO = {"coxa": 24, "joelho": 54, "braco": 20}


def criar_materiais():
    m = c.Materiais()
    return m, {
        "pele": m.novo("pele", "#dea07c"),
        "cabelo": m.novo("cabelo", "#a98458"),
        "sobrancelha": m.novo("sobrancelha", "#6e5030", "plano"),
        "jaqueta": m.novo("jaqueta", "#8a4a22"),
        "jaqueta_escura": m.novo("jaqueta_escura", "#6a3818"),
        "punho": m.novo("punho", "#a9672d"),
        "listra_amarela": m.novo("listra_amarela", "#f0b73c"),
        "listra_laranja": m.novo("listra_laranja", "#d9702a"),
        "listra_creme": m.novo("listra_creme", "#f1dfb0"),
        "jeans": m.novo("jeans", "#3f6594"),
        "cinto": m.novo("cinto", "#1d1a1c"),
        "fivela": m.novo("fivela", "#d9b64a", "plano"),
        "bota": m.novo("bota", "#5c3a24"),
        "plataforma": m.novo("plataforma", "#3a2416"),
        "aro": m.novo("aro", "#c2641c"),
        "lente": m.novo("lente", "#f0a54a", "plano"),
        "ouro": m.novo("ouro", "#e6bf4c", "plano"),
        "olho": m.novo("olho", "#2a1c18", "plano"),
        "boca": m.novo("boca", "#8a3a30", "plano"),
    }


# ---------------------------------------------------------------------------
# A Diana
# ---------------------------------------------------------------------------
#
# 1,65 m de corpo mais as plataformas e o volume do cabelo, um pouco mais
# alta que a Clarice. Os nomes das juntas são os do gerar_gabriel.py: é isso
# que deixa o comum.pose_andar e o comum.pose_parado mexerem nela.


def perna(nome, lado, mt, quadril):
    """Calça jeans boca de sino (a canela alarga até a barra) e bota de
    plataforma."""
    junta = c.pivo(f"{nome}Quadril", (0.085 * lado, 0.0, 0.0), quadril)
    c.membro(f"{nome}Coxa", 0.082, 0.07, 0.39, mt["jeans"], junta)
    joelho = c.pivo(f"{nome}Joelho", (0, 0, -0.39), junta)
    c.membro(f"{nome}Canela", 0.07, 0.118, 0.36, mt["jeans"], joelho)
    tornozelo = c.pivo(f"{nome}Tornozelo", (0, 0, -0.36), joelho)
    c.caixa(f"{nome}Bota", (0.1, 0.25, 0.1), (0, -0.045, -0.05), mt["bota"], tornozelo, bisel=0.02)
    c.caixa(f"{nome}Plataforma", (0.108, 0.27, 0.05), (0, -0.045, -0.12), mt["plataforma"], tornozelo, bisel=0.012)
    c.caixa(f"{nome}Biqueira", (0.1, 0.05, 0.07), (0, -0.16, -0.085), mt["bota"], tornozelo, bisel=0.015)


def braco(nome, lado, mt, tronco, giro_ombro, giro_cotovelo):
    """Manga da jaqueta, punho dobrado (mais claro) e a mão."""
    ombro = c.pivo(f"{nome}Ombro", (0.205 * lado, 0.0, 0.43), tronco, (giro_ombro, 5 * lado, 0))
    c.membro(f"{nome}Braco", 0.07, 0.062, 0.27, mt["jaqueta"], ombro)
    cotovelo = c.pivo(f"{nome}Cotovelo", (0, 0, -0.27), ombro, (giro_cotovelo, 0, 0))
    c.membro(f"{nome}Antebraco", 0.062, 0.055, 0.22, mt["jaqueta"], cotovelo)
    c.cone(f"{nome}Punho", 0.066, 0.066, 0.05, (0, 0, -0.2), mt["punho"], cotovelo, lados=6)
    c.caixa(f"{nome}Mao", (0.052, 0.075, 0.09), (0, 0, -0.27), mt["pele"], cotovelo, bisel=0.015)


def cabeca(mt, tronco):
    pescoco = c.pivo("Cabeca", (0, 0, 0.55), tronco)
    c.caixa("Rosto", (0.19, 0.21, 0.23), (0, 0, 0.115), mt["pele"], pescoco, bisel=0.04)
    c.caixa("Nariz", (0.03, 0.045, 0.045), (0, -0.105, 0.095), mt["pele"], pescoco)
    c.caixa("Boca", (0.05, 0.01, 0.012), (0, -0.103, 0.05), mt["boca"], pescoco)
    c.caixa("BocaAberta", (0.03, 0.01, 0.03), (0, -0.103, 0.046), mt["boca"], pescoco)
    for lado in (-1, 1):
        c.caixa(f"Olho{lado}", (0.022, 0.006, 0.026), (0.047 * lado, -0.108, 0.125), mt["olho"], pescoco)
        # Óculos grandes de armação laranja: a lente alaranjada por cima do
        # olho e o aro em volta (cima, baixo e os dois lados).
        c.caixa(f"Lente{lado}", (0.076, 0.006, 0.062), (0.05 * lado, -0.112, 0.125), mt["lente"], pescoco)
        c.caixa(f"AroCima{lado}", (0.088, 0.01, 0.012), (0.05 * lado, -0.114, 0.159), mt["aro"], pescoco)
        c.caixa(f"AroBaixo{lado}", (0.088, 0.01, 0.012), (0.05 * lado, -0.114, 0.091), mt["aro"], pescoco)
        c.caixa(f"AroLado{lado}", (0.012, 0.01, 0.07), (0.092 * lado, -0.114, 0.125), mt["aro"], pescoco)
        c.caixa(f"AroMeio{lado}", (0.012, 0.01, 0.07), (0.008 * lado, -0.114, 0.125), mt["aro"], pescoco)
        c.caixa(f"Haste{lado}", (0.01, 0.12, 0.012), (0.096 * lado, -0.05, 0.14), mt["aro"], pescoco)
        c.caixa(f"Sobrancelha{lado}", (0.05, 0.012, 0.013), (0.048 * lado, -0.108, 0.178), mt["sobrancelha"], pescoco)
        c.caixa(f"Orelha{lado}", (0.025, 0.045, 0.055), (0.097 * lado, 0.01, 0.105), mt["pele"], pescoco)
        # Argola dourada na orelha: no sprite de 48 px é um ponto de 1 px.
        c.esfera(f"Argola{lado}", 0.019, (0.108 * lado, 0.005, 0.062), mt["ouro"], pescoco, seg=6, aneis=4)
    # Cabelo castanho-claro volumoso e repicado, dos anos 70: o topo, a
    # franja repartida no meio e virada para os lados, as laterais que
    # descem até os ombros com as pontas viradas para fora e o volume nas
    # costas.
    c.caixa("CabeloTopo", (0.235, 0.265, 0.09), (0, 0.015, 0.235), mt["cabelo"], pescoco, bisel=0.035)
    for lado in (-1, 1):
        c.caixa(f"Franja{lado}", (0.11, 0.055, 0.075), (0.065 * lado, -0.095, 0.222), mt["cabelo"], pescoco,
                (14, 0, -16 * lado), bisel=0.015)
        c.esfera(f"Lateral{lado}", 0.085, (0.122 * lado, 0.03, 0.14), mt["cabelo"], pescoco,
                 escala=(0.75, 1.15, 1.5), seg=6, aneis=4)
        c.esfera(f"Meio{lado}", 0.078, (0.135 * lado, 0.04, 0.03), mt["cabelo"], pescoco,
                 escala=(0.8, 1.1, 1.3), seg=6, aneis=4)
        c.esfera(f"Ponta{lado}", 0.062, (0.15 * lado, 0.045, -0.07), mt["cabelo"], pescoco,
                 escala=(0.9, 1.0, 1.1), seg=6, aneis=4)
    c.caixa("CabeloCostas", (0.25, 0.11, 0.34), (0, 0.105, 0.06), mt["cabelo"], pescoco, bisel=0.04)
    c.esfera("CabeloNuca", 0.08, (0, 0.13, -0.08), mt["cabelo"], pescoco, escala=(1.4, 1.0, 1.0), seg=6, aneis=4)
    return pescoco


def montar(mt):
    raiz = c.pivo("Diana")
    quadril = c.pivo("Quadril", (0, 0, 0.85), raiz)
    perna("PernaDir", -1, mt, quadril)
    perna("PernaEsq", +1, mt, quadril)
    tronco = c.pivo("Tronco", (0, 0, 0), quadril)
    c.caixa("Bacia", (0.27, 0.15, 0.15), (0, 0, 0.0), mt["jeans"], tronco, bisel=0.03)
    # Cinto preto com fivela dourada, que aparece abaixo da camiseta.
    c.cone("Cinto", 0.2, 0.2, 0.04, (0, 0, 0.025), mt["cinto"], tronco, lados=8, achatar=0.6)
    c.caixa("Fivela", (0.04, 0.012, 0.03), (0, -0.126, 0.025), mt["fivela"], tronco)
    # Jaqueta marrom-caramelo, aberta na frente.
    c.cone("Jaqueta", 0.2, 0.218, 0.46, (0, 0, 0.27), mt["jaqueta"], tronco, lados=8, achatar=0.6)
    c.cone("JaquetaBarra", 0.221, 0.221, 0.05, (0, 0, 0.065), mt["jaqueta_escura"], tronco, lados=8, achatar=0.62)
    # A camiseta listrada aparece na abertura: três listras de cima para baixo.
    for i, (z, cor) in enumerate(((0.43, "listra_amarela"), (0.375, "listra_laranja"), (0.32, "listra_creme"),
                                  (0.265, "listra_amarela"), (0.21, "listra_laranja"), (0.155, "listra_creme"))):
        c.caixa(f"Listra{i}", (0.1, 0.02, 0.055), (0, -0.131, z), mt[cor], tronco)
    # Lapelas de abas largas, bolsos no peito e no quadril, e a gola alta.
    for lado in (-1, 1):
        c.caixa(f"Lapela{lado}", (0.075, 0.02, 0.3), (0.088 * lado, -0.129, 0.31), mt["jaqueta_escura"], tronco,
                (0, 0, -9 * lado), bisel=0.008)
        c.caixa(f"BolsoPeito{lado}", (0.07, 0.014, 0.06), (0.125 * lado, -0.127, 0.36), mt["jaqueta_escura"], tronco)
        c.caixa(f"BolsoQuadril{lado}", (0.09, 0.014, 0.085), (0.12 * lado, -0.126, 0.15), mt["jaqueta_escura"], tronco)
        c.caixa(f"GolaAba{lado}", (0.1, 0.04, 0.09), (0.085 * lado, -0.11, 0.5), mt["jaqueta"], tronco,
                (-12, 0, 24 * lado), bisel=0.012)
    c.caixa("Gola", (0.25, 0.14, 0.05), (0, 0.025, 0.505), mt["jaqueta"], tronco, bisel=0.02)
    c.cone("Pescoco", 0.045, 0.045, 0.1, (0, 0, 0.535), mt["pele"], tronco, lados=6)
    # Nervosa: os cotovelos ficam dobrados, as mãos perto do corpo.
    braco("BracoDir", -1, mt, tronco, 2, -22)
    braco("BracoEsq", +1, mt, tronco, 2, -18)
    cabeca(mt, tronco)
    return raiz


# ---------------------------------------------------------------------------
# Retratos do Blender (só para a folha de referência)
# ---------------------------------------------------------------------------
#   normal     boca reta;
#   assustada  boca aberta e as sobrancelhas levantadas no meio;
#   irritada   boca reta e as sobrancelhas baixas, viradas para o meio.

EXPRESSOES = ("normal", "assustada", "irritada")


def expressao(qual):
    bpy.data.objects["Boca"].hide_render = qual == "assustada"
    bpy.data.objects["BocaAberta"].hide_render = qual != "assustada"
    for lado in (-1, 1):
        sob = bpy.data.objects[f"Sobrancelha{lado}"]
        altura, giro = {"normal": (0.178, 0), "assustada": (0.188, -14 * lado),
                        "irritada": (0.172, 16 * lado)}[qual]
        sob.location.z = altura
        sob.rotation_euler = (0, math.radians(giro), 0)


def esconder_boca():
    for nome in ("Boca", "BocaAberta"):
        bpy.data.objects[nome].hide_render = True


def main():
    c.DETALHE = DETALHE
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = criar_materiais()
    c.usar_colecao("Diana")
    raiz = montar(mt)
    c.achatar_sombra("Rosto")
    c.gerar_em_pe("diana", raiz, materiais, MAX_CORES, EXPRESSOES, expressao, esconder_boca,
                  passo=PASSO, salvar_retratos=False)


main()
