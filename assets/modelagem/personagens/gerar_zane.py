# gerar_zane.py — modela o Zane (2123) no Blender, por código, e renderiza
# os mesmos sprites do Gabriel: as cinco vistas de jogo, a caminhada e a
# respiração em cada uma e a folha de referência.
#
# ATENÇÃO: desde 2026-10-17 os retratos do Zane (normal, confiante, assustado,
# empolgado, desconfiado, concentrado e frustrado) vêm do pixelar_retratos.py,
# a partir da folha desenhada em zane_referencia/expressoes.jpg. Este script
# só renderiza os retratos antigos para a folha de referência e NÃO grava os
# zane_retrato_<expressão>.png.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_zane.py
#
# O que sai (em assets/sprites/personagens/zane/), com os tamanhos do Gabriel:
#   zane_<vista>.png             96 x 112 (resolução dobrada: o Godot mostra
#                                com escala 0,5), vistas lado, frente,
#                                tres_quartos, costas e tres_quartos_costas
#   zane_andar_<vista>.png       caminhada: 12 quadros de 96 x 112 lado a lado
#   zane_parado_<vista>.png      parado respirando: 8 quadros
#   zane_referencia.png          frente, 3/4, lado e costas, e os retratos
#                                (os do Blender, não os do jogo)
#   assets/modelagem/personagens/zane.blend   o modelo, para abrir e mexer
#
# Quem é (docs/historia/personagens/zane.md): rapaz de uns 20 anos, de 2123,
# quando a Unifor já era um polo de IA. Tem implantes cibernéticos, entende
# a tecnologia da Âncora melhor que ninguém e cuida das comunicações do
# grupo no computador do bunker.
# Confiante, direto, elétrico, e mais assustado do que admite.
#
# O visual conta isso (desde 2026-10-17 segue os retratos desenhados em
# zane_referencia/expressoes.jpg):
#   - implantes à vista: o braço direito inteiro é uma prótese de metal com
#     linhas de luz, um VISOR verde sobre os dois olhos, uma peça de metal na
#     orelha e na têmpora com luzinhas, uma placa de metal na mandíbula e uma
#     porta de conexão na nuca. A luz é o ciano-esverdeado da interface
#     holográfica dos áudios dele (a ficha, item 5);
#   - roupa de um futuro que ninguém reconhece: jaqueta técnica grafite
#     escuro com gola alta aberta em duas abas, painéis cinza, linhas de luz
#     e um hexágono no peito, zíper na diagonal, a manga do braço de metal
#     cortada no ombro, camiseta preta comprida aparecendo embaixo, calça
#     larga com tiras, botas de sola branca grossa com um friso de luz;
#   - cabelo branco, bagunçado, caindo na testa e nas orelhas e até a nuca;
#   - a cor dele é o grafite com a luz verde-ciano: nenhum outro personagem
#     é tão escuro, e a luz o separa do cenário (o amarelo-ácido da ficha
#     continua só na cor do nome dele na caixa de diálogo);
#   - postura: o contrário do Gabriel cansado. Peito aberto, queixo para
#     cima, braços um pouco afastados do corpo e um passo largo e saltado.
#
# Os implantes ficam do lado direito dele (-X), que é o lado virado para a
# câmera nas vistas de lado e de 3/4 e no retrato: o jogador vê o metal
# quase o tempo todo.
#
# Modelagem: só primitivas, com DETALHE 3 e sombreamento suave, como o
# Gabriel e a Clarice (ver comum.py). O esqueleto tem as mesmas juntas do
# Gabriel, então a caminhada e a respiração são as do comum.py (item 7),
# com amplitudes próprias.

import math
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as c  # noqa: E402
import bpy  # noqa: E402

MAX_CORES = 48
DETALHE = 3

# Caminhada mais larga e mais saltada que a do Gabriel (comum.pose_andar),
# com o braço balançando mais: é o jeito elétrico dele.
PASSO = {"coxa": 26, "joelho": 60, "braco": 22, "descida": 0.045}
# Respiração: a cabeça pende menos (ele fica de queixo erguido).
RESPIRAR = {"balanco_cabeca": 2}


def criar_materiais():
    m = c.Materiais()
    return m, {
        "pele": m.novo("pele", "#d6a07a"),
        "cabelo": m.novo("cabelo", "#e9eaf3"),          # branco, com um tom azulado nas sombras
        "cabelo_raiz": m.novo("cabelo_raiz", "#7a7f8c"),  # sobrancelhas
        "jaqueta": m.novo("jaqueta", "#2f343c"),
        "jaqueta_escura": m.novo("jaqueta_escura", "#23272e"),
        "grafite": m.novo("grafite", "#59606c"),
        "camiseta": m.novo("camiseta", "#15171c"),
        "calca": m.novo("calca", "#2d3139"),
        "bota": m.novo("bota", "#23252b"),
        "sola": m.novo("sola", "#d9d8d0"),
        "metal": m.novo("metal", "#8e97a3", aspereza=0.5),
        "metal_escuro": m.novo("metal_escuro", "#4a505b", aspereza=0.5),
        # Luz dos implantes e o olho de implante: emitem, cor sempre chapada.
        "luz": m.novo("luz", "#3df2d2", "brilho"),
        "visor_lente": m.novo("visor_lente", "#52f59d", "brilho"),
        "visor_aro": m.novo("visor_aro", "#1d2128"),
        "olho": m.novo("olho", "#1b1822", "plano"),
        "boca": m.novo("boca", "#5a3028", "plano"),
    }


# ---------------------------------------------------------------------------
# O Zane
# ---------------------------------------------------------------------------
#
# 1,80 m de corpo (o topete passa disso), um pouco mais alto que o Gabriel.
# Os nomes das juntas são os do gerar_gabriel.py: é isso que deixa o
# comum.pose_andar e o comum.pose_parado mexerem nele.
#
# Abertura (rotação em Y) afasta a perna ou o braço do corpo. A peça pende
# para baixo, e girar +θ em Y leva a ponta para -X; por isso o lado +1 usa
# -θ e o lado -1 usa +θ: os dois abrem para fora.


def perna(nome, lado, mt, quadril, giro_coxa, giro_joelho):
    """Calça larga e reta, bota de sola grossa com um friso de luz."""
    junta = c.pivo(f"{nome}Quadril", (0.1 * lado, 0.0, 0.0), quadril, (giro_coxa, -2 * lado, 0))
    c.membro(f"{nome}Coxa", 0.095, 0.082, 0.43, mt["calca"], junta)
    joelho = c.pivo(f"{nome}Joelho", (0, 0, -0.43), junta, (giro_joelho, 0, 0))
    c.membro(f"{nome}Canela", 0.082, 0.08, 0.37, mt["calca"], joelho)
    tornozelo = c.pivo(f"{nome}Tornozelo", (0, 0, -0.37), joelho, (-giro_coxa - giro_joelho, 0, 0))
    c.caixa(f"{nome}Bota", (0.12, 0.25, 0.11), (0, -0.035, -0.04), mt["bota"], tornozelo, bisel=0.025)
    c.caixa(f"{nome}Sola", (0.13, 0.28, 0.05), (0, -0.04, -0.097), mt["sola"], tornozelo, bisel=0.012)
    # O friso de luz na lateral da sola: um pouco mais largo que ela, para
    # aparecer dos dois lados.
    c.caixa(f"{nome}FrisoLuz", (0.134, 0.2, 0.012), (0, -0.04, -0.097), mt["luz"], tornozelo)
    c.caixa(f"{nome}Fivela", (0.124, 0.03, 0.025), (0, 0.02, 0.0), mt["metal_escuro"], tornozelo)


def braco_jaqueta(nome, lado, mt, tronco, giro_ombro, giro_cotovelo):
    """O braço esquerdo: manga amarela inteira, punho grafite e a mão."""
    ombro = c.pivo(f"{nome}Ombro", (0.245 * lado, 0.0, 0.5), tronco, (giro_ombro, -6 * lado, 0))
    c.membro(f"{nome}Braco", 0.076, 0.066, 0.31, mt["jaqueta"], ombro)
    cotovelo = c.pivo(f"{nome}Cotovelo", (0, 0, -0.31), ombro, (giro_cotovelo, 0, 0))
    c.membro(f"{nome}Antebraco", 0.066, 0.06, 0.24, mt["jaqueta"], cotovelo)
    c.cone(f"{nome}Punho", 0.063, 0.063, 0.05, (0, 0, -0.24), mt["grafite"], cotovelo, lados=6)
    c.caixa(f"{nome}Mao", (0.06, 0.085, 0.1), (0, 0, -0.31), mt["pele"], cotovelo, bisel=0.02)


def braco_implante(nome, lado, mt, tronco, giro_ombro, giro_cotovelo):
    """O braço direito: a manga da jaqueta acaba no ombro e daí para baixo
    é prótese. Mais fino que a manga, com a junta do cotovelo à mostra,
    linhas de luz no antebraço e a mão de metal escuro."""
    ombro = c.pivo(f"{nome}Ombro", (0.245 * lado, 0.0, 0.5), tronco, (giro_ombro, -6 * lado, 0))
    c.membro(f"{nome}Manga", 0.08, 0.077, 0.1, mt["jaqueta"], ombro)
    c.cone(f"{nome}MangaBarra", 0.079, 0.079, 0.03, (0, 0, -0.1), mt["grafite"], ombro, lados=6)
    c.membro(f"{nome}Braco", 0.055, 0.05, 0.31, mt["metal"], ombro)
    c.cone(f"{nome}Anel", 0.058, 0.058, 0.025, (0, 0, -0.2), mt["metal_escuro"], ombro, lados=6)
    cotovelo = c.pivo(f"{nome}Cotovelo", (0, 0, -0.31), ombro, (giro_cotovelo, 0, 0))
    c.esfera(f"{nome}Junta", 0.057, (0, 0, 0), mt["metal_escuro"], cotovelo, seg=6, aneis=4)
    c.membro(f"{nome}Antebraco", 0.058, 0.05, 0.25, mt["metal"], cotovelo)
    c.caixa(f"{nome}LuzFrente", (0.012, 0.01, 0.17), (0, -0.057, -0.12), mt["luz"], cotovelo)
    c.caixa(f"{nome}LuzLado", (0.01, 0.012, 0.15), (0.057 * lado, 0, -0.12), mt["luz"], cotovelo)
    c.cone(f"{nome}Pulso", 0.05, 0.05, 0.03, (0, 0, -0.25), mt["metal_escuro"], cotovelo, lados=6)
    c.caixa(f"{nome}Mao", (0.065, 0.09, 0.1), (0, 0, -0.31), mt["metal_escuro"], cotovelo, bisel=0.02)


def cabeca(mt, tronco):
    # Queixo um pouco para cima: o contrário da cabeça baixa do Gabriel.
    pescoco = c.pivo("Cabeca", (0, 0, 0.61), tronco, (-4, 0, 0))
    c.caixa("Rosto", (0.2, 0.22, 0.245), (0, 0, 0.125), mt["pele"], pescoco, bisel=0.04)
    c.caixa("Nariz", (0.035, 0.05, 0.055), (0, -0.112, 0.1), mt["pele"], pescoco)
    for lado in (-1, 1):
        c.caixa(f"Orelha{lado}", (0.03, 0.05, 0.06), (0.105 * lado, 0.01, 0.12), mt["pele"], pescoco)
        c.caixa(f"Sobrancelha{lado}", (0.048, 0.012, 0.013), (0.048 * lado, -0.112, 0.172), mt["cabelo_raiz"], pescoco)
    # Boca: só nos retratos, como a do Gabriel. O canto é o sorriso de lado
    # do "confiante"; a aberta é a do "assustado".
    c.caixa("Boca", (0.05, 0.01, 0.012), (0, -0.114, 0.05), mt["boca"], pescoco)
    c.caixa("CantoBoca", (0.018, 0.01, 0.012), (0.04, -0.1135, 0.062), mt["boca"], pescoco, (0, -30, 0))
    c.caixa("BocaAberta", (0.026, 0.01, 0.028), (0, -0.114, 0.048), mt["boca"], pescoco)
    # Visor: uma faixa escura sobre os dois olhos, com a lente verde que
    # brilha, e as hastes que vão até as orelhas.
    c.caixa("Visor", (0.214, 0.02, 0.062), (0, -0.117, 0.135), mt["visor_aro"], pescoco, bisel=0.01)
    c.caixa("VisorLente", (0.186, 0.01, 0.042), (0, -0.1285, 0.135), mt["visor_lente"], pescoco)
    for lado in (-1, 1):
        c.caixa(f"VisorHaste{lado}", (0.012, 0.1, 0.03), (0.108 * lado, -0.055, 0.135), mt["visor_aro"], pescoco)
    # Implantes da cabeça: peça de metal na orelha e na têmpora direita com
    # dois pontos de luz, a placa de metal na mandíbula e a porta na nuca.
    c.caixa("PlacaTempora", (0.026, 0.1, 0.085), (-0.118, 0.01, 0.125), mt["metal"], pescoco, bisel=0.008)
    for i, y in enumerate((-0.02, 0.025)):
        c.caixa(f"LuzTempora{i}", (0.01, 0.016, 0.014), (-0.132, y, 0.14), mt["luz"], pescoco)
    c.caixa("Mandibula", (0.03, 0.1, 0.055), (-0.098, -0.04, 0.035), mt["metal"], pescoco, bisel=0.008)
    c.caixa("MandibulaEscura", (0.034, 0.05, 0.02), (-0.1, -0.075, 0.01), mt["metal_escuro"], pescoco)
    c.caixa("PortaNuca", (0.05, 0.022, 0.05), (0, 0.112, 0.025), mt["metal_escuro"], pescoco, bisel=0.008)
    c.caixa("LuzNuca", (0.022, 0.01, 0.014), (0, 0.124, 0.03), mt["luz"], pescoco)
    # Cabelo branco e bagunçado: o topo, mechas caindo na testa, mechas
    # grandes nos lados (cobrem as orelhas) e a nuca comprida.
    c.caixa("CabeloTopo", (0.22, 0.25, 0.09), (0, 0.01, 0.245), mt["cabelo"], pescoco, bisel=0.03)
    for i, (x, rx, rz) in enumerate([(-0.07, 14, 10), (0.0, 18, 0), (0.07, 12, -12)]):
        c.caixa(f"Franja{i}", (0.07, 0.05, 0.075), (x, -0.1, 0.212), mt["cabelo"], pescoco, (rx, 0, rz), bisel=0.012)
    for lado in (-1, 1):
        c.caixa(f"Madeixa{lado}", (0.045, 0.15, 0.17), (0.108 * lado, 0.02, 0.16), mt["cabelo"], pescoco, bisel=0.015)
        c.caixa(f"MadeixaPonta{lado}", (0.04, 0.07, 0.07), (0.112 * lado, 0.0, 0.07), mt["cabelo"], pescoco,
                (0, 0, 8 * lado), bisel=0.012)
    c.caixa("CabeloNuca", (0.215, 0.075, 0.2), (0, 0.095, 0.15), mt["cabelo"], pescoco, bisel=0.02)
    for i, (x, y, z, rx, ry) in enumerate([(-0.045, -0.02, 0.3, -20, -12), (0.03, 0.0, 0.305, -15, 14),
                                            (-0.01, 0.05, 0.295, 10, 0)]):
        c.caixa(f"Ponta{i}", (0.06, 0.06, 0.07), (x, y, z), mt["cabelo"], pescoco, (rx, ry, 0), bisel=0.01)
    return pescoco


def montar(mt):
    raiz = c.pivo("Zane")
    quadril = c.pivo("Quadril", (0, 0, 0.92), raiz)
    perna("PernaDir", -1, mt, quadril, -2, 3)
    perna("PernaEsq", +1, mt, quadril, 3, 2)
    # Tronco um pouco para trás: peito aberto.
    tronco = c.pivo("Tronco", (0, 0, 0), quadril, (-2, 0, 0))
    c.caixa("Bacia", (0.31, 0.16, 0.16), (0, 0, 0.0), mt["calca"], tronco, bisel=0.03)
    # Camiseta preta comprida, saindo por baixo da jaqueta curta.
    c.cone("Camiseta", 0.2, 0.205, 0.2, (0, 0, 0.08), mt["camiseta"], tronco, lados=8, achatar=0.6)
    # Jaqueta técnica: corpo amarelo, barra grafite, painéis grafite nos
    # lados, zíper na diagonal e a gola alta.
    c.cone("Jaqueta", 0.222, 0.24, 0.4, (0, 0, 0.36), mt["jaqueta"], tronco, lados=8, achatar=0.6)
    c.cone("JaquetaBarra", 0.226, 0.226, 0.05, (0, 0, 0.165), mt["grafite"], tronco, lados=8, achatar=0.62)
    for lado in (-1, 1):
        c.caixa(f"Painel{lado}", (0.03, 0.17, 0.34), (0.218 * lado, 0.0, 0.36), mt["grafite"], tronco)
    c.caixa("Ziper", (0.014, 0.012, 0.42), (0.0, -0.142, 0.36), mt["grafite"], tronco, (0, -16, 0))
    c.cone("Gola", 0.105, 0.095, 0.08, (0, 0, 0.575), mt["jaqueta_escura"], tronco, lados=8)
    c.cone("Pescoco", 0.05, 0.05, 0.1, (0, 0, 0.6), mt["pele"], tronco, lados=6)
    # Gola alta aberta em duas abas, com a borda cinza.
    for lado in (-1, 1):
        c.caixa(f"GolaAba{lado}", (0.05, 0.13, 0.13), (0.09 * lado, 0.0, 0.62), mt["jaqueta"], tronco,
                (0, 14 * lado, 0), bisel=0.012)
        c.caixa(f"GolaBorda{lado}", (0.012, 0.13, 0.12), (0.112 * lado, 0.0, 0.62), mt["grafite"], tronco,
                (0, 14 * lado, 0))
    # Ombreira no ombro esquerdo (o do braço de carne), e uma faixa de luz no
    # peito do mesmo lado.
    c.caixa("Ombreira", (0.12, 0.2, 0.05), (0.2, 0.0, 0.55), mt["jaqueta_escura"], tronco, (0, -18, 0), bisel=0.015)
    for i, z in enumerate((0.47, 0.44, 0.41)):
        c.caixa(f"FaixaLuz{i}", (0.07 - 0.012 * i, 0.01, 0.01), (0.1, -0.143, z), mt["luz"], tronco)
    c.cone("HexPeito", 0.03, 0.03, 0.01, (-0.115, -0.145, 0.46), mt["luz"], tronco, (90, 0, 0), lados=6)
    # Nas costas: um painel grafite com um risco de luz.
    c.caixa("PainelCostas", (0.12, 0.012, 0.12), (0, 0.145, 0.4), mt["grafite"], tronco)
    c.caixa("LuzCostas", (0.08, 0.01, 0.012), (0, 0.152, 0.4), mt["luz"], tronco)
    # Tiras: uma pendurada do cós e uma presa na coxa direita.
    c.caixa("TiraCos", (0.03, 0.012, 0.22), (-0.12, -0.112, -0.06), mt["camiseta"], tronco, (0, 8, 0))
    c.cone("TiraCoxa", 0.099, 0.099, 0.03, (0, 0, -0.18), mt["camiseta"], bpy.data.objects["PernaDirQuadril"], lados=8)
    braco_implante("BracoDir", -1, mt, tronco, -3, -10)
    braco_jaqueta("BracoEsq", +1, mt, tronco, 4, -14)
    cabeca(mt, tronco)
    return raiz


# ---------------------------------------------------------------------------
# Retratos (caixa de diálogo)
# ---------------------------------------------------------------------------
#
# Enquadramento do comum.py (renderizar_retrato), igual ao do Gabriel. Três
# expressões, feitas com a boca e as sobrancelhas:
#   normal     boca reta, sobrancelhas retas;
#   confiante  sorriso de lado (a boca anda para um lado e o canto sobe) e
#              uma sobrancelha erguida;
#   assustado  boca aberta e as sobrancelhas levantadas no meio: o medo que
#              ele não admite.

EXPRESSOES = ("normal", "confiante", "assustado")


def expressao(qual):
    boca = bpy.data.objects["Boca"]
    boca.hide_render = qual == "assustado"
    boca.location.x = 0.012 if qual == "confiante" else 0.0
    boca.scale = (0.8, 1, 1) if qual == "confiante" else (1, 1, 1)
    bpy.data.objects["CantoBoca"].hide_render = qual != "confiante"
    bpy.data.objects["BocaAberta"].hide_render = qual != "assustado"
    for lado in (-1, 1):
        sob = bpy.data.objects[f"Sobrancelha{lado}"]
        if qual == "confiante":
            altura, giro = (0.188, -14) if lado > 0 else (0.168, 6)
        else:
            altura, giro = {"normal": (0.172, 0), "assustado": (0.18, -14 * lado)}[qual]
        sob.location.z = altura
        sob.rotation_euler = (0, math.radians(giro), 0)


def esconder_boca():
    for nome in ("Boca", "CantoBoca", "BocaAberta"):
        bpy.data.objects[nome].hide_render = True


def main():
    c.DETALHE = DETALHE
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = criar_materiais()
    c.usar_colecao("Zane")
    raiz = montar(mt)
    c.achatar_sombra("Rosto")
    c.gerar_em_pe("zane", raiz, materiais, MAX_CORES, EXPRESSOES, expressao, esconder_boca,
                  passo=PASSO, respirar=RESPIRAR, salvar_retratos=False)


main()
