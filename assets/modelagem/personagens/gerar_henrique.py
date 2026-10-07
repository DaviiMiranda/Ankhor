# gerar_henrique.py — modela o Henrique (2019), o pesquisador, no Blender,
# por código, e renderiza os mesmos sprites do Gabriel: as cinco vistas de
# jogo, a caminhada e a respiração em cada uma, os retratos da caixa de
# diálogo e a folha de referência.
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_henrique.py
#
# O que sai (em assets/sprites/personagens/henrique/), com os tamanhos do Gabriel:
#   henrique_<vista>.png             96 x 112 (resolução dobrada: o Godot
#                                    mostra com escala 0,5), vistas lado,
#                                    frente, tres_quartos, costas e
#                                    tres_quartos_costas
#   henrique_andar_<vista>.png       caminhada: 12 quadros de 96 x 112
#   henrique_parado_<vista>.png      parado respirando: 8 quadros
#   henrique_retrato_<expressão>.png 80 x 80 (normal, nervoso, timido)
#   henrique_referencia.png          frente, 3/4, lado e costas, e os retratos
#   assets/modelagem/personagens/henrique.blend   o modelo
#
# Quem é (docs/historia/personagens/henrique.md): aluno de iniciação
# científica da Unifor em 2019, uns 20 anos. Estudava à noite na Biblioteca
# e sumiu. Gênio quieto, introvertido, perfeccionista e ansioso, que fala
# pouco e anota muito.
#
# O visual conta isso:
#   - 2019: camisa de flanela xadrez aberta por cima de uma camiseta cinza,
#     calça jeans preta, tênis de lona escuro com biqueira e sola brancas;
#   - o aluno que anota tudo: o caderno de capa dura sempre na mão esquerda
#     (com o elástico) e um lápis atrás da orelha direita;
#   - óculos redondos de aro fino e o cabelo escuro bagunçado caindo na
#     testa: noites sem dormir em cima das contas;
#   - a cor dele é o laranja-queimado da flanela. Gabriel vermelho, Clarice
#     verde-azulado, Zane amarelo-ácido, Baltazar vinho, Rafael azul-celeste;
#   - postura: o contrário do Zane. Ombros fechados, cabeça baixa, braços
#     colados ao corpo, passo curto: quem não quer ocupar espaço.
#
# O lápis fica do lado direito dele (-X), virado para a câmera nas vistas de
# lado e de 3/4.
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

# Passo curto e braço quase parado: o caderno vai junto, e ele não quer
# chamar atenção.
PASSO = {"coxa": 18, "joelho": 48, "braco": 9}


def criar_materiais():
    m = c.Materiais()
    return m, {
        "pele": m.novo("pele", "#d3a383"),
        "cabelo": m.novo("cabelo", "#2b211d"),
        "flanela": m.novo("flanela", "#b8622e"),
        "xadrez": m.novo("xadrez", "#4a1c18"),
        "camiseta": m.novo("camiseta", "#8b8d93"),
        "jeans": m.novo("jeans", "#2c2d35"),
        "tenis": m.novo("tenis", "#33384a"),
        "borracha": m.novo("borracha", "#e1ddd2"),
        "caderno": m.novo("caderno", "#2f4a5e"),
        "folhas": m.novo("folhas", "#e4dccb"),
        "lapis": m.novo("lapis", "#e2b43a"),
        "olho": m.novo("olho", "#1b1620", "plano"),
        "oculos": m.novo("oculos", "#2a2a30", "plano"),
        "lente": m.novo("lente", "#b8cfdb", "plano"),
        "boca": m.novo("boca", "#5c2f28", "plano"),
    }


# ---------------------------------------------------------------------------
# O Henrique
# ---------------------------------------------------------------------------
#
# 1,76 m, magro, com os ombros caídos para a frente. Juntas com os nomes do
# gerar_gabriel.py.


def perna(nome, lado, mt, quadril, giro_coxa, giro_joelho):
    """Jeans preto justo e tênis de lona com biqueira branca."""
    junta = c.pivo(f"{nome}Quadril", (0.09 * lado, 0.0, 0.0), quadril, (giro_coxa, 0, 0))
    c.membro(f"{nome}Coxa", 0.08, 0.062, 0.41, mt["jeans"], junta)
    joelho = c.pivo(f"{nome}Joelho", (0, 0, -0.41), junta, (giro_joelho, 0, 0))
    c.membro(f"{nome}Canela", 0.062, 0.054, 0.37, mt["jeans"], joelho)
    tornozelo = c.pivo(f"{nome}Tornozelo", (0, 0, -0.37), joelho, (-giro_coxa - giro_joelho, 0, 0))
    c.caixa(f"{nome}Tenis", (0.1, 0.25, 0.08), (0, -0.04, -0.05), mt["tenis"], tornozelo, bisel=0.02)
    c.caixa(f"{nome}Biqueira", (0.102, 0.06, 0.05), (0, -0.145, -0.065), mt["borracha"], tornozelo, bisel=0.012)
    c.caixa(f"{nome}Sola", (0.108, 0.26, 0.025), (0, -0.04, -0.088), mt["borracha"], tornozelo)


def braco(nome, lado, mt, tronco, giro_ombro, giro_cotovelo):
    """Manga comprida da flanela, dobrada uma vez no punho, e a mão."""
    ombro = c.pivo(f"{nome}Ombro", (0.21 * lado, 0.0, 0.46), tronco, (giro_ombro, 8 * lado, 0))
    c.membro(f"{nome}Braco", 0.064, 0.056, 0.3, mt["flanela"], ombro)
    c.cone(f"{nome}Listra", 0.066, 0.066, 0.025, (0, 0, -0.12), mt["xadrez"], ombro, lados=6)
    cotovelo = c.pivo(f"{nome}Cotovelo", (0, 0, -0.3), ombro, (giro_cotovelo, 0, 0))
    c.membro(f"{nome}Antebraco", 0.056, 0.05, 0.24, mt["flanela"], cotovelo)
    c.cone(f"{nome}Dobra", 0.055, 0.055, 0.04, (0, 0, -0.225), mt["xadrez"], cotovelo, lados=6)
    c.caixa(f"{nome}Mao", (0.055, 0.08, 0.09), (0, 0, -0.29), mt["pele"], cotovelo, bisel=0.02)
    return cotovelo


def caderno(mt, cotovelo):
    """O caderno de capa dura na mão esquerda, em pé, com o elástico."""
    c.caixa("Caderno", (0.03, 0.17, 0.22), (0.035, -0.02, -0.29), mt["caderno"], cotovelo, bisel=0.006)
    c.caixa("CadernoFolhas", (0.022, 0.16, 0.21), (0.035, -0.023, -0.29), mt["folhas"], cotovelo,
            desloc=(0, -0.009, 0))
    c.caixa("CadernoElastico", (0.034, 0.012, 0.222), (0.035, 0.035, -0.29), mt["xadrez"], cotovelo)


def cabeca(mt, tronco):
    # Cabeça baixa: quem não quer ocupar espaço.
    pescoco = c.pivo("Cabeca", (0, 0, 0.58), tronco, (8, 0, 0))
    c.caixa("Rosto", (0.195, 0.225, 0.24), (0, 0, 0.12), mt["pele"], pescoco, bisel=0.04)
    c.caixa("Nariz", (0.032, 0.05, 0.05), (0, -0.112, 0.095), mt["pele"], pescoco)
    for lado in (-1, 1):
        c.caixa(f"Orelha{lado}", (0.03, 0.05, 0.06), (0.1 * lado, 0.01, 0.115), mt["pele"], pescoco)
        c.caixa(f"Olho{lado}", (0.03, 0.006, 0.026), (0.045 * lado, -0.116, 0.128), mt["olho"], pescoco)
        # Óculos redondos de aro fino: a lente clara e o aro em cima e embaixo.
        c.caixa(f"Lente{lado}", (0.056, 0.006, 0.048), (0.046 * lado, -0.112, 0.128), mt["lente"], pescoco)
        c.caixa(f"AroCima{lado}", (0.058, 0.01, 0.008), (0.046 * lado, -0.114, 0.154), mt["oculos"], pescoco)
        c.caixa(f"AroBaixo{lado}", (0.05, 0.01, 0.008), (0.046 * lado, -0.114, 0.103), mt["oculos"], pescoco)
        c.caixa(f"Haste{lado}", (0.008, 0.12, 0.008), (0.098 * lado, -0.05, 0.14), mt["oculos"], pescoco)
        c.caixa(f"Sobrancelha{lado}", (0.048, 0.014, 0.016), (0.046 * lado, -0.115, 0.178), mt["cabelo"], pescoco)
        c.caixa(f"CantoBoca{lado}", (0.012, 0.01, 0.012), (0.026 * lado, -0.1135, 0.056), mt["boca"], pescoco)
    c.caixa("Ponte", (0.03, 0.01, 0.008), (0, -0.115, 0.135), mt["oculos"], pescoco)
    c.caixa("Boca", (0.04, 0.01, 0.012), (0, -0.114, 0.05), mt["boca"], pescoco)
    # Cabelo escuro bagunçado, com a franja caindo na testa por cima dos óculos.
    c.caixa("CabeloTopo", (0.215, 0.24, 0.08), (0, 0.01, 0.235), mt["cabelo"], pescoco, bisel=0.025)
    c.caixa("CabeloNuca", (0.21, 0.08, 0.16), (0, 0.085, 0.16), mt["cabelo"], pescoco, bisel=0.02)
    for lado in (-1, 1):
        c.caixa(f"CabeloLado{lado}", (0.03, 0.15, 0.1), (0.102 * lado, 0.035, 0.19), mt["cabelo"], pescoco)
    for i, (x, rz, ry) in enumerate(((-0.06, 8, -18), (0.0, -4, 6), (0.055, -10, 20))):
        c.caixa(f"Franja{i}", (0.07, 0.05, 0.06), (x, -0.095, 0.24), mt["cabelo"], pescoco, (8, ry, rz), bisel=0.01)
    # O lápis atrás da orelha direita.
    c.caixa("Lapis", (0.012, 0.012, 0.13), (-0.112, 0.02, 0.17), mt["lapis"], pescoco, (60, 0, 0))
    return pescoco


def montar(mt):
    raiz = c.pivo("Henrique")
    quadril = c.pivo("Quadril", (0, 0, 0.88), raiz)
    perna("PernaDir", -1, mt, quadril, -2, 3)
    perna("PernaEsq", +1, mt, quadril, 2, 3)
    # Ombros fechados para a frente.
    tronco = c.pivo("Tronco", (0, 0, 0), quadril, (6, 0, 0))
    c.caixa("Bacia", (0.28, 0.15, 0.15), (0, 0, 0.0), mt["jeans"], tronco, bisel=0.03)
    # Camiseta cinza por baixo; a flanela aberta por cima, com as duas
    # metades da frente afastadas e as listras do xadrez.
    c.cone("Flanela", 0.2, 0.212, 0.52, (0, 0, 0.27), mt["flanela"], tronco, lados=8, achatar=0.6)
    for i, z in enumerate((0.12, 0.3)):
        c.cone(f"ListraH{i}", 0.222, 0.222, 0.036, (0, 0, z), mt["xadrez"], tronco, lados=8, achatar=0.6)
    for i, x in enumerate((-0.13, 0.13)):
        for nome, y in (("Frente", -0.112), ("Costas", 0.112)):
            c.caixa(f"ListraV{nome}{i}", (0.034, 0.014, 0.5), (x, y, 0.27), mt["xadrez"], tronco)
    c.caixa("AberturaCamiseta", (0.06, 0.02, 0.46), (0, -0.124, 0.27), mt["camiseta"], tronco)
    for lado in (-1, 1):
        c.caixa(f"Carcela{lado}", (0.022, 0.022, 0.46), (0.041 * lado, -0.122, 0.27), mt["flanela"], tronco)
    c.caixa("Gola", (0.25, 0.13, 0.04), (0, 0.0, 0.52), mt["flanela"], tronco, bisel=0.012)
    c.cone("Pescoco", 0.046, 0.046, 0.1, (0, 0, 0.55), mt["pele"], tronco, lados=6)
    braco("BracoDir", -1, mt, tronco, -1, -10)
    cotovelo_esq = braco("BracoEsq", +1, mt, tronco, -6, -28)
    caderno(mt, cotovelo_esq)
    cabeca(mt, tronco)
    return raiz


# ---------------------------------------------------------------------------
# Retratos (caixa de diálogo)
# ---------------------------------------------------------------------------
#
# Enquadramento do comum.py (renderizar_retrato). Três expressões:
#   normal   boca reta, sobrancelhas retas: o rosto fechado de quem pensa;
#   nervoso  boca curta e sobrancelhas levantadas no meio: a ansiedade de
#            quem desconfia ter causado tudo;
#   timido   um sorriso pequeno (os cantos sobem) e as sobrancelhas um
#            pouco erguidas.

EXPRESSOES = ("normal", "nervoso", "timido")


def expressao(qual):
    boca = bpy.data.objects["Boca"]
    boca.hide_render = False
    boca.scale = (0.6, 1, 1) if qual == "nervoso" else (1, 1, 1)
    for lado in (-1, 1):
        bpy.data.objects[f"CantoBoca{lado}"].hide_render = qual != "timido"
        sob = bpy.data.objects[f"Sobrancelha{lado}"]
        altura, giro = {"normal": (0.176, 0), "nervoso": (0.182, -24 * lado), "timido": (0.186, 0)}[qual]
        sob.location.z = altura
        sob.rotation_euler = (0, math.radians(giro), 0)


def esconder_boca():
    for nome in ("Boca", "CantoBoca-1", "CantoBoca1"):
        bpy.data.objects[nome].hide_render = True


def main():
    c.DETALHE = DETALHE
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = criar_materiais()
    c.usar_colecao("Henrique")
    raiz = montar(mt)
    c.achatar_sombra("Rosto")
    c.gerar_em_pe("henrique", raiz, materiais, MAX_CORES, EXPRESSOES, expressao, esconder_boca, passo=PASSO)


main()
