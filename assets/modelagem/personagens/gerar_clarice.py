# gerar_clarice.py — modela a Clarice (1994) no Blender, por código, com a
# estação de trabalho dela no bunker, e renderiza os sprites, os retratos
# da caixa de diálogo e a folha de referência.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_clarice.py
#
# O que sai (em assets/sprites/personagens/clarice/):
#   clarice_digitando.png    8 quadros de 160 x 128 (resolução dobrada: o Godot
#                            mostra com escala 0,5), lado a lado: sentada de
#                            costas para a câmera, digitando nos terminais
#   clarice_virando.png      5 quadros: a cadeira girando até ela olhar para
#                            a esquerda (de onde o Gabriel chega)
#   clarice_olhando.png      6 quadros: virada para o Gabriel, respirando
#   clarice_retrato_normal.png, clarice_retrato_sorrindo.png, clarice_retrato_seria.png
#                            80 x 80: rosto e ombros, para a caixa de diálogo
#   clarice_<vista>.png      em pé, as mesmas vistas do Gabriel, 96 x 112:
#                            lado, frente, tres_quartos, costas e
#                            tres_quartos_costas
#   clarice_andar_<vista>.png    caminhada: 12 quadros de 96 x 112 lado a lado
#   clarice_parado_<vista>.png   parada respirando: 8 quadros
#   clarice_referencia.png   em pé (frente, 3/4, lado, costas), sentada
#                            (digitando e virada) e os retratos
#   assets/modelagem/personagens/clarice.blend   o modelo, para abrir e mexer
#
# Quem é (docs/historia/personagens/clarice.md): aluna de processamento de dados,
# puxada de uma madrugada de 1994 na Biblioteca. Está em 3026 há alguns
# dias, escondida no bunker perto do núcleo da Âncora, e foi a primeira a
# ver que as rotas dos robôs formam um grafo. Sarcástica, rápida, gíria
# dos anos 90.
#
# O visual conta isso:
#   - anos 90 de verdade: jaqueta corta-vento em blocos de cor (verde-
#     -azulado, roxo e branco), cabelo volumoso e cacheado preso no alto com
#     uma XUXINHA magenta, óculos grandes, fone de walkman de espuma laranja
#     no pescoço e o walkman no cós da calça, tênis branco de lona;
#   - a cor dela é o verde-azulado: o contrário do vermelho do Gabriel.
#     Lado a lado, o jogador acha cada um na tela sem pensar;
#   - meses no bunker: mangas arregaçadas, jaqueta gasta, a estação de
#     trabalho montada com o que achou (três monitores de tubo, teclado e
#     gabinete bege, o telefone bege com o fio enrolado por onde ela liga
#     para o campus, disquetes, caneca, adesivos nos monitores).
#
# A cena da estação é renderizada com a câmera um pouco inclinada para
# baixo (INCLINACAO graus), para aparecer o tampo da mesa e o teclado,
# como os objetos do cenário 2.5D. Os outros personagens usam a câmera
# reta; a diferença de escala na altura é cos(22°) = 0,93, quase nada.
#
# Modelagem: só primitivas (caixas, cones, esferas). A Clarice usa DETALHE 3
# e sombreamento suave, como o Gabriel (ver comum.py): cabelo com mais
# cachos redondos, quinas arredondadas. A estação de trabalho fica no
# detalhe normal de propósito: monitor de tubo, gabinete e mesa são caixas
# de verdade, e arredondar deixaria tudo com cara de plástico mole. Ver comum.py para o render em dois passes (luz e ID)
# e a paleta fixa.

import math
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comum as c  # noqa: E402
import numpy as np  # noqa: E402
import bpy  # noqa: E402

PASTA_SAIDA = os.path.join(c.PASTA_SPRITES, "clarice")
ARQUIVO_BLEND = os.path.join(c.PASTA_SCRIPT, "clarice.blend")
MAX_CORES = 56
RESOLUCAO = 2
DETALHE = 3
QUADRO_MESA = (80 * RESOLUCAO, 64 * RESOLUCAO)
PE_MESA_PX = 4 * RESOLUCAO
INCLINACAO = 22            # graus: câmera olhando um pouco para baixo
QUADRO_RETRATO = (40 * RESOLUCAO, 40 * RESOLUCAO)
PX_POR_M_RETRATO = 88 * RESOLUCAO      # o rosto ocupa quase o retrato inteiro
ALTURA_RETRATO_M = 1.5    # altura (em pé) que fica no meio do retrato
QUADROS_DIGITANDO = 8
QUADROS_OLHANDO = 6
GIROS_VIRANDO = (180, 211, 242, 273, 300)   # giro da cadeira em cada quadro
GIRO_OLHANDO = 305                          # 3/4 virada para a esquerda


class MateriaisClarice(c.Materiais):
    """Igual aos materiais do comum.py, com uma exceção: o brilho do cabelo.
    A rampa padrão puxa o tom mais claro para um branco frio, e num castanho
    escuro isso vira CINZA (parecia cabelo grisalho). Aqui o brilho do
    cabelo é o próprio castanho clareado (x 1,4), que continua quente."""

    def rampas(self):
        saida = super().rampas()
        for i, (nome, hexa, _, _) in enumerate(self.lista):
            if nome == "cabelo":
                saida[i][3] = np.clip(c.hex_para_rgb(hexa) * 1.4, 0, 1)
        return saida


def criar_materiais():
    m = MateriaisClarice()
    return m, {
        "pele": m.novo("pele", "#8d5c3f"),
        "cabelo": m.novo("cabelo", "#3d2116"),
        "xuxinha": m.novo("xuxinha", "#c63f8c"),
        "jaqueta": m.novo("jaqueta", "#2e8c88"),
        "jaqueta_roxo": m.novo("jaqueta_roxo", "#6a3e9e"),
        "jaqueta_branco": m.novo("jaqueta_branco", "#ddd6c4"),
        "camiseta": m.novo("camiseta", "#2b2a33"),
        "calca": m.novo("calca", "#2a2833"),
        "tenis": m.novo("tenis", "#e2ddd0"),
        "sola": m.novo("sola", "#9d968a"),
        "fone": m.novo("fone", "#3b3b46"),
        "espuma": m.novo("espuma", "#e07a2c"),
        "walkman": m.novo("walkman", "#b9b3a6"),
        "bege": m.novo("bege", "#cfc5a9"),
        "bege_escuro": m.novo("bege_escuro", "#9e9479"),
        "mesa": m.novo("mesa", "#5d5f66"),
        "mesa_tampo": m.novo("mesa_tampo", "#7b6a55"),
        "cadeira": m.novo("cadeira", "#33333d"),
        "metal": m.novo("metal", "#6f7680"),
        "cabo": m.novo("cabo", "#1f1f26"),
        "caneca": m.novo("caneca", "#b8483a"),
        "disquete_azul": m.novo("disquete_azul", "#3d5fa8"),
        "disquete_amarelo": m.novo("disquete_amarelo", "#d6b43a"),
        "papel": m.novo("papel", "#d8d2bd"),
        "adesivo_rosa": m.novo("adesivo_rosa", "#e5609f", "plano"),
        "adesivo_amarelo": m.novo("adesivo_amarelo", "#f0d148", "plano"),
        "tela": m.novo("tela", "#1f5c34", "brilho"),
        "texto_tela": m.novo("texto_tela", "#7cf09a", "brilho"),
        "led": m.novo("led", "#ff5a3a", "brilho"),
        "olho": m.novo("olho", "#1b1620", "plano"),
        "oculos": m.novo("oculos", "#1b1620", "plano"),
        "lente": m.novo("lente", "#b9d8e4", "plano"),
        "boca": m.novo("boca", "#5a2f27", "plano"),
    }


# ---------------------------------------------------------------------------
# A Clarice
# ---------------------------------------------------------------------------
#
# Um pouco mais baixa que o Gabriel (1,62 m contra 1,75 m). Os nomes das
# juntas seguem o gerar_gabriel.py (Quadril, Tronco, Cabeca, <lado>Ombro...),
# e o modelo é montado de frente para a câmera (-Y) em pé; as poses de
# sentada só giram juntas.


def perna(nome, lado, mt, quadril):
    junta = c.pivo(f"{nome}Quadril", (0.085 * lado, 0.0, 0.0), quadril)
    c.membro(f"{nome}Coxa", 0.080, 0.062, 0.39, mt["calca"], junta)
    joelho = c.pivo(f"{nome}Joelho", (0, 0, -0.39), junta)
    c.membro(f"{nome}Canela", 0.062, 0.050, 0.36, mt["calca"], joelho)
    tornozelo = c.pivo(f"{nome}Tornozelo", (0, 0, -0.36), joelho)
    c.caixa(f"{nome}Tenis", (0.10, 0.24, 0.07), (0, -0.04, -0.045), mt["tenis"], tornozelo, bisel=0.02)
    c.caixa(f"{nome}Biqueira", (0.10, 0.05, 0.05), (0, -0.14, -0.055), mt["sola"], tornozelo, bisel=0.01)
    c.caixa(f"{nome}Sola", (0.105, 0.25, 0.025), (0, -0.04, -0.082), mt["sola"], tornozelo)
    c.caixa(f"{nome}Cadarco", (0.06, 0.09, 0.012), (0, -0.07, -0.014), mt["sola"], tornozelo, (-12, 0, 0))


def braco(nome, lado, mt, tronco):
    """Manga da jaqueta arregaçada até o cotovelo: o antebraço é pele,
    com um relógio de 1 px no pulso esquerdo."""
    ombro = c.pivo(f"{nome}Ombro", (0.205 * lado, 0.0, 0.43), tronco, (0, 6 * lado, 0))
    c.membro(f"{nome}Braco", 0.068, 0.058, 0.27, mt["jaqueta"], ombro)
    c.cone(f"{nome}Faixa", 0.070, 0.070, 0.05, (0, 0, -0.08), mt["jaqueta_roxo"], ombro, lados=6)
    cotovelo = c.pivo(f"{nome}Cotovelo", (0, 0, -0.27), ombro)
    c.cone(f"{nome}Arregacado", 0.064, 0.064, 0.05, (0, 0, -0.02), mt["jaqueta_branco"], cotovelo, lados=6)
    c.membro(f"{nome}Antebraco", 0.045, 0.038, 0.23, mt["pele"], cotovelo)
    if lado > 0:
        c.cone(f"{nome}Relogio", 0.044, 0.044, 0.025, (0, 0, -0.20), mt["fone"], cotovelo, lados=6)
    c.caixa(f"{nome}Mao", (0.05, 0.075, 0.09), (0, 0, -0.28), mt["pele"], cotovelo, bisel=0.015)


def cabeca(mt, tronco):
    pescoco = c.pivo("Cabeca", (0, 0, 0.55), tronco)
    c.caixa("Rosto", (0.19, 0.21, 0.23), (0, 0, 0.115), mt["pele"], pescoco, bisel=0.04)
    c.caixa("Nariz", (0.03, 0.045, 0.045), (0, -0.105, 0.095), mt["pele"], pescoco)
    c.caixa("Boca", (0.05, 0.01, 0.012), (0, -0.103, 0.05), mt["boca"], pescoco)
    for lado in (-1, 1):
        c.caixa(f"Olho{lado}", (0.022, 0.006, 0.026), (0.045 * lado, -0.117, 0.122), mt["olho"], pescoco)
        # Óculos grandes: a lente clara por cima do olho e o aro escuro em volta.
        c.caixa(f"Lente{lado}", (0.062, 0.006, 0.05), (0.047 * lado, -0.112, 0.122), mt["lente"], pescoco)
        c.caixa(f"AroCima{lado}", (0.07, 0.01, 0.012), (0.047 * lado, -0.114, 0.152), mt["oculos"], pescoco)
        c.caixa(f"Sobrancelha{lado}", (0.048, 0.012, 0.013), (0.047 * lado, -0.108, 0.174), mt["cabelo"], pescoco)
        c.caixa(f"CantoBoca{lado}", (0.012, 0.01, 0.012), (0.03 * lado, -0.1035, 0.058), mt["boca"], pescoco)
        c.caixa(f"Haste{lado}", (0.01, 0.13, 0.012), (0.094 * lado, -0.05, 0.14), mt["oculos"], pescoco)
        c.caixa(f"Orelha{lado}", (0.025, 0.045, 0.055), (0.097 * lado, 0.01, 0.11), mt["pele"], pescoco)
    c.caixa("Ponte", (0.03, 0.01, 0.01), (0, -0.114, 0.135), mt["oculos"], pescoco)
    # Cabelo: volume cacheado em volta da cabeça (esferas facetadas), franja
    # e o rabo alto, preso com a xuxinha, que vira um "pompom" de cachos.
    c.caixa("CabeloTopo", (0.23, 0.25, 0.08), (0, 0.01, 0.235), mt["cabelo"], pescoco, bisel=0.03)
    c.caixa("Franja", (0.2, 0.05, 0.045), (0, -0.092, 0.218), mt["cabelo"], pescoco, (15, 0, 0), bisel=0.015)
    for lado in (-1, 1):
        c.esfera(f"Volume{lado}", 0.075, (0.1 * lado, 0.03, 0.15), mt["cabelo"], pescoco, escala=(0.8, 1.1, 1.2), seg=6, aneis=4)
        c.esfera(f"VolumeNuca{lado}", 0.07, (0.06 * lado, 0.09, 0.08), mt["cabelo"], pescoco, seg=6, aneis=4)
    c.cone("Xuxinha", 0.05, 0.05, 0.035, (0, 0.11, 0.25), mt["xuxinha"], pescoco, (-60, 0, 0), lados=8)
    cachos = [(0, 0.17, 0.3, 0.075), (-0.05, 0.2, 0.25, 0.06), (0.05, 0.2, 0.26, 0.06),
              (0, 0.23, 0.2, 0.055), (0.02, 0.15, 0.34, 0.05), (-0.06, 0.14, 0.31, 0.045),
              (0.07, 0.15, 0.3, 0.045), (-0.03, 0.25, 0.17, 0.045), (0.04, 0.24, 0.15, 0.04),
              (0, 0.2, 0.36, 0.04)]
    for i, (x, y, z, r) in enumerate(cachos):
        c.esfera(f"Cacho{i}", r, (x, y, z), mt["cabelo"], pescoco, seg=6, aneis=4)
    # Cachinhos soltos na frente das orelhas e na nuca.
    for lado in (-1, 1):
        c.esfera(f"Solto{lado}", 0.03, (0.105 * lado, -0.03, 0.07), mt["cabelo"], pescoco, escala=(0.7, 0.8, 1.4), seg=6, aneis=4)
    return pescoco


def montar_clarice(mt, pai):
    raiz = c.pivo("Clarice", (0, 0, 0), pai)
    quadril = c.pivo("Quadril", (0, 0, 0.83), raiz)
    perna("PernaDir", -1, mt, quadril)
    perna("PernaEsq", +1, mt, quadril)
    tronco = c.pivo("Tronco", (0, 0, 0), quadril)
    c.caixa("Bacia", (0.27, 0.15, 0.15), (0, 0, 0.0), mt["calca"], tronco, bisel=0.03)
    # Jaqueta corta-vento: corpo verde-azulado, faixa roxa no peito e uma
    # faixa branca embaixo dela (os blocos de cor de 1994), gola alta e o
    # zíper aberto mostrando a camiseta preta.
    c.cone("Jaqueta", 0.2, 0.215, 0.5, (0, 0, 0.24), mt["jaqueta"], tronco, lados=8, achatar=0.6)
    c.cone("FaixaRoxa", 0.212, 0.212, 0.1, (0, 0, 0.36), mt["jaqueta_roxo"], tronco, lados=8, achatar=0.62)
    c.cone("FaixaBranca", 0.214, 0.214, 0.035, (0, 0, 0.295), mt["jaqueta_branco"], tronco, lados=8, achatar=0.63)
    c.cone("Barra", 0.215, 0.215, 0.05, (0, 0, 0.0), mt["jaqueta_roxo"], tronco, lados=8, achatar=0.63)
    c.caixa("Camiseta", (0.06, 0.02, 0.14), (0, -0.126, 0.42), mt["camiseta"], tronco)
    # Zíper aberto (as duas carreiras de dentes, claras) e os bolsos.
    for lado in (-1, 1):
        c.caixa(f"Ziper{lado}", (0.01, 0.012, 0.36), (0.036 * lado, -0.128, 0.26), mt["jaqueta_branco"], tronco)
        c.caixa(f"Bolso{lado}", (0.07, 0.012, 0.012), (0.12 * lado, -0.124, 0.12), mt["jaqueta_roxo"], tronco, (0, 0, 0))
    # Um botton de carinha amarela no peito (o mesmo amarelo dos adesivos).
    c.cone("Botton", 0.022, 0.022, 0.01, (-0.1, -0.131, 0.26), mt["adesivo_amarelo"], tronco, (90, 0, 0), lados=8)
    c.caixa("Gola", (0.3, 0.14, 0.06), (0, 0.0, 0.5), mt["jaqueta_branco"], tronco, bisel=0.02)
    c.cone("Pescoco", 0.045, 0.045, 0.1, (0, 0, 0.54), mt["pele"], tronco, lados=6)
    # Fone de walkman caído no pescoço: o arco por trás e as espumas laranja
    # em cima dos ombros, com o fio descendo até o walkman no cós.
    c.caixa("FoneArco", (0.2, 0.025, 0.025), (0, 0.075, 0.55), mt["fone"], tronco)
    for lado in (-1, 1):
        c.esfera(f"Espuma{lado}", 0.045, (0.095 * lado, -0.03, 0.53), mt["espuma"], tronco, escala=(0.6, 1, 1), seg=6, aneis=4)
    c.caixa("Walkman", (0.1, 0.04, 0.13), (0.13, -0.1, 0.02), mt["walkman"], tronco, bisel=0.01)
    c.caixa("Fio", (0.008, 0.008, 0.45), (0.1, -0.115, 0.3), mt["cabo"], tronco, (0, 12, 0))
    braco("BracoDir", -1, mt, tronco)
    braco("BracoEsq", +1, mt, tronco)
    cabeca(mt, tronco)
    return raiz


# ---------------------------------------------------------------------------
# Estação de trabalho (fica parada; só a cadeira gira)
# ---------------------------------------------------------------------------
#
# Coordenadas da cena da estação (câmera olhando para +Y): a mesa encosta
# no fundo (y de 0,55 a 1,25) e a cadeira fica na frente dela (y = 0,22).
# O ponto (0, 0, 0) é o pé do sprite: no Godot, o nó da Clarice fica ali,
# e é por esse y que ela entra na ordem de desenho (y-sort).

MESA_Y = (0.55, 1.25)
MESA_X = (-0.62, 0.92)
TAMPO_Z = 0.74
CADEIRA_POS = (0.0, 0.22, 0.0)


def monitor(nome, pos, giro, mt, pai, largura=0.36):
    """Monitor de tubo (CRT): a caixa da tela, a traseira que afunila e o
    pé. A tela é verde-escura com linhas de texto claras (fósforo verde)."""
    base = c.pivo(nome, pos, pai, (0, 0, giro))
    alt = largura * 0.85
    c.caixa(f"{nome}Moldura", (largura, 0.07, alt), (0, 0, 0.1 + alt / 2), mt["bege"], base, bisel=0.015)
    c.cone(f"{nome}Tubo", largura * 0.42, largura * 0.62, 0.26, (0, 0.15, 0.1 + alt / 2), mt["bege_escuro"], base,
           (90, 0, 0), lados=4)
    c.caixa(f"{nome}Pe", (largura * 0.5, 0.2, 0.06), (0, 0.06, 0.03), mt["bege_escuro"], base)
    c.caixa(f"{nome}Pescoco", (0.08, 0.06, 0.05), (0, 0.06, 0.085), mt["bege_escuro"], base)
    tela_l, tela_a = largura * 0.78, alt * 0.72
    c.caixa(f"{nome}Tela", (tela_l, 0.01, tela_a), (0, -0.036, 0.1 + alt / 2), mt["tela"], base)
    for i in range(4):
        comp = tela_l * (0.35 + 0.15 * ((i * 7) % 4))
        z = 0.1 + alt / 2 + tela_a * 0.3 - i * tela_a * 0.2
        c.caixa(f"{nome}Linha{i}", (comp, 0.008, 0.012), (-tela_l / 2 + comp / 2 + 0.01, -0.042, z), mt["texto_tela"], base)
    c.caixa(f"{nome}Led", (0.015, 0.008, 0.012), (largura * 0.38, -0.037, 0.12), mt["led"], base)
    return base


def montar_estacao(mt):
    raiz = c.pivo("Estacao")
    y0, y1 = MESA_Y
    x0, x1 = MESA_X
    cy, cx = (y0 + y1) / 2, (x0 + x1) / 2
    # Mesa de metal com tampo de fórmica marrom e um painel na frente.
    c.caixa("Tampo", (x1 - x0, y1 - y0, 0.04), (cx, cy, TAMPO_Z - 0.02), mt["mesa_tampo"], raiz, bisel=0.01)
    for (px, py) in ((x0 + 0.04, y0 + 0.04), (x1 - 0.04, y0 + 0.04), (x0 + 0.04, y1 - 0.04), (x1 - 0.04, y1 - 0.04)):
        c.caixa(f"PeMesa{px:.2f}{py:.2f}", (0.04, 0.04, TAMPO_Z - 0.04), (px, py, (TAMPO_Z - 0.04) / 2), mt["mesa"], raiz)
    c.caixa("PainelMesa", (x1 - x0 - 0.1, 0.02, 0.32), (cx, y1 - 0.06, 0.52), mt["mesa"], raiz)
    c.caixa("Gaveteiro", (0.36, 0.55, 0.62), (x1 - 0.22, cy, 0.34), mt["mesa"], raiz, bisel=0.01)
    for i in range(3):
        c.caixa(f"Gaveta{i}", (0.3, 0.01, 0.16), (x1 - 0.22, y0 + 0.07, 0.52 - i * 0.19), mt["metal"], raiz)
    # Três monitores: o do meio reto, os dos lados virados para ela.
    tampo = TAMPO_Z
    monitor("MonitorMeio", (0.02, 0.98, tampo), 0, mt, raiz, 0.4)
    monitor("MonitorEsq", (-0.42, 0.92, tampo), 22, mt, raiz, 0.32)
    monitor("MonitorDir", (0.5, 0.95, tampo), -18, mt, raiz, 0.34)
    # Adesivos da Clarice nas molduras (o mesmo do bilhete dela).
    c.caixa("Adesivo1", (0.05, 0.005, 0.05), (0.14, 0.93 - 0.041, tampo + 0.34), mt["adesivo_rosa"], raiz)
    c.caixa("Adesivo2", (0.04, 0.005, 0.04), (-0.47, 0.875 - 0.04, tampo + 0.27), mt["adesivo_amarelo"], raiz, (0, 0, 22))
    # Teclado bege inclinado (aparece o tampo das teclas) e o mouse.
    c.caixa("Teclado", (0.46, 0.17, 0.035), (0.0, 0.68, tampo + 0.025), mt["bege"], raiz, (6, 0, 0), bisel=0.008)
    for i in range(3):
        c.caixa(f"Teclas{i}", (0.4, 0.03, 0.006), (0.0, 0.63 + i * 0.045, tampo + 0.047 + i * 0.005), mt["bege_escuro"], raiz, (6, 0, 0))
    c.caixa("Mouse", (0.06, 0.1, 0.035), (0.34, 0.7, tampo + 0.02), mt["bege"], raiz, bisel=0.012)
    # Gabinete bege no chão, à direita, com o LED aceso e o drive de disquete.
    c.caixa("Gabinete", (0.2, 0.46, 0.44), (1.12, 0.85, 0.22), mt["bege"], raiz, bisel=0.015)
    c.caixa("Drive", (0.13, 0.01, 0.025), (1.12, 0.619, 0.34), mt["bege_escuro"], raiz)
    c.caixa("GabineteLed", (0.02, 0.01, 0.015), (1.07, 0.619, 0.28), mt["led"], raiz)
    # Telefone bege com o fone no gancho e o fio enrolado: é por ele que a
    # Clarice liga para os telefones velhos do campus.
    c.caixa("Telefone", (0.2, 0.2, 0.07), (0.66, 0.66, tampo + 0.035), mt["bege"], raiz, (0, 0, -10), bisel=0.02)
    c.caixa("Monofone", (0.22, 0.06, 0.045), (0.66, 0.68, tampo + 0.09), mt["bege_escuro"], raiz, (0, 0, -10), bisel=0.015)
    c.caixa("FioTelefone", (0.015, 0.015, 0.4), (0.8, 0.6, 0.55), mt["cabo"], raiz, (0, 15, 0))
    # Pilha de disquetes, caneca, papéis e cabos descendo para o chão.
    for i, cor in enumerate(("disquete_azul", "disquete_amarelo", "disquete_azul", "cabo")):
        c.caixa(f"Disquete{i}", (0.09, 0.09, 0.006), (-0.5, 0.64, tampo + 0.004 + i * 0.007), mt[cor], raiz, (0, 0, i * 9))
    c.cone("Caneca", 0.04, 0.04, 0.1, (0.3, 0.6, tampo + 0.05), mt["caneca"], raiz, lados=6)
    c.caixa("Papeis", (0.2, 0.26, 0.01), (-0.22, 0.66, tampo + 0.005), mt["papel"], raiz, (0, 0, 8))
    for i, x in enumerate((-0.3, 0.1, 0.45)):
        c.caixa(f"Cabo{i}", (0.02, 0.02, 0.72), (x, 1.2, 0.38), mt["cabo"], raiz, (0, 6 - 6 * i, 0))
    c.caixa("CaboChao", (1.4, 0.03, 0.015), (0.3, 1.18, 0.01), mt["cabo"], raiz)
    return raiz


def montar_cadeira(mt, pai):
    """Cadeira de escritório giratória: base de cinco patas (aqui, uma cruz
    de duas barras e um pé a mais), coluna de gás, assento e encosto."""
    giro = c.pivo("Cadeira", CADEIRA_POS, pai)
    for i in range(5):
        c.caixa(f"Pata{i}", (0.04, 0.3, 0.03), (0, 0, 0.04), mt["cadeira"], giro, (0, 0, i * 72), desloc=(0, 0.15, 0))
    c.cone("Coluna", 0.03, 0.03, 0.3, (0, 0, 0.2), mt["metal"], giro, lados=6)
    c.caixa("Assento", (0.46, 0.44, 0.08), (0, 0.0, 0.39), mt["cadeira"], giro, bisel=0.025)
    c.caixa("HasteEncosto", (0.05, 0.04, 0.3), (0, 0.24, 0.51), mt["metal"], giro)
    c.caixa("Encosto", (0.4, 0.07, 0.28), (0, 0.27, 0.72), mt["cadeira"], giro, (-6, 0, 0), bisel=0.03)
    return giro


# ---------------------------------------------------------------------------
# Poses
# ---------------------------------------------------------------------------


def girar(nome, x=None, y=None, z=None):
    obj = bpy.data.objects[nome]
    rot = list(obj.rotation_euler)
    for i, v in enumerate((x, y, z)):
        if v is not None:
            rot[i] = math.radians(v)
    obj.rotation_euler = rot


def sentar(clarice):
    """Pose sentada: quadril na altura do assento, coxas para a frente,
    canelas para baixo e o pé reto no chão."""
    clarice.location = (0, 0, 0)
    bpy.data.objects["Quadril"].location = (0, 0.02, 0.48)
    for lado in ("PernaDir", "PernaEsq"):
        girar(f"{lado}Quadril", x=-88)
        girar(f"{lado}Joelho", x=88)
        girar(f"{lado}Tornozelo", x=0)
    girar("PernaDirQuadril", y=-4)
    girar("PernaEsqQuadril", y=6)


def pose_digitando(fase):
    """Inclinada para os monitores, braços no teclado. As mãos sobem e
    descem 1 px, alternadas (a esquerda meio ciclo depois da direita), e a
    cabeça acompanha o texto na tela, de leve."""
    girar("Tronco", x=12 + 3 * math.sin(math.radians(fase * 2)), z=4 * math.sin(math.radians(fase)))
    girar("Cabeca", x=-6 + 5 * math.sin(math.radians(fase * 2)), z=9 * math.sin(math.radians(fase)))
    for lado, desloc in (("BracoDir", 0), ("BracoEsq", 180)):
        onda = math.sin(math.radians(fase * 2 + desloc))
        girar(f"{lado}Ombro", x=-62 - 4 * onda)
        girar(f"{lado}Cotovelo", x=-52 + 6 * onda)
    girar("BracoDirOmbro", y=-14)
    girar("BracoEsqOmbro", y=14)


def pose_relaxada(fase):
    """Virada para o Gabriel: encostada, uma mão no colo e o outro braço
    apoiado no encosto. Respira devagar (a cabeça sobe e desce 1 px)."""
    girar("Tronco", x=-4 + 1.5 * math.sin(math.radians(fase)))
    girar("Cabeca", x=4 * (1 - math.cos(math.radians(fase))) / 2 - 2, z=-8)
    girar("BracoDirOmbro", x=-38, y=-8)
    girar("BracoDirCotovelo", x=-55)
    girar("BracoEsqOmbro", x=-20, y=30)
    girar("BracoEsqCotovelo", x=-70)


def pose_em_pe(tronco=0.0):
    girar("Tronco", x=tronco)
    girar("Cabeca", x=0, z=0)
    for lado, sinal in (("BracoDir", -1), ("BracoEsq", 1)):
        girar(f"{lado}Ombro", x=2, y=6 * sinal)
        girar(f"{lado}Cotovelo", x=-10)


def expressao(qual):
    """Monta a expressão com a boca, os cantos da boca e as sobrancelhas
    (num retrato de 40 px, 1 px de diferença já muda o rosto):
      normal   boca reta, sobrancelhas retas;
      sorrindo boca mais larga e os cantos para cima, sobrancelhas erguidas
               (o sorrisinho de canto de quem já sabe o que você vai dizer);
      seria    boca curta, sobrancelhas baixas e inclinadas para o meio."""
    boca_obj = bpy.data.objects["Boca"]
    boca_obj.scale = {"normal": (1, 1, 1), "sorrindo": (1.3, 1, 1), "seria": (0.6, 1, 1)}[qual]
    for lado in (-1, 1):
        canto = bpy.data.objects[f"CantoBoca{lado}"]
        canto.hide_render = qual != "sorrindo"
        sob = bpy.data.objects[f"Sobrancelha{lado}"]
        sob.location.z = {"normal": 0.174, "sorrindo": 0.18, "seria": 0.168}[qual]
        sob.rotation_euler = (0, math.radians({"normal": 0, "sorrindo": -6, "seria": 16}[qual] * lado), 0)


# ---------------------------------------------------------------------------
# Câmera inclinada
# ---------------------------------------------------------------------------
#
# A câmera ortográfica gira INCLINACAO graus para baixo. Com ela inclinada,
# o vetor "para cima" da tela é u = (0, sen t, cos t) e a direção do olhar
# é d = (0, cos t, -sen t). Um ponto p aparece na altura (p - camera) · u
# da tela. Queremos o chão no ponto (0, 0, 0) a pe_px pixels da borda de
# baixo, ou seja, a -(altura/2 - pe_px)/px_por_m do meio. Pondo a câmera em
# 20·(-d) + k·u, sobra (0 - camera) · u = -k, então k = (altura/2 - pe_px)/px_por_m.


def enquadrar_inclinado(cam, largura_px, altura_px, px_por_m, pe_px):
    cena = bpy.context.scene
    cena.render.resolution_x = largura_px
    cena.render.resolution_y = altura_px
    cam.data.ortho_scale = largura_px / px_por_m
    t = math.radians(INCLINACAO)
    k = (altura_px / 2 - pe_px) / px_por_m
    cam.rotation_euler = (math.radians(90) - t, 0, 0)
    cam.location = (0.0, -20 * math.cos(t) + k * math.sin(t), 20 * math.sin(t) + k * math.cos(t))


def enquadrar_retrato(cam, largura_px, altura_px, px_por_m, pe_px):
    cena = bpy.context.scene
    cena.render.resolution_x = largura_px
    cena.render.resolution_y = altura_px
    cam.data.ortho_scale = largura_px / px_por_m
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.location = (0.0, -20.0, ALTURA_RETRATO_M)


def render(cam, raiz, materiais, angulo, quadro, px_por_m, pe_px, enquadrar):
    original = c.enquadrar
    c.enquadrar = enquadrar
    try:
        img, ind, _ = c.renderizar_vista(cam, raiz, materiais, angulo, quadro, px_por_m, pe_px)
    finally:
        c.enquadrar = original
    return c.contorno(img, ind, materiais)


def main():
    c.cena_vazia()
    materiais, mt = criar_materiais()
    c.usar_colecao("Clarice")
    cena = c.pivo("Cena")
    estacao = montar_estacao(mt)
    estacao.parent = cena
    cadeira = montar_cadeira(mt, cena)
    c.DETALHE = DETALHE
    c.SUAVE = True
    clarice = montar_clarice(mt, None)
    c.achatar_sombra("Rosto")
    cam = c.criar_camera()
    c.criar_luzes()
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    # 1. Em pé, sozinha (folha de referência e retratos): a estação some.
    for obj in bpy.data.objects:
        if obj.name.startswith(("Estacao", "Cadeira")) or obj.parent in (estacao, cadeira) or _dentro(obj, estacao) or _dentro(obj, cadeira):
            obj.hide_render = True
    pose_em_pe()
    expressao("normal")
    # Sprites de jogo em pé, com as mesmas vistas, animações e tamanhos do
    # Gabriel (comum.py, item 7), para quando ela andar pelo campus.
    jogo = c.renderizar_vistas_jogo(cam, clarice, materiais, "clarice")
    parado = c.guardar_pose()
    andar = c.renderizar_ciclo(cam, clarice, materiais, lambda fase: c.pose_andar(parado, fase),
                               c.QUADROS_ANDAR, "clarice andar")
    c.restaurar_pose(parado)
    respirar = c.renderizar_ciclo(cam, clarice, materiais, lambda fase: c.pose_parado(parado, fase),
                                  c.QUADROS_PARADO, "clarice parado")
    c.restaurar_pose(parado)
    em_pe = []
    for angulo in (0, 35, 90, 180):
        em_pe.append(render(cam, clarice, materiais, angulo, c.QUADRO_REF, c.PX_POR_M_REF, c.PE_REF_PX, c.enquadrar))
    retratos = {}
    for qual in ("normal", "sorrindo", "seria"):
        expressao(qual)
        retratos[qual] = render(cam, clarice, materiais, 24, QUADRO_RETRATO, PX_POR_M_RETRATO, 0, enquadrar_retrato)
    expressao("normal")
    print("[clarice] em pé e retratos prontos")

    # 2. Sentada na estação. A Clarice passa a ser filha da cadeira: girar a
    #    cadeira gira ela junto, e a mesa fica parada.
    for obj in bpy.data.objects:
        obj.hide_render = False
    clarice.parent = cadeira
    sentar(clarice)
    digitando = []
    for q in range(QUADROS_DIGITANDO):
        pose_digitando(360 * q / QUADROS_DIGITANDO)
        girar("Cadeira", z=180)
        digitando.append(render(cam, cena, materiais, 0, QUADRO_MESA, c.PX_POR_M_JOGO * RESOLUCAO, PE_MESA_PX, enquadrar_inclinado))
    print("[clarice] digitando pronto")
    virando = []
    for i, giro in enumerate(GIROS_VIRANDO):
        mistura = i / (len(GIROS_VIRANDO) - 1)
        pose_digitando(0)
        _misturar_com_relaxada(mistura)
        girar("Cadeira", z=giro + (GIRO_OLHANDO - GIROS_VIRANDO[-1]) * mistura)
        virando.append(render(cam, cena, materiais, 0, QUADRO_MESA, c.PX_POR_M_JOGO * RESOLUCAO, PE_MESA_PX, enquadrar_inclinado))
    print("[clarice] virando pronto")
    olhando = []
    for q in range(QUADROS_OLHANDO):
        pose_relaxada(360 * q / QUADROS_OLHANDO)
        girar("Cadeira", z=GIRO_OLHANDO)
        olhando.append(render(cam, cena, materiais, 0, QUADRO_MESA, c.PX_POR_M_JOGO * RESOLUCAO, PE_MESA_PX, enquadrar_inclinado))
    print("[clarice] olhando pronto")

    # 3. Uma paleta só para tudo, e os arquivos.
    todas = digitando + virando + olhando + em_pe + list(retratos.values())
    convertidas, paleta = c.unificar_paleta(todas, materiais, MAX_CORES)
    n1, n2, n3 = len(digitando), len(virando), len(olhando)
    digitando, virando, olhando = convertidas[:n1], convertidas[n1:n1 + n2], convertidas[n1 + n2:n1 + n2 + n3]
    em_pe = convertidas[n1 + n2 + n3:n1 + n2 + n3 + 4]
    retratos = dict(zip(retratos.keys(), convertidas[n1 + n2 + n3 + 4:]))
    for nome, quadros in (("digitando", digitando), ("virando", virando), ("olhando", olhando)):
        c.salvar_png(np.concatenate(quadros, axis=1), os.path.join(PASTA_SAIDA, f"clarice_{nome}.png"))
    for nome, img in retratos.items():
        c.salvar_png(img, os.path.join(PASTA_SAIDA, f"clarice_retrato_{nome}.png"))
    # Os sprites em pé só usam a paleta já calculada: as cores dos sprites
    # sentados e dos retratos não mudam.
    c.salvar_sprites_jogo(PASTA_SAIDA, "clarice", paleta, jogo, andar, respirar)
    folha = c.montar_folha([em_pe, [digitando[0], virando[2], olhando[0]], list(retratos.values())])
    c.salvar_png(folha, os.path.join(PASTA_SAIDA, "clarice_referencia.png"))
    print("[clarice] paleta:", " ".join(c.rgb_para_hex(np.array(cor) / 255) for cor in paleta))
    c.salvar_blend(ARQUIVO_BLEND, cena, angulo=0)
    print("[clarice] pronto")


def _dentro(obj, raiz):
    while obj.parent is not None:
        if obj.parent == raiz:
            return True
        obj = obj.parent
    return False


def _misturar_com_relaxada(mistura):
    """Meio caminho entre digitar e se encostar: interpola as juntas dos
    braços e do tronco entre as duas poses (mistura de 0 a 1)."""
    nomes = ("Tronco", "Cabeca", "BracoDirOmbro", "BracoDirCotovelo", "BracoEsqOmbro", "BracoEsqCotovelo")
    antes = {n: tuple(bpy.data.objects[n].rotation_euler) for n in nomes}
    pose_relaxada(0)
    depois = {n: tuple(bpy.data.objects[n].rotation_euler) for n in nomes}
    for n in nomes:
        bpy.data.objects[n].rotation_euler = [a + (b - a) * mistura for a, b in zip(antes[n], depois[n])]


main()
