# montar_convivencia.py — monta as cenas do kit do Centro de Convivência
# (cenas/cenario/convivencia/) e as 8 cenas da fase
# (cenas/salas/centro_de_convivencia/).
#
# Como rodar:
#   python assets/modelagem/cenario/gerar_convivencia.py
#   python assets/modelagem/salas/centro_de_convivencia/montar_convivencia.py

import math
import os

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "..", ".."))
PASTA_KIT_CONV = os.path.join(PASTA_PROJETO, "cenas", "cenario", "convivencia")
PASTA_SALAS = os.path.join(PASTA_PROJETO, "cenas", "salas", "centro_de_convivencia")

PECA = 80
CHAO = 128
FUNDO = 64
Y_CHAO = 112
X_PORTA = 41
Y_PORTA = 124

OBJETOS_CONV = {
    "mesa_concreto": ((28, 34), (48, 12)),
    "balcao_cantina": ((48, 38), (92, 10)),
}


def pascal(nome):
    return "".join(parte.capitalize() for parte in nome.split("_"))


def escrever(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as arquivo:
        arquivo.write(texto)


def cena_objeto_conv(nome):
    (px, py), (larg, alt) = OBJETOS_CONV[nome]
    return f"""[gd_scene format=3]

[ext_resource type="Script" path="res://scripts/cenario/objeto_cenario.gd" id="1_objeto"]
[ext_resource type="Texture2D" path="res://assets/sprites/cenario/convivencia/{nome}.png" id="2_sprite"]

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


def cena_cacos_vidro():
    return """[gd_scene format=3]

[ext_resource type="Texture2D" path="res://assets/sprites/cenario/convivencia/cacos_vidro.png" id="1_tex"]

[node name="CacosVidro" type="Sprite2D"]
texture = ExtResource("1_tex")
centered = false
offset = Vector2(-32, -24)
"""


def montar_kit():
    for nome in OBJETOS_CONV:
        escrever(os.path.join(PASTA_KIT_CONV, f"{nome}.tscn"), cena_objeto_conv(nome))
    escrever(os.path.join(PASTA_KIT_CONV, "cacos_vidro.tscn"), cena_cacos_vidro())
    print("  kit: cenas/cenario/convivencia/")


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

    def nome(self, base):
        self.contagem[base] = self.contagem.get(base, 0) + 1
        return f"{base}{self.contagem[base]}"

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


PLACA = """[sub_resource type="StyleBoxFlat" id="Placa"]
bg_color = Color(0.12, 0.13, 0.14, 1)"""

MAPA_PAREDE = {
    "lisa": "res://cenas/cenario/paredes/parede_lisa.tscn",
    "rachada": "res://cenas/cenario/paredes/parede_rachada.tscn",
    "janela": "res://cenas/cenario/paredes/parede_janela.tscn",
    "arandela": "res://cenas/cenario/paredes/parede_arandela.tscn",
    "desabada": "res://cenas/cenario/paredes/parede_desabada.tscn",
    "mural": "res://cenas/cenario/paredes/parede_mural.tscn",
    "conduites": "res://cenas/cenario/paredes/parede_conduites.tscn",
    "fluorescente": "res://cenas/cenario/paredes/parede_fluorescente.tscn",
    "servidores": "res://cenas/cenario/paredes/parede_servidores.tscn",
    "painel_ciano": "res://cenas/cenario/paredes/parede_painel_ciano.tscn",
    "escada_sobe": "res://cenas/cenario/paredes/parede_escada_sobe.tscn",
    "escada_desce": "res://cenas/cenario/paredes/parede_escada_desce.tscn",
    "nicho_armario": "res://cenas/cenario/paredes/parede_nicho_armario.tscn",
    "nicho_bebedouro": "res://cenas/cenario/paredes/parede_nicho_bebedouro.tscn",
    "porta": "res://cenas/cenario/bloco_de_salas/parede_porta_animada.tscn",
}

MAPA_CHAO = {
    "lajotas": ("res://cenas/cenario/chao/chao_lajotas.tscn", "res://cenas/cenario/chao/chao_lajotas_fundo.tscn"),
    "areia": ("res://cenas/cenario/chao/chao_areia.tscn", "res://cenas/cenario/chao/chao_areia_fundo.tscn"),
    "mato": ("res://cenas/cenario/chao/chao_mato.tscn", "res://cenas/cenario/chao/chao_mato_fundo.tscn"),
    "tapete": ("res://cenas/cenario/chao/chao_tapete.tscn", "res://cenas/cenario/chao/chao_tapete_fundo.tscn"),
}

MAPA_OBJETO = {
    "mesa_concreto": "res://cenas/cenario/convivencia/mesa_concreto.tscn",
    "balcao_cantina": "res://cenas/cenario/convivencia/balcao_cantina.tscn",
    "cacos_vidro": "res://cenas/cenario/convivencia/cacos_vidro.tscn",
    "arvore": "res://cenas/cenario/objetos/arvore.tscn",
    "entulho": "res://cenas/cenario/objetos/entulho.tscn",
    "lampada": "res://cenas/cenario/objetos/lampada.tscn",
    "gerador": "res://cenas/cenario/objetos/gerador.tscn",
    "painel_distribuicao": "res://cenas/cenario/objetos/painel_distribuicao.tscn",
    "terminal": "res://cenas/cenario/objetos/terminal.tscn",
    "torre_equipamentos": "res://cenas/cenario/objetos/torre_equipamentos.tscn",
    "mesa_leitura": "res://cenas/cenario/objetos/mesa_leitura.tscn",
    "cadeira": "res://cenas/cenario/objetos/cadeira.tscn",
    "carrinho": "res://cenas/cenario/objetos/carrinho.tscn",
    "livros": "res://cenas/cenario/objetos/livros.tscn",
    "estante_vazia": "res://cenas/cenario/objetos/estante_vazia.tscn",
    "estante_quebrada": "res://cenas/cenario/objetos/estante_quebrada.tscn",
    "estante_metal": "res://cenas/cenario/bunker/objetos/estante_metal.tscn",
    "caixas": "res://cenas/cenario/bunker/objetos/caixas.tscn",
    "latas": "res://cenas/cenario/bunker/objetos/latas.tscn",
    "tambor": "res://cenas/cenario/bunker/objetos/tambor.tscn",
    "colchao": "res://cenas/cenario/bunker/objetos/colchao.tscn",
    "mesa_metal": "res://cenas/cenario/bunker/objetos/mesa_metal.tscn",
    "mesa_computador": "res://cenas/cenario/dtec/objetos/mesa_computador.tscn",
    "bancada_eletronica": "res://cenas/cenario/dtec/objetos/bancada_eletronica.tscn",
}


def montar_sala(sala):
    m = Montagem()
    id_sala, largura, altura = sala["id"], sala["largura"], sala["altura"]
    funda = altura > 180
    m.cena("res://cenas/salas/modelo_sala.tscn")
    ceu_tex = m.recurso("Texture2D", "res://assets/sprites/cenario/ceu/ceu_noite.png")
    m.no('[node name="Sprite2D" parent="Ceu"]', ["self_modulate = Color(1, 1, 1, 1)", f'texture = ExtResource("{ceu_tex}")'])

    paredes = list(sala["paredes"])
    pecas = largura // PECA
    paredes += ["lisa"] * (pecas - len(paredes))
    portas = {p["peca"]: p for p in sala.get("portas", [])}
    for i, tipo in enumerate(paredes[:pecas]):
        if i in portas and portas[i].get("parede_tipo"):
            tipo_p = portas[i]["parede_tipo"]
        elif i in portas:
            tipo_p = "porta"
        else:
            tipo_p = tipo
        m.instancia(f"Parede{i + 1:02d}", "Paredes", MAPA_PAREDE[tipo_p], [f"position = Vector2({i * PECA}, 0)"])
        if tipo_p in ("nicho_armario", "nicho_bebedouro"):
            m.instancia(f"Nicho{i * PECA}", "Objetos", "res://cenas/sistemas/nicho_esconderijo.tscn",
                        [f"position = Vector2({i * PECA + 40}, 128)"])

    m.instancia("PilarEsquerda", "Paredes", "res://cenas/cenario/paredes/pilar.tscn", ["position = Vector2(0, 0)"])
    m.instancia("PilarDireita", "Paredes", "res://cenas/cenario/paredes/pilar.tscn", [f"position = Vector2({largura - 16}, 0)"])

    for i, porta in portas.items():
        if porta.get("placa"):
            x = i * PECA
            m.no(f'[node name="Placa{pascal(porta["id"])}" type="Label" parent="Paredes"]', [
                f"offset_left = {x + 6}.0", "offset_top = 30.0", f"offset_right = {x + 74}.0", "offset_bottom = 44.0",
                "theme_override_colors/font_color = Color(0.82, 0.8, 0.7, 1)",
                'theme_override_styles/normal = SubResource("Placa")',
                f'text = "{porta["placa"]}"', "horizontal_alignment = 1"])

    if sala.get("comporta_rampa") is not None:
        peca_c = sala["comporta_rampa"]
        tex_comp = m.recurso("Texture2D", "res://assets/sprites/cenario/convivencia/comporta_rampa.png")
        m.instancia("ComportaRampa", "Paredes", "res://cenas/sistemas/grade_seguranca.tscn",
                    [f"position = Vector2({peca_c * PECA + 16}, 44)", 'marca = "convivencia_energia"'])
        m.no('[node name="Grade" parent="Paredes/ComportaRampa" index="0"]', [f'texture = ExtResource("{tex_comp}")'])

    colunas = math.ceil(largura / CHAO)
    trocas = sala.get("chao_trocas", {})
    chao_padrao = sala.get("chao", "lajotas")
    for c in range(colunas):
        tipo_c = trocas.get(c, chao_padrao)
        m.instancia(f"Chao{c + 1}", "Chao", MAPA_CHAO[tipo_c][0], [f"position = Vector2({c * CHAO}, 0)"])
    if funda:
        linhas = math.ceil((altura - 180) / FUNDO)
        trocas_fundo = sala.get("fundo_trocas", {})
        for c in range(colunas):
            tipo_c = trocas.get(c, chao_padrao)
            for f in range(linhas):
                tipo_f = trocas_fundo.get((c, f), tipo_c)
                m.instancia(f"Fundo{c + 1}_{f + 1}", "Chao", MAPA_CHAO[tipo_f][1],
                            [f"position = Vector2({c * CHAO}, {180 + f * FUNDO})"])
        for f in range(math.ceil((altura - Y_CHAO) / FUNDO)):
            y = Y_CHAO + f * FUNDO
            m.instancia(f"LateralEsq{f + 1}", "Chao", "res://cenas/cenario/paredes/parede_lateral.tscn", [f"position = Vector2(0, {y})"])
            m.instancia(f"LateralDir{f + 1}", "Chao", "res://cenas/cenario/paredes/parede_lateral.tscn",
                        [f"position = Vector2({largura - 16}, {y})", "flip_h = true"])

    for (nome, x, y, *resto) in sala.get("objetos", []):
        caminho = MAPA_OBJETO[nome]
        props = [f"position = Vector2({x}, {y})"]
        if resto and resto[0]:
            props.append("espelhado = true")
        m.instancia(m.nome(pascal(nome)), "Objetos", caminho, props)

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

    if sala.get("checkpoint"):
        id_cp, x_cp, y_cp = sala["checkpoint"]
        m.instancia("Checkpoint", "Objetos", "res://cenas/sistemas/checkpoint.tscn",
                    [f"position = Vector2({x_cp}, {y_cp})", f'id = "{id_cp}"'])

    if sala.get("painel_comutacao"):
        x_pc, y_pc = sala["painel_comutacao"]
        m.instancia("PainelComutacao", "Objetos", "res://cenas/sistemas/painel_comutacao.tscn",
                    [f"position = Vector2({x_pc}, {y_pc})"])

    for (cena_luz, x, y, *props) in sala.get("luzes", []):
        m.instancia(m.nome("Luz"), "Luzes", f"res://cenas/cenario/luzes/{cena_luz}.tscn", [f"position = Vector2({x}, {y})", *props])

    if sala.get("holofotes"):
        scr_vcm = m.recurso("Script", "res://scripts/sistemas/visivel_com_marca.gd")
        m.no('[node name="HolofotesPerimetrais" type="Node2D" parent="."]', [
            f'script = ExtResource("{scr_vcm}")', 'marca = "convivencia_energia"', "revela_quem_passa = true"])
        for idx, (hx, hy) in enumerate(sala["holofotes"]):
            m.instancia(f"Holofote{idx + 1}", "HolofotesPerimetrais", "res://cenas/cenario/luzes/luz_fria.tscn",
                        [f"position = Vector2({hx}, {hy})", "scale = Vector2(2.2, 2.0)", "color = Color(0.85, 0.95, 1, 1)", "energy = 1.15"])

    m.no('[node name="Escuridao" parent="."]', [f"color = Color{sala.get('escuridao', (0.22, 0.24, 0.36, 1))}"])
    if "gabriel" in sala:
        m.no('[node name="Gabriel" parent="Objetos"]', [f"position = Vector2{sala['gabriel']}"])

    for i, porta in portas.items():
        x = i * PECA + X_PORTA
        props = [f"position = Vector2({x}, {Y_PORTA})", f'id = "{porta["id"]}"']
        if porta.get("liberada_por"):
            props += [f'liberada_por = "{porta["liberada_por"]}"', f'aviso_bloqueada = "{porta["aviso"]}"']
        if porta.get("bloqueada"):
            props += ["bloqueada = true", f'aviso_bloqueada = "{porta["aviso"]}"']
        else:
            props += [f'cena_destino = "res://cenas/salas/centro_de_convivencia/{porta["destino"]}.tscn"',
                      f'porta_destino = "{porta["porta_destino"]}"']
        m.instancia(f"Porta_{porta['id']}", ".", "res://cenas/sistemas/porta.tscn", props)

    sub_recursos = [PLACA]
    rodape = ['[editable path="Ceu"]']

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
                props_r += [f'rota_com_marca = NodePath("../../{nome_rota_e}")', 'marca_da_rota = "convivencia_energia"']
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
    if funda:
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
text = "VOCÊ DESCEU PELA RAMPA"

[node name="Subtitulo" parent="SaidaFase/Tela/Titulo" index="0"]
text = "Próxima fase: o Bunker"
"""
    escrever(os.path.join(PASTA_SALAS, "fim_da_convivencia.tscn"), texto)
    print("  sala: cenas/salas/centro_de_convivencia/fim_da_convivencia.tscn")


SALAS = [
    {
        "id": "passarela_acesso", "largura": 640, "altura": 180, "gabriel": "(96, 152)",
        "paredes": ["escada_sobe", "janela", "mural", "arandela", "nicho_bebedouro", "janela", "escada_desce", "rachada"],
        "portas": [
            {"peca": 0, "parede_tipo": "escada_sobe", "id": "passarela_subsolo", "placa": "SUBSOLO",
             "bloqueada": True, "aviso": "O alçapão de manutenção se fechou por trás na subida."},
            {"peca": 6, "parede_tipo": "escada_desce", "id": "passarela_patio", "placa": "PÁTIO",
             "destino": "patio_central", "porta_destino": "patio_passarela"},
        ],
        "objetos": [("lampada", 290, 134), ("entulho", 420, 148)],
        "itens": [("pilha", 360, 162), ("lanterna", 140, 160), ("radio", 180, 160)],
        "checkpoint": ("conv_passarela", 60, 140),
        "transmissoes": [("zane_convivencia_01", 220, 152, "")],
        "luzes": [
            ("luz_fria", 120, 50, "color = Color(0.5, 0.65, 0.95, 1)", "energy = 0.65"),
            ("luz_lampada", 290, 126, "energy = 0.65"),
            ("luz_fria", 440, 50, "color = Color(0.5, 0.65, 0.95, 1)", "energy = 0.65"),
        ],
        "escuridao": (0.24, 0.26, 0.38, 1),
    },
    {
        "id": "patio_central", "largura": 1280, "altura": 360,
        "paredes": ["escada_sobe", "desabada", "janela", "nicho_armario", "porta", "rachada", "desabada", "arandela",
                    "desabada", "porta", "nicho_bebedouro", "desabada", "rachada", "porta", "janela", "desabada"],
        "portas": [
            {"peca": 0, "parede_tipo": "escada_sobe", "id": "patio_passarela", "placa": "PASSARELA",
             "destino": "passarela_acesso", "porta_destino": "passarela_patio"},
            {"peca": 4, "id": "patio_cantina", "placa": "CANTINA",
             "destino": "cantina", "porta_destino": "cantina_patio"},
            {"peca": 9, "id": "patio_grafica", "placa": "GRÁFICA",
             "destino": "grafica_rapida", "porta_destino": "grafica_patio"},
            {"peca": 13, "id": "patio_rampa", "placa": "RAMPA",
             "destino": "rampa_subsolo", "porta_destino": "rampa_patio"},
        ],
        "chao": "lajotas",
        "chao_trocas": {1: "mato", 2: "areia", 4: "mato", 5: "areia", 7: "mato", 8: "areia"},
        "fundo_trocas": {(1, 0): "mato", (2, 1): "areia", (4, 1): "mato", (6, 0): "areia", (7, 1): "mato"},
        "objetos": [
            ("arvore", 220, 210), ("mesa_concreto", 310, 185), ("mesa_concreto", 440, 290, True),
            ("arvore", 590, 235, True), ("mesa_concreto", 700, 185), ("mesa_concreto", 860, 290),
            ("arvore", 990, 215), ("mesa_concreto", 1140, 250, True),
            ("entulho", 150, 310), ("entulho", 640, 320, True), ("lampada", 520, 145), ("lampada", 1020, 145),
        ],
        "itens": [("pedra", 170, 318), ("pedra", 620, 325), ("pedra", 940, 315)],
        "transmissoes": [("zane_convivencia_02", 760, 150, "convivencia_energia")],
        "luzes": [
            ("luz_fria", 160, 90, "scale = Vector2(1.8, 1.8)", "color = Color(0.5, 0.65, 0.98, 1)", "energy = 0.7"),
            ("luz_fria", 520, 180, "scale = Vector2(2.0, 1.8)", "color = Color(0.5, 0.65, 0.98, 1)", "energy = 0.75"),
            ("luz_fria", 880, 190, "scale = Vector2(2.0, 1.8)", "color = Color(0.5, 0.65, 0.98, 1)", "energy = 0.75"),
            ("luz_fria", 1160, 160, "scale = Vector2(1.8, 1.8)", "color = Color(0.5, 0.65, 0.98, 1)", "energy = 0.7"),
            ("luz_lampada", 520, 137, "energy = 0.55"),
            ("luz_lampada", 1020, 137, "energy = 0.55"),
        ],
        "holofotes": [(260, 240), (540, 200), (820, 240), (1060, 200)],
        "robos": [
            {
                "tipo": "sentinela", "pos": "(420, 160)",
                "rota": ["(200, 155)", "(520, 155)", "(520, 315)", "(200, 315)"],
                "rota_energia": ["(180, 155)", "(660, 155)", "(660, 250)", "(180, 315)"],
            },
            {
                "tipo": "sentinela", "pos": "(920, 310)",
                "rota": ["(740, 155)", "(1080, 155)", "(1080, 315)", "(740, 315)"],
                "rota_energia": ["(680, 315)", "(1120, 155)", "(1120, 315)", "(680, 155)"],
            },
        ],
        "zonas_piso": [
            (0, 112, 420, 248, 0.7, "areia e folhas"),
            (420, 112, 440, 248, 1.0, "lajota rachada"),
            (860, 112, 420, 248, 0.7, "areia e raízes"),
        ],
        "escuridao": (0.2, 0.23, 0.35, 1),
    },
    {
        "id": "cantina", "largura": 640, "altura": 260,
        "paredes": ["porta", "mural", "nicho_armario", "fluorescente", "rachada", "conduites", "porta", "arandela"],
        "portas": [
            {"peca": 0, "id": "cantina_patio", "placa": "PÁTIO",
             "destino": "patio_central", "porta_destino": "patio_cantina"},
            {"peca": 6, "id": "cantina_deposito", "placa": "CÂMARA",
             "destino": "deposito_cantina", "porta_destino": "deposito_cantina"},
        ],
        "chao": "lajotas",
        "chao_trocas": {0: "tapete", 4: "tapete"},
        "objetos": [
            ("balcao_cantina", 300, 165), ("balcao_cantina", 420, 165, True),
            ("cacos_vidro", 220, 210), ("cacos_vidro", 320, 215), ("cacos_vidro", 420, 210),
            ("mesa_concreto", 120, 225), ("carrinho", 560, 215),
        ],
        "robos": [
            {
                "tipo": "rastreador", "pos": "(460, 220)",
                "rota": ["(180, 145)", "(460, 145)", "(540, 230)", "(180, 230)"],
            }
        ],
        "zonas_piso": [
            (0, 112, 160, 148, 0.6, "passadeira de borracha"),
            (160, 180, 320, 80, 2.0, "cacos de louça e vidro"),
            (480, 112, 160, 148, 0.6, "passadeira de borracha"),
        ],
        "luzes": [
            ("luz_tubo", 280, 34, "energy = 0.65"),
            ("luz_emergencia", 440, 34, "energy = 0.5"),
        ],
        "escuridao": (0.2, 0.21, 0.28, 1),
    },
    {
        "id": "deposito_cantina", "largura": 400, "altura": 240,
        "paredes": ["porta", "conduites", "fluorescente", "rachada", "painel_ciano"],
        "portas": [
            {"peca": 0, "id": "deposito_cantina", "placa": "CANTINA",
             "destino": "cantina", "porta_destino": "cantina_deposito"},
        ],
        "objetos": [
            ("estante_metal", 140, 145), ("estante_metal", 210, 145),
            ("gerador", 320, 185), ("caixas", 100, 215), ("tambor", 250, 215), ("latas", 180, 210),
        ],
        "itens": [("celula_energia", 290, 205), ("pilha", 140, 215)],
        "luzes": [
            ("luz_tubo", 200, 34, "energy = 0.6"),
            ("luz_fria", 320, 160, "color = Color(0.3, 0.9, 1, 1)", "energy = 0.75"),
        ],
        "escuridao": (0.18, 0.2, 0.26, 1),
    },
    {
        "id": "grafica_rapida", "largura": 480, "altura": 260,
        "paredes": ["porta", "mural", "conduites", "painel_ciano", "fluorescente", "porta"],
        "portas": [
            {"peca": 0, "id": "grafica_patio", "placa": "PÁTIO",
             "destino": "patio_central", "porta_destino": "patio_grafica"},
            {"peca": 5, "id": "grafica_posto", "placa": "MANUTENÇÃO",
             "destino": "posto_manutencao", "porta_destino": "posto_grafica"},
        ],
        "objetos": [
            ("bancada_eletronica", 160, 195), ("mesa_computador", 310, 205),
            ("estante_vazia", 110, 140), ("livros", 210, 230), ("caixas", 380, 225),
        ],
        "documentos": [("panfleto_universitario", 160, 210, "Ler o panfleto na bancada")],
        "painel_comutacao": (240, 132),
        "luzes": [
            ("luz_tubo", 360, 34, "energy = 0.7"),
            ("luz_fria", 240, 90, "color = Color(0.35, 0.85, 1, 1)", "energy = 0.6"),
        ],
        "escuridao": (0.22, 0.23, 0.3, 1),
    },
    {
        "id": "posto_manutencao", "largura": 400, "altura": 240,
        "paredes": ["porta", "mural", "conduites", "servidores", "arandela"],
        "portas": [
            {"peca": 0, "id": "posto_grafica", "placa": "GRÁFICA",
             "destino": "grafica_rapida", "porta_destino": "grafica_posto"},
        ],
        "chao": "tapete",
        "objetos": [
            ("colchao", 290, 205), ("mesa_metal", 180, 160), ("lampada", 235, 165),
            ("painel_distribuicao", 340, 145), ("caixas", 90, 215),
        ],
        "itens": [("pilha", 180, 185), ("clarao", 330, 215)],
        "documentos": [("ordem_manutencao_convivencia", 120, 134, "Ler a ordem de manutenção")],
        "checkpoint": ("conv_posto_seguro", 235, 190),
        "luzes": [
            ("luz_lampada", 235, 157, "energy = 0.85"),
            ("luz_tubo", 180, 34, "energy = 0.55"),
        ],
        "escuridao": (0.24, 0.24, 0.3, 1),
    },
    {
        "id": "rampa_subsolo", "largura": 640, "altura": 360,
        "paredes": ["porta", "rachada", "nicho_armario", "conduites", "painel_ciano", "arandela", "porta", "conduites"],
        "portas": [
            {"peca": 0, "id": "rampa_patio", "placa": "PÁTIO",
             "destino": "patio_central", "porta_destino": "patio_rampa"},
            {"peca": 6, "id": "rampa_bunker", "placa": "BUNKER",
             "liberada_por": "convivencia_energia",
             "aviso": "Comporta magnética travada. Relé de comutação na Gráfica sem alimentação primária.",
             "destino": "fim_da_convivencia", "porta_destino": ""},
        ],
        "comporta_rampa": 6,
        "chao": "lajotas",
        "chao_trocas": {1: "areia", 3: "areia"},
        "objetos": [
            ("caixas", 160, 210), ("tambor", 220, 240), ("mesa_concreto", 340, 270),
            ("entulho", 460, 220), ("torre_equipamentos", 420, 145), ("lampada", 560, 155),
        ],
        "robos": [
            {
                "tipo": "sentinela", "pos": "(360, 220)",
                "rota": ["(180, 160)", "(440, 160)", "(440, 310)", "(180, 310)"],
                "rota_energia": ["(160, 160)", "(520, 160)", "(520, 310)", "(260, 310)"],
            }
        ],
        "holofotes": [(320, 210), (500, 190)],
        "luzes": [
            ("luz_emergencia", 520, 34, "energy = 0.7"),
            ("luz_lampada", 560, 147, "energy = 0.6"),
            ("luz_fria", 280, 120, "color = Color(0.5, 0.65, 0.95, 1)", "energy = 0.6"),
        ],
        "escuridao": (0.2, 0.22, 0.32, 1),
    },
]


def main():
    montar_kit()
    for sala in SALAS:
        montar_sala(sala)
    montar_fim_convivencia()


if __name__ == "__main__":
    main()
