# gerar_labirinto.py — gera o MAPA e a ARTE do Labirinto (o subsolo escuro
# onde o Gabriel foge dos robôs).
#
# Como rodar (Python 3 + numpy):
#
#   python assets/modelagem/salas/labirinto/gerar_labirinto.py
#
# O que sai:
#   dados/labirinto/mapa_labirinto.tres         o mapa (texto, uma linha por fileira)
#   assets/sprites/salas/labirinto/piso.png     64 x 64, repete sem emenda nos dois sentidos
#   assets/sprites/salas/labirinto/parede_topo_<n>.png    32 x 32, o alto do bloco (3 variações)
#   assets/sprites/salas/labirinto/parede_frente_<n>.png  32 x 40, a face da frente (4 variações)
#   assets/sprites/salas/labirinto/porta_saida.png        64 x 40, a saída, com a placa SAÍDA
#   assets/sprites/salas/labirinto/marcas_garra.png, poca.png, papel.png   detalhes do chão
#   assets/sprites/cenario/objetos/checkpoint_apagado.png e checkpoint_aceso.png
#   assets/sprites/cenario/luzes/luz_cone.png   textura do feixe (lanterna e farol da Sentinela)
# Com PREVIA=1, também salva previa_labirinto.png nesta pasta (não commitar).
#
# ---------------------------------------------------------------------------
# O MAPA: UM LABIRINTO "GROSSO" GERADO POR BUSCA EM PROFUNDIDADE
# ---------------------------------------------------------------------------
#
# O labirinto tem duas grades:
#
#   Grade LÓGICA: 12 x 8 salinhas. É nela que o labirinto é sorteado e é o
#   GRAFO que os robôs usam para patrulhar (cada salinha é um nó; duas
#   salinhas vizinhas sem parede entre elas são ligadas por uma aresta).
#
#   Grade de BLOCOS (32 x 32 px): cada salinha vira 2 x 2 blocos de chão e
#   as paredes têm 1 bloco de espessura. Por isso a grade de blocos tem
#   3 · 12 + 1 = 37 colunas e 3 · 8 + 1 = 25 fileiras (1184 x 800 px). É
#   nela que rodam o A* (perseguição) e a BFS (som), no Godot.
#
# Por que corredores de 2 blocos? Na vista do jogo (lateral com
# profundidade), uma parede de 40 px de altura esconde o que está logo
# atrás dela. Com corredor de 1 bloco (32 px), a parede de baixo cobriria o
# corredor inteiro. Com 2 blocos, sobram 24 px de chão à vista, e quem anda
# rente à parede de baixo some da cintura para baixo, como deve ser.
#
# Sorteio: BUSCA EM PROFUNDIDADE com volta atrás ("recursive backtracker"):
#   1. começa numa salinha e marca como visitada;
#   2. escolhe ao acaso uma vizinha NÃO visitada, derruba a parede entre as
#      duas e vai para ela (empilha);
#   3. se não há vizinha livre, volta (desempilha);
#   4. termina quando a pilha esvazia.
# O resultado é uma ÁRVORE: entre duas salinhas existe um caminho só. Num
# jogo de fuga isso é ruim (todo corredor vira beco sem saída com um robô
# atrás). Por isso derrubamos depois mais 18% das paredes internas: surgem
# CICLOS, e sempre dá para dar a volta num quarteirão para despistar.
#
# Os marcadores no mapa (uma letra por bloco):
#   #  parede          .  chão           G  início do Gabriel   T  lanterna
#   D  porta de saída (na parede de cima)                        S  saída (gatilho)
#   C  checkpoint      P  pilha          L  lâmpada               V  Sentinela   R  Rastreador
# Todos os marcadores ficam na fileira de CIMA da salinha: a de baixo fica
# atrás do topo da parede de baixo (ver "Por que corredores de 2 blocos").
# Os checkpoints (se houver: ver CHECKPOINTS) ficam em frações do caminho
# mais curto do início à saída (calculado por BFS no grafo lógico). Os robôs nascem longe do início; as
# pilhas ficam em becos sem saída; as lâmpadas, em cruzamentos.

import importlib.util
import os

import numpy as np

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "..", ".."))
PASTA_SALA = os.path.join(PASTA_PROJETO, "assets", "sprites", "salas", "labirinto")
PASTA_OBJETOS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "objetos")
PASTA_LUZES = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "luzes")
ARQUIVO_MAPA = os.path.join(PASTA_PROJETO, "dados", "labirinto", "mapa_labirinto.tres")
PREVIA = os.environ.get("PREVIA", "")

_spec = importlib.util.spec_from_file_location(
    "gerar_biblioteca",
    os.path.join(PASTA_PROJETO, "assets", "modelagem", "salas", "biblioteca", "gerar_biblioteca.py"))
bib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bib)
Imagem, RAMPAS, CONTORNO, salvar_png = bib.Imagem, bib.RAMPAS, bib.CONTORNO, bib.salvar_png

COLUNAS, FILEIRAS = 12, 8
BLOCO = 32
ALTURA_PAREDE = 40
SEMENTE = 3026
FRACAO_CICLOS = 0.18
# Onde pôr checkpoints, em fração do caminho mais curto até a saída (ex.:
# (0.40, 0.75)). Vazio por enquanto: a fase ainda é pequena e morrer
# recomeça do início.
CHECKPOINTS = ()

VERDE = bib.hexa("#0c2014", "#14432a", "#1f7a46", "#3fbf6e", "#9cf2b4", "#e4ffe9")
VERMELHO = bib.hexa("#1e0a0a", "#4a1212", "#7e1c1a", "#b7302a")
AMARELO = bib.hexa("#2a220c", "#5c4a16", "#9a7c22", "#c9a83a")


# ---------------------------------------------------------------------------
# Mapa
# ---------------------------------------------------------------------------

def sortear_labirinto(rng):
    """Busca em profundidade com volta atrás, e depois os ciclos. Devolve o
    conjunto de arestas abertas entre salinhas: {((x, y), (x2, y2)), ...}."""
    visitada = np.zeros((FILEIRAS, COLUNAS), dtype=bool)
    abertas = set()
    pilha = [(0, FILEIRAS - 1)]
    visitada[FILEIRAS - 1, 0] = True
    while pilha:
        x, y = pilha[-1]
        livres = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= x + dx < COLUNAS and 0 <= y + dy < FILEIRAS and not visitada[y + dy, x + dx]]
        if not livres:
            pilha.pop()
            continue
        nx, ny = livres[rng.integers(len(livres))]
        visitada[ny, nx] = True
        abertas.add(tuple(sorted(((x, y), (nx, ny)))))
        pilha.append((nx, ny))
    fechadas = []
    for y in range(FILEIRAS):
        for x in range(COLUNAS):
            for nx, ny in ((x + 1, y), (x, y + 1)):
                if nx < COLUNAS and ny < FILEIRAS:
                    aresta = tuple(sorted(((x, y), (nx, ny))))
                    if aresta not in abertas:
                        fechadas.append(aresta)
    rng.shuffle(fechadas)
    for aresta in fechadas[:int(len(fechadas) * FRACAO_CICLOS)]:
        abertas.add(aresta)
    return abertas


def vizinhos(abertas, c):
    x, y = c
    return [v for v in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
            if tuple(sorted((c, v))) in abertas]


def bfs(abertas, origem):
    """Busca em largura no grafo lógico: distância (em salinhas) e de onde
    cada salinha foi alcançada (para reconstruir o caminho)."""
    dist, pai = {origem: 0}, {origem: None}
    fila = [origem]
    while fila:
        c = fila.pop(0)
        for v in vizinhos(abertas, c):
            if v not in dist:
                dist[v] = dist[c] + 1
                pai[v] = c
                fila.append(v)
    return dist, pai


def montar_mapa(rng):
    abertas = sortear_labirinto(rng)
    w, h = 3 * COLUNAS + 1, 3 * FILEIRAS + 1
    grade = [["#"] * w for _ in range(h)]
    for y in range(FILEIRAS):
        for x in range(COLUNAS):
            for dy in (1, 2):
                for dx in (1, 2):
                    grade[3 * y + dy][3 * x + dx] = "."
    for (a, b) in abertas:
        (x1, y1), (x2, y2) = a, b
        if y1 == y2:
            for dy in (1, 2):
                grade[3 * y1 + dy][3 * x2] = "."
        else:
            for dx in (1, 2):
                grade[3 * y2][3 * x1 + dx] = "."

    inicio, fim = (0, FILEIRAS - 1), (COLUNAS - 1, 0)
    dist, pai = bfs(abertas, inicio)
    caminho = [fim]
    while pai[caminho[-1]] is not None:
        caminho.append(pai[caminho[-1]])
    caminho.reverse()
    usadas = {inicio, fim}

    def marcar(c, letra, dx=1, dy=1):
        grade[3 * c[1] + dy][3 * c[0] + dx] = letra
        usadas.add(c)

    marcar(inicio, "G")
    marcar(inicio, "T", 2, 1)
    grade[0][3 * fim[0] + 1] = "D"
    grade[0][3 * fim[0] + 2] = "D"
    marcar(fim, "S")
    for fracao in CHECKPOINTS:
        marcar(caminho[int(len(caminho) * fracao)], "C", 2, 1)

    longe = sorted(dist, key=lambda c: -dist[c])
    robos = []
    for c in longe:
        if c in usadas or dist[c] < 6 or any(abs(c[0] - r[0]) + abs(c[1] - r[1]) < 4 for r in robos):
            continue
        robos.append(c)
        if len(robos) == 3:
            break
    for c, letra in zip(robos, ("V", "R", "V")):
        marcar(c, letra, 2, 1)

    becos = [c for c in dist if len(vizinhos(abertas, c)) == 1 and c not in usadas]
    becos.sort(key=lambda c: -dist[c])
    for c in becos[::max(1, len(becos) // 3)][:3]:
        marcar(c, "P", 2, 1)

    cruzamentos = [c for c in dist if len(vizinhos(abertas, c)) >= 3 and c not in usadas]
    rng.shuffle(cruzamentos)
    for c in cruzamentos[:8]:
        marcar(c, "L", 1, 1)
    return ["".join(linha) for linha in grade], len(caminho)


def salvar_mapa(linhas):
    os.makedirs(os.path.dirname(ARQUIVO_MAPA), exist_ok=True)
    corpo = ", ".join(f'"{l}"' for l in linhas)
    with open(ARQUIVO_MAPA, "w", encoding="utf-8", newline="\n") as f:
        f.write('[gd_resource type="Resource" script_class="MapaLabirinto" format=3]\n\n')
        f.write('[ext_resource type="Script" path="res://scripts/labirinto/mapa_labirinto.gd" id="1_mapa"]\n\n')
        f.write('[resource]\nscript = ExtResource("1_mapa")\n')
        f.write(f"tamanho_bloco = {BLOCO}\nblocos_por_salinha = 3\n")
        f.write(f"linhas = PackedStringArray({corpo})\n")
    print("  salvo:", os.path.relpath(ARQUIVO_MAPA, PASTA_PROJETO))


# ---------------------------------------------------------------------------
# Arte
# ---------------------------------------------------------------------------

def ruido_toro(largura, altura, passo, semente):
    """Ruído de valor que dá a volta nos DOIS sentidos (como a superfície de
    uma rosquinha, um toro): a coluna depois da última é a primeira, e a
    fileira depois da última também. Assim a textura repete sem emenda para
    os lados e para cima/baixo. largura e altura precisam ser múltiplas do
    passo."""
    rng = np.random.default_rng(semente)
    gw, gh = largura // passo, altura // passo
    grade = rng.random((gh, gw))
    y, x = np.mgrid[0:altura, 0:largura]
    fx, fy = (x + 0.5) / passo, (y + 0.5) / passo
    x0, y0 = np.floor(fx).astype(int), np.floor(fy).astype(int)
    tx, ty = fx - x0, fy - y0
    sx, sy = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
    a = grade[y0 % gh, x0 % gw]
    b = grade[y0 % gh, (x0 + 1) % gw]
    c = grade[(y0 + 1) % gh, x0 % gw]
    d = grade[(y0 + 1) % gh, (x0 + 1) % gw]
    return (a * (1 - sx) + b * sx) * (1 - sy) + (c * (1 - sx) + d * sx) * sy


def piso():
    """Chão do subsolo: placas de concreto de 32 x 32 com juntas escuras,
    manchas de umidade e sujeira. Bem mais escuro que a Biblioteca: aqui
    nunca bate sol."""
    n = 64
    img = Imagem(n, n)
    X, Y = img.X, img.Y
    manchas = ruido_toro(n, n, 16, 401)
    fino = ruido_toro(n, n, 2, 402)
    valor = 0.22 + 0.12 * manchas + 0.05 * fino
    tudo = img.ret(0, 0, n, n)
    img.pintar(tudo, "piso", valor)
    junta = (X % 32 == 0) | (Y % 32 == 0)
    img.pintar(junta, "piso", 0.06)
    sujeira = tudo & (ruido_toro(n, n, 4, 403) > 0.82)
    img.pintar(sujeira, "piso", 0.12 + 0.06 * fino)
    return img


def parede_topo(variacao):
    """O alto do bloco de parede: concreto mais claro que o chão (é a face
    que recebe a luz de cima), com a emenda das placas. Três variações
    (lisa, com rachadura, com mancha escura) sorteadas por bloco no Godot,
    para a repetição não aparecer. As bordas são iguais nas três: blocos
    vizinhos formam uma parede contínua."""
    img = Imagem(BLOCO, BLOCO)
    X, Y = img.X, img.Y
    manchas = ruido_toro(BLOCO, BLOCO, 16, 411 + variacao)
    fino = ruido_toro(BLOCO, BLOCO, 2, 412 + variacao)
    img.pintar(img.ret(0, 0, BLOCO, BLOCO), "concreto", 0.40 + 0.06 * manchas + 0.05 * fino)
    img.pintar((X == 0) | (Y == 0), "concreto", 0.26)
    if variacao == 1:
        img.pintar(img.caminho([(5, 9), (11, 13), (14, 21), (20, 24)], 0.45), "concreto", 0.18)
    elif variacao == 2:
        mancha = img.elipse(20, 12, 7, 5) & (ruido_toro(BLOCO, BLOCO, 4, 415) > 0.35)
        img.pintar(mancha, "concreto", 0.3)
    return img


def parede_frente(variacao):
    """A face da frente do bloco (40 px de altura: ~1,5 m na escala do
    Gabriel). Luz vem de cima: a borda de cima é clara (a quina com o
    topo) e a de baixo escurece até a sombra de contato com o chão.
    Variações: 0 lisa, 1 com ferrugem escorrendo, 2 com um cano, 3 com a
    faixa de perigo amarela e preta desbotada."""
    img = Imagem(BLOCO, ALTURA_PAREDE)
    X, Y = img.X, img.Y
    manchas = ruido_toro(BLOCO, ALTURA_PAREDE, 8, 420 + variacao)
    fino = ruido_toro(BLOCO, ALTURA_PAREDE, 2, 430 + variacao)
    descida = Y / ALTURA_PAREDE
    valor = 0.30 + 0.08 * manchas + 0.04 * fino - 0.16 * descida
    img.pintar(img.ret(0, 0, BLOCO, ALTURA_PAREDE), "concreto", valor)
    img.pintar(X == 0, "concreto", 0.12)
    img.pintar(img.ret(0, 0, BLOCO, 1), "concreto", 0.62)
    img.pintar(img.ret(0, 14, BLOCO, 15), "concreto", 0.15)
    if variacao == 1:
        for x0 in (7, 19, 24):
            escorrido = (X == x0) & (Y > 2) & (Y < 16 + (x0 * 7) % 16)
            img.pintar(escorrido, "ferrugem", 0.45 + 0.2 * fino)
    elif variacao == 2:
        img.pintar(img.ret(0, 20, BLOCO, 24), "metal", 0.30 + 0.25 * (Y == 20))
        img.pintar(img.ret(12, 18, 17, 26), "ferrugem", 0.45 + 0.2 * (Y == 18))
    elif variacao == 3:
        faixa = img.ret(0, 28, BLOCO, 33)
        listra = ((X + Y) // 4) % 2 == 0
        img.pintar(faixa & listra, AMARELO, 0.45 + 0.2 * fino)
        img.pintar(faixa & ~listra, "concreto", 0.08)
    img.pintar(img.ret(0, ALTURA_PAREDE - 3, BLOCO, ALTURA_PAREDE), "concreto", 0.05)
    return img


# Letras 3 x 5 para a placa (só as que a palavra SAÍDA usa).
LETRAS = {
    "S": ["111", "100", "111", "001", "111"],
    "A": ["010", "101", "111", "101", "101"],
    "I": ["111", "010", "010", "010", "111"],
    "D": ["110", "101", "101", "101", "110"],
}


def porta_saida():
    """A saída: duas folhas de porta de metal na parede de cima e, acima,
    a placa verde SAÍDA acesa (a única coisa verde no escuro). No Godot,
    uma luz verde fica em cima da placa."""
    img = Imagem(2 * BLOCO, ALTURA_PAREDE)
    X, Y = img.X, img.Y
    fino = ruido_toro(2 * BLOCO, ALTURA_PAREDE, 2, 440)
    img.pintar(img.ret(0, 0, 2 * BLOCO, ALTURA_PAREDE), "concreto", 0.30 - 0.14 * Y / ALTURA_PAREDE + 0.04 * fino)
    img.pintar(img.ret(0, 0, 2 * BLOCO, 1), "concreto", 0.62)
    img.pintar(img.ret(14, 12, 50, ALTURA_PAREDE), "metal", 0.1)
    for x0 in (15, 33):
        folha = img.ret(x0, 13, x0 + 16, ALTURA_PAREDE)
        img.pintar(folha, "metal", 0.36 + 0.08 * fino - 0.1 * (Y / ALTURA_PAREDE))
        img.pintar(img.ret(x0 + 2, 16, x0 + 14, 22), "metal", 0.2)
    img.pintar(img.ret(29, 26, 35, 28), "ferrugem", 0.6)                      # barra antipânico
    img.pintar(img.ret(20, 3, 44, 10), VERDE, 0.35)
    img.pintar(img.ret(21, 4, 43, 9), VERDE, 0.55)
    x = 23
    for letra in "SAIDA":
        for j, linha in enumerate(LETRAS[letra]):
            for k, ch in enumerate(linha):
                if ch == "1":
                    img.cor(img.ret(x + k, 4 + j, x + k + 1, 5 + j), VERDE[5])
        x += 4
    img.cor(img.ret(32, 3, 33, 4), VERDE[5])                                  # acento do Í
    img.pintar(img.ret(0, ALTURA_PAREDE - 3, 2 * BLOCO, ALTURA_PAREDE), "concreto", 0.05)
    return img


def marcas_garra():
    """Três riscos paralelos no concreto: as garras da Sentinela. Avisam
    o jogador de que algo passa por ali."""
    img = Imagem(14, 9)
    for i in range(3):
        img.pintar(img.linha(1 + 3 * i, 1, 5 + 3 * i, 7, 0.5), "concreto", 0.55)
    return img


def poca():
    """Poça d'água escura com o reflexo claro de 1 px de uma luz."""
    img = Imagem(18, 7)
    img.pintar(img.elipse(9, 3.5, 8.5, 3.2), "concreto", 0.03)
    img.pintar(img.elipse(9, 3.5, 7, 2.2), "metal", 0.12)
    img.cor(img.ret(6, 2, 9, 3), RAMPAS["ceu"][2])
    return img


def papel():
    """Uma folha de papel velha no chão, dobrada."""
    img = Imagem(7, 5)
    img.pintar(img.poligono([(0, 1), (6, 0), (7, 4), (1, 5)]), "papel", 0.55)
    img.pintar(img.linha(1, 3, 5, 2, 0.4), "papel", 0.25)
    return img


def checkpoint(aceso):
    """Posto de emergência: um poste baixo de metal com uma caixa de luz em
    cima. Apagado, a lente é vermelha e fraca; aceso (checkpoint salvo),
    fica verde e forte, e uma luz verde acende em volta no Godot."""
    img = Imagem(14, 26)
    X, Y = img.X, img.Y
    img.pintar(img.ret(3, 23, 11, 26), "metal", 0.2)                          # base
    img.pintar(img.ret(6, 9, 8, 23), "metal", 0.3 + 0.2 * (X == 6))            # poste
    img.pintar(img.ret(2, 1, 12, 10), "metal", 0.35 + 0.25 * (Y == 1))         # caixa
    lente = img.ret(4, 3, 10, 8)
    if aceso:
        img.pintar(lente, VERDE, 0.6 + 0.35 * (1 - np.abs(X - 6.5) / 3))
        img.cor(img.ret(5, 4, 7, 5), VERDE[5])
    else:
        img.pintar(lente, VERMELHO, 0.35)
    img.contornar()
    return img, 7, 25


def luz_cone():
    """Textura do FEIXE de luz (lanterna do Gabriel e farol da Sentinela).
    A luz sai do centro da imagem e aponta para a direita (+x); no Godot a
    PointLight2D gira para onde o feixe deve apontar.

    Intensidade de cada pixel = (queda com a distância) x (queda com o
    ângulo). Distância d (0 no centro, 1 na borda): (1 - d)^1,4. Ângulo:
    o cosseno entre a direção do pixel e o eixo do feixe (produto escalar
    de dois vetores unitários, o mesmo cálculo do campo de visão dos
    robôs). Dentro de ±20° a luz é cheia; de 20° a 32° ela some suave
    (smoothstep). Um brilho redondo e fraco em volta da origem ilumina o
    próprio Gabriel. Depois cortamos em degraus com dithering, como a
    textura de luz da Biblioteca."""
    n = 256
    img = Imagem(n, n)
    dx = (img.X + 0.5 - n / 2) / (n / 2)
    dy = (img.Y + 0.5 - n / 2) / (n / 2)
    d = np.sqrt(dx * dx + dy * dy)
    cosseno = np.where(d > 0, dx / np.maximum(d, 1e-6), 1.0)
    cheio, borda = np.cos(np.radians(20)), np.cos(np.radians(32))
    t = np.clip((cosseno - borda) / (cheio - borda), 0, 1)
    angular = t * t * (3 - 2 * t)
    feixe = np.clip(1 - d, 0, 1) ** 1.4 * angular
    halo = np.clip(1 - d / 0.14, 0, 1) ** 2 * 0.55
    i = np.clip(np.maximum(feixe, halo), 0, 1)
    i = np.floor(i * 8 + img.limiar * 0.999) / 8
    img.px[..., :3] = 255
    img.px[..., 3] = (np.clip(i, 0, 1) * 255).astype(np.uint8)
    return img


# ---------------------------------------------------------------------------

def previa(linhas, sprites):
    """Monta o labirinto inteiro como o Godot desenha (sem luzes), para
    conferir o mapa e a arte."""
    h, w = len(linhas), len(linhas[0])
    sala = Imagem(w * BLOCO, h * BLOCO)
    for y in range(0, sala.h, 64):
        for x in range(0, sala.w, 64):
            sala.colar(sprites["piso"], x, y)
    for by in range(h):
        for bx in range(w):
            if linhas[by][bx] not in "#D":
                continue
            x, y = bx * BLOCO, by * BLOCO
            sala.colar(sprites["topo"][(bx * 5 + by * 11) % 3], x, y - ALTURA_PAREDE)
            abaixo = linhas[by + 1][bx] if by + 1 < h else "."
            if abaixo not in "#D":
                if linhas[by][bx] == "D":
                    if bx == 0 or linhas[by][bx - 1] != "D":
                        sala.colar(sprites["porta"], x, y + BLOCO - ALTURA_PAREDE)
                else:
                    sala.colar(sprites["frente"][(bx * 7 + by * 3) % 4], x, y + BLOCO - ALTURA_PAREDE)
    cores = {"G": (60, 200, 255), "C": (80, 255, 120), "V": (255, 60, 60), "R": (255, 140, 40),
             "P": (240, 240, 80), "L": (255, 220, 150), "S": (80, 255, 120), "T": (200, 200, 255)}
    for by in range(h):
        for bx in range(w):
            if linhas[by][bx] in cores:
                sala.cor(sala.ret(bx * BLOCO + 10, by * BLOCO + 10, bx * BLOCO + 22, by * BLOCO + 22),
                         list(cores[linhas[by][bx]]) + [255])
    salvar_png(os.path.join(PASTA_SCRIPT if PREVIA == "1" else PREVIA, "previa_labirinto.png"), sala.px)
    print("  prévia: previa_labirinto.png (não commitar)")


def main():
    print("Gerando o Labirinto")
    rng = np.random.default_rng(SEMENTE)
    linhas, tamanho_caminho = montar_mapa(rng)
    for l in linhas:
        print("   ", l)
    print(f"  caminho mais curto do início à saída: {tamanho_caminho} salinhas")
    salvar_mapa(linhas)

    os.makedirs(PASTA_SALA, exist_ok=True)
    sprites = {"piso": piso(), "topo": [parede_topo(v) for v in range(3)],
               "frente": [parede_frente(v) for v in range(4)],
               "porta": porta_saida()}
    sprites["piso"].salvar("piso.png", PASTA_SALA)
    for v, img in enumerate(sprites["topo"]):
        img.salvar(f"parede_topo_{v}.png", PASTA_SALA)
    for v, img in enumerate(sprites["frente"]):
        img.salvar(f"parede_frente_{v}.png", PASTA_SALA)
    sprites["porta"].salvar("porta_saida.png", PASTA_SALA)
    marcas_garra().salvar("marcas_garra.png", PASTA_SALA)
    poca().salvar("poca.png", PASTA_SALA)
    papel().salvar("papel.png", PASTA_SALA)
    for aceso, nome in ((False, "checkpoint_apagado"), (True, "checkpoint_aceso")):
        img, px, py = checkpoint(aceso)
        img.salvar(f"{nome}.png", PASTA_OBJETOS)
    print(f"    checkpoint: pé em ({px}, {py}) -> offset = Vector2({-px}, {-py})")
    luz_cone().salvar("luz_cone.png", PASTA_LUZES)
    if PREVIA:
        previa(linhas, sprites)


if __name__ == "__main__":
    main()
