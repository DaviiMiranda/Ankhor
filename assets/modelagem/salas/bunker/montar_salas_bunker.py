# montar_salas_bunker.py — monta as cenas do Godot das salas do bunker que
# entraram depois da primeira versão (docs/fases/bunker.md): o arsenal e as
# duas salas antigas, e as cenas das peças do kit das salas antigas.
#
# Como rodar (Python 3, depois do gerar_salas_antigas.py):
#
#   python assets/modelagem/cenario/gerar_salas_antigas.py
#   python assets/modelagem/salas/bunker/montar_salas_bunker.py
#
# ATENÇÃO: este script sobrescreve as três salas. Depois que alguém ajustar
# uma delas no editor do Godot, passe o ajuste para a descrição da sala aqui
# embaixo antes de rodar de novo. As outras salas do bunker não são tocadas.
#
# As regras de montagem são as mesmas das outras salas do bunker (ver
# cenas/salas/bunker/deposito.tscn): parede do fundo em peças de 80 px com um
# pilar de 16 px em cada ponta, chão de perto em peças de 128 px, o chão de
# fundo em peças de 128 x 64 a partir de y = 180, as paredes laterais de
# 16 px a partir de y = 112, e cada porta em x = (x da peça) + 41, y = 124.

import math
import os

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "..", ".."))
PASTA_SALAS = os.path.join(PASTA_PROJETO, "cenas", "salas", "bunker")
PASTA_KIT_ANTIGAS = os.path.join(PASTA_PROJETO, "cenas", "cenario", "bunker", "salas_antigas")

PECA, CHAO, FUNDO, Y_CHAO = 80, 128, 64, 112
BUNKER = "res://cenas/cenario/bunker"
ANTIGAS = "res://cenas/cenario/bunker/salas_antigas"

# Pés e pegadas dos móveis das salas antigas (os números que o
# gerar_salas_antigas.py imprime).
OBJETOS_ANTIGOS = {
    "sofa_xix": ((32, 32), (60, 6)),
    "poltrona_xix": ((15, 32), (26, 5)),
    "mesa_lampiao": ((18, 44), (24, 5)),
    "relogio_pendulo": ((9, 60), (16, 4)),
    "cristaleira": ((17, 56), (32, 5)),
    "sofa_80": ((33, 30), (62, 6)),
    "mesinha_80": ((20, 22), (36, 5)),
    "vitrola": ((29, 34), (56, 6)),
    "abajur_80": ((9, 52), (10, 3)),
}
PAREDES_ANTIGAS = ["antiga_xix_papel", "antiga_xix_quadro", "antiga_xix_janela", "antiga_xix_porta",
                   "antiga_80_papel", "antiga_80_estante", "antiga_80_quadro", "antiga_80_porta"]
CHAOS_ANTIGOS = ["assoalho", "carpete"]
FUNDOS_ANTIGOS = ["assoalho_fundo", "carpete_fundo"]


def pascal(nome):
    return "".join(p.capitalize() for p in nome.split("_"))


def escrever(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def cena_sprite(nome, pasta, deslocamento=None):
    linhas = ["[gd_scene format=3]", "",
              f'[ext_resource type="Texture2D" path="res://assets/sprites/cenario/bunker/salas_antigas/{pasta}/{nome}.png" id="1_peca"]', "",
              f'[node name="{pascal(nome)}" type="Sprite2D"]', 'texture = ExtResource("1_peca")', "centered = false"]
    if deslocamento:
        linhas.append(f"offset = Vector2(0, {deslocamento})")
    return "\n".join(linhas) + "\n"


def cena_objeto(nome):
    (px, py), (larg, alt) = OBJETOS_ANTIGOS[nome]
    return f"""[gd_scene format=3]

[ext_resource type="Script" path="res://scripts/cenario/objeto_cenario.gd" id="1_objeto"]
[ext_resource type="Texture2D" path="res://assets/sprites/cenario/bunker/salas_antigas/objetos/{nome}.png" id="2_sprite"]

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


def montar_kit():
    for nome in PAREDES_ANTIGAS:
        escrever(os.path.join(PASTA_KIT_ANTIGAS, "paredes", f"{nome}.tscn"), cena_sprite(nome, "paredes"))
    for nome in CHAOS_ANTIGOS:
        escrever(os.path.join(PASTA_KIT_ANTIGAS, "chao", f"{nome}.tscn"), cena_sprite(nome, "chao", Y_CHAO))
    for nome in FUNDOS_ANTIGOS:
        escrever(os.path.join(PASTA_KIT_ANTIGAS, "chao", f"{nome}.tscn"), cena_sprite(nome, "chao"))
    for nome in OBJETOS_ANTIGOS:
        escrever(os.path.join(PASTA_KIT_ANTIGAS, "objetos", f"{nome}.tscn"), cena_objeto(nome))


class Montagem:
    def __init__(self):
        self.recursos, self.nos, self.contagem = {}, [], {}

    def recurso(self, tipo, caminho):
        if caminho not in self.recursos:
            self.recursos[caminho] = (tipo, f"r{len(self.recursos) + 1}")
        return self.recursos[caminho][1]

    def nome(self, base):
        self.contagem[base] = self.contagem.get(base, 0) + 1
        return f"{base}{self.contagem[base]}"

    def no(self, cabecalho, propriedades=()):
        self.nos.append((cabecalho, list(propriedades)))

    def instancia(self, nome, pai, caminho, propriedades=()):
        self.no(f'[node name="{nome}" parent="{pai}" instance=ExtResource("{self.recurso("PackedScene", caminho)}")]', propriedades)


PLACA = """[sub_resource type="StyleBoxFlat" id="Placa"]
bg_color = Color(0.09, 0.1, 0.12, 1)
border_width_bottom = 1
border_color = Color(0.3, 0.33, 0.38, 1)"""


def caminho_peca(peca):
    return peca if peca.startswith("res://") else f"{BUNKER}/paredes/{peca}.tscn"


def montar_sala(sala):
    m = Montagem()
    largura, altura = sala["largura"], sala["altura"]
    m.recurso("PackedScene", "res://cenas/salas/modelo_sala.tscn")
    som_porta = m.recurso("AudioStream", "res://assets/audio/efeitos/objetos/porta_blindada.wav")
    pecas = largura // PECA
    paredes = list(sala["paredes"]) + ["bunker_lisa"] * (pecas - len(sala["paredes"]))
    for i, peca in enumerate(paredes[:pecas]):
        m.instancia(f"Parede{i + 1:02d}", "Paredes", caminho_peca(peca), [f"position = Vector2({i * PECA}, 0)"])
    m.instancia("PilarEsquerda", "Paredes", f"{BUNKER}/paredes/pilar_bunker.tscn", ["position = Vector2(0, 0)"])
    m.instancia("PilarDireita", "Paredes", f"{BUNKER}/paredes/pilar_bunker.tscn", [f"position = Vector2({largura - 16}, 0)"])
    porta = sala["porta"]
    if porta.get("placa"):
        x = porta["peca"] * PECA
        m.no('[node name="PlacaPorta" type="Label" parent="Paredes"]', [
            f"offset_left = {x + 9}.0", "offset_top = 26.0", f"offset_right = {x + 73}.0", "offset_bottom = 40.0",
            "theme_override_colors/font_color = Color(0.86, 0.74, 0.34, 1)",
            'theme_override_styles/normal = SubResource("Placa")', f'text = "{porta["placa"]}"', "horizontal_alignment = 1"])
    for c in range(math.ceil(largura / CHAO)):
        m.instancia(f"Chao{c + 1}", "Chao", sala["chao"], [f"position = Vector2({c * CHAO}, 0)"])
        for f in range(math.ceil((altura - 180) / FUNDO)):
            m.instancia(f"Fundo{c + 1}_{f + 1}", "Chao", sala["fundo"], [f"position = Vector2({c * CHAO}, {180 + f * FUNDO})"])
    for f in range(math.ceil((altura - Y_CHAO) / FUNDO)):
        y = Y_CHAO + f * FUNDO
        m.instancia(f"LateralEsq{f + 1}", "Chao", f"{BUNKER}/paredes/bunker_lateral.tscn", [f"position = Vector2(0, {y})"])
        m.instancia(f"LateralDir{f + 1}", "Chao", f"{BUNKER}/paredes/bunker_lateral.tscn",
                    [f"position = Vector2({largura - 16}, {y})", "flip_h = true"])
    for (caminho, x, y, *resto) in sala.get("objetos", []):
        props = [f"position = Vector2({x}, {y})"] + (["espelhado = true"] if resto and resto[0] else [])
        m.instancia(m.nome(pascal(os.path.basename(caminho).replace(".tscn", ""))), "Objetos", caminho, props)
    for (item, x, y) in sala.get("itens", []):
        if item == "pilha":
            m.instancia(m.nome("Pilha"), "Objetos", "res://cenas/itens/pilha_no_chao.tscn", [f"position = Vector2({x}, {y})"])
        else:
            id_item = m.recurso("Resource", f"res://dados/itens/{item}.tres")
            m.instancia(m.nome(pascal(item)), "Objetos", "res://cenas/itens/item_no_chao.tscn",
                        [f"position = Vector2({x}, {y})", f'item = ExtResource("{id_item}")'])
    for (cena_luz, x, y, *props) in sala.get("luzes", []):
        m.instancia(m.nome("Luz"), "Luzes", f"res://cenas/cenario/luzes/{cena_luz}.tscn", [f"position = Vector2({x}, {y})", *props])
    m.no('[node name="Escuridao" parent="."]', [f"color = Color{sala['escuridao']}"])
    m.instancia(f"Porta_{porta['id']}", ".", "res://cenas/sistemas/porta.tscn", [
        f"position = Vector2({porta['peca'] * PECA + 41}, 124)", f'id = "{porta["id"]}"',
        f'cena_destino = "res://cenas/salas/bunker/{porta["destino"]}.tscn"', f'porta_destino = "{porta["porta_destino"]}"',
        f'som_abrir = ExtResource("{som_porta}")'])
    zumbido = m.recurso("AudioStream", "res://assets/audio/ambiente/bunker/bunker_zumbido.wav")
    m.no('[node name="Zumbido" type="AudioStreamPlayer" parent="."]', [
        f'stream = ExtResource("{zumbido}")', "volume_db = -10.0", "autoplay = true", 'bus = &"Efeitos"'])
    m.instancia("MusicaBunker", ".", "res://cenas/sistemas/musica_bunker.tscn")

    linhas = ["[gd_scene format=3]", ""]
    for caminho, (tipo, id_) in m.recursos.items():
        linhas.append(f'[ext_resource type="{tipo}" path="{caminho}" id="{id_}"]')
    linhas += ["", PLACA, "", f'[node name="{pascal(sala["id"])}" instance=ExtResource("r1")]',
               f'id = "bunker_{sala["id"]}"', f"largura = {largura}", f"altura = {altura}", f"chao_frente = {altura - 4}", ""]
    for cabecalho, propriedades in m.nos:
        linhas += [cabecalho] + propriedades + [""]
    escrever(os.path.join(PASTA_SALAS, f"{sala['id']}.tscn"), "\n".join(linhas))
    print(f"  sala: cenas/salas/bunker/{sala['id']}.tscn ({largura} x {altura})")


def antigo(nome):
    return f"{ANTIGAS}/objetos/{nome}.tscn"


def do_bunker(nome):
    return f"{BUNKER}/objetos/{nome}.tscn"


SALAS = [
    {
        # O arsenal do setor A: abre quando a energia volta (a trava é elétrica).
        "id": "arsenal", "largura": 400, "altura": 360,
        "paredes": ["bunker_porta", "bunker_armarios", "bunker_luminaria", "bunker_prateleiras", "bunker_armarios"],
        "porta": {"peca": 0, "id": "arsenal_corredor", "placa": "CORREDOR", "destino": "corredor_a", "porta_destino": "arsenal"},
        "chao": f"{BUNKER}/chao/chao_bunker.tscn", "fundo": f"{BUNKER}/chao/chao_bunker_fundo.tscn",
        "objetos": [(do_bunker("estante_metal"), 120, 220), (do_bunker("estante_metal"), 280, 220, True),
                    (do_bunker("mesa_metal"), 200, 300), (do_bunker("caixas"), 340, 320), (do_bunker("caixas"), 60, 330, True)],
        "itens": [("clarao", 180, 320), ("clarao", 230, 320), ("pilha", 340, 250)],
        "luzes": [("luz_tubo", 200, 34, "energy = 0.7"), ("luz_tubo", 200, 260, "energy = 0.6")],
        "escuridao": (0.24, 0.25, 0.24, 1),
    },
    {
        # Sala antiga 1: a sala de visitas de um casarão do fim do século XIX.
        "id": "sala_antiga_xix", "largura": 480, "altura": 360,
        "paredes": [f"{ANTIGAS}/paredes/antiga_xix_porta.tscn", f"{ANTIGAS}/paredes/antiga_xix_papel.tscn",
                    f"{ANTIGAS}/paredes/antiga_xix_janela.tscn", f"{ANTIGAS}/paredes/antiga_xix_quadro.tscn",
                    f"{ANTIGAS}/paredes/antiga_xix_janela.tscn", f"{ANTIGAS}/paredes/antiga_xix_papel.tscn"],
        "porta": {"peca": 0, "id": "sala_antiga_xix_corredor", "destino": "corredor_b", "porta_destino": "sala_antiga_xix"},
        "chao": f"{ANTIGAS}/chao/assoalho.tscn", "fundo": f"{ANTIGAS}/chao/assoalho_fundo.tscn",
        "objetos": [(antigo("relogio_pendulo"), 160, 140), (antigo("cristaleira"), 440, 150), (antigo("sofa_xix"), 260, 220),
                    (antigo("mesa_lampiao"), 260, 280), (antigo("poltrona_xix"), 170, 290), (antigo("poltrona_xix"), 350, 290)],
        "luzes": [("luz_lampada", 260, 246, "energy = 1.2"), ("luz_lampada", 240, 120, "energy = 0.8"), ("luz_lampada", 440, 140, "energy = 0.5")],
        "escuridao": (0.3, 0.25, 0.23, 1),
    },
    {
        # Sala antiga 2: a sala de estar de uma casa dos anos 80.
        "id": "sala_antiga_80", "largura": 480, "altura": 360,
        "paredes": [f"{ANTIGAS}/paredes/antiga_80_porta.tscn", f"{ANTIGAS}/paredes/antiga_80_papel.tscn",
                    f"{ANTIGAS}/paredes/antiga_80_estante.tscn", f"{ANTIGAS}/paredes/antiga_80_papel.tscn",
                    f"{ANTIGAS}/paredes/antiga_80_quadro.tscn", f"{ANTIGAS}/paredes/antiga_80_papel.tscn"],
        "porta": {"peca": 0, "id": "sala_antiga_80_corredor", "destino": "corredor_b", "porta_destino": "sala_antiga_80"},
        "chao": f"{ANTIGAS}/chao/carpete.tscn", "fundo": f"{ANTIGAS}/chao/carpete_fundo.tscn",
        "objetos": [(antigo("vitrola"), 400, 150), (antigo("abajur_80"), 120, 230), (antigo("sofa_80"), 230, 230),
                    (antigo("mesinha_80"), 230, 290), (antigo("abajur_80"), 340, 230)],
        "luzes": [("luz_lampada", 120, 186, "energy = 0.7"), ("luz_lampada", 340, 186, "energy = 0.7"),
                  ("luz_fria", 200, 60, "energy = 0.45", "color = Color(0.55, 0.75, 1, 1)")],
        "escuridao": (0.3, 0.27, 0.25, 1),
    },
]


def main():
    montar_kit()
    print("  kit: cenas/cenario/bunker/salas_antigas/")
    for sala in SALAS:
        montar_sala(sala)


if __name__ == "__main__":
    main()
