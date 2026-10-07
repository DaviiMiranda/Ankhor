# preparar_menu.py — transforma o vídeo de referência do menu no fundo animado
# que o jogo toca, com a tela do monitor vazia.
#
# Como rodar (precisa de Python com Pillow e NumPy, e do ffmpeg no PATH):
#
#   python assets/modelagem/menu/preparar_menu.py
#
# Entra:  assets/modelagem/menu/menu_referencia.mp4  (1280×720, 24 quadros/s, 10 s,
#         com o menu pintado na tela do monitor)
# Sai:    assets/video/menu/menu_fundo.ogv           (o vídeo em loop, tela vazia)
#         assets/sprites/menu/menu_cena.png          (o primeiro quadro, parado)
#
# Por que apagar o texto? O vídeo já vem com "ANKHOR", os cinco itens e a
# barra azul de seleção desenhados no monitor. No jogo esses itens são botões
# de verdade (mudam de cor, a barra anda, aparecem as telas de Fases e Opções),
# então o Godot desenha tudo isso por cima. O vídeo precisa da tela vazia.
#
# Por que Ogg Theora (.ogv)? É o único formato de vídeo que o Godot 4 toca
# sem plugin.
#
# Ideia geral:
#   1. Ler alguns quadros do vídeo e tirar a MEDIANA de cada pixel. A câmera
#      é parada e o vidro do monitor quase não muda; a mediana tira o ruído
#      da compressão e dá uma imagem limpa do vidro (com o texto).
#   2. Apagar o texto dessa imagem: marcar numa máscara as letras e a faixa
#      da barra, e preencher resolvendo a equação de Laplace (preenchimento
#      harmônico): cada pixel apagado vira a média dos 4 vizinhos, repetido
#      milhares de vezes, até estabilizar. É o degradê mais suave que
#      "encosta" nas bordas do buraco, como uma película de sabão num arame.
#   3. Devolver a textura do vidro (linhas de CRT e granulado), que o
#      preenchimento deixa lisa demais.
#   4. Recortar só o vidro e colar essa "placa" parada por cima do vídeo
#      inteiro (filtro overlay do ffmpeg).
#   5. Fazer o loop sem emenda: o vídeo começa em 1 s, e no último segundo
#      ele se mistura aos poucos com o primeiro segundo (filtro xfade). Assim
#      o último quadro é quase igual ao primeiro e o loop não dá "pulo"
#      (os papéis voando estão em lugares diferentes no começo e no fim).

import os
import subprocess
import tempfile

import numpy as np
from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
ENTRADA = os.path.join(PASTA_SCRIPT, "menu_referencia.mp4")
SAIDA_VIDEO = os.path.join(PASTA_PROJETO, "assets", "video", "menu", "menu_fundo.ogv")
SAIDA_QUADRO = os.path.join(PASTA_PROJETO, "assets", "sprites", "menu", "menu_cena.png")

LARGURA, ALTURA = 1280, 720
DURACAO = 10.0      # segundos do vídeo de referência
MISTURA = 1.0       # segundos de mistura no fim do loop

# Vidro do monitor, em pixels do vídeo (x0, y0, x1, y1). No jogo (320×180)
# é só dividir por 4: x 91–229,5 e y 29,5–130,5.
VIDRO = (364, 118, 918, 522)
# Onde procurar letras: a coluna do meio do vidro (o reflexo claro no canto
# de cima à esquerda do vidro fica de fora, senão seria apagado também).
COLUNA_TEXTO = (500, 790)
LIMIAR_LETRA = 33   # brilho (0–255) acima do qual um pixel é letra ou brilho de letra
FOLGA = 9           # pixels de folga em volta de cada letra
# A barra de seleção (atrás de "Novo jogo") atravessa o vidro: vai de x ≈ 380
# a 908. A máscara para 2 px antes da borda escura do vidro de cada lado, para
# que o preenchimento parta do vidro, e não do plástico bege da moldura.
BARRA = (366, 230, 910, 292)
# Faixa limpa do vidro de onde tiramos as linhas de CRT e o granulado.
FAIXA_LIMPA = (800, 900)
TAMANHO_GRAO = 4.0  # tamanho do "pixel" da pintura, em pixels do vídeo


def ler_quadros(caminho, quadros_por_segundo=6):
    """Pede ao ffmpeg os quadros em RGB cru e devolve um array (n, altura, largura, 3)."""
    bruto = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", caminho, "-vf", f"fps={quadros_por_segundo}",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        check=True, capture_output=True).stdout
    return np.frombuffer(bruto, np.uint8).reshape(-1, ALTURA, LARGURA, 3)


def dilatar(mascara, raio):
    """Engorda a máscara 'raio' pixels para cada lado (cada pixel marcado
    marca também os vizinhos)."""
    saida = mascara.copy()
    for dy in range(-raio, raio + 1):
        for dx in range(-raio, raio + 1):
            saida |= np.roll(np.roll(mascara, dy, 0), dx, 1)
    return saida


def montar_mascara(img):
    brilho = img.mean(axis=2)
    mascara = np.zeros(brilho.shape, dtype=bool)
    x0, x1 = COLUNA_TEXTO
    _, vy0, _, vy1 = VIDRO
    mascara[vy0:vy1, x0:x1] = brilho[vy0:vy1, x0:x1] > LIMIAR_LETRA
    mascara = dilatar(mascara, FOLGA)
    bx0, by0, bx1, by1 = BARRA
    mascara[by0:by1, bx0:bx1] = True
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


def devolver_textura(limpa, ref, mascara):
    """Soma ao remendo as linhas de CRT e o granulado do vidro original."""
    rng = np.random.default_rng(7)  # mesma semente: a arte não muda de uma rodada para outra
    fx0, fx1 = FAIXA_LIMPA
    # Linhas: brilho médio de cada linha da faixa limpa menos a versão
    # suavizada (média móvel de 9 linhas). Sobra só a oscilação das linhas.
    perfil = ref[:, fx0:fx1].mean(axis=(1, 2))
    suave = np.convolve(perfil, np.ones(9) / 9, mode="same")
    linhas = perfil - suave
    # Nas linhas da barra a faixa limpa também estava coberta: usamos o
    # padrão das linhas logo acima, deslocado pela altura da barra.
    _, by0, _, by1 = BARRA
    altura = by1 - by0
    linhas[by0:by1] = linhas[by0 - altura:by1 - altura]
    # Granulado: ruído sorteado numa grade menor e ampliado sem suavizar
    # (cada sorteio vira um bloco), com o mesmo desvio-padrão do vidro. Para
    # medir só o granulado (e não o degradê do vidro), subtraímos de cada
    # pixel a média do quadrado 9×9 em volta dele (um filtro passa-alta).
    trecho = ref[330:480, fx0:fx1].mean(axis=2)
    janelas = np.lib.stride_tricks.sliding_window_view(np.pad(trecho, 4, mode="edge"), (9, 9))
    desvio = (trecho - janelas.mean(axis=(2, 3))).std()
    h, w = mascara.shape
    grade = rng.normal(0.0, desvio, (int(h / TAMANHO_GRAO) + 1, int(w / TAMANHO_GRAO) + 1))
    grao = np.asarray(Image.fromarray(grade.astype(np.float32)).resize((w, h), Image.NEAREST))
    textura = linhas[:, None] + grao
    limpa[mascara] += textura[mascara][:, None]
    return limpa


def placa_do_vidro():
    """Passos 1 a 3: devolve a imagem limpa do vidro (só o retângulo VIDRO)."""
    mediana = np.median(ler_quadros(ENTRADA), axis=0).astype(np.float32)
    mascara = montar_mascara(mediana)
    x0, y0, x1, y1 = VIDRO
    # Só a região do vidro (com folga) entra na conta: é muito mais rápido.
    m = 12
    limpa = mediana.copy()
    limpa[y0 - m:y1 + m, x0 - m:x1 + m] = preencher_harmonico(
        mediana[y0 - m:y1 + m, x0 - m:x1 + m], mascara[y0 - m:y1 + m, x0 - m:x1 + m])
    limpa = devolver_textura(limpa, mediana, mascara)
    return Image.fromarray(np.clip(limpa[y0:y1, x0:x1], 0, 255).astype(np.uint8))


def gerar_video(caminho_placa):
    """Passos 4 e 5, num comando só do ffmpeg."""
    x0, y0, _, _ = VIDRO
    # O trecho [resto] vai de 1 s a 10 s (9 s). A mistura com o primeiro
    # segundo [comeco] começa 1 s antes do fim dele; o vídeo final tem 9 s e
    # termina no quadro de 1 s, que é exatamente onde o loop recomeça.
    inicio = DURACAO - 1.0 - MISTURA
    filtro = (
        f"[0:v]trim=1:{DURACAO},setpts=PTS-STARTPTS[resto];"
        f"[0:v]trim=0:{MISTURA},setpts=PTS-STARTPTS[comeco];"
        f"[resto][comeco]xfade=transition=fade:duration={MISTURA}:offset={inicio}[loop];"
        f"[loop][1:v]overlay={x0}:{y0}[saida]"
    )
    os.makedirs(os.path.dirname(SAIDA_VIDEO), exist_ok=True)
    # -an: sem áudio (o menu já tem a trilha própria). -q:v 7: qualidade do
    # Theora de 0 a 10; 7 deixa o pixel art nítido sem o arquivo ficar enorme.
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", ENTRADA, "-i", caminho_placa,
         "-filter_complex", filtro, "-map", "[saida]", "-an",
         "-c:v", "libtheora", "-q:v", "7", SAIDA_VIDEO],
        check=True)
    print(f"[menu] vídeo salvo em {SAIDA_VIDEO}")


def salvar_primeiro_quadro():
    """O Godot mostra este quadro parado atrás do vídeo, para não piscar preto
    no instante antes do vídeo começar."""
    os.makedirs(os.path.dirname(SAIDA_QUADRO), exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SAIDA_VIDEO, "-frames:v", "1", SAIDA_QUADRO],
                   check=True)
    print(f"[menu] primeiro quadro salvo em {SAIDA_QUADRO}")


def main():
    with tempfile.TemporaryDirectory() as pasta:
        caminho_placa = os.path.join(pasta, "placa.png")
        placa_do_vidro().save(caminho_placa)
        gerar_video(caminho_placa)
    salvar_primeiro_quadro()


main()
