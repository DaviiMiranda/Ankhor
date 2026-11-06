# gerar_correr.py — anima o ZANE, a CLARICE e a DIANA correndo, de lado.
#
# Como rodar (sem abrir a janela do Blender; precisa dos gerar_<nome>.py e do
# gerar_gabriel_correr.py ao lado):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_correr.py
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_correr.py -- zane
#
# Sem nome, faz os três. O que sai:
#   assets/sprites/personagens/<nome>/<nome>_correr_lado.png
#       24 quadros de 96 x 112 lado a lado, na paleta da caminhada do
#       personagem (as cores não mudam de uma tira para a outra).
#
# Usado na fuga do fim do Bunker (cenas/salas/bunker/fuga.tscn), onde o grupo
# corre na frente do Gabriel. Só a vista de lado, porque é a única que a fuga usa.
#
# A ANIMAÇÃO
#   É a mesma corrida do Gabriel (gerar_gabriel_correr.py, onde estão as
#   fórmulas): coxa, joelho, ombro e cotovelo em função da fase φ, o tronco
#   inclinado para a frente e o quadril numa onda suave (a série de Fourier
#   da altura da perna mais esticada). Os quatro personagens têm o mesmo
#   esqueleto (comum.py: PernaDirQuadril, BracoEsqCotovelo...), então a pose
#   vale para todos. As medidas da perna usadas na altura do quadril são as do
#   Gabriel; como os quatro têm altura parecida, o pé fica, no máximo, um pixel
#   acima ou abaixo do chão.
#
#   Com 24 quadros (15° cada) e a pisada nos quadros 6 e 18, o jogo mostra a
#   tira na mesma velocidade da corrida do Gabriel: um quadro a cada 5 px
#   andados (Gabriel.px_por_quadro_correndo).

import os
import sys

sys.dont_write_bytecode = True
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA_SCRIPT)
import comum as c  # noqa: E402
import numpy as np  # noqa: E402
import bpy  # noqa: E402


def carregar(arquivo):
    # Lê um gerador sem rodar o main() dele, para usar as funções.
    caminho = os.path.join(PASTA_SCRIPT, arquivo)
    fonte = open(caminho, encoding="utf-8").read().rsplit("\nmain()", 1)[0]
    modulo = {"__file__": caminho, "__name__": arquivo.replace(".py", "")}
    exec(compile(fonte, arquivo, "exec"), modulo)
    return modulo


corrida = carregar("gerar_gabriel_correr.py")


def montar_zane(g, mt):
    raiz = g["montar"](mt)
    c.achatar_sombra("Rosto")
    g["expressao"](g["EXPRESSOES"][0])
    g["esconder_boca"]()
    return raiz


def montar_diana(g, mt):
    return montar_zane(g, mt)


def montar_clarice(g, mt):
    raiz = g["montar_clarice"](mt, None)
    c.achatar_sombra("Rosto")
    g["pose_em_pe"]()
    g["expressao"]("normal")
    return raiz


PERSONAGENS = {
    "zane": ("gerar_zane.py", "Zane", montar_zane),
    "diana": ("gerar_diana.py", "Diana", montar_diana),
    "clarice": ("gerar_clarice.py", "Clarice", montar_clarice),
}


def paleta_da_caminhada(nome):
    # As cores que já existem na tira de caminhada de lado: a corrida usa só elas.
    img = c._ler_png(os.path.join(c.PASTA_SPRITES, nome, f"{nome}_andar_lado.png"))
    return sorted({tuple(p) for p in np.round(img[img[..., 3] > 0][:, :3] * 255).astype(int)})


def gerar(nome):
    arquivo, colecao, montar = PERSONAGENS[nome]
    g = carregar(arquivo)
    c.DETALHE = g["DETALHE"]
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = g["criar_materiais"]()
    c.usar_colecao(colecao)
    raiz = montar(g, mt)
    cam = c.criar_camera()
    c.criar_luzes()
    parado = c.guardar_pose()

    quadros = []
    total = corrida["QUADROS_CORRER"]
    for q in range(total):
        corrida["pose_correr"](parado, 360 * q / total)
        img, ind, _ = corrida["renderizar"](cam, raiz, materiais, 90)
        quadros.append(c.contorno(img, ind, materiais))
        print(f"[correr {nome}] quadro {q + 1}/{total}")
    c.restaurar_pose(parado)

    tira = np.concatenate(c.aplicar_paleta(quadros, paleta_da_caminhada(nome)), axis=1)
    saida = os.path.join(c.PASTA_SPRITES, nome, f"{nome}_correr_lado.png")
    c.salvar_png(tira, saida)
    print(f"[correr {nome}] pronto: {saida}")


def main():
    argumentos = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    for nome in argumentos or list(PERSONAGENS):
        gerar(nome)


main()
