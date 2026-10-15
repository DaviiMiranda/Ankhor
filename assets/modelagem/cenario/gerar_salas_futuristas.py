# gerar_salas_futuristas.py — desenha, por código, o visual FUTURISTA das salas
# de aula do Bloco de salas: a cadeira com óculos de realidade virtual no lugar
# da carteira, a lousa holográfica (que mantém os tracinhos do puzzle) e o
# professor robô desligado na doca de recarga.
#
# Piloto: sala 101. O resto do bloco segue o mesmo kit depois.
#
# Como rodar (Python 3 + numpy):
#
#   python assets/modelagem/cenario/gerar_salas_futuristas.py
#
# O que sai (em assets/sprites/cenario/):
#   objetos/cadeira_vr.png               24 x 30  cadeira com os óculos no assento
#   objetos/cadeira_vr_lente.png         24 x 30  só a lente (camada de luz, sem sombreamento)
#   objetos/cadeira_vr_caida.png         30 x 16  a mesma cadeira tombada, óculos no chão
#   paredes/parede_lousa_holo_7.png      80 x 112 o painel apagado, preso na parede
#   paredes/parede_lousa_holo_7_luz.png  80 x 112 o que ainda acende nele (sem sombreamento)
#   paredes/parede_doca_professor.png    80 x 112 o nicho da doca e o professor desligado
#   paredes/parede_doca_professor_luz.png 80 x 112 o indicador âmbar da doca (sem sombreamento)
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


# ---------------------------------------------------------------------------
# Cadeira com óculos VR
# ---------------------------------------------------------------------------


def cadeira_vr():
    """Cadeira de sala de aula de 3026, vista de lado, virada para a direita
    como a carteira antiga: pedestal único com disco no chão, assento e
    encosto de casco moldado, e os óculos de realidade virtual deixados no
    assento, com a tira de cabeça em laço. A lente (camada de luz) sai à
    parte. Pé em (11, 29): mesma pegada da carteira."""
    img = Imagem(24, 30)
    lente = Imagem(24, 30)
    # disco do pé e pedestal
    img.pintar(img.elipse(11, 28, 8, 2), CASCO, 0.28)
    img.pintar(img.ret(10, 21, 13, 27), CASCO, gradiente(img, 10, 13, 0.4, 0.5))
    img.pintar(img.ret(9, 24, 14, 25), "metal", 0.45)
    # assento: casco moldado com a borda da frente mais clara
    assento = img.poligono([(3, 18), (19, 17), (20, 19), (18, 21), (4, 21)])
    img.pintar(assento, CASCO, gradiente(img, 3, 20, 0.5, 0.35))
    img.pintar(img.ret(5, 17, 19, 18) & assento, CASCO, 0.78)
    img.cor(img.ret(6, 20, 17, 21), rgba(CIANO[0], 255))
    # encosto: painel curvo que sobe para trás, com a almofada escura por dentro
    encosto = img.poligono([(2, 19), (1, 7), (3, 3), (7, 3), (7, 19)])
    img.pintar(encosto, CASCO, gradiente(img, 1, 7, 0.45, 0.4))
    img.pintar(img.ret(4, 5, 7, 18) & encosto, VIDRO, 0.45)
    img.pintar(img.ret(3, 3, 7, 4), CASCO, 0.8)
    # óculos: caixa com espuma, placa frontal e a lente escura
    img.pintar(img.ret(9, 11, 17, 17), "metal", 0.28)
    img.pintar(img.ret(9, 11, 17, 12), "metal", 0.7)
    img.pintar(img.ret(8, 12, 9, 16), "tecido", 0.35)
    img.pintar(img.ret(17, 12, 19, 16), CASCO, 0.62)
    img.pintar(img.ret(17, 13, 19, 15), VIDRO, 0.25)
    # tira da cabeça: um laço fino que sai do aro e dá a volta por trás
    laco = img.elipse(8.5, 10.5, 4.5, 5) & ~img.elipse(8.5, 10.5, 3.2, 3.8)
    img.pintar(laco & (img.Y < 15), "metal", 0.22)
    lente.cor(lente.ret(17, 13, 19, 15), rgba(CIANO[3], 255))
    lente.cor(lente.ret(17, 13, 18, 14), rgba(CIANO[4], 255))
    bib.musgo_por_cima(img, 0.08, 160)
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
    bib.musgo_por_cima(img, 0.25, 161)
    img.contornar()
    return img


# ---------------------------------------------------------------------------
# Lousa holográfica
# ---------------------------------------------------------------------------

LOUSA_X0, LOUSA_X1, LOUSA_Y0, LOUSA_Y1 = 6, 74, 26, 70
VIDRO_X0, VIDRO_X1, VIDRO_Y0, VIDRO_Y1 = 8, 72, 28, 68


def lousa_holografica_corpo():
    """O painel de ensino que substituiu o quadro-negro: moldura de metal
    escuro, vidro apagado com reflexos, um canto de pixels mortos, uma
    trinca fina e a barra do emissor embaixo. Mesmo lugar da lousa antiga
    (a parede_lousa), então os tracinhos continuam onde o jogador procura."""
    img = kit.parede_base()
    X, Y = img.X, img.Y
    img.pintar(img.ret(LOUSA_X0, LOUSA_Y0, LOUSA_X1, LOUSA_Y1), "metal", 0.28 + 0.1 * img.fino)
    img.pintar(img.ret(LOUSA_X0, LOUSA_Y0, LOUSA_X1, LOUSA_Y0 + 1), "metal", 0.62)
    vidro = img.ret(VIDRO_X0, VIDRO_Y0, VIDRO_X1, VIDRO_Y1)
    reflexo = kit.ruido_ciclico(img.w, img.h, 20, 12, 90)
    img.pintar(vidro, VIDRO, 0.18 + 0.4 * reflexo)
    faixa = vidro & (((X * 2 + Y * 3) % 47) < 4)
    img.pintar(faixa, VIDRO, 0.85, achatar=False)
    mortos = img.ret(VIDRO_X1 - 17, VIDRO_Y0, VIDRO_X1, VIDRO_Y0 + 10)
    img.cor(mortos, VIDRO[0])
    img.pintar(mortos & (((X + Y) % 4) == 0), VIDRO, 0.5, achatar=False)
    trinca = img.caminho([(24, VIDRO_Y1), (27, 58), (25, 52), (30, 45), (29, 40)], 0.45) & vidro
    img.pintar(trinca, VIDRO, 1.0, achatar=False)
    img.pintar(img.ret(LOUSA_X0 + 14, LOUSA_Y1, LOUSA_X1 - 14, LOUSA_Y1 + 2), "metal", 0.4)
    img.pintar(img.ret(LOUSA_X0 + 14, LOUSA_Y1, LOUSA_X1 - 14, LOUSA_Y1 + 1), "metal", 0.7)
    for x in (LOUSA_X0 + 18, LOUSA_X1 - 20):
        img.cor(img.ret(x, LOUSA_Y1 + 1, x + 2, LOUSA_Y1 + 2), rgba(AMBAR[0], 255))
    img.pintar(img.ret(LOUSA_X0 - 1, LOUSA_Y0 + 6, LOUSA_X0, LOUSA_Y0 + 14), "metal", 0.15)
    img.pintar(img.ret(LOUSA_X1, LOUSA_Y0 + 6, LOUSA_X1 + 1, LOUSA_Y0 + 14), "metal", 0.15)
    return img


def varredura(img, fator=0.45):
    """Uma fileira em cada três perde alfa: a textura de projeção."""
    for y in range(img.h):
        if y % 3 == 2:
            img.px[y, :, 3] = (img.px[y, :, 3] * fator).astype(np.uint8)


def falha(img, y0, y1, desloca):
    """Desloca uma faixa de fileiras para o lado (quadro fora de sincronia),
    só dentro do vidro: a borda do painel não sai da moldura."""
    faixa = img.px[y0:y1, VIDRO_X0:VIDRO_X1].copy()
    img.px[y0:y1, VIDRO_X0:VIDRO_X1] = np.roll(faixa, desloca, axis=1)


def lousa_holografica_luz(tracinhos=7):
    """O que o painel ainda mostra: um véu ciano quase invisível, o resto
    apagado da conta (traços curtos, uma raiz, uma fração), uma faixa de
    falha, o aviso âmbar de 'sem sinal' e, embaixo, os TRACINHOS contados em
    grupos de cinco (quatro em pé e um cortando), na mesma geometria da
    lousa de giz: grupos de 12 px, riscos a cada 2 px."""
    luz = Imagem(80, 112)
    vidro = luz.ret(VIDRO_X0, VIDRO_Y0, VIDRO_X1, VIDRO_Y1)
    luz.cor(vidro, rgba(CIANO[1], 22))
    luz.cor(luz.ret(VIDRO_X0, VIDRO_Y0, VIDRO_X1, VIDRO_Y0 + 1), rgba(CIANO[2], 110))
    luz.cor(luz.ret(VIDRO_X0, VIDRO_Y1 - 1, VIDRO_X1, VIDRO_Y1), rgba(CIANO[2], 110))
    luz.cor(luz.ret(VIDRO_X0, VIDRO_Y0, VIDRO_X0 + 1, VIDRO_Y1), rgba(CIANO[2], 110))
    luz.cor(luz.ret(VIDRO_X1 - 1, VIDRO_Y0, VIDRO_X1, VIDRO_Y1), rgba(CIANO[2], 110))
    conta = luz.ret(0, 0, 0, 0)
    for y, x0, x1 in ((34, 14, 36), (39, 14, 30), (44, 18, 44)):
        conta |= luz.ret(x0, y, x1, y + 1)
    conta |= luz.caminho([(40, 34), (42, 37), (44, 33), (50, 33)], 0.5)
    conta |= luz.ret(14, 49, 28, 50) | luz.ret(18, 46, 19, 49) | luz.ret(22, 51, 24, 52)
    luz.cor(conta & vidro, rgba(CIANO[3], 120))
    luz.cor(luz.ret(VIDRO_X0 + 3, VIDRO_Y0 + 3, VIDRO_X0 + 13, VIDRO_Y0 + 5), rgba(AMBAR[2], 235))
    varredura(luz)
    falha(luz, 40, 43, 3)
    tinta = luz.ret(0, 0, 0, 0)
    for g in range((tracinhos + 4) // 5):
        gx, gy = VIDRO_X0 + 6 + g * 12, VIDRO_Y1 - 12
        no_grupo = min(5, tracinhos - 5 * g)
        for k in range(min(4, no_grupo)):
            tinta |= luz.ret(gx + 2 * k, gy, gx + 2 * k + 1, gy + 7)
        if no_grupo == 5:
            tinta |= luz.linha(gx - 1, gy + 5, gx + 8, gy + 1, 0.45)
    luz.cor(tinta, rgba(CIANO[4], 255))
    return luz


# ---------------------------------------------------------------------------
# O professor robô na doca
# ---------------------------------------------------------------------------

NICHO_X0, NICHO_X1, NICHO_Y0, NICHO_Y1 = 18, 62, 34, 108


def doca_professor():
    """O nicho da doca de recarga com o professor desligado. O robô é de
    propósito o oposto dos robôs inimigos: baixo (uns 58 px, pouco mais que o
    Gabriel), redondo, claro, com a cabeça de tela e uma base flutuante em
    vez de pernas, para ninguém confundir um com o outro. A tela do rosto
    está escura (dois olhos fantasma, quase invisíveis, e a linha da boca);
    um cabo da doca pende solto do teto e termina num plugue no ar; a poeira
    e as manchas de ferrugem dizem há quanto tempo ele está parado."""
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

    # base flutuante: disco com o anel de contato apagado
    peca(img.elipse(40, 101, 11.5, 3.6), CASCO, 0.32)
    peca(img.ret(29, 101, 51, 104) & img.elipse(40, 102, 11.5, 3.2), CASCO, 0.14)
    anel = img.elipse(40, 101, 9.5, 2.7) & ~img.elipse(40, 101, 7.5, 1.7)
    img.cor(anel, CIANO[0])
    # saia (a parte de baixo do corpo) e torso arredondado
    peca(img.poligono([(33, 79), (47, 79), (50, 99), (30, 99)]), CASCO, gradiente(img, 30, 50, 0.46, 0.4))
    peca(img.ret(31, 62, 49, 80), CASCO, gradiente(img, 31, 49, 0.55, 0.45))
    chanfrar(img, 31, 62, 49, 80)
    img.pintar(img.ret(31, 62, 49, 63), CASCO, 0.85)
    img.pintar(img.ret(32, 77, 48, 79), CASCO, 0.22)
    # painel do peito com a lente do projetor de aula (apagada)
    img.pintar(img.ret(34, 66, 46, 76), VIDRO, 0.32)
    img.pintar(img.elipse(40, 71, 3.4, 3.4), CASCO, 0.28)
    img.pintar(img.elipse(40, 71, 2.2, 2.2), VIDRO, 0.12)
    img.cor(img.ret(39, 70, 40, 71), CIANO[0])
    # ombros e braços: o direito segura o ponteiro
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
    # pescoço, cabeça com orelhas e o cristal do projetor no topo
    peca(img.ret(37, 58, 43, 63), "metal", 0.22)
    peca(img.ret(30, 46, 50, 60), CASCO, gradiente(img, 30, 50, 0.58, 0.5))
    chanfrar(img, 30, 46, 50, 60)
    img.pintar(img.ret(30, 46, 50, 47), CASCO, 0.9)
    peca(img.ret(28, 50, 30, 57), "metal", 0.3)
    peca(img.ret(50, 50, 52, 57), "metal", 0.22)
    peca(img.ret(36, 43, 44, 46), CASCO, 0.42)
    peca(img.ret(38, 41, 42, 43), CASCO, 0.58)
    # tela do rosto: vidro escuro, brilho em diagonal, olhos fantasma e boca
    tela = img.ret(32, 48, 48, 58)
    img.pintar(tela, VIDRO, 0.22 + 0.25 * ((X * 2 + Y) % 23 < 4))
    img.pintar(tela & (((X + Y * 2) % 29) < 3) & (Y < 54), VIDRO, 0.9, achatar=False)
    img.cor(img.ret(35, 51, 38, 53), CIANO[0])
    img.cor(img.ret(42, 51, 45, 53), CIANO[0])
    img.cor(img.ret(37, 55, 43, 56), CIANO[0])
    img.pintar(img.caminho([(44, 48), (42, 51), (43, 54), (40, 58)], 0.45) & tela, CASCO, 0.78, achatar=False)
    # o tempo: poeira em cima das superfícies e ferrugem escorrendo das juntas
    poeira = kit.ruido_ciclico(img.w, img.h, 8, 3, 91)
    topo = silhueta & ~np.roll(silhueta, 1, axis=0)
    img.pintar(topo & (poeira > 0.35), "areia", 0.4 + 0.3 * img.fino)
    for x, y0, y1 in ((30, 69, 76), (50, 69, 75), (40, 63, 66), (33, 82, 94)):
        img.pintar(img.ret(x, y0, x + 1, y1) & silhueta, "ferrugem", 0.5, achatar=False)
    # cabo da doca que pende do teto do nicho, com o plugue solto no ar
    cabo = img.caminho([(21, NICHO_Y0 + 4), (20.5, 50), (21.5, 64), (20.5, 72), (21, 78)], 0.7)
    img.pintar(cabo & fundo, "metal", 0.85, achatar=False)
    img.pintar(img.ret(20, 78, 23, 83), "metal", 0.7)
    img.pintar(img.ret(20, 78, 23, 79), "metal", 0.95)
    img.cor(img.ret(20, 83, 21, 85), rgba(AMBAR[1], 255))
    img.cor(img.ret(22, 83, 23, 85), rgba(AMBAR[1], 255))
    silhueta |= img.ret(20, 78, 23, 85)
    # contorno escuro do robô contra o fundo do nicho
    borda = dilatar(silhueta) & ~silhueta & fundo
    img.cor(borda, CONTORNO)
    return img


def doca_professor_luz():
    """O único sinal de vida: o indicador da doca, âmbar, na plataforma.
    Sem carga."""
    luz = Imagem(80, 112)
    luz.cor(luz.ret(34, 105, 46, 108), rgba(AMBAR[1], 70))
    luz.cor(luz.ret(36, 106, 44, 107), rgba(AMBAR[2], 255))
    luz.cor(luz.ret(39, 106, 41, 107), rgba(AMBAR[3], 255))
    return luz


# ---------------------------------------------------------------------------
# Saída
# ---------------------------------------------------------------------------


def sobrepor(fundo, camada, x, y):
    """Compõe a camada de luz sobre o fundo respeitando o alfa, como o Godot
    faz com o material sem luz: cor = fundo * (1 - a) + camada * a."""
    a = camada.px[..., 3:4].astype(float) / 255.0
    area = fundo.px[y:y + camada.h, x:x + camada.w]
    area[..., :3] = (area[..., :3] * (1 - a) + camada.px[..., :3] * a).astype(np.uint8)


def main():
    print("Gerando o visual futurista das salas de aula (piloto: sala 101)")
    os.makedirs(PASTA_OBJETOS, exist_ok=True)
    os.makedirs(PASTA_PAREDES, exist_ok=True)
    cadeira, lente = cadeira_vr()
    caida = cadeira_vr_caida()
    lousa, lousa_luz = lousa_holografica_corpo(), lousa_holografica_luz(7)
    doca, doca_luz = doca_professor(), doca_professor_luz()
    cadeira.salvar("cadeira_vr.png", PASTA_OBJETOS)
    lente.salvar("cadeira_vr_lente.png", PASTA_OBJETOS)
    caida.salvar("cadeira_vr_caida.png", PASTA_OBJETOS)
    lousa.salvar("parede_lousa_holo_7.png", PASTA_PAREDES)
    lousa_luz.salvar("parede_lousa_holo_7_luz.png", PASTA_PAREDES)
    doca.salvar("parede_doca_professor.png", PASTA_PAREDES)
    doca_luz.salvar("parede_doca_professor_luz.png", PASTA_PAREDES)
    if PREVIA:
        folha = Imagem(80 * 2 + 3 * 24 + 40, 118)
        folha.px[:, :] = [26, 28, 36, 255]
        for i, (corpo, luz) in enumerate(((lousa, lousa_luz), (doca, doca_luz))):
            folha.colar(corpo, i * 80, 0)
            sobrepor(folha, luz, i * 80, 0)
        x = 80 * 2 + 6
        folha.colar(cadeira, x, 4)
        sobrepor(folha, lente, x, 4)
        folha.colar(caida, x + 28, 18)
        os.makedirs(PREVIA, exist_ok=True)
        bib.salvar_png(os.path.join(PREVIA, "previa_salas_futuristas.png"), folha.px)


if __name__ == "__main__":
    main()
