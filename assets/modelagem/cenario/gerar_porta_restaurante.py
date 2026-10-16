# gerar_porta_restaurante.py — a PORTA DE VIDRO dos restaurantes do Centro de
# Convivência: duas folhas de vidro que correm para os lados, com batente de
# aço e um friso de neon na cor do restaurante.
#
# Como rodar (Python 3 + numpy + Pillow):
#
#   python assets/modelagem/cenario/gerar_porta_restaurante.py
#
# O que sai (em assets/sprites/cenario/praca/portas/), uma vez por cor de neon
# (ambar, verde, vermelho, magenta e ciano):
#   porta_<cor>_folha.png     as 14 imagens da abertura lado a lado numa folha
#                             só (14 x 80 px de largura, 88 de altura)
#   porta_<cor>_quadros.tres  o SpriteFrames do Godot, com um AtlasTexture por
#                             quadro, na animação "abrir" (como a porta do
#                             Bloco de salas, que a FolhaPorta já sabe tocar)
#
# O quadro tem 80 x 88 px, como a FolhaPorta do Bloco de salas, mas só o BATENTE
# (60 x 88 px, no meio) é opaco: o resto é transparente. A parede em volta
# muda de sala para sala (fachada de cerâmica por fora, parede de restaurante
# por dentro), e a mesma porta serve em todo lugar.
#
# ---------------------------------------------------------------------------
# A ANIMAÇÃO
# ---------------------------------------------------------------------------
#
# As duas folhas começam coladas no meio e correm cada uma para o seu lado,
# até sumirem atrás do batente. O deslocamento segue a curva
# "smootherstep", S(t) = 6t^5 - 15t^4 + 10t^3: ela sai devagar, acelera no meio
# e freia no fim, como um motor de porta automática de verdade. A derivada
# S'(t) = 30t^2 (1 - t)^2 vale zero em t = 0 e em t = 1, por isso não há
# "tranco" no começo nem no fim.

import os

import numpy as np

import gerar_praca_base as base

Imagem, RAMPAS, dilatar = base.Imagem, base.RAMPAS, base.dilatar
QUADROS = 14
VELOCIDADE = 28.0
LARGURA, ALTURA = 60, 88
LARGURA_PECA = 80
X_BATENTE = 10
X_VAO0, X_VAO1 = 4, 56
Y_VAO0, Y_VAO1 = 8, 86
RES_PORTAS = "res://assets/sprites/cenario/praca/portas"
CORES = ("ambar", "verde", "vermelho", "magenta", "ciano")


def suave(t):
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


def batente(cor, t):
    """O batente (60 x 88) com as folhas abertas até a fração t (0 = fechada,
    1 = aberta)."""
    img = Imagem(LARGURA, ALTURA)
    X, Y = img.X, img.Y
    rampa = base.NEON[cor]
    fino = base.ruido_ciclico(LARGURA, ALTURA, 2, 2, 700)
    tudo = img.ret(0, 0, LARGURA, ALTURA)
    # Batente de aço escovado, com realce na esquerda e em cima.
    img.pintar(tudo, "inox", 0.40 + 0.06 * fino + 0.16 * (Y == 0) + 0.1 * (X == 0) - 0.1 * (X == LARGURA - 1))
    img.pintar(img.ret(2, 2, LARGURA - 2, 7), "grafite", 0.2)
    # O vão: fundo escuro com a luz do restaurante (a cor do neon) caindo do teto.
    vao = img.ret(X_VAO0, Y_VAO0, X_VAO1, Y_VAO1)
    prof = np.clip((Y - Y_VAO0) / float(Y_VAO1 - Y_VAO0), 0.0, 1.0)
    img.pintar(vao, rampa, 0.10 + 0.20 * (1.0 - prof) ** 1.5 + 0.03 * fino)
    img.pintar(vao & (Y > Y_VAO1 - 14), "grafite", 0.08 + 0.08 * prof)
    img.pintar(vao & (Y > Y_VAO1 - 14) & (Y == Y_VAO1 - 14), rampa, 0.35, achatar=False)
    # As duas folhas de vidro: cada uma com metade do vão.
    meio = (X_VAO0 + X_VAO1) // 2
    deslocamento = int(round((meio - X_VAO0) * suave(t)))
    for lado, (xa, xb) in enumerate(((X_VAO0, meio), (meio, X_VAO1))):
        xa2, xb2 = (xa - deslocamento, xb - deslocamento) if lado == 0 else (xa + deslocamento, xb + deslocamento)
        folha = img.ret(xa2, Y_VAO0, xb2, Y_VAO1) & vao
        if not folha.any():
            continue
        img.pintar(folha, "gelo", 0.2 + 0.1 * (1 - prof) + 0.05 * fino)
        reflexo = folha & ((np.abs((X - xa2) - (Y - Y_VAO0) * 0.45 - 7) < 1.2) | (np.abs((X - xa2) - (Y - Y_VAO0) * 0.45 - 14) < 0.7))
        img.pintar(reflexo, "gelo", 0.62, achatar=False)
        # Moldura da folha (aço) e o puxador junto ao meio.
        borda = folha & ((Y < Y_VAO0 + 2) | (Y >= Y_VAO1 - 3) | (X == xa2) | (X == xb2 - 1))
        img.pintar(borda, "inox", 0.46 + 0.14 * (Y < Y_VAO0 + 1))
        x_puxador = (xb2 - 3) if lado == 0 else xa2 + 2
        img.pintar(img.ret(x_puxador, 44, x_puxador + 1, 60) & vao, "inox", 0.78)
        # Friso de neon na borda do meio, onde as folhas se encontram.
        x_friso = xb2 - 1 if lado == 0 else xa2
        img.pintar(img.ret(x_friso, Y_VAO0 + 3, x_friso + 1, Y_VAO1 - 4) & vao, rampa, 0.82, achatar=False)
    # Moldura de neon em volta do vão e a barra do lintel.
    contorno = dilatar(vao) & ~vao
    img.pintar(contorno, rampa, 0.62, achatar=False)
    img.pintar(img.ret(X_VAO0, 3, X_VAO1, 6), rampa, 0.88, achatar=False)
    img.pintar(img.ret(X_VAO0, 3, X_VAO1, 4), rampa, 1.0, achatar=False)
    for x in (X_VAO0 + 3, meio - 1, X_VAO1 - 5):
        img.pintar(img.ret(x, 6, x + 2, 7), "grafite", 0.1)
    # Sensor de presença na lateral e o leitor com o LED.
    img.pintar(img.ret(LARGURA - 3, 40, LARGURA - 1, 52), "grafite", 0.08)
    img.cor(img.ret(LARGURA - 3, 43, LARGURA - 2, 44), base.hexa("#6cf28e")[0])
    img.cor(img.ret(LARGURA - 3, 47, LARGURA - 2, 48), base.hexa("#ffc24a")[0])
    img.px[..., 3] = 255
    return img


def quadro(cor, t):
    """O quadro de 80 x 88 px da animação: o batente no meio, o resto vazio."""
    img = Imagem(LARGURA_PECA, ALTURA)
    img.colar(batente(cor, t), X_BATENTE, 0)
    return img


def folha_de_quadros(cor):
    return [quadro(cor, i / float(QUADROS - 1)) for i in range(QUADROS)]


def peca_de_parede(parede, cor, y_quadro=24):
    """Cola o quadro fechado da porta na peça de parede 'parede' (80 x 112), a
    partir de y_quadro: a parede em volta fica como estava."""
    peca = Imagem(parede.w, parede.h)
    peca.px[:] = parede.px
    peca.colar(quadro(cor, 0.0), 0, y_quadro)
    return peca


def gravar_quadros(cor, quadros):
    pasta = os.path.join(base.PASTA_PRACA, "portas")
    os.makedirs(pasta, exist_ok=True)
    folha = np.zeros((ALTURA, LARGURA_PECA * len(quadros), 4), dtype=np.uint8)
    for i, q in enumerate(quadros):
        folha[:, i * LARGURA_PECA:(i + 1) * LARGURA_PECA] = q.px
    base.bib.salvar_png(os.path.join(pasta, f"porta_{cor}_folha.png"), folha)
    linhas = ['[gd_resource type="SpriteFrames" format=3]', "",
              f'[ext_resource type="Texture2D" path="{RES_PORTAS}/porta_{cor}_folha.png" id="1_folha"]', ""]
    for i in range(len(quadros)):
        linhas += [f'[sub_resource type="AtlasTexture" id="Quadro{i}"]', 'atlas = ExtResource("1_folha")',
                   f"region = Rect2({i * LARGURA_PECA}, 0, {LARGURA_PECA}, {ALTURA})", ""]
    linhas += ["[resource]", "animations = [{", '"frames": [{']
    itens = [f'"duration": 1.0,\n"texture": SubResource("Quadro{i}")' for i in range(len(quadros))]
    linhas.append("}, {\n".join(itens) + "\n}],")
    linhas += ['"loop": false,', '"name": &"abrir",', f'"speed": {VELOCIDADE}', "}]", ""]
    with open(os.path.join(pasta, f"porta_{cor}_quadros.tres"), "w", encoding="utf-8", newline="\n") as arquivo:
        arquivo.write("\n".join(linhas))


def main():
    print("Gerando a porta de vidro dos restaurantes")
    for cor in CORES:
        gravar_quadros(cor, folha_de_quadros(cor))
    amostra = []
    for i in (0, 3, 6, 9, 13):
        amostra.append((f"ambar_{i}", quadro("ambar", i / float(QUADROS - 1))))
    for cor in CORES:
        amostra.append((f"{cor}_0", quadro(cor, 0.0)))
    base.salvar_catalogo("praca_portas", amostra, 5, 3)


if __name__ == "__main__":
    main()
