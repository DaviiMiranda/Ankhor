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
# Nas vistas em que aparecem duas mãos fica a mancha de maior x (a mão da direita
# do quadro), e manchas à esquerda da coluna COLUNA_MIN (a outra mão, que some e
# volta durante a caminhada) são ignoradas, para a lanterna não pular de mão.
# Se um quadro não tem mão visível, vale a posição do quadro anterior.
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
COLUNA_MIN = 44


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


def mao_do_quadro(quadro):
    rgb = quadro[..., :3].astype(np.float64)
    pele = np.zeros(quadro.shape[:2], dtype=bool)
    for cor in PELE:
        pele |= np.sqrt(((rgb - np.array(cor)) ** 2).sum(axis=-1)) < LIMITE_COR
    pele &= quadro[..., 3] > 0
    pele[:LINHA_MIN] = False
    pele[LINHA_MAX:] = False
    achadas = [m for m in manchas(pele) if len(m) >= MANCHA_MINIMA]
    centros = [(sum(p[0] for p in m) / len(m), sum(p[1] for p in m) / len(m)) for m in achadas]
    centros = [c for c in centros if c[0] >= COLUNA_MIN]
    if not centros:
        return None
    x, y = max(centros)
    return [round(x + 0.5, 1), round(y + 0.5, 1)]


def medir_tira(caminho):
    tira = np.array(Image.open(caminho).convert("RGBA"))
    pontos = []
    ultimo = None
    for i in range(tira.shape[1] // LARGURA):
        ponto = mao_do_quadro(tira[:, i * LARGURA:(i + 1) * LARGURA])
        ultimo = ponto or ultimo
        pontos.append(ultimo)
    primeiro = next((p for p in pontos if p), [LARGURA / 2, 66])
    return [p or primeiro for p in pontos]


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
