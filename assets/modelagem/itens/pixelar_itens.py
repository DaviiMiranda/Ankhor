# pixelar_itens.py — transforma as artes de referência dos itens em
# sprites de jogo (pixel art no tamanho do jogo, paleta fechada), como o
# pixelar_gabriel.py faz com o Gabriel.
#
# Como rodar (só precisa de Python 3 com Pillow e NumPy, sem Blender):
#
#   python assets/modelagem/itens/pixelar_itens.py
#
# Entrada (assets/modelagem/itens/referencias/):
#   <item>.webp      a arte de referência do item (pode ter cenário em volta)
#
# Saída (assets/sprites/itens/), para cada item da tabela ITENS:
#   <item>.png           32 x 32: ícone do inventário em RESOLUÇÃO DOBRADA
#                        (mostrado em 16 x 16 na tela, com o dobro de detalhe,
#                        como os personagens; ver docs/decisoes.md)
#   <item>_detalhe.png   a imagem grande da tela de examinar, também em
#                        resolução dobrada (mostrada com escala 0,5)
#   <item>_referencia.png  folha para conferir: o recorte, o detalhe e o ícone
#
# O item caído no chão (<item>_chao.png) continua saindo do
# gerar_interface.py: ele fica no cenário, que é desenhado em 1×.
#
# Passos, para cada item:
#   1. Recorte. A referência é uma cena (mesa, cabos, garrafa), e o fundo
#      tem cores parecidas com o item. Por isso a silhueta do item é um
#      polígono marcado à mão (CONTORNO, em pixels da imagem original):
#      dentro dele é item, fora é vazio.
#   2. Redução. A figura é reduzida até caber na caixa do tamanho pedido,
#      com as funções do pixelar_gabriel.py: a cor do item é espalhada para
#      fora da silhueta antes (senão o fundo entra na média e a borda
#      desbota), a cor reduz com Lanczos e a transparência com média simples.
#   3. Paleta. Um k-médias no espaço Lab acha as MAX_CORES cores que melhor
#      representam o item; detalhe e ícone usam a mesma paleta.
#   4. Contorno. Todo pixel da borda vira um tom escuro da própria cor.
#
# Para um item novo: ponha a referência em referencias/, marque o polígono
# da silhueta (um programa de imagem mostra as coordenadas do cursor) e
# acrescente uma linha em ITENS.

import importlib.util
import os

import numpy as np
from PIL import Image, ImageDraw

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_REF = os.path.join(PASTA_SCRIPT, "referencias")
PASTA_SAIDA = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "sprites", "itens"))

# Importa as funções do pixelar_gabriel.py (redução, k-médias, contorno)
# como um módulo, sem rodar o main dele.
_spec = importlib.util.spec_from_file_location(
    "pixelar_gabriel", os.path.join(PASTA_SCRIPT, "..", "personagens", "pixelar_gabriel.py"))
pg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pg)

TAMANHO_ICONE = 32   # 16 x 16 na tela
# Caixa da imagem de examinar, em pixels da imagem (o dobro do que aparece
# na tela): a tela de examinar reserva 140 x 120 para ela.
CAIXA_DETALHE = (272, 232)
MAX_CORES = 40

ITENS = {
    "notebook": {
        "referencia": "notebook.webp",
        # Notebook robusto aberto, visto de cima e de lado: cantoneiras
        # claras nos quatro cantos da tampa e da base, alça na frente.
        # A volta começa na cantoneira de cima à esquerda e segue no
        # sentido do relógio.
        "contorno": [
            (160, 172), (172, 162), (195, 156), (228, 156),          # cantoneira da tampa, esquerda
            (495, 20), (510, 9), (535, 5), (565, 11), (587, 33),     # topo da tampa e cantoneira direita
            (593, 65), (615, 280), (625, 282), (645, 312),           # lado direito da tampa e dobradiça
            (850, 424), (880, 430), (901, 450), (901, 503),          # fundo da base e cantoneira direita
            (888, 517), (790, 560), (685, 640), (607, 645),          # frente da base e alça
            (569, 668), (569, 686), (479, 688), (479, 655),          # cantoneira da frente
            (280, 567), (255, 540), (255, 508),                      # lado esquerdo da base
            (232, 490), (212, 470), (210, 440), (198, 330), (160, 245),  # lado esquerdo da tampa
        ],
    },
}


def recortar(cfg):
    img = Image.open(os.path.join(PASTA_REF, cfg["referencia"])).convert("RGB")
    mascara = Image.new("L", img.size, 0)
    ImageDraw.Draw(mascara).polygon(cfg["contorno"], fill=255)
    rgb = np.asarray(img).astype(np.float32)
    return pg.aparar(rgb, np.asarray(mascara) > 0)


def caber(rgb, mascara, largura_max, altura_max):
    # Reduz mantendo a proporção, até a figura caber na caixa.
    h, w = mascara.shape
    escala = min(largura_max / w, altura_max / h)
    return pg.reduzir(rgb, mascara, max(1, round(w * escala)), max(1, round(h * escala)))


def centralizar(spr, largura, altura):
    quadro = np.full((altura, largura), -1, np.int32)
    h, w = spr.shape
    y0, x0 = (altura - h) // 2, (largura - w) // 2
    quadro[y0:y0 + h, x0:x0 + w] = spr
    return quadro


def folha_referencia(recorte, detalhe, icone):
    # O recorte da referência ao lado do detalhe e do ícone, ampliados com
    # pixels quadrados, para comparar.
    rgb, m = recorte
    fundo = np.array([40, 40, 46], np.uint8)
    orig = np.where(m[..., None], rgb.astype(np.uint8), fundo)
    orig = Image.fromarray(orig).resize((detalhe.shape[1] * 2, detalhe.shape[0] * 2), Image.LANCZOS)

    def ampliar(rgba, fator):
        img = Image.fromarray(rgba, "RGBA")
        return img.resize((img.width * fator, img.height * fator), Image.NEAREST)

    det = ampliar(detalhe, 2)
    ico = ampliar(icone, 4)
    folha = Image.new("RGBA", (orig.width + det.width + ico.width + 40,
                               max(orig.height, det.height, ico.height) + 20), (*fundo, 255))
    folha.paste(orig, (10, 10))
    folha.alpha_composite(det, (orig.width + 20, 10))
    folha.alpha_composite(ico, (orig.width + det.width + 30, 10))
    return folha


def pixelar(nome, cfg):
    recorte = recortar(cfg)
    detalhe = caber(*recorte, *CAIXA_DETALHE)
    icone = caber(*recorte, TAMANHO_ICONE - 2, TAMANHO_ICONE - 2)
    paleta = pg.paleta_de([detalhe], MAX_CORES)
    spr_detalhe = pg.contornar(pg.indexar(*detalhe, paleta), paleta)
    spr_icone = pg.contornar(pg.indexar(*icone, paleta), paleta)
    rgba_detalhe = pg.para_rgba(spr_detalhe, paleta)
    rgba_icone = pg.para_rgba(centralizar(spr_icone, TAMANHO_ICONE, TAMANHO_ICONE), paleta)
    Image.fromarray(rgba_detalhe, "RGBA").save(os.path.join(PASTA_SAIDA, f"{nome}_detalhe.png"))
    Image.fromarray(rgba_icone, "RGBA").save(os.path.join(PASTA_SAIDA, f"{nome}.png"))
    folha_referencia(recorte, rgba_detalhe, rgba_icone).save(
        os.path.join(PASTA_SAIDA, f"{nome}_referencia.png"))
    print(f"{nome}: detalhe {spr_detalhe.shape[1]} x {spr_detalhe.shape[0]}, "
          f"ícone {TAMANHO_ICONE} x {TAMANHO_ICONE}, {len(np.unique(paleta, axis=0))} cores")


def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    for nome, cfg in ITENS.items():
        pixelar(nome, cfg)


if __name__ == "__main__":
    main()
