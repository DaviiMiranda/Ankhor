# gerar_texturas_quarto.py — desenha por código, pixel a pixel, as texturas e
# os pôsteres do quarto do Gabriel no visor 3D (docs/mecanicas/visor_3d.md).
#
# Como rodar (Python 3 + Pillow):
#   python assets/modelagem/cenario/gerar_texturas_quarto.py
#
# O que sai, em assets/sprites/cenario/visor/:
#
#   TEXTURAS (ladrilhos que se repetem sem emenda)
#     piso_madeira.png   tábuas de 20 cm, com veio, emendas e frestas
#     parede.png         papel de parede de listras finas, gasto
#     madeira.png        veio de madeira dos móveis (e a versão escura)
#     madeira_escura.png
#     porta.png          veio vertical da porta
#     cortica.png        cortiça pintada de grãos
#     tapete.png         trama vermelha com losangos (e a borda)
#     tapete_borda.png
#     cobertor.png       xadrez azul
#     lencol.png         trama clara do lençol e do travesseiro
#     cortina.png        dobras verticais
#     quadro.png         branco com manchas de caneta mal apagada
#     moletom.png        malha vermelha do moletom
#     mochila.png        lona verde
#
#   PÔSTERES
#     poster_fortaleza.png  o pôr do sol na praia, com uma jangada
#     poster_astro.png      um jogo de nave inventado (ASTRO 8)
#     folha_equacoes.png    a folha de Modelagem e Simulação colada na parede
#     calendario_2026.png   um calendário com dias riscados
#     flamula_unifor.png    a flâmula azul da Unifor
#
#   RECORTES DA ILUSTRAÇÃO DO PRÓLOGO (assets/sprites/cutscenes/seg_prologo/cena_02_quarto.png)
#     janela_prologo.png    o vidro da janela, com o pôr do sol na cidade
#     poster_robo.png       o pôster do robô de olhos vermelhos
#     poster_oito_bits.png  o pôster pequeno de 8 bits
#   São cópias, e não a ilustração em si, para o quarto 3D ter as próprias
#   configurações de importação: se o Godot detectar a ilustração do prólogo em
#   uso no 3D, ele pode trocar a compressão dela e borrar a cutscene.
#
# As texturas não têm UV: o Godot as projeta no mundo com mapeamento
# TRIPLANAR (scripts/visor/texturas_do_quarto.gd). Para cada ponto da
# superfície, ele escolhe a textura pela posição no mundo (x, y, z) projetada
# no plano mais de frente para a normal: o chão usa (x, z), uma parede do fundo
# usa (x, y), uma parede lateral usa (z, y). Por isso cada ladrilho tem que
# emendar com ele mesmo nas quatro bordas (o desenho "dá a volta").
#
# Tudo usa um sorteio com semente fixa: rodar de novo dá as mesmas imagens.

import os
import random

from PIL import Image

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", ".."))
SAIDA = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "visor")


def cor(hexa, alfa=255):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4)) + (alfa,)


def mudar(c, quanto):
    """Clareia (quanto > 0) ou escurece (quanto < 0) uma cor, somando em cada canal."""
    return tuple(max(0, min(255, v + quanto)) for v in c[:3]) + (c[3],)


def misturar(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)


def ret(img, x, y, largura, altura, c):
    """Retângulo que dá a volta nas bordas (x e y em módulo do tamanho): é o
    que deixa o ladrilho emendar com ele mesmo."""
    w, h = img.size
    for j in range(y, y + altura):
        for i in range(x, x + largura):
            img.putpixel((i % w, j % h), c)


def px(img, x, y, c):
    w, h = img.size
    img.putpixel((x % w, y % h), c)


def salvar(img, nome):
    img.save(os.path.join(SAIDA, nome + ".png"))


# ---------------------------------------------------------------------------
# TEXTURAS
# ---------------------------------------------------------------------------

def veio(img, sorteio, base, faixas, vertical):
    """Madeira: faixas de tom levemente diferente (as tábuas) e, dentro de cada
    uma, riscos curtos mais escuros no sentido do veio, às vezes um nó."""
    w, h = img.size
    comprimento, largura = (h, w) if vertical else (w, h)
    tamanho_faixa = largura // faixas
    for f in range(faixas):
        tom = mudar(base, sorteio.randint(-10, 10))
        for a in range(f * tamanho_faixa, (f + 1) * tamanho_faixa):
            for b in range(comprimento):
                c = mudar(tom, sorteio.choice([0, 0, 0, -3, 3]))
                img.putpixel((a, b) if vertical else (b, a), c)
        for _ in range(comprimento // 3):
            a = f * tamanho_faixa + sorteio.randrange(tamanho_faixa)
            b = sorteio.randrange(comprimento)
            for k in range(sorteio.randint(2, 6)):
                ponto = (a, b + k) if vertical else (b + k, a)
                px(img, *ponto, mudar(tom, -16))
        if sorteio.random() < 0.5:
            a = f * tamanho_faixa + sorteio.randrange(1, tamanho_faixa - 1)
            b = sorteio.randrange(comprimento)
            ponto = (a, b) if vertical else (b, a)
            px(img, *ponto, mudar(tom, -28))
            px(img, ponto[0] + 1, ponto[1], mudar(tom, -20))
    return tamanho_faixa


def piso_madeira():
    """64 x 64 = 0,8 m de chão: quatro tábuas de 16 px (20 cm) no sentido z,
    com fresta escura entre elas e uma emenda (ponta de tábua) em cada uma,
    em alturas diferentes."""
    sorteio = random.Random(1)
    img = Image.new("RGBA", (64, 64))
    largura = veio(img, sorteio, cor("#4e3728"), 4, vertical=True)
    fresta = cor("#22170f")
    for f in range(4):
        ret(img, f * largura, 0, 1, 64, fresta)
        emenda = sorteio.randrange(64)
        ret(img, f * largura, emenda, largura, 1, fresta)
        ret(img, f * largura + 1, emenda + 1, largura - 1, 1, mudar(cor("#4e3728"), 12))
    salvar(img, "piso_madeira")


def madeira(nome, base, vertical=False):
    sorteio = random.Random(sum(ord(letra) for letra in nome))
    img = Image.new("RGBA", (32, 32))
    veio(img, sorteio, cor(base), 4, vertical)
    salvar(img, nome)


def parede():
    """Papel de parede: listras verticais finas, de 8 em 8 px, um pouco mais
    claras, com uma fileira de pontinhos entre elas, e ruído de manchas."""
    sorteio = random.Random(2)
    base = cor("#57555f")
    img = Image.new("RGBA", (32, 32), base)
    for y in range(32):
        for x in range(32):
            if sorteio.random() < 0.15:
                px(img, x, y, mudar(base, sorteio.choice([-5, 4])))
    for x in range(0, 32, 8):
        ret(img, x, 0, 1, 32, mudar(base, 9))
        for y in range(2, 32, 6):
            px(img, x + 4, y, mudar(base, 6))
    salvar(img, "parede")


def cortica():
    """Grãos de cortiça: três tons sorteados por pixel, com mais do tom do meio."""
    sorteio = random.Random(3)
    tons = [cor("#a5763f"), cor("#a5763f"), cor("#8c6033"), cor("#bf8d52"), cor("#7a522a")]
    img = Image.new("RGBA", (32, 32))
    for y in range(32):
        for x in range(32):
            img.putpixel((x, y), sorteio.choice(tons))
    salvar(img, "cortica")


def tapete():
    """Trama vermelha (xadrez miúdo de dois tons) com um losango claro no meio
    do ladrilho; a borda é a mesma trama, mais escura, com uma listra."""
    img = Image.new("RGBA", (32, 32))
    a, b = cor("#7a2a2e"), cor("#6c2428")
    for y in range(32):
        for x in range(32):
            img.putpixel((x, y), a if (x + y) % 2 == 0 else b)
    claro = cor("#b8584a")
    for i in range(8):
        for (x, y) in [(16 + i, 8 + i), (16 - i, 8 + i), (16 + i, 24 - i), (16 - i, 24 - i)]:
            px(img, x, y, claro)
    px(img, 16, 16, cor("#d8a060"))
    salvar(img, "tapete")

    borda = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            borda.putpixel((x, y), cor("#4e1a1e") if (x + y) % 2 == 0 else cor("#45161a"))
    ret(borda, 0, 7, 16, 2, cor("#b8584a"))
    salvar(borda, "tapete_borda")


def cobertor():
    """Xadrez azul: faixas horizontais e verticais de 8 em 8 px, mais escuras
    onde se cruzam, e uma linha clara fina no meio de cada faixa."""
    img = Image.new("RGBA", (32, 32))
    base, faixa, cruz, fio = cor("#3d4f74"), cor("#33445f"), cor("#2a3850"), cor("#6a7fa6")
    for y in range(32):
        for x in range(32):
            fx, fy = (x % 16) < 6, (y % 16) < 6
            c = cruz if fx and fy else faixa if fx or fy else base
            if x % 16 == 3 or y % 16 == 3:
                c = fio
            img.putpixel((x, y), c)
    salvar(img, "cobertor")


def tecido(nome, base, desenho, semente):
    """Trama simples: um padrão pequeno repetido, mais ruído para não ficar
    perfeito demais. desenho: lista de strings, '#' = mais escuro, '+' = mais claro."""
    sorteio = random.Random(semente)
    altura, largura = len(desenho), len(desenho[0])
    img = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            letra = desenho[y % altura][x % largura]
            c = mudar(cor(base), {"#": -14, "+": 10}.get(letra, 0))
            if sorteio.random() < 0.08:
                c = mudar(c, sorteio.choice([-6, 6]))
            img.putpixel((x, y), c)
    salvar(img, nome)


def cortina():
    """Dobras verticais: o tom sobe e desce como um seno ao longo de x."""
    import math
    img = Image.new("RGBA", (16, 16))
    base = cor("#8a8f9a")
    for x in range(16):
        tom = mudar(base, round(14 * math.sin(2 * math.pi * x / 16)))
        for y in range(16):
            img.putpixel((x, y), tom)
    salvar(img, "cortina")


def quadro():
    """Quadro branco quase limpo: manchas de caneta mal apagada, bem fracas."""
    sorteio = random.Random(5)
    base = cor("#e6e8ec")
    img = Image.new("RGBA", (64, 64), base)
    for _ in range(6):
        cx, cy = sorteio.randrange(64), sorteio.randrange(64)
        tom = misturar(base, sorteio.choice([cor("#c02a2a"), cor("#2a4ac0"), cor("#555a66")]), 0.07)
        for _ in range(40):
            px(img, cx + sorteio.randint(-6, 6), cy + sorteio.randint(-2, 2), tom)
    salvar(img, "quadro")


# ---------------------------------------------------------------------------
# PÔSTERES
# ---------------------------------------------------------------------------

# Fonte de 3 x 5 pixels, só com o que os pôsteres escrevem.
FONTE = {
    "A": ["###", "#.#", "###", "#.#", "#.#"], "C": ["###", "#..", "#..", "#..", "###"],
    "D": ["##.", "#.#", "#.#", "#.#", "##."], "E": ["###", "#..", "##.", "#..", "###"],
    "F": ["###", "#..", "##.", "#..", "#.."], "G": ["###", "#..", "#.#", "#.#", "###"],
    "I": ["###", ".#.", ".#.", ".#.", "###"], "L": ["#..", "#..", "#..", "#..", "###"],
    "M": ["#.#", "###", "###", "#.#", "#.#"], "N": ["##.", "#.#", "#.#", "#.#", "#.#"],
    "O": ["###", "#.#", "#.#", "#.#", "###"], "R": ["##.", "#.#", "##.", "#.#", "#.#"],
    "S": ["###", "#..", "###", "..#", "###"], "T": ["###", ".#.", ".#.", ".#.", ".#."],
    "U": ["#.#", "#.#", "#.#", "#.#", "###"], "X": ["#.#", "#.#", ".#.", "#.#", "#.#"],
    "Z": ["###", "..#", ".#.", "#..", "###"], "0": ["###", "#.#", "#.#", "#.#", "###"],
    "2": ["###", "..#", "###", "#..", "###"], "6": ["###", "#..", "###", "#.#", "###"],
    "8": ["###", "#.#", "###", "#.#", "###"], "=": ["...", "###", "...", "###", "..."],
    "(": [".#.", "#..", "#..", "#..", ".#."], ")": [".#.", "..#", "..#", "..#", ".#."],
    "'": [".#.", ".#.", "...", "...", "..."], "/": ["..#", "..#", ".#.", "#..", "#.."],
    "-": ["...", "...", "###", "...", "..."], "+": ["...", ".#.", "###", ".#.", "..."],
    " ": ["...", "...", "...", "...", "..."],
}


def escrever(img, x, y, texto, c):
    for letra in texto:
        for j, linha in enumerate(FONTE[letra]):
            for i, marca in enumerate(linha):
                if marca == "#":
                    img.putpixel((x + i, y + j), c)
        x += 4


def largura_do_texto(texto):
    return len(texto) * 4 - 1


def moldura(img, c):
    w, h = img.size
    for x in range(w):
        img.putpixel((x, 0), c)
        img.putpixel((x, h - 1), c)
    for y in range(h):
        img.putpixel((0, y), c)
        img.putpixel((w - 1, y), c)


def poster_fortaleza():
    """Pôr do sol na praia: céu em faixas (do roxo ao laranja), o sol pela
    metade no horizonte, o mar com reflexos e uma jangada de vela triangular."""
    img = Image.new("RGBA", (64, 88))
    ceu = [cor("#3a2a5a"), cor("#6a3a6a"), cor("#a84a5a"), cor("#d8704a"), cor("#f0a050")]
    for y in range(60):
        img.putpixel((0, y), ceu[min(4, y // 12)])
        for x in range(64):
            img.putpixel((x, y), ceu[min(4, y // 12)])
    for y in range(48, 60):
        for x in range(64):
            if (x - 32) ** 2 + (y - 60) ** 2 < 120:
                img.putpixel((x, y), cor("#ffe0a0"))
    for y in range(60, 88):
        for x in range(64):
            img.putpixel((x, y), cor("#1e4a6a") if y > 70 else cor("#2a6a8a"))
    sorteio = random.Random(7)
    for _ in range(40):
        x, y = sorteio.randrange(20, 44), sorteio.randrange(61, 76)
        ret(img, x, y, sorteio.randint(2, 4), 1, cor("#f0b060"))
    # Jangada: casco, mastro e a vela triangular.
    ret(img, 12, 66, 14, 2, cor("#3a2418"))
    ret(img, 18, 48, 1, 18, cor("#3a2418"))
    for j in range(16):
        ret(img, 19, 49 + j, j * 9 // 16 + 1, 1, cor("#f4ead8"))
    escrever(img, (64 - largura_do_texto("FORTALEZA")) // 2, 8, "FORTALEZA", cor("#fff0d0"))
    moldura(img, cor("#e8e0d0"))
    salvar(img, "poster_fortaleza")


def poster_astro():
    """Pôster de um jogo inventado: fundo de estrelas, um planeta com anel e
    uma nave em pixel art, com o título em cima."""
    sorteio = random.Random(8)
    img = Image.new("RGBA", (64, 88), cor("#0c0f24"))
    for _ in range(70):
        px(img, sorteio.randrange(64), sorteio.randrange(88), sorteio.choice([cor("#ffffff"), cor("#8ad8ff"), cor("#ffb0e0")]))
    for y in range(88):
        for x in range(64):
            d = (x - 46) ** 2 + (y - 30) ** 2
            if d < 110:
                img.putpixel((x, y), cor("#c86a3a") if (y // 3) % 2 else cor("#e0904a"))
    for x in range(30, 63):
        px(img, x, 30 + (x - 46) // 5, cor("#f0d080"))
    nave = [
        "....#....",
        "...###...",
        "...#+#...",
        "..#####..",
        ".##+++##.",
        "#########",
        "#.#...#.#",
        "..o...o..",
    ]
    cores = {"#": cor("#d0d8e8"), "+": cor("#40c8f0"), "o": cor("#ff8a30")}
    for j, linha in enumerate(nave):
        for i, letra in enumerate(linha):
            if letra in cores:
                for a in range(2):
                    for b in range(2):
                        img.putpixel((16 + i * 2 + a, 50 + j * 2 + b), cores[letra])
    escrever(img, (64 - largura_do_texto("ASTRO 8")) // 2, 8, "ASTRO 8", cor("#ffd040"))
    moldura(img, cor("#30365a"))
    salvar(img, "poster_astro")


def folha_equacoes():
    """A folha quadriculada de Modelagem e Simulação colada na parede: o
    título, umas contas e o gráfico de uma onda (seno) que amortece."""
    import math
    img = Image.new("RGBA", (48, 64), cor("#f2ecd8"))
    for i in range(0, 48, 4):
        ret(img, i, 0, 1, 64, cor("#dde0e8"))
    for j in range(0, 64, 4):
        ret(img, 0, j, 48, 1, cor("#dde0e8"))
    tinta = cor("#2a3a8a")
    escrever(img, 2, 3, "MODELAGEM", cor("#a02a2a"))
    escrever(img, 2, 12, "X'=-X", tinta)
    escrever(img, 2, 20, "X(0)=2", tinta)
    for x in range(4, 46):
        t = (x - 4) / 42
        y = 46 - round(12 * math.exp(-2.2 * t) * math.cos(14 * t))
        px(img, x, y, tinta)
    ret(img, 4, 46, 42, 1, cor("#888c99"))
    ret(img, 4, 32, 1, 28, cor("#888c99"))
    moldura(img, cor("#c8c0a8"))
    salvar(img, "folha_equacoes")


def calendario():
    """Calendário de parede: cabeçalho vermelho com o ano, grade de dias e
    alguns dias riscados com um X (os que já passaram)."""
    img = Image.new("RGBA", (40, 52), cor("#f4f2ee"))
    ret(img, 0, 0, 40, 10, cor("#b8292f"))
    escrever(img, (40 - largura_do_texto("2026")) // 2, 3, "2026", cor("#ffffff"))
    riscados = 17
    for dia in range(30):
        x, y = 3 + (dia % 7) * 5, 14 + (dia // 7) * 7
        ret(img, x, y, 4, 4, cor("#d8d4cc"))
        if dia < riscados:
            for k in range(4):
                px(img, x + k, y + k, cor("#c02a2a"))
                px(img, x + 3 - k, y + k, cor("#c02a2a"))
    moldura(img, cor("#c8c4bc"))
    salvar(img, "calendario_2026")


def flamula():
    """Flâmula triangular azul com a borda amarela e o nome escrito."""
    img = Image.new("RGBA", (72, 28), (0, 0, 0, 0))
    for x in range(72):
        meia = round(13 * (1 - x / 72))
        for y in range(14 - meia, 14 + meia + 1):
            borda = y in (14 - meia, 14 + meia) or x == 0
            img.putpixel((x, y), cor("#e8c040") if borda else cor("#1e4aa0"))
    escrever(img, 6, 12, "UNIFOR", cor("#ffffff"))
    salvar(img, "flamula_unifor")


PROLOGO = os.path.join(PASTA_PROJETO, "assets", "sprites", "cutscenes", "seg_prologo", "cena_02_quarto.png")
RECORTES = {
    "janela_prologo": (56, 30, 224, 196),
    "poster_robo": (509, 55, 579, 143),
    "poster_oito_bits": (544, 149, 581, 193),
}


def recortes_do_prologo():
    """Copia três pedaços da ilustração do prólogo (caixas em pixels: esquerda,
    topo, direita, baixo)."""
    ilustracao = Image.open(PROLOGO).convert("RGBA")
    for nome, caixa in RECORTES.items():
        salvar(ilustracao.crop(caixa), nome)


def main():
    os.makedirs(SAIDA, exist_ok=True)
    recortes_do_prologo()
    piso_madeira()
    parede()
    madeira("madeira", "#6b4a32")
    madeira("madeira_escura", "#3a281c")
    madeira("porta", "#6a4a34", vertical=True)
    madeira("movel", "#3f322c")
    cortica()
    tapete()
    cobertor()
    tecido("lencol", "#d6d8e0", ["#.", ".."], 9)
    tecido("moletom", "#b8292f", ["#..", ".#.", "..#"], 10)
    tecido("mochila", "#5a6b3c", ["#+", "+#"], 11)
    cortina()
    quadro()
    poster_fortaleza()
    poster_astro()
    folha_equacoes()
    calendario()
    flamula()
    print("Texturas e pôsteres salvos em", SAIDA)


main()
