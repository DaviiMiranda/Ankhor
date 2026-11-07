# gerar_zane_casaco.py — anima o Zane abrindo a jaqueta com as duas mãos, para
# a tela do inventário: é o gesto dele no lugar da mochila do Gabriel. Por dentro
# da jaqueta ficam o forro escuro, os bolsos internos com o que ele carrega e uma
# linha de luz em cada aba.
#
# Como rodar (sem abrir a janela do Blender; precisa do gerar_zane.py ao lado):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_zane_casaco.py
#
# Para testar uma vista só (mais rápido), passe o nome dela depois de --:
#
#   blender -b --factory-startup --python .../gerar_zane_casaco.py -- frente
#
# O que sai (24 quadros de 96 x 112 lado a lado, na paleta dele, como a mochila):
#   assets/sprites/personagens/zane/zane_casaco_<vista>.png
#
# Como a mochila, a tira toca para a frente ao ABRIR o inventário e de trás para
# a frente ao FECHAR.
#
# ---------------------------------------------------------------------------
# AS ABAS
# ---------------------------------------------------------------------------
#
# No modelo (gerar_zane.py) a jaqueta é uma peça só, um cone de seção oval. Para
# ela abrir, a frente vira duas ABAS, caixas finas presas por uma dobradiça na
# costura do lado (x = ±0,15 m, um pouco atrás da frente do peito). Fechada, a
# aba vai da dobradiça até o meio do peito, onde as duas se encontram no zíper:
#
#     dobradiça (±0,15; -0,11)  →  borda livre (0; -0,152)
#
# O ângulo dessa reta, visto de cima, é α0 = atan(0,042 / 0,15) ≈ 15,6°. Abrir
# é girar a aba em volta do eixo vertical da dobradiça, α = (α0 + abertura) · lado,
# com a abertura indo de 0° a 140°: a borda livre vem para a frente e depois
# para fora, e o forro (a face de dentro), com os bolsos, passa a olhar para a
# câmera. Em 140° a aba aponta para fora e só um pouco para a frente.
#
# As abas só aparecem quando a abertura passa de meio grau. Antes disso fica a
# jaqueta original, para o quadro 0 ser igual ao sprite parado e o gesto
# começar sem salto. Atrás das abas abertas aparece a camiseta preta.
#
# ---------------------------------------------------------------------------
# OS BRAÇOS
# ---------------------------------------------------------------------------
#
# Poses-chave com os ângulos (graus, somados à pose parada) do ombro e do
# cotovelo, da abertura do braço (rotação em Y: positivo afasta do corpo), da
# torção do braço (em Z: positivo vira o antebraço para dentro), do tronco, da
# cabeça e das abas. As mãos sobem até a gola, seguram as bordas e
# puxam para os lados, e a cabeça abaixa para olhar os bolsos. Os quadros entre as
# chaves saem de Catmull-Rom (ver gerar_gabriel_mochila.py).

import math
import os
import sys

sys.dont_write_bytecode = True
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA_SCRIPT)
import comum as c  # noqa: E402
import numpy as np  # noqa: E402
import bpy  # noqa: E402

_fonte = open(os.path.join(PASTA_SCRIPT, "gerar_zane.py"), encoding="utf-8").read()
_fonte = _fonte.rsplit("\nmain()", 1)[0]
gz = {"__file__": os.path.join(PASTA_SCRIPT, "gerar_zane.py"), "__name__": "gerar_zane"}
exec(compile(_fonte, "gerar_zane.py", "exec"), gz)

PASTA_ZANE = os.path.join(c.PASTA_SPRITES, "zane")

QUADROS = 24
DOBRADICA_X, DOBRADICA_Y = 0.15, -0.11
BORDA_Y = -0.152
LARGURA_ABA = math.hypot(DOBRADICA_X, BORDA_Y - DOBRADICA_Y)
ANGULO_FECHADA = math.degrees(math.atan2(DOBRADICA_Y - BORDA_Y, DOBRADICA_X))
ALTURA_ABA, CENTRO_ABA_Z = 0.37, 0.365
PECAS_DA_FRENTE = ("Ziper", "HexPeito", "FaixaLuz0", "FaixaLuz1", "FaixaLuz2")

# Os dois braços fazem o mesmo gesto, espelhado:
# (ombro, cotovelo, abre, torce, tronco, cabeça, abas)
POSES = [
    (0,    0,    0,  0,  0, 0,   0),
    (-12, -60,   0, 30,  1, 2,   0),
    (-18, -100, -4, 55,  2, 4,   0),
    (-20, -104, -4, 58,  2, 6,   6),
    (-18, -90,  10, 40,  3, 9,  60),
    (-14, -70,  24, 20,  3, 13, 115),
    (-12, -60,  30, 10,  3, 16, 138),
    (-12, -62,  30, 10,  3, 18, 140),
]


def catmull_rom(p0, p1, p2, p3, t):
    return 0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                  + (3 * p1 - p0 - 3 * p2 + p3) * t ** 3)


def pose_do_quadro(quadro):
    ultima = len(POSES) - 1
    posicao = quadro / (QUADROS - 1) * ultima
    i = min(int(posicao), ultima - 1)
    t = posicao - i
    vizinhas = [POSES[max(i - 1, 0)], POSES[i], POSES[i + 1], POSES[min(i + 2, ultima)]]
    angulos = [catmull_rom(*(v[campo] for v in vizinhas), t) for campo in range(7)]
    angulos[6] = max(angulos[6], 0.0)
    return angulos


def paleta_do_zane():
    cores = set()
    for vista, _ in c.VISTAS_JOGO:
        img = c._ler_png(os.path.join(PASTA_ZANE, f"zane_andar_{vista}.png"))
        cores |= {tuple(p) for p in np.round(img[img[..., 3] > 0][:, :3] * 255).astype(int)}
    return sorted(cores)


def montar_abas(mt):
    """As duas abas da frente, o forro, os bolsos de dentro e a camiseta que
    aparece quando a jaqueta abre. Devolve as peças que só existem aberta."""
    tronco = bpy.data.objects["Tronco"]
    pecas = [c.caixa("CasacoDentro", (0.26, 0.012, 0.36), (0, BORDA_Y, CENTRO_ABA_Z), mt["camiseta"], tronco)]
    for lado in (-1, 1):
        aba = c.pivo(f"Aba{lado}", (DOBRADICA_X * lado, DOBRADICA_Y, CENTRO_ABA_Z), tronco,
                     (0, 0, ANGULO_FECHADA * lado))
        meio = -LARGURA_ABA / 2 * lado
        borda = -LARGURA_ABA * lado
        pecas += [
            # A face de fora (jaqueta) e a de dentro (forro), um pouco atrás dela.
            c.caixa(f"AbaFora{lado}", (LARGURA_ABA, 0.018, ALTURA_ABA), (0, 0, 0), mt["jaqueta"], aba,
                    desloc=(meio, 0, 0)),
            c.caixa(f"AbaForro{lado}", (LARGURA_ABA - 0.01, 0.006, ALTURA_ABA - 0.02), (0, 0, 0),
                    mt["jaqueta_escura"], aba, desloc=(meio, 0.011, 0)),
            # A borda livre: o zíper, metade em cada aba.
            c.caixa(f"AbaZiper{lado}", (0.012, 0.022, ALTURA_ABA), (0, 0, 0), mt["grafite"], aba,
                    desloc=(borda + 0.006 * lado, 0, 0)),
            # A linha de luz que corre por dentro, rente à borda.
            c.caixa(f"AbaLuz{lado}", (0.008, 0.008, ALTURA_ABA - 0.04), (0, 0, 0), mt["luz"], aba,
                    desloc=(borda + 0.02 * lado, 0.016, 0)),
        ]
        # Dois bolsos no forro, cada um com uma peça espetada para fora: o que ele
        # carrega (cápsulas, cabos, um módulo com luz).
        for i, z in enumerate((0.07, -0.08)):
            x = meio + 0.012 * lado
            pecas += [
                c.caixa(f"Bolso{lado}{i}", (0.07, 0.012, 0.08), (0, 0, 0), mt["grafite"], aba,
                        desloc=(x, 0.018, z)),
                c.caixa(f"BolsoPeca{lado}{i}", (0.022, 0.014, 0.05), (0, 0, 0), mt["metal"], aba,
                        desloc=(x - 0.014 * lado, 0.02, z + 0.05)),
                c.caixa(f"BolsoLuz{lado}{i}", (0.012, 0.016, 0.012), (0, 0, 0), mt["luz"], aba,
                        desloc=(x + 0.016 * lado, 0.022, z + 0.03)),
            ]
        # O que estava pintado na frente da jaqueta vai junto com a aba do lado.
        if lado > 0:
            for i, z in enumerate((0.47, 0.44, 0.41)):
                pecas.append(c.caixa(f"AbaFaixaLuz{i}", (0.07 - 0.012 * i, 0.01, 0.01), (0, 0, 0), mt["luz"],
                                     aba, desloc=(-0.05 * lado, -0.012, z - CENTRO_ABA_Z)))
        else:
            pecas.append(c.cone("AbaHex", 0.03, 0.03, 0.01, (0, 0, 0), mt["luz"], aba, (90, 0, 0), lados=6,
                                desloc=(-0.035 * lado, 0.46 - CENTRO_ABA_Z, 0.012)))
    return pecas


def girar(parado, nome, x=0.0, y=0.0, z=0.0):
    rot, _ = parado[nome]
    bpy.data.objects[nome].rotation_euler = (rot[0] + math.radians(x), rot[1] + math.radians(y),
                                             rot[2] + math.radians(z))


def aplicar_pose(parado, pecas_abertas, pose):
    ombro, cotovelo, abre, torce, tronco, cabeca, abas = pose
    c.restaurar_pose(parado)
    # Abrir e torcer o braço: os dois lados giram ao contrário (lado -1 é o
    # direito). Torcer em Z vira a dobra do cotovelo para dentro, e o antebraço
    # cruza o peito em vez de apontar para a frente.
    for braco, lado in (("BracoDir", -1), ("BracoEsq", 1)):
        girar(parado, f"{braco}Ombro", ombro, -abre * lado, -torce * lado)
        girar(parado, f"{braco}Cotovelo", cotovelo)
    girar(parado, "Tronco", tronco)
    girar(parado, "Cabeca", cabeca)
    for lado in (-1, 1):
        bpy.data.objects[f"Aba{lado}"].rotation_euler = (0, 0, math.radians((ANGULO_FECHADA + abas) * lado))
    aberta = abas > 0.5
    for obj in pecas_abertas:
        obj.hide_render = not aberta
    for nome in PECAS_DA_FRENTE:
        bpy.data.objects[nome].hide_render = aberta
    bpy.context.view_layer.update()


def vistas_pedidas():
    argumentos = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return [v for v in c.VISTAS_JOGO if not argumentos or v[0] in argumentos]


def main():
    c.DETALHE = gz["DETALHE"]
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = gz["criar_materiais"]()
    c.usar_colecao("Zane")
    raiz = gz["montar"](mt)
    pecas_abertas = montar_abas(mt)
    c.achatar_sombra("Rosto")
    gz["expressao"]("normal")
    gz["esconder_boca"]()
    cam = c.criar_camera()
    c.criar_luzes()
    parado = c.guardar_pose()
    paleta = paleta_do_zane()

    for vista, angulo in vistas_pedidas():
        quadros = []
        for i in range(QUADROS):
            aplicar_pose(parado, pecas_abertas, pose_do_quadro(i))
            img, ind, _ = c.renderizar_vista(cam, raiz, materiais, angulo, c.QUADRO_JOGO_2X, c.PX_POR_M_JOGO_2X,
                                             c.PE_JOGO_2X)
            quadros.append(c.contorno(img, ind, materiais))
        c.restaurar_pose(parado)
        tira = np.concatenate(c.aplicar_paleta(quadros, paleta), axis=1)
        c.salvar_png(tira, os.path.join(PASTA_ZANE, f"zane_casaco_{vista}.png"))
        print(f"[casaco] {vista}: pronto")
    print("[casaco] pronto")


main()
