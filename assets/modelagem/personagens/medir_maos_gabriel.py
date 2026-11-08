# medir_maos_gabriel.py — acha, em cada quadro dos sprites do Gabriel, onde está
# a mão que segura a lanterna, e grava a tabela em
# scripts/personagens/maos_do_gabriel.gd (uma constante que o gabriel.gd usa).
#
# Como rodar (Python 3 + numpy + Pillow):
#
#   python assets/modelagem/personagens/medir_maos_gabriel.py
#
# Rode de novo se os sprites do Gabriel mudarem (gerar_gabriel.py).
#
# Como acha a mão: a mão é o único pedaço de pele abaixo do moletom. Um pixel
# conta como pele se a cor dele está perto de uma das duas cores de pele do
# personagem (distância euclidiana no espaço RGB, menor que LIMITE_COR) e se
# está na faixa de altura dos braços caídos (linhas 56 a 90 do quadro de
# 96 x 112). Os pixels de pele ficam em manchas conexas (BFS nos 4 vizinhos);
# o centro de cada mancha é a média das posições dos seus pixels,
#
#     centro = (soma dos x / n, soma dos y / n)
#
# A lanterna fica sempre na MESMA mão. O primeiro quadro da tira escolhe a mão
# (a mancha de maior x, a da direita do quadro) e dali em diante a mão é seguida
# quadro a quadro: vale a mancha mais perto do ponto previsto, que é o anterior
# mais a velocidade que a mão vinha tendo,
#
#     p_previsto = 2 * p_anterior - p_anterior_do_anterior
#
# desde que fique a menos de ERRO_MAXIMO_DA_PREVISAO pixels dele. Quando as duas
# mãos se cruzam (o braço de lá vem para cá), é a velocidade que diz qual é
# qual. Sem velocidade (no segundo quadro e depois de um quadro sem mão), valem
# só as manchas a menos de SALTO_MAXIMO pixels do último ponto achado, e entre
# elas a de maior x. Antes, a escolha era "a mancha de maior x
# de cada quadro", e a lanterna saltava para a outra mão sempre que a primeira
# sumia atrás do corpo (na vista de três quartos o salto passava de 17 pixels).
#
# Quadros em que a mão seguida não aparece (atrás do corpo) são preenchidos por
# interpolação linear entre o último e o próximo quadro com mão, contando a tira
# como um ciclo (depois do último quadro vem o primeiro).
#
# O braço que segura a lanterna balança menos que o outro, então o balanço em x
# é reduzido a AMORTECIMENTO do original em volta da média da tira:
#
#     x = media + AMORTECIMENTO * (x_medido - media)
#
# O que sai: MAOS[vista][tira][quadro] = Vector2(x, y), com tira "imovel" (1 quadro),
# "parado" (8) ou "andar" (12), em pixels do quadro (96 x 112), do canto de cima
# à esquerda.

import os
from collections import deque

import numpy as np
from PIL import Image

PASTA_PROJETO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PASTA_SPRITES = os.path.join(PASTA_PROJETO, "assets", "sprites", "personagens", "gabriel")
SAIDA = os.path.join(PASTA_PROJETO, "scripts", "personagens", "maos_do_gabriel.gd")

VISTAS = ["lado", "frente", "tres_quartos", "costas", "tres_quartos_costas"]
LARGURA = 96
PELE = [(185, 130, 96), (119, 86, 70)]
LIMITE_COR = 18.0
LINHA_MIN, LINHA_MAX = 56, 90
MANCHA_MINIMA = 3
SALTO_MAXIMO = 7.0
ERRO_MAXIMO_DA_PREVISAO = 7.0
AMORTECIMENTO = 0.6


def manchas(mascara):
    altura, largura = mascara.shape
    visto = np.zeros_like(mascara)
    achadas = []
    for y, x in np.argwhere(mascara):
        if visto[y, x]:
            continue
        fila = deque([(y, x)])
        visto[y, x] = True
        pontos = []
        while fila:
            py, px = fila.popleft()
            pontos.append((px, py))
            for vy, vx in ((py - 1, px), (py + 1, px), (py, px - 1), (py, px + 1)):
                if 0 <= vy < altura and 0 <= vx < largura and mascara[vy, vx] and not visto[vy, vx]:
                    visto[vy, vx] = True
                    fila.append((vy, vx))
        achadas.append(pontos)
    return achadas


def centros_do_quadro(quadro):
    rgb = quadro[..., :3].astype(np.float64)
    pele = np.zeros(quadro.shape[:2], dtype=bool)
    for cor in PELE:
        pele |= np.sqrt(((rgb - np.array(cor)) ** 2).sum(axis=-1)) < LIMITE_COR
    pele &= quadro[..., 3] > 0
    pele[:LINHA_MIN] = False
    pele[LINHA_MAX:] = False
    achadas = [m for m in manchas(pele) if len(m) >= MANCHA_MINIMA]
    return [(sum(p[0] for p in m) / len(m) + 0.5, sum(p[1] for p in m) / len(m) + 0.5) for m in achadas]


def distancia(a, b):
    return float(np.hypot(a[0] - b[0], a[1] - b[1]))


def seguir_a_mao(quadros_de_centros):
    trilha = []
    for centros in quadros_de_centros:
        achados = [p for p in trilha if p]
        escolhido = None
        if centros and not achados:
            escolhido = max(centros)
        elif centros:
            if len(trilha) >= 2 and trilha[-1] and trilha[-2]:
                previsto = (2 * trilha[-1][0] - trilha[-2][0], 2 * trilha[-1][1] - trilha[-2][1])
                perto = [c for c in centros if distancia(c, previsto) <= ERRO_MAXIMO_DA_PREVISAO]
                escolhido = min(perto, key=lambda c: distancia(c, previsto)) if perto else None
            else:
                perto = [c for c in centros if distancia(c, achados[-1]) <= SALTO_MAXIMO]
                escolhido = max(perto) if perto else None
        trilha.append(escolhido)
    return trilha


def preencher_buracos(trilha, padrao):
    achados = [i for i, p in enumerate(trilha) if p]
    if not achados:
        return [padrao for _ in trilha]
    total = len(trilha)
    pontos = []
    for i in range(total):
        if trilha[i]:
            pontos.append(trilha[i])
            continue
        antes = max(j for j in range(i - total, i) if trilha[j % total])
        depois = min(j for j in range(i + 1, i + total + 1) if trilha[j % total])
        a, b = trilha[antes % total], trilha[depois % total]
        t = (i - antes) / (depois - antes)
        pontos.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return pontos


def medir_tira(caminho):
    tira = np.array(Image.open(caminho).convert("RGBA"))
    quadros = [centros_do_quadro(tira[:, i * LARGURA:(i + 1) * LARGURA]) for i in range(tira.shape[1] // LARGURA)]
    pontos = preencher_buracos(seguir_a_mao(quadros), (LARGURA / 2, 66))
    media = sum(p[0] for p in pontos) / len(pontos)
    return [[round(media + AMORTECIMENTO * (x - media), 1), round(y, 1)] for x, y in pontos]


def main():
    tabela = {}
    for vista in VISTAS:
        tabela[vista] = {
            "imovel": medir_tira(os.path.join(PASTA_SPRITES, f"gabriel_{vista}.png")),
            "parado": medir_tira(os.path.join(PASTA_SPRITES, f"gabriel_parado_{vista}.png")),
            "andar": medir_tira(os.path.join(PASTA_SPRITES, f"gabriel_andar_{vista}.png")),
        }
        for tira, pontos in tabela[vista].items():
            xs = [p[0] for p in pontos]
            ys = [p[1] for p in pontos]
            print(f"  {vista:20s} {tira:7s} x {min(xs):5.1f}..{max(xs):5.1f}  y {min(ys):5.1f}..{max(ys):5.1f}")
    linhas = ["const MAOS := {"]
    for vista, tiras in tabela.items():
        linhas.append(f'\t"{vista}": {{')
        for tira, pontos in tiras.items():
            quadros = ", ".join(f"Vector2({x}, {y})" for x, y in pontos)
            linhas.append(f'\t\t"{tira}": [{quadros}],')
        linhas.append("\t},")
    linhas += ["}", ""]
    with open(SAIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(linhas))
    print("  salvo:", os.path.relpath(SAIDA, PASTA_PROJETO))


if __name__ == "__main__":
    main()
