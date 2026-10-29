# pixelar_retratos.py — transforma as folhas de expressões desenhadas (uma
# imagem com todos os rostos de um personagem) nos retratos da caixa de
# diálogo: PNG de 80 x 80 com fundo transparente, paleta fechada por
# personagem. As ferramentas (máscara do fundo, redução, paleta por k-médias)
# são as do pixelar_gabriel.py.
#
# Como rodar (só precisa de Python 3 com Pillow e NumPy, sem Blender):
#
#   python assets/modelagem/personagens/pixelar_retratos.py            # todos
#   python assets/modelagem/personagens/pixelar_retratos.py diana zane # só esses
#
# Entrada: <personagem>_referencia/expressoes.jpg, uma folha de 2000 x 1116
# com os rostos em molduras. Para cada personagem, CONFIG diz onde está cada
# moldura (x0, y0, x1, y1 na folha) e quanto recuar para fora da borda
# decorativa.
#
# Saída: assets/sprites/personagens/<personagem>/<personagem>_retrato_<nome>.png
#
# Como cada rosto vira um retrato:
#   1. a moldura é recortada (sem a borda) num quadrado, na mesma posição em
#      todas as expressões do personagem: a cabeça não pula de um retrato
#      para outro quando a fala troca de emoção;
#   2. o fundo (cinza escuro, ligado às bordas do quadrado) vira transparente;
#   3. o quadrado é reduzido a 80 x 80 (Lanczos para a cor, média para a
#      transparência);
#   4. todas as expressões do personagem usam a mesma paleta de 48 cores
#      (k-médias em Lab), para a pele e a roupa não mudarem de tom entre uma
#      fala e outra;
#   5. pontinhos soltos de 1 ou 2 pixels (restos da grade da folha) são
#      apagados.
# A figura não é contornada de novo: o desenho já vem com o próprio contorno.

import os
import sys

import numpy as np
from PIL import Image, ImageDraw

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA_SCRIPT)
import pixelar_gabriel as base  # noqa: E402

PASTA_SPRITES = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "sprites", "personagens"))
TAM = base.TAM_RETRATO
MAX_CORES = 48
# Pedaços soltos de menos de MIGALHA pixels (restos da grade do fundo) somem.
MIGALHA = 3

# Fundo: até que diferença (no maior canal) um pixel ainda conta como fundo.
# O fundo das folhas tem linhas de grade fracas e ruído de JPEG. No Henrique o
# cabelo é quase da cor do fundo, então a tolerância dele é menor (CONFIG).
TOLERANCIA = 26

# apagar: retângulos (em coordenadas da moldura recortada) que são marcas da
# folha e não do desenho (a estrela de "já usada"), pintados com a cor do fundo.
CONFIG = {
    "diana": {
        "folha": "diana_referencia/expressoes.jpg",
        "recuo": 13,
        "retratos": {
            "normal": (55, 50, 478, 471),
            "assustada": (543, 50, 967, 471),
            "dramatica": (1033, 50, 1457, 471),
            "ansiosa": (1523, 50, 1947, 471),
            "irritada": (284, 597, 711, 1018),
            "determinada": (787, 597, 1213, 1018),
            "aliviada": (1290, 597, 1717, 1018),
        },
    },
    "henrique": {
        "folha": "henrique_referencia/expressoes.jpg",
        "recuo": 0,
        "tolerancia": 12,
        "fundo_opaco": True,
        "retratos": {
            "normal": (58, 45, 492, 495),
            "nervoso": (541, 45, 975, 495),
            "timido": (1025, 45, 1459, 495),
            "cansado": (1508, 45, 1942, 495),
            "pensativo": (291, 580, 733, 1020),
            "triste": (775, 580, 1225, 1020),
            "culpado": (1267, 580, 1708, 1020),
        },
    },
    "zane": {
        "folha": "zane_referencia/expressoes.jpg",
        "recuo": 17,
        "retratos": {
            "normal": (50, 67, 472, 478),
            "confiante": (543, 67, 965, 478),
            "assustado": (1037, 67, 1458, 478),
            "empolgado": (1528, 67, 1950, 478),
            "desconfiado": (50, 602, 472, 1033),
            "concentrado": (543, 602, 965, 1033),
            "frustrado": (1037, 602, 1458, 1033),
        },
        "apagar": {
            "confiante": [(315, 0, 405, 62)],
            "assustado": [(335, 0, 395, 50)],
        },
    },
    "baltazar": {
        "folha": "baltazar_referencia/expressoes.jpg",
        "recuo": 17,
        "retratos": {
            "encantado": (35, 70, 400, 893),
            "aflito": (427, 70, 792, 893),
            "rezando": (818, 70, 1183, 893),
            "teimoso": (1210, 70, 1575, 893),
            "orgulhoso": (1600, 70, 1965, 893),
        },
        # A folha não tem rosto "normal": o normal é uma cópia do orgulhoso.
        # Sem isto, as falas com "normal" mostravam o retrato antigo do Blender.
        "copias": {"normal": "orgulhoso"},
        "janela": {"y": 20, "lado": 440, "fundo": (38, 41, 53)},
    },
    # Gabriel: as dez emoções da folha nova (molduras com borda dupla; a
    # janela pega da franja ao moletom sem encostar na borda de baixo) e, da
    # folha antiga sem moldura, as três que a nova não tem. Os quadrados da
    # folha antiga foram medidos para a cabeça ficar do mesmo tamanho e na
    # mesma altura que na nova.
    "gabriel": {
        "folhas": [
            {
                "folha": "gabriel_referencia/expressoes_novas.jpg",
                "recuo": 25,
                "janela": {"y": 0, "lado": 350, "fundo": (95, 103, 116)},
                "retratos": {
                    "assustado": (50, 29, 400, 437),
                    "sorrindo": (433, 29, 792, 437),
                    "aliviado": (825, 29, 1175, 437),
                    "determinado": (1208, 29, 1567, 437),
                    "desconfiado": (1600, 29, 1950, 437),
                    "pensativo": (42, 587, 408, 995),
                    "triste": (442, 587, 800, 995),
                    "bravo": (817, 587, 1183, 995),
                    "envergonhado": (1217, 587, 1575, 995),
                    "cansado": (1592, 587, 1959, 995),
                },
            },
            {
                "folha": "gabriel_referencia/expressoes.webp",
                "recuo": 0,
                # O fundo cinza-claro deixava uma franja clara no contorno.
                "tolerancia": 40,
                "retratos": {
                    "normal": (37, 12, 225, 200),
                    "preocupado": (547, 12, 735, 200),
                    "surpreso": (799, 12, 987, 200),
                },
            },
        ],
    },
}


def recortar(img, caixa, recuo, janela):
    # Sem "janela", o recorte é o maior quadrado centrado na moldura. Com
    # janela (as molduras altas do Baltazar), o recorte é um quadrado de
    # "lado" px que começa "y" px abaixo do alto da moldura e é mais largo que
    # ela: o que sobra dos lados é pintado com a cor do fundo.
    x0, y0, x1, y1 = caixa
    x0, y0, x1, y1 = x0 + recuo, y0 + recuo, x1 - recuo, y1 - recuo
    if janela is None:
        lado = min(x1 - x0, y1 - y0)
        xa = (x0 + x1) // 2 - lado // 2
        return np.asarray(img.crop((xa, y0, xa + lado, y0 + lado))).astype(np.float32)
    lado = janela["lado"]
    faixa = np.asarray(img.crop((x0, y0 + janela["y"], x1, y0 + janela["y"] + lado))).astype(np.float32)
    tela = np.empty((lado, lado, 3), np.float32)
    tela[:] = janela["fundo"]
    xa = (lado - faixa.shape[1]) // 2
    tela[:, xa:xa + faixa.shape[1]] = faixa
    return tela


def cor_do_fundo(rgb):
    borda = np.concatenate([rgb[:4].reshape(-1, 3), rgb[:, :4].reshape(-1, 3),
                            rgb[:, -4:].reshape(-1, 3)])
    return np.median(borda, axis=0)


def apagar_marcas(rgb, retangulos, fundo):
    rgb = rgb.copy()
    for x0, y0, x1, y1 in retangulos:
        rgb[y0:y1, x0:x1] = fundo
    return rgb


def reduzir_retrato(rgb, tolerancia, fundo_opaco):
    # Com fundo_opaco o fundo não vira transparente: vira uma cor lisa (a
    # mediana da borda). O cabelo do Henrique é quase da cor do fundo da caixa
    # de diálogo e sumiria sobre ela.
    mascara = base.mascara_figura(rgb, tolerancia=tolerancia)
    if fundo_opaco:
        rgb = np.where(mascara[..., None], rgb, cor_do_fundo(rgb))
        mascara = np.ones_like(mascara)
    return base.reduzir(rgb, mascara, TAM, TAM)


def folhas_de(cfg):
    # Um personagem pode ter os rostos espalhados em mais de uma folha
    # ("folhas", cada uma com as próprias molduras, recuo e janela). A paleta
    # continua uma só, calculada com os rostos de todas as folhas juntos.
    return cfg.get("folhas", [cfg])


def gerar(personagem):
    cfg = CONFIG[personagem]
    figuras = {}
    for folha in folhas_de(cfg):
        img = Image.open(os.path.join(PASTA_SCRIPT, folha["folha"])).convert("RGB")
        for nome, caixa in folha["retratos"].items():
            rgb = recortar(img, caixa, folha["recuo"], folha.get("janela"))
            rgb = apagar_marcas(rgb, folha.get("apagar", {}).get(nome, []), cor_do_fundo(rgb))
            figuras[nome] = reduzir_retrato(rgb, folha.get("tolerancia", TOLERANCIA),
                                            folha.get("fundo_opaco", False))
    paleta = base.paleta_de(list(figuras.values()), MAX_CORES)
    pasta = os.path.join(PASTA_SPRITES, personagem)
    os.makedirs(pasta, exist_ok=True)
    saida = {}
    for nome, (cor, mascara) in figuras.items():
        spr = base.limpar_migalhas(base.indexar(cor, mascara, paleta), MIGALHA)
        rgba = base.para_rgba(spr, paleta)
        Image.fromarray(rgba, "RGBA").save(os.path.join(pasta, f"{personagem}_retrato_{nome}.png"))
        saida[nome] = rgba
        print(f"{personagem}: retrato {nome}")
    for nome, original in cfg.get("copias", {}).items():
        Image.fromarray(saida[original], "RGBA").save(os.path.join(pasta, f"{personagem}_retrato_{nome}.png"))
        saida[nome] = saida[original]
        print(f"{personagem}: retrato {nome} (cópia do {original})")
    return saida


def main():
    quais = sys.argv[1:] or list(CONFIG)
    for personagem in quais:
        gerar(personagem)


if __name__ == "__main__":
    main()
