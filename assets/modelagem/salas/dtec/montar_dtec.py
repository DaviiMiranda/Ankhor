# montar_dtec.py — monta as cenas do Godot do DTEC (docs/fases/dtec.md):
# a cena de cada peça do kit (cenas/cenario/dtec/) e as 10 salas da fase
# (cenas/salas/dtec/), a partir das descrições no fim deste arquivo.
#
# Como rodar (Python 3, depois do gerar_dtec.py):
#
#   python assets/modelagem/cenario/gerar_dtec.py
#   python assets/modelagem/salas/dtec/montar_dtec.py
#
# ATENÇÃO: este script é a PRIMEIRA montagem. Ele sobrescreve as cenas das
# salas. Depois que alguém ajustar uma sala no editor do Godot, não rode de
# novo sem antes passar o ajuste para a descrição da sala aqui embaixo.
#
# Como uma sala é montada (as mesmas regras do bunker, ver
# cenas/salas/bunker/gerador.tscn):
#   - a parede do fundo é uma fileira de peças de 80 px, de x = 0 até a
#     largura, com um pilar de 16 px em cada ponta;
#   - o chão de perto é uma fileira de peças de 128 px (com y = 0: a peça
#     já desenha a partir de y = 112, onde a parede encontra o chão);
#   - salas FUNDAS (mais altas que 180) continuam o chão para baixo com as
#     peças "_fundo" de 64 px, a partir de y = 180, e as paredes laterais
#     de 16 px nas duas pontas, a partir de y = 112;
#   - uma porta na parede fica em x = (x da peça) + 41 e y = 124: é onde o
#     vão da porta toca o chão.

import math
import os

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "..", ".."))
PASTA_KIT = os.path.join(PASTA_PROJETO, "cenas", "cenario", "dtec")
PASTA_SALAS = os.path.join(PASTA_PROJETO, "cenas", "salas", "dtec")

PECA = 80
CHAO = 128
FUNDO = 64
Y_CHAO = 112
X_PORTA = 41
X_PORTA_CENTRAL = 40
Y_PORTA = 124

# Pegadas e pés dos objetos (os mesmos números que o gerar_dtec.py imprime).
OBJETOS = {
    "bancada_lab": ((36, 38), (66, 6)),
    "bancada_eletronica": ((36, 38), (66, 6)),
    "mesa_computador": ((26, 34), (46, 5)),
    "cadeira_escritorio": ((9, 24), (12, 3)),
    "rack_dtec": ((13, 54), (24, 5)),
    "armario_quimico": ((18, 52), (34, 5)),
    "capela": ((25, 62), (46, 5)),
    "cilindros": ((14, 46), (26, 5)),
    "braco_robotico": ((18, 50), (26, 5)),
    "robo_desmontado": ((32, 36), (60, 5)),
    "console": ((32, 34), (58, 5)),
    "planta": ((15, 38), (14, 4)),
    "balcao_recepcao": ((50, 36), (96, 6)),
    "catraca": ((10, 28), (14, 4)),
    "maquina": ((88, 154), (150, 22)),
    "caixas_lab": ((22, 28), (40, 5)),
}
PAREDES = ["dtec_lisa", "dtec_rachada", "dtec_luminaria", "dtec_porta", "dtec_porta_trancada",
           "dtec_porta_lacrada", "dtec_porta_central", "dtec_vidro", "dtec_quadro", "dtec_painel",
           "dtec_armario", "dtec_cartaz", "dtec_terminal", "dtec_extintor", "dtec_canos",
           "dtec_tela_grande", "pilar_dtec", "dtec_lateral"]
CHAOS = ["chao_dtec", "chao_dtec_cabos", "chao_dtec_elevado", "chao_dtec_faixa"]
CHAOS_FUNDO = ["chao_dtec_fundo", "chao_dtec_elevado_fundo", "chao_dtec_cabos_fundo", "chao_dtec_faixa_fundo"]


def pascal(nome):
    return "".join(parte.capitalize() for parte in nome.split("_"))


def escrever(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as arquivo:
        arquivo.write(texto)


# ---------------------------------------------------------------------------
# Cenas das peças do kit
# ---------------------------------------------------------------------------


def cena_sprite(nome, pasta, deslocamento=None):
    linhas = [
        "[gd_scene format=3]", "",
        f'[ext_resource type="Texture2D" path="res://assets/sprites/cenario/dtec/{pasta}/{nome}.png" id="1_peca"]', "",
        f'[node name="{pascal(nome)}" type="Sprite2D"]',
        'texture = ExtResource("1_peca")',
        "centered = false",
    ]
    if deslocamento:
        linhas.append(f"offset = Vector2(0, {deslocamento})")
    return "\n".join(linhas) + "\n"


def cena_objeto(nome):
    (px, py), (larg, alt) = OBJETOS[nome]
    texto = f"""[gd_scene format=3]

[ext_resource type="Script" path="res://scripts/cenario/objeto_cenario.gd" id="1_objeto"]
[ext_resource type="Texture2D" path="res://assets/sprites/cenario/dtec/objetos/{nome}.png" id="2_sprite"]
"""
    if nome == "maquina":
        texto += """
[sub_resource type="Gradient" id="Gradient_faisca"]
colors = PackedColorArray(0.85, 1, 1, 1, 0.3, 0.9, 1, 0)
"""
    texto += f"""
[sub_resource type="RectangleShape2D" id="Pegada"]
size = Vector2({larg}, {alt})

[node name="{pascal(nome)}" type="StaticBody2D"]
script = ExtResource("1_objeto")

[node name="Sprite2D" type="Sprite2D" parent="."]
texture = ExtResource("2_sprite")
centered = false
offset = Vector2({-px}, {-py})

[node name="Pegada" type="CollisionShape2D" parent="."]
position = Vector2(0, {-alt / 2})
shape = SubResource("Pegada")
"""
    if nome == "maquina":
        # Faíscas subindo do núcleo (o núcleo fica 88 px acima do pé).
        texto += """
[node name="Faiscas" type="CPUParticles2D" parent="."]
position = Vector2(0, -88)
amount = 28
lifetime = 1.8
emission_shape = 1
emission_sphere_radius = 16.0
direction = Vector2(0, -1)
spread = 70.0
gravity = Vector2(0, -6)
initial_velocity_min = 4.0
initial_velocity_max = 14.0
scale_amount_min = 1.0
scale_amount_max = 2.0
color_ramp = SubResource("Gradient_faisca")
"""
    return texto


def montar_kit():
    for nome in PAREDES:
        escrever(os.path.join(PASTA_KIT, "paredes", f"{nome}.tscn"), cena_sprite(nome, "paredes"))
    for nome in CHAOS:
        escrever(os.path.join(PASTA_KIT, "chao", f"{nome}.tscn"), cena_sprite(nome, "chao", Y_CHAO))
    for nome in CHAOS_FUNDO:
        escrever(os.path.join(PASTA_KIT, "chao", f"{nome}.tscn"), cena_sprite(nome, "chao"))
    for nome in OBJETOS:
        escrever(os.path.join(PASTA_KIT, "objetos", f"{nome}.tscn"), cena_objeto(nome))


# ---------------------------------------------------------------------------
# Cenas das salas
# ---------------------------------------------------------------------------


class Montagem:
    """Junta os recursos externos (cada um com um id) e os nós de uma sala,
    e escreve o .tscn no fim."""

    def __init__(self):
        self.recursos = {}
        self.nos = []
        self.contagem = {}

    def recurso(self, tipo, caminho):
        if caminho not in self.recursos:
            self.recursos[caminho] = (tipo, f"r{len(self.recursos) + 1}")
        return self.recursos[caminho][1]

    def cena(self, caminho):
        return self.recurso("PackedScene", caminho)

    def nome(self, base):
        self.contagem[base] = self.contagem.get(base, 0) + 1
        return f"{base}{self.contagem[base]}"

    def no(self, cabecalho, propriedades):
        self.nos.append((cabecalho, propriedades))

    def instancia(self, nome, pai, caminho, propriedades=()):
        self.no(f'[node name="{nome}" parent="{pai}" instance=ExtResource("{self.cena(caminho)}")]', list(propriedades))

    def texto(self, raiz, propriedades_raiz, sub_recursos):
        linhas = ["[gd_scene format=3]", ""]
        for caminho, (tipo, id_) in self.recursos.items():
            linhas.append(f'[ext_resource type="{tipo}" path="{caminho}" id="{id_}"]')
        linhas.append("")
        for sub in sub_recursos:
            linhas += [sub, ""]
        linhas.append(raiz)
        linhas += propriedades_raiz
        linhas.append("")
        for cabecalho, propriedades in self.nos:
            linhas.append(cabecalho)
            linhas += propriedades
            linhas.append("")
        return "\n".join(linhas)


def kit(pasta, nome):
    return f"res://cenas/cenario/dtec/{pasta}/{nome}.tscn"


PLACA = """[sub_resource type="StyleBoxFlat" id="Placa"]
bg_color = Color(0.06, 0.12, 0.2, 1)
border_width_bottom = 1
border_color = Color(0.24, 0.4, 0.6, 1)"""

PORTAS_PECA = {"porta": "dtec_porta", "trancada": "dtec_porta_trancada",
               "lacrada": "dtec_porta_lacrada", "central": "dtec_porta_central"}


def montar_sala(sala):
    m = Montagem()
    id_sala, largura, altura = sala["id"], sala["largura"], sala["altura"]
    funda = altura > 180
    m.cena("res://cenas/salas/modelo_sala.tscn")
    som_porta = m.recurso("AudioStream", "res://assets/audio/efeitos/objetos/porta_abrir.wav")

    # Parede do fundo: as peças da descrição, completadas com parede lisa.
    paredes = list(sala["paredes"])
    pecas = largura // PECA
    paredes += ["lisa"] * (pecas - len(paredes))
    portas = {p["peca"]: p for p in sala.get("portas", [])}
    for i, tipo in enumerate(paredes[:pecas]):
        if i in portas:
            tipo = PORTAS_PECA[portas[i]["tipo"]]
        else:
            tipo = f"dtec_{tipo}"
        m.instancia(f"Parede{i + 1:02d}", "Paredes", kit("paredes", tipo), [f"position = Vector2({i * PECA}, 0)"])
    m.instancia("PilarEsquerda", "Paredes", kit("paredes", "pilar_dtec"), ["position = Vector2(0, 0)"])
    m.instancia("PilarDireita", "Paredes", kit("paredes", "pilar_dtec"), [f"position = Vector2({largura - 16}, 0)"])

    # Placas com o nome da sala em cima de cada porta, e os letreiros.
    for i, porta in portas.items():
        if porta.get("placa"):
            x = i * PECA
            m.no(f'[node name="Placa{pascal(porta["id"])}" type="Label" parent="Paredes"]', [
                f"offset_left = {x + 6}.0", "offset_top = 26.0", f"offset_right = {x + 74}.0", "offset_bottom = 40.0",
                "theme_override_colors/font_color = Color(0.78, 0.88, 0.98, 1)",
                'theme_override_styles/normal = SubResource("Placa")',
                f'text = "{porta["placa"]}"', "horizontal_alignment = 1"])
    for k, (texto, x0, y0, x1, y1, tamanho) in enumerate(sala.get("letreiros", [])):
        m.no(f'[node name="Letreiro{k + 1}" type="Label" parent="Paredes"]', [
            f"offset_left = {x0}.0", f"offset_top = {y0}.0", f"offset_right = {x1}.0", f"offset_bottom = {y1}.0",
            "theme_override_colors/font_color = Color(0.62, 0.8, 1, 1)",
            f"theme_override_font_sizes/font_size = {tamanho}",
            f'text = "{texto}"', "horizontal_alignment = 1", "vertical_alignment = 1"])

    # Chão de perto: tipo padrão, trocado nas colunas pedidas.
    colunas = math.ceil(largura / CHAO)
    trocas = sala.get("chao_trocas", {})
    for c in range(colunas):
        tipo = trocas.get(c, sala.get("chao", "chao_dtec"))
        m.instancia(f"Chao{c + 1}", "Chao", kit("chao", tipo), [f"position = Vector2({c * CHAO}, 0)"])
    if funda:
        linhas = math.ceil((altura - 180) / FUNDO)
        trocas_fundo = sala.get("fundo_trocas", {})
        for c in range(colunas):
            for f in range(linhas):
                tipo = trocas_fundo.get((c, f), sala.get("fundo", "chao_dtec_fundo"))
                m.instancia(f"Fundo{c + 1}_{f + 1}", "Chao", kit("chao", tipo),
                            [f"position = Vector2({c * CHAO}, {180 + f * FUNDO})"])
        for f in range(math.ceil((altura - Y_CHAO) / FUNDO)):
            y = Y_CHAO + f * FUNDO
            m.instancia(f"LateralEsq{f + 1}", "Chao", kit("paredes", "dtec_lateral"), [f"position = Vector2(0, {y})"])
            m.instancia(f"LateralDir{f + 1}", "Chao", kit("paredes", "dtec_lateral"),
                        [f"position = Vector2({largura - 16}, {y})", "flip_h = true"])

    # Objetos (y-sort: a posição é o pé do objeto).
    for (nome, x, y, *resto) in sala.get("objetos", []):
        caminho = kit("objetos", nome) if nome in OBJETOS else nome
        props = [f"position = Vector2({x}, {y})"]
        if resto and resto[0]:
            props.append("espelhado = true")
        m.instancia(m.nome(pascal(os.path.basename(caminho).replace(".tscn", ""))), "Objetos", caminho, props)

    # Itens no chão.
    for (item, x, y) in sala.get("itens", []):
        if item == "pilha":
            m.instancia(m.nome("Pilha"), "Objetos", "res://cenas/itens/pilha_no_chao.tscn", [f"position = Vector2({x}, {y})"])
        else:
            id_item = m.recurso("Resource", f"res://dados/itens/{item}.tres")
            m.instancia(m.nome(pascal(item)), "Objetos", "res://cenas/itens/item_no_chao.tscn",
                        [f"position = Vector2({x}, {y})", f'item = ExtResource("{id_item}")'])

    # Luzes: as fluorescentes em cima de cada peça de luminária, mais as da descrição.
    for i, tipo in enumerate(paredes[:pecas]):
        if tipo == "luminaria" and i not in portas:
            m.instancia(m.nome("Luz"), "Luzes", "res://cenas/cenario/luzes/luz_tubo.tscn",
                        [f"position = Vector2({i * PECA + 40}, 34)", f"energy = {sala.get('energia_tubo', 0.85)}"])
    # Nas salas fundas, as luminárias da parede não chegam ao chão de baixo:
    # espalhamos luminárias numa grade (uma a cada ~240 px na largura e a
    # cada 200 px na altura), como no bunker.
    if funda and sala.get("luzes_chao", True):
        colunas_luz = max(1, round(largura / 240))
        for i in range(colunas_luz):
            for y in range(250, altura - 40, 200):
                x = round(largura * (i + 0.5) / colunas_luz)
                m.instancia(m.nome("Luz"), "Luzes", "res://cenas/cenario/luzes/luz_tubo.tscn",
                            [f"position = Vector2({x}, {y})", f"energy = {sala.get('energia_chao', 0.9)}"])
    for (cena_luz, x, y, *props) in sala.get("luzes", []):
        m.instancia(m.nome("Luz"), "Luzes", f"res://cenas/cenario/luzes/{cena_luz}.tscn", [f"position = Vector2({x}, {y})", *props])

    m.no('[node name="Escuridao" parent="."]', [f"color = Color{sala.get('escuridao', (0.26, 0.27, 0.34, 1))}"])
    if "gabriel" in sala:
        m.no('[node name="Gabriel" parent="Objetos"]', [f"position = Vector2{sala['gabriel']}"])

    # Portas.
    for i, porta in portas.items():
        x = i * PECA + (X_PORTA_CENTRAL if porta["tipo"] == "central" else X_PORTA)
        props = [f"position = Vector2({x}, {Y_PORTA})", f'id = "{porta["id"]}"']
        if porta["tipo"] == "lacrada":
            props += ["bloqueada = true", f'aviso_bloqueada = "{porta["aviso"]}"']
        else:
            if porta["tipo"] == "trancada":
                props.append("trancada = true")
            props += [f'cena_destino = "res://cenas/salas/dtec/{porta["destino"]}.tscn"',
                      f'porta_destino = "{porta["porta_destino"]}"', f'som_abrir = ExtResource("{som_porta}")']
        m.instancia(f"Porta_{porta['id']}", ".", "res://cenas/sistemas/porta.tscn", props)

    # Som: o zumbido do prédio em toda sala e, perto da máquina, o ronco grave dela.
    zumbido = m.recurso("AudioStream", "res://assets/audio/ambiente/bunker/bunker_zumbido.wav")
    m.no('[node name="Zumbido" type="AudioStreamPlayer" parent="."]', [
        f'stream = ExtResource("{zumbido}")', "volume_db = -14.0", "pitch_scale = 1.15", "autoplay = true", 'bus = &"Efeitos"'])
    for (x, y) in sala.get("ronco", []):
        m.no(f'[node name="{m.nome("Ronco")}" type="AudioStreamPlayer2D" parent="."]', [
            f'stream = ExtResource("{zumbido}")', f"position = Vector2({x}, {y})", "volume_db = 4.0",
            "pitch_scale = 0.5", "autoplay = true", "max_distance = 900.0", 'bus = &"Efeitos"'])

    raiz = f'[node name="{pascal(id_sala)}" instance=ExtResource("r1")]'
    props_raiz = [f'id = "dtec_{id_sala}"', f"largura = {largura}"]
    if funda:
        props_raiz += [f"altura = {altura}", f"chao_frente = {altura - 4}"]
    escrever(os.path.join(PASTA_SALAS, f"{id_sala}.tscn"), m.texto(raiz, props_raiz, [PLACA]))
    print(f"  sala: cenas/salas/dtec/{id_sala}.tscn ({largura} x {altura})")


# ---------------------------------------------------------------------------
# As salas
# ---------------------------------------------------------------------------
# paredes: uma palavra por peça de 80 px (sem o "dtec_"); as que faltam no
#          fim viram parede lisa. Onde há porta, a peça vem da porta.
# portas:  peca (índice da peça), tipo (porta, trancada, lacrada, central),
#          id, placa, e destino + porta_destino (ou o aviso, se lacrada).
# objetos: (nome, x, y[, espelhado]); itens: (item, x, y).
# luzes:   (cena em cenas/cenario/luzes, x, y, propriedades extras...).

ESCURO = (0.33, 0.34, 0.41, 1)
AVISO_LACRADA = "Lacrada. O leitor nem acende."

SALAS = [
    {
        "id": "recepcao", "largura": 640, "altura": 400, "gabriel": "(90, 320)",
        "paredes": ["cartaz", "lisa", "luminaria", "lisa", "porta", "terminal", "luminaria", "rachada"],
        "portas": [
            {"peca": 4, "tipo": "porta", "id": "recepcao_corredor", "placa": "LABORATÓRIOS",
             "destino": "corredor_norte", "porta_destino": "norte_recepcao"},
            {"peca": 0, "tipo": "lacrada", "id": "recepcao_saida", "placa": "SAÍDA",
             "aviso": "As portas da entrada estão travadas por fora."},
        ],
        "letreiros": [("DTEC", 90, 28, 230, 56, 16)],
        "objetos": [("balcao_recepcao", 300, 220), ("cadeira_escritorio", 280, 196), ("mesa_computador", 140, 170),
                    ("catraca", 380, 150), ("catraca", 420, 150), ("catraca", 460, 150), ("planta", 40, 140),
                    ("planta", 600, 370, True), ("caixas_lab", 540, 260), ("cadeira_escritorio", 120, 300, True)],
        "itens": [("pilha", 520, 330), ("lanterna", 200, 290)],
        "luzes": [("luz_emergencia", 560, 30, "energy = 0.5")],
        "escuridao": (0.32, 0.33, 0.4, 1),
    },
    {
        "id": "corredor_norte", "largura": 2400, "altura": 180,
        "paredes": ["lisa", "extintor", "porta", "luminaria", "vidro", "cartaz", "porta", "quadro", "luminaria",
                    "vidro", "porta", "canos", "luminaria", "armario", "lisa", "central", "painel", "luminaria",
                    "rachada", "terminal", "porta", "vidro", "luminaria", "extintor", "porta", "lisa", "luminaria",
                    "cartaz", "porta", "rachada"],
        "portas": [
            {"peca": 2, "tipo": "porta", "id": "norte_recepcao", "placa": "RECEPÇÃO",
             "destino": "recepcao", "porta_destino": "recepcao_corredor"},
            {"peca": 6, "tipo": "porta", "id": "norte_eletronica", "placa": "ELETRÔNICA",
             "destino": "lab_eletronica", "porta_destino": "eletronica_corredor"},
            {"peca": 10, "tipo": "porta", "id": "norte_informatica", "placa": "INFORMÁTICA",
             "destino": "lab_informatica", "porta_destino": "informatica_corredor"},
            {"peca": 15, "tipo": "central", "id": "norte_central", "placa": "LAB CENTRAL",
             "destino": "lab_central", "porta_destino": "central_norte"},
            {"peca": 20, "tipo": "trancada", "id": "norte_servidores", "placa": "SERVIDORES",
             "destino": "sala_servidores", "porta_destino": "servidores_corredor"},
            {"peca": 24, "tipo": "lacrada", "id": "norte_deposito", "placa": "DEPÓSITO", "aviso": AVISO_LACRADA},
            {"peca": 28, "tipo": "lacrada", "id": "norte_diretoria", "placa": "DIRETORIA", "aviso": AVISO_LACRADA},
        ],
        "chao_trocas": {9: "chao_dtec_faixa", 10: "chao_dtec_cabos"},
        "objetos": [("planta", 70, 140), ("caixas_lab", 700, 150), ("cilindros", 1050, 130), ("cadeira_escritorio", 1420, 160, True),
                    ("caixas_lab", 1800, 160, True), ("planta", 2340, 150, True), ("cilindros", 2100, 132)],
        "itens": [("pilha", 940, 160), ("clarao", 2020, 150)],
        "luzes": [("luz_maquina", 1240, 110, "scale = Vector2(3, 2.5)", "energy = 0.9"),
                  ("luz_emergencia", 1960, 30, "energy = 0.5")],
        "escuridao": ESCURO,
    },
    {
        "id": "lab_central", "largura": 960, "altura": 560, "gabriel": "(160, 200)",
        "paredes": ["painel", "porta", "canos", "luminaria", "tela_grande", "vidro", "vidro", "tela_grande",
                    "luminaria", "canos", "porta", "painel"],
        "portas": [
            {"peca": 1, "tipo": "porta", "id": "central_norte", "placa": "ALA NORTE",
             "destino": "corredor_norte", "porta_destino": "norte_central"},
            {"peca": 10, "tipo": "porta", "id": "central_sul", "placa": "ALA SUL",
             "destino": "corredor_sul", "porta_destino": "sul_central"},
        ],
        "chao": "chao_dtec_cabos",
        "fundo_trocas": {(3, 3): "chao_dtec_faixa_fundo", (4, 3): "chao_dtec_faixa_fundo",
                         (2, 2): "chao_dtec_cabos_fundo", (5, 2): "chao_dtec_cabos_fundo",
                         (2, 4): "chao_dtec_cabos_fundo", (5, 4): "chao_dtec_cabos_fundo"},
        "objetos": [("maquina", 480, 380), ("console", 210, 440), ("console", 750, 440, True),
                    ("cadeira_escritorio", 200, 470), ("cadeira_escritorio", 760, 470, True),
                    ("rack_dtec", 60, 250), ("rack_dtec", 90, 250), ("rack_dtec", 870, 250, True), ("rack_dtec", 900, 250, True),
                    ("cilindros", 300, 150), ("cilindros", 660, 150, True), ("caixas_lab", 120, 520), ("caixas_lab", 860, 530, True)],
        "itens": [("clarao", 480, 500)],
        "luzes": [("luz_maquina", 480, 300), ("luz_maquina", 480, 290, "scale = Vector2(3, 3)", "energy = 1.4", "periodo = 1.2"),
                  ("luz_fria", 160, 220, "energy = 0.4"), ("luz_fria", 800, 220, "energy = 0.4")],
        "ronco": [(480, 300)],
        "escuridao": (0.18, 0.19, 0.25, 1),
        "energia_tubo": 0.5, "energia_chao": 0.35,
    },
    {
        "id": "corredor_sul", "largura": 2400, "altura": 180,
        "paredes": ["rachada", "lisa", "porta", "luminaria", "extintor", "canos", "porta", "vidro", "luminaria",
                    "cartaz", "porta", "vidro", "luminaria", "quadro", "lisa", "central", "terminal", "luminaria",
                    "armario", "lisa", "porta", "tela_grande", "luminaria", "lisa", "porta", "extintor", "luminaria",
                    "rachada", "lisa", "cartaz"],
        "portas": [
            {"peca": 2, "tipo": "lacrada", "id": "sul_emergencia", "placa": "EMERGÊNCIA",
             "aviso": "Bloqueada. Do outro lado, só entulho."},
            {"peca": 6, "tipo": "porta", "id": "sul_quimica", "placa": "QUÍMICA",
             "destino": "lab_quimica", "porta_destino": "quimica_corredor"},
            {"peca": 10, "tipo": "trancada", "id": "sul_robotica", "placa": "ROBÓTICA",
             "destino": "lab_robotica", "porta_destino": "robotica_corredor"},
            {"peca": 15, "tipo": "central", "id": "sul_central", "placa": "LAB CENTRAL",
             "destino": "lab_central", "porta_destino": "central_sul"},
            {"peca": 20, "tipo": "porta", "id": "sul_controle", "placa": "CONTROLE",
             "destino": "sala_controle", "porta_destino": "controle_corredor"},
            {"peca": 24, "tipo": "lacrada", "id": "sul_arquivo", "placa": "ARQUIVO", "aviso": AVISO_LACRADA},
        ],
        "chao_trocas": {9: "chao_dtec_faixa", 10: "chao_dtec_cabos", 4: "chao_dtec_cabos"},
        "objetos": [("caixas_lab", 120, 150), ("planta", 400, 140), ("cilindros", 980, 132), ("caixas_lab", 1500, 160, True),
                    ("planta", 1880, 140, True), ("cadeira_escritorio", 2150, 165), ("caixas_lab", 2300, 150)],
        "itens": [("pilha", 1460, 165), ("pedra", 600, 160), ("pedra", 2200, 150)],
        "luzes": [("luz_maquina", 1240, 110, "scale = Vector2(3, 2.5)", "energy = 0.9"),
                  ("luz_emergencia", 200, 30, "energy = 0.6")],
        "escuridao": ESCURO,
    },
    {
        "id": "lab_eletronica", "largura": 480, "altura": 560,
        "paredes": ["porta", "painel", "luminaria", "quadro", "armario", "luminaria"],
        "portas": [{"peca": 0, "tipo": "porta", "id": "eletronica_corredor", "placa": "CORREDOR",
                    "destino": "corredor_norte", "porta_destino": "norte_eletronica"}],
        "objetos": [("bancada_eletronica", 250, 210), ("cadeira_escritorio", 230, 235), ("bancada_eletronica", 250, 320),
                    ("cadeira_escritorio", 270, 345, True), ("bancada_eletronica", 250, 430), ("cadeira_escritorio", 220, 455),
                    ("cilindros", 440, 160, True), ("caixas_lab", 70, 380), ("caixas_lab", 420, 520, True), ("planta", 40, 520)],
        "itens": [("pilha", 400, 260), ("clarao", 90, 470)],
        "escuridao": ESCURO,
    },
    {
        "id": "lab_informatica", "largura": 560, "altura": 560,
        "paredes": ["armario", "porta", "luminaria", "terminal", "quadro", "luminaria", "cartaz"],
        "portas": [{"peca": 1, "tipo": "porta", "id": "informatica_corredor", "placa": "CORREDOR",
                    "destino": "corredor_norte", "porta_destino": "norte_informatica"}],
        "objetos": [(n, x, y) for y in (210, 320, 430) for (n, x) in (("mesa_computador", 150), ("mesa_computador", 290), ("mesa_computador", 430))]
                   + [(n, x, y + 24, (x // 10) % 2 == 0) for y in (210, 320, 430) for (n, x) in (("cadeira_escritorio", 150), ("cadeira_escritorio", 290), ("cadeira_escritorio", 430))]
                   + [("planta", 520, 150, True), ("rack_dtec", 40, 260), ("caixas_lab", 500, 520)],
        "itens": [("notebook", 290, 360), ("pilha", 60, 480)],
        "escuridao": ESCURO,
    },
    {
        "id": "sala_servidores", "largura": 480, "altura": 480,
        "paredes": ["porta", "painel", "luminaria", "terminal", "painel", "luminaria"],
        "portas": [{"peca": 0, "tipo": "porta", "id": "servidores_corredor", "placa": "CORREDOR",
                    "destino": "corredor_norte", "porta_destino": "norte_servidores"}],
        "chao": "chao_dtec_elevado", "fundo": "chao_dtec_elevado_fundo",
        "objetos": [("rack_dtec", x, y) for y in (210, 320, 430) for x in (150, 176, 202, 280, 306, 332, 358)],
        "itens": [("pilha", 240, 260), ("pilha", 420, 380), ("clarao", 100, 440)],
        "luzes": [("luz_fria", 240, 260, "energy = 0.35", "color = Color(0.4, 1, 0.6, 1)"),
                  ("luz_fria", 240, 380, "energy = 0.35", "color = Color(0.4, 1, 0.6, 1)")],
        "escuridao": (0.22, 0.24, 0.29, 1),
        "energia_tubo": 0.6, "energia_chao": 0.45,
    },
    {
        "id": "lab_quimica", "largura": 400, "altura": 480,
        "paredes": ["porta", "canos", "luminaria", "armario", "canos"],
        "portas": [{"peca": 0, "tipo": "porta", "id": "quimica_corredor", "placa": "CORREDOR",
                    "destino": "corredor_sul", "porta_destino": "sul_quimica"}],
        "objetos": [("capela", 180, 140), ("capela", 300, 140), ("armario_quimico", 370, 150, True),
                    ("bancada_lab", 200, 280), ("bancada_lab", 200, 390), ("cilindros", 40, 220),
                    ("armario_quimico", 40, 400), ("cadeira_escritorio", 220, 305, True)],
        "itens": [("pilha", 330, 330)],
        "escuridao": ESCURO,
    },
    {
        "id": "lab_robotica", "largura": 560, "altura": 560,
        "paredes": ["porta", "painel", "luminaria", "quadro", "vidro", "luminaria", "cartaz"],
        "portas": [{"peca": 0, "tipo": "porta", "id": "robotica_corredor", "placa": "CORREDOR",
                    "destino": "corredor_sul", "porta_destino": "sul_robotica"}],
        "chao": "chao_dtec_cabos",
        "objetos": [("braco_robotico", 160, 220), ("braco_robotico", 400, 220, True), ("robo_desmontado", 280, 330),
                    ("robo_desmontado", 280, 450, True), ("braco_robotico", 470, 420, True), ("bancada_eletronica", 110, 400),
                    ("caixas_lab", 500, 160), ("cilindros", 40, 520), ("caixas_lab", 520, 520, True)],
        "itens": [("clarao", 200, 300), ("clarao", 420, 480), ("pilha", 60, 260)],
        "luzes": [("luz_emergencia", 280, 30, "energy = 0.6")],
        "escuridao": ESCURO,
    },
    {
        "id": "sala_controle", "largura": 560, "altura": 480,
        "paredes": ["porta", "tela_grande", "tela_grande", "luminaria", "vidro", "painel", "terminal"],
        "portas": [{"peca": 0, "tipo": "porta", "id": "controle_corredor", "placa": "CORREDOR",
                    "destino": "corredor_sul", "porta_destino": "sul_controle"}],
        "objetos": [("console", 160, 220), ("console", 300, 220), ("console", 440, 220, True),
                    ("cadeira_escritorio", 160, 245), ("cadeira_escritorio", 300, 245, True), ("cadeira_escritorio", 440, 245),
                    ("mesa_computador", 200, 360), ("mesa_computador", 380, 360), ("planta", 520, 440, True), ("rack_dtec", 40, 300)],
        "itens": [("pilha", 300, 420)],
        "luzes": [("luz_fria", 160, 60, "energy = 0.8", "color = Color(0.4, 0.95, 1, 1)"),
                  ("luz_fria", 400, 70, "energy = 0.6", "color = Color(0.4, 0.95, 1, 1)"),
                  ("luz_fria", 300, 230, "energy = 0.6", "color = Color(0.4, 0.95, 1, 1)")],
        "escuridao": ESCURO,
    },
]


def main():
    montar_kit()
    print("  kit: cenas/cenario/dtec/")
    for sala in SALAS:
        montar_sala(sala)


if __name__ == "__main__":
    main()
