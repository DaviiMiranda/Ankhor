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
#   assets/sprites/salas/labirinto/porta_sala_segura.png  64 x 40, a porta da sala segura (luz verde)
#   assets/sprites/salas/labirinto/porta_corredor_tempo.png  64 x 40, a porta do Corredor do Tempo (luz âmbar)
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
#   Grade LÓGICA: 18 x 11 salinhas. É nela que o labirinto é sorteado e é o
#   GRAFO que os robôs usam para patrulhar (cada salinha é um nó; duas
#   salinhas vizinhas sem parede entre elas são ligadas por uma aresta).
#
#   Grade de BLOCOS (32 x 32 px): cada salinha vira 2 x 2 blocos de chão e
#   as paredes têm 1 bloco de espessura. Por isso a grade de blocos tem
#   3 · 18 + 1 = 55 colunas e 3 · 11 + 1 = 34 fileiras, mais as 6 do
#   esconderijo do Baltazar em cima: 40 fileiras (1760 x 1280 px). É
#   nela que rodam o A* (perseguição) e a BFS (som), no Godot.
#
# ---------------------------------------------------------------------------
# AS SALAS: RETÂNGULOS DE SALINHAS COM UMA ENTRADA SÓ
# ---------------------------------------------------------------------------
#
# A fase tem quatro salas (ver SALAS): a oficina do Zane, que é o primeiro
# destino do Gabriel, e três salas com um nó de controle para hackear. Cada sala é um
# retângulo de salinhas com TODAS as paredes internas derrubadas: um
# salão aberto de (3w - 1) x (3h - 1) blocos.
#
# No sorteio, cada sala é tratada como UM vértice só (uma região) e como
# FOLHA: a busca em profundidade entra nela por uma aresta e volta
# imediatamente, sem expandir. Resultado: a sala tem exatamente uma
# entrada (um beco sem saída, bom para esconder-se... ou para ser
# encurralado). Na etapa dos ciclos, nenhuma parede encostada numa sala é
# derrubada, para a entrada continuar única.
#
# O que fica dentro de cada sala (bancadas, racks, hologramas, o nó, o
# Zane) vem dos MODELOS: um desenho em letras, um caractere por bloco.
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
#   #  parede          .  chão           G  início do Gabriel   T  lanterna (ao lado do início)
#   D  porta de saída (na parede de cima)                        S  saída (gatilho)
#      (D e S só existem no mapa de teste: a saída da fase é o alçapão A)
#   Q  porta da sala segura   H  porta do Corredor do Tempo   (2 blocos de parede cada)
#   A  alçapão escondido na oficina (a saída da fase; o Zane o revela)
#   C  checkpoint      P  pilha          L  lâmpada               V  Sentinela   R  Rastreador
#   Z  o Zane          N  nó de controle (hackeável; 2 blocos de largura)
#   Objetos das salas (minúsculas):
#   b  bancada   c  console   m  mesa com computador   x  robô desmontado   (largos: 2 blocos)
#   r  rack      k  caixas    a  braço robótico        u  cadeira
#   h  holograma de ondas     i  holograma de barras   j  holograma de código
#   O esconderijo do Baltazar (ver "O ESCONDERIJO DO BALTAZAR", abaixo):
#   F  parede falsa (2 blocos; parece parede, só a lanterna revela)
#   B  o Baltazar      y  altar improvisado (com velas)   e  estrelas riscadas na parede (largo)
#   n  ninho de panos (largo)   l  pilha de livros   v  tocos de vela no chão
# Todos os marcadores ficam na fileira de CIMA da salinha: a de baixo fica
# atrás do topo da parede de baixo (ver "Por que corredores de 2 blocos").
# Os checkpoints ficam dentro das salas (nos modelos). Os robôs nascem
# longe do início e da porta da oficina; as pilhas ficam em becos sem
# saída; as lâmpadas, em cruzamentos.
#
# ---------------------------------------------------------------------------
# O ESCONDERIJO DO BALTAZAR: UMA SALA FORA DO GRAFO
# ---------------------------------------------------------------------------
#
# Depois do sorteio, o mapa ganha FILEIRAS_DO_ESCONDERIJO fileiras de
# salinhas EM CIMA, todas de parede, e nelas cavamos uma sala (o
# esconderijo do Baltazar). O sorteio continua idêntico (a mesma semente
# gera o mesmo labirinto); só desloca tudo 3 · FILEIRAS_DO_ESCONDERIJO
# blocos para baixo. Deslocar um múltiplo de 3 mantém as salinhas alinhadas.
#
# A entrada da sala é a parede falsa "FF", na parede de cima do corredor
# que passa embaixo dela. Para o mapa (A*, BFS e as salinhas dos robôs),
# "F" é PAREDE: a sala fica fora do grafo, nenhum robô acha caminho até lá
# e o som não chega. É por isso que o Baltazar sobreviveu escondido nela.
# No jogo, quem desenha a parede falsa e decide quando ela abre é
# scripts/sistemas/parede_falsa.gd.

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

COLUNAS, FILEIRAS = 18, 11
BLOCO = 32
ALTURA_PAREDE = 40
SEMENTE = 3026
FRACAO_CICLOS = 0.18
# Quantos robôs e de que tipo (V = Sentinela, R = Rastreador). Eram 3 numa
# grade de 96 salinhas; a grade nova tem 198, então o dobro.
TIPOS_DE_ROBO = ("V", "R", "V", "V", "R", "V")
DISTANCIA_MINIMA_DO_INICIO = 10
SEPARACAO_ENTRE_ROBOS = 5
QUANTIDADE_PILHAS = 5
QUANTIDADE_LAMPADAS = 14

# Onde o Gabriel começa (uma salinha, com a lanterna ao lado): fora da
# oficina, mas a poucos passos da porta dela. Esta salinha é uma câmara
# logo acima do corredor de baixo, a 5 salinhas de caminho da porta. O
# caminho mais curto até a entrada da oficina tem de ficar nesta faixa
# (em salinhas), senão o gerador reclama.
INICIO = (7, 9)
CAMINHO_ATE_A_OFICINA = (3, 8)
# Os robôs não nascem a menos disso de caminho da entrada da oficina: o
# destino não pode ter um robô parado na porta.
DISTANCIA_MINIMA_DA_OFICINA = 5
# A porta do Corredor do Tempo ("HH", sala opcional): na parede de cima
# desta salinha, no meio do mapa, entre os nós 1 e 2 (10 salinhas de
# caminho do início). Marcar a porta não sorteia nada, então o resto do
# mapa não muda.
PORTA_DO_CORREDOR = (11, 3)

# Cada sala: posição (x, y) e tamanho (w, h) em SALINHAS. A oficina tem a
# entrada fixa (o par de salinhas, de dentro para fora) e é "segura": os
# robôs não patrulham nela (mas podem entrar se estiverem perseguindo).
SALAS = (
    {"nome": "oficina", "x": 0, "y": 9, "w": 4, "h": 2, "entrada": ((3, 10), (4, 10)), "segura": True},
    {"nome": "no_1", "x": 1, "y": 0, "w": 3, "h": 2},
    {"nome": "no_2", "x": 8, "y": 4, "w": 3, "h": 2},
    {"nome": "no_3", "x": 13, "y": 8, "w": 3, "h": 2},
)

# O desenho de cada sala, um caractere por bloco. A fileira 0 é a de cima.
# As duas últimas fileiras de baixo ficam parcialmente atrás do topo da
# parede de baixo (40 px de altura): nada importante nelas.
MODELOS = {
    "oficina": (
        "hLbb.rr.kj.",
        ".....mm...a",
        "k....Z.Au..",
        "..C.....xx.",
        "...........",
    ),
    "no_1": (
        "r.rLr.rh",
        "........",
        "...NN...",
        ".C......",
        "........",
    ),
    "no_2": (
        "cc.hcc.i",
        "........",
        "..NN....",
        "......C.",
        "........",
    ),
    "no_3": (
        "bb.a.kkj",
        "........",
        "...NN...",
        ".C..xx..",
        "........",
    ),
}

# O esconderijo: posição (x, y) e tamanho (w, h) em salinhas, contando as
# fileiras novas de cima. A parede falsa fica embaixo da salinha "entrada_x",
# na parede de baixo da sala, que era a parede de cima do labirinto.
FILEIRAS_DO_ESCONDERIJO = 2
ESCONDERIJO = {"x": 5, "y": 0, "w": 3, "h": 2, "entrada_x": 6}

# O desenho do esconderijo, como os MODELOS das salas. Bagunçado de
# propósito: o Baltazar vive ali desde que chegou ao subsolo. Ele fica logo
# acima da passagem (embaixo, nas colunas 3 e 4), com velas do lado: quem
# entra dá de cara com ele, já iluminado, dentro do raio de visão.
MODELO_ESCONDERIJO = (
    "y.ee.lkl",
    "nn......",
    "..v.B.xx",
    "l.......",
    "........",
)

VERDE = bib.hexa("#0c2014", "#14432a", "#1f7a46", "#3fbf6e", "#9cf2b4", "#e4ffe9")
VERMELHO = bib.hexa("#1e0a0a", "#4a1212", "#7e1c1a", "#b7302a")
AMARELO = bib.hexa("#2a220c", "#5c4a16", "#9a7c22", "#c9a83a")


# ---------------------------------------------------------------------------
# Mapa
# ---------------------------------------------------------------------------

def aresta(a, b):
    return tuple(sorted((a, b)))


def celulas_da_sala(sala):
    return [(x, y) for y in range(sala["y"], sala["y"] + sala["h"])
            for x in range(sala["x"], sala["x"] + sala["w"])]


def sortear_labirinto(rng):
    """Busca em profundidade com volta atrás sobre REGIÕES (uma salinha
    comum é uma região; cada sala inteira é uma só, e é folha), e depois
    os ciclos. Devolve o conjunto de arestas abertas entre salinhas:
    {((x, y), (x2, y2)), ...}."""
    sala_da = {}
    abertas = set()
    for i, sala in enumerate(SALAS):
        celulas = celulas_da_sala(sala)
        for c in celulas:
            sala_da[c] = i
        for (x, y) in celulas:
            for v in ((x + 1, y), (x, y + 1)):
                if v in celulas:
                    abertas.add(aresta((x, y), v))

    def regiao(c):
        return ("sala", sala_da[c]) if c in sala_da else c

    indice_oficina = next(i for i, s in enumerate(SALAS) if s["nome"] == "oficina")
    dentro, fora = SALAS[indice_oficina]["entrada"]
    abertas.add(aresta(dentro, fora))
    visitadas = {("sala", indice_oficina), fora}
    pilha = [fora]
    while pilha:
        x, y = pilha[-1]
        candidatas = [((x, y), (x + dx, y + dy)) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                      if 0 <= x + dx < COLUNAS and 0 <= y + dy < FILEIRAS
                      and regiao((x + dx, y + dy)) not in visitadas]
        if not candidatas:
            pilha.pop()
            continue
        de, para = candidatas[rng.integers(len(candidatas))]
        abertas.add(aresta(de, para))
        visitadas.add(regiao(para))
        if para not in sala_da:
            pilha.append(para)
    esperadas = COLUNAS * FILEIRAS - len(sala_da) + len(SALAS)
    assert len(visitadas) == esperadas, f"regiões inalcançáveis: {len(visitadas)} de {esperadas}"

    fechadas = []
    for y in range(FILEIRAS):
        for x in range(COLUNAS):
            for nx, ny in ((x + 1, y), (x, y + 1)):
                if nx < COLUNAS and ny < FILEIRAS and (x, y) not in sala_da and (nx, ny) not in sala_da:
                    a = aresta((x, y), (nx, ny))
                    if a not in abertas:
                        fechadas.append(a)
    rng.shuffle(fechadas)
    for a in fechadas[:int(len(fechadas) * FRACAO_CICLOS)]:
        abertas.add(a)
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

    for sala in SALAS:
        for by in range(3 * sala["y"] + 1, 3 * (sala["y"] + sala["h"])):
            for bx in range(3 * sala["x"] + 1, 3 * (sala["x"] + sala["w"])):
                grade[by][bx] = "."

    oficina = next(s for s in SALAS if s["nome"] == "oficina")
    entrada_da_oficina = oficina["entrada"][0]
    inicio = INICIO
    dist_oficina, _ = bfs(abertas, entrada_da_oficina)
    assert CAMINHO_ATE_A_OFICINA[0] <= dist_oficina[inicio] <= CAMINHO_ATE_A_OFICINA[1], \
        f"o início fica a {dist_oficina[inicio]} salinhas da oficina"
    dist, _ = bfs(abertas, inicio)
    em_sala = {c for sala in SALAS for c in celulas_da_sala(sala)}
    usadas = em_sala | {inicio}

    def marcar(c, letra, dx=1, dy=1):
        grade[3 * c[1] + dy][3 * c[0] + dx] = letra
        usadas.add(c)

    for sala in SALAS:
        modelo = MODELOS[sala["nome"]]
        assert len(modelo) == 3 * sala["h"] - 1, f"{sala['nome']}: altura do modelo"
        for j, linha in enumerate(modelo):
            assert len(linha) == 3 * sala["w"] - 1, f"{sala['nome']}: largura da fileira {j}"
            for i, letra in enumerate(linha):
                if letra != ".":
                    grade[3 * sala["y"] + 1 + j][3 * sala["x"] + 1 + i] = letra

    marcar(inicio, "G")
    marcar(inicio, "T", 2, 1)

    # A porta da sala segura ("QQ"): na parede de cima da câmara onde o
    # Gabriel começa, para ser a primeira coisa que ele vê. As duas letras
    # ocupam os blocos de parede logo acima da salinha do início.
    yq, xq = 3 * inicio[1], 3 * inicio[0] + 1
    assert grade[yq][xq] == "#" and grade[yq][xq + 1] == "#", "a parede de cima do início não está fechada"
    grade[yq][xq] = grade[yq][xq + 1] = "Q"

    yh, xh = 3 * PORTA_DO_CORREDOR[1], 3 * PORTA_DO_CORREDOR[0] + 1
    assert grade[yh][xh] == "#" and grade[yh][xh + 1] == "#", "a parede de cima da porta do corredor não está fechada"
    assert grade[yh + 1][xh] == "." and grade[yh + 1][xh + 1] == ".", "há um marcador na frente da porta do corredor"
    grade[yh][xh] = grade[yh][xh + 1] = "H"

    longe = sorted(dist, key=lambda c: -dist[c])
    robos = []
    for c in longe:
        if c in usadas or dist[c] < DISTANCIA_MINIMA_DO_INICIO:
            continue
        if dist_oficina[c] < DISTANCIA_MINIMA_DA_OFICINA:
            continue
        if any(abs(c[0] - r[0]) + abs(c[1] - r[1]) < SEPARACAO_ENTRE_ROBOS for r in robos):
            continue
        robos.append(c)
        if len(robos) == len(TIPOS_DE_ROBO):
            break
    assert len(robos) == len(TIPOS_DE_ROBO), f"só coube {len(robos)} robôs"
    for c, letra in zip(robos, TIPOS_DE_ROBO):
        marcar(c, letra, 2, 1)

    becos = [c for c in dist if len(vizinhos(abertas, c)) == 1 and c not in usadas]
    becos.sort(key=lambda c: -dist[c])
    for c in becos[::max(1, len(becos) // QUANTIDADE_PILHAS)][:QUANTIDADE_PILHAS]:
        marcar(c, "P", 2, 1)

    cruzamentos = [c for c in dist if len(vizinhos(abertas, c)) >= 3 and c not in usadas]
    rng.shuffle(cruzamentos)
    for c in cruzamentos[:QUANTIDADE_LAMPADAS]:
        marcar(c, "L", 1, 1)
    print(f"  caminho do início até a entrada da oficina: {dist_oficina[inicio]} salinhas")
    return ["".join(linha) for linha in grade], dist_oficina[inicio]


def miolo(sala, deslocamento=0):
    """O miolo de uma sala em BLOCOS (sem as paredes), como Rect2i: x, y,
    largura, altura. 'deslocamento' são as fileiras de salinhas que entraram
    em cima do mapa depois do sorteio."""
    y = sala["y"] + deslocamento
    return 3 * sala["x"] + 1, 3 * y + 1, 3 * sala["w"] - 1, 3 * sala["h"] - 1


def cavar_esconderijo(linhas):
    """Põe as fileiras novas em cima do mapa sorteado, cava o esconderijo
    do Baltazar nelas e troca dois blocos da parede de cima do labirinto
    (o chão da sala) pela parede falsa "FF"."""
    largura = len(linhas[0])
    grade = [["#"] * largura for _ in range(3 * FILEIRAS_DO_ESCONDERIJO)] + [list(l) for l in linhas]
    x0, y0, w, h = miolo(ESCONDERIJO)
    assert len(MODELO_ESCONDERIJO) == h, "esconderijo: altura do modelo"
    for j, linha in enumerate(MODELO_ESCONDERIJO):
        assert len(linha) == w, f"esconderijo: largura da fileira {j}"
        for i, letra in enumerate(linha):
            grade[y0 + j][x0 + i] = letra
    yf = y0 + h
    xf = 3 * ESCONDERIJO["entrada_x"] + 1
    assert yf == 3 * FILEIRAS_DO_ESCONDERIJO, "a parede falsa tem de ficar na antiga parede de cima"
    assert grade[yf + 1][xf] == "." and grade[yf + 1][xf + 1] == ".", "não há corredor embaixo da parede falsa"
    grade[yf][xf] = grade[yf][xf + 1] = "F"
    return ["".join(linha) for linha in grade]


def salvar_mapa(linhas):
    os.makedirs(os.path.dirname(ARQUIVO_MAPA), exist_ok=True)
    corpo = ", ".join(f'"{l}"' for l in linhas)
    d = FILEIRAS_DO_ESCONDERIJO
    seguras = [s for s in SALAS if s.get("segura")]
    retangulos = ", ".join(f"Rect2i({s['x']}, {s['y'] + d}, {s['w']}, {s['h']})" for s in seguras)
    oficina = next(s for s in SALAS if s["nome"] == "oficina")
    area = miolo(oficina, d)
    # O miolo de cada sala em BLOCOS (sem as paredes). O jogo acha a
    # entrada de cada sala (o único buraco na parede em volta) a partir
    # desses retângulos, põe a porta ali e esconde o que há dentro.
    salas = ", ".join("Rect2i(%d, %d, %d, %d)" % miolo(s, d) for s in SALAS)
    esconderijo = "Rect2i(%d, %d, %d, %d)" % miolo(ESCONDERIJO)
    with open(ARQUIVO_MAPA, "w", encoding="utf-8", newline="\n") as f:
        f.write('[gd_resource type="Resource" script_class="MapaLabirinto" format=3]\n\n')
        f.write('[ext_resource type="Script" path="res://scripts/labirinto/mapa_labirinto.gd" id="1_mapa"]\n\n')
        f.write('[resource]\nscript = ExtResource("1_mapa")\n')
        f.write(f"tamanho_bloco = {BLOCO}\nblocos_por_salinha = 3\n")
        f.write(f"salinhas_seguras = Array[Rect2i]([{retangulos}])\n")
        f.write(f"area_oficina = Rect2i({area[0]}, {area[1]}, {area[2]}, {area[3]})\n")
        f.write(f"salas = Array[Rect2i]([{salas}])\n")
        f.write(f"esconderijo = {esconderijo}\n")
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
            if linhas[by][bx] not in "#DQHF":
                continue
            x, y = bx * BLOCO, by * BLOCO
            sala.colar(sprites["topo"][(bx * 5 + by * 11) % 3], x, y - ALTURA_PAREDE)
            abaixo = linhas[by + 1][bx] if by + 1 < h else "."
            if abaixo not in "#DQHF":
                if linhas[by][bx] in "DQH":
                    if bx == 0 or linhas[by][bx - 1] != linhas[by][bx]:
                        nome = {"D": "porta", "Q": "porta_segura", "H": "porta_corredor"}[linhas[by][bx]]
                        sala.colar(sprites[nome], x, y + BLOCO - ALTURA_PAREDE)
                else:
                    sala.colar(sprites["frente"][(bx * 7 + by * 3) % 4], x, y + BLOCO - ALTURA_PAREDE)
    cores = {"G": (60, 200, 255), "C": (80, 255, 120), "V": (255, 60, 60), "R": (255, 140, 40),
             "P": (240, 240, 80), "L": (255, 220, 150), "S": (80, 255, 120), "T": (200, 200, 255),
             "Z": (255, 255, 60), "N": (255, 60, 255), "A": (255, 255, 255),
             "B": (150, 30, 60), "F": (255, 180, 60)}
    for letra in "bcmxrkauhij":
        cores[letra] = (60, 160, 200)
    for letra in "yenlv":
        cores[letra] = (200, 140, 90)
    for by in range(h):
        for bx in range(w):
            if linhas[by][bx] in cores:
                sala.cor(sala.ret(bx * BLOCO + 10, by * BLOCO + 10, bx * BLOCO + 22, by * BLOCO + 22),
                         list(cores[linhas[by][bx]]) + [255])
    salvar_png(os.path.join(PASTA_SCRIPT if PREVIA == "1" else PREVIA, "previa_labirinto.png"), sala.px)
    print("  prévia: previa_labirinto.png (não commitar)")


def porta_sala_segura():
    """A porta da sala segura: as mesmas folhas de metal da saída, mas em cima,
    no lugar da placa SAÍDA, a lâmpada verde e a plaquinha com a casinha (o
    sinal da sala segura, igual em todas as fases; ver
    assets/modelagem/cenario/gerar_sinal_sala_segura.py). O telhado da casinha
    é um triângulo: |x - meio| <= (y - topo) + 1,5."""
    img = Imagem(2 * BLOCO, ALTURA_PAREDE)
    X, Y = img.X, img.Y
    fino = ruido_toro(2 * BLOCO, ALTURA_PAREDE, 2, 441)
    img.pintar(img.ret(0, 0, 2 * BLOCO, ALTURA_PAREDE), "concreto", 0.30 - 0.14 * Y / ALTURA_PAREDE + 0.04 * fino)
    img.pintar(img.ret(0, 0, 2 * BLOCO, 1), "concreto", 0.62)
    img.pintar(img.ret(14, 12, 50, ALTURA_PAREDE), "metal", 0.1)
    for x0 in (15, 33):
        folha = img.ret(x0, 13, x0 + 16, ALTURA_PAREDE)
        img.pintar(folha, "metal", 0.36 + 0.08 * fino - 0.1 * (Y / ALTURA_PAREDE))
        img.pintar(img.ret(x0 + 2, 16, x0 + 14, 22), "metal", 0.2)
    img.pintar(img.ret(29, 26, 35, 28), "ferrugem", 0.6)                      # maçaneta
    img.pintar(img.ret(18, 2, 24, 8), VERDE, 0.75)                             # a lâmpada
    img.cor(img.ret(20, 4, 22, 6), VERDE[5])
    img.pintar(img.ret(26, 2, 46, 11), VERDE, 0.2)                             # a plaquinha
    meio = 35.5
    telhado = (Y >= 3) & (Y <= 5) & (np.abs(X - meio) <= (Y - 3) + 1.5)
    corpo = (Y >= 6) & (Y <= 9) & (X >= 33) & (X <= 38)
    porta = (Y >= 8) & (X >= 35) & (X <= 36)
    img.cor((telhado | corpo) & ~porta, VERDE[5])
    img.pintar(img.ret(0, ALTURA_PAREDE - 3, 2 * BLOCO, ALTURA_PAREDE), "concreto", 0.05)
    return img


def porta_corredor_tempo():
    """A porta do Corredor do Tempo: as mesmas folhas de metal da porta da
    sala segura, mas com a lâmpada ÂMBAR e, na plaquinha, um relógio: um
    anel (r entre 2,5 e 4) com os dois ponteiros marcando 10 para as 2."""
    img = Imagem(2 * BLOCO, ALTURA_PAREDE)
    X, Y = img.X, img.Y
    fino = ruido_toro(2 * BLOCO, ALTURA_PAREDE, 2, 557)
    img.pintar(img.ret(0, 0, 2 * BLOCO, ALTURA_PAREDE), "concreto", 0.30 - 0.14 * Y / ALTURA_PAREDE + 0.04 * fino)
    img.pintar(img.ret(0, 0, 2 * BLOCO, 1), "concreto", 0.62)
    img.pintar(img.ret(14, 12, 50, ALTURA_PAREDE), "metal", 0.1)
    for x0 in (15, 33):
        folha = img.ret(x0, 13, x0 + 16, ALTURA_PAREDE)
        img.pintar(folha, "metal", 0.36 + 0.08 * fino - 0.1 * (Y / ALTURA_PAREDE))
        img.pintar(img.ret(x0 + 2, 16, x0 + 14, 22), "metal", 0.2)
    img.pintar(img.ret(29, 26, 35, 28), "ferrugem", 0.6)                      # maçaneta
    img.pintar(img.ret(18, 2, 24, 8), "lampada", 0.75)                        # a lâmpada
    img.cor(img.ret(20, 4, 22, 6), RAMPAS["lampada"][-1])
    img.pintar(img.ret(26, 1, 46, 12), "lampada", 0.15)                       # a plaquinha
    cx, cy = 36.0, 6.5
    r = np.hypot(X + 0.5 - cx, Y + 0.5 - cy)
    img.cor((r >= 2.5) & (r <= 4.0), RAMPAS["lampada"][-2])
    img.cor(img.linha(cx, cy, cx - 1.5, cy - 1.5, 0.5), RAMPAS["lampada"][-1])
    img.cor(img.linha(cx, cy, cx + 2.0, cy - 1.0, 0.5), RAMPAS["lampada"][-1])
    img.pintar(img.ret(0, ALTURA_PAREDE - 3, 2 * BLOCO, ALTURA_PAREDE), "concreto", 0.05)
    return img


def main():
    print("Gerando o Labirinto")
    rng = np.random.default_rng(SEMENTE)
    linhas, tamanho_caminho = montar_mapa(rng)
    linhas = cavar_esconderijo(linhas)
    for l in linhas:
        print("   ", l)
    salvar_mapa(linhas)

    os.makedirs(PASTA_SALA, exist_ok=True)
    sprites = {"piso": piso(), "topo": [parede_topo(v) for v in range(3)],
               "frente": [parede_frente(v) for v in range(4)],
               "porta": porta_saida(), "porta_segura": porta_sala_segura(),
               "porta_corredor": porta_corredor_tempo()}
    sprites["piso"].salvar("piso.png", PASTA_SALA)
    for v, img in enumerate(sprites["topo"]):
        img.salvar(f"parede_topo_{v}.png", PASTA_SALA)
    for v, img in enumerate(sprites["frente"]):
        img.salvar(f"parede_frente_{v}.png", PASTA_SALA)
    sprites["porta"].salvar("porta_saida.png", PASTA_SALA)
    sprites["porta_segura"].salvar("porta_sala_segura.png", PASTA_SALA)
    sprites["porta_corredor"].salvar("porta_corredor_tempo.png", PASTA_SALA)
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
