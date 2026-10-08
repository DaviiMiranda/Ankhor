# gerar_gabriel.py — modela o Gabriel no Blender, por código, e renderiza
# os sprites de jogo (frente, 3/4, lado e costas) e a folha de referência.
#
# ATENÇÃO: desde 2026-10-07 os sprites do Gabriel que o jogo usa saem do
# pixelar_gabriel.py (pixel art feita a partir das referências em
# gabriel_referencia/). Este script fica como o modelo 3D do Gabriel; rodar
# ele sobrescreve os sprites novos. Ver docs/decisoes.md.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_gabriel.py
#
# O que sai:
#   assets/sprites/personagens/gabriel/gabriel_lado.png        sprites de jogo, 96 x 112 (2x):
#   assets/sprites/personagens/gabriel/gabriel_frente.png        de lado (olhando para a direita),
#   assets/sprites/personagens/gabriel/gabriel_tres_quartos.png  de frente, de 3/4 (virado para a
#   assets/sprites/personagens/gabriel/gabriel_costas.png        direita), de costas e de 3/4
#   assets/sprites/personagens/gabriel/gabriel_tres_quartos_costas.png   de costas
#   assets/sprites/personagens/gabriel/gabriel_andar_<vista>.png   caminhada: 12 quadros de 96 x 112
#                                                                 lado a lado, um arquivo por vista
#   assets/sprites/personagens/gabriel/gabriel_parado_<vista>.png  parado respirando: 8 quadros
#   assets/sprites/personagens/gabriel/gabriel_referencia.png  frente, 3/4, lado e costas, 128 px
#   assets/sprites/personagens/gabriel/gabriel_retrato_<expressão>.png  80 x 80: rosto e ombros
#                                                                 para a caixa de diálogo (normal,
#                                                                 surpreso, preocupado)
#   assets/modelagem/personagens/gabriel.blend                 o modelo, para abrir e mexer
#
# Quem é (docs/gdd.md, item 3): aluno comum, cansado, que só queria passar
# nas provas. Pegou no sono estudando na Biblioteca na véspera da semana de
# provas e acordou mil anos depois — dormindo, não envelheceu. Então o
# visual é o de um estudante numa noite de estudo: moletom, calça jeans,
# tênis e mochila. Nada de herói: ombros caídos e cabeça um pouco baixa.
#
# Cores: o moletom é vermelho-tijolo de propósito. Os cenários do jogo são
# verdes (mato), bege (areia), cinza (concreto) e o escuro frio dos subsolos; um
# tom quente e contrário a eles faz o jogador achar o Gabriel na tela.
#
# Modelagem: só primitivas (caixas, cones, esferas), agora com DETALHE 3 e
# sombreamento suave (ver comum.py): cones de 18 a 24 lados, quinas
# arredondadas e a luz deslizando pelas curvas. A silhueta continua sendo o
# que importa (cabelo arrepiado, capuz nas costas, a mochila), mas com mais
# gomos ela fica redonda, e os detalhes pequenos (cordões do capuz, cadarço,
# zíper e fivelas da mochila, sobrancelhas) aparecem na folha de referência
# e dão um pixel a mais de leitura no sprite de jogo.

import math
import os
import sys

sys.dont_write_bytecode = True   # não criar a pasta __pycache__ ao importar o comum.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as c  # noqa: E402  (precisa vir depois do sys.path)
import numpy as np  # noqa: E402
import bpy  # noqa: E402

PASTA_SAIDA = os.path.join(c.PASTA_SPRITES, "gabriel")
ARQUIVO_BLEND = os.path.join(c.PASTA_SCRIPT, "gabriel.blend")
MAX_CORES = 40   # tamanho máximo da paleta do Gabriel
DETALHE = 3      # gomos x3 e quinas arredondadas (comum.DETALHE)
# Resolução dobrada (96 x 112 por quadro, escala 0,5 no Godot), as cinco
# vistas de jogo e os quadros das animações são os mesmos de todos os
# personagens em pé: ficam no comum.py (item 7).


def criar_materiais():
    m = c.Materiais()
    return m, {
        "pele": m.novo("pele", "#b98260"),
        "cabelo": m.novo("cabelo", "#3a2c24"),
        "moletom": m.novo("moletom", "#a4453b"),
        "moletom_escuro": m.novo("moletom_escuro", "#7a3531"),
        "jeans": m.novo("jeans", "#40537a"),
        "tenis": m.novo("tenis", "#d3cfc4"),
        "sola": m.novo("sola", "#4d4d57"),
        "mochila": m.novo("mochila", "#556650"),
        "mochila_escura": m.novo("mochila_escura", "#3a4639"),
        # Detalhes de 1 px: cor chapada (modo 'plano'), sem sombreamento.
        "olho": m.novo("olho", "#1c1822", "plano"),
        "olheira": m.novo("olheira", "#8c5a48", "plano"),   # noite sem dormir
        "cordao": m.novo("cordao", "#d8d1c3"),
        "boca": m.novo("boca", "#5e3029", "plano"),
        "fivela": m.novo("fivela", "#2a2f2a"),
    }


def perna(nome, lado, mt, quadril, giro_coxa, giro_joelho):
    """Perna pendurada na junta do quadril. lado = -1 (direita dele) ou +1."""
    junta = c.pivo(f"{nome}Quadril", (0.095 * lado, 0.0, 0.0), quadril, (giro_coxa, 0, 0))
    c.membro(f"{nome}Coxa", 0.085, 0.066, 0.41, mt["jeans"], junta)
    joelho = c.pivo(f"{nome}Joelho", (0, 0, -0.41), junta, (giro_joelho, 0, 0))
    c.membro(f"{nome}Canela", 0.066, 0.056, 0.37, mt["jeans"], joelho)
    # Tênis: cabedal claro + sola escura, com a ponta para a frente (-Y).
    tornozelo = c.pivo(f"{nome}Tornozelo", (0, 0, -0.37), joelho, (-giro_coxa - giro_joelho, 0, 0))
    c.caixa(f"{nome}Tenis", (0.115, 0.26, 0.075), (0, -0.045, -0.05), mt["tenis"], tornozelo, bisel=0.02)
    c.caixa(f"{nome}Cadarco", (0.07, 0.1, 0.012), (0, -0.07, -0.012), mt["sola"], tornozelo, (-12, 0, 0))
    c.cone(f"{nome}Bainha", 0.06, 0.06, 0.035, (0, 0, -0.35), mt["jeans"], joelho, lados=6)
    c.caixa(f"{nome}Sola", (0.12, 0.275, 0.028), (0, -0.045, -0.086), mt["sola"], tornozelo)


def braco(nome, lado, mt, tronco, abertura, giro_ombro, giro_cotovelo):
    """Braço: manga do moletom (duas partes) e a mão."""
    ombro = c.pivo(f"{nome}Ombro", (0.235 * lado, 0.0, 0.47), tronco, (giro_ombro, abertura * lado, 0))
    c.membro(f"{nome}Braco", 0.068, 0.058, 0.30, mt["moletom"], ombro)
    cotovelo = c.pivo(f"{nome}Cotovelo", (0, 0, -0.30), ombro, (giro_cotovelo, 0, 0))
    c.membro(f"{nome}Antebraco", 0.058, 0.052, 0.24, mt["moletom"], cotovelo)
    c.cone(f"{nome}Punho", 0.054, 0.054, 0.035, (0, 0, -0.245), mt["moletom_escuro"], cotovelo, lados=6)
    c.caixa(f"{nome}Mao", (0.06, 0.085, 0.10), (0, 0, -0.31), mt["pele"], cotovelo, bisel=0.02)


def montar(mt):
    raiz = c.pivo("Gabriel")
    # Quadril a 0,88 m do chão. Leve inclinação do tronco para a frente:
    # cansaço, não curvatura de monstro (essa fica para o Vigia).
    quadril = c.pivo("Quadril", (0, 0, 0.88), raiz)
    perna("PernaDir", -1, mt, quadril, -3, 4)
    perna("PernaEsq", +1, mt, quadril, 3, 2)

    tronco = c.pivo("Tronco", (0, 0, 0), quadril, (4, 0, 0))
    c.caixa("Bacia", (0.30, 0.15, 0.16), (0, 0, 0.0), mt["jeans"], tronco, bisel=0.03)
    # Moletom: um bloco levemente mais largo em cima (ombros) e a barra.
    c.cone("Moletom", 0.215, 0.228, 0.54, (0, 0, 0.25), mt["moletom"], tronco, lados=8, achatar=0.58)
    c.cone("MoletomBarra", 0.222, 0.222, 0.07, (0, 0, 0.0), mt["moletom_escuro"], tronco, lados=8, achatar=0.60)
    c.caixa("Bolso", (0.24, 0.02, 0.11), (0, -0.128, 0.12), mt["moletom_escuro"], tronco)
    # Capuz caído nas costas: faz um "calombo" atrás do pescoço.
    c.caixa("Capuz", (0.28, 0.12, 0.13), (0, 0.10, 0.55), mt["moletom_escuro"], tronco, (-25, 0, 0), bisel=0.035)
    c.cone("Pescoco", 0.05, 0.05, 0.10, (0, 0, 0.58), mt["pele"], tronco, lados=6)
    # Cordões do capuz, pendurados na gola, um de cada lado do zíper.
    for lado in (-1, 1):
        c.caixa(f"Cordao{lado}", (0.012, 0.012, 0.16), (0.035 * lado, -0.13, 0.45), mt["cordao"], tronco, (0, 4 * lado, 0))
        c.caixa(f"Ponteira{lado}", (0.016, 0.016, 0.02), (0.037 * lado, -0.132, 0.37), mt["fivela"], tronco)

    # Mochila nas costas (alças por cima dos ombros).
    c.caixa("Mochila", (0.31, 0.16, 0.40), (0, 0.205, 0.30), mt["mochila"], tronco, (-4, 0, 0), bisel=0.04)
    c.caixa("MochilaBolso", (0.25, 0.06, 0.17), (0, 0.29, 0.18), mt["mochila_escura"], tronco, bisel=0.02)
    c.caixa("MochilaZiper", (0.2, 0.012, 0.012), (0, 0.322, 0.25), mt["fivela"], tronco)
    c.caixa("MochilaAlca", (0.08, 0.03, 0.035), (0, 0.25, 0.52), mt["mochila_escura"], tronco, bisel=0.01)
    for lado in (-1, 1):
        c.caixa(f"Alca{lado}Cima", (0.05, 0.26, 0.03), (0.11 * lado, 0.0, 0.535), mt["mochila_escura"], tronco)
        c.caixa(f"Alca{lado}Frente", (0.05, 0.025, 0.30), (0.11 * lado, -0.13, 0.38), mt["mochila_escura"], tronco)
        c.caixa(f"Fivela{lado}", (0.055, 0.03, 0.03), (0.11 * lado, -0.14, 0.24), mt["fivela"], tronco)

    braco("BracoDir", -1, mt, tronco, 7, -2, -8)
    braco("BracoEsq", +1, mt, tronco, 7, 4, -12)

    # Cabeça um pouco baixa (cansado).
    pescoco = c.pivo("Cabeca", (0, 0, 0.60), tronco, (5, 0, 0))
    c.caixa("Rosto", (0.21, 0.23, 0.25), (0, 0, 0.125), mt["pele"], pescoco, bisel=0.04)
    c.caixa("Nariz", (0.035, 0.05, 0.05), (0, -0.115, 0.10), mt["pele"], pescoco)
    for lado in (-1, 1):
        c.caixa(f"Orelha{lado}", (0.03, 0.05, 0.06), (0.105 * lado, 0.01, 0.12), mt["pele"], pescoco)
        c.caixa(f"Olho{lado}", (0.035, 0.01, 0.03), (0.048 * lado, -0.112, 0.135), mt["olho"], pescoco)
        c.caixa(f"Olheira{lado}", (0.04, 0.01, 0.014), (0.048 * lado, -0.111, 0.112), mt["olheira"], pescoco)
        c.caixa(f"Sobrancelha{lado}", (0.045, 0.012, 0.013), (0.048 * lado, -0.112, 0.168), mt["cabelo"], pescoco, (0, 6 * lado, 0))
    # Boca: só aparece nos retratos (no sprite de 48 px ela seria um risco
    # escuro no queixo). A aberta é a do "surpreso".
    c.caixa("Boca", (0.045, 0.01, 0.012), (0, -0.114, 0.052), mt["boca"], pescoco)
    c.caixa("BocaAberta", (0.024, 0.01, 0.026), (0, -0.114, 0.05), mt["boca"], pescoco)
    # Cabelo: uma "tampa", a nuca e tufos arrepiados (de quem deitou a
    # cabeça em cima do livro).
    c.caixa("CabeloTopo", (0.225, 0.245, 0.075), (0, 0.005, 0.235), mt["cabelo"], pescoco, bisel=0.025)
    c.caixa("CabeloNuca", (0.225, 0.08, 0.17), (0, 0.085, 0.17), mt["cabelo"], pescoco, bisel=0.02)
    for lado in (-1, 1):
        c.caixa(f"CabeloLado{lado}", (0.03, 0.14, 0.09), (0.105 * lado, 0.04, 0.20), mt["cabelo"], pescoco)
    for i, (x, y, rx, ry) in enumerate([(-0.06, -0.09, -30, -15), (0.02, -0.10, -40, 10),
                                         (0.07, -0.06, -20, 25), (-0.05, -0.02, -10, -20)]):
        c.caixa(f"Tufo{i}", (0.06, 0.05, 0.07), (x, y, 0.265), mt["cabelo"], pescoco, (rx, ry, 0))
    return raiz


# ---------------------------------------------------------------------------
# Caminhada e respiração
# ---------------------------------------------------------------------------
#
# As poses estão no comum.py (pose_andar e pose_parado), com as mesmas
# vistas e tamanhos para todos os personagens em pé. Os valores padrão de
# lá são os do Gabriel: passo cansado, braço balançando pouco, e a
# respiração lenta com a cabeça pendendo atrasada em relação ao peito.


# ---------------------------------------------------------------------------
# Retratos (caixa de diálogo)
# ---------------------------------------------------------------------------
#
# Enquadramento no comum.py (renderizar_retrato), igual para todos: 80 x 80
# px (mostrados em 40 x 40 na caixa), câmera reta na altura do rosto,
# virado 24 graus para a direita (para o texto da caixa). Três expressões,
# feitas com a boca e as sobrancelhas, porque num retrato de 40 px 1 pixel
# já muda o rosto:
#   normal      boca reta, sobrancelhas no lugar (o cansaço de sempre);
#   surpreso    boca aberta, sobrancelhas lá em cima;
#   preocupado  boca reta, sobrancelhas levantadas no meio (inclinadas).

EXPRESSOES = ("normal", "surpreso", "preocupado")


def expressao(qual):
    bpy.data.objects["Boca"].hide_render = qual == "surpreso"
    bpy.data.objects["BocaAberta"].hide_render = qual != "surpreso"
    for lado in (-1, 1):
        sob = bpy.data.objects[f"Sobrancelha{lado}"]
        sob.location.z = {"normal": 0.168, "surpreso": 0.18, "preocupado": 0.173}[qual]
        sob.rotation_euler = (0, math.radians({"normal": 6, "surpreso": 0, "preocupado": -16}[qual] * lado), 0)


def renderizar_retratos(cam, raiz, materiais):
    retratos = {}
    for qual in EXPRESSOES:
        expressao(qual)
        retratos[qual] = c.renderizar_retrato(cam, raiz, materiais)
    expressao("normal")
    bpy.data.objects["Boca"].hide_render = True
    bpy.data.objects["BocaAberta"].hide_render = True
    return retratos


def main():
    c.DETALHE = DETALHE
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = criar_materiais()
    c.usar_colecao("Gabriel")
    raiz = montar(mt)
    c.achatar_sombra("Rosto")
    bpy.data.objects["Boca"].hide_render = True
    bpy.data.objects["BocaAberta"].hide_render = True
    cam = c.criar_camera()
    c.criar_luzes()
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    # Sprites de jogo, um para cada direção em que ele anda (o scripts/
    # personagens/gabriel.gd escolhe qual mostrar), a caminhada e a
    # respiração em cada vista.
    jogo = c.renderizar_vistas_jogo(cam, raiz, materiais, "gabriel")
    parado = c.guardar_pose()
    andar = c.renderizar_ciclo(cam, raiz, materiais, lambda fase: c.pose_andar(parado, fase),
                               c.QUADROS_ANDAR, "gabriel andar")
    c.restaurar_pose(parado)
    respirar = c.renderizar_ciclo(cam, raiz, materiais, lambda fase: c.pose_parado(parado, fase),
                                  c.QUADROS_PARADO, "gabriel parado")
    c.restaurar_pose(parado)

    # Folha de referência: frente, 3/4, lado e costas, em 128 px.
    vistas = []
    for angulo in (0, 35, 90, 180):
        img, ind, _ = c.renderizar_vista(cam, raiz, materiais, angulo, c.QUADRO_REF, c.PX_POR_M_REF, c.PE_REF_PX)
        vistas.append(c.contorno(img, ind, materiais))

    # Uma paleta só para tudo do Gabriel (sprites e referência). Ela é
    # calculada com o sprite de lado e a referência, e as outras imagens
    # só usam essa paleta: assim as cores de antes não mudam.
    vistas, paleta = c.unificar_paleta([jogo["lado"]] + vistas, materiais, MAX_CORES)
    vistas = vistas[1:]
    c.salvar_sprites_jogo(PASTA_SAIDA, "gabriel", paleta, jogo, andar, respirar)
    retratos = renderizar_retratos(cam, raiz, materiais)
    for (qual, img) in zip(retratos, c.aplicar_paleta(list(retratos.values()), paleta)):
        c.salvar_png(img, os.path.join(PASTA_SAIDA, f"gabriel_retrato_{qual}.png"))
    c.salvar_png(c.montar_folha([vistas, list(retratos.values())]), os.path.join(PASTA_SAIDA, "gabriel_referencia.png"))
    print("[gabriel] paleta:", " ".join(c.rgb_para_hex(np.array(cor) / 255) for cor in paleta))

    c.salvar_blend(ARQUIVO_BLEND, raiz)
    print("[gabriel] pronto")


main()
