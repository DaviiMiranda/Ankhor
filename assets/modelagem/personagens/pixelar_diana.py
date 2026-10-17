# pixelar_diana.py — transforma a folha de caminhada da Diana
# (diana_referencia/andar.jpg) nos sprites de jogo: pixel art no tamanho do
# jogo (quadro de 96 x 112), paleta fechada, nos mesmos nomes e tamanhos dos
# outros personagens. As ferramentas (máscara, redução, paleta por k-médias,
# contorno, giro de pixel art) são as do pixelar_gabriel.py.
#
# Como rodar (só precisa de Python 3 com Pillow e NumPy, sem Blender):
#
#   python assets/modelagem/personagens/pixelar_diana.py
#
# Os retratos dela saem do pixelar_retratos.py, não daqui.
#
# Entrada: diana_referencia/andar.jpg (2000 x 1116), duas fileiras de seis
# poses de uma grade:
#   fileira de cima  andando de lado, para a direita (a mesma sequência de
#                    três poses desenhada duas vezes)
#   fileira de baixo cinco poses em 3/4 de frente andando para a esquerda e,
#                    por último, uma pose em 3/4 de costas andando para a
#                    direita
#
# Saída (assets/sprites/personagens/diana/):
#   diana_<vista>.png          96 x 112, parada
#   diana_parado_<vista>.png   respiração, 8 quadros de 96 x 112
#   diana_referencia.png       folha com o que sai daqui, para conferir
# para as vistas lado, tres_quartos e tres_quartos_costas. A folha não tem
# Diana de frente nem de costas, e não tem uma caminhada completa (as poses
# mostram sempre a mesma perna à frente), então ainda não há diana_andar_*.
#
# No jogo todos os sprites olham para a direita e o Godot espelha para a
# esquerda. A fileira de baixo vem virada para a esquerda, então o 3/4 de
# frente é espelhado aqui.

import os
import sys

import numpy as np
from PIL import Image, ImageDraw

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA_SCRIPT)
import pixelar_gabriel as base  # noqa: E402

PASTA_REF = os.path.join(PASTA_SCRIPT, "diana_referencia")
PASTA_SAIDA = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "sprites",
                                            "personagens", "diana"))

QUADRO = base.QUADRO
LINHA_PE = base.LINHA_PE
CENTRO_X = base.CENTRO_X
QUADROS_PARADO = base.QUADROS_PARADO
MAX_CORES = 48

# Altura da Diana no sprite, do alto do cabelo à sola da bota: 1,65 m do
# couro cabeludo ao pé (90 px na escala do Gabriel, que tem 1,75 m e 97 px
# sem o volume do cabelo) e o volume do cabelo por cima.
ALTURA_PX = 92

# O fundo da folha tem uma grade de linhas só um pouco mais claras que ele.
# Fundo é o que parece o cinza liso ou o cinza da grade (tolerância pequena nos
# dois: a calça escura e o contorno ficam perto do cinza do fundo) E está
# ligado à borda da imagem.
TOLERANCIA_FUNDO = 12
TOLERANCIA_GRADE = 14
SOMA_GRADE = np.array([22, 24, 24], np.float32)
# Faixas de linhas de cada fileira (a folha termina em uma borda mais clara).
FILEIRAS = {"cima": (30, 575), "baixo": (575, 1100)}
LARGURA_MINIMA = 100

# vista -> (fileira, quais poses, se espelha)
VISTAS = {
    "lado": ("cima", range(0, 6), False),
    "tres_quartos": ("baixo", range(0, 5), True),
    "tres_quartos_costas": ("baixo", range(5, 6), False),
}


# Como cada vista fica em pé. Todas as poses da folha estão no meio de um
# passo; para a Diana ficar parada, uma perna fica como está e a outra é
# trocada por uma cópia dela:
#   pose    qual das poses desenhadas serve de base (a de passo mais curto)
#   boa     a perna que fica (polígono, em pixels do quadro de 96 x 112)
#   ruim    a perna que sai (tudo o que o polígono cobre é apagado)
#   copia   quanto a cópia da perna boa anda (dx, dy), e quanto escurece
#   girar   (graus, pivô) para a perna boa antes de copiar, se ela estiver
#           torta (positivo leva o pé para a direita)
#   queixo, bainha  linhas do corpo para a respiração (ver quadro_parado)
PARADA = {
    "lado": {
        "pose": 2,
        "boa": [(50, 69), (70, 69), (70, 108), (50, 108)],
        "ruim": [(20, 73), (50, 73), (50, 108), (20, 108)],
        "copia": (-4, 0), "escurece": 0.78, "girar": None,
        "queixo": 35, "bainha": 67,
    },
    "tres_quartos": {
        "pose": 3,
        "boa": [(26, 73), (42, 73), (42, 108), (26, 108)],
        "ruim": [(43, 73), (80, 73), (80, 108), (43, 108)],
        "copia": (11, 0), "escurece": 0.78, "girar": None,
        "queixo": 36, "bainha": 66,
    },
    "tres_quartos_costas": {
        "pose": 0,
        "boa": [(50, 67), (74, 67), (74, 108), (50, 108)],
        "ruim": [(18, 70), (49, 70), (49, 108), (18, 108)],
        "copia": (-11, 0), "escurece": 0.78, "girar": (-8.0, (53.0, 72.0)),
        "queixo": 38, "bainha": 65,
    },
}
SUBIDA = 2.0


# ---------------------------------------------------------------------------
# 1. Recorte e redução
# ---------------------------------------------------------------------------

def separar_figuras(ocupadas, vazio_minimo=12):
    colunas = np.where(ocupadas)[0]
    grupos, inicio, anterior = [], colunas[0], colunas[0]
    for c in colunas[1:]:
        if c - anterior > vazio_minimo:
            grupos.append((inicio, anterior))
            inicio = c
        anterior = c
    grupos.append((inicio, anterior))
    return [(a, b) for a, b in grupos if b - a + 1 >= LARGURA_MINIMA]


def mascara_com_grade(rgb):
    borda = np.concatenate([rgb[:4].reshape(-1, 3), rgb[:, :4].reshape(-1, 3),
                            rgb[:, -4:].reshape(-1, 3)])
    fundo = np.median(borda, axis=0)
    grade = fundo + SOMA_GRADE
    parece_fundo = ((np.abs(rgb - fundo).max(axis=2) <= TOLERANCIA_FUNDO)
                    | (np.abs(rgb - grade).max(axis=2) <= TOLERANCIA_GRADE))
    h, w = parece_fundo.shape
    img = Image.new("L", (w + 2, h + 2), 255)
    img.paste(Image.fromarray(parece_fundo.astype(np.uint8) * 255), (1, 1))
    ImageDraw.floodfill(img, (0, 0), 128, thresh=0)
    return np.asarray(img)[1:-1, 1:-1] != 128


def recortar_fileira(img, fileira):
    y0, y1 = FILEIRAS[fileira]
    rgb = np.asarray(img.crop((0, y0, img.width, y1))).astype(np.float32)
    mascara = mascara_com_grade(rgb)
    figuras = []
    for a, b in separar_figuras(mascara.sum(axis=0) > 3):
        fig_rgb, fig_m = base.aparar(rgb[:, a:b + 1], mascara[:, a:b + 1])
        figuras.append((fig_rgb, fig_m))
    return figuras


def recortar_poses():
    img = Image.open(os.path.join(PASTA_REF, "andar.jpg")).convert("RGB")
    fileiras = {f: recortar_fileira(img, f) for f in FILEIRAS}
    poses = {}
    for vista, (fileira, quais, espelhar) in VISTAS.items():
        poses[vista] = []
        for i in quais:
            rgb, m = fileiras[fileira][i]
            if espelhar:
                rgb, m = rgb[:, ::-1].copy(), m[:, ::-1].copy()
            poses[vista].append((rgb, m))
    return poses


def reduzir_vista(poses):
    # Todas as poses da vista saem da mesma folha, na mesma escala: a escala
    # é a que leva a pose mais alta (a de passo mais curto) a ALTURA_PX.
    altura = max(m.shape[0] for _, m in poses)
    escala = ALTURA_PX / altura
    reduzidas = []
    for rgb, m in poses:
        largura = max(1, round(m.shape[1] * escala))
        alt = max(1, round(m.shape[0] * escala))
        reduzidas.append(base.reduzir(rgb, m, largura, alt))
    return reduzidas


def no_quadro(cor_m, paleta):
    # Põe a figura no quadro: o pé mais baixo na linha do chão e o meio do
    # corpo na coluna do centro.
    cor, m = cor_m
    spr = base.indexar(cor, m, paleta)
    quadro = base.vazio()
    ys, xs = np.where(spr >= 0)
    x0 = int(round(CENTRO_X + 0.5 - (xs.min() + xs.max() + 1) / 2))
    y0 = LINHA_PE - ys.max()
    ok = (ys + y0 >= 0) & (ys + y0 < QUADRO[1]) & (xs + x0 >= 0) & (xs + x0 < QUADRO[0])
    quadro[ys[ok] + y0, xs[ok] + x0] = spr[ys[ok], xs[ok]]
    return quadro


# ---------------------------------------------------------------------------
# 2. Em pé
# ---------------------------------------------------------------------------

def ficar_em_pe(spr, cfg, paleta):
    boa = base.mascara_poligono(cfg["boa"])
    ruim = base.mascara_poligono(cfg["ruim"])
    perna = base.so(spr, boa)
    if cfg["girar"] is not None:
        graus, pivo = cfg["girar"]
        perna = base.limpar_migalhas(base.girar(perna, graus, pivo), 4)
    dx, dy = cfg["copia"]
    de_tras = base.escurecer(base.mover(perna, dx, dy), base.tabela_escura(paleta, cfg["escurece"]))
    corpo = np.where(ruim | boa, -1, spr)
    em_pe = base.compor(de_tras, corpo, perna)
    return base.limpar_migalhas(em_pe, 6)


# ---------------------------------------------------------------------------
# 3. Respiração
# ---------------------------------------------------------------------------
# A mesma conta do Gabriel (pixelar_gabriel.py, quadro_parado): o peito sobe
# até 2 pixels e a cabeça vai junto, 60° atrasada; as pernas não mexem.

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
# 4. Folha de conferência
# ---------------------------------------------------------------------------

def folha_referencia(paradas, paleta):
    # As vistas paradas, em cima, e os retratos (feitos pelo pixelar_retratos.py)
    # embaixo, se já existirem.
    retratos = sorted(f for f in os.listdir(PASTA_SAIDA) if f.startswith("diana_retrato_"))
    margem = 8
    largura = max(len(paradas) * (QUADRO[0] + margem), len(retratos) * (base.TAM_RETRATO + margem)) + margem
    altura = margem + QUADRO[1] + margem + base.TAM_RETRATO + margem
    folha = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    for i, spr in enumerate(paradas.values()):
        folha.alpha_composite(Image.fromarray(base.para_rgba(spr, paleta)),
                              (margem + i * (QUADRO[0] + margem), margem))
    for i, nome in enumerate(retratos):
        folha.alpha_composite(Image.open(os.path.join(PASTA_SAIDA, nome)).convert("RGBA"),
                              (margem + i * (base.TAM_RETRATO + margem), 2 * margem + QUADRO[1]))
    return folha


# ---------------------------------------------------------------------------
# 5. Tudo junto
# ---------------------------------------------------------------------------

def salvar(rgba, nome):
    Image.fromarray(rgba, "RGBA").save(os.path.join(PASTA_SAIDA, nome))


def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    poses = recortar_poses()
    reduzidas = {vista: reduzir_vista(p) for vista, p in poses.items()}
    paleta = base.paleta_de([cm for lista in reduzidas.values() for cm in lista], MAX_CORES)
    contorno = base.tabela_escura(paleta, 0.42)
    fases = [360 * q / QUADROS_PARADO for q in range(QUADROS_PARADO)]
    paradas = {}
    for vista, cfg in PARADA.items():
        pose = no_quadro(reduzidas[vista][cfg["pose"]], paleta)
        pose = base.contorno_final(base.contornar(pose, paleta), paleta, contorno)
        parada = base.contorno_final(ficar_em_pe(pose, cfg, paleta), paleta, contorno)
        paradas[vista] = parada
        salvar(base.para_rgba(parada, paleta), f"diana_{vista}.png")
        respirando = [base.contorno_final(quadro_parado(parada, f, cfg["queixo"], cfg["bainha"]),
                                          paleta, contorno) for f in fases]
        salvar(np.concatenate([base.para_rgba(q, paleta) for q in respirando], axis=1),
               f"diana_parado_{vista}.png")
        print(f"{vista}: parada e {QUADROS_PARADO} quadros respirando")
    folha_referencia(paradas, paleta).save(os.path.join(PASTA_SAIDA, "diana_referencia.png"))
    print(f"paleta dos sprites: {len(np.unique(paleta, axis=0))} cores")


if __name__ == "__main__":
    main()
