# gerar_biblioteca_moderna.py — desenha, por código, o visual FUTURISTA da
# Biblioteca (Fase 1): racks de arquivo no lugar das estantes, mesas
# holográficas, cabines de vidro ciano, torres de equipamentos, o gerador e o
# painel da manutenção, paredes de servidores e de conduítes, o robô
# bibliotecário desligado e o fundo pintado do salão e da ala leste.
#
# Como rodar (Python 3 + numpy):
#
#   python assets/modelagem/cenario/gerar_biblioteca_moderna.py
#
# O que sai (em assets/sprites/):
#   cenario/objetos/rack_arquivo.png, rack_arquivo_musgo.png   68 x 90  (a mesma medida da estante vazia)
#   cenario/objetos/mesa_holografica.png                       116 x 42 (a mesma da mesa de leitura)
#   cenario/objetos/cabine_vidro_ciano.png                     80 x 68  (a mesma da cabine)
#   cenario/objetos/torre_equipamentos.png                     30 x 62
#   cenario/objetos/gerador.png                                48 x 40
#   cenario/objetos/painel_distribuicao.png                    38 x 48
#   cenario/paredes/parede_servidores.png                      80 x 112
#   cenario/paredes/parede_conduites.png                       80 x 112
#   cenario/paredes/parede_painel_ciano.png                    80 x 112
#   cenario/paredes/parede_doca_bibliotecario.png              80 x 112
#   salas/biblioteca/biblioteca_fundo_moderna.png              1440 x 180
# Cada peça com função tem uma segunda imagem, <nome>_luz.png, do mesmo
# tamanho, com só o que brilha (desenhada sem sombreamento no Godot).
# Com PREVIA=<pasta>, também salva previa_biblioteca_moderna.png nela (não
# commitar).
#
# O QUE ACENDE QUANDO
# -------------------
# A camada de luz de cada peça fica num nó VisivelComMarca. Antes de o
# Gabriel religar os disjuntores (marca "energia"), a peça aparece apagada:
# só o corpo escuro. Quando a energia volta, a camada acende, com as mesmas
# piscadas das luzes de emergência. A cabine fica sempre acesa (marca vazia),
# como no vídeo da abertura.
#
# O ARQUIVO ANTIGO FICA
# ---------------------
# gerar_biblioteca.py é importado pelo gerar_kit.py (o kit de todas as
# fases). Por isso este script NÃO o altera: ele chama o desenhar_fundo()
# original e pinta por cima. O biblioteca_fundo.png antigo continua no
# projeto, caso se queira voltar atrás.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")
PASTA_PAREDES = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "paredes")
PASTA_SALA = os.path.join(PASTA_PROJETO, "assets", "sprites", "salas", "biblioteca")
PREVIA = os.environ.get("PREVIA", "")

_spec = importlib.util.spec_from_file_location("gerar_salas_futuristas", os.path.join(PASTA_SCRIPT, "gerar_salas_futuristas.py"))
gsf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gsf)
kit, bib = gsf.kit, gsf.bib
Imagem, RAMPAS, CONTORNO, dilatar = gsf.Imagem, gsf.RAMPAS, gsf.CONTORNO, gsf.dilatar
CASCO, VIDRO, CIANO, AMBAR = gsf.CASCO, gsf.VIDRO, gsf.CIANO, gsf.AMBAR
rgba, gradiente, chanfrar, varredura, sobrepor = gsf.rgba, gsf.gradiente, gsf.chanfrar, gsf.varredura, gsf.sobrepor


def led(img, luz, x, y, aceso, cor=CIANO):
    """Um pixel de LED: apagado no corpo (azul-petróleo escuro) ou aceso na
    camada de luz."""
    if aceso:
        luz.cor(luz.ret(x, y, x + 1, y + 1), rgba(cor[3], 255))
    else:
        img.cor(img.ret(x, y, x + 1, y + 1), CIANO[0])


# ---------------------------------------------------------------------------
# Objetos
# ---------------------------------------------------------------------------


def rack_arquivo(musgo=False, semente=0):
    """Armário de arquivo digital, no lugar da estante vazia: quatro módulos
    com ventilação e três baias de disco cada, LEDs por baia. Pé em (34, 89),
    como o da estante vazia, então troca sem mexer na navegação."""
    rng = np.random.default_rng(400 + semente)
    img, luz = Imagem(68, 90), Imagem(68, 90)
    img.pintar(img.ret(1, 2, 67, 88), CASCO, gradiente(img, 1, 67, 0.4, 0.34) + 0.05 * (1 - img.Y / 88.0))
    chanfrar(img, 1, 2, 67, 88)
    img.pintar(img.ret(1, 2, 67, 3), CASCO, 0.85)
    for k in range(4):
        y0 = 6 + k * 20
        img.pintar(img.ret(5, y0, 63, y0 + 17), VIDRO, 0.1)
        img.pintar(img.ret(5, y0, 63, y0 + 1), VIDRO, 0.0)
        for j in range(4):
            img.cor(img.ret(8, y0 + 3 + 3 * j, 38, y0 + 4 + 3 * j), VIDRO[0])
        for b in range(3):
            bx = 42 + b * 7
            img.pintar(img.ret(bx, y0 + 3, bx + 5, y0 + 14), CASCO, 0.3)
            img.cor(img.ret(bx + 1, y0 + 4, bx + 4, y0 + 5), VIDRO[0])
            cor = AMBAR if rng.random() < 0.12 else CIANO
            led(img, luz, bx + 2, y0 + 11, rng.random() < 0.55, cor)
        img.pintar(img.ret(5, y0 + 17, 63, y0 + 19), "metal", 0.4)
    img.pintar(img.ret(3, 84, 65, 88), "metal", 0.22)
    img.pintar(img.ret(2, 88, 10, 90), "metal", 0.15)
    img.pintar(img.ret(58, 88, 66, 90), "metal", 0.15)
    if musgo:
        bib.musgo_por_cima(img, 0.45, 411 + semente)
        for x in (12, 33, 55):
            img.pintar(img.caminho([(x, 4), (x + 1, 18), (x - 1, 30)], 0.5) & img.ret(1, 4, 67, 86), "verde", 0.5, achatar=False)
    img.contornar()
    return img, luz


def mesa_holografica():
    """Mesa de leitura com o tampo de vidro e dois emissores que projetam
    telas de dados. Pé em (49, 40), a mesma da mesa de leitura de madeira."""
    img, luz = Imagem(116, 42), Imagem(116, 42)
    img.pintar(img.ret(10, 26, 14, 40), "metal", 0.28)
    img.pintar(img.ret(82, 26, 86, 40), "metal", 0.22)
    img.pintar(img.ret(10, 34, 86, 36), "metal", 0.2)
    img.pintar(img.ret(4, 24, 92, 29), CASCO, gradiente(img, 4, 92, 0.45, 0.35))
    img.pintar(img.ret(4, 24, 92, 25), CASCO, 0.85)
    img.pintar(img.ret(5, 19, 91, 24), VIDRO, 0.22)
    img.pintar(img.ret(5, 19, 91, 20), VIDRO, 0.5)
    luz.cor(luz.ret(7, 21, 89, 23), rgba(CIANO[1], 90))
    for cx in (28, 68):
        img.pintar(img.ret(cx - 4, 17, cx + 4, 20), CASCO, 0.5)
        luz.cor(luz.ret(cx - 2, 17, cx + 2, 18), rgba(CIANO[3], 255))
        luz.cor(luz.ret(cx - 8, 6, cx + 8, 16), rgba(CIANO[1], 40))
        borda = luz.ret(cx - 8, 6, cx + 8, 16) & ~luz.ret(cx - 7, 7, cx + 7, 15)
        luz.cor(borda, rgba(CIANO[3], 190))
        for j in range(3):
            luz.cor(luz.ret(cx - 5, 8 + 3 * j, cx + 2 + 2 * (j % 2), 9 + 3 * j), rgba(CIANO[4], 220))
    varredura(luz)
    img.contornar()
    return img, luz


def cabine_vidro_ciano():
    """A cabine de estudo do vídeo: divisória de vidro com moldura de casco e
    friso ciano, mesa com um holograma no lugar do monitor de tubo. Pé em
    (40, 66), como a da cabine antiga."""
    img, luz = Imagem(80, 68), Imagem(80, 68)
    vidro = img.ret(7, 13, 73, 48)
    img.cor(vidro, rgba(VIDRO[3], 120))
    img.pintar(img.ret(4, 10, 8, 52), CASCO, gradiente(img, 4, 8, 0.5, 0.3))
    img.pintar(img.ret(72, 10, 76, 52), CASCO, gradiente(img, 72, 76, 0.4, 0.3))
    img.pintar(img.ret(4, 10, 76, 13), CASCO, 0.6)
    img.pintar(img.ret(4, 10, 76, 11), CASCO, 0.88)
    luz.cor(luz.ret(8, 13, 72, 14), rgba(CIANO[2], 170))
    luz.cor(luz.ret(8, 47, 72, 48), rgba(CIANO[2], 110))
    img.pintar(img.ret(8, 40, 72, 46), CASCO, gradiente(img, 8, 72, 0.5, 0.35))
    img.pintar(img.ret(8, 40, 72, 41), CASCO, 0.85)
    img.pintar(img.ret(10, 46, 14, 64), "metal", 0.28)
    img.pintar(img.ret(66, 46, 70, 64), "metal", 0.2)
    img.pintar(img.ret(30, 37, 50, 40), CASCO, 0.3)
    img.cor(img.ret(32, 38, 48, 39), VIDRO[1])
    img.pintar(img.ret(54, 34, 62, 40), "livro_azul", 0.5)
    img.pintar(img.ret(54, 32, 62, 34), "livro_vermelho", 0.5)
    img.pintar(img.ret(36, 34, 44, 37), CASCO, 0.5)
    luz.cor(luz.ret(26, 17, 54, 33), rgba(CIANO[1], 40))
    luz.cor(luz.ret(26, 17, 54, 33) & ~luz.ret(27, 18, 53, 32), rgba(CIANO[3], 190))
    for j in range(4):
        luz.cor(luz.ret(29, 20 + 3 * j, 41 + 4 * (j % 2), 21 + 3 * j), rgba(CIANO[4], 220))
    luz.cor(luz.ret(45, 20, 51, 30), rgba(CIANO[2], 150))
    luz.cor(luz.ret(39, 33, 41, 37), rgba(CIANO[1], 80))
    varredura(luz)
    img.contornar()
    return img, luz


def torre_equipamentos():
    """A torre de equipamentos entre as estantes: cinco módulos empilhados,
    com ventilação e LEDs, e um feixe de cabos que desce para o chão. Pé em
    (15, 61)."""
    rng = np.random.default_rng(420)
    img, luz = Imagem(30, 62), Imagem(30, 62)
    img.pintar(img.ret(3, 2, 27, 58), CASCO, gradiente(img, 3, 27, 0.45, 0.4))
    chanfrar(img, 3, 2, 27, 58)
    img.pintar(img.ret(3, 2, 27, 3), CASCO, 0.88)
    for k in range(5):
        y0 = 5 + k * 10
        img.pintar(img.ret(5, y0, 25, y0 + 8), VIDRO, 0.1)
        for j in range(2):
            img.cor(img.ret(7, y0 + 2 + 3 * j, 17, y0 + 3 + 3 * j), VIDRO[0])
        for b in range(3):
            led(img, luz, 19 + 2 * b, y0 + 4, rng.random() < 0.6, AMBAR if (k == 4 and b == 2) else CIANO)
    img.pintar(img.ret(5, 58, 25, 61), "metal", 0.22)
    img.pintar(img.caminho([(26, 20), (28, 40), (24, 58)], 0.7), "metal", 0.3)
    img.contornar()
    return img, luz


def gerador():
    """O gerador da manutenção: caixa de casco com a turbina em cima e tubos.
    Apagado, tem um indicador âmbar escuro; com a energia, as luzes acendem em
    ciano. Pé em (24, 39)."""
    img, luz = Imagem(48, 40), Imagem(48, 40)
    img.pintar(img.ret(3, 16, 45, 37), CASCO, gradiente(img, 3, 45, 0.45, 0.4))
    chanfrar(img, 3, 16, 45, 37)
    img.pintar(img.ret(3, 16, 45, 17), CASCO, 0.85)
    img.pintar(img.elipse(16, 12, 10, 6), CASCO, 0.42)
    img.pintar(img.ret(6, 10, 26, 16), CASCO, 0.42)
    img.pintar(img.elipse(16, 7, 8, 3), CASCO, 0.65)
    img.pintar(img.elipse(16, 7, 5, 1.8), VIDRO, 0.1)
    img.pintar(img.ret(32, 6, 36, 16), "metal", 0.35)
    img.pintar(img.ret(30, 5, 38, 7), "metal", 0.55)
    img.pintar(img.ret(8, 20, 28, 33), VIDRO, 0.1)
    for j in range(4):
        img.cor(img.ret(10, 22 + 3 * j, 26, 23 + 3 * j), VIDRO[0])
    img.pintar(img.ret(32, 21, 42, 33), CASCO, 0.3)
    for j in range(3):
        img.cor(img.ret(34, 23 + 3 * j, 40, 24 + 3 * j), VIDRO[1])
        led(img, luz, 41, 23 + 3 * j, True, CIANO if j else AMBAR)
    luz.cor(luz.ret(14, 6, 19, 8), rgba(CIANO[3], 220))
    img.pintar(img.ret(2, 37, 46, 40), "metal", 0.18)
    img.contornar()
    return img, luz


def painel_distribuicao():
    """Armário de distribuição de energia: porta com fileiras de disjuntores e
    LEDs de linha. Pé em (19, 47)."""
    rng = np.random.default_rng(421)
    img, luz = Imagem(38, 48), Imagem(38, 48)
    img.pintar(img.ret(2, 2, 36, 46), CASCO, gradiente(img, 2, 36, 0.45, 0.4))
    chanfrar(img, 2, 2, 36, 46)
    img.pintar(img.ret(2, 2, 36, 3), CASCO, 0.88)
    img.pintar(img.ret(5, 5, 33, 43), VIDRO, 0.12)
    for fileira in range(4):
        y = 8 + fileira * 9
        for k in range(5):
            x = 8 + k * 5
            img.pintar(img.ret(x, y, x + 3, y + 6), CASCO, 0.35)
            img.cor(img.ret(x + 1, y + 1, x + 2, y + 3), VIDRO[0])
            led(img, luz, x + 1, y + 4, rng.random() < 0.7, AMBAR if (fileira == 3 and k == 4) else CIANO)
    img.pintar(img.ret(2, 46, 36, 48), "metal", 0.18)
    img.contornar()
    return img, luz


# ---------------------------------------------------------------------------
# Paredes (80 x 112)
# ---------------------------------------------------------------------------


def parede_servidores():
    """Um vão de parede com servidores: duas colunas de seis módulos, cada um
    com ventilação e LEDs, no lugar da estante de madeira."""
    rng = np.random.default_rng(430)
    img, luz = kit.parede_base(), Imagem(80, 112)
    img.pintar(img.ret(6, 12, 74, 104), "metal", 0.26 + 0.08 * img.fino)
    img.pintar(img.ret(8, 14, 72, 102), VIDRO, 0.08)
    for coluna in range(2):
        x0 = 10 + coluna * 32
        img.pintar(img.ret(x0 - 1, 14, x0 + 1, 102), "metal", 0.35)
        for k in range(7):
            y0 = 16 + k * 12
            img.pintar(img.ret(x0 + 1, y0, x0 + 29, y0 + 10), CASCO, 0.36 - 0.04 * ((k + coluna) % 2))
            img.pintar(img.ret(x0 + 1, y0, x0 + 29, y0 + 1), CASCO, 0.7)
            for j in range(3):
                img.cor(img.ret(x0 + 3, y0 + 3 + 2 * j, x0 + 17, y0 + 4 + 2 * j), VIDRO[0])
            for b in range(4):
                led(img, luz, x0 + 20 + 2 * b, y0 + 5, rng.random() < 0.55, AMBAR if rng.random() < 0.1 else CIANO)
    img.pintar(img.ret(6, 102, 74, 104), "metal", 0.16)
    return img, luz


def parede_conduites():
    """Parede de serviço com três conduítes horizontais, braçadeiras e caixas
    de junção. A camada de luz é o fio de ciano que corre dentro do conduíte."""
    rng = np.random.default_rng(431)
    img, luz = kit.parede_base(), Imagem(80, 112)
    for y in (32, 52, 72):
        img.pintar(img.ret(0, y, 80, y + 5), "metal", 0.5)
        img.pintar(img.ret(0, y, 80, y + 1), "metal", 0.85)
        img.pintar(img.ret(0, y + 4, 80, y + 5), "metal", 0.2)
        luz.cor(luz.ret(0, y + 2, 80, y + 3), rgba(CIANO[2], 190))
        for x in (14, 46, 70):
            img.pintar(img.ret(x, y - 2, x + 3, y + 7), "metal", 0.42)
    img.pintar(img.ret(26, 28, 38, 76), "metal", 0.22)
    img.pintar(img.ret(26, 28, 38, 29), "metal", 0.5)
    for j in range(3):
        led(img, luz, 29 + 3 * j, 80, rng.random() < 0.7, AMBAR if j == 2 else CIANO)
    img.pintar(img.ret(25, 76, 39, 86), CASCO, 0.35)
    img.pintar(img.ret(25, 76, 39, 77), CASCO, 0.75)
    img.pintar(img.caminho([(60, 78), (62, 92), (58, 104)], 0.7), "metal", 0.3)
    return img, luz


def parede_painel_ciano():
    """Um painel de parede grande, apagado, com o esquema da rede do prédio
    quando a energia volta: nós ligados por linhas e três barras."""
    img, luz = kit.parede_base(), Imagem(80, 112)
    img.pintar(img.ret(8, 20, 72, 74), "metal", 0.3 + 0.08 * img.fino)
    img.pintar(img.ret(8, 20, 72, 21), "metal", 0.62)
    img.pintar(img.ret(10, 22, 70, 72), VIDRO, 0.16 + 0.3 * kit.ruido_ciclico(80, 112, 20, 12, 440))
    img.pintar(img.ret(10, 22, 70, 72) & (((img.X * 2 + img.Y * 3) % 41) < 4), VIDRO, 0.8, achatar=False)
    nos = [(18, 32), (34, 28), (50, 36), (62, 30), (26, 50), (44, 56), (58, 52)]
    luz.cor(luz.ret(10, 22, 70, 72), rgba(CIANO[1], 26))
    ligacoes = [(0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (5, 6), (2, 6), (1, 5)]
    for a, b in ligacoes:
        luz.cor(luz.caminho([nos[a], nos[b]], 0.5), rgba(CIANO[2], 190))
    for i, (x, y) in enumerate(nos):
        luz.cor(luz.ret(x - 1, y - 1, x + 2, y + 2), rgba(AMBAR[2] if i == 5 else CIANO[4], 255))
    for k, altura in enumerate((8, 14, 10)):
        luz.cor(luz.ret(14 + k * 4, 70 - altura, 16 + k * 4, 70), rgba(CIANO[3], 200))
    varredura(luz)
    img.pintar(img.ret(16, 74, 64, 76), "metal", 0.4)
    img.pintar(img.ret(16, 74, 64, 75), "metal", 0.7)
    return img, luz


def parede_doca_bibliotecario():
    """O bibliotecário: o mesmo robô-professor desligado na doca, com óculos de
    leitura redondos sobre a tela escura. Só cenário."""
    img = gsf.doca_professor("padrao")
    for cx in (36.5, 43.5):
        aro = img.elipse(cx, 52, 3.3, 2.7) & ~img.elipse(cx, 52, 2.2, 1.7)
        img.cor(aro, CASCO[6])
    img.cor(img.ret(40, 51, 41, 52), CASCO[6])
    img.cor(img.ret(32, 51, 33, 52), CASCO[6])
    img.cor(img.ret(47, 51, 48, 52), CASCO[6])
    img.pintar(img.ret(36, 77, 44, 79), CASCO, 0.8)
    luz = gsf.doca_professor_luz("padrao")
    return img, luz


# ---------------------------------------------------------------------------
# O fundo pintado do salão e da ala leste
# ---------------------------------------------------------------------------

ESTANTES_DE_PAREDE = ((350, 400), (476, 610), (720, 790), (820, 880), (980, 1090), (1250, 1330))
VAOS_DE_SERVIDOR = (1, 3, 5)


def servidores_de_parede(img, luz, xa, xb, ya, yb, semente):
    """Pinta por cima de uma estante embutida um vão de servidores: colunas de
    módulos de 10 px com ventilação e LEDs."""
    rng = np.random.default_rng(semente)
    img.pintar(img.ret(xa, ya, xb, yb), "metal", 0.22)
    img.pintar(img.ret(xa + 2, ya + 2, xb - 2, yb), VIDRO, 0.08)
    x = xa + 4
    while x + 18 <= xb - 3:
        img.pintar(img.ret(x - 1, ya + 2, x, yb), "metal", 0.36)
        k = 0
        y = ya + 4
        while y + 9 <= yb - 2:
            img.pintar(img.ret(x, y, x + 17, y + 8), CASCO, 0.34 - 0.04 * (k % 2))
            img.pintar(img.ret(x, y, x + 17, y + 1), CASCO, 0.68)
            for j in range(2):
                img.cor(img.ret(x + 2, y + 2 + 3 * j, x + 10, y + 3 + 3 * j), VIDRO[0])
            for b in range(3):
                led(img, luz, x + 12 + 2 * b, y + 4, rng.random() < 0.5, AMBAR if rng.random() < 0.08 else CIANO)
            y += 10
            k += 1
        x += 20


def fundo_moderna():
    """O fundo do salão e da ala leste (1440 x 180): o original, com três vãos
    de estante trocados por servidores e a placa SILÊNCIO virando um letreiro
    de vidro. Os letreiros das portas são Labels nas cenas, não pintura."""
    img = bib.desenhar_fundo()
    luz = Imagem(img.w, img.h)
    for i in VAOS_DE_SERVIDOR:
        xa, xb = ESTANTES_DE_PAREDE[i]
        servidores_de_parede(img, luz, xa, xb, 30, 100, 450 + i)
    x, y, texto = 642, 42, "SILENCIO"
    larg = 4 * len(texto) + 5
    img.pintar(img.ret(x - 1, y - 1, x + larg + 1, y + 11), "metal", 0.2)
    img.pintar(img.ret(x, y, x + larg, y + 10), VIDRO, 0.1)
    luz.cor(luz.ret(x, y, x + larg, y + 10), rgba(CIANO[1], 50))
    for i, letra in enumerate(texto):
        for j, linha in enumerate(bib.FONTE[letra]):
            for k, ch in enumerate(linha):
                if ch == "1":
                    luz.cor(luz.ret(x + 3 + 4 * i + k, y + 3 + j, x + 4 + 4 * i + k, y + 4 + j), rgba(CIANO[4], 240))
    xe = x + 3 + 4 * 3
    for (dx, dy) in ((0, 2), (1, 1), (2, 2)):
        luz.cor(luz.ret(xe + dx, y + dy, xe + dx + 1, y + dy + 1), rgba(CIANO[3], 240))
    varredura(luz, 0.6)
    return img, luz


# ---------------------------------------------------------------------------
# Saída
# ---------------------------------------------------------------------------


def main():
    print("Gerando o visual futurista da Biblioteca")
    for pasta in (PASTA_OBJETOS, PASTA_PAREDES, PASTA_SALA):
        os.makedirs(pasta, exist_ok=True)
    objetos, paredes = [], []

    def salvar(par, pasta, nome, lista):
        corpo, luz = par
        corpo.salvar(f"{nome}.png", pasta)
        luz.salvar(f"{nome}_luz.png", pasta)
        lista.append((corpo, luz))

    salvar(rack_arquivo(), PASTA_OBJETOS, "rack_arquivo", objetos)
    rack_musgo, _ = rack_arquivo(musgo=True)
    rack_musgo.salvar("rack_arquivo_musgo.png", PASTA_OBJETOS)
    salvar(mesa_holografica(), PASTA_OBJETOS, "mesa_holografica", objetos)
    salvar(cabine_vidro_ciano(), PASTA_OBJETOS, "cabine_vidro_ciano", objetos)
    salvar(torre_equipamentos(), PASTA_OBJETOS, "torre_equipamentos", objetos)
    salvar(gerador(), PASTA_OBJETOS, "gerador", objetos)
    salvar(painel_distribuicao(), PASTA_OBJETOS, "painel_distribuicao", objetos)
    salvar(parede_servidores(), PASTA_PAREDES, "parede_servidores", paredes)
    salvar(parede_conduites(), PASTA_PAREDES, "parede_conduites", paredes)
    salvar(parede_painel_ciano(), PASTA_PAREDES, "parede_painel_ciano", paredes)
    salvar(parede_doca_bibliotecario(), PASTA_PAREDES, "parede_doca_bibliotecario", paredes)
    fundo, fundo_luz = fundo_moderna()
    fundo.salvar("biblioteca_fundo_moderna.png", PASTA_SALA)
    fundo_luz.salvar("biblioteca_fundo_moderna_luz.png", PASTA_SALA)

    if PREVIA:
        largura = 4 * 82
        folha = Imagem(largura + 700, 400)
        folha.px[:, :] = [26, 28, 36, 255]
        for i, (corpo, luz) in enumerate(paredes):
            folha.colar(corpo, i * 82, 0)
            sobrepor(folha, luz, i * 82, 0)
        x = 2
        for corpo, luz in objetos:
            folha.colar(corpo, x, 118)
            sobrepor(folha, luz, x, 118)
            x += corpo.w + 6
        trecho = Imagem(900, 180)
        trecho.colar(fundo, -440, 0)
        faixa = Imagem(900, 180)
        faixa.px[:, :] = [60, 64, 70, 255]
        faixa.colar(fundo, -440, 0)
        luz_trecho = Imagem(900, 180)
        luz_trecho.colar(fundo_luz, -440, 0)
        sobrepor(faixa, luz_trecho, 0, 0)
        folha.colar(faixa, 0, 214)
        os.makedirs(PREVIA, exist_ok=True)
        bib.salvar_png(os.path.join(PREVIA, "previa_biblioteca_moderna.png"), folha.px)


if __name__ == "__main__":
    main()
