# gerar_zane.py — modela o Zane (2123) no Blender, por código, e renderiza
# os mesmos sprites do Gabriel: as cinco vistas de jogo, a caminhada e a
# respiração em cada uma, os retratos da caixa de diálogo e a folha de
# referência.
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
#   zane_retrato_<expressão>.png 80 x 80: rosto e ombros para a caixa de
#                                diálogo (normal, confiante, assustado)
#   zane_referencia.png          frente, 3/4, lado e costas, e os retratos
#   assets/modelagem/personagens/zane.blend   o modelo, para abrir e mexer
#
# Quem é (docs/historia/personagens/zane.md): rapaz de uns 20 anos, de 2123,
# quando a Unifor já era um polo de IA. Tem implantes cibernéticos, entende
# a tecnologia da Âncora melhor que ninguém e é o último a chegar em 3026.
# Confiante, direto, elétrico, e mais assustado do que admite.
#
# O visual conta isso:
#   - implantes à vista: o braço direito inteiro é uma prótese de metal com
#     linhas de luz ciano, o olho direito é um implante que brilha, uma placa
#     de metal na têmpora e uma porta de conexão na nuca. O ciano é o mesmo
#     da interface holográfica dos áudios dele (a ficha, item 5);
#   - roupa de um futuro que ninguém reconhece: jaqueta curta e técnica,
#     amarelo-ácido com painéis grafite, zíper na diagonal e gola alta até o
#     queixo, a manga do braço de metal cortada no ombro, camiseta preta
#     comprida aparecendo embaixo, calça larga com tiras, botas de sola
#     branca grossa com um friso de luz;
#   - cabelo raspado dos lados e o topo descolorido, quase branco, num
#     topete para cima: a silhueta mais alta e pontuda do grupo;
#   - a cor dele é o amarelo-ácido: o Gabriel é vermelho, a Clarice é
#     verde-azulado, e nenhum cenário do jogo tem esse amarelo. Ele destoa
#     de todo mundo, como a ficha pede (é o único que veio depois do Gabriel);
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
import numpy as np  # noqa: E402
import bpy  # noqa: E402

PASTA_SAIDA = os.path.join(c.PASTA_SPRITES, "zane")
ARQUIVO_BLEND = os.path.join(c.PASTA_SCRIPT, "zane.blend")
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
        "pele": m.novo("pele", "#cf9f80"),
        "cabelo": m.novo("cabelo", "#e3d9bd"),          # topo descolorido
        "cabelo_raiz": m.novo("cabelo_raiz", "#3a302b"),  # lados raspados e sobrancelhas
        "jaqueta": m.novo("jaqueta", "#dcc43c"),
        "jaqueta_escura": m.novo("jaqueta_escura", "#a8902a"),
        "grafite": m.novo("grafite", "#30323b"),
        "camiseta": m.novo("camiseta", "#1c1d24"),
        "calca": m.novo("calca", "#3b3e4a"),
        "bota": m.novo("bota", "#2b2c33"),
        "sola": m.novo("sola", "#d9d8d0"),
        "metal": m.novo("metal", "#8e97a3", aspereza=0.5),
        "metal_escuro": m.novo("metal_escuro", "#4a505b", aspereza=0.5),
        # Luz dos implantes e o olho de implante: emitem, cor sempre chapada.
        "luz": m.novo("luz", "#56f0ff", "brilho"),
        "olho_implante": m.novo("olho_implante", "#9ff8ff", "brilho"),
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
        olho = mt["olho_implante"] if lado < 0 else mt["olho"]
        c.caixa(f"Olho{lado}", (0.035, 0.01, 0.03), (0.048 * lado, -0.112, 0.135), olho, pescoco)
        c.caixa(f"Sobrancelha{lado}", (0.048, 0.012, 0.013), (0.048 * lado, -0.112, 0.172), mt["cabelo_raiz"], pescoco)
    # Boca: só nos retratos, como a do Gabriel. O canto é o sorriso de lado
    # do "confiante"; a aberta é a do "assustado".
    c.caixa("Boca", (0.05, 0.01, 0.012), (0, -0.114, 0.05), mt["boca"], pescoco)
    c.caixa("CantoBoca", (0.018, 0.01, 0.012), (0.04, -0.1135, 0.062), mt["boca"], pescoco, (0, -30, 0))
    c.caixa("BocaAberta", (0.026, 0.01, 0.028), (0, -0.114, 0.048), mt["boca"], pescoco)
    # Implantes da cabeça: placa na têmpora direita com dois pontos de luz,
    # um risco de metal saindo do olho de implante, e a porta na nuca.
    c.caixa("PlacaTempora", (0.022, 0.09, 0.07), (-0.112, 0.0, 0.14), mt["metal"], pescoco, bisel=0.008)
    for i, y in enumerate((-0.022, 0.018)):
        c.caixa(f"LuzTempora{i}", (0.01, 0.016, 0.014), (-0.124, y, 0.15), mt["luz"], pescoco)
    c.caixa("RiscoOlho", (0.04, 0.01, 0.008), (-0.08, -0.111, 0.112), mt["metal_escuro"], pescoco, (0, -20, 0))
    c.caixa("PortaNuca", (0.05, 0.022, 0.06), (0, 0.112, 0.06), mt["metal_escuro"], pescoco, bisel=0.008)
    c.caixa("LuzNuca", (0.022, 0.01, 0.014), (0, 0.124, 0.065), mt["luz"], pescoco)
    # Cabelo: raspado dos lados e na nuca (a cor da raiz, bem rente), e o
    # topo descolorido, mais estreito que a cabeça, subindo num topete.
    for lado in (-1, 1):
        c.caixa(f"Raspado{lado}", (0.02, 0.17, 0.11), (0.104 * lado, 0.03, 0.18), mt["cabelo_raiz"], pescoco)
    c.caixa("RaspadoNuca", (0.2, 0.03, 0.11), (0, 0.105, 0.175), mt["cabelo_raiz"], pescoco)
    c.caixa("CabeloTopo", (0.17, 0.23, 0.07), (0, 0.01, 0.255), mt["cabelo"], pescoco, bisel=0.02)
    c.caixa("Topete", (0.15, 0.12, 0.11), (0.0, -0.06, 0.285), mt["cabelo"], pescoco, (-28, 0, 6), bisel=0.03)
    for i, (x, y, z, rx, ry) in enumerate([(-0.045, -0.02, 0.3, -20, -12), (0.03, 0.0, 0.305, -15, 14),
                                            (-0.01, 0.05, 0.29, 10, 0)]):
        c.caixa(f"Ponta{i}", (0.05, 0.05, 0.08), (x, y, z), mt["cabelo"], pescoco, (rx, ry, 0))
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
    c.cone("Gola", 0.105, 0.095, 0.1, (0, 0, 0.585), mt["grafite"], tronco, lados=8)
    c.cone("Pescoco", 0.05, 0.05, 0.1, (0, 0, 0.6), mt["pele"], tronco, lados=6)
    # Ombreira no ombro esquerdo (o do braço de carne), e uma faixa de luz no
    # peito do mesmo lado.
    c.caixa("Ombreira", (0.12, 0.2, 0.05), (0.2, 0.0, 0.55), mt["jaqueta_escura"], tronco, (0, -18, 0), bisel=0.015)
    c.caixa("FaixaLuz", (0.07, 0.01, 0.012), (0.1, -0.143, 0.47), mt["luz"], tronco)
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


def renderizar_retratos(cam, raiz, materiais):
    retratos = {}
    for qual in EXPRESSOES:
        expressao(qual)
        retratos[qual] = c.renderizar_retrato(cam, raiz, materiais)
    expressao("normal")
    esconder_boca()
    return retratos


def main():
    c.DETALHE = DETALHE
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = criar_materiais()
    c.usar_colecao("Zane")
    raiz = montar(mt)
    c.achatar_sombra("Rosto")
    expressao("normal")
    esconder_boca()
    cam = c.criar_camera()
    c.criar_luzes()
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    # Sprites de jogo: as cinco vistas, a caminhada e a respiração.
    jogo = c.renderizar_vistas_jogo(cam, raiz, materiais, "zane")
    parado = c.guardar_pose()
    andar = c.renderizar_ciclo(cam, raiz, materiais, lambda fase: c.pose_andar(parado, fase, **PASSO),
                               c.QUADROS_ANDAR, "zane andar")
    c.restaurar_pose(parado)
    respirar = c.renderizar_ciclo(cam, raiz, materiais, lambda fase: c.pose_parado(parado, fase, **RESPIRAR),
                                  c.QUADROS_PARADO, "zane parado")
    c.restaurar_pose(parado)

    # Folha de referência: frente, 3/4, lado e costas, em 128 px.
    vistas = []
    for angulo in (0, 35, 90, 180):
        img, ind, _ = c.renderizar_vista(cam, raiz, materiais, angulo, c.QUADRO_REF, c.PX_POR_M_REF, c.PE_REF_PX)
        vistas.append(c.contorno(img, ind, materiais))
    retratos = renderizar_retratos(cam, raiz, materiais)

    # Uma paleta só para tudo do Zane, calculada com o sprite de lado, a
    # referência e os retratos; as animações só usam essa paleta.
    todas = [jogo["lado"]] + vistas + list(retratos.values())
    convertidas, paleta = c.unificar_paleta(todas, materiais, MAX_CORES)
    vistas = convertidas[1:5]
    retratos = dict(zip(retratos.keys(), convertidas[5:]))
    c.salvar_sprites_jogo(PASTA_SAIDA, "zane", paleta, jogo, andar, respirar)
    for qual, img in retratos.items():
        c.salvar_png(img, os.path.join(PASTA_SAIDA, f"zane_retrato_{qual}.png"))
    c.salvar_png(c.montar_folha([vistas, list(retratos.values())]), os.path.join(PASTA_SAIDA, "zane_referencia.png"))
    print("[zane] paleta:", " ".join(c.rgb_para_hex(np.array(cor) / 255) for cor in paleta))

    c.salvar_blend(ARQUIVO_BLEND, raiz)
    print("[zane] pronto")


main()
