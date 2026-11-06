# gerar_ciborgue.py — modela o Ciborgue, o robô que o Carlos fez à própria
# imagem para caçar no bunker, e renderiza as tiras de caminhada no formato
# dos robôs (corpo + tira só dos olhos).
#
# Como rodar (sem abrir a janela do Blender):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_ciborgue.py
#
# O que sai (em assets/sprites/personagens/robos/):
#   ciborgue_andar_<vista>.png        caminhada: 12 quadros de 96 x 112
#                                     (resolução dobrada, como o Carlos: o
#                                     Godot mostra com escala 0,5), vistas
#                                     lado, frente e costas
#   ciborgue_andar_<vista>_olhos.png  os mesmos quadros, só com os pixels que
#                                     brilham (olhos, lupa e o núcleo do peito)
#   ciborgue_referencia.png           frente, 3/4, lado e costas
#   assets/modelagem/personagens/ciborgue.blend   o modelo
#
# Quem é (docs/historia/História_Completa.md, seção 2.3): o Carlos nunca vai
# ao bunker, então mandou para lá uma cópia dele mesmo, de metal por baixo
# da pele. O corpo é o do Carlos (gerar_carlos.py, importado: as mesmas
# juntas, o jaleco, a camiseta dos anos 80, o jeans e o tênis), e por cima
# vêm as peças de máquina:
#   - pele cinza, sem sangue, e a roupa do Carlos mais gasta e suja de óleo;
#   - a metade direita do crânio e o queixo são uma placa de metal;
#   - os dois olhos brilham no vermelho dos robôs, e a lupa vermelha do
#     Carlos virou uma terceira luz;
#   - no peito, por baixo do jaleco aberto, uma placa com um núcleo vermelho;
#   - o antebraço esquerdo é metal exposto, com o relógio-calculadora ainda
#     no pulso, e a mão é uma garra de metal;
#   - cabos saindo da nuca para dentro do jaleco e um joelho de metal.
# Anda duro, como máquina: passo curto, joelho quase reto e braços parados.
#
# Por que a tira dos olhos? Igual aos robôs (gerar_robos.py): no escuro do
# bunker o Godot desenha os pixels que brilham por cima, sem luz.

import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import comum as c  # noqa: E402
import gerar_carlos as carlos  # noqa: E402
import bpy  # noqa: E402

PASTA_SAIDA = os.path.join(c.PASTA_SPRITES, "robos")
NOME = "ciborgue"
MAX_CORES = 48
DETALHE = 3
VISTAS = (("lado", 90), ("frente", 0), ("costas", 180))

# Passo de máquina: curto, com o joelho quase reto e os braços parados.
PASSO = {"coxa": 13, "joelho": 24, "braco": 3, "descida": 0.02}


def criar_materiais():
    m = c.Materiais()
    return m, {
        "pele": m.novo("pele", "#b1a9a3"),
        "cabelo": m.novo("cabelo", "#a29d95"),
        "jaleco": m.novo("jaleco", "#bcb7aa"),
        "mancha": m.novo("mancha", "#5b5144"),
        "camiseta": m.novo("camiseta", "#8e3066"),
        "estampa_turquesa": m.novo("estampa_turquesa", "#2a8a86", "plano"),
        "estampa_amarela": m.novo("estampa_amarela", "#b39632", "plano"),
        "calca": m.novo("calca", "#5e7190"),
        "tenis": m.novo("tenis", "#c4bfb3"),
        "faixa_tenis": m.novo("faixa_tenis", "#a33a31", "plano"),
        "sola": m.novo("sola", "#7c766b"),
        "relogio": m.novo("relogio", "#2a2a2e"),
        "visor": m.novo("visor", "#9fbf8a", "plano"),
        "luva": m.novo("luva", "#25252b"),
        "metal": m.novo("metal", "#7d848d", aspereza=0.5),
        "cromo": m.novo("cromo", "#9ea7b1", aspereza=0.3),
        "cromo_escuro": m.novo("cromo_escuro", "#58606b", aspereza=0.4),
        "cabo": m.novo("cabo", "#1d1d24"),
        "caneta_azul": m.novo("caneta_azul", "#3d5fa8", "plano"),
        "caneta_vermelha": m.novo("caneta_vermelha", "#b8483a", "plano"),
        "luz_vermelha": m.novo("luz_vermelha", "#ff4032", "brilho"),
        # Tudo o que brilha usa este material: é ele que vai para a tira dos olhos.
        "olho": m.novo("olho", "#ff4032", "brilho"),
        "oculos": m.novo("oculos", "#1a1618", "plano"),
        "lente": m.novo("lente", "#c6dde6", "plano"),
        "boca": m.novo("boca", "#5a2a26", "plano"),
    }


def trocar_material(nome, mat):
    bpy.data.objects[nome].data.materials[0] = mat


def pecas_de_maquina(mt):
    """As peças que fazem do corpo do Carlos o Ciborgue. Os pivôs (Cabeca,
    Tronco, BracoEsqCotovelo, PernaDirJoelho) são os do gerar_carlos.py."""
    cabeca = bpy.data.objects["Cabeca"]
    tronco = bpy.data.objects["Tronco"]
    cotovelo = bpy.data.objects["BracoEsqCotovelo"]
    joelho = bpy.data.objects["PernaDirJoelho"]

    # A metade direita do crânio (lado -X, o da lupa) e o queixo de metal.
    c.caixa("PlacaCranio", (0.105, 0.235, 0.14), (-0.05, 0.0, 0.195), mt["cromo"], cabeca, bisel=0.02)
    c.caixa("RisoPlaca", (0.006, 0.2, 0.012), (-0.0, -0.005, 0.2), mt["cromo_escuro"], cabeca)
    c.caixa("Queixo", (0.17, 0.17, 0.07), (0, -0.012, 0.03), mt["cromo"], cabeca, bisel=0.015)
    for i, x in enumerate((-0.05, 0.05)):
        c.caixa(f"Junta{i}", (0.02, 0.06, 0.03), (x * 1.9, -0.02, 0.045), mt["cromo_escuro"], cabeca)

    # Os olhos e a lupa brilham no vermelho dos robôs.
    for nome in ("Olho-1", "Olho1", "LupaLente"):
        trocar_material(nome, mt["olho"])

    # Cabos da nuca descendo para dentro da gola do jaleco.
    for i, (x, giro) in enumerate(((-0.035, 28), (0.0, 36), (0.04, 30))):
        c.cone(f"CaboNuca{i}", 0.011, 0.011, 0.22, (x, 0.1, 0.02), mt["cabo"], cabeca, rot=(giro, 0, 0), lados=4)

    # Placa no peito, com o núcleo vermelho, por cima da camiseta.
    c.caixa("PlacaPeito", (0.115, 0.016, 0.12), (0, -0.142, 0.37), mt["cromo_escuro"], tronco, bisel=0.01)
    c.caixa("Nucleo", (0.05, 0.02, 0.05), (0, -0.152, 0.37), mt["olho"], tronco, (0, 45, 0))

    # O antebraço esquerdo é metal exposto; o relógio-calculadora ficou no pulso.
    trocar_material("BracoEsqAntebraco", mt["cromo"])
    trocar_material("BracoEsqLuva", mt["cromo_escuro"])
    trocar_material("BracoEsqMao", mt["cromo_escuro"])
    c.cone("PistaoAntebraco", 0.014, 0.014, 0.2, (0.0, 0.05, -0.12), mt["cabo"], cotovelo, lados=4)
    for i, x in enumerate((-0.022, 0.0, 0.022)):
        garra = c.pivo(f"Garra{i}", (x, -0.03, -0.34), cotovelo, (-15, 0, 0))
        c.cone(f"GarraPeca{i}", 0.011, 0.003, 0.07, (0, 0, -0.035), mt["cromo"], garra, lados=4)

    # O joelho direito rasgou o jeans: aparece a articulação de metal.
    c.esfera("JoelhoMetal", 0.05, (0, -0.035, 0.0), mt["cromo"], joelho, seg=6, aneis=4)


def renderizar():
    c.DETALHE = DETALHE
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = criar_materiais()
    c.usar_colecao("Ciborgue")
    raiz = carlos.montar(mt)
    pecas_de_maquina(mt)
    c.achatar_sombra("Rosto")
    carlos.esconder_boca()
    cam = c.criar_camera()
    c.criar_luzes()
    olho = [n for n, _, _, _ in materiais.lista].index("olho")

    parado = c.guardar_pose()
    corpos = {v: [] for v, _ in VISTAS}
    olhos = {v: [] for v, _ in VISTAS}
    for q in range(c.QUADROS_ANDAR):
        c.pose_andar(parado, 360 * q / c.QUADROS_ANDAR, **PASSO)
        for vista, angulo in VISTAS:
            img, ind, _ = c.renderizar_vista(cam, raiz, materiais, angulo, c.QUADRO_JOGO_2X,
                                             c.PX_POR_M_JOGO_2X, c.PE_JOGO_2X)
            corpos[vista].append(c.contorno(img, ind, materiais))
            so_olhos = np.zeros_like(img)
            so_olhos[ind == olho] = img[ind == olho]
            olhos[vista].append(so_olhos)
        print(f"[{NOME}] andar: quadro {q + 1}/{c.QUADROS_ANDAR}")
    c.restaurar_pose(parado)
    linhas = corpos["lado"][0][..., 3].any(axis=1).nonzero()[0]
    print(f"[{NOME}] altura no sprite: {linhas[-1] - linhas[0] + 1} px (resolução 2x)")

    referencia = []
    for angulo in (0, 35, 90, 180):
        img, ind, _ = c.renderizar_vista(cam, raiz, materiais, angulo, c.QUADRO_REF, c.PX_POR_M_REF, c.PE_REF_PX)
        referencia.append(c.contorno(img, ind, materiais))

    todas = [q for v in corpos.values() for q in v]
    convertidas, paleta = c.unificar_paleta(todas + referencia, materiais, MAX_CORES)
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    i = 0
    for vista, _ in VISTAS:
        c.salvar_png(np.concatenate(convertidas[i:i + c.QUADROS_ANDAR], axis=1),
                     os.path.join(PASTA_SAIDA, f"{NOME}_andar_{vista}.png"))
        c.salvar_png(np.concatenate(olhos[vista], axis=1),
                     os.path.join(PASTA_SAIDA, f"{NOME}_andar_{vista}_olhos.png"))
        i += c.QUADROS_ANDAR
    c.salvar_png(c.montar_folha([convertidas[i:]]), os.path.join(PASTA_SAIDA, f"{NOME}_referencia.png"))
    c.salvar_blend(os.path.join(c.PASTA_SCRIPT, f"{NOME}.blend"), raiz)
    print(f"[{NOME}] pronto")


renderizar()
