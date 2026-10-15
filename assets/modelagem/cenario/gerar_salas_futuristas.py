# gerar_salas_futuristas.py — desenha, por código, o visual FUTURISTA das salas
# de aula do Bloco de salas: a cadeira com óculos de realidade virtual no lugar
# da carteira, a lousa holográfica (que mantém os tracinhos do puzzle), o
# professor robô desligado (na doca, caído ou desmontado) e os racks de óculos.
#
# Como rodar (Python 3 + numpy):
#
#   python assets/modelagem/cenario/gerar_salas_futuristas.py
#
# O que sai (em assets/sprites/cenario/):
#   objetos/cadeira_vr.png             24 x 30  cadeira com os óculos no assento (lente ciano)
#   objetos/cadeira_vr_ambar.png       24 x 30  a mesma, com o friso e a lente âmbar (sala dos professores)
#   objetos/cadeira_vr_limpa.png       24 x 30  a mesma, nova em folha (sala 205, "intacta demais")
#   objetos/cadeira_vr_lente.png       24 x 30  só a lente ciano (camada de luz, sem sombreamento)
#   objetos/cadeira_vr_ambar_lente.png 24 x 30  só a lente âmbar
#   objetos/cadeira_vr_caida.png       30 x 16  a cadeira tombada, óculos no chão
#   objetos/estante_oculos_vr.png      64 x 84  rack de óculos para os alunos (3 prateleiras)
#   objetos/estante_oculos_vr_musgo.png 64 x 84 o mesmo rack, tomado de musgo
#   objetos/estante_oculos_vr_lente.png 64 x 84 as lentes acesas e o letreiro do rack
#   objetos/professor_caido.png        64 x 28  o professor robô desligado, deitado no chão
#   objetos/professor_desmontado.png   64 x 16  as peças do professor espalhadas pelo chão
#   objetos/oculos_no_chao.png         20 x 9   dois óculos caídos
#   paredes/parede_lousa_holo_<n>.png  80 x 112 o painel apagado, preso na parede (e _luz.png)
#   paredes/parede_doca_professor*.png 80 x 112 o nicho da doca: padrão, _limpo, _sem_cabeca, _vazia (e _luz.png)
#   paredes/parede_oculos_vr.png       80 x 112 o painel de parede com óculos nos encaixes (e _luz.png)
# Com PREVIA=<pasta>, também salva previa_salas_futuristas.png nela (não commitar).
#
# ---------------------------------------------------------------------------
# DUAS CAMADAS POR PEÇA: O QUE É LUZ NÃO PODE SER ESCURECIDO
# ---------------------------------------------------------------------------
#
# A sala é escura: o Godot multiplica tudo pela cor da escuridão (e pelas
# luzes). Uma lente acesa pintada na peça normal seria escurecida junto e
# pareceria apagada. Por isso o que brilha vai numa SEGUNDA imagem, do mesmo
# tamanho, desenhada com o material "sem luz" (mesma técnica dos olhos dos
# robôs e dos hologramas do Labirinto). A peça principal fica só com o corpo.
#
# A lousa holográfica usa duas receitas de gerar_oficina.py:
#   - LINHAS DE VARREDURA: o alfa de uma fileira em cada três é multiplicado
#     por 0,45, uma onda quadrada vertical, que dá a textura de projeção;
#   - FALHA DE SINAL: uma faixa de fileiras é deslocada alguns pixels para o
#     lado (np.roll), como um quadro que chegou fora de sincronia.
#
# O sombreamento do corpo do robô vem de um gradiente horizontal, com a luz
# do luar vindo da esquerda: valor = base + amplitude * (0,5 - u), onde u vai
# de 0 (borda esquerda da peça) a 1 (borda direita). Perto da borda esquerda o
# tom é mais claro, e perto da direita, mais escuro, o que dá volume de
# cilindro a braços, torso e cabeça sem precisar de mais nada.
#
# A VARIAÇÃO ENTRE SALAS vem de parâmetros e de sementes: o mesmo desenho
# (lousa, doca, rack) muda de estado (trincada, soterrada de areia, com
# musgo, nova em folha) e a semente embaralha reflexos e óculos faltando.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")
PASTA_PAREDES = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "paredes")
PREVIA = os.environ.get("PREVIA", "")

_spec = importlib.util.spec_from_file_location("gerar_kit", os.path.join(PASTA_SCRIPT, "gerar_kit.py"))
kit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kit)
bib = kit.bib
Imagem, RAMPAS, CONTORNO, dilatar = bib.Imagem, bib.RAMPAS, bib.CONTORNO, bib.dilatar

# Casco claro e sujo do mobiliário de 3026: cerâmica fria, escurecida pela
# noite. O topo da rampa (#a0a7b0) é mais escuro que branco de propósito: a
# sala toda é pintada com "luz neutra" 0,7 (ver LUZ no gerar_kit.py).
CASCO = bib.hexa("#101216", "#1d2026", "#2e323a", "#444a53", "#5f6670", "#7d858f", "#a0a7b0")
VIDRO = bib.hexa("#06090c", "#0b1217", "#101b22", "#18272f", "#233640")
# A mesma rampa de ciano e de âmbar dos hologramas do Labirinto.
CIANO = bib.hexa("#04333d", "#0a6173", "#17b2c9", "#5be6f5", "#c9fcff")
AMBAR = bib.hexa("#4a2a08", "#9a5a14", "#e0902a", "#ffd27a")


def rgba(cor, alfa):
    return [cor[0], cor[1], cor[2], int(alfa)]


def gradiente(img, x0, x1, base, amplitude):
    """Valor de 'base + amplitude * (0,5 - u)': claro na esquerda, escuro na
    direita (u = 0 em x0 e 1 em x1)."""
    u = np.clip((img.X - x0) / float(max(x1 - x0, 1)), 0.0, 1.0)
    return base + amplitude * (0.5 - u)


def chanfrar(img, x0, y0, x1, y1):
    """Apaga os quatro pixels de canto de um retângulo (cantinho chanfrado)."""
    for cx, cy in ((x0, y0), (x1 - 1, y0), (x0, y1 - 1), (x1 - 1, y1 - 1)):
        img.apagar(img.ret(cx, cy, cx + 1, cy + 1))


def varredura(img, fator=0.45):
    """Uma fileira em cada três perde alfa: a textura de projeção."""
    for y in range(img.h):
        if y % 3 == 2:
            img.px[y, :, 3] = (img.px[y, :, 3] * fator).astype(np.uint8)


def sobrepor(fundo, camada, x, y):
    """Compõe a camada de luz sobre o fundo respeitando o alfa, como o Godot
    faz com o material sem luz: cor = fundo * (1 - a) + camada * a."""
    a = camada.px[..., 3:4].astype(float) / 255.0
    area = fundo.px[y:y + camada.h, x:x + camada.w]
    area[..., :3] = (area[..., :3] * (1 - a) + camada.px[..., :3] * a).astype(np.uint8)


# ---------------------------------------------------------------------------
# Óculos de frente (usados nos racks) e letras do letreiro
# ---------------------------------------------------------------------------

LETRA_V = ("1...1", "1...1", "1...1", ".1.1.", "..1..")
LETRA_R = ("1111.", "1...1", "1111.", "1..1.", "1...1")


def letras_vr(lente, x, y, cor, alfa=230):
    for deslocamento, letra in ((0, LETRA_V), (7, LETRA_R)):
        for j, linha in enumerate(letra):
            for i, c in enumerate(linha):
                if c == "1":
                    lente.cor(lente.ret(x + deslocamento + i, y + j, x + deslocamento + i + 1, y + j + 1), rgba(cor, alfa))


def oculos_frente(img, lente, x, y, cor_lente, aceso, largura=10, altura=5):
    """Um óculos visto de frente, no encaixe do rack: casco claro, visor
    escuro e duas lentes quadradas. Acesas, as lentes vão para a camada de luz."""
    img.pintar(img.ret(x, y, x + largura, y + altura), CASCO, 0.52)
    img.pintar(img.ret(x, y, x + largura, y + 1), CASCO, 0.85)
    img.pintar(img.ret(x + 1, y + 1, x + largura - 1, y + altura - 1), VIDRO, 0.1)
    img.cor(img.ret(x - 1, y + 2, x, y + 3), RAMPAS["metal"][2])
    img.cor(img.ret(x + largura, y + 2, x + largura + 1, y + 3), RAMPAS["metal"][2])
    for cx in (x + 2, x + largura - 4):
        img.cor(img.ret(cx, y + 2, cx + 2, y + 4), VIDRO[0])
        if aceso:
            lente.cor(lente.ret(cx, y + 2, cx + 2, y + 4), rgba(cor_lente[3], 255))


# ---------------------------------------------------------------------------
# Cadeira com óculos VR
# ---------------------------------------------------------------------------

ACABAMENTOS = {
    "ciano": dict(friso=CIANO[0], lente=CIANO, musgo=0.08, tom=0.0),
    "ambar": dict(friso=AMBAR[0], lente=AMBAR, musgo=0.08, tom=0.0),
    "limpa": dict(friso=CIANO[2], lente=CIANO, musgo=0.0, tom=0.12),
}


def cadeira_vr(acabamento="ciano"):
    """Cadeira de sala de aula de 3026, vista de lado, virada para a direita
    como a carteira antiga: pedestal único com disco no chão, assento e
    encosto de casco moldado, e os óculos de realidade virtual deixados no
    assento, com a tira de cabeça em laço. A lente (camada de luz) sai à
    parte. Pé em (11, 29): mesma pegada da carteira. O acabamento troca o
    friso e a cor da lente (ou tira o musgo, na sala 205)."""
    a = ACABAMENTOS[acabamento]
    t = a["tom"]
    img = Imagem(24, 30)
    lente = Imagem(24, 30)
    img.pintar(img.elipse(11, 28, 8, 2), CASCO, 0.28 + t)
    img.pintar(img.ret(10, 21, 13, 27), CASCO, gradiente(img, 10, 13, 0.4 + t, 0.5))
    img.pintar(img.ret(9, 24, 14, 25), "metal", 0.45)
    assento = img.poligono([(3, 18), (19, 17), (20, 19), (18, 21), (4, 21)])
    img.pintar(assento, CASCO, gradiente(img, 3, 20, 0.5 + t, 0.35))
    img.pintar(img.ret(5, 17, 19, 18) & assento, CASCO, 0.78 + t)
    img.cor(img.ret(6, 20, 17, 21), rgba(a["friso"], 255))
    encosto = img.poligono([(2, 19), (1, 7), (3, 3), (7, 3), (7, 19)])
    img.pintar(encosto, CASCO, gradiente(img, 1, 7, 0.45 + t, 0.4))
    img.pintar(img.ret(4, 5, 7, 18) & encosto, VIDRO, 0.45)
    img.pintar(img.ret(3, 3, 7, 4), CASCO, 0.8 + t)
    img.pintar(img.ret(9, 11, 17, 17), "metal", 0.28)
    img.pintar(img.ret(9, 11, 17, 12), "metal", 0.7)
    img.pintar(img.ret(8, 12, 9, 16), "tecido", 0.35)
    img.pintar(img.ret(17, 12, 19, 16), CASCO, 0.62 + t)
    img.pintar(img.ret(17, 13, 19, 15), VIDRO, 0.25)
    laco = img.elipse(8.5, 10.5, 4.5, 5) & ~img.elipse(8.5, 10.5, 3.2, 3.8)
    img.pintar(laco & (img.Y < 15), "metal", 0.22)
    lente.cor(lente.ret(17, 13, 19, 15), rgba(a["lente"][-2], 255))
    lente.cor(lente.ret(17, 13, 18, 14), rgba(a["lente"][-1], 255))
    if a["musgo"] > 0:
        bib.musgo_por_cima(img, a["musgo"], 160)
    img.contornar()
    return img, lente


def cadeira_vr_caida():
    """A mesma cadeira tombada de lado: o assento em pé, o encosto deitado
    para a esquerda, o pedestal apontando para a direita, e os óculos caídos
    no chão, com a lente trincada e apagada."""
    img = Imagem(30, 16)
    img.pintar(img.ret(14, 3, 18, 15), CASCO, gradiente(img, 14, 18, 0.5, 0.4))
    img.pintar(img.ret(14, 3, 15, 15), CASCO, 0.78)
    img.pintar(img.ret(18, 8, 26, 11), CASCO, gradiente(img, 18, 26, 0.4, 0.5))
    img.pintar(img.elipse(27, 8.5, 1.8, 5), CASCO, 0.3)
    encosto = img.poligono([(7, 10), (14, 9), (14, 15), (6, 15), (4, 13)])
    img.pintar(encosto, CASCO, gradiente(img, 4, 14, 0.45, 0.4))
    img.pintar(img.ret(7, 12, 13, 14), VIDRO, 0.45)
    img.pintar(img.ret(0, 11, 7, 15), "metal", 0.28)
    img.pintar(img.ret(0, 11, 7, 12), "metal", 0.65)
    img.pintar(img.ret(0, 12, 2, 15), CASCO, 0.6)
    img.pintar(img.ret(0, 12, 2, 15), VIDRO, 0.2)
    img.cor(img.caminho([(0.5, 12), (1.5, 14.5)], 0.4), rgba(CASCO[6], 255))
    bib.musgo_por_cima(img, 0.12, 161)
    img.contornar()
    return img


def oculos_no_chao():
    """Dois óculos caídos no chão, um virado para cima, com a tira em laço.
    Sem colisão: dá para pisar por cima."""
    img = Imagem(20, 9)
    laco = img.elipse(5, 4, 4.5, 3.5) & ~img.elipse(5, 4, 3, 2.2)
    img.pintar(laco, "metal", 0.25)
    img.pintar(img.ret(5, 3, 15, 8), CASCO, 0.38)
    img.pintar(img.ret(5, 3, 15, 4), CASCO, 0.75)
    img.pintar(img.ret(6, 4, 14, 7), VIDRO, 0.16)
    img.cor(img.ret(7, 5, 9, 7), VIDRO[0])
    img.cor(img.ret(11, 5, 13, 7), VIDRO[0])
    img.pintar(img.ret(10, 0, 19, 4), CASCO, 0.3)
    img.pintar(img.ret(10, 0, 19, 1), CASCO, 0.65)
    img.cor(img.ret(12, 1, 14, 3), VIDRO[1])
    img.cor(img.caminho([(17, 1), (15, 3)], 0.4), rgba(CASCO[6], 255))
    img.contornar()
    return img


# ---------------------------------------------------------------------------
# Racks de óculos
# ---------------------------------------------------------------------------


def rack_oculos(musgo=False, semente=0):
    """O rack de óculos para os alunos: moldura de casco, fundo escuro, o
    letreiro 'VR' no alto e três prateleiras de quatro óculos. Alguns
    encaixes estão vazios (alguém levou), e uns poucos óculos ainda têm a
    lente acesa. Pé em (32, 83): a mesma base da estante vazia da Biblioteca,
    então troca com ela sem mexer na navegação."""
    rng = np.random.default_rng(310 + semente)
    img = Imagem(64, 84)
    lente = Imagem(64, 84)
    corpo = img.ret(0, 0, 64, 82)
    img.pintar(corpo, CASCO, gradiente(img, 0, 64, 0.42, 0.34) + 0.04 * (1 - (img.Y / 82.0)))
    chanfrar(img, 0, 0, 64, 82)
    img.pintar(img.ret(0, 0, 64, 1), CASCO, 0.85)
    img.pintar(img.ret(3, 13, 61, 79), VIDRO, 0.12)
    img.pintar(img.ret(3, 13, 61, 14), VIDRO, 0.02)
    img.pintar(img.ret(3, 3, 61, 11), VIDRO, 0.1)
    letras_vr(lente, 8, 4, CIANO[3])
    for x in range(26, 56, 3):
        lente.cor(lente.ret(x, 6, x + 2, 7), rgba(CIANO[2], 170))
    for fileira in range(3):
        y = 19 + fileira * 18
        for k in range(4):
            x = 8 + k * 13
            if rng.random() < 0.22:
                continue
            aceso = rng.random() < 0.24
            oculos_frente(img, lente, x, y, CIANO, aceso, largura=11, altura=6)
        img.pintar(img.ret(3, y + 8, 61, y + 10), "metal", 0.4)
        img.pintar(img.ret(3, y + 8, 61, y + 9), "metal", 0.72)
    img.pintar(img.ret(3, 69, 61, 79), CASCO, 0.34)
    img.pintar(img.ret(3, 69, 61, 70), CASCO, 0.7)
    img.pintar(img.ret(26, 73, 38, 75), "metal", 0.6)
    img.pintar(img.ret(4, 82, 12, 84), "metal", 0.18)
    img.pintar(img.ret(52, 82, 60, 84), "metal", 0.18)
    if musgo:
        bib.musgo_por_cima(img, 0.45, 311 + semente)
        for x in (10, 29, 51):
            img.pintar(img.caminho([(x, 12), (x + 1, 22), (x - 1, 34)], 0.5) & img.ret(3, 12, 61, 80), "verde", 0.5, achatar=False)
    img.contornar()
    return img, lente


def parede_oculos():
    """Painel de parede com 3 fileiras de 5 óculos nos encaixes, com uma
    faixa de título e a luz de status âmbar. Os que ainda estão carregados
    acendem a lente."""
    rng = np.random.default_rng(320)
    img = kit.parede_base()
    lente = Imagem(80, 112)
    img.pintar(img.ret(8, 22, 72, 78), "metal", 0.3 + 0.08 * img.fino)
    img.pintar(img.ret(8, 22, 72, 23), "metal", 0.62)
    img.pintar(img.ret(10, 24, 70, 76), VIDRO, 0.14)
    img.pintar(img.ret(10, 24, 70, 31), VIDRO, 0.04)
    letras_vr(lente, 13, 25, CIANO[3])
    for x in range(30, 60, 3):
        lente.cor(lente.ret(x, 27, x + 2, 28), rgba(CIANO[2], 170))
    lente.cor(lente.ret(64, 26, 67, 29), rgba(AMBAR[2], 255))
    for fileira in range(3):
        y = 36 + fileira * 13
        for k in range(5):
            x = 12 + k * 12
            if rng.random() < 0.15:
                continue
            oculos_frente(img, lente, x, y, CIANO, rng.random() < 0.28)
        img.pintar(img.ret(10, y + 6, 70, y + 8), "metal", 0.42)
        img.pintar(img.ret(10, y + 6, 70, y + 7), "metal", 0.7)
    img.pintar(img.ret(14, 78, 18, 80), "metal", 0.2)
    img.pintar(img.ret(62, 78, 66, 80), "metal", 0.2)
    return img, lente


# ---------------------------------------------------------------------------
# Lousa holográfica
# ---------------------------------------------------------------------------

LOUSA_X0, LOUSA_X1, LOUSA_Y0, LOUSA_Y1 = 6, 74, 26, 70
VIDRO_X0, VIDRO_X1, VIDRO_Y0, VIDRO_Y1 = 8, 72, 28, 68

# Cada lousa é um dicionário de parâmetros: o corpo e a luz dependem dele.
LOUSAS = {
    "parede_lousa_holo_7": dict(tracinhos=7),
    "parede_lousa_holo_3": dict(tracinhos=3, semente=1),
    "parede_lousa_holo_0": dict(tracinhos=0, semente=2),
    "parede_lousa_holo_25": dict(tracinhos=25, semente=8),
    "parede_lousa_holo_25_areia": dict(tracinhos=25, areia=True, semente=3),
    "parede_lousa_holo_25_trincada": dict(tracinhos=25, trincada=True, semente=4),
    "parede_lousa_holo_25_musgo": dict(tracinhos=25, musgo=True, semente=5),
    "parede_lousa_holo_8_limpa": dict(tracinhos=8, limpa=True, semente=6),
    "parede_lousa_holo_mapa": dict(mapa=True, semente=7),
}


def mascara_areia(img):
    """O monte de areia que a duna empurrou para dentro da sala: cobre o
    canto de baixo do painel."""
    monte = img.elipse(24, 70, 26, 15) | img.elipse(62, 70, 15, 9)
    return monte & img.ret(LOUSA_X0 - 2, LOUSA_Y0, LOUSA_X1 + 2, LOUSA_Y1 + 4)


def mascara_canto_quebrado(img):
    return img.poligono([(VIDRO_X0, VIDRO_Y0), (VIDRO_X0 + 16, VIDRO_Y0), (VIDRO_X0 + 9, VIDRO_Y0 + 8),
                         (VIDRO_X0 + 3, VIDRO_Y0 + 15), (VIDRO_X0, VIDRO_Y0 + 17)])


def lousa_corpo(tracinhos=0, semente=0, trincada=False, areia=False, musgo=False, limpa=False, mapa=False):
    """O painel de ensino que substituiu o quadro-negro: moldura de metal
    escuro, vidro apagado com reflexos e a barra do emissor embaixo. Mesmo
    lugar da lousa antiga (a parede_lousa), então os tracinhos continuam onde
    o jogador procura. O estado muda por sala: pixels mortos e trinca fina
    (padrão), vidro quebrado (trincada), areia da duna (areia), musgo
    (musgo), nova em folha (limpa) ou o mapa a giz da Clarice (mapa)."""
    img = kit.parede_base()
    X, Y = img.X, img.Y
    img.pintar(img.ret(LOUSA_X0, LOUSA_Y0, LOUSA_X1, LOUSA_Y1), "metal", 0.28 + 0.1 * img.fino)
    img.pintar(img.ret(LOUSA_X0, LOUSA_Y0, LOUSA_X1, LOUSA_Y0 + 1), "metal", 0.62)
    vidro = img.ret(VIDRO_X0, VIDRO_Y0, VIDRO_X1, VIDRO_Y1)
    reflexo = kit.ruido_ciclico(img.w, img.h, 20, 12, 90 + semente)
    if limpa:
        img.pintar(vidro, VIDRO, 0.3 + 0.22 * reflexo)
    else:
        img.pintar(vidro, VIDRO, 0.18 + 0.4 * reflexo)
    faixa = vidro & (((X * 2 + Y * 3 + semente * 5) % 47) < 4)
    img.pintar(faixa, VIDRO, 0.85, achatar=False)
    if not limpa:
        mortos = img.ret(VIDRO_X1 - 17, VIDRO_Y0, VIDRO_X1, VIDRO_Y0 + 10)
        img.cor(mortos, VIDRO[0])
        img.pintar(mortos & (((X + Y) % 4) == 0), VIDRO, 0.5, achatar=False)
        trinca = img.caminho([(24, VIDRO_Y1), (27, 58), (25, 52), (30, 45), (29, 40)], 0.45) & vidro
        img.pintar(trinca, VIDRO, 1.0, achatar=False)
    if trincada:
        impacto = (52, 44)
        for fim in ((VIDRO_X1, 30), (VIDRO_X1, 62), (30, VIDRO_Y1), (16, 52), (44, VIDRO_Y0), (VIDRO_X1, 46)):
            meio = ((impacto[0] + fim[0]) / 2 + 3, (impacto[1] + fim[1]) / 2 - 2)
            img.pintar(img.caminho([impacto, meio, fim], 0.45) & vidro, VIDRO, 1.0, achatar=False)
        img.pintar(img.elipse(impacto[0], impacto[1], 4, 3) & vidro, VIDRO, 0.0, achatar=False)
        quebrado = mascara_canto_quebrado(img)
        img.pintar(quebrado, "metal", 0.1)
        img.pintar(quebrado & (((X + Y) % 3) == 0), "concreto", 0.1, achatar=False)
    if mapa:
        giz = img.ret(0, 0, 0, 0)
        for y0 in (33, 49):
            for k in range(6):
                x0 = 8 + k * 9
                giz |= (img.ret(x0, y0, x0 + 8, y0 + 1) | img.ret(x0, y0 + 8, x0 + 8, y0 + 9)
                        | img.ret(x0, y0, x0 + 1, y0 + 9) | img.ret(x0 + 7, y0, x0 + 8, y0 + 9))
        giz |= img.linha(63, 57, 70, 34, 0.5)
        for k in range(4):
            giz |= img.ret(64 + k * 2, 53 - k * 5, 67 + k * 2, 54 - k * 5)
        giz |= img.linha(70, 34, 70, 30, 0.5) | img.linha(68, 32, 70, 30, 0.5) | img.linha(72, 32, 70, 30, 0.5)
        img.pintar(giz & vidro, "ceu", 0.8, achatar=False)
        x103 = 8 + 2 * 9
        img.pintar(img.ret(x103 + 3, 52, x103 + 5, 55), "ceu", 0.95)
        x206 = 8 + 5 * 9
        xis = img.linha(x206 + 2, 35, x206 + 5, 39, 0.5) | img.linha(x206 + 5, 35, x206 + 2, 39, 0.5)
        img.pintar(xis & vidro, "sol", 0.8, achatar=False)
    img.pintar(img.ret(LOUSA_X0 + 14, LOUSA_Y1, LOUSA_X1 - 14, LOUSA_Y1 + 2), "metal", 0.4)
    img.pintar(img.ret(LOUSA_X0 + 14, LOUSA_Y1, LOUSA_X1 - 14, LOUSA_Y1 + 1), "metal", 0.7)
    for x in (LOUSA_X0 + 18, LOUSA_X1 - 20):
        img.cor(img.ret(x, LOUSA_Y1 + 1, x + 2, LOUSA_Y1 + 2), rgba(AMBAR[0], 255))
    img.pintar(img.ret(LOUSA_X0 - 1, LOUSA_Y0 + 6, LOUSA_X0, LOUSA_Y0 + 14), "metal", 0.15)
    img.pintar(img.ret(LOUSA_X1, LOUSA_Y0 + 6, LOUSA_X1 + 1, LOUSA_Y0 + 14), "metal", 0.15)
    if musgo:
        moldura = img.ret(LOUSA_X0 - 1, LOUSA_Y0 - 1, LOUSA_X1 + 1, LOUSA_Y1 + 3) & ~vidro
        mancha = kit.ruido_ciclico(img.w, img.h, 4, 3, 330 + semente) > 0.38
        img.pintar(moldura & mancha, "verde", 0.45 + 0.3 * img.fino)
        for x in (14, 31, 52, 66):
            img.pintar(img.caminho([(x, LOUSA_Y0), (x + 1, LOUSA_Y0 + 9), (x - 1, LOUSA_Y0 + 15)], 0.5) & vidro,
                       "verde", 0.55, achatar=False)
    if areia:
        monte = mascara_areia(img)
        img.pintar(monte, "areia", 0.22 + 0.3 * kit.ruido_ciclico(img.w, img.h, 4, 3, 340) + 0.08 * img.fino)
    return img


def falha(img, y0, y1, desloca):
    """Desloca uma faixa de fileiras para o lado (quadro fora de sincronia),
    só dentro do vidro: a borda do painel não sai da moldura."""
    faixa = img.px[y0:y1, VIDRO_X0:VIDRO_X1].copy()
    img.px[y0:y1, VIDRO_X0:VIDRO_X1] = np.roll(faixa, desloca, axis=1)


def lousa_luz(tracinhos=0, semente=0, trincada=False, areia=False, musgo=False, limpa=False, mapa=False):
    """O que o painel ainda mostra: um véu ciano quase invisível, o resto
    apagado da conta (traços curtos, uma raiz, uma fração), uma faixa de
    falha, o aviso âmbar de 'sem sinal' e, embaixo, os TRACINHOS contados em
    grupos de cinco (quatro em pé e um cortando), na mesma geometria da
    lousa de giz: grupos de 12 px, riscos a cada 2 px. A lousa nova em folha
    (205) mostra só uma fileira de riscos gravados, estável e sem falha. A
    do mapa da Clarice não mostra nada: só a luz de status âmbar."""
    luz = Imagem(80, 112)
    if mapa:
        luz.cor(luz.ret(LOUSA_X0 + 18, LOUSA_Y1 + 1, LOUSA_X0 + 20, LOUSA_Y1 + 2), rgba(AMBAR[2], 255))
        return luz
    vidro = luz.ret(VIDRO_X0, VIDRO_Y0, VIDRO_X1, VIDRO_Y1)
    if limpa:
        luz.cor(vidro, rgba(CIANO[1], 38))
        borda = vidro & ~luz.ret(VIDRO_X0 + 1, VIDRO_Y0 + 1, VIDRO_X1 - 1, VIDRO_Y1 - 1)
        luz.cor(borda, rgba(CIANO[3], 200))
        varredura(luz, 0.7)
        for k in range(tracinhos):
            gx = VIDRO_X0 + 12 + k * 6
            luz.cor(luz.ret(gx, VIDRO_Y1 - 26, gx + 1, VIDRO_Y1 - 14), rgba(CIANO[4], 255))
        luz.cor(luz.ret(LOUSA_X0 + 18, LOUSA_Y1 + 1, LOUSA_X0 + 20, LOUSA_Y1 + 2), rgba(CIANO[3], 255))
        return luz
    veu = vidro.copy()
    if trincada:
        veu &= luz.ret(VIDRO_X0, VIDRO_Y0, 50, VIDRO_Y1)
    luz.cor(veu, rgba(CIANO[1], 22))
    luz.cor(luz.ret(VIDRO_X0, VIDRO_Y0, VIDRO_X1, VIDRO_Y0 + 1) & veu, rgba(CIANO[2], 110))
    luz.cor(luz.ret(VIDRO_X0, VIDRO_Y1 - 1, VIDRO_X1, VIDRO_Y1) & veu, rgba(CIANO[2], 110))
    luz.cor(luz.ret(VIDRO_X0, VIDRO_Y0, VIDRO_X0 + 1, VIDRO_Y1), rgba(CIANO[2], 110))
    luz.cor(luz.ret(VIDRO_X1 - 1, VIDRO_Y0, VIDRO_X1, VIDRO_Y1) & veu, rgba(CIANO[2], 110))
    conta = luz.ret(0, 0, 0, 0)
    for y, x0, x1 in ((34, 14, 36), (39, 14, 30), (44, 18, 44)):
        conta |= luz.ret(x0, y, x1, y + 1)
    conta |= luz.caminho([(40, 34), (42, 37), (44, 33), (50, 33)], 0.5)
    conta |= luz.ret(14, 49, 28, 50) | luz.ret(18, 46, 19, 49) | luz.ret(22, 51, 24, 52)
    luz.cor(conta & vidro & veu, rgba(CIANO[3], 120))
    luz.cor(luz.ret(VIDRO_X0 + 3, VIDRO_Y0 + 3, VIDRO_X0 + 13, VIDRO_Y0 + 5), rgba(AMBAR[2], 235))
    varredura(luz)
    falha(luz, 40 + semente % 3, 43 + semente % 3, 3 + (semente % 2))
    if trincada:
        falha(luz, 52, 55, -4)
    tinta = luz.ret(0, 0, 0, 0)
    for g in range((tracinhos + 4) // 5):
        gx, gy = VIDRO_X0 + 6 + g * 12, VIDRO_Y1 - 12
        no_grupo = min(5, tracinhos - 5 * g)
        for k in range(min(4, no_grupo)):
            tinta |= luz.ret(gx + 2 * k, gy, gx + 2 * k + 1, gy + 7)
        if no_grupo == 5:
            tinta |= luz.linha(gx - 1, gy + 5, gx + 8, gy + 1, 0.45)
    if trincada:
        tinta &= luz.ret(0, 0, 50, 112)
    luz.cor(tinta, rgba(CIANO[4], 255))
    if areia:
        luz.apagar(mascara_areia(luz))
    if trincada:
        luz.apagar(mascara_canto_quebrado(luz))
    return luz


# ---------------------------------------------------------------------------
# O professor robô: na doca, caído e desmontado
# ---------------------------------------------------------------------------

NICHO_X0, NICHO_X1, NICHO_Y0, NICHO_Y1 = 18, 62, 34, 108


def desenhar_cabeca(img, silhueta_pecas, x, y, largura=20, altura=14, tom=0.58):
    """A cabeça do professor (tela escura, olhos fantasma, trinca), em (x, y).
    Usada na doca e, solta, no chão da doca sem cabeça."""
    X, Y = img.X, img.Y
    cabeca = img.ret(x, y, x + largura, y + altura)
    img.pintar(cabeca, CASCO, gradiente(img, x, x + largura, tom, 0.5))
    chanfrar(img, x, y, x + largura, y + altura)
    img.pintar(img.ret(x, y, x + largura, y + 1), CASCO, 0.9)
    img.pintar(img.ret(x - 2, y + 4, x, y + 11), "metal", 0.3)
    img.pintar(img.ret(x + largura, y + 4, x + largura + 2, y + 11), "metal", 0.22)
    tela = img.ret(x + 2, y + 2, x + largura - 2, y + altura - 2)
    img.pintar(tela, VIDRO, 0.22 + 0.25 * ((X * 2 + Y) % 23 < 4))
    img.pintar(tela & (((X + Y * 2) % 29) < 3) & (Y < y + altura - 4), VIDRO, 0.9, achatar=False)
    img.cor(img.ret(x + 5, y + 5, x + 8, y + 7), CIANO[0])
    img.cor(img.ret(x + largura - 8, y + 5, x + largura - 5, y + 7), CIANO[0])
    img.cor(img.ret(x + 7, y + 9, x + largura - 7, y + 10), CIANO[0])
    img.pintar(img.caminho([(x + largura - 4, y + 2), (x + largura - 6, y + 5), (x + largura - 5, y + 8),
                            (x + largura - 9, y + altura - 2)], 0.45) & tela, CASCO, 0.78, achatar=False)
    return cabeca | img.ret(x - 2, y + 4, x + largura + 2, y + 11)


def doca_professor(estado="padrao"):
    """O nicho da doca de recarga com o professor desligado. O robô é de
    propósito o oposto dos robôs inimigos: baixo (uns 58 px, pouco mais que o
    Gabriel), redondo, claro, com a cabeça de tela e uma base flutuante em
    vez de pernas, para ninguém confundir um com o outro. A tela do rosto
    está escura; um cabo da doca pende solto do teto e termina num plugue no
    ar; a poeira e as manchas de ferrugem dizem há quanto tempo ele está
    parado.

    estado: 'padrao' (o descrito), 'limpo' (nova em folha, sem ferrugem nem
    poeira nem cabo solto), 'sem_cabeca' (o pescoço exposto com fios e a
    cabeça caída na plataforma) ou 'vazia' (só a doca, o anel e o cabo)."""
    limpo = estado == "limpo"
    img = kit.parede_base()
    X, Y = img.X, img.Y
    img.pintar(img.ret(NICHO_X0 - 2, NICHO_Y0 - 2, NICHO_X1 + 2, NICHO_Y1 + 2), "metal", 0.3 + 0.08 * img.fino)
    img.pintar(img.ret(NICHO_X0 - 2, NICHO_Y0 - 2, NICHO_X1 + 2, NICHO_Y0 - 1), "metal", 0.6)
    fundo = img.ret(NICHO_X0, NICHO_Y0, NICHO_X1, NICHO_Y1)
    img.pintar(fundo, "concreto", 0.1 + 0.05 * img.fino + 0.05 * (Y - NICHO_Y0) / (NICHO_Y1 - NICHO_Y0))
    img.pintar(img.ret(NICHO_X0, NICHO_Y0, NICHO_X1, NICHO_Y0 + 4), "concreto", 0.03)
    img.pintar(img.ret(NICHO_X0, NICHO_Y0, NICHO_X0 + 3, NICHO_Y1), "concreto", 0.04)
    img.pintar(img.ret(NICHO_X0 + 6, NICHO_Y0 + 3, NICHO_X1 - 6, NICHO_Y0 + 6), "metal", 0.45)
    img.pintar(img.ret(NICHO_X0 + 6, NICHO_Y0 + 3, NICHO_X1 - 6, NICHO_Y0 + 4), "metal", 0.75)
    img.pintar(img.ret(NICHO_X0, 104, NICHO_X1, NICHO_Y1), "metal", 0.32)
    img.pintar(img.ret(NICHO_X0, 104, NICHO_X1, 105), "metal", 0.68)

    silhueta = img.ret(0, 0, 0, 0)

    def peca(mascara, rampa, valor):
        nonlocal silhueta
        img.pintar(mascara, rampa, valor)
        silhueta |= mascara

    if estado == "vazia":
        img.pintar(img.elipse(40, 104, 12, 2.6), "metal", 0.45)
        anel = img.elipse(40, 104, 10, 2.0) & ~img.elipse(40, 104, 7.5, 1.2)
        img.cor(anel, CIANO[0])
    else:
        peca(img.elipse(40, 101, 11.5, 3.6), CASCO, 0.32)
        peca(img.ret(29, 101, 51, 104) & img.elipse(40, 102, 11.5, 3.2), CASCO, 0.14)
        anel = img.elipse(40, 101, 9.5, 2.7) & ~img.elipse(40, 101, 7.5, 1.7)
        img.cor(anel, CIANO[0])
        peca(img.poligono([(33, 79), (47, 79), (50, 99), (30, 99)]), CASCO, gradiente(img, 30, 50, 0.46, 0.4))
        peca(img.ret(31, 62, 49, 80), CASCO, gradiente(img, 31, 49, 0.55, 0.45))
        chanfrar(img, 31, 62, 49, 80)
        img.pintar(img.ret(31, 62, 49, 63), CASCO, 0.85)
        img.pintar(img.ret(32, 77, 48, 79), CASCO, 0.22)
        img.pintar(img.ret(34, 66, 46, 76), VIDRO, 0.32)
        img.pintar(img.elipse(40, 71, 3.4, 3.4), CASCO, 0.28)
        img.pintar(img.elipse(40, 71, 2.2, 2.2), VIDRO, 0.12)
        img.cor(img.ret(39, 70, 40, 71), CIANO[0])
        for cx in (30, 50):
            peca(img.elipse(cx, 66, 3.4, 3.4), CASCO, gradiente(img, cx - 3, cx + 3, 0.5, 0.35))
        peca(img.ret(26, 67, 30, 79), CASCO, gradiente(img, 26, 30, 0.45, 0.5))
        peca(img.ret(27, 79, 30, 88), CASCO, gradiente(img, 27, 30, 0.38, 0.5))
        peca(img.elipse(28.5, 90, 2.3, 2.3), CASCO, 0.3)
        peca(img.ret(50, 67, 54, 79), CASCO, gradiente(img, 50, 54, 0.4, 0.5))
        peca(img.ret(50, 79, 53, 88), CASCO, gradiente(img, 50, 53, 0.34, 0.5))
        peca(img.elipse(51.5, 90, 2.3, 2.3), CASCO, 0.26)
        peca(img.linha(54, 90, 58, 74, 0.5), "metal", 0.55)
        img.cor(img.ret(58, 73, 59, 75), CIANO[1])
        peca(img.ret(37, 58, 43, 63), "metal", 0.22)
        if estado == "sem_cabeca":
            peca(img.ret(36, 55, 44, 59), CASCO, 0.2)
            for x, cor in ((37, AMBAR[1]), (39, CIANO[1]), (41, RAMPAS["ferrugem"][4]), (43, AMBAR[0])):
                img.cor(img.caminho([(x, 55), (x + (1 if x % 2 else -1), 51), (x + (3 if x % 2 else -3), 49)], 0.45), cor)
            silhueta |= desenhar_cabeca(img, silhueta, 46, 92, largura=14, altura=11, tom=0.4)
        else:
            silhueta |= desenhar_cabeca(img, silhueta, 30, 46)
            peca(img.ret(36, 43, 44, 46), CASCO, 0.42)
            peca(img.ret(38, 41, 42, 43), CASCO, 0.58)
        if not limpo:
            poeira = kit.ruido_ciclico(img.w, img.h, 8, 3, 91)
            topo = silhueta & ~np.roll(silhueta, 1, axis=0)
            img.pintar(topo & (poeira > 0.35), "areia", 0.4 + 0.3 * img.fino)
            for x, y0, y1 in ((30, 69, 76), (50, 69, 75), (40, 63, 66), (33, 82, 94)):
                img.pintar(img.ret(x, y0, x + 1, y1) & silhueta, "ferrugem", 0.5, achatar=False)
    if estado != "limpo":
        cabo = img.caminho([(21, NICHO_Y0 + 4), (20.5, 50), (21.5, 64), (20.5, 72), (21, 78)], 0.7)
        img.pintar(cabo & fundo, "metal", 0.85, achatar=False)
        img.pintar(img.ret(20, 78, 23, 83), "metal", 0.7)
        img.pintar(img.ret(20, 78, 23, 79), "metal", 0.95)
        img.cor(img.ret(20, 83, 21, 85), rgba(AMBAR[1], 255))
        img.cor(img.ret(22, 83, 23, 85), rgba(AMBAR[1], 255))
        silhueta |= img.ret(20, 78, 23, 85)
    else:
        img.pintar(img.ret(38, NICHO_Y0 + 6, 42, 38), "metal", 0.6)
        img.pintar(img.ret(39, 38, 41, 44), "metal", 0.8)
    borda = dilatar(silhueta) & ~silhueta & fundo
    img.cor(borda, CONTORNO)
    return img


def doca_professor_luz(estado="padrao"):
    """O único sinal de vida: o indicador da doca na plataforma. Âmbar nas
    docas sem carga; ciano e firme na doca nova em folha da 205."""
    luz = Imagem(80, 112)
    cor = CIANO if estado == "limpo" else AMBAR
    luz.cor(luz.ret(34, 105, 46, 108), rgba(cor[1], 70))
    luz.cor(luz.ret(36, 106, 44, 107), rgba(cor[2], 255))
    luz.cor(luz.ret(39, 106, 41, 107), rgba(cor[3], 255))
    return luz


def professor_caido():
    """O professor robô desligado, deitado de costas no chão: a cabeça com a
    tela para cima e trincada, o torso com a lente do peito, a saia afunilada
    e a base flutuante de pé na ponta, um braço jogado para fora. Pé em
    (32, 27); a pegada é baixa, só o corpo."""
    img = Imagem(64, 28)
    X, Y = img.X, img.Y
    img.pintar(img.elipse(58, 17, 3.2, 8.5), CASCO, 0.28)
    img.pintar(img.elipse(58, 17, 1.6, 6), CASCO, 0.12)
    saia = img.poligono([(40, 11), (56, 8), (56, 24), (40, 22)])
    img.pintar(saia, CASCO, 0.58 - 0.4 * (Y - 8) / 16.0)
    img.pintar(img.ret(40, 11, 56, 12) & saia, CASCO, 0.82)
    torso = img.ret(20, 9, 41, 23)
    img.pintar(torso, CASCO, 0.62 - 0.42 * (Y - 9) / 14.0)
    chanfrar(img, 20, 9, 41, 23)
    img.pintar(img.ret(20, 9, 41, 10), CASCO, 0.9)
    img.pintar(img.ret(24, 11, 36, 14), VIDRO, 0.3)
    img.pintar(img.elipse(30, 12.5, 3.5, 1.4), CASCO, 0.3)
    img.cor(img.ret(30, 12, 31, 13), CIANO[0])
    head = img.ret(3, 8, 19, 23)
    img.pintar(head, CASCO, 0.62 - 0.42 * (Y - 8) / 15.0)
    chanfrar(img, 3, 8, 19, 23)
    img.pintar(img.ret(3, 8, 19, 9), CASCO, 0.9)
    tela = img.ret(5, 10, 17, 15)
    img.pintar(tela, VIDRO, 0.25 + 0.25 * ((X * 2 + Y) % 23 < 4))
    img.cor(img.ret(7, 12, 9, 13), CIANO[0])
    img.cor(img.ret(13, 12, 15, 13), CIANO[0])
    img.pintar(img.caminho([(15, 10), (12, 12), (14, 14)], 0.45) & tela, CASCO, 0.78, achatar=False)
    img.pintar(img.ret(1, 13, 3, 19), "metal", 0.3)
    img.pintar(img.ret(8, 5, 14, 8), CASCO, 0.4)
    braco = img.ret(22, 22, 46, 26)
    img.pintar(braco, CASCO, 0.36 + 0.1 * (1 - (Y - 22) / 4.0))
    img.pintar(img.elipse(48, 24, 2.6, 2.2), CASCO, 0.3)
    img.pintar(img.ret(26, 21, 29, 23), "ferrugem", 0.55, achatar=False)
    img.pintar(img.ret(46, 14, 47, 22) & saia, "ferrugem", 0.5, achatar=False)
    poeira = kit.ruido_ciclico(64, 28, 8, 4, 350)
    topo = img.opaco() & ~np.roll(img.opaco(), 1, axis=0)
    img.pintar(topo & (poeira > 0.4), "areia", 0.45)
    img.contornar()
    return img


def professor_desmontado():
    """As peças do professor espalhadas pelo chão, como o robô desmontado da
    105, mas claras: a cabeça com a tela quebrada, o torso aberto com os fios
    de fora, um braço e a base. Sem colisão. Pé em (32, 14)."""
    img = Imagem(64, 16)
    X, Y = img.X, img.Y
    img.pintar(img.elipse(54, 13, 8.5, 2.6), CASCO, 0.24)
    img.pintar(img.elipse(54, 12.4, 6.5, 1.6), CASCO, 0.38)
    torso = img.ret(19, 3, 38, 14)
    img.pintar(torso, CASCO, 0.5 - 0.2 * (Y - 3) / 11.0)
    chanfrar(img, 19, 3, 38, 14)
    img.pintar(img.ret(19, 3, 38, 4), CASCO, 0.85)
    img.pintar(img.ret(21, 5, 36, 12), VIDRO, 0.02)
    for fim, cor in (((24, 5), AMBAR[1]), ((29, 4), CIANO[1]), ((33, 5), RAMPAS["ferrugem"][4])):
        img.cor(img.caminho([(fim[0], 10), (fim[0] + 2, 8), (fim[0] + 1, 6), fim], 0.45), cor)
    img.pintar(img.ret(40, 9, 53, 12), CASCO, 0.42)
    img.pintar(img.ret(40, 9, 53, 10), CASCO, 0.75)
    img.pintar(img.elipse(54, 10.5, 2.2, 2.2), CASCO, 0.3)
    head = img.ret(2, 5, 17, 15)
    img.pintar(head, CASCO, 0.58 - 0.3 * (Y - 5) / 10.0)
    chanfrar(img, 2, 5, 17, 15)
    img.pintar(img.ret(2, 5, 17, 6), CASCO, 0.9)
    tela = img.ret(4, 7, 15, 12)
    img.pintar(tela, VIDRO, 0.2)
    for fim in ((15, 7), (4, 8), (10, 12)):
        img.pintar(img.caminho([(9.5, 9.5), fim], 0.45) & tela, CASCO, 0.8, achatar=False)
    img.cor(img.ret(0, 8, 2, 12), RAMPAS["metal"][3])
    for x, y in ((20, 15), (38, 14), (60, 7), (17, 1)):
        img.cor(img.ret(x, y, x + 1, y + 1), RAMPAS["metal"][5])
    poeira = kit.ruido_ciclico(64, 16, 8, 4, 351)
    topo = img.opaco() & ~np.roll(img.opaco(), 1, axis=0)
    img.pintar(topo & (poeira > 0.4), "areia", 0.45)
    img.contornar()
    return img


# ---------------------------------------------------------------------------
# Saída
# ---------------------------------------------------------------------------


def main():
    print("Gerando o visual futurista das salas de aula do Bloco de salas")
    os.makedirs(PASTA_OBJETOS, exist_ok=True)
    os.makedirs(PASTA_PAREDES, exist_ok=True)
    objetos, paredes = [], []
    for nome, acabamento in (("cadeira_vr", "ciano"), ("cadeira_vr_ambar", "ambar"), ("cadeira_vr_limpa", "limpa")):
        corpo, lente = cadeira_vr(acabamento)
        corpo.salvar(f"{nome}.png", PASTA_OBJETOS)
        if acabamento != "limpa":
            lente.salvar(f"{nome}_lente.png", PASTA_OBJETOS)
        objetos.append((corpo, lente))
    caida = cadeira_vr_caida()
    caida.salvar("cadeira_vr_caida.png", PASTA_OBJETOS)
    objetos.append((caida, None))
    rack, rack_lente = rack_oculos()
    rack.salvar("estante_oculos_vr.png", PASTA_OBJETOS)
    rack_lente.salvar("estante_oculos_vr_lente.png", PASTA_OBJETOS)
    rack_musgo, _ = rack_oculos(musgo=True)
    rack_musgo.salvar("estante_oculos_vr_musgo.png", PASTA_OBJETOS)
    objetos += [(rack, rack_lente), (rack_musgo, rack_lente)]
    for nome, f in (("professor_caido", professor_caido), ("professor_desmontado", professor_desmontado),
                    ("oculos_no_chao", oculos_no_chao)):
        img = f()
        img.salvar(f"{nome}.png", PASTA_OBJETOS)
        objetos.append((img, None))
    for nome, parametros in LOUSAS.items():
        corpo, luz = lousa_corpo(**parametros), lousa_luz(**parametros)
        corpo.salvar(f"{nome}.png", PASTA_PAREDES)
        luz.salvar(f"{nome}_luz.png", PASTA_PAREDES)
        paredes.append((corpo, luz))
    for sufixo, estado in (("", "padrao"), ("_limpo", "limpo"), ("_sem_cabeca", "sem_cabeca"), ("_vazia", "vazia")):
        corpo, luz = doca_professor(estado), doca_professor_luz(estado)
        corpo.salvar(f"parede_doca_professor{sufixo}.png", PASTA_PAREDES)
        luz.salvar(f"parede_doca_professor{sufixo}_luz.png", PASTA_PAREDES)
        paredes.append((corpo, luz))
    corpo, luz = parede_oculos()
    corpo.salvar("parede_oculos_vr.png", PASTA_PAREDES)
    luz.salvar("parede_oculos_vr_luz.png", PASTA_PAREDES)
    paredes.append((corpo, luz))
    if PREVIA:
        colunas = 6
        linhas = (len(paredes) + colunas - 1) // colunas
        largura = colunas * 82
        folha = Imagem(largura, linhas * 114 + 100)
        folha.px[:, :] = [26, 28, 36, 255]
        for i, (corpo, luz) in enumerate(paredes):
            x, y = (i % colunas) * 82, (i // colunas) * 114
            folha.colar(corpo, x, y)
            sobrepor(folha, luz, x, y)
        y = linhas * 114 + 4
        x = 2
        for corpo, lente in objetos:
            if x + corpo.w > largura:
                x, y = 2, y + 40
            folha.colar(corpo, x, y)
            if lente is not None:
                sobrepor(folha, lente, x, y)
            x += corpo.w + 4
        os.makedirs(PREVIA, exist_ok=True)
        bib.salvar_png(os.path.join(PREVIA, "previa_salas_futuristas.png"), folha.px)


if __name__ == "__main__":
    main()
