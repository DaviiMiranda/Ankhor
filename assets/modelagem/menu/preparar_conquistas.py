# preparar_conquistas.py — prepara a transição do menu para o caderno de
# conquistas e a arte do caderno.
#
# Como rodar (precisa de Python com Pillow e NumPy, e do ffmpeg no PATH):
#
#   python assets/modelagem/menu/preparar_conquistas.py
#
# Entra:  assets/modelagem/menu/menu_transicao_referencia.mp4  (1280×720, 24 q/s, 10 s:
#         a câmera sai do monitor, passa pela mesa e para num caderno aberto)
# Sai:    assets/video/menu/menu_transicao.ogv        (ida: monitor -> caderno)
#         assets/video/menu/menu_transicao_volta.ogv  (volta: o mesmo, de trás para frente)
#         assets/sprites/menu/menu_caderno.png        (o caderno parado, páginas limpas)
#         assets/sprites/interface/conquistas/*.png   (ícones recortados do caderno)
#
# Ideia geral:
#   1. Cortar as partes paradas do vídeo (a câmera só se mexe entre 1 s e
#      7,5 s) e acelerar 1,5× (setpts divide o tempo de cada quadro), para a
#      transição não demorar demais num menu. A volta usa o filtro "reverse"
#      do ffmpeg, que guarda os quadros e os devolve na ordem inversa.
#   2. O caderno parado: mediana dos quadros do fim (câmera já parada), que
#      tira o ruído da compressão.
#   3. Limpar as páginas: o vídeo traz textos e ícones de mentira ("ACHIEVEMENTS",
#      frases sem sentido). Os retângulos de conteúdo são apagados com o mesmo
#      preenchimento harmônico do preparar_menu.py (equação de Laplace: cada
#      pixel vira a média dos vizinhos até estabilizar) e ganham de volta o
#      granulado do papel. O X vermelho de fechar e as abas coloridas ficam:
#      o Godot põe um botão em cima do X.
#   4. Recortar três ícones do caderno (troféu, troféu apagado e "?") e trocar
#      a cor do papel por transparência, para usá-los como ícones de conquista.

import os
import subprocess
import sys

import numpy as np
from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA_SCRIPT)
from preparar_menu import preencher_harmonico  # noqa: E402

PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
ENTRADA = os.path.join(PASTA_SCRIPT, "menu_transicao_referencia.mp4")
PASTA_VIDEO = os.path.join(PASTA_PROJETO, "assets", "video", "menu")
SAIDA_IDA = os.path.join(PASTA_VIDEO, "menu_transicao.ogv")
SAIDA_VOLTA = os.path.join(PASTA_VIDEO, "menu_transicao_volta.ogv")
SAIDA_CADERNO = os.path.join(PASTA_PROJETO, "assets", "sprites", "menu", "menu_caderno.png")
PASTA_ICONES = os.path.join(PASTA_PROJETO, "assets", "sprites", "interface", "conquistas")

LARGURA, ALTURA = 1280, 720
INICIO, FIM = 0.5, 7.6   # trecho usado do vídeo, em segundos
VELOCIDADE = 1.5

# Retângulos (x0, y0, x1, y1) do conteúdo de mentira nas páginas, em pixels
# do vídeo. A página direita é dividida para não apagar o X vermelho (canto
# de cima à direita) nem a orelha da folha (canto de baixo à direita).
CONTEUDO = [
    (340, 135, 628, 578),   # página esquerda inteira
    (688, 140, 924, 172),   # título da página direita, até antes do X
    (688, 172, 950, 578),   # ícones e frases da página direita
    (950, 172, 982, 520),   # faixa da direita, acima da orelha da folha
]
# Papel limpo, de onde medimos o granulado.
PAPEL_LIMPO = (955, 200, 975, 440)

# Ícones: quadrados de 64×64 no quadro final (o centro de cada desenho).
ICONES = {
    "trofeu": (791, 283),            # troféu prateado da 2ª linha
    "trofeu_bloqueado": (709, 373),  # troféu apagado, dentro da moldura tracejada
    "secreta": (878, 373),           # o "?"
}
TAMANHO_ICONE = 64


def ffmpeg(*argumentos):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *argumentos], check=True)


def gerar_transicoes():
    """Passo 1: ida e volta, sem áudio, em Ogg Theora (o formato que o Godot toca)."""
    os.makedirs(PASTA_VIDEO, exist_ok=True)
    corte = f"trim=start={INICIO}:end={FIM},setpts=(PTS-STARTPTS)/{VELOCIDADE}"
    for saida, filtro in ((SAIDA_IDA, corte), (SAIDA_VOLTA, corte + ",reverse")):
        ffmpeg("-i", ENTRADA, "-vf", filtro, "-an", "-c:v", "libtheora", "-q:v", "7", saida)
        print(f"[conquistas] vídeo salvo em {saida}")


def ultimo_quadro_ida():
    """O quadro onde a ida termina (FIM), lido do vídeo original, que tem mais
    qualidade que o convertido: a tela do caderno precisa começar igual a ele."""
    bruto = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", str(FIM - 0.05), "-t", "0.4", "-i", ENTRADA,
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], check=True, capture_output=True).stdout
    quadros = np.frombuffer(bruto, np.uint8).reshape(-1, ALTURA, LARGURA, 3)
    # Mediana dos últimos quadros (a câmera já parou): tira o ruído da compressão.
    return np.median(quadros, axis=0).astype(np.float32)


def limpar_paginas(img):
    """Passo 3: apaga o conteúdo de mentira e devolve o granulado do papel."""
    mascara = np.zeros(img.shape[:2], dtype=bool)
    for x0, y0, x1, y1 in CONTEUDO:
        mascara[y0:y1, x0:x1] = True
    # Só a região do caderno entra na conta (com folga): muito mais rápido.
    y0, y1, x0, x1 = 110, 600, 320, 1000
    limpa = img.copy()
    limpa[y0:y1, x0:x1] = preencher_harmonico(img[y0:y1, x0:x1], mascara[y0:y1, x0:x1])
    # Granulado: desvio-padrão do papel limpo depois de tirar a média de cada
    # linha (o papel escurece devagar de cima para baixo).
    px0, py0, px1, py1 = PAPEL_LIMPO
    trecho = img[py0:py1, px0:px1].mean(axis=2)
    desvio = (trecho - trecho.mean(axis=1, keepdims=True)).std()
    rng = np.random.default_rng(11)  # mesma semente: a arte não muda de uma rodada para outra
    ruido = rng.normal(0.0, desvio, img.shape[:2]).astype(np.float32)
    limpa[mascara] += ruido[mascara][:, None]
    return limpa


def recortar_icones(img):
    """Passo 4: recorta os ícones e troca o papel por transparência."""
    os.makedirs(PASTA_ICONES, exist_ok=True)
    px0, py0, px1, py1 = PAPEL_LIMPO
    cor_papel = np.median(img[py0:py1, px0:px1].reshape(-1, 3), axis=0)
    for nome, (x, y) in ICONES.items():
        recorte = img[y:y + TAMANHO_ICONE, x:x + TAMANHO_ICONE]
        # Distância de cada pixel até a cor do papel. Perto do papel vira
        # transparente; longe fica opaco; no meio, uma rampa curta, para a
        # borda do desenho não ficar serrilhada.
        distancia = np.linalg.norm(recorte - cor_papel, axis=2)
        alfa = np.clip((distancia - 14.0) / 20.0, 0.0, 1.0)
        rgba = np.dstack([recorte, alfa * 255]).astype(np.uint8)
        caminho = os.path.join(PASTA_ICONES, f"{nome}.png")
        Image.fromarray(rgba, "RGBA").save(caminho)
        print(f"[conquistas] ícone salvo em {caminho}")


def main():
    gerar_transicoes()
    quadro = ultimo_quadro_ida()
    recortar_icones(quadro)
    limpo = limpar_paginas(quadro)
    os.makedirs(os.path.dirname(SAIDA_CADERNO), exist_ok=True)
    Image.fromarray(np.clip(limpo, 0, 255).astype(np.uint8)).save(SAIDA_CADERNO)
    print(f"[conquistas] caderno salvo em {SAIDA_CADERNO}")


if __name__ == "__main__":
    main()
