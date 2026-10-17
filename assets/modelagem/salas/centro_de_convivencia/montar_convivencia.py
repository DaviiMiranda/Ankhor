# montar_convivencia.py — monta as cenas do Godot da fase CENTRO DE
# CONVIVÊNCIA (docs/fases/centro_de_convivencia.md): as peças do kit da praça
# (cenas/cenario/praca/) e as salas da fase (cenas/salas/centro_de_convivencia/).
#
# Como rodar (Python 3, depois dos geradores de sprites):
#
#   python assets/modelagem/cenario/gerar_porta_restaurante.py
#   python assets/modelagem/cenario/gerar_praca.py
#   python assets/modelagem/cenario/gerar_restaurantes.py
#   python assets/modelagem/salas/centro_de_convivencia/montar_convivencia.py
#
# ATENÇÃO: este script é a montagem das cenas. Ele sobrescreve as cenas das
# salas. Depois que alguém ajustar uma sala no editor do Godot, não rode de
# novo sem antes passar o ajuste para a descrição da sala aqui embaixo.
#
# Diferente do Bloco de salas e do DTEC (que montam a sala com peças de parede
# de 80 px e de chão de 128 px), aqui cada sala tem um FUNDO PRONTO: uma
# imagem só com a parede e o piso. A praça tem formato de arco, e cada
# restaurante tem a sua decoração. O que o Godot ainda monta por cima do fundo:
#   - as portas de vidro (a folha que corre) e os letreiros de neon;
#   - os objetos (mesas, balcões...), com a "pegada" de colisão no chão;
#   - na praça, as colisões do arco: uma caixa por coluna de 80 px, do topo da
#     sala até a altura em que a parede dela encosta no chão;
#   - no mezanino (segundo andar), além disso, uma caixa por coluna na BEIRADA
#     da laje (o corrimão), e o sprite do corrimão na camada Frente, na frente
#     do Gabriel;
#   - a tela animada do cinema.

import os
import sys

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "..", ".."))
PASTA_KIT_PRACA = os.path.join(PASTA_PROJETO, "cenas", "cenario", "praca")
PASTA_SALAS = os.path.join(PASTA_PROJETO, "cenas", "salas", "centro_de_convivencia")
PASTA_LETREIROS = os.path.join(PASTA_PROJETO, "assets", "sprites", "cenario", "praca", "letreiros")
sys.path.insert(0, os.path.join(PASTA_PROJETO, "assets", "modelagem", "cenario"))

import gerar_praca_base as base  # noqa: E402
import gerar_praca_objetos as gerador_objetos  # noqa: E402
import gerar_andar2_objetos as gerador_objetos2  # noqa: E402

sys.path.insert(0, PASTA_SCRIPT)
import salas_convivencia  # noqa: E402

PECA = base.PECA
X_PORTA = 41
RES_PRACA = "res://assets/sprites/cenario/praca"
COR_DA_LUZ = {
    "ciano": "Color(0.45, 0.9, 1, 1)",
    "ambar": "Color(1, 0.7, 0.3, 1)",
    "verde": "Color(0.35, 1, 0.65, 1)",
    "vermelho": "Color(1, 0.4, 0.3, 1)",
    "magenta": "Color(1, 0.4, 0.85, 1)",
    "violeta": "Color(0.7, 0.5, 1, 1)",
    "azul": "Color(0.4, 0.62, 1, 1)",
    "limao": "Color(0.85, 1, 0.3, 1)",
}
MARCA_ENERGIA = "convivencia_energia"

LETREIROS = {
    "letreiro_loja_1": ("ambar", 240, 28),
    "letreiro_loja_2": ("verde", 240, 28),
    "letreiro_loja_3": ("vermelho", 240, 28),
    "letreiro_loja_4": ("magenta", 240, 28),
    "letreiro_entrada": ("ciano", 240, 28),
    "letreiro_grafica": ("limao", 240, 28),
    "letreiro_loja_uni": ("azul", 240, 28),
    "letreiro_cinema": ("violeta", 240, 28),
    "letreiro_mezanino": ("ciano", 240, 28),
}


def pascal(nome):
    return "".join(parte.capitalize() for parte in nome.split("_"))


def escrever(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as arquivo:
        arquivo.write(texto)


# ---------------------------------------------------------------------------
# Peças do kit
# ---------------------------------------------------------------------------


def cena_porta(cor):
    return f"""[gd_scene format=3]

[ext_resource type="SpriteFrames" path="{RES_PRACA}/portas/porta_{cor}_quadros.tres" id="1_quadros"]
[ext_resource type="Script" path="res://scripts/sistemas/folha_porta.gd" id="2_script"]
[ext_resource type="AudioStream" path="res://assets/audio/efeitos/objetos/porta_restaurante.wav" id="3_som"]

[node name="Porta{pascal(cor)}" type="Node2D"]

[node name="Folha" type="AnimatedSprite2D" parent="." groups=["folhas_de_porta"]]
position = Vector2(0, 24)
sprite_frames = ExtResource("1_quadros")
animation = &"abrir"
centered = false
script = ExtResource("2_script")
som_abrir = ExtResource("3_som")
"""


def cena_letreiro(nome, cor, largura, altura):
    luz = COR_DA_LUZ[cor]
    return f"""[gd_scene format=3]

[ext_resource type="Script" path="res://scripts/sistemas/visivel_com_marca.gd" id="1_marca"]
[ext_resource type="Texture2D" path="{RES_PRACA}/letreiros/{nome}.png" id="2_apagado"]
[ext_resource type="Texture2D" path="{RES_PRACA}/letreiros/{nome}_aceso.png" id="3_aceso"]
[ext_resource type="Texture2D" uid="uid://dtfpmqdy5b1wa" path="res://assets/sprites/cenario/luzes/luz.png" id="4_luz"]

[node name="{pascal(nome)}" type="Sprite2D"]
texture = ExtResource("2_apagado")
centered = false

[node name="Acende" type="Node2D" parent="."]
script = ExtResource("1_marca")
marca = "{MARCA_ENERGIA}"

[node name="Camada" type="PointLight2D" parent="Acende"]
position = Vector2({largura // 2}, {altura // 2 + 2})
energy = 2.2
range_item_cull_mask = 1
texture = ExtResource("3_aceso")

[node name="Luz" type="PointLight2D" parent="Acende"]
position = Vector2({largura // 2}, {altura + 14})
color = {luz}
energy = 0.7
range_item_cull_mask = 3
texture = ExtResource("4_luz")
texture_scale = {round(largura / 120.0, 2)}
"""


# Luzes que cada objeto leva junto: (x, y, cor, energia, escala), com o ponto
# (x, y) em relação ao pé do objeto. O brilho de verdade vem do Godot.
LUZES_DOS_OBJETOS = {
    "poste_luz": [(0, -82, "Color(1, 0.78, 0.45, 1)", 0.95, 2.4)],
    "mesa_holo": [(0, -40, "Color(0.45, 0.9, 1, 1)", 0.3, 1.0)],
    "holograma_central": [(0, -62, "Color(0.42, 0.95, 1, 1)", 1.1, 4.0)],
    "guarda_sol_holo": [(0, -64, "Color(0.45, 0.9, 1, 1)", 0.4, 1.6)],
    "totem_pedidos": [(0, -32, "Color(0.45, 0.9, 1, 1)", 0.35, 0.9)],
    "vaso_planta": [(0, -30, "Color(0.4, 1, 0.8, 1)", 0.3, 0.8)],
    "arvore_cupula": [(0, -110, "Color(0.4, 1, 0.8, 1)", 0.45, 2.6)],
    "balcao_tapioca": [(-22, -34, "Color(1, 0.7, 0.3, 1)", 0.8, 1.6)],
    "maquina_cafe": [(0, -34, "Color(0.45, 0.9, 1, 1)", 0.3, 0.8)],
    "estufa_salgados": [(0, -26, "Color(1, 0.7, 0.3, 1)", 0.5, 1.0)],
    "bufe": [(0, -30, "Color(0.35, 1, 0.65, 1)", 0.6, 2.2)],
    "mesa_vidro": [(0, -24, "Color(0.35, 1, 0.65, 1)", 0.25, 0.8)],
    "tanque_cripto": [(0, -40, "Color(0.5, 0.9, 1, 1)", 0.6, 1.2)],
    "forno_plasma": [(0, -26, "Color(1, 0.45, 0.2, 1)", 1.0, 2.0)],
    "grelha_solar": [(0, -50, "Color(1, 0.4, 0.85, 1)", 0.9, 2.2)],
    "balcao_bar": [(0, -30, "Color(1, 0.4, 0.85, 1)", 0.6, 2.2)],
    "banqueta_alta": [],
    "maquina_venda": [(0, -30, "Color(0.45, 0.9, 1, 1)", 0.4, 1.0)],
    "diretorio_holo": [(0, -40, "Color(0.4, 0.62, 1, 1)", 0.45, 1.2)],
    "jardineira": [(0, -24, "Color(0.4, 1, 0.8, 1)", 0.35, 1.4)],
    "luminaria_chao": [(0, -60, "Color(0.6, 0.95, 1, 1)", 0.8, 2.0)],
    "balcao_caixa_uni": [(0, -30, "Color(0.4, 0.62, 1, 1)", 0.5, 1.6)],
    "impressora_3d": [(0, -24, "Color(0.85, 1, 0.3, 1)", 0.5, 1.0)],
    "plotter_grande": [(0, -30, "Color(0.85, 1, 0.3, 1)", 0.4, 1.4)],
    "balcao_grafica": [(-30, -34, "Color(0.85, 1, 0.3, 1)", 0.5, 1.4)],
    "balcao_pipoca": [(-30, -30, "Color(1, 0.7, 0.3, 1)", 0.9, 1.8)],
    "bilheteria_balcao": [(0, -30, "Color(0.7, 0.5, 1, 1)", 0.6, 1.4)],
    "standee_filme": [(0, -34, "Color(0.7, 0.5, 1, 1)", 0.35, 1.0)],
}
OBJETOS_SEM_COLISAO = ("cacos_louca", "elevador_carga")


def cena_objeto(nome, px, py, larg, alt):
    luzes = LUZES_DOS_OBJETOS.get(nome, [])
    texto = f"""[gd_scene format=3]

[ext_resource type="Script" path="res://scripts/cenario/objeto_cenario.gd" id="1_objeto"]
[ext_resource type="Texture2D" path="{RES_PRACA}/objetos/{nome}.png" id="2_sprite"]
"""
    if luzes:
        texto += '[ext_resource type="Texture2D" uid="uid://dtfpmqdy5b1wa" path="res://assets/sprites/cenario/luzes/luz.png" id="3_luz"]\n'
    if nome == "holograma_central":
        texto += '[ext_resource type="Script" path="res://scripts/cenario/luz_pulsante.gd" id="4_pulsante"]\n'
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
    for k, (x, y, cor, energia, escala) in enumerate(luzes):
        texto += f"""
[node name="Luz{k + 1}" type="PointLight2D" parent="."]
position = Vector2({x}, {y})
color = {cor}
energy = {energia}
texture = ExtResource("3_luz")
texture_scale = {escala}
"""
        if nome == "holograma_central":
            texto += 'script = ExtResource("4_pulsante")\nperiodo = 3.2\nvariacao = 0.25\n'
    return texto


def cena_decal(nome, largura, altura):
    return f"""[gd_scene format=3]

[ext_resource type="Texture2D" path="{RES_PRACA}/objetos/{nome}.png" id="1_tex"]

[node name="{pascal(nome)}" type="Sprite2D"]
texture = ExtResource("1_tex")
"""


def montar_objetos():
    """Uma cena por objeto (cenas/cenario/praca/objetos/). O pé de cada um e a
    pegada vêm do próprio gerador de sprites."""
    caminhos = {}
    for nome, (funcao, pegada) in {**gerador_objetos.OBJETOS, **gerador_objetos2.OBJETOS}.items():
        img, px, py = funcao()
        escrever(os.path.join(PASTA_KIT_PRACA, "objetos", f"{nome}.tscn"), cena_objeto(nome, px, py, pegada[0], pegada[1]))
        caminhos[nome] = f"res://cenas/cenario/praca/objetos/{nome}.tscn"
    for nome in ("cacos_louca",):
        img, _, _ = gerador_objetos.ENFEITES[nome]()
        escrever(os.path.join(PASTA_KIT_PRACA, "objetos", f"{nome}.tscn"), cena_decal(nome, img.w, img.h))
        caminhos[nome] = f"res://cenas/cenario/praca/objetos/{nome}.tscn"
    return caminhos


def montar_kit():
    for cor in ("ambar", "verde", "vermelho", "magenta", "ciano", "azul", "limao", "violeta"):
        escrever(os.path.join(PASTA_KIT_PRACA, f"porta_{cor}.tscn"), cena_porta(cor))
    for nome, (cor, largura, altura) in LETREIROS.items():
        if os.path.exists(os.path.join(PASTA_LETREIROS, f"{nome}_aceso.png")):
            escrever(os.path.join(PASTA_KIT_PRACA, f"{nome}.tscn"), cena_letreiro(nome, cor, largura, altura))
    print("  kit: cenas/cenario/praca/")


# ---------------------------------------------------------------------------
# Montagem de uma sala
# ---------------------------------------------------------------------------


class Montagem:
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

    def nome(self, base_nome):
        self.contagem[base_nome] = self.contagem.get(base_nome, 0) + 1
        return f"{base_nome}{self.contagem[base_nome]}"

    def no(self, cabecalho, propriedades):
        self.nos.append((cabecalho, propriedades))

    def instancia(self, nome, pai, caminho, propriedades=()):
        self.no(f'[node name="{nome}" parent="{pai}" instance=ExtResource("{self.cena(caminho)}")]', list(propriedades))

    def texto(self, raiz, propriedades_raiz, sub_recursos, rodape=()):
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
        for linha in rodape:
            linhas.append(linha)
        return "\n".join(linhas)


def montar_sala(sala, objetos):
    m = Montagem()
    id_sala, largura, altura = sala["id"], sala["largura"], sala["altura"]
    m.cena("res://cenas/salas/modelo_sala.tscn")
    m.no('[node name="Ceu" parent="."]', ["visible = false"])
    fundo = m.recurso("Texture2D", f"{RES_PRACA}/{sala['fundo']}.png")
    m.no('[node name="Fundo" type="Sprite2D" parent="Chao"]', [f'texture = ExtResource("{fundo}")', "centered = false"])
    sub_recursos = []
    rodape = []

    escuridao = sala.get("escuridao", (0.22, 0.24, 0.36, 1))
    luz_png = m.recurso("Texture2D", f"{RES_PRACA}/{sala['fundo']}_luz.png")
    camada = [f"position = Vector2({largura // 2}, {altura // 2})", f'texture = ExtResource("{luz_png}")',
              f"energy = {sala.get('energia_do_brilho', 1.3)}", "range_item_cull_mask = 1"]
    if sala.get("acende_com_energia"):
        scr_marca = m.recurso("Script", "res://scripts/sistemas/visivel_com_marca.gd")
        m.no('[node name="Brilho" type="Node2D" parent="Chao"]', [f'script = ExtResource("{scr_marca}")', f'marca = "{MARCA_ENERGIA}"'])
        m.no('[node name="Camada" type="PointLight2D" parent="Chao/Brilho"]', camada)
    else:
        m.no('[node name="Brilho" type="PointLight2D" parent="Chao"]', camada)

    for porta in sala.get("portas", []):
        if porta.get("cor"):
            m.instancia(f"Folha{pascal(porta['id'])}", "Chao", f"res://cenas/cenario/praca/porta_{porta['cor']}.tscn",
                        [f"position = Vector2({porta['coluna'] * PECA}, {porta['y_peca']})"])

    for (nome_decal, x, y) in sala.get("decais", []):
        m.instancia(m.nome(pascal(nome_decal)), "Chao", objetos[nome_decal], [f"position = Vector2({x}, {y})"])

    for (nome_letreiro, x, y) in sala.get("letreiros", []):
        if os.path.exists(os.path.join(PASTA_KIT_PRACA, f"{nome_letreiro}.tscn")):
            m.instancia(pascal(nome_letreiro), "Chao", f"res://cenas/cenario/praca/{nome_letreiro}.tscn", [f"position = Vector2({x}, {y})"])

    if sala.get("arco"):
        m.no('[node name="LimitesArco" type="StaticBody2D" parent="."]', ["collision_layer = 9"])
        for c in range(base.COLUNAS_PRACA):
            topo, baixo = -40, base.y_base(c) + 8
            sub_id = f"CaixaArco{c}"
            sub_recursos.append(f'[sub_resource type="RectangleShape2D" id="{sub_id}"]\nsize = Vector2({PECA}, {baixo - topo})')
            m.no(f'[node name="Coluna{c}" type="CollisionShape2D" parent="LimitesArco"]',
                 [f"position = Vector2({c * PECA + PECA // 2}, {(topo + baixo) // 2})", f'shape = SubResource("{sub_id}")'])
        if sala.get("balcao"):
            for c in range(base.COLUNAS_PRACA):
                topo, baixo = base.y_frente(c) - 4, altura + 40
                sub_id = f"CaixaBeirada{c}"
                sub_recursos.append(f'[sub_resource type="RectangleShape2D" id="{sub_id}"]\nsize = Vector2({PECA}, {baixo - topo})')
                m.no(f'[node name="Beirada{c}" type="CollisionShape2D" parent="LimitesArco"]',
                     [f"position = Vector2({c * PECA + PECA // 2}, {(topo + baixo) // 2})", f'shape = SubResource("{sub_id}")'])

    if sala.get("corrimao"):
        corrimao = m.recurso("Texture2D", f"{RES_PRACA}/{sala['corrimao']}.png")
        m.no('[node name="Corrimao" type="Sprite2D" parent="Frente"]', [f'texture = ExtResource("{corrimao}")', "centered = false"])

    for (nome_animado, x, y, animacao) in sala.get("animados", []):
        quadros = m.recurso("SpriteFrames", f"{RES_PRACA}/objetos/{nome_animado}_quadros.tres")
        m.no(f'[node name="{pascal(nome_animado)}" type="AnimatedSprite2D" parent="Chao"]',
             [f"position = Vector2({x}, {y})", f'sprite_frames = ExtResource("{quadros}")', f'animation = &"{animacao}"', "autoplay = " + f'"{animacao}"', "centered = false"])
        scr_tremula = m.recurso("Script", "res://scripts/salas/luz_tremula.gd")
        tex_luz = m.recurso("Texture2D", "res://assets/sprites/cenario/luzes/luz.png")
        m.no(f'[node name="Luz{pascal(nome_animado)}" type="PointLight2D" parent="Chao"]',
             [f"position = Vector2({x + 115}, {y + 90})", 'color = Color(0.82, 0.88, 1, 1)', "energy = 0.9", f'texture = ExtResource("{tex_luz}")',
              "texture_scale = 5.0", f'script = ExtResource("{scr_tremula}")', "tremor = 0.25", "piscadas_por_segundo = 0.6"])

    for (nome, x, y, *resto) in sala.get("objetos", []):
        props = [f"position = Vector2({x}, {y})"]
        if resto and resto[0]:
            props.append("espelhado = true")
        m.instancia(m.nome(pascal(nome)), "Objetos", objetos[nome], props)

    for (item, x, y) in sala.get("itens", []):
        if item == "pilha":
            m.instancia(m.nome("Pilha"), "Objetos", "res://cenas/itens/pilha_no_chao.tscn", [f"position = Vector2({x}, {y})"])
        else:
            id_item = m.recurso("Resource", f"res://dados/itens/{item}.tres")
            m.instancia(m.nome(pascal(item)), "Objetos", "res://cenas/itens/item_no_chao.tscn",
                        [f"position = Vector2({x}, {y})", f'item = ExtResource("{id_item}")'])

    for (doc, x, y, acao) in sala.get("documentos", []):
        id_doc = m.recurso("Resource", f"res://dados/documentos/{doc}.tres")
        m.instancia(m.nome("Documento"), "Objetos", "res://cenas/itens/documento_no_mundo.tscn",
                    [f"position = Vector2({x}, {y})", f'texto_acao = "{acao}"', f'documento = ExtResource("{id_doc}")', "altura_aviso = 52.0"])

    for (x, y) in sala.get("nichos", []):
        m.instancia(m.nome("Nicho"), "Objetos", "res://cenas/sistemas/nicho_esconderijo.tscn", [f"position = Vector2({x}, {y})"])

    for (x, y, codigo, item, quantidade, marca_cofre, aviso) in sala.get("cofres", []):
        id_item = m.recurso("Resource", f"res://dados/itens/{item}.tres")
        m.instancia(m.nome("Cofre"), "Objetos", "res://cenas/sistemas/cofre.tscn",
                    [f"position = Vector2({x}, {y})", f'codigo = "{codigo}"', f'marca = "{marca_cofre}"',
                     f'item_ao_abrir = ExtResource("{id_item}")', f"quantidade = {quantidade}", f'aviso_aberto = "{aviso}"'])

    if sala.get("checkpoint"):
        id_cp, x_cp, y_cp = sala["checkpoint"]
        m.instancia("Checkpoint", "Objetos", "res://cenas/sistemas/checkpoint.tscn",
                    [f"position = Vector2({x_cp}, {y_cp})", f'id = "{id_cp}"'])

    if sala.get("painel_comutacao"):
        x_pc, y_pc = sala["painel_comutacao"]
        m.instancia("PainelComutacao", "Objetos", "res://cenas/sistemas/painel_comutacao.tscn", [f"position = Vector2({x_pc}, {y_pc})"])

    for (cena_luz, x, y, *props) in sala.get("luzes", []):
        m.instancia(m.nome("Luz"), "Luzes", f"res://cenas/cenario/luzes/{cena_luz}.tscn", [f"position = Vector2({x}, {y})", *props])

    if sala.get("holofotes"):
        scr_vcm = m.recurso("Script", "res://scripts/sistemas/visivel_com_marca.gd")
        m.no('[node name="HolofotesPerimetrais" type="Node2D" parent="."]', [
            f'script = ExtResource("{scr_vcm}")', f'marca = "{MARCA_ENERGIA}"', "revela_quem_passa = true"])
        for idx, (hx, hy) in enumerate(sala["holofotes"]):
            m.instancia(f"Holofote{idx + 1}", "HolofotesPerimetrais", "res://cenas/cenario/luzes/luz_fria.tscn",
                        [f"position = Vector2({hx}, {hy})", "scale = Vector2(2.2, 2.0)", "color = Color(0.85, 0.95, 1, 1)", "energy = 1.15"])

    m.no('[node name="Escuridao" parent="."]', [f"color = Color{escuridao}"])
    if "gabriel" in sala:
        m.no('[node name="Gabriel" parent="Objetos"]', [f"position = Vector2{sala['gabriel']}"])

    if sala.get("comporta"):
        c = sala["comporta"]
        tex = m.recurso("Texture2D", f"{RES_PRACA}/objetos/{c['textura']}.png")
        m.instancia("ComportaCarga", "Objetos", "res://cenas/sistemas/grade_seguranca.tscn",
                    [f"position = Vector2({c['x']}, {c['y']})", f'marca = "{MARCA_ENERGIA}"'])
        m.no('[node name="Grade" parent="Objetos/ComportaCarga" index="0"]', [f'texture = ExtResource("{tex}")'])

    for porta in sala.get("portas", []):
        props = [f"position = Vector2({porta['x']}, {porta['y']})", f'id = "{porta["id"]}"']
        if porta.get("som"):
            som = m.recurso("AudioStream", f"res://assets/audio/efeitos/objetos/{porta['som']}.wav")
            props.append(f'som_abrir = ExtResource("{som}")')
        if porta.get("liberada_por"):
            props += [f'liberada_por = "{porta["liberada_por"]}"', f'aviso_bloqueada = "{porta["aviso"]}"']
        if porta.get("bloqueada"):
            props += ["bloqueada = true", f'aviso_bloqueada = "{porta["aviso"]}"']
        else:
            props += [f'cena_destino = "res://cenas/salas/centro_de_convivencia/{porta["destino"]}.tscn"',
                      f'porta_destino = "{porta["porta_destino"]}"']
        m.instancia(f"Porta_{porta['id']}", ".", "res://cenas/sistemas/porta.tscn", props)

    rodape.append('[editable path="Ceu"]')
    for idx, (trans_id, gx, gy, marca_req) in enumerate(sala.get("transmissoes", [])):
        sub_id = f"AreaTransmissao{idx + 1}"
        sub_recursos.append(f'[sub_resource type="CircleShape2D" id="{sub_id}"]\nradius = 65.0')
        res_tr = m.recurso("Resource", f"res://dados/transmissoes/{trans_id}.tres")
        nome_g = f"GatilhoTransmissao{idx + 1}"
        props_g = [f"position = Vector2({gx}, {gy})", f'transmissao = ExtResource("{res_tr}")']
        if marca_req:
            props_g.append(f'requer_marca = "{marca_req}"')
        m.instancia(nome_g, "Objetos", "res://cenas/sistemas/gatilho_transmissao.tscn", props_g)
        m.no(f'[node name="Area" parent="Objetos/{nome_g}" index="0"]', [f'shape = SubResource("{sub_id}")'])
        rodape.append(f'[editable path="Objetos/{nome_g}"]')

    if sala.get("robos"):
        for r_idx, r in enumerate(sala["robos"]):
            cena_robo = f"res://cenas/personagens/robo_{r['tipo']}.tscn"
            nome_r = f"{pascal(r['tipo'])}{r_idx + 1}"
            nome_rota = f"Rota{nome_r}"
            props_r = [f"position = Vector2{r['pos']}", f'rota = NodePath("../../{nome_rota}")']
            if r.get("rota_energia"):
                nome_rota_e = f"Rota{nome_r}Energia"
                props_r += [f'rota_com_marca = NodePath("../../{nome_rota_e}")', f'marca_da_rota = "{MARCA_ENERGIA}"']
            if r["tipo"] == "sentinela":
                props_r.append("bipa_antes_de_virar = true")
            m.instancia(nome_r, "Objetos", cena_robo, props_r)
            m.no(f'[node name="{nome_rota}" type="Node2D" parent="."]', [])
            for p_idx, pt in enumerate(r["rota"]):
                m.no(f'[node name="Ponto{p_idx + 1}" type="Marker2D" parent="{nome_rota}"]', [f"position = Vector2{pt}"])
            if r.get("rota_energia"):
                nome_rota_e = f"Rota{nome_r}Energia"
                m.no(f'[node name="{nome_rota_e}" type="Node2D" parent="."]', [])
                for p_idx, pt in enumerate(r["rota_energia"]):
                    m.no(f'[node name="Ponto{p_idx + 1}" type="Marker2D" parent="{nome_rota_e}"]', [f"position = Vector2{pt}"])
        scr_robos = m.recurso("Script", "res://scripts/salas/robos_da_sala.gd")
        m.no('[node name="RobosDaSala" type="Node" parent="."]', [f'script = ExtResource("{scr_robos}")'])

    for z_idx, (zx, zy, zw, zh, fator, nome_piso) in enumerate(sala.get("zonas_piso", [])):
        scr_zona = m.recurso("Script", "res://scripts/sistemas/zona_de_piso.gd")
        m.no(f'[node name="ZonaPiso{z_idx + 1}" type="Node2D" parent="."]', [
            f"position = Vector2({zx}, {zy})", f'script = ExtResource("{scr_zona}")',
            f"tamanho = Vector2({zw}, {zh})", f"fator_ruido = {fator}", f'nome_piso = "{nome_piso}"'])

    m.instancia("MusicaFase", ".", "res://cenas/sistemas/musica_fase.tscn", [])

    raiz = f'[node name="{pascal(id_sala)}" instance=ExtResource("r1")]'
    props_raiz = [f'id = "conv_{id_sala}"', f"largura = {largura}"]
    if altura > 180:
        props_raiz += [f"altura = {altura}", f"chao_frente = {altura - 4}"]
    escrever(os.path.join(PASTA_SALAS, f"{id_sala}.tscn"), m.texto(raiz, props_raiz, sub_recursos, rodape))
    print(f"  sala: cenas/salas/centro_de_convivencia/{id_sala}.tscn ({largura} x {altura})")


def montar_fim_convivencia():
    texto = """[gd_scene format=3]

[ext_resource type="PackedScene" path="res://cenas/sistemas/saida_fase.tscn" id="1_saida"]

[node name="FimDaConvivencia" type="Node2D"]

[node name="Fundo" type="ColorRect" parent="."]
offset_right = 320.0
offset_bottom = 180.0
color = Color(0, 0, 0, 1)

[node name="SaidaFase" parent="." instance=ExtResource("1_saida")]
cena_destino = "res://cenas/salas/bunker/entrada.tscn"
sair_ao_carregar = true

[node name="Titulo" parent="SaidaFase/Tela" index="1"]
text = "VOCÊ DESCEU PELO ELEVADOR DE CARGA"

[node name="Subtitulo" parent="SaidaFase/Tela/Titulo" index="0"]
text = "Próxima fase: o Bunker"
"""
    escrever(os.path.join(PASTA_SALAS, "fim_da_convivencia.tscn"), texto)
    print("  sala: cenas/salas/centro_de_convivencia/fim_da_convivencia.tscn")


# ---------------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------------


def main():
    montar_kit()
    objetos = montar_objetos()
    for sala in salas_convivencia.SALAS:
        montar_sala(sala, objetos)
    montar_fim_convivencia()


if __name__ == "__main__":
    main()
