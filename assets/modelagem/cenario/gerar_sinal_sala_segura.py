# gerar_sinal_sala_segura.py — desenha, por código, o SINAL DA SALA SEGURA: a
# lâmpada verde com a plaquinha que fica em cima (ou do lado) da porta da sala
# segura de cada fase (docs/mecanicas/vida_e_checkpoint.md, "Sala segura").
#
# Como rodar (Python 3 + Pillow):
#
#   python assets/modelagem/cenario/gerar_sinal_sala_segura.py
#
# O que sai: assets/sprites/cenario/objetos/sinal_sala_segura.png (16 x 18 px,
# na escala do cenário, 1x). A cena que usa o sprite é
# cenas/cenario/objetos/sinal_sala_segura.tscn, que põe por cima uma
# PointLight2D verde que pulsa devagar (LuzPulsante).
#
# O desenho, de cima para baixo:
#   - o SUPORTE: um toco de metal escuro preso na parede;
#   - a LÂMPADA: uma cúpula em elipse. Cada pixel (x, y) está dentro dela se
#     ((x - cx) / rx)^2 + ((y - cy) / ry)^2 <= 1. O verde fica mais claro perto
#     do centro: o tom é escolhido pela distância normalizada
#     d = raiz(((x - cx) / rx)^2 + ((y - cy) / ry)^2), em três faixas;
#   - a PLAQUINHA: um retângulo verde-escuro com a borda de metal e uma
#     casinha branca (o telhado é um triângulo: |x - meio| <= linha do telhado).
#
# O sinal é o mesmo em todas as fases, para o jogador aprender a reconhecê-lo:
# luz verde na porta = ali dentro os robôs não entram e há um checkpoint.

import os

from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos", "sinal_sala_segura.png")

LARGURA, ALTURA = 16, 18

METAL_ESCURO = (28, 32, 38, 255)
METAL = (58, 64, 74, 255)
VERDE_CLARO = (190, 255, 210, 255)
VERDE = (60, 255, 138, 255)
VERDE_MEDIO = (34, 170, 92, 255)
VERDE_ESCURO = (22, 74, 46, 255)
BRANCO = (230, 244, 236, 255)


def desenhar():
    img = Image.new("RGBA", (LARGURA, ALTURA), (0, 0, 0, 0))
    px = img.load()

    # O suporte: 4 px de largura no meio, nas duas primeiras linhas.
    for y in range(0, 2):
        for x in range(6, 10):
            px[x, y] = METAL

    # A lâmpada: a borda escura é a elipse um pouco maior, o vidro é a menor.
    cx, cy = 7.5, 5.5
    for y in range(1, 10):
        for x in range(LARGURA):
            borda = ((x - cx) / 5.6) ** 2 + ((y - cy) / 4.2) ** 2
            vidro = ((x - cx) / 4.6) ** 2 + ((y - cy) / 3.3) ** 2
            if vidro <= 1:
                d = vidro ** 0.5
                px[x, y] = VERDE_CLARO if d < 0.35 else VERDE if d < 0.7 else VERDE_MEDIO
            elif borda <= 1:
                px[x, y] = METAL_ESCURO

    # A plaquinha: borda de metal e fundo verde-escuro.
    for y in range(10, 18):
        for x in range(LARGURA):
            na_borda = x in (0, LARGURA - 1) or y in (10, 17)
            px[x, y] = METAL_ESCURO if na_borda else VERDE_ESCURO

    # A casinha: telhado em triângulo (linhas 11 a 13) e o corpo (14 a 16),
    # com a porta escura no meio.
    meio = 7.5
    for y in range(11, 14):
        meia_largura = (y - 11) + 1.5
        for x in range(LARGURA):
            if abs(x - meio) <= meia_largura:
                px[x, y] = BRANCO
    for y in range(14, 17):
        for x in range(5, 11):
            px[x, y] = VERDE_ESCURO if (x in (7, 8) and y >= 15) else BRANCO

    return img


def main():
    img = desenhar()
    img.save(SAIDA)
    print(f"  salvo: {os.path.relpath(SAIDA, PASTA_PROJETO)} ({LARGURA}x{ALTURA})")


if __name__ == "__main__":
    main()
