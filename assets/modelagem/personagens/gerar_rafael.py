# gerar_rafael.py — modela o Rafael (2008) no Blender, por código, e
# renderiza os mesmos sprites do Gabriel: as cinco vistas de jogo, a
# caminhada e a respiração em cada uma, os retratos da caixa de diálogo e a
# folha de referência.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_rafael.py
#
# O que sai (em assets/sprites/personagens/rafael/), com os tamanhos do Gabriel:
#   rafael_<vista>.png             96 x 112 (resolução dobrada: o Godot mostra
#                                  com escala 0,5), vistas lado, frente,
#                                  tres_quartos, costas e tres_quartos_costas
#   rafael_andar_<vista>.png       caminhada: 12 quadros de 96 x 112
#   rafael_parado_<vista>.png      parado respirando: 8 quadros
#   rafael_retrato_<expressão>.png 80 x 80 (normal, rindo, triste)
#   rafael_referencia.png          frente, 3/4, lado e costas, e os retratos
#   assets/modelagem/personagens/rafael.blend   o modelo
#
# Quem é (docs/historia/personagens/rafael.md): segurança noturno da Unifor
# em 2008, no primeiro emprego, com uns 20 anos. Puxado na ronda da
# Biblioteca com o rádio e a lanterna. Caloroso, brincalhão, protetor; quer
# ser chamado de "Seu Rafael" para parecer mais velho, e jura que 3026 é
# "reforma".
#
# O visual conta isso:
#   - uniforme de vigilante de 2008: camisa de manga curta azul-celeste com
#     dragonas e bolsos azul-marinho, o emblema amarelo de SEGURANÇA na
#     manga e no boné, crachá no peito, calça azul-marinho, cinto preto e
#     coturno;
#   - o uniforme é GRANDE para ele: camisa larga, mangas compridas e folgadas
#     quase até o cotovelo, calça folgada. É um rapaz magro dentro da roupa
#     de um homem mais velho;
#   - tentando parecer mais velho: um bigodinho ralo e o boné bem
#     enterrado na cabeça;
#   - no cinto, o rádio HT (o mesmo do inventário, em gerar_interface.py:
#     plástico preto, antena de borracha) e a lanterna antiga de metal;
#   - a cor dele é o azul-celeste do uniforme: o Gabriel é vermelho, a
#     Clarice verde-azulado, o Zane amarelo-ácido;
#   - postura: peito estufado de quem está de serviço, passo de ronda.
#
# O rádio fica do lado direito dele (-X), virado para a câmera nas vistas de
# lado e de 3/4: o jogador sempre vê o rádio, que é como o Rafael fala com
# o grupo, na frequência do rádio.
#
# Modelagem: só primitivas, DETALHE 3 e sombreamento suave, como o Gabriel
# (ver comum.py). O esqueleto tem as mesmas juntas do Gabriel, então a
# caminhada, a respiração, os retratos e o resto do roteiro são os do
# comum.py (item 7, gerar_em_pe).

import math
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as c  # noqa: E402
import bpy  # noqa: E402

MAX_CORES = 48
DETALHE = 3

# Passo de ronda: o do Gabriel com o braço balançando um pouco mais.
PASSO = {"coxa": 22, "joelho": 52, "braco": 18}


def criar_materiais():
    m = c.Materiais()
    return m, {
        "pele": m.novo("pele", "#9a6a4a"),
        "cabelo": m.novo("cabelo", "#221a18"),
        "bigode": m.novo("bigode", "#3a2a22", "plano"),
        "camisa": m.novo("camisa", "#93b4d6"),
        "camisa_escura": m.novo("camisa_escura", "#6a8bb3"),
        "marinho": m.novo("marinho", "#28304a"),
        "cinto": m.novo("cinto", "#1c1c22"),
        "metal": m.novo("metal", "#9aa0a8", aspereza=0.5),
        "metal_escuro": m.novo("metal_escuro", "#3a3d44", aspereza=0.5),
        "coturno": m.novo("coturno", "#202027"),
        "radio": m.novo("radio", "#2a2b30"),
        "visor": m.novo("visor", "#7fa36a", "plano"),     # o LCD esverdeado do HT
        "emblema": m.novo("emblema", "#e2c04a", "plano"),
        "cracha": m.novo("cracha", "#e6e4dc", "plano"),
        "olho": m.novo("olho", "#1b1618", "plano"),
        "boca": m.novo("boca", "#55291f", "plano"),
    }


# ---------------------------------------------------------------------------
# O Rafael
# ---------------------------------------------------------------------------
#
# 1,72 m, magro, quase da altura do Gabriel. Juntas com os nomes do
# gerar_gabriel.py. A roupa é larga: os raios da camisa e da calça são
# maiores que o corpo pediria.


def perna(nome, lado, mt, quadril, giro_coxa, giro_joelho):
    """Calça azul-marinho folgada e coturno preto."""
    junta = c.pivo(f"{nome}Quadril", (0.095 * lado, 0.0, 0.0), quadril, (giro_coxa, 0, 0))
    c.membro(f"{nome}Coxa", 0.09, 0.08, 0.41, mt["marinho"], junta)
    joelho = c.pivo(f"{nome}Joelho", (0, 0, -0.41), junta, (giro_joelho, 0, 0))
    c.membro(f"{nome}Canela", 0.08, 0.074, 0.36, mt["marinho"], joelho)
    tornozelo = c.pivo(f"{nome}Tornozelo", (0, 0, -0.36), joelho, (-giro_coxa - giro_joelho, 0, 0))
    c.caixa(f"{nome}Coturno", (0.11, 0.25, 0.13), (0, -0.03, -0.035), mt["coturno"], tornozelo, bisel=0.02)
    c.caixa(f"{nome}Cadarco", (0.06, 0.012, 0.09), (0, -0.098, -0.01), mt["cinto"], tornozelo, (-8, 0, 0))
    c.caixa(f"{nome}Sola", (0.115, 0.27, 0.03), (0, -0.035, -0.085), mt["cinto"], tornozelo)


def braco(nome, lado, mt, tronco, giro_ombro, giro_cotovelo, emblema=False):
    """Manga curta, larga e comprida demais (quase no cotovelo), o braço
    fino saindo dela e a mão."""
    ombro = c.pivo(f"{nome}Ombro", (0.235 * lado, 0.0, 0.47), tronco, (giro_ombro, 4 * lado, 0))
    c.membro(f"{nome}Manga", 0.085, 0.082, 0.24, mt["camisa"], ombro)
    c.membro(f"{nome}Braco", 0.052, 0.048, 0.28, mt["pele"], ombro)
    if emblema:
        c.caixa(f"{nome}Emblema", (0.012, 0.055, 0.06), (0.085 * lado, 0.0, -0.08), mt["emblema"], ombro)
    cotovelo = c.pivo(f"{nome}Cotovelo", (0, 0, -0.28), ombro, (giro_cotovelo, 0, 0))
    c.membro(f"{nome}Antebraco", 0.048, 0.042, 0.23, mt["pele"], cotovelo)
    c.caixa(f"{nome}Mao", (0.055, 0.08, 0.09), (0, 0, -0.285), mt["pele"], cotovelo, bisel=0.02)


def cabeca(mt, tronco):
    pescoco = c.pivo("Cabeca", (0, 0, 0.58), tronco, (-1, 0, 0))
    c.caixa("Rosto", (0.2, 0.23, 0.245), (0, 0, 0.125), mt["pele"], pescoco, bisel=0.04)
    c.caixa("Nariz", (0.036, 0.05, 0.055), (0, -0.115, 0.1), mt["pele"], pescoco)
    for lado in (-1, 1):
        c.caixa(f"Orelha{lado}", (0.03, 0.05, 0.065), (0.105 * lado, 0.01, 0.12), mt["pele"], pescoco)
        c.caixa(f"Olho{lado}", (0.035, 0.01, 0.03), (0.048 * lado, -0.112, 0.135), mt["olho"], pescoco)
        c.caixa(f"Sobrancelha{lado}", (0.046, 0.012, 0.013), (0.048 * lado, -0.112, 0.168), mt["cabelo"], pescoco)
        c.caixa(f"CantoCima{lado}", (0.012, 0.01, 0.012), (0.03 * lado, -0.1135, 0.056), mt["boca"], pescoco)
        c.caixa(f"CantoBaixo{lado}", (0.012, 0.01, 0.012), (0.027 * lado, -0.1135, 0.044), mt["boca"], pescoco)
    # Bigodinho ralo, de quem quer parecer mais velho: aparece no sprite de
    # jogo também (é o que diferencia o rosto dele de longe).
    c.caixa("Bigode", (0.075, 0.012, 0.012), (0, -0.117, 0.07), mt["bigode"], pescoco)
    c.caixa("Boca", (0.045, 0.01, 0.012), (0, -0.114, 0.05), mt["boca"], pescoco)
    c.caixa("BocaRiso", (0.05, 0.01, 0.024), (0, -0.114, 0.047), mt["boca"], pescoco)
    # Cabelo curto aparecendo embaixo do boné, nos lados e na nuca.
    for lado in (-1, 1):
        c.caixa(f"CabeloLado{lado}", (0.025, 0.12, 0.08), (0.103 * lado, 0.03, 0.17), mt["cabelo"], pescoco)
    c.caixa("CabeloNuca", (0.21, 0.06, 0.12), (0, 0.09, 0.15), mt["cabelo"], pescoco, bisel=0.015)
    # Boné azul-marinho enterrado na cabeça, aba um pouco caída, com o
    # emblema amarelo na frente.
    c.caixa("Bone", (0.226, 0.246, 0.09), (0, 0.005, 0.24), mt["marinho"], pescoco, bisel=0.04)
    c.caixa("Aba", (0.19, 0.12, 0.018), (0, -0.16, 0.2), mt["marinho"], pescoco, (8, 0, 0), bisel=0.008)
    c.caixa("EmblemaBone", (0.045, 0.01, 0.035), (0, -0.124, 0.245), mt["emblema"], pescoco)
    return pescoco


def montar(mt):
    raiz = c.pivo("Rafael")
    quadril = c.pivo("Quadril", (0, 0, 0.87), raiz)
    perna("PernaDir", -1, mt, quadril, -2, 3)
    perna("PernaEsq", +1, mt, quadril, 3, 2)
    # Peito estufado de quem está de serviço.
    tronco = c.pivo("Tronco", (0, 0, 0), quadril, (-2, 0, 0))
    c.caixa("Bacia", (0.29, 0.16, 0.16), (0, 0, 0.0), mt["marinho"], tronco, bisel=0.03)
    # Cinto preto com a fivela de metal; a camisa larga por dentro da calça.
    c.cone("Cinto", 0.205, 0.205, 0.045, (0, 0, 0.032), mt["cinto"], tronco, lados=8, achatar=0.62)
    c.caixa("Fivela", (0.05, 0.012, 0.035), (0, -0.13, 0.032), mt["metal"], tronco)
    c.cone("Camisa", 0.222, 0.238, 0.48, (0, 0, 0.295), mt["camisa"], tronco, lados=8, achatar=0.62)
    c.caixa("Carcela", (0.014, 0.012, 0.44), (0, -0.147, 0.3), mt["camisa_escura"], tronco)
    for lado in (-1, 1):
        c.caixa(f"Bolso{lado}", (0.085, 0.012, 0.075), (0.095 * lado, -0.146, 0.39), mt["marinho"], tronco)
        c.caixa(f"Dragona{lado}", (0.09, 0.17, 0.022), (0.16 * lado, 0.0, 0.53), mt["marinho"], tronco, (0, -14 * lado, 0))
    c.caixa("Cracha", (0.06, 0.01, 0.03), (0.095, -0.15, 0.33), mt["cracha"], tronco)
    c.caixa("Gola", (0.21, 0.14, 0.05), (0, 0.0, 0.535), mt["camisa_escura"], tronco, bisel=0.012)
    c.cone("Pescoco", 0.048, 0.048, 0.1, (0, 0, 0.56), mt["pele"], tronco, lados=6)
    # No cinto: o rádio HT no quadril direito (antena para cima, o visor
    # verde virado para fora) e a lanterna antiga de metal no esquerdo.
    radio = c.pivo("Radio", (-0.215, -0.03, 0.03), tronco, (0, 0, 0))
    c.caixa("RadioCorpo", (0.04, 0.065, 0.12), (0, 0, 0), mt["radio"], radio, bisel=0.008)
    c.caixa("RadioVisor", (0.008, 0.04, 0.025), (-0.022, 0, 0.03), mt["visor"], radio)
    c.cone("RadioAntena", 0.01, 0.007, 0.12, (0, 0.015, 0.12), mt["radio"], radio, lados=4)
    lanterna = c.pivo("Lanterna", (0.215, -0.02, -0.05), tronco, (0, 0, 0))
    c.cone("LanternaCorpo", 0.024, 0.024, 0.24, (0, 0, 0), mt["metal"], lanterna, lados=6)
    c.cone("LanternaCabeca", 0.036, 0.03, 0.05, (0, 0, -0.135), mt["metal_escuro"], lanterna, lados=6)
    braco("BracoDir", -1, mt, tronco, -2, -10, emblema=True)
    braco("BracoEsq", +1, mt, tronco, 3, -12)
    cabeca(mt, tronco)
    return raiz


# ---------------------------------------------------------------------------
# Retratos (caixa de diálogo)
# ---------------------------------------------------------------------------
#
# Enquadramento do comum.py (renderizar_retrato). Três expressões:
#   normal  meio sorriso (os cantos da boca para cima): caloroso;
#   rindo   boca aberta num riso e sobrancelhas erguidas: o brincalhão;
#   triste  boca curta com os cantos para baixo e sobrancelhas levantadas no
#           meio: a hora em que ele admite que não é reforma.

EXPRESSOES = ("normal", "rindo", "triste")


def expressao(qual):
    boca = bpy.data.objects["Boca"]
    boca.hide_render = qual == "rindo"
    boca.scale = (0.7, 1, 1) if qual == "triste" else (1, 1, 1)
    bpy.data.objects["BocaRiso"].hide_render = qual != "rindo"
    for lado in (-1, 1):
        bpy.data.objects[f"CantoCima{lado}"].hide_render = qual == "triste"
        bpy.data.objects[f"CantoBaixo{lado}"].hide_render = qual != "triste"
        sob = bpy.data.objects[f"Sobrancelha{lado}"]
        altura, giro = {"normal": (0.168, 0), "rindo": (0.178, 0), "triste": (0.172, -16 * lado)}[qual]
        sob.location.z = altura
        sob.rotation_euler = (0, math.radians(giro), 0)


def esconder_boca():
    for nome in ("Boca", "BocaRiso", "CantoCima-1", "CantoCima1", "CantoBaixo-1", "CantoBaixo1"):
        bpy.data.objects[nome].hide_render = True


def main():
    c.DETALHE = DETALHE
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = criar_materiais()
    c.usar_colecao("Rafael")
    raiz = montar(mt)
    c.achatar_sombra("Rosto")
    c.gerar_em_pe("rafael", raiz, materiais, MAX_CORES, EXPRESSOES, expressao, esconder_boca, passo=PASSO)


main()
