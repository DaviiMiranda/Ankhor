# montar_escritorio.py — monta as cenas do Godot da ALA DO ESCRITÓRIO, a
# mini fase do Zane no fim do Labirinto (docs/fases/labirinto.md, seção 5.1),
# e as cenas das peças do kit do escritório.
#
# Como rodar (Python 3, depois do gerar_escritorio.py):
#
#   python assets/modelagem/cenario/gerar_escritorio.py
#   python assets/modelagem/salas/labirinto/montar_escritorio.py
#
# ATENÇÃO: este script sobrescreve as quatro salas. Depois que alguém ajustar
# uma delas no editor do Godot, passe o ajuste para a descrição da sala aqui
# embaixo antes de rodar de novo.
#
# A planta (vista de cima; a parede do fundo é a de cima):
#
#              ARQUIVO          REUNIÕES         SEGURANÇA
#            (Rastreador)      (Mariposa)       (Sentinela)
#            ordenar pastas    código 1985      painel de chaves
#                 |                |                 |
#   +--duto--[porta]----------[porta]----------[porta]----------[RESTRITA]--+
#   |  Zane                                                     3 lâmpadas |
#   |        [cadeiras] [cadeiras]     [cadeiras] [cadeiras]     balcão    |
#   |        [cadeiras] [cadeiras]     [cadeiras] [cadeiras]     (nicho)   |
#   |        [cadeiras] [cadeiras]     [cadeiras] [cadeiras]               |
#   |              a Ronda dá a volta nas cadeiras                         |
#   +------------------------------------ RECEPÇÃO -------------------------+
#
# Cada sala solta uma trava (uma marca no Progresso) e acende uma lâmpada em
# cima da porta restrita. Com as três, a porta leva à câmara selada.
#
# As regras de montagem são as das salas fundas do bunker
# (montar_salas_bunker.py): parede do fundo em peças de 80 px com um pilar
# de 16 px em cada ponta, chão de perto em peças de 128 px, o chão de fundo
# em peças de 128 x 64 a partir de y = 180, as paredes laterais de 16 px a
# partir de y = 112 e cada porta em x = (x da peça) + 41, y = 124.
#
# Os móveis que tapam a visão dos robôs e o caminho deles (arquivos,
# cadeiras, balcão, mesas) ficam na camada 1 + 8 = 9: a camada 8 é a das
# paredes, que o raio de visão e a grade do A* dos robôs consultam.

import math
import os

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "..", ".."))
PASTA_SALAS = os.path.join(PASTA_PROJETO, "cenas", "salas", "labirinto", "escritorio")
PASTA_KIT = os.path.join(PASTA_PROJETO, "cenas", "cenario", "escritorio")

PECA, CHAO, FUNDO, Y_CHAO = 80, 128, 64, 112
ALTURA = 360
KIT = "res://cenas/cenario/escritorio"
SPRITES = "res://assets/sprites/cenario/escritorio"
SALAS = "res://cenas/salas/labirinto/escritorio"
CAMADA_BARREIRA = 9
YA_PORTA = 44

# Pés, pegadas e se o móvel é barreira (os números que o
# gerar_escritorio.py imprime).
OBJETOS = {
    "cadeiras_espera": ((33, 28), (62, 6), True),
    "cadeiras_espera_quebrada": ((33, 28), (62, 6), True),
    "balcao_recepcao": ((56, 46), (108, 10), True),
    "bebedouro": ((9, 44), (12, 4), False),
    "planta_seca": ((12, 40), (14, 4), False),
    "mesa_centro": ((21, 16), (38, 5), False),
    "arquivo_aco": ((13, 48), (24, 6), True),
    "arquivo_aco_aberto": ((13, 48), (24, 6), True),
    "mesa_escritorio": ((31, 40), (58, 8), True),
    "cadeira_escritorio": ((11, 30), (12, 4), False),
    "mesa_reuniao": ((62, 32), (120, 10), True),
    "copiadora": ((21, 42), (38, 8), True),
    "console_seguranca": ((40, 44), (76, 8), True),
    "lixeira": ((7, 15), (8, 3), False),
    "caixas_papel": ((18, 27), (32, 6), True),
}
PAREDES = ["escritorio_lisa", "escritorio_forro_aberto", "escritorio_luminaria", "escritorio_duto",
           "escritorio_senhas", "escritorio_quadro_avisos", "escritorio_janela", "escritorio_relogio",
           "escritorio_poster", "escritorio_arquivo_parede", "escritorio_quadro_branco", "escritorio_monitores",
           "escritorio_painel", "pilar_escritorio", "escritorio_lateral"]
PORTAS = {"escritorio_porta": "porta_escritorio", "escritorio_porta_restrita": "porta_restrita"}
CHAOS = ["piso_vinilico", "carpete_azul"]


def pascal(nome):
    return "".join(p.capitalize() for p in nome.split("_"))


def escrever(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def cena_sprite(nome, pasta, deslocamento=None):
    linhas = ["[gd_scene format=3]", "",
              f'[ext_resource type="Texture2D" path="{SPRITES}/{pasta}/{nome}.png" id="1_peca"]', "",
              f'[node name="{pascal(nome)}" type="Sprite2D"]', 'texture = ExtResource("1_peca")', "centered = false"]
    if deslocamento:
        linhas.append(f"offset = Vector2(0, {deslocamento})")
    return "\n".join(linhas) + "\n"


def cena_porta(nome, quadros):
    return f"""[gd_scene format=3]

[ext_resource type="Texture2D" path="{SPRITES}/paredes/{nome}.png" id="1_peca"]
[ext_resource type="SpriteFrames" path="{SPRITES}/porta/{quadros}_quadros.tres" id="2_quadros"]
[ext_resource type="Script" path="res://scripts/sistemas/folha_porta.gd" id="3_script"]

[node name="{pascal(nome)}" type="Sprite2D"]
texture = ExtResource("1_peca")
centered = false

[node name="Folha" type="AnimatedSprite2D" parent="." groups=["folhas_de_porta"]]
position = Vector2(0, {YA_PORTA})
sprite_frames = ExtResource("2_quadros")
animation = &"abrir"
centered = false
script = ExtResource("3_script")
"""


def cena_objeto(nome):
    (px, py), (larg, alt), barreira = OBJETOS[nome]
    camada = f"collision_layer = {CAMADA_BARREIRA}\n" if barreira else ""
    return f"""[gd_scene format=3]

[ext_resource type="Script" path="res://scripts/cenario/objeto_cenario.gd" id="1_objeto"]
[ext_resource type="Texture2D" path="{SPRITES}/objetos/{nome}.png" id="2_sprite"]

[sub_resource type="RectangleShape2D" id="Pegada"]
size = Vector2({larg}, {alt})

[node name="{pascal(nome)}" type="StaticBody2D"]
{camada}script = ExtResource("1_objeto")

[node name="Sprite2D" type="Sprite2D" parent="."]
texture = ExtResource("2_sprite")
centered = false
offset = Vector2({-px}, {-py})

[node name="Pegada" type="CollisionShape2D" parent="."]
position = Vector2(0, {-alt / 2})
shape = SubResource("Pegada")
"""


def montar_kit():
    for nome in PAREDES:
        escrever(os.path.join(PASTA_KIT, "paredes", f"{nome}.tscn"), cena_sprite(nome, "paredes"))
    for nome, quadros in PORTAS.items():
        escrever(os.path.join(PASTA_KIT, "paredes", f"{nome}.tscn"), cena_porta(nome, quadros))
    for nome in CHAOS:
        escrever(os.path.join(PASTA_KIT, "chao", f"{nome}.tscn"), cena_sprite(nome, "chao", Y_CHAO))
        escrever(os.path.join(PASTA_KIT, "chao", f"{nome}_fundo.tscn"), cena_sprite(f"{nome}_fundo", "chao"))
    for nome in OBJETOS:
        escrever(os.path.join(PASTA_KIT, "objetos", f"{nome}.tscn"), cena_objeto(nome))


def texto(valor):
    return '"%s"' % valor.replace("\\", "\\\\").replace('"', '\\"')


def v(x, y):
    return f"Vector2({x}, {y})"


class Montagem:
    def __init__(self):
        self.recursos, self.nos, self.contagem = {}, [], {}

    def recurso(self, tipo, caminho):
        if caminho not in self.recursos:
            self.recursos[caminho] = (tipo, f"r{len(self.recursos) + 1}")
        return f'ExtResource("{self.recursos[caminho][1]}")'

    def nome(self, base):
        self.contagem[base] = self.contagem.get(base, 0) + 1
        return f"{base}{self.contagem[base]}"

    def no(self, nome, pai, cena=None, tipo=None, **props):
        if cena:
            cabecalho = f'[node name="{nome}" parent="{pai}" instance={self.recurso("PackedScene", cena)}]'
        else:
            cabecalho = f'[node name="{nome}" type="{tipo}" parent="{pai}"]'
        self.nos.append((cabecalho, [f"{k} = {val}" for k, val in props.items()]))


SUBRECURSOS = """[sub_resource type="StyleBoxFlat" id="Placa"]
bg_color = Color(0.36, 0.28, 0.12, 1)
border_width_bottom = 1
border_color = Color(0.62, 0.5, 0.22, 1)"""


def montar_sala(sala):
    m = Montagem()
    largura = sala["largura"]
    m.recurso("PackedScene", "res://cenas/salas/modelo_sala.tscn")
    m.recurso("Script", sala["script"])
    for i, peca in enumerate(sala["paredes"]):
        m.no(f"Parede{i + 1:02d}", "Paredes", f"{KIT}/paredes/{peca}.tscn", position=v(i * PECA, 0))
    m.no("PilarEsquerda", "Paredes", f"{KIT}/paredes/pilar_escritorio.tscn", position=v(0, 0))
    m.no("PilarDireita", "Paredes", f"{KIT}/paredes/pilar_escritorio.tscn", position=v(largura - 16, 0), flip_h="true")
    for peca, nome in sala.get("placas", {}).items():
        x = peca * PECA
        m.no(f"Placa{peca + 1:02d}", "Paredes", tipo="Label",
             offset_left=f"{x + 9}.0", offset_top="26.0", offset_right=f"{x + 73}.0", offset_bottom="40.0",
             **{"theme_override_colors/font_color": "Color(0.12, 0.09, 0.04, 1)",
                "theme_override_styles/normal": 'SubResource("Placa")'},
             text=texto(nome), horizontal_alignment="1")
    chao = sala["chao"]
    for c in range(math.ceil(largura / CHAO)):
        m.no(f"Chao{c + 1}", "Chao", f"{KIT}/chao/{chao}.tscn", position=v(c * CHAO, 0))
        for f in range(math.ceil((ALTURA - 180) / FUNDO)):
            m.no(f"Fundo{c + 1}_{f + 1}", "Chao", f"{KIT}/chao/{chao}_fundo.tscn", position=v(c * CHAO, 180 + f * FUNDO))
    for f in range(math.ceil((ALTURA - Y_CHAO) / FUNDO)):
        y = Y_CHAO + f * FUNDO
        m.no(f"LateralEsq{f + 1}", "Chao", f"{KIT}/paredes/escritorio_lateral.tscn", position=v(0, y))
        m.no(f"LateralDir{f + 1}", "Chao", f"{KIT}/paredes/escritorio_lateral.tscn", position=v(largura - 16, y), flip_h="true")
    m.nos.append((f'[node name="Gabriel" parent="Objetos"]', [f"position = {v(*sala['entrada'])}"]))
    for (nome, x, y, *resto) in sala.get("objetos", []):
        caminho = nome if nome.startswith("res://") else f"{KIT}/objetos/{nome}.tscn"
        props = {"position": v(x, y)}
        if resto and resto[0]:
            props["espelhado"] = "true"
        m.no(m.nome(pascal(os.path.basename(caminho).replace(".tscn", ""))), "Objetos", caminho, **props)
    for (cena_luz, x, y, *extras) in sala.get("luzes", []):
        props = {"position": v(x, y)}
        props.update(dict(extras))
        m.no(m.nome("Luz"), "Luzes", f"res://cenas/cenario/luzes/{cena_luz}.tscn", **props)
    m.nos.append(('[node name="Escuridao" parent="."]', [f"color = Color{sala['escuridao']}"]))
    som_porta = m.recurso("AudioStream", "res://assets/audio/efeitos/objetos/porta_abrir.wav")
    for porta in sala["portas"]:
        props = {"position": v(porta["peca"] * PECA + 41, 124), "id": texto(porta["id"]),
                 "cena_destino": texto(porta["destino"])}
        if porta.get("porta_destino"):
            props["porta_destino"] = texto(porta["porta_destino"])
        if porta.get("liberada_por"):
            props["liberada_por"] = texto(porta["liberada_por"])
            props["aviso_bloqueada"] = texto(porta["aviso_bloqueada"])
        props["som_abrir"] = m.recurso("AudioStream", porta["som"]) if porta.get("som") else som_porta
        m.no(f"Porta_{porta['id']}", ".", "res://cenas/sistemas/porta.tscn", **props)
    for extra in sala.get("extras", []):
        extra(m)
    zumbido = m.recurso("AudioStream", "res://assets/audio/ambiente/bunker/bunker_zumbido.wav")
    m.no("Zumbido", ".", tipo="AudioStreamPlayer", stream=zumbido, volume_db="-16.0", autoplay="true", bus='&"Efeitos"')
    m.no("RobosDaSala", ".", tipo="Node", script=m.recurso("Script", "res://scripts/salas/robos_da_sala.gd"))

    linhas = ["[gd_scene format=3]", ""]
    for caminho, (tipo, id_) in m.recursos.items():
        linhas.append(f'[ext_resource type="{tipo}" path="{caminho}" id="{id_}"]')
    linhas += ["", SUBRECURSOS, "", f'[node name="{sala["no"]}" instance=ExtResource("r1")]', 'script = ExtResource("r2")',
               f'id = "{sala["id"]}"', f"largura = {largura}", f"altura = {ALTURA}", f"chao_frente = {ALTURA - 4}", ""]
    for cabecalho, propriedades in m.nos:
        linhas += [cabecalho] + propriedades + [""]
    escrever(os.path.join(PASTA_SALAS, f"{sala['arquivo']}.tscn"), "\n".join(linhas))
    print(f"  sala: cenas/salas/labirinto/escritorio/{sala['arquivo']}.tscn ({largura} x {ALTURA})")


# ---------------------------------------------------------------------------
# Peças que se repetem nas salas
# ---------------------------------------------------------------------------


def robo(nome, tipo, x, y, pontos=None, **props):
    def colocar(m):
        if pontos:
            props["rota"] = f'NodePath("../../Rota{nome}")'
        m.no(nome, "Objetos", f"res://cenas/personagens/robo_{tipo}.tscn", position=v(x, y), **props)
        if pontos:
            m.no(f"Rota{nome}", ".", tipo="Node2D")
            for i, (px, py) in enumerate(pontos):
                m.no(f"Ponto{i + 1}", f"Rota{nome}", tipo="Marker2D", position=v(px, py))
    return colocar


def checkpoint(id_, x, y):
    return lambda m: m.no("Checkpoint", "Objetos", "res://cenas/sistemas/checkpoint.tscn", position=v(x, y), id=texto(id_))


def gatilho(nome, x, y, dialogo, marca_ao_terminar, marca_necessaria=""):
    def colocar(m):
        props = {"position": v(x, y), "dialogo": texto(f"res://dados/dialogos/{dialogo}.json"),
                 "marca_ao_terminar": texto(marca_ao_terminar)}
        if marca_necessaria:
            props["marca_necessaria"] = texto(marca_necessaria)
        m.no(nome, ".", "res://cenas/sistemas/gatilho_dialogo.tscn", **props)
    return colocar


def nicho(x, y, aviso):
    return lambda m: m.no(m.nome("Esconderijo"), "Objetos", "res://cenas/sistemas/nicho_esconderijo.tscn",
                          position=v(x, y), aviso=texto(aviso))


def no_livre(nome, pai, cena, x, y, **props):
    return lambda m: m.no(nome, pai, cena, position=v(x, y), **props)


def lampadas_da_porta(peca):
    """As três lâmpadas verdes da porta restrita (escondidas até cada trava
    soltar), na ordem arquivo, reuniões, segurança."""
    def colocar(m):
        m.no("Travas", ".", tipo="Node2D")
        textura = m.recurso("Texture2D", f"{SPRITES}/porta/lampada_trava.png")
        luz = m.recurso("Texture2D", "res://assets/sprites/cenario/luzes/luz.png")
        for i, dx in enumerate((31, 40, 49)):
            nome = f"Lampada{i + 1}"
            m.no(nome, "Travas", tipo="Sprite2D", visible="false", position=v(peca * PECA + dx, 32), texture=textura)
            m.no("Luz", f"Travas/{nome}", tipo="PointLight2D", color="Color(0.45, 1, 0.55, 1)", energy="1.4",
                 texture=luz, texture_scale="0.3")
    return colocar


SCRIPT_ZANE = "res://scripts/salas/sala_do_zane.gd"
CAMARA = "res://cenas/salas/labirinto/camara_selada.tscn"
SOM_BLINDADA = "res://assets/audio/efeitos/objetos/porta_blindada.wav"
AVISO_BALCAO = "Agachado atrás do balcão, parado e de lanterna apagada, os robôs não me veem."
AVISO_ARQUIVOS = "Parado no vão escuro entre os arquivos, de lanterna apagada, os robôs não me veem."
ESCURO = (0.34, 0.33, 0.37, 1)

CADEIRAS = [("cadeiras_espera", x, y) for y in (200, 252, 304) for x in (226, 298, 438, 510)]
CADEIRAS[6] = ("cadeiras_espera_quebrada", 438, 252)

SALAS_DO_ESCRITORIO = [
    {
        "arquivo": "recepcao", "no": "Recepcao", "id": "escritorio_recepcao", "largura": 960,
        "script": "res://scripts/salas/recepcao_do_escritorio.gd",
        "paredes": ["escritorio_luminaria", "escritorio_duto", "escritorio_porta", "escritorio_senhas",
                    "escritorio_relogio", "escritorio_porta", "escritorio_luminaria", "escritorio_quadro_avisos",
                    "escritorio_porta", "escritorio_janela", "escritorio_forro_aberto", "escritorio_porta_restrita"],
        "placas": {2: "ARQUIVO", 5: "REUNIÕES", 8: "SEGURANÇA"},
        "chao": "piso_vinilico", "entrada": (111, 140),
        "objetos": CADEIRAS + [
            ("planta_seca", 30, 130), ("bebedouro", 300, 128), ("planta_seca", 620, 128),
            ("mesa_centro", 368, 282), ("balcao_recepcao", 800, 222), ("cadeira_escritorio", 834, 196),
            ("lixeira", 742, 140), ("copiadora", 70, 334), ("caixas_papel", 906, 330), ("caixas_papel", 870, 344, True),
        ],
        "luzes": [("luz_tubo", 40, 34, ("energy", "0.7")), ("luz_tubo", 520, 34, ("energy", "0.7")),
                  ("luz_fria", 800, 190, ("energy", "0.3")), ("luz_fria", 368, 260, ("energy", "0.3"))],
        "escuridao": ESCURO,
        "portas": [
            {"peca": 2, "id": "recepcao_arquivo", "destino": f"{SALAS}/arquivo.tscn", "porta_destino": "arquivo_recepcao"},
            {"peca": 5, "id": "recepcao_reunioes", "destino": f"{SALAS}/reunioes.tscn", "porta_destino": "reunioes_recepcao"},
            {"peca": 8, "id": "recepcao_seguranca", "destino": f"{SALAS}/seguranca.tscn", "porta_destino": "seguranca_recepcao"},
            {"peca": 11, "id": "recepcao_camara", "destino": CAMARA, "liberada_por": "zane_passagem_concluida",
             "aviso_bloqueada": "Três lâmpadas em cima da porta. Uma para cada sala.", "som": SOM_BLINDADA},
        ],
        "extras": [
            checkpoint("escritorio_recepcao", 111, 168),
            nicho(784, 202, AVISO_BALCAO),
            robo("Ronda", "ronda", 168, 172, [(168, 172), (568, 172), (568, 336), (168, 336)], bipa_antes_de_virar="true"),
            gatilho("GatilhoEntrada", 111, 150, "zane_escritorio_recepcao", "zane_escritorio_recepcao_visto"),
            gatilho("GatilhoFim", 900, 160, "zane_passagem_fim", "zane_passagem_concluida", "escritorio_tres_travas"),
            lampadas_da_porta(11),
        ],
    },
    {
        "arquivo": "arquivo", "no": "Arquivo", "id": "escritorio_arquivo", "largura": 480, "script": SCRIPT_ZANE,
        "paredes": ["escritorio_porta", "escritorio_arquivo_parede", "escritorio_luminaria", "escritorio_arquivo_parede",
                    "escritorio_forro_aberto", "escritorio_arquivo_parede"],
        "placas": {0: "RECEPÇÃO"},
        "chao": "carpete_azul", "entrada": (41, 140),
        "objetos": [
            ("arquivo_aco", 132, 206), ("arquivo_aco_aberto", 156, 206), ("arquivo_aco", 180, 206),
            ("arquivo_aco", 300, 206), ("arquivo_aco", 324, 206), ("arquivo_aco_aberto", 348, 206), ("arquivo_aco", 372, 206),
            ("arquivo_aco", 214, 272), ("arquivo_aco", 238, 272), ("arquivo_aco", 262, 272),
            ("arquivo_aco", 394, 272), ("arquivo_aco_aberto", 418, 272),
            ("arquivo_aco", 92, 336), ("arquivo_aco", 116, 336), ("arquivo_aco", 300, 336), ("arquivo_aco", 324, 336),
            ("caixas_papel", 450, 336), ("caixas_papel", 60, 250, True), ("lixeira", 200, 140), ("mesa_escritorio", 110, 140),
            ("cadeira_escritorio", 112, 160),
        ],
        "luzes": [("luz_tubo", 200, 34, ("energy", "0.6")), ("luz_fria", 260, 250, ("energy", "0.3"))],
        "escuridao": (0.3, 0.3, 0.34, 1),
        "portas": [{"peca": 0, "id": "arquivo_recepcao", "destino": f"{SALAS}/recepcao.tscn", "porta_destino": "recepcao_arquivo"}],
        "extras": [
            checkpoint("escritorio_arquivo", 70, 168),
            nicho(250, 236, AVISO_ARQUIVOS),
            robo("Rastreador", "rastreador", 340, 240),
            gatilho("GatilhoEntrada", 41, 150, "zane_escritorio_arquivo", "zane_escritorio_arquivo_visto"),
            no_livre("ArquivoDeslizante", "Objetos", "res://cenas/sistemas/painel_ordenacao.tscn", 440, 128,
                     ordem_certa='PackedStringArray("1979", "1981", "1983", "1985", "1988")',
                     ordem_inicial="PackedInt32Array(3, 0, 4, 2, 1)", marca=texto("escritorio_trava_arquivo"),
                     titulo=texto("ARQUIVO DESLIZANTE"), pedido=texto("PASTAS DA MAIS ANTIGA PARA A MAIS NOVA"),
                     texto_acao=texto("Organizar as pastas"),
                     aviso_ordenado=texto("As pastas estão em ordem. Lá na recepção, uma lâmpada acendeu."),
                     aviso_ja_ordenado=texto("As pastas já estão em ordem.")),
        ],
    },
    {
        "arquivo": "reunioes", "no": "Reunioes", "id": "escritorio_reunioes", "largura": 480, "script": SCRIPT_ZANE,
        "paredes": ["escritorio_porta", "escritorio_quadro_branco", "escritorio_luminaria", "escritorio_janela",
                    "escritorio_poster", "escritorio_lisa"],
        "placas": {0: "RECEPÇÃO"},
        "chao": "carpete_azul", "entrada": (41, 140),
        "objetos": [
            ("mesa_reuniao", 262, 252),
            ("cadeira_escritorio", 214, 232), ("cadeira_escritorio", 252, 232), ("cadeira_escritorio", 290, 232),
            ("cadeira_escritorio", 328, 232), ("cadeira_escritorio", 196, 286), ("cadeira_escritorio", 300, 290),
            ("copiadora", 420, 150), ("planta_seca", 460, 330), ("planta_seca", 30, 330), ("lixeira", 380, 140),
            ("caixas_papel", 70, 300),
        ],
        "luzes": [("luz_tubo", 200, 34, ("energy", "0.45"))],
        "escuridao": (0.26, 0.26, 0.31, 1),
        "portas": [{"peca": 0, "id": "reunioes_recepcao", "destino": f"{SALAS}/recepcao.tscn", "porta_destino": "recepcao_reunioes"}],
        "extras": [
            checkpoint("escritorio_reunioes", 70, 168),
            robo("Mariposa", "mariposa", 330, 320),
            gatilho("GatilhoEntrada", 41, 150, "zane_escritorio_reunioes", "zane_escritorio_reunioes_visto"),
            no_livre("Quadro", "Objetos", "res://cenas/itens/aviso_no_mundo.tscn", 120, 128, texto_acao=texto("Ler o quadro"),
                     altura_aviso="60.0",
                     texto=texto("No quadro branco, a pauta de uma reunião: \"CALIBRAÇÃO — DATA-ALVO: 26/10/1985\". "
                                 "Embaixo, de caneta vermelha e circulado: \"O ano basta.\"")),
            no_livre("PainelCodigo", "Objetos", "res://cenas/sistemas/painel_codigo.tscn", 448, 132, codigo=texto("1985"),
                     marca_energia=texto(""), marca=texto("escritorio_trava_reunioes"), texto_acao=texto("Digitar o código"),
                     aviso_aberto=texto("Código aceito. Lá na recepção, uma lâmpada acendeu."),
                     aviso_ja_aberto=texto("Essa trava já está solta.")),
        ],
    },
    {
        "arquivo": "seguranca", "no": "Seguranca", "id": "escritorio_seguranca", "largura": 480, "script": SCRIPT_ZANE,
        "paredes": ["escritorio_porta", "escritorio_monitores", "escritorio_monitores", "escritorio_luminaria",
                    "escritorio_lisa", "escritorio_painel"],
        "placas": {0: "RECEPÇÃO"},
        "chao": "carpete_azul", "entrada": (41, 140),
        "objetos": [
            ("console_seguranca", 160, 176), ("cadeira_escritorio", 160, 200),
            ("res://cenas/cenario/bunker/objetos/rack_servidor.tscn", 300, 300),
            ("res://cenas/cenario/bunker/objetos/rack_servidor.tscn", 326, 300),
            ("res://cenas/cenario/bunker/objetos/rack_servidor.tscn", 352, 300),
            ("caixas_papel", 60, 330), ("lixeira", 236, 140), ("mesa_escritorio", 120, 300),
        ],
        "luzes": [("luz_tubo", 280, 34, ("energy", "0.5")),
                  ("luz_fria", 160, 150, ("energy", "0.4"), ("color", "Color(0.4, 0.95, 0.6, 1)")),
                  ("luz_fria", 330, 260, ("energy", "0.25"))],
        "escuridao": (0.3, 0.31, 0.34, 1),
        "portas": [{"peca": 0, "id": "seguranca_recepcao", "destino": f"{SALAS}/recepcao.tscn", "porta_destino": "recepcao_seguranca"}],
        "extras": [
            checkpoint("escritorio_seguranca", 70, 168),
            robo("Sentinela", "sentinela", 420, 176, [(390, 176), (452, 176)], pausa_no_ponto="2.0"),
            gatilho("GatilhoEntrada", 41, 150, "zane_escritorio_seguranca", "zane_escritorio_seguranca_visto"),
            no_livre("QuadroDeChaves", "Objetos", "res://cenas/sistemas/painel_bits.tscn", 440, 128, alvo="19",
                     quantidade_chaves="5", marca=texto("escritorio_trava_seguranca"), titulo=texto("TRAVA DA SEGURANÇA"),
                     texto_acao=texto("Mexer nas chaves"),
                     aviso_liberado=texto("A trava soltou. Lá na recepção, uma lâmpada acendeu."),
                     aviso_ja_liberado=texto("Essa trava já está solta.")),
        ],
    },
]


def main():
    montar_kit()
    print("  kit: cenas/cenario/escritorio/")
    for sala in SALAS_DO_ESCRITORIO:
        montar_sala(sala)


if __name__ == "__main__":
    main()
