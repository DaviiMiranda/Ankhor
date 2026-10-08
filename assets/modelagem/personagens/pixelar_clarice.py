# pixelar_clarice.py — transforma as artes de referência da Clarice em
# sprites de jogo (pixel art no tamanho do jogo, paleta fechada), do mesmo
# jeito que o pixelar_gabriel.py faz com o Gabriel. As ferramentas (recorte,
# redução, paleta por k-médias, contorno) são as do pixelar_gabriel.py.
#
# Como rodar (só precisa de Python 3 com Pillow e NumPy, sem Blender):
#
#   python assets/modelagem/personagens/pixelar_clarice.py
#
# Entrada (assets/modelagem/personagens/clarice_referencia/):
#   expressoes.png      cinco rostos: neutro, raiva, triste, vergonha e feliz
#   andar_frente.webp   oito poses andando de frente (duas fileiras de quatro)
#   andar_costas.webp   oito poses andando de costas
#
# Saída (assets/sprites/personagens/clarice/), nos mesmos nomes e tamanhos
# que o gerar_clarice.py usava, para as cenas do Godot não mudarem:
#   clarice_frente.png, clarice_costas.png    96 x 112, parada
#   clarice_andar_frente.png, clarice_andar_costas.png
#                                 caminhada, 12 quadros de 96 x 112 lado a lado
#   clarice_parado_frente.png, clarice_parado_costas.png
#                                 respiração, 8 quadros de 96 x 112
#   clarice_retrato_<nome>.png    80 x 80, para a caixa de diálogo
#   clarice_referencia.png        folha com o que sai daqui, para conferir
#
# As vistas de lado e de 3/4 ainda não têm referência: continuam saindo do
# gerar_clarice.py (Blender), e este script não mexe nelas.
#
# Consistência entre as poses: a jaqueta tem a mesma largura nas dezesseis
# poses, mas a cabeça, o tronco e as pernas não saíram do mesmo tamanho
# (na fileira de baixo a cabeça é ~4% maior, o tronco ~5% menor e as pernas
# ~8% maiores). Então:
#   1. cada pose é cortada em três trechos (do alto do cabelo à faixa roxa
#      do peito, da faixa à barra da jaqueta, da barra ao pé), e cada trecho
#      é esticado para a média das dezesseis poses; depois todas são
#      reduzidas pela mesma escala;
#   2. todas (de frente e de costas) usam a mesma paleta de 40 cores;
#   3. o corpo é centrado pela faixa do peito e o pé vai para a linha do chão;
#   4. a cabeça da pose parada é colada em todos os quadros da mesma vista
#      (o coque e o rabo de cavalo mudavam de forma de uma pose para outra).

import os
import sys

import numpy as np
from PIL import Image, ImageDraw

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA_SCRIPT)
import pixelar_gabriel as base  # noqa: E402

PASTA_REF = os.path.join(PASTA_SCRIPT, "clarice_referencia")
PASTA_SAIDA = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "sprites",
                                            "personagens", "clarice"))

QUADRO = base.QUADRO
LINHA_PE = base.LINHA_PE
CENTRO_X = base.CENTRO_X
QUADROS_ANDAR = base.QUADROS_ANDAR
QUADROS_PARADO = base.QUADROS_PARADO
TAM_RETRATO = base.TAM_RETRATO
MAX_CORES = 40
MAX_CORES_RETRATO = 48

# Altura da Clarice no sprite, do alto do coque ao pé: 1,62 m do couro
# cabeludo ao pé (90 px na escala do Gabriel, que tem 1,75 m e 97 px sem o
# volume do cabelo) e o coque por cima.
ALTURA_PX = 95

# Cada folha de caminhada é uma grade de 2 fileiras x 4 colunas.
FOLHA_LINHAS = ((0, 383), (383, 765))
FOLHA_COLUNAS = ((0, 256), (256, 512), (512, 768), (768, 1024))

# Ordem das poses na folha (da esquerda para a direita, de cima para baixo)
# é a ordem do ciclo. Doze quadros com oito poses: as poses pares (pé
# no chão) ficam dois quadros, as ímpares (passando) um, como no
# "contato segurado" das caminhadas desenhadas à mão.
POSE_DO_QUADRO = [0, 0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7]

# Pose usada como "parada" (a de pernas mais juntas, escolhida olhando a
# folha) em cada folha.
POSE_PARADA = {"frente": 3, "costas": 3}

RETRATOS = {
    "normal": 0,
    "seria": 1,
    "triste": 2,
    "envergonhada": 3,
    "sorrindo": 4,
}


# ---------------------------------------------------------------------------
# 1. Recorte
# ---------------------------------------------------------------------------

def abrir_rgb(nome, caixa):
    img = Image.open(os.path.join(PASTA_REF, nome)).convert("RGB").crop(caixa)
    return np.asarray(img).astype(np.float32)


def roxo(rgb, mascara):
    # A faixa roxa da jaqueta (e as munhequeiras, também roxas).
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    return mascara & (b > 140) & (r > 90) & (g < 90) & (b > r + 25)


def so_a_figura(mascara, semente):
    # As folhas têm texto ("FRAME 1", "NEUTRO"...) no canto. O texto não
    # encosta na figura, então ficam só os pixels ligados à semente (um
    # ponto que com certeza é da figura), por inundação.
    img = Image.fromarray(mascara.astype(np.uint8) * 255).copy()
    ImageDraw.floodfill(img, (int(semente[0]), int(semente[1])), 128, thresh=0)
    return np.asarray(img) == 128


def faixa_do_peito(rgb, mascara):
    # A primeira linha (de cima para baixo) com bastante roxo é o topo da
    # faixa do peito; o centro dela, na horizontal, é o centro do corpo.
    linhas = np.where(roxo(rgb, mascara).sum(axis=1) >= 12)[0]
    topo = int(linhas.min())
    xs = np.where(roxo(rgb, mascara)[topo:topo + 6].any(axis=0))[0]
    return topo, (xs.min() + xs.max() + 1) / 2


def recortar_pose(nome, caixa):
    rgb = abrir_rgb(nome, caixa)
    m = base.mascara_figura(rgb)
    topo, centro = faixa_do_peito(rgb, m)
    m = so_a_figura(m, (centro, topo + 2))
    return base.aparar(rgb, m)


# ---------------------------------------------------------------------------
# 2. Caminhada de frente e de costas
# ---------------------------------------------------------------------------

def bainha(rgb, m, centro):
    # A última linha com roxo no meio do corpo (a barra da jaqueta). Só o
    # meio: as munhequeiras, também roxas, ficam dos lados.
    c = int(centro)
    linhas = np.where(roxo(rgb, m)[:, c - 15:c + 15].sum(axis=1) >= 10)[0]
    return int(linhas.max())


def marcos(rgb, m):
    # Onde começa cada trecho do corpo, de cima para baixo: alto do cabelo,
    # faixa do peito, barra da jaqueta e sola do pé.
    peito, centro = faixa_do_peito(rgb, m)
    return [0, peito, bainha(rgb, m, centro), m.shape[0] - 1], centro


def esticar_trechos(rgb, m, de, para):
    # Estica ou encolhe cada trecho na vertical (cabeça, tronco, pernas)
    # para o tamanho de "para", escolhendo para cada linha nova a linha
    # original correspondente (conta linear dentro de cada trecho).
    ys = np.arange(int(round(para[-1])) + 1)
    origem = np.clip(np.round(np.interp(ys, para, de)).astype(int), 0, m.shape[0] - 1)
    return rgb[origem], m[origem]


def reduzir_pose(rgb, m, padrao, escala):
    # Cada trecho do corpo vai para o tamanho padrão (a média das poses) e
    # a pose inteira é reduzida pela mesma escala, igual para todas.
    de, centro = marcos(rgb, m)
    rgb, m = esticar_trechos(rgb, m, de, padrao)
    largura = max(1, round(m.shape[1] * escala))
    altura = max(1, round(m.shape[0] * escala))
    cor, mm = base.reduzir(rgb, m, largura, altura)
    return cor, mm, centro * largura / m.shape[1]


def no_quadro(spr, centro):
    # Centra pela faixa do peito e põe o pé mais baixo no chão.
    quadro = base.vazio()
    ys, xs = np.where(spr >= 0)
    x0 = int(round(CENTRO_X + 0.5 - centro))
    y0 = LINHA_PE - ys.max()
    ok = (ys + y0 >= 0) & (ys + y0 < QUADRO[1]) & (xs + x0 >= 0) & (xs + x0 < QUADRO[0])
    quadro[ys[ok] + y0, xs[ok] + x0] = spr[ys[ok], xs[ok]]
    return quadro


def recortar_folha(nome):
    return [recortar_pose(nome, (x0, y0, x1, y1))
            for y0, y1 in FOLHA_LINHAS for x0, x1 in FOLHA_COLUNAS]


def reduzir_folhas(folhas):
    # O tamanho padrão de cada trecho é a média de todas as poses, de frente
    # e de costas: assim as duas caminhadas têm a mesma cabeça, o mesmo
    # tronco e as mesmas pernas.
    todos = [marcos(rgb, m)[0] for poses in folhas.values() for rgb, m in poses]
    padrao = np.mean(todos, axis=0)
    escala = (ALTURA_PX - 1) / padrao[-1]
    return {nome: [reduzir_pose(rgb, m, padrao, escala) for rgb, m in poses]
            for nome, poses in folhas.items()}


# ---------------------------------------------------------------------------
# 3. Respiração
# ---------------------------------------------------------------------------
# A mesma conta do Gabriel (pixelar_gabriel.py, quadro_parado): o peito sobe
# até 2 pixels e a cabeça vai junto, 60° atrasada; as pernas não mexem. As
# linhas do corpo saem da própria figura: o queixo fica 7 px acima da faixa
# do peito, e a bainha da jaqueta é a última linha com roxo no meio do corpo.

SUBIDA = 2.0


def linhas_do_corpo(spr, paleta):
    cor = paleta[np.maximum(spr, 0)].astype(np.float32)
    eh_roxo = roxo(cor, spr >= 0)
    meio = eh_roxo[:, CENTRO_X - 6:CENTRO_X + 7].sum(axis=1)
    linhas = np.where(meio >= 6)[0]
    return int(linhas.min()) - 7, int(linhas.max())


def mesma_cabeca(quadro, molde, queixo):
    # A cabeça muda um pouco de uma pose desenhada para outra (o coque de
    # frente muda de forma, o rabo de cavalo de costas pula de lugar). Como
    # todas as poses já estão alinhadas pela faixa do peito e com os trechos
    # do corpo do mesmo tamanho, a cabeça da pose parada (tudo até a linha
    # do queixo) é colada em todos os quadros, sempre no mesmo lugar.
    out = quadro.copy()
    out[:queixo + 1] = molde[:queixo + 1]
    return out


def quadro_parado(spr, fase, queixo, bainha):
    phi = np.radians(fase)
    peito = round(SUBIDA * (1 - np.cos(phi)) / 2)
    cabeca = round(SUBIDA * (1 - np.cos(phi - np.radians(60))) / 2) if fase else 0
    meio_peito = (queixo + bainha) // 2
    return base.remapear_linhas(spr, [
        (0, -cabeca), (queixo - 2, queixo - 2 - cabeca),
        (queixo + 2, queixo + 2 - peito), (meio_peito, meio_peito - peito),
        (bainha - 4, bainha - 4), (QUADRO[1] - 1, QUADRO[1] - 1)])


# ---------------------------------------------------------------------------
# 4. Retratos da caixa de diálogo
# ---------------------------------------------------------------------------
# A folha de expressões tem cinco rostos lado a lado, cada um numa faixa de
# 1/5 da largura, com o nome escrito no canto. Cada rosto é recortado,
# reduzido até 80 px de altura e centrado num quadro de 80 x 80. Os cinco
# usam a mesma paleta, para a pele e a jaqueta não mudarem de cor entre uma
# fala e outra.

def retratos():
    img = Image.open(os.path.join(PASTA_REF, "expressoes.png")).convert("RGB")
    largura_faixa = img.width / 5
    figuras = {}
    for nome, i in RETRATOS.items():
        caixa = (round(i * largura_faixa), 0, round((i + 1) * largura_faixa), img.height)
        rgb = abrir_rgb("expressoes.png", caixa)
        m = base.mascara_figura(rgb)
        m = so_a_figura(m, (rgb.shape[1] / 2, rgb.shape[0] - 3))
        rgb, m = base.aparar(rgb, m)
        largura = max(1, round(m.shape[1] * TAM_RETRATO / m.shape[0]))
        figuras[nome] = base.reduzir(rgb, m, min(largura, TAM_RETRATO), TAM_RETRATO)
    paleta = base.paleta_de(list(figuras.values()), MAX_CORES_RETRATO)
    saida = {}
    for nome, (cor, m) in figuras.items():
        spr = base.contornar(base.indexar(cor, m, paleta), paleta)
        quadro = np.full((TAM_RETRATO, TAM_RETRATO), -1, np.int32)
        x0 = (TAM_RETRATO - spr.shape[1]) // 2
        quadro[:, x0:x0 + spr.shape[1]] = spr
        saida[nome] = base.para_rgba(quadro, paleta)
    return saida


# ---------------------------------------------------------------------------
# 5. Tudo junto
# ---------------------------------------------------------------------------

def salvar(rgba, nome):
    Image.fromarray(rgba, "RGBA").save(os.path.join(PASTA_SAIDA, nome))


def folha_referencia(vistas, andar, retratos_rgba, paleta):
    # Para conferir: as vistas paradas, as duas caminhadas e os retratos.
    margem = 8
    largura = margem + QUADROS_ANDAR * QUADRO[0] + margem
    altura = margem + 3 * (QUADRO[1] + margem) + TAM_RETRATO + margem
    folha = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    for i, spr in enumerate(vistas.values()):
        folha.alpha_composite(Image.fromarray(base.para_rgba(spr, paleta)),
                              (margem + i * (QUADRO[0] + margem), margem))
    for j, quadros in enumerate(andar.values()):
        for i, spr in enumerate(quadros):
            folha.alpha_composite(Image.fromarray(base.para_rgba(spr, paleta)),
                                  (margem + i * QUADRO[0], margem + (j + 1) * (QUADRO[1] + margem)))
    for i, rgba in enumerate(retratos_rgba.values()):
        folha.alpha_composite(Image.fromarray(rgba),
                              (margem + i * (TAM_RETRATO + margem), margem + 3 * (QUADRO[1] + margem)))
    return folha


def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    folhas = reduzir_folhas({"frente": recortar_folha("andar_frente.webp"),
                             "costas": recortar_folha("andar_costas.webp")})
    paleta = base.paleta_de([(cor, m) for poses in folhas.values() for cor, m, _ in poses],
                            MAX_CORES)
    contorno = base.tabela_escura(paleta, 0.42)

    vistas, andar = {}, {}
    for vista, poses in folhas.items():
        quadros = [base.contorno_final(no_quadro(base.contornar(base.indexar(cor, m, paleta),
                                                                paleta), centro),
                                       paleta, contorno)
                   for cor, m, centro in poses]
        parada = quadros[POSE_PARADA[vista]]
        queixo, _ = linhas_do_corpo(parada, paleta)
        quadros = [base.contorno_final(mesma_cabeca(q, parada, queixo), paleta, contorno)
                   for q in quadros]
        vistas[vista] = parada
        andar[vista] = [quadros[p] for p in POSE_DO_QUADRO]

    fases_parado = [360 * q / QUADROS_PARADO for q in range(QUADROS_PARADO)]
    for vista, spr in vistas.items():
        salvar(base.para_rgba(spr, paleta), f"clarice_{vista}.png")
        salvar(np.concatenate([base.para_rgba(q, paleta) for q in andar[vista]], axis=1),
               f"clarice_andar_{vista}.png")
        queixo, bainha = linhas_do_corpo(spr, paleta)
        parado = [base.contorno_final(quadro_parado(spr, f, queixo, bainha), paleta, contorno)
                  for f in fases_parado]
        salvar(np.concatenate([base.para_rgba(q, paleta) for q in parado], axis=1),
               f"clarice_parado_{vista}.png")
        print(f"{vista}: parada, {QUADROS_ANDAR} quadros andando, {QUADROS_PARADO} respirando")

    rets = retratos()
    for nome, rgba in rets.items():
        salvar(rgba, f"clarice_retrato_{nome}.png")
        print(f"retrato {nome}")
    folha_referencia(vistas, andar, rets, paleta).save(
        os.path.join(PASTA_SAIDA, "clarice_referencia.png"))
    print(f"paleta dos sprites: {len(np.unique(paleta, axis=0))} cores")


if __name__ == "__main__":
    main()
