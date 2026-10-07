# preparar_menu.py — transforma a imagem de referência do menu na arte que o
# jogo usa, sem o texto que veio pintado na tela do monitor.
#
# Como rodar (precisa de Python com Pillow e NumPy):
#
#   python assets/modelagem/menu/preparar_menu.py
#
# Entra:  assets/modelagem/menu/menu_referencia.webp  (1024×572, com o menu pintado)
# Sai:    assets/sprites/menu/menu_cena.png           (1280×720, tela do monitor vazia)
#
# Por que apagar o texto? A imagem de referência já vem com "ANKHOR", os cinco
# itens e a barra azul de seleção desenhados. No jogo esses itens precisam ser
# botões de verdade (mudam de cor, a barra anda, aparecem as telas de Fases e
# Opções), então o Godot desenha tudo isso por cima. A arte precisa da tela
# vazia, só com o vidro escuro.
#
# Ideia geral:
#   1. Marcar numa máscara os pixels "sujos": os retângulos em volta de cada
#      linha de texto e a faixa inteira da barra de seleção.
#   2. Preencher esses pixels resolvendo a equação de Laplace (preenchimento
#      harmônico): cada pixel apagado vira a média dos 4 vizinhos, repetido
#      milhares de vezes, até estabilizar. O resultado é o degradê mais suave
#      possível que "encosta" nas bordas do buraco, como uma película de sabão
#      esticada num arame. Como o vidro do monitor é um degradê escuro e liso,
#      o remendo fica invisível.
#   3. Devolver a textura do vidro. O remendo sai liso demais, e o vidro de
#      verdade tem linhas finas de CRT e um granulado em blocos (os "pixels"
#      da pintura, de ~3 px). Medimos as linhas numa faixa limpa do vidro
#      (à direita do texto) e o granulado pelo desvio-padrão dessa faixa,
#      e aplicamos os dois só dentro da máscara.
#   4. Cortar para 16:9 e ampliar para 1280×720 (4× a resolução do jogo,
#      320×180). No Godot a imagem é mostrada com escala 0,25.

import os

import numpy as np
from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
ENTRADA = os.path.join(PASTA_SCRIPT, "menu_referencia.webp")
SAIDA = os.path.join(PASTA_PROJETO, "assets", "sprites", "menu", "menu_cena.png")

# Retângulos (x0, y0, x1, y1) em pixels da imagem de referência (1024×572).
# Linhas de texto: medidas na imagem, com folga para o brilho em volta das letras.
TEXTOS = [
    (390, 100, 636, 184),  # ANKHOR
    (420, 186, 606, 232),  # Novo jogo
    (430, 232, 600, 276),  # Continuar
    (450, 276, 576, 318),  # Fases
    (468, 364, 564, 410),  # Sair
]
# A barra de seleção atravessa o vidro de ponta a ponta (atrás de "Opções").
BARRA = (298, 314, 734, 367)

# Corte para 16:9: 572 × 16 / 9 ≈ 1017 de largura. Tiramos 3 px da esquerda
# e 4 da direita. A conta para achar um ponto da referência no jogo é
#   x_jogo = (x - 3) × 320 / 1017      y_jogo = y × 180 / 572
CORTE = (3, 0, 1020, 572)
TAMANHO_FINAL = (1280, 720)


def montar_mascara(altura, largura):
    mascara = np.zeros((altura, largura), dtype=bool)
    for x0, y0, x1, y1 in TEXTOS + [BARRA]:
        mascara[y0:y1, x0:x1] = True
    return mascara


def preencher_harmonico(img, mascara, iteracoes=4000):
    """Preenche os pixels da máscara com a média dos vizinhos, repetidamente
    (método de Jacobi para a equação de Laplace). Os pixels fora da máscara
    ficam fixos e servem de borda."""
    img = img.copy()
    # Ponto de partida: a cor média da borda do buraco (converge mais rápido
    # do que começar do preto).
    img[mascara] = img[~mascara & np.roll(mascara, 1, 0)].mean(axis=0)
    for _ in range(iteracoes):
        media = (np.roll(img, 1, 0) + np.roll(img, -1, 0) +
                 np.roll(img, 1, 1) + np.roll(img, -1, 1)) / 4
        img[mascara] = media[mascara]
    return img


# Faixa limpa do vidro (sem texto) de onde tiramos as linhas e o granulado.
FAIXA_LIMPA = (640, 720)
TAMANHO_GRAO = 3.2  # tamanho do "pixel" da pintura, em pixels da referência


def devolver_textura(limpa, ref, mascara, y0, y1):
    """Soma ao remendo as linhas de CRT e o granulado do vidro original."""
    rng = np.random.default_rng(7)  # mesma semente: a arte não muda de uma rodada para outra
    fx0, fx1 = FAIXA_LIMPA
    # Linhas: brilho médio de cada linha da faixa limpa menos a versão
    # suavizada (média móvel de 9 linhas). Sobra só a oscilação das linhas.
    perfil = ref[:, fx0:fx1].mean(axis=(1, 2))
    linhas = perfil - np.convolve(perfil, np.ones(9) / 9, mode="same")
    # Nas linhas da barra a faixa limpa também estava coberta: usamos o
    # padrão das linhas logo acima, deslocado pela altura da barra.
    bx0, by0, bx1, by1 = BARRA
    altura = by1 - by0
    linhas[by0:by1] = linhas[by0 - altura:by1 - altura]
    # Granulado: ruído sorteado numa grade menor e ampliado sem suavizar
    # (cada sorteio vira um bloco), com o mesmo desvio-padrão do vidro.
    desvio = (ref[y0:y1, fx0:fx1].mean(axis=2) - np.convolve(perfil, np.ones(9) / 9, mode="same")[y0:y1, None]).std()
    h, w = mascara.shape
    gh, gw = int(h / TAMANHO_GRAO) + 1, int(w / TAMANHO_GRAO) + 1
    grade = rng.normal(0.0, desvio * 0.8, (gh, gw)).astype(np.float32)
    grao = np.asarray(Image.fromarray(grade).resize((w, h), Image.NEAREST))
    textura = linhas[:, None] + grao
    limpa[mascara] += textura[mascara][:, None]
    return limpa


def main():
    ref = np.asarray(Image.open(ENTRADA).convert("RGB")).astype(np.float32)
    mascara = montar_mascara(*ref.shape[:2])
    # Só a região da tela do monitor entra na conta (com folga): é muito mais
    # rápido do que repetir a média na imagem inteira.
    y0, y1, x0, x1 = 90, 425, 285, 750
    limpa = ref.copy()
    limpa[y0:y1, x0:x1] = preencher_harmonico(ref[y0:y1, x0:x1], mascara[y0:y1, x0:x1])
    limpa = devolver_textura(limpa, ref, mascara, 180, 240)
    imagem = Image.fromarray(np.clip(limpa, 0, 255).astype(np.uint8))
    # Lanczos: o filtro de ampliação que menos borra (usa uma janela de
    # vizinhos pesada pela função sinc).
    imagem = imagem.crop(CORTE).resize(TAMANHO_FINAL, Image.LANCZOS)
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    imagem.save(SAIDA)
    print(f"[menu] arte salva em {SAIDA}")


main()
