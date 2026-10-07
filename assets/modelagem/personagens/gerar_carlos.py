# gerar_carlos.py — modela o Carlos, o cientista de 3026, no Blender, por
# código, e renderiza os mesmos sprites do Gabriel: as cinco vistas de jogo,
# a caminhada e a respiração em cada uma, os retratos da caixa de diálogo e
# a folha de referência.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_carlos.py
#
# O que sai (em assets/sprites/personagens/carlos/), com os tamanhos do Gabriel:
#   carlos_<vista>.png             96 x 112 (resolução dobrada: o Godot mostra
#                                  com escala 0,5), vistas lado, frente,
#                                  tres_quartos, costas e tres_quartos_costas
#   carlos_andar_<vista>.png       caminhada: 12 quadros de 96 x 112
#   carlos_parado_<vista>.png      parado respirando: 8 quadros
#   carlos_retrato_<expressão>.png 80 x 80 (normal, maniaco, furioso)
#   carlos_referencia.png          frente, 3/4, lado e costas, e os retratos
#   assets/modelagem/personagens/carlos.blend   o modelo
#
# Quem é: a ideia 23 de docs/historia/outras_ideias.md, AINDA NÃO APROVADA.
# Cientista que já vivia em 3026 e criou a Âncora. Quando a humanidade foi
# embora, ele ficou, obcecado por uma época antiga (a ideia sugere os anos
# 60), para fugir para ela. Este modelo é o visual dele caso a ideia entre;
# se a ideia mudar, o visual muda junto.
#
# O visual conta isso (o "cientista maluco" pedido pelo Davi):
#   - mais velho que todo o grupo (que tem uns 20 anos): cabelo grisalho
#     arrepiado dos lados, careca no alto, sobrancelhas grossas, magro e
#     pálido de quem vive trancado no laboratório;
#   - o cientista: jaleco comprido até o joelho, sujo e manchado, com
#     canetas no bolso, luvas de borracha pretas;
#   - a obsessão pela época antiga, por baixo do jaleco: colete de tricô,
#     camisa clara, gravata fina mostarda, calça de tergal marrom e sapato
#     social, como um professor dos anos 60, e óculos de aro grosso;
#   - o lado de 3026: uma lupa articulada com lente VERMELHA presa nos
#     óculos, sobre o olho direito, e um controle com luz vermelha no cinto.
#     É o mesmo vermelho dos olhos dos robôs: na ideia, ele controla parte
#     deles;
#   - a cor dele é o branco sujo do jaleco com o ponto vermelho: ninguém
#     mais no jogo usa branco;
#   - postura: curvado para a frente, a cabeça esticada, braços um pouco
#     para a frente. Passo curto e rápido.
#
# A lupa e o controle ficam do lado direito dele (-X), virado para a câmera
# nas vistas de lado e de 3/4.
#
# Modelagem: só primitivas, DETALHE 3 e sombreamento suave, como o Gabriel
# (ver comum.py). O esqueleto tem as mesmas juntas do Gabriel, e o resto do
# roteiro é o do comum.py (item 7, gerar_em_pe).

import math
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as c  # noqa: E402
import bpy  # noqa: E402

MAX_CORES = 48
DETALHE = 3

# Passo curto (o jaleco atrapalha as pernas) e braço balançando pouco.
PASSO = {"coxa": 16, "joelho": 46, "braco": 10}
# Respiração mais funda, com a cabeça balançando mais: sempre agitado.
RESPIRAR = {"balanco_cabeca": 4}


def criar_materiais():
    m = c.Materiais()
    return m, {
        "pele": m.novo("pele", "#dcb8a0"),
        "cabelo": m.novo("cabelo", "#bdb9b2"),
        "jaleco": m.novo("jaleco", "#d6d4cc"),
        "mancha": m.novo("mancha", "#a59c86"),
        "camisa": m.novo("camisa", "#b9c7cf"),
        "gravata": m.novo("gravata", "#c08a2c"),
        "trico": m.novo("trico", "#6b5a3a"),
        "calca": m.novo("calca", "#5a4838"),
        "sapato": m.novo("sapato", "#3a2a20"),
        "luva": m.novo("luva", "#25252b"),
        "metal": m.novo("metal", "#7d848d", aspereza=0.5),
        "caneta_azul": m.novo("caneta_azul", "#3d5fa8", "plano"),
        "caneta_vermelha": m.novo("caneta_vermelha", "#b8483a", "plano"),
        # O vermelho dos olhos dos robôs (gerar_robos.py): a lente e a luz do controle.
        "luz_vermelha": m.novo("luz_vermelha", "#ff4032", "brilho"),
        "olho": m.novo("olho", "#1b1620", "plano"),
        "oculos": m.novo("oculos", "#1a1618", "plano"),
        "lente": m.novo("lente", "#c6dde6", "plano"),
        "boca": m.novo("boca", "#5a2a26", "plano"),
    }


# ---------------------------------------------------------------------------
# O Carlos
# ---------------------------------------------------------------------------
#
# 1,80 m de corpo, mas curvado. Juntas com os nomes do gerar_gabriel.py.


def perna(nome, lado, mt, quadril, giro_coxa, giro_joelho):
    """Calça de tergal marrom e sapato social."""
    junta = c.pivo(f"{nome}Quadril", (0.09 * lado, 0.0, 0.0), quadril, (giro_coxa, 0, 0))
    c.membro(f"{nome}Coxa", 0.078, 0.064, 0.42, mt["calca"], junta)
    joelho = c.pivo(f"{nome}Joelho", (0, 0, -0.42), junta, (giro_joelho, 0, 0))
    c.membro(f"{nome}Canela", 0.064, 0.058, 0.38, mt["calca"], joelho)
    tornozelo = c.pivo(f"{nome}Tornozelo", (0, 0, -0.38), joelho, (-giro_coxa - giro_joelho, 0, 0))
    c.caixa(f"{nome}Sapato", (0.095, 0.26, 0.07), (0, -0.045, -0.055), mt["sapato"], tornozelo, bisel=0.022)
    c.caixa(f"{nome}Sola", (0.1, 0.27, 0.02), (0, -0.045, -0.09), mt["sapato"], tornozelo)


def braco(nome, lado, mt, tronco, giro_ombro, giro_cotovelo):
    """Manga comprida do jaleco e a luva de borracha preta."""
    ombro = c.pivo(f"{nome}Ombro", (0.22 * lado, 0.0, 0.47), tronco, (giro_ombro, 4 * lado, 0))
    c.membro(f"{nome}Braco", 0.068, 0.06, 0.31, mt["jaleco"], ombro)
    cotovelo = c.pivo(f"{nome}Cotovelo", (0, 0, -0.31), ombro, (giro_cotovelo, 0, 0))
    c.membro(f"{nome}Antebraco", 0.06, 0.056, 0.24, mt["jaleco"], cotovelo)
    c.cone(f"{nome}Luva", 0.045, 0.05, 0.06, (0, 0, -0.24), mt["luva"], cotovelo, lados=6)
    c.caixa(f"{nome}Mao", (0.058, 0.085, 0.1), (0, 0, -0.3), mt["luva"], cotovelo, bisel=0.02)


def cabeca(mt, tronco):
    # O corpo curva para a frente e a cabeça se estica, olhando para cima.
    pescoco = c.pivo("Cabeca", (0, -0.02, 0.6), tronco, (-14, 0, 0))
    c.caixa("Rosto", (0.19, 0.22, 0.255), (0, 0, 0.125), mt["pele"], pescoco, bisel=0.04)
    c.caixa("Nariz", (0.034, 0.06, 0.065), (0, -0.118, 0.1), mt["pele"], pescoco, (8, 0, 0))
    for lado in (-1, 1):
        c.caixa(f"Orelha{lado}", (0.03, 0.05, 0.065), (0.098 * lado, 0.01, 0.12), mt["pele"], pescoco)
        c.caixa(f"Olho{lado}", (0.028, 0.006, 0.024), (0.045 * lado, -0.116, 0.135), mt["olho"], pescoco)
        # Óculos de aro grosso (anos 60): lente clara com o aro inteiro em volta.
        c.caixa(f"Lente{lado}", (0.06, 0.006, 0.046), (0.047 * lado, -0.112, 0.135), mt["lente"], pescoco)
        c.caixa(f"AroCima{lado}", (0.068, 0.012, 0.016), (0.047 * lado, -0.115, 0.162), mt["oculos"], pescoco)
        c.caixa(f"AroBaixo{lado}", (0.062, 0.012, 0.01), (0.047 * lado, -0.115, 0.109), mt["oculos"], pescoco)
        c.caixa(f"Haste{lado}", (0.01, 0.12, 0.012), (0.094 * lado, -0.05, 0.15), mt["oculos"], pescoco)
        # Sobrancelhas grossas e grisalhas.
        c.caixa(f"Sobrancelha{lado}", (0.054, 0.016, 0.018), (0.047 * lado, -0.113, 0.178), mt["cabelo"], pescoco)
        c.caixa(f"CantoBoca{lado}", (0.014, 0.01, 0.014), (0.036 * lado, -0.1135, 0.06), mt["boca"], pescoco)
    c.caixa("Ponte", (0.03, 0.012, 0.012), (0, -0.115, 0.145), mt["oculos"], pescoco)
    c.caixa("Boca", (0.05, 0.01, 0.012), (0, -0.114, 0.05), mt["boca"], pescoco)
    c.caixa("BocaAberta", (0.06, 0.01, 0.03), (0, -0.114, 0.05), mt["boca"], pescoco)
    # A lupa articulada presa no aro direito: braço de metal e a lente
    # vermelha na frente do olho.
    c.caixa("LupaBraco", (0.012, 0.05, 0.012), (-0.085, -0.13, 0.165), mt["metal"], pescoco, (0, 0, 20))
    lupa = c.pivo("Lupa", (-0.06, -0.155, 0.135), pescoco, (90, 0, 0))
    c.cone("LupaAro", 0.03, 0.03, 0.03, (0, 0, 0), mt["metal"], lupa, lados=8)
    c.cone("LupaLente", 0.022, 0.022, 0.034, (0, 0, 0), mt["luz_vermelha"], lupa, lados=8)
    # Cabelo: careca no alto, tufos grisalhos arrepiados dos lados e atrás.
    # Cada mecha é um cone saindo da cabeça para fora e para cima. Girar +θ
    # em Y leva a ponta de uma peça em pé para +X, então o lado +1 usa +θ e
    # o lado -1 usa -θ: as duas abrem para fora. O giro em X joga para trás.
    for lado in (-1, 1):
        c.esfera(f"Tufo{lado}", 0.055, (0.1 * lado, 0.03, 0.17), mt["cabelo"], pescoco, escala=(0.8, 1.3, 1.1), seg=6, aneis=4)
        for i, (z, abre, tras, comp) in enumerate(((0.22, 62, -10, 0.13), (0.17, 85, 5, 0.12),
                                                     (0.12, 105, 15, 0.1), (0.2, 55, 35, 0.11))):
            mecha = c.pivo(f"Mecha{lado}_{i}", (0.09 * lado, 0.04, z), pescoco, (tras, abre * lado, 0))
            c.cone(f"MechaPeca{lado}_{i}", 0.032, 0.004, comp, (0, 0, comp / 2), mt["cabelo"], mecha, lados=5)
    c.esfera("TufoNuca", 0.07, (0, 0.1, 0.15), mt["cabelo"], pescoco, escala=(1.3, 0.7, 1.0), seg=6, aneis=4)
    for i, (x, tras) in enumerate(((-0.04, 50), (0.04, 55), (0.0, 70))):
        mecha = c.pivo(f"MechaNuca{i}", (x, 0.1, 0.2), pescoco, (tras, 0, 0))
        c.cone(f"MechaNucaPeca{i}", 0.03, 0.004, 0.1, (0, 0, 0.05), mt["cabelo"], mecha, lados=5)
    return pescoco


def montar(mt):
    raiz = c.pivo("Carlos")
    quadril = c.pivo("Quadril", (0, 0, 0.9), raiz)
    perna("PernaDir", -1, mt, quadril, -2, 4)
    perna("PernaEsq", +1, mt, quadril, 2, 3)
    # Curvado para a frente.
    tronco = c.pivo("Tronco", (0, 0, 0), quadril, (11, 0, 0))
    c.caixa("Bacia", (0.29, 0.15, 0.15), (0, 0, 0.0), mt["calca"], tronco, bisel=0.03)
    # Jaleco comprido até perto do joelho, aberto na frente: aparecem o
    # colete de tricô, a camisa, a gravata fina e a calça.
    c.cone("Jaleco", 0.24, 0.215, 0.86, (0, 0, 0.13), mt["jaleco"], tronco, lados=8, achatar=0.6)
    c.caixa("GolaJaleco", (0.3, 0.15, 0.05), (0, 0.01, 0.53), mt["jaleco"], tronco, bisel=0.015)
    for lado in (-1, 1):
        c.caixa(f"Lapela{lado}", (0.04, 0.02, 0.3), (0.07 * lado, -0.136, 0.4), mt["jaleco"], tronco, (0, 10 * lado, 0))
        c.caixa(f"BolsoBaixo{lado}", (0.1, 0.015, 0.08), (0.14 * lado, -0.135, -0.05), mt["jaleco"], tronco)
    c.caixa("Colete", (0.13, 0.02, 0.32), (0, -0.132, 0.3), mt["trico"], tronco)
    c.caixa("Camisa", (0.06, 0.02, 0.08), (0, -0.137, 0.49), mt["camisa"], tronco)
    c.caixa("Gravata", (0.026, 0.012, 0.3), (0, -0.145, 0.36), mt["gravata"], tronco)
    c.caixa("AberturaCalca", (0.12, 0.02, 0.3), (0, -0.138, -0.13), mt["calca"], tronco)
    # Manchas no jaleco e as canetas no bolso do peito.
    c.caixa("Mancha0", (0.07, 0.012, 0.05), (0.15, -0.128, 0.1), mt["mancha"], tronco, (0, 20, 0))
    c.caixa("Mancha1", (0.05, 0.012, 0.07), (-0.16, -0.125, -0.2), mt["mancha"], tronco)
    c.caixa("Mancha2", (0.08, 0.012, 0.06), (0.05, 0.14, 0.0), mt["mancha"], tronco)
    c.caixa("BolsoPeito", (0.08, 0.015, 0.07), (0.13, -0.133, 0.38), mt["jaleco"], tronco)
    c.caixa("CanetaAzul", (0.012, 0.012, 0.06), (0.115, -0.14, 0.42), mt["caneta_azul"], tronco)
    c.caixa("CanetaVermelha", (0.012, 0.012, 0.055), (0.14, -0.14, 0.415), mt["caneta_vermelha"], tronco)
    c.cone("Pescoco", 0.045, 0.045, 0.12, (0, -0.01, 0.57), mt["pele"], tronco, lados=6)
    # O controle no cinto, do lado direito, com a luz vermelha dos robôs.
    c.caixa("Controle", (0.05, 0.08, 0.1), (-0.235, -0.02, 0.02), mt["metal"], tronco, bisel=0.01)
    c.caixa("ControleLuz", (0.01, 0.025, 0.02), (-0.262, -0.03, 0.045), mt["luz_vermelha"], tronco)
    braco("BracoDir", -1, mt, tronco, -10, -18)
    braco("BracoEsq", +1, mt, tronco, -8, -22)
    cabeca(mt, tronco)
    return raiz


# ---------------------------------------------------------------------------
# Retratos (caixa de diálogo)
# ---------------------------------------------------------------------------
#
# Enquadramento do comum.py (renderizar_retrato). Três expressões:
#   normal   boca reta, sobrancelhas retas;
#   maniaco  boca aberta num sorriso largo (cantos para cima) e sobrancelhas
#            lá em cima: o cientista maluco;
#   furioso  boca aberta e as sobrancelhas baixas, viradas para o meio.

EXPRESSOES = ("normal", "maniaco", "furioso")


def expressao(qual):
    bpy.data.objects["Boca"].hide_render = qual != "normal"
    aberta = bpy.data.objects["BocaAberta"]
    aberta.hide_render = qual == "normal"
    aberta.scale = (1, 1, 0.6) if qual == "maniaco" else (0.6, 1, 1)
    for lado in (-1, 1):
        bpy.data.objects[f"CantoBoca{lado}"].hide_render = qual != "maniaco"
        sob = bpy.data.objects[f"Sobrancelha{lado}"]
        altura, giro = {"normal": (0.178, 0), "maniaco": (0.19, 0), "furioso": (0.17, 20 * lado)}[qual]
        sob.location.z = altura
        sob.rotation_euler = (0, math.radians(giro), 0)


def esconder_boca():
    for nome in ("Boca", "BocaAberta", "CantoBoca-1", "CantoBoca1"):
        bpy.data.objects[nome].hide_render = True


def main():
    c.DETALHE = DETALHE
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = criar_materiais()
    c.usar_colecao("Carlos")
    raiz = montar(mt)
    c.achatar_sombra("Rosto")
    c.gerar_em_pe("carlos", raiz, materiais, MAX_CORES, EXPRESSOES, expressao, esconder_boca,
                  passo=PASSO, respirar=RESPIRAR)


main()
