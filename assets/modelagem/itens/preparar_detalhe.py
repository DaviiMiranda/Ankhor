# preparar_detalhe.py — prepara a imagem detalhada de um item (a que aparece
# na tela de "item novo") a partir da imagem crua que saiu do gerador de imagem.
#
# Como rodar (Python 3 + numpy + Pillow):
#
#   python assets/modelagem/itens/preparar_detalhe.py <imagem_crua> <id_do_item>
#
#   ex.: python assets/modelagem/itens/preparar_detalhe.py ~/Downloads/lanterna.webp lanterna
#
# O que sai:
#   assets/sprites/itens/<id_do_item>_detalhe.png   RGBA, fundo transparente, cortada rente
#
# Depois, no recurso do item (dados/itens/<id_do_item>.tres), aponte o campo
# "Imagem detalhe" para o PNG. Item sem esse campo mostra o ícone ampliado.
#
# Por que o fundo precisa sair: o gerador de imagem entrega o objeto sobre um
# fundo cinza chapado, e a tela de item novo desenha o objeto sobre uma luz
# escura. Um retângulo cinza em volta estragaria tudo.
#
# A matemática ("color to alpha"): seja f a cor do fundo e c a cor de um pixel.
# Medimos a distância euclidiana d = |c - f| no espaço RGB. O alfa do pixel é
#
#     a = clamp((d - d0) / (d1 - d0), 0, 1)
#
# ou seja, 0 (transparente) perto do fundo, 1 (opaco) longe dele, com uma
# rampa suave no meio para o contorno do objeto não virar serrilhado. Um
# pixel de borda é uma mistura "a * objeto + (1 - a) * fundo"; para não deixar
# um halo cinza, recuperamos a cor do objeto invertendo a mistura:
#
#     objeto = (c - (1 - a) * f) / a
#
# Isso também faz o brilho em volta da lente virar um halo quente e translúcido,
# em vez de um borrão cinza.
#
# Sombra no chão: o gerador às vezes desenha uma sombra embaixo do objeto (o
# rádio tem). Sombra é o próprio fundo, só que mais escuro: a cor dela fica na
# reta que vai do preto até a cor do fundo, c ≈ k * f, com 0 < k < 1. Por isso,
# em vez de medir a distância até o ponto f, medimos a distância até essa reta.
# A projeção de c na reta dá o k:
#
#     k = (c · f) / (f · f)        (produto escalar)
#
# e o ponto mais perto é k * f (com k limitado entre K_MINIMO e 1). A distância
# d = |c - k * f| entra na mesma rampa do alfa, e o "fundo" que se tira na
# inversão da mistura passa a ser k * f. Com K_MINIMO = 0,4 o contorno preto e
# as partes cinza do objeto ficam longe da reta e não somem.
#
# Só o fundo ligado às bordas da imagem sai: uma busca em largura (BFS) parte
# de todos os pixels da borda e anda pelos vizinhos que parecem fundo. Uma
# parte do objeto da mesma cor do fundo, mas cercada por ele (um vão dentro do
# desenho, um reflexo), não é alcançada e continua opaca. Uma segunda BFS,
# partindo do centro, fica só com a mancha do objeto e apaga os pontinhos
# soltos que o ruído do JPEG deixa no fundo.

import argparse
import os
from collections import deque

import numpy as np
from PIL import Image

PASTA_PROJETO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PASTA_ITENS = os.path.join(PASTA_PROJETO, "assets", "sprites", "itens")

D0 = 4.0      # até aqui o pixel é fundo puro (alfa 0)
D1 = 13.0     # daqui para cima o pixel é objeto puro (alfa 1)
K_MINIMO = 0.4  # sombra mais escura que 40% do fundo já conta como objeto
MARGEM = 8    # pixels de folga em volta do objeto
LIMITE_LADO = 512


def cor_do_fundo(rgb):
    """A cor mais comum nas quatro bordas da imagem (o fundo chapado)."""
    bordas = np.concatenate([rgb[0, :], rgb[-1, :], rgb[:, 0], rgb[:, -1]])
    valores, contagens = np.unique(bordas, axis=0, return_counts=True)
    return valores[np.argmax(contagens)].astype(np.float64)


def busca_em_largura(pode_andar, sementes):
    """BFS: marca todo pixel alcançável a partir das sementes, andando só para
    os 4 vizinhos onde pode_andar é verdadeiro."""
    altura, largura = pode_andar.shape
    alcancado = np.zeros_like(pode_andar)
    fila = deque()
    for y, x in sementes:
        if pode_andar[y, x] and not alcancado[y, x]:
            alcancado[y, x] = True
            fila.append((y, x))
    while fila:
        y, x = fila.popleft()
        for vy, vx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= vy < altura and 0 <= vx < largura and pode_andar[vy, vx] and not alcancado[vy, vx]:
                alcancado[vy, vx] = True
                fila.append((vy, vx))
    return alcancado


def fundo_alcancavel(parece_fundo):
    altura, largura = parece_fundo.shape
    bordas = [(y, x) for y in range(altura) for x in (0, largura - 1)]
    bordas += [(y, x) for x in range(largura) for y in (0, altura - 1)]
    return busca_em_largura(parece_fundo, bordas)


def so_o_objeto(rgba):
    """Apaga os pontinhos soltos (ruído do JPEG que passou do limiar): fica só
    a mancha opaca ligada ao pixel mais opaco do centro da imagem."""
    visivel = rgba[..., 3] > 12
    altura, largura = visivel.shape
    centro = np.argwhere(visivel)
    meio = np.array([altura / 2, largura / 2])
    semente = tuple(centro[np.argmin(((centro - meio) ** 2).sum(axis=1))])
    objeto = busca_em_largura(visivel, [semente])
    rgba[~objeto] = 0
    return rgba


def remover_fundo(rgb):
    fundo = cor_do_fundo(rgb)
    pix = rgb.astype(np.float64)
    k = np.clip((pix @ fundo) / (fundo @ fundo), K_MINIMO, 1.0)[..., None]
    fundo_local = k * fundo
    distancia = np.sqrt(((pix - fundo_local) ** 2).sum(axis=2))
    alfa = np.clip((distancia - D0) / (D1 - D0), 0.0, 1.0)
    alfa[~fundo_alcancavel(alfa < 1.0)] = 1.0
    seguro = np.maximum(alfa, 1e-3)[..., None]
    objeto = (pix - (1.0 - alfa[..., None]) * fundo_local) / seguro
    objeto = np.clip(objeto, 0, 255)
    saida = np.zeros(rgb.shape[:2] + (4,), dtype=np.uint8)
    saida[..., :3] = objeto.round().astype(np.uint8)
    saida[..., 3] = (alfa * 255).round().astype(np.uint8)
    saida[alfa == 0.0, :3] = 0
    return saida


def cortar_rente(rgba):
    visivel = rgba[..., 3] > 12
    linhas = np.where(visivel.any(axis=1))[0]
    colunas = np.where(visivel.any(axis=0))[0]
    y0 = max(linhas[0] - MARGEM, 0)
    y1 = min(linhas[-1] + MARGEM + 1, rgba.shape[0])
    x0 = max(colunas[0] - MARGEM, 0)
    x1 = min(colunas[-1] + MARGEM + 1, rgba.shape[1])
    return rgba[y0:y1, x0:x1]


def main():
    parser = argparse.ArgumentParser(description="Prepara a imagem detalhada de um item (fundo transparente, corte rente).")
    parser.add_argument("entrada", help="imagem crua (png, jpg ou webp)")
    parser.add_argument("item", help="id do item, o mesmo de dados/itens/<id>.tres")
    args = parser.parse_args()

    rgb = np.array(Image.open(args.entrada).convert("RGB"))
    rgba = cortar_rente(so_o_objeto(remover_fundo(rgb)))
    imagem = Image.fromarray(rgba, "RGBA")
    if max(imagem.size) > LIMITE_LADO:
        escala = LIMITE_LADO / max(imagem.size)
        imagem = imagem.resize((round(imagem.width * escala), round(imagem.height * escala)), Image.LANCZOS)
    caminho = os.path.join(PASTA_ITENS, f"{args.item}_detalhe.png")
    imagem.save(caminho, optimize=True)
    print("  salvo:", os.path.relpath(caminho, PASTA_PROJETO), f"({imagem.width}x{imagem.height})")


if __name__ == "__main__":
    main()
