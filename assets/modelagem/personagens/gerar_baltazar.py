# gerar_baltazar.py — modela o Baltazar Magalhães (~1750) no Blender, por
# código, e renderiza os mesmos sprites do Gabriel: as cinco vistas de
# jogo, a caminhada e a respiração em cada uma, os retratos da caixa de
# diálogo e a folha de referência.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_baltazar.py
#
# O que sai (em assets/sprites/personagens/baltazar/), com os tamanhos do Gabriel:
#   baltazar_<vista>.png             96 x 112 (resolução dobrada: o Godot
#                                    mostra com escala 0,5), vistas lado,
#                                    frente, tres_quartos, costas e
#                                    tres_quartos_costas
#   baltazar_andar_<vista>.png       caminhada: 12 quadros de 96 x 112
#   baltazar_parado_<vista>.png      parado respirando: 8 quadros
#   baltazar_retrato_<expressão>.png 80 x 80 (normal, encantado, aflito)
#   baltazar_referencia.png          frente, 3/4, lado e costas, e os retratos
#   assets/modelagem/personagens/baltazar.blend   o modelo
#
# Quem é (docs/historia/personagens/baltazar.md): rapaz de uns 20 anos, filho
# de colonos portugueses no Ceará de ~1750, de família de sítio, sem nada de
# nobre. Antepassado do Gabriel. Viu pela luneta uma luz sobre a mata, foi
# investigar e foi puxado. Homem de fé com olhos de cientista: cerimonioso,
# devoto, encantado com tudo.
#
# O visual conta isso:
#   - século XVIII à primeira vista: chapéu de três bicos (tricórnio) de
#     feltro, cabelo comprido preso atrás com uma fita (o rabicho), casaca
#     aberta até o meio da coxa com canhões largos nas mangas, colete por
#     baixo, camisa de linho, calções até o joelho, meias e sapato de fivela;
#   - de sítio, não de corte: tecidos simples e gastos pelos dias em 3026,
#     com um remendo na casaca. Nada de renda, galão ou peruca;
#   - a luneta de latão sempre por perto, pendurada no quadril direito por
#     uma bandoleira de couro (é o mesmo latão queimado da luneta do
#     acampamento, em gerar_antecessores.py);
#   - o ANEL de ouro na mão direita, novo (o do Gabriel é o mesmo, gasto);
#   - a casaca é cor de vinho, o tom do pau-brasil, a tinta da colônia. É
#     um eco escuro do vermelho do Gabriel: a mesma família, mil anos antes.
#     O chapéu e a silhueta de casaca separam os dois na tela;
#   - postura: em pé direito, cerimonioso, a cabeça um pouco para a frente,
#     de quem quer olhar tudo de perto. Passo curto e cuidadoso.
#
# A luneta e o anel ficam do lado direito dele (-X), virado para a câmera
# nas vistas de lado e de 3/4.
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

# Passo mais curto e com menos balanço de braço que o do Gabriel: cuidadoso.
PASSO = {"coxa": 19, "joelho": 50, "braco": 11}


def criar_materiais():
    m = c.Materiais()
    return m, {
        "pele": m.novo("pele", "#c98f68"),
        "cabelo": m.novo("cabelo", "#4a3020"),
        "fita": m.novo("fita", "#1f1c22"),
        "chapeu": m.novo("chapeu", "#3a3234"),
        "chapeu_debrum": m.novo("chapeu_debrum", "#5c5052"),   # a borda gasta das abas
        "linho": m.novo("linho", "#d8cfb5"),
        "colete": m.novo("colete", "#6e4c2e"),
        "casaca": m.novo("casaca", "#7a2e3a"),
        "casaca_escura": m.novo("casaca_escura", "#5a2230"),
        "remendo": m.novo("remendo", "#8f6a4c"),
        "calcoes": m.novo("calcoes", "#8a6c48"),
        "meia": m.novo("meia", "#c9c1ab"),
        "sapato": m.novo("sapato", "#2e2522"),
        "couro": m.novo("couro", "#5a3b24"),
        "latao": m.novo("latao", "#9c7d3a", aspereza=0.5),
        "latao_escuro": m.novo("latao_escuro", "#5a451d", aspereza=0.5),
        # O anel: cor chapada e clara, para o pixel de ouro não sumir na mão.
        "ouro": m.novo("ouro", "#e6bf4c", "plano"),
        "olho": m.novo("olho", "#1c1618", "plano"),
        "boca": m.novo("boca", "#5e2e28", "plano"),
    }


# ---------------------------------------------------------------------------
# O Baltazar
# ---------------------------------------------------------------------------
#
# 1,63 m de corpo (o tricórnio passa disso): um pouco mais baixo que o
# Gabriel, como era comum no século XVIII. Juntas com os nomes do
# gerar_gabriel.py.


def perna(nome, lado, mt, quadril, giro_coxa, giro_joelho):
    """Calções até o joelho, meia de lã e sapato de fivela."""
    junta = c.pivo(f"{nome}Quadril", (0.09 * lado, 0.0, 0.0), quadril, (giro_coxa, 0, 0))
    c.membro(f"{nome}Coxa", 0.085, 0.07, 0.39, mt["calcoes"], junta)
    joelho = c.pivo(f"{nome}Joelho", (0, 0, -0.39), junta, (giro_joelho, 0, 0))
    c.cone(f"{nome}Liga", 0.068, 0.068, 0.04, (0, 0, -0.01), mt["couro"], joelho, lados=6)
    c.membro(f"{nome}Canela", 0.062, 0.05, 0.34, mt["meia"], joelho)
    tornozelo = c.pivo(f"{nome}Tornozelo", (0, 0, -0.34), joelho, (-giro_coxa - giro_joelho, 0, 0))
    c.caixa(f"{nome}Sapato", (0.1, 0.23, 0.07), (0, -0.035, -0.05), mt["sapato"], tornozelo, bisel=0.02)
    c.caixa(f"{nome}Lingueta", (0.07, 0.03, 0.06), (0, -0.075, -0.01), mt["sapato"], tornozelo, (-20, 0, 0))
    c.caixa(f"{nome}Fivela", (0.05, 0.012, 0.03), (0, -0.098, -0.03), mt["latao"], tornozelo, (-20, 0, 0))
    c.caixa(f"{nome}Sola", (0.105, 0.24, 0.02), (0, -0.035, -0.09), mt["sapato"], tornozelo)


def braco(nome, lado, mt, tronco, giro_ombro, giro_cotovelo, anel=False):
    """Manga da casaca com o canhão largo, o punho da camisa e a mão."""
    ombro = c.pivo(f"{nome}Ombro", (0.215 * lado, 0.0, 0.44), tronco, (giro_ombro, 0, 0))
    c.membro(f"{nome}Braco", 0.07, 0.062, 0.29, mt["casaca"], ombro)
    cotovelo = c.pivo(f"{nome}Cotovelo", (0, 0, -0.29), ombro, (giro_cotovelo, 0, 0))
    c.membro(f"{nome}Antebraco", 0.062, 0.058, 0.2, mt["casaca"], cotovelo)
    c.cone(f"{nome}Canhao", 0.076, 0.08, 0.075, (0, 0, -0.17), mt["casaca_escura"], cotovelo, lados=6)
    c.cone(f"{nome}Punho", 0.052, 0.058, 0.035, (0, 0, -0.225), mt["linho"], cotovelo, lados=6)
    c.caixa(f"{nome}Mao", (0.055, 0.08, 0.09), (0, 0, -0.285), mt["pele"], cotovelo, bisel=0.02)
    if anel:
        c.caixa(f"{nome}Anel", (0.062, 0.088, 0.018), (0, 0, -0.3), mt["ouro"], cotovelo)


def tricornio(mt, pescoco):
    """Chapéu de três bicos: a copa redonda e três abas viradas para cima,
    formando um triângulo com uma ponta para a frente. Cada aba é uma caixa
    presa num pivô girado em Z (0°, 120° e 240°): a de 0° fica atrás, as
    outras duas nos lados da frente, e as quinas se encontram nas pontas."""
    c.esfera("Copa", 0.118, (0, 0.0, 0.265), mt["chapeu"], pescoco, escala=(1, 1, 0.75), seg=8, aneis=5)
    for i, giro in enumerate((0, 120, 240)):
        aba = c.pivo(f"Aba{i}", (0, 0.0, 0.24), pescoco, (0, 0, giro))
        c.caixa(f"AbaPeca{i}", (0.4, 0.022, 0.07), (0, 0.11, 0.025), mt["chapeu"], aba, (-32, 0, 0), bisel=0.008)
        c.caixa(f"AbaDebrum{i}", (0.4, 0.026, 0.012), (0, 0.11, 0.025), mt["chapeu_debrum"], aba, (-32, 0, 0),
                desloc=(0, 0, 0.033))


def cabeca(mt, tronco):
    # Cabeça um pouco para a frente: quer olhar tudo de perto.
    pescoco = c.pivo("Cabeca", (0, 0, 0.56), tronco, (3, 0, 0))
    c.caixa("Rosto", (0.2, 0.23, 0.24), (0, 0, 0.12), mt["pele"], pescoco, bisel=0.04)
    c.caixa("Nariz", (0.036, 0.055, 0.055), (0, -0.115, 0.095), mt["pele"], pescoco)
    for lado in (-1, 1):
        c.caixa(f"Orelha{lado}", (0.03, 0.05, 0.06), (0.103 * lado, 0.01, 0.115), mt["pele"], pescoco)
        c.caixa(f"Olho{lado}", (0.035, 0.01, 0.03), (0.047 * lado, -0.112, 0.13), mt["olho"], pescoco)
        c.caixa(f"Sobrancelha{lado}", (0.046, 0.012, 0.013), (0.047 * lado, -0.112, 0.165), mt["cabelo"], pescoco)
        c.caixa(f"CantoBoca{lado}", (0.012, 0.01, 0.012), (0.03 * lado, -0.1135, 0.056), mt["boca"], pescoco)
    c.caixa("Boca", (0.045, 0.01, 0.012), (0, -0.114, 0.05), mt["boca"], pescoco)
    c.caixa("BocaAberta", (0.024, 0.01, 0.026), (0, -0.114, 0.047), mt["boca"], pescoco)
    # Cabelo comprido puxado para trás, preso na nuca com a fita (rabicho).
    c.caixa("CabeloTopo", (0.215, 0.235, 0.06), (0, 0.01, 0.225), mt["cabelo"], pescoco, bisel=0.02)
    for lado in (-1, 1):
        c.caixa(f"CabeloLado{lado}", (0.03, 0.15, 0.12), (0.1 * lado, 0.03, 0.15), mt["cabelo"], pescoco)
    c.caixa("CabeloNuca", (0.2, 0.06, 0.15), (0, 0.09, 0.13), mt["cabelo"], pescoco, bisel=0.015)
    c.caixa("Rabicho", (0.05, 0.05, 0.17), (0, 0.13, 0.04), mt["cabelo"], pescoco, (22, 0, 0), bisel=0.015)
    c.caixa("Fita", (0.075, 0.035, 0.03), (0, 0.125, 0.11), mt["fita"], pescoco, (22, 0, 0))
    tricornio(mt, pescoco)
    return pescoco


def montar(mt):
    raiz = c.pivo("Baltazar")
    quadril = c.pivo("Quadril", (0, 0, 0.83), raiz)
    perna("PernaDir", -1, mt, quadril, -2, 3)
    perna("PernaEsq", +1, mt, quadril, 2, 2)
    # Tronco direito, quase sem inclinação: cerimonioso.
    tronco = c.pivo("Tronco", (0, 0, 0), quadril, (1, 0, 0))
    c.caixa("Bacia", (0.28, 0.15, 0.15), (0, 0, 0.0), mt["calcoes"], tronco, bisel=0.03)
    # Casaca aberta até o meio da coxa, mais larga embaixo. Na frente, a
    # abertura mostra o colete (com os botões de latão) e os calções.
    c.cone("Casaca", 0.238, 0.21, 0.6, (0, 0, 0.17), mt["casaca"], tronco, lados=8, achatar=0.6)
    c.caixa("GolaCasaca", (0.3, 0.15, 0.05), (0, 0.01, 0.475), mt["casaca_escura"], tronco, bisel=0.015)
    c.caixa("AberturaColete", (0.12, 0.02, 0.36), (0, -0.135, 0.28), mt["colete"], tronco)
    c.caixa("AberturaCalcoes", (0.11, 0.02, 0.16), (0, -0.14, -0.05), mt["calcoes"], tronco)
    for i, z in enumerate((0.4, 0.33, 0.26, 0.19)):
        c.caixa(f"Botao{i}", (0.016, 0.012, 0.016), (0, -0.147, z), mt["latao"], tronco)
    for lado in (-1, 1):
        c.caixa(f"Lapela{lado}", (0.035, 0.02, 0.5), (0.075 * lado, -0.138, 0.2), mt["casaca_escura"], tronco)
        c.caixa(f"BolsoCasaca{lado}", (0.1, 0.015, 0.035), (0.14 * lado, -0.13, 0.0), mt["casaca_escura"], tronco)
    c.caixa("Remendo", (0.075, 0.012, 0.075), (0.15, -0.128, -0.07), mt["remendo"], tronco, (0, 0, 0))
    # Camisa de linho aberta no pescoço.
    c.caixa("Camisa", (0.1, 0.03, 0.08), (0, -0.118, 0.47), mt["linho"], tronco)
    c.cone("GolaCamisa", 0.07, 0.065, 0.06, (0, 0, 0.52), mt["linho"], tronco, lados=6)
    c.cone("Pescoco", 0.048, 0.048, 0.1, (0, 0, 0.54), mt["pele"], tronco, lados=6)
    # Bandoleira de couro do ombro esquerdo ao quadril direito, na frente e
    # atrás, e a luneta de latão pendurada no quadril direito.
    for nome, y in (("BandoleiraFrente", -0.142), ("BandoleiraCostas", 0.142)):
        c.caixa(nome, (0.04, 0.012, 0.62), (-0.01, y, 0.2), mt["couro"], tronco, (0, 36, 0))
    luneta = c.pivo("Luneta", (-0.215, 0.05, -0.04), tronco, (68, 0, 0))
    c.cone("LunetaCorpo", 0.032, 0.026, 0.3, (0, 0, 0), mt["latao"], luneta, lados=6)
    c.cone("LunetaAnelFrente", 0.035, 0.035, 0.03, (0, 0, -0.14), mt["latao_escuro"], luneta, lados=6)
    c.cone("LunetaAnelMeio", 0.03, 0.03, 0.02, (0, 0, 0.03), mt["latao_escuro"], luneta, lados=6)
    braco("BracoDir", -1, mt, tronco, -2, -12, anel=True)
    braco("BracoEsq", +1, mt, tronco, 3, -10)
    cabeca(mt, tronco)
    return raiz


# ---------------------------------------------------------------------------
# Retratos (caixa de diálogo)
# ---------------------------------------------------------------------------
#
# Enquadramento do comum.py (renderizar_retrato). Três expressões:
#   normal     boca reta, sobrancelhas retas: a seriedade cerimoniosa;
#   encantado  sorriso (boca larga, cantos para cima) e sobrancelhas lá em
#              cima: tudo em 3026 é um milagre a estudar;
#   aflito     boca aberta e sobrancelhas levantadas no meio: o medo do
#              castigo, a hora em que ele solta o latim.

EXPRESSOES = ("normal", "encantado", "aflito")


def expressao(qual):
    boca = bpy.data.objects["Boca"]
    boca.hide_render = qual == "aflito"
    boca.scale = (1.3, 1, 1) if qual == "encantado" else (1, 1, 1)
    bpy.data.objects["BocaAberta"].hide_render = qual != "aflito"
    for lado in (-1, 1):
        bpy.data.objects[f"CantoBoca{lado}"].hide_render = qual != "encantado"
        sob = bpy.data.objects[f"Sobrancelha{lado}"]
        altura, giro = {"normal": (0.165, 0), "encantado": (0.178, 0), "aflito": (0.17, -16 * lado)}[qual]
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
    c.usar_colecao("Baltazar")
    raiz = montar(mt)
    c.achatar_sombra("Rosto")
    c.gerar_em_pe("baltazar", raiz, materiais, MAX_CORES, EXPRESSOES, expressao, esconder_boca, passo=PASSO)


main()
