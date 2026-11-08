# gerar_gabriel_correr.py — anima o Gabriel correndo, nas cinco vistas de jogo.
#
# Como rodar (sem abrir a janela do Blender; precisa do gerar_gabriel.py ao lado):
#
#   blender -b --factory-startup --python assets/modelagem/personagens/gerar_gabriel_correr.py
#
# O que sai:
#   assets/sprites/personagens/gabriel/gabriel_correr_<vista>.png
#       24 quadros de 96 x 112 lado a lado, um arquivo por vista, na paleta dele.
#   scripts/personagens/maos_correndo_gabriel.gd
#       onde fica, em cada quadro, a mão que segura o item (o braço de hack sai dela).
#
# ---------------------------------------------------------------------------
# A ANIMAÇÃO
# ---------------------------------------------------------------------------
#
# Mesma ideia da caminhada (comum.pose_andar), com a mesma fase φ, mas o dobro de
# quadros: cada quadro avança 15°, os pés se cruzam nos quadros 0 e 12 e as pisadas
# caem nos quadros 6 e 18. Um quadro da caminhada vale dois daqui, então o jogo
# troca de uma tira para a outra no mesmo ponto do ciclo, sem salto. O que muda é
# o tamanho do gesto:
#
#   coxa      = C0 - C · sen(φ) - E · max(0, -cos φ)^1,5
#               vai mais para a frente que para trás; o último termo adianta a
#               coxa enquanto a perna aguenta o peso (cos φ < 0)
#   joelho    = J0 + J · max(0, cos φ)^1,2 + F · max(0, -cos φ)^1,5
#               dobra muito quando a perna volta pelo ar (o calcanhar sobe) e um
#               pouco ao aguentar o peso, como uma mola
#   ombro     = A · sen(φ), ao contrário da perna do mesmo lado
#   cotovelo  = -(B + D · (1 - sen(φ - ATRASO)) / 2), sempre dobrado, mais ainda
#               à frente. A onda não tem quina (um max(0, ...) mudaria de direção
#               de repente) e vem atrasada em relação ao ombro: o antebraço segue
#               o braço em vez de mexer junto, e é isso que deixa o gesto suave
#   tronco    = inclinado para a frente, torcendo com os braços; a cabeça desfaz
#               parte disso, porque ele olha para onde corre
#
# As duas pernas usam os mesmos ângulos, meio ciclo defasados. Na pose parada elas
# são um pouco diferentes (coxas -3° e 3°, joelhos 4° e 2°); somar a corrida em cima
# disso faz um passo afundar mais que o outro, e ele manca. Por isso aqui o ângulo é
# absoluto, a partir da média das duas (JOELHO_REPOUSO).
#
# A altura do quadril sai da perna mais esticada. A distância vertical do quadril
# até a sola de uma perna é
#
#   h = L1 · cos(a) + L2 · cos(a + b) + SOLA
#
# (a = giro da coxa, b = giro do joelho). A altura crua seria
#
#   H(φ) = max(h da direita, h da esquerda) + VOO · sen²(2φ)
#
# mas o max tem uma quina a cada passo: o corpo desce e volta de repente, e é isso
# que parece travado. Então fica só o começo da série de Fourier de H, a média e a
# onda na frequência dos passos, sem quina nenhuma:
#
#   H̃(φ) = M + A · cos(2φ) + B · sen(2φ)
#   M = média de H     A = 2 · média de H · cos(2φ)     B = 2 · média de H · sen(2φ)
#
# O pé pode ficar um pouco acima ou abaixo do chão (H - H̃, o script imprime o
# máximo), bem menos visível que o tranco.
#
# A mão não é medida na imagem, como em medir_maos_gabriel.py: correndo, as duas
# mãos cruzam o corpo, e a "mão mais à direita" trocaria de lado no meio do ciclo,
# fazendo o item pular. Em cada vista fica a mão que está mais à direita na
# pose parada (a mesma regra da medição), seguida do começo ao fim pelo modelo 3D:
#
#   px = u · largura         py = (1 - v) · altura
#
# onde (u, v) é a posição do ponto no enquadramento (world_to_camera_view).

import math
import os
import sys

sys.dont_write_bytecode = True
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA_SCRIPT)
import comum as c  # noqa: E402
import numpy as np  # noqa: E402
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402

# Reaproveita as funções do gerar_gabriel.py sem rodar o main() dele.
_fonte = open(os.path.join(PASTA_SCRIPT, "gerar_gabriel.py"), encoding="utf-8").read()
_fonte = _fonte.rsplit("\nmain()", 1)[0]
gg = {"__file__": os.path.join(PASTA_SCRIPT, "gerar_gabriel.py"), "__name__": "gerar_gabriel"}
exec(compile(_fonte, "gerar_gabriel.py", "exec"), gg)

PASTA_GABRIEL = os.path.join(c.PASTA_SPRITES, "gabriel")
SAIDA_TABELA = os.path.join(c.PASTA_PROJETO, "scripts", "personagens", "maos_correndo_gabriel.gd")

QUADROS_CORRER = 24                 # o dobro da caminhada (comum.QUADROS_ANDAR)
COXA_MEIO, COXA, COXA_APOIO = -9, 35, 20
JOELHO_BASE, JOELHO_AR, JOELHO_APOIO = 12, 78, 32
JOELHO_REPOUSO = 3                  # média dos joelhos na pose parada; a das coxas é 0
OMBRO, COTOVELO, COTOVELO_FRENTE, ATRASO_COTOVELO = 36, 66, 18, 35
INCLINACAO_TRONCO, TORCAO_TRONCO = 13, 5
CABECA_LEVANTA, CABECA_DESTORCE = -10, 4
PE_NO_AR = 28                       # a ponta do pé cai quando a perna volta pelo ar
COXA_M, CANELA_M, SOLA_M = 0.41, 0.37, 0.10
VOO_M = 0.018


def paleta_do_gabriel():
    cores = set()
    for vista, _ in c.VISTAS_JOGO:
        img = c._ler_png(os.path.join(PASTA_GABRIEL, f"gabriel_andar_{vista}.png"))
        cores |= {tuple(p) for p in np.round(img[img[..., 3] > 0][:, :3] * 255).astype(int)}
    return sorted(cores)


def girar(parado, nome, x=0.0, z=0.0):
    rot, _ = parado[nome]
    bpy.data.objects[nome].rotation_euler = (rot[0] + math.radians(x), rot[1], rot[2] + math.radians(z))


def altura_da_perna(a_graus, b_graus):
    a = math.radians(a_graus)
    return COXA_M * math.cos(a) + CANELA_M * math.cos(a + math.radians(b_graus)) + SOLA_M


def angulos_da_perna(fase):
    phi = math.radians(fase)
    no_ar = max(0.0, math.cos(phi))
    no_apoio = max(0.0, -math.cos(phi))
    coxa = COXA_MEIO - COXA * math.sin(phi) - COXA_APOIO * no_apoio ** 1.5
    joelho = JOELHO_REPOUSO + JOELHO_BASE + JOELHO_AR * no_ar ** 1.2 + JOELHO_APOIO * no_apoio ** 1.5
    return coxa, joelho, no_ar


def altura_crua(fase):
    alturas = [altura_da_perna(*angulos_da_perna(fase + desloc)[:2]) for desloc in (0, 180)]
    return max(alturas) + VOO_M * math.sin(math.radians(2 * fase)) ** 2


def onda_do_quadril(amostras=720):
    fases = [360 * i / amostras for i in range(amostras)]
    alturas = [altura_crua(fase) for fase in fases]
    media = sum(alturas) / amostras
    a = 2 * sum(h * math.cos(math.radians(2 * f)) for h, f in zip(alturas, fases)) / amostras
    b = 2 * sum(h * math.sin(math.radians(2 * f)) for h, f in zip(alturas, fases)) / amostras
    return media, a, b


ONDA_QUADRIL = onda_do_quadril()


def altura_suave(fase):
    media, a, b = ONDA_QUADRIL
    dobro = math.radians(2 * fase)
    return media + a * math.cos(dobro) + b * math.sin(dobro)


def girar_absoluto(parado, nome, x):
    rot, _ = parado[nome]
    bpy.data.objects[nome].rotation_euler = (math.radians(x), rot[1], rot[2])


def pose_correr(parado, fase):
    for perna, desloc in (("PernaDir", 0), ("PernaEsq", 180)):
        coxa, joelho, no_ar = angulos_da_perna(fase + desloc)
        girar_absoluto(parado, f"{perna}Quadril", coxa)
        girar_absoluto(parado, f"{perna}Joelho", joelho)
        # O tornozelo desfaz coxa e joelho (pé reto) e deixa a ponta cair no ar.
        girar_absoluto(parado, f"{perna}Tornozelo", -coxa - joelho + PE_NO_AR * no_ar)
    for braco, desloc in (("BracoDir", 0), ("BracoEsq", 180)):
        seno = math.sin(math.radians(fase + desloc))
        atrasado = math.sin(math.radians(fase + desloc - ATRASO_COTOVELO))
        girar(parado, f"{braco}Ombro", OMBRO * seno)
        girar(parado, f"{braco}Cotovelo", -(COTOVELO + COTOVELO_FRENTE * (1 - atrasado) / 2))
    seno = math.sin(math.radians(fase))
    girar(parado, "Tronco", INCLINACAO_TRONCO, -TORCAO_TRONCO * seno)
    girar(parado, "Cabeca", CABECA_LEVANTA, CABECA_DESTORCE * seno)
    _, pos = parado["Quadril"]
    bpy.data.objects["Quadril"].location = (pos[0], pos[1], altura_suave(fase))
    bpy.context.view_layer.update()


def para_pixel(cam, ponto):
    cena = bpy.context.scene
    u, v, _ = world_to_camera_view(cena, cam, ponto)
    return u * cena.render.resolution_x, (1.0 - v) * cena.render.resolution_y


def posicao_da_mao(cam, braco):
    return para_pixel(cam, bpy.data.objects[f"{braco}Mao"].matrix_world.translation)


def renderizar(cam, raiz, materiais, angulo):
    return c.renderizar_vista(cam, raiz, materiais, angulo, c.QUADRO_JOGO_2X, c.PX_POR_M_JOGO_2X, c.PE_JOGO_2X)


def braco_do_item(cam, raiz, materiais, angulo):
    renderizar(cam, raiz, materiais, angulo)
    bpy.context.view_layer.update()
    return max(("BracoDir", "BracoEsq"), key=lambda braco: posicao_da_mao(cam, braco)[0])


def main():
    c.DETALHE = gg["DETALHE"]
    c.SUAVE = True
    c.cena_vazia()
    materiais, mt = gg["criar_materiais"]()
    c.usar_colecao("Gabriel")
    raiz = gg["montar"](mt)
    c.achatar_sombra("Rosto")
    bpy.data.objects["Boca"].hide_render = True
    bpy.data.objects["BocaAberta"].hide_render = True
    cam = c.criar_camera()
    c.criar_luzes()
    parado = c.guardar_pose()

    bracos = {vista: braco_do_item(cam, raiz, materiais, angulo) for vista, angulo in c.VISTAS_JOGO}
    print("[correr] mão do item:", bracos)
    folga = max(abs(altura_crua(f) - altura_suave(f)) for f in range(360))
    print(f"[correr] pé longe do chão, no máximo: {folga * c.PX_POR_M_JOGO_2X:.1f} px")

    tiras = {vista: [] for vista, _ in c.VISTAS_JOGO}
    maos = {vista: [] for vista, _ in c.VISTAS_JOGO}
    for q in range(QUADROS_CORRER):
        pose_correr(parado, 360 * q / QUADROS_CORRER)
        for vista, angulo in c.VISTAS_JOGO:
            img, ind, _ = renderizar(cam, raiz, materiais, angulo)
            tiras[vista].append(c.contorno(img, ind, materiais))
            bpy.context.view_layer.update()
            maos[vista].append(posicao_da_mao(cam, bracos[vista]))
        print(f"[correr] quadro {q + 1}/{QUADROS_CORRER}")

    paleta = paleta_do_gabriel()
    for vista, quadros in tiras.items():
        tira = np.concatenate(c.aplicar_paleta(quadros, paleta), axis=1)
        c.salvar_png(tira, os.path.join(PASTA_GABRIEL, f"gabriel_correr_{vista}.png"))

    linhas = ["const MAOS_CORRENDO := {"]
    for vista, pontos in maos.items():
        quadros = ", ".join("Vector2(%.1f, %.1f)" % ponto for ponto in pontos)
        linhas.append(f'\t"{vista}": [{quadros}],')
    linhas.append("}")
    with open(SAIDA_TABELA, "w", encoding="utf-8", newline="\n") as arq:
        arq.write("\n".join(linhas) + "\n")
    print("[correr] pronto")


main()
