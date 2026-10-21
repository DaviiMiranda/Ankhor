# salas_convivencia.py — a DESCRIÇÃO das salas da fase Centro de Convivência
# (docs/fases/centro_de_convivencia.md), lida pelo montar_convivencia.py.
#
# Todas as posições são as do Godot: o "pé" do objeto (onde ele encosta no
# chão). As portas ficam em x = (coluna * 80) + 41 e y = (altura em que a
# parede encosta no chão) + 12.
#
# O mapa:
#
#                       passarela_acesso
#                              |
#                       [entrada da praça]
#        loja_2        loja_1  praca_central  loja_3        loja_4
#   (Self Nebulosa) (Tapioca)               (Pizzaria)   (Churrasco Solar)
#        |                                                      |
#   camara_fria                                         elevador de carga
#                                                       (para o Bunker)
#
#   A escada da praça (coluna 14) sobe para o segundo_andar (o mezanino), de onde
#   saem a grafica, a loja_uni e o cinema (mais embaixo, na seção "O segundo andar").

import sys
import os

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(PASTA_PROJETO, "assets", "modelagem", "cenario"))

import gerar_praca_base as base  # noqa: E402

PECA = base.PECA
X_PORTA = 41
Y_PORTA_INTERNA = 124


def espelhar_x(x, largura=base.LARGURA_PRACA):
    return largura - x


def porta_da_praca(loja, destino, porta_destino, **extras):
    coluna = base.LOJAS_PRACA[loja]
    y_base = base.y_base(coluna)
    return {"id": f"praca_{loja}", "coluna": coluna, "y_peca": y_base - base.ALTURA_PAREDE, "cor": base.COR_LOJA[loja],
            "x": coluna * PECA + X_PORTA, "y": y_base + 12, "destino": destino, "porta_destino": porta_destino, **extras}


def porta_interna(id_porta, coluna, cor, destino, porta_destino, **extras):
    return {"id": id_porta, "coluna": coluna, "y_peca": 0, "cor": cor, "x": coluna * PECA + X_PORTA, "y": Y_PORTA_INTERNA,
            "destino": destino, "porta_destino": porta_destino, **extras}


def letreiro_da_loja(loja):
    coluna = base.LOJAS_PRACA[loja]
    topo_da_fachada = base.y_base(coluna) - base.ALTURA_PAREDE
    return (f"letreiro_{loja}", (coluna - 1) * PECA, topo_da_fachada - 30)


COLUNA_ENTRADA = base.COLUNA_ENTRADA

COR_NEON_LUZ = {
    "ciano": "Color(0.45, 0.9, 1, 1)",
    "ambar": "Color(1, 0.7, 0.3, 1)",
    "verde": "Color(0.35, 1, 0.65, 1)",
    "vermelho": "Color(1, 0.4, 0.3, 1)",
    "magenta": "Color(1, 0.4, 0.85, 1)",
    "violeta": "Color(0.7, 0.5, 1, 1)",
    "azul": "Color(0.4, 0.62, 1, 1)",
    "limao": "Color(0.85, 1, 0.3, 1)",
}

# ---------------------------------------------------------------------------
# Passarela
# ---------------------------------------------------------------------------

PASSARELA = {
    "id": "passarela_acesso", "largura": 640, "altura": 180, "fundo": "fundo_passarela", "gabriel": "(96, 152)",
    "portas": [
        {"id": "passarela_subsolo", "coluna": 0, "y_peca": 0, "x": X_PORTA, "y": Y_PORTA_INTERNA, "bloqueada": True,
         "aviso": "A escotilha de manutenção travou por trás na subida."},
        porta_interna("passarela_sala_segura", 4, "verde", "sala_segura", "safe_room_saida"),
        porta_interna("passarela_praca", 6, "ciano", "praca_central", "praca_passarela"),
    ],
    "sinais_sala_segura": [(4 * PECA + X_PORTA, 4)],
    "objetos": [("vaso_planta", 330, 156), ("banco_curvo", 450, 160)],
    "itens": [("pilha", 360, 168), ("lanterna", 140, 160), ("radio", 180, 160)],
    "checkpoint": ("conv_passarela", 60, 140),
    "transmissoes": [("zane_convivencia_01", 220, 152, "")],
    "luzes": [
        ("luz_fria", 120, 50, "color = Color(0.5, 0.65, 0.95, 1)", "energy = 0.65"),
        ("luz_fria", 330, 60, "color = Color(0.45, 0.9, 1, 1)", "energy = 0.55"),
        ("luz_fria", 560, 50, "color = Color(0.5, 0.65, 0.95, 1)", "energy = 0.65"),
    ],
    "escuridao": (0.26, 0.28, 0.4, 1),
}

# ---------------------------------------------------------------------------
# A praça
# ---------------------------------------------------------------------------

MESAS_PRACA = [(560, 330), (470, 450), (800, 300), (840, 500)]


def conjunto_mesa(x, y, lado_esq=True):
    return [("mesa_holo", x, y), ("cadeira_fut", x - 38, y + 9), ("cadeira_fut", x + 38, y + 9, True)]


OBJETOS_PRACA = []
for (mx, my) in MESAS_PRACA:
    OBJETOS_PRACA += conjunto_mesa(mx, my)
    OBJETOS_PRACA += conjunto_mesa(espelhar_x(mx), my)
OBJETOS_PRACA += [
    ("arvore_cupula", 300, 452), ("arvore_cupula", 1700, 452), ("arvore_cupula", 200, 524), ("arvore_cupula", 1800, 524),
    ("holograma_central", 1000, 396),
    ("poste_luz", 705, 330), ("poste_luz", 705, 470), ("poste_luz", 1295, 330), ("poste_luz", 1295, 470),
    ("guarda_sol_holo", 700, 200), ("guarda_sol_holo", 1300, 200),
    ("banco_curvo", 790, 410), ("banco_curvo", 1210, 410, True),
    ("vaso_planta", 900, 178), ("vaso_planta", 1100, 178),
    ("totem_pedidos", 640, 206), ("totem_pedidos", 1360, 206), ("totem_pedidos", 340, 300), ("totem_pedidos", 1660, 300),
]

PRACA = {
    "id": "praca_central", "largura": base.LARGURA_PRACA, "altura": base.ALTURA_PRACA, "fundo": "fundo_praca",
    "arco": True, "acende_com_energia": True, "gabriel": "(1040, 150)",
    "portas": [
        {"id": "praca_passarela", "coluna": COLUNA_ENTRADA, "y_peca": 0, "cor": "ciano",
         "x": COLUNA_ENTRADA * PECA + X_PORTA, "y": base.y_base(COLUNA_ENTRADA) + 12,
         "destino": "passarela_acesso", "porta_destino": "passarela_praca"},
        porta_da_praca("loja_1", "loja_1", "loja_1_praca"),
        porta_da_praca("loja_2", "loja_2", "loja_2_praca"),
        porta_da_praca("loja_3", "loja_3", "loja_3_praca"),
        porta_da_praca("loja_4", "loja_4", "loja_4_praca"),
    ],
    "letreiros": [letreiro_da_loja(f"loja_{i}") for i in (1, 2, 3, 4)] + [("letreiro_entrada", 880, 2)],
    "objetos": OBJETOS_PRACA,
    "itens": [("pedra", 520, 400), ("pedra", 1000, 480), ("pedra", 1460, 400)],
    "nichos": [(440, 192), (1560, 192)],
    "sinais_sala_segura": [(base.LOJAS_PRACA["loja_1"] * PECA + 40, base.y_base(base.LOJAS_PRACA["loja_1"]) - 108)],
    "transmissoes": [("zane_convivencia_02", 1000, 300, "convivencia_energia")],
    "luzes": [
        *[("luz_fria", base.LOJAS_PRACA[loja] * PECA + X_PORTA, base.y_base(base.LOJAS_PRACA[loja]) + 34,
           f"color = {COR_NEON_LUZ[base.COR_LOJA[loja]]}", "energy = 0.6", "scale = Vector2(2.8, 1.7)")
          for loja in base.LOJAS_PRACA],
        ("luz_fria", COLUNA_ENTRADA * PECA + X_PORTA, 150, f"color = {COR_NEON_LUZ['ciano']}", "energy = 0.55", "scale = Vector2(3.2, 1.8)"),
        ("luz_fria", 380, 300, "color = Color(0.5, 0.65, 0.98, 1)", "energy = 0.4", "scale = Vector2(5, 3.5)"),
        ("luz_fria", 1620, 300, "color = Color(0.5, 0.65, 0.98, 1)", "energy = 0.4", "scale = Vector2(5, 3.5)"),
        ("luz_fria", 700, 480, "color = Color(0.5, 0.65, 0.98, 1)", "energy = 0.35", "scale = Vector2(5, 3)"),
        ("luz_fria", 1300, 480, "color = Color(0.5, 0.65, 0.98, 1)", "energy = 0.35", "scale = Vector2(5, 3)"),
    ],
    "holofotes": [(520, 300), (800, 420), (1200, 420), (1480, 300)],
    "robos": [
        {"tipo": "sentinela", "pos": "(500, 262)",
         "rota": ["(380, 262)", "(940, 262)", "(940, 540)", "(380, 540)"],
         "rota_energia": ["(380, 262)", "(660, 262)", "(660, 540)", "(940, 540)", "(940, 262)"]},
        {"tipo": "sentinela", "pos": "(1500, 262)",
         "rota": ["(1620, 262)", "(1060, 262)", "(1060, 540)", "(1620, 540)"],
         "rota_energia": ["(1620, 262)", "(1340, 262)", "(1340, 540)", "(1060, 540)", "(1060, 262)"]},
    ],
    "zonas_piso": [
        (0, 112, 700, 448, 0.7, "pedra rachada e musgo"),
        (700, 112, 600, 448, 1.0, "emblema de pedra"),
        (1300, 112, 700, 448, 0.7, "pedra rachada e musgo"),
    ],
    "escuridao": (0.3, 0.34, 0.48, 1),
}

# ---------------------------------------------------------------------------
# Restaurantes
# ---------------------------------------------------------------------------

LOJA_1 = {
    "id": "loja_1", "largura": 400, "altura": 240, "fundo": "fundo_loja_1", "gabriel": "(80, 160)",
    "portas": [porta_interna("loja_1_praca", 0, "ambar", "praca_central", "praca_loja_1")],
    "objetos": [
        ("balcao_tapioca", 200, 146), ("maquina_cafe", 300, 138), ("estufa_salgados", 350, 144),
        ("mesa_cafe", 110, 204), ("banqueta", 80, 212), ("banqueta", 140, 212),
        ("mesa_cafe", 300, 218), ("banqueta", 270, 226), ("banqueta", 330, 226, True),
    ],
    "itens": [("pilha", 190, 190), ("clarao", 350, 190)],
    "documentos": [("ordem_manutencao_convivencia", 125, 152, "Ler a ordem de serviço")],
    "checkpoint": ("conv_posto_seguro", 235, 190),
    "luzes": [
        ("luz_lampada", 235, 157, "energy = 0.85"),
        ("luz_lampada", 100, 120, "energy = 0.6"),
        ("luz_fria", 330, 100, "color = Color(1, 0.7, 0.3, 1)", "energy = 0.5"),
    ],
    "escuridao": (0.32, 0.29, 0.3, 1),
}

# O cofre do bufê do Self Nebulosa: o bilhete da gerência (perto da porta) diz
# que a senha são as cubas do prato do dia, na ordem do cardápio; o cardápio
# está em cima do bufê, no meio do salão, perto dos cacos e do Rastreador.
# Prato do dia: baião de dois (6), paçoca (1) e vinagrete (9).
CODIGO_DO_COFRE_DO_BUFE = "619"

LOJA_2 = {
    "id": "loja_2", "largura": 640, "altura": 280, "fundo": "fundo_loja_2", "gabriel": "(80, 160)",
    "portas": [
        porta_interna("loja_2_praca", 0, "verde", "praca_central", "praca_loja_2"),
        porta_interna("loja_2_camara", 6, "ciano", "camara_fria", "camara_loja_2"),
    ],
    "objetos": [
        ("bufe", 258, 154), ("rack_bandejas", 150, 154), ("lixeira_reciclagem", 600, 150),
        ("mesa_vidro", 200, 240), ("cadeira_fut", 160, 248), ("cadeira_fut", 242, 248, True),
        ("mesa_vidro", 400, 236), ("cadeira_fut", 360, 244), ("cadeira_fut", 442, 244, True),
        ("mesa_vidro", 580, 250), ("cadeira_fut", 540, 258),
    ],
    "decais": [("cacos_louca", 250, 205), ("cacos_louca", 340, 212), ("cacos_louca", 430, 205)],
    "documentos": [
        ("bilhete_cofre_bufe", 100, 174, "Ler o bilhete da gerência"),
        ("cardapio_self_nebulosa", 258, 172, "Ler o cardápio do dia"),
    ],
    "cofres": [(440, 152, CODIGO_DO_COFRE_DO_BUFE, "clarao", 1, "cofre_bufe_aberto",
                "O cofre do bufê abriu: caiu uma cápsula de clarão.")],
    "nichos": [(360, 128)],
    "robos": [{"tipo": "rastreador", "pos": "(460, 220)", "rota": ["(180, 160)", "(480, 160)", "(540, 245)", "(180, 245)"]}],
    "zonas_piso": [
        (0, 112, 160, 168, 0.6, "passadeira de borracha"),
        (160, 180, 320, 100, 2.0, "cacos de louça e vidro"),
        (480, 112, 160, 168, 0.6, "passadeira de borracha"),
    ],
    "luzes": [
        ("luz_fria", 160, 90, "color = Color(0.35, 1, 0.65, 1)", "energy = 0.6"),
        ("luz_fria", 420, 90, "color = Color(0.35, 1, 0.65, 1)", "energy = 0.6"),
        ("luz_tubo", 300, 34, "energy = 0.55"),
    ],
    "escuridao": (0.25, 0.3, 0.3, 1),
}

CAMARA_FRIA = {
    "id": "camara_fria", "largura": 400, "altura": 240, "fundo": "fundo_camara", "gabriel": "(80, 160)",
    "portas": [porta_interna("camara_loja_2", 0, "ciano", "loja_2", "loja_2_camara")],
    "objetos": [
        ("prateleira_fria", 160, 158), ("prateleira_fria", 250, 158), ("gerador_frio", 335, 152),
        ("tanque_cripto", 365, 218), ("caixas_termicas", 110, 218), ("caixas_termicas", 200, 228),
    ],
    "itens": [("celula_energia", 290, 205), ("pilha", 150, 205)],
    "luzes": [
        ("luz_fria", 200, 80, "color = Color(0.5, 0.9, 1, 1)", "energy = 0.8"),
        ("luz_fria", 340, 140, "color = Color(0.3, 0.9, 1, 1)", "energy = 0.7"),
    ],
    "escuridao": (0.22, 0.27, 0.34, 1),
}

LOJA_3 = {
    "id": "loja_3", "largura": 480, "altura": 260, "fundo": "fundo_loja_3", "gabriel": "(80, 160)",
    "portas": [porta_interna("loja_3_praca", 0, "vermelho", "praca_central", "praca_loja_3")],
    "objetos": [
        ("forno_plasma", 122, 150), ("bancada_inox", 250, 150), ("mesa_pizza", 170, 222), ("mesa_pizza", 340, 232),
        ("caixas_pizza", 440, 152),
    ],
    "documentos": [("panfleto_universitario", 215, 156, "Ler o panfleto na bancada")],
    "painel_comutacao": (330, 134),
    "luzes": [
        ("luz_fria", 125, 110, "color = Color(1, 0.45, 0.2, 1)", "energy = 0.85"),
        ("luz_tubo", 300, 34, "energy = 0.6"),
        ("luz_fria", 400, 130, "color = Color(1, 0.4, 0.3, 1)", "energy = 0.4"),
    ],
    "escuridao": (0.3, 0.25, 0.25, 1),
}

# O quadro do bar do Churrasco Solar: o checklist (no chão, perto do balcão)
# dá a ordem pelos nomes (exaustor antes da grelha, a geladeira depois da
# grelha, o neon por último); o quadro mostra o nome de cada disjuntor. Errar
# faz um estalo que a Sentinela ouve (ruido_ao_desarmar, em células de 16 px).
ORDEM_DO_QUADRO_DO_BAR = "2, 4, 1, 3"

LOJA_4 = {
    "id": "loja_4", "largura": 640, "altura": 360, "fundo": "fundo_loja_4", "gabriel": "(80, 160)",
    "portas": [
        porta_interna("loja_4_praca", 0, "magenta", "praca_central", "praca_loja_4"),
        {"id": "loja_4_elevador", "coluna": 7, "y_peca": 0, "x": 7 * PECA + X_PORTA, "y": Y_PORTA_INTERNA,
         "liberada_por": "convivencia_energia", "destino": "fim_da_convivencia", "porta_destino": "",
         "aviso": "Elevador de carga sem alimentação. O quadro de comutação da cozinha da Pizzaria Quasar está desligado."},
    ],
    "comporta": {"textura": "elevador_carga", "x": 7 * PECA + 8, "y": 28},
    "objetos": [
        ("grelha_solar", 175, 170), ("balcao_bar", 350, 178),
        ("banqueta_alta", 290, 200), ("banqueta_alta", 335, 200), ("banqueta_alta", 380, 200), ("banqueta_alta", 425, 200),
        ("mesa_vidro", 170, 290), ("cadeira_fut", 130, 298), ("cadeira_fut", 212, 298, True),
        ("mesa_vidro", 450, 310), ("cadeira_fut", 410, 318), ("cadeira_fut", 492, 318, True),
        ("caixas_carga", 560, 250),
    ],
    "nichos": [(360, 128)],
    "documentos": [("checklist_churrasco_solar", 240, 194, "Ler o checklist do bar")],
    "paineis": [{
        "nome": "QuadroDoBar", "cena": "quadro_energia", "x": 490, "y": 132, "premio": ("pilha", 2),
        "campos": [
            'texto_acao = "Abrir o quadro do bar"', 'titulo = "QUADRO DO BAR"', 'marca = "churrasco_quadro_ligado"',
            f"ordem = PackedInt32Array({ORDEM_DO_QUADRO_DO_BAR})",
            'nomes = PackedStringArray("GELAD", "EXAUST", "NEON", "GRELHA")', "ruido_ao_desarmar = 14",
            'aviso_ligado = "Quadro do bar ligado. A gaveta de reserva destravou: duas pilhas."',
            'aviso_ja_ligado = "O quadro do bar já está ligado."',
        ],
    }],
    "robos": [{"tipo": "sentinela", "pos": "(400, 250)",
               "rota": ["(180, 240)", "(520, 240)", "(520, 335)", "(180, 335)"],
               "rota_energia": ["(160, 250)", "(560, 300)", "(560, 335)", "(260, 335)"]}],
    "holofotes": [(320, 210), (500, 200)],
    "luzes": [
        ("luz_fria", 175, 120, "color = Color(1, 0.4, 0.85, 1)", "energy = 0.8"),
        ("luz_fria", 360, 110, "color = Color(1, 0.4, 0.85, 1)", "energy = 0.7"),
        ("luz_emergencia", 580, 40, "energy = 0.6"),
    ],
    "escuridao": (0.26, 0.22, 0.3, 1),
}

# ---------------------------------------------------------------------------
# O segundo andar (o mezanino)
# ---------------------------------------------------------------------------
#
# A praça tem uma escada ao lado da entrada (coluna 14) que sobe para o
# mezanino, um anel em volta do vazio com a Gráfica Quântica e a Loja
# Universitária de um lado e o Cine Andrômeda do outro (a planta do Davi). A
# escada da coluna 10 está interditada. O corredor do mezanino é uma faixa de
# 112 px que acompanha o arco (ver gerar_andar2.py), com o corrimão na frente.
#
#                  praca_central ── escada ──► segundo_andar
#                                                  │
#                      ┌───────────────────────────┼─────────────────────────┐
#                    grafica                   loja_uni                    cinema


def no_corredor(coluna, fundo):
    """O ponto do corredor na coluna: o meio dela e 'fundo' px abaixo da
    parede."""
    return (coluna * PECA + PECA // 2, base.y_base(coluna) + fundo)


def porta_do_mezanino(loja, destino, porta_destino, **extras):
    coluna = base.LOJAS_ANDAR2[loja]
    y_base = base.y_base(coluna)
    return {"id": f"mezanino_{loja}", "coluna": coluna, "y_peca": y_base - base.ALTURA_PAREDE, "cor": base.COR_LOJA[loja],
            "x": coluna * PECA + X_PORTA, "y": y_base + 12, "destino": destino, "porta_destino": porta_destino, **extras}


def letreiro_do_mezanino(loja):
    coluna = base.LOJAS_ANDAR2[loja]
    topo_da_fachada = base.y_base(coluna) - base.ALTURA_PAREDE
    return (f"letreiro_{loja}", (coluna - 1) * PECA, topo_da_fachada - 30)


def ronda_do_corredor(primeira, ultima, fundo=56):
    """A rota de ida e volta da Sentinela: um ponto no meio de cada coluna,
    na faixa de andar do corredor (fundo px abaixo da parede)."""
    colunas = list(range(primeira, ultima + 1))
    ida = [f"({c * PECA + PECA // 2}, {base.y_base(c) + fundo})" for c in colunas]
    volta = ida[-2:0:-1]
    return ida + volta


PORTAS_ESCADA_DA_PRACA = [
    {"id": "praca_escada", "coluna": base.COLUNA_ESCADA_PRACA, "y_peca": 0, "x": base.COLUNA_ESCADA_PRACA * PECA + X_PORTA,
     "y": base.y_base(base.COLUNA_ESCADA_PRACA) + 12, "destino": "segundo_andar", "porta_destino": "mezanino_escada",
     "som": "escada"},
    {"id": "praca_escada_interditada", "coluna": base.COLUNA_ESCADA_INTERDITADA, "y_peca": 0,
     "x": base.COLUNA_ESCADA_INTERDITADA * PECA + X_PORTA, "y": base.y_base(base.COLUNA_ESCADA_INTERDITADA) + 12,
     "bloqueada": True, "aviso": "Escada de emergência interditada: fiação exposta e avisos de área interditada."},
]

OBJETOS_MEZANINO = [
    ("jardineira", 44, base.y_base(0) + 40),
    ("maquina_venda", *no_corredor(4, 32)),
    ("banco_mirante", *no_corredor(9, 80)),
    ("luminaria_chao", 862, base.y_base(10) + 30),
    ("diretorio_holo", 912, base.y_base(11) + 36),
    ("banco_mirante", 960, base.y_base(12) + 90),
    ("banco_mirante", 1040, base.y_base(12) + 90, True),
    ("diretorio_holo", 1088, base.y_base(13) + 36),
    ("luminaria_chao", 1138, base.y_base(14) + 30),
    ("maquina_venda", *no_corredor(16, 32), True),
    ("jardineira", *no_corredor(18, 40)),
    ("cadeira_espera", *no_corredor(20, 94)),
    ("carrinho_limpeza", 1700, base.y_base(21) + 94),
    ("jardineira", 1956, base.y_base(24) + 40),
]

MEZANINO = {
    "id": "segundo_andar", "largura": base.ANDAR2_LARGURA, "altura": base.ANDAR2_ALTURA, "fundo": "fundo_andar2",
    "arco": True, "balcao": True, "corrimao": "corrimao_andar2", "acende_com_energia": True, "gabriel": "(1001, 140)",
    "portas": [
        {"id": "mezanino_escada", "coluna": base.COLUNA_ESCADA_MEZANINO, "y_peca": 0, "x": base.COLUNA_ESCADA_MEZANINO * PECA + X_PORTA,
         "y": base.y_base(base.COLUNA_ESCADA_MEZANINO) + 12, "destino": "praca_central", "porta_destino": "praca_escada",
         "som": "escada"},
        porta_do_mezanino("grafica", "grafica", "grafica_mezanino"),
        porta_do_mezanino("loja_uni", "loja_uni", "loja_uni_mezanino"),
        porta_do_mezanino("cinema", "cinema", "cinema_mezanino"),
    ],
    "letreiros": [letreiro_do_mezanino(loja) for loja in ("grafica", "loja_uni", "cinema")] + [("letreiro_mezanino", 880, 2)],
    "objetos": OBJETOS_MEZANINO,
    "itens": [("pedra", 330, base.y_base(4) + 88), ("pedra", 1440, base.y_base(18) + 84), ("pilha", 1880, base.y_base(23) + 72)],
    "nichos": [(440, base.y_base(5) + 16), (1560, base.y_base(19) + 16)],
    "luzes": [
        *[("luz_fria", base.LOJAS_ANDAR2[loja] * PECA + X_PORTA, base.y_base(base.LOJAS_ANDAR2[loja]) + 34,
           f"color = {COR_NEON_LUZ[base.COR_LOJA[loja]]}", "energy = 0.6", "scale = Vector2(2.8, 1.7)")
          for loja in base.LOJAS_ANDAR2],
        ("luz_fria", COLUNA_ENTRADA * PECA + X_PORTA, 150, f"color = {COR_NEON_LUZ['ciano']}", "energy = 0.55", "scale = Vector2(3.2, 1.8)"),
        ("luz_fria", 520, base.y_base(6) + 70, "color = Color(0.5, 0.65, 0.98, 1)", "energy = 0.35", "scale = Vector2(5, 3)"),
        ("luz_fria", 1480, base.y_base(18) + 70, "color = Color(0.5, 0.65, 0.98, 1)", "energy = 0.35", "scale = Vector2(5, 3)"),
        ("luz_fria", 120, base.y_base(1) + 70, "color = Color(0.5, 0.65, 0.98, 1)", "energy = 0.3", "scale = Vector2(4, 3)"),
        ("luz_fria", 1880, base.y_base(23) + 70, "color = Color(0.5, 0.65, 0.98, 1)", "energy = 0.3", "scale = Vector2(4, 3)"),
    ],
    "robos": [
        {"tipo": "sentinela", "pos": f"({3 * PECA + 40}, {base.y_base(3) + 56})", "rota": ronda_do_corredor(3, 21)},
    ],
    "zonas_piso": [(0, 112, base.ANDAR2_LARGURA, 528, 1.0, "chapa de aço")],
    "escuridao": (0.24, 0.27, 0.4, 1),
}

# ---------------------------------------------------------------------------
# Lojas do mezanino
# ---------------------------------------------------------------------------

# A arara inteligente da Loja Universitária: os moletons estão fora de ordem e
# o Gabriel troca dois vizinhos de cada vez até ficar do PP ao GG. A ordem
# inicial (G, PP, GG, M, P) tem 6 inversões, o mínimo de trocas.
ORDEM_INICIAL_DA_ARARA = "3, 0, 4, 2, 1"

LOJA_UNI = {
    "id": "loja_uni", "largura": 560, "altura": 240, "fundo": "fundo_loja_uni", "gabriel": "(80, 160)",
    "portas": [porta_interna("loja_uni_mezanino", 0, "azul", "segundo_andar", "mezanino_loja_uni")],
    "objetos": [
        ("manequim_uni", 140, 152), ("arara_a", 215, 156), ("balcao_caixa_uni", 330, 152),
        ("mesa_dobrados", 160, 208), ("arara_b", 262, 214), ("estante_moletons", 372, 216), ("cesto_promocao", 452, 208),
        ("espelho_standing", 526, 206),
    ],
    "itens": [("pilha", 110, 228), ("pedra", 330, 232)],
    "documentos": [("aviso_loja_universitaria", 330, 170, "Ler o aviso do balcão")],
    "paineis": [{
        "nome": "AraraInteligente", "cena": "painel_ordenacao", "x": 215, "y": 160, "premio": ("pilha", 2),
        "campos": [
            'marca = "arara_loja_uni_ordenada"', 'pedido = "DO PP AO GG, DA ESQUERDA PARA A DIREITA"',
            'ordem_certa = PackedStringArray("PP", "P", "M", "G", "GG")',
            f"ordem_inicial = PackedInt32Array({ORDEM_INICIAL_DA_ARARA})",
            'aviso_ordenado = "A arara apitou: tudo em ordem. Caíram duas pilhas de um bolso."',
        ],
    }],
    "nichos": [(440, 128)],
    "luzes": [
        ("luz_lampada", 150, 100, "energy = 0.7"),
        ("luz_fria", 330, 100, "color = Color(0.4, 0.62, 1, 1)", "energy = 0.55"),
        ("luz_fria", 490, 110, "color = Color(0.4, 0.62, 1, 1)", "energy = 0.4"),
    ],
    "zonas_piso": [(0, 112, 560, 128, 0.5, "carpete macio")],
    "escuridao": (0.28, 0.3, 0.42, 1),
}

# A trava do plotter da Gráfica Quântica: a etiqueta diz que o código é quantos
# avisos ainda faltam imprimir na ordem parada; a Ordem de Impressão diz 4.000
# pedidos e 3.912 impressos: faltam 88 = 64 + 16 + 8 = 1011000 em binário.
CODIGO_DA_TRAVA_DO_PLOTTER = 4000 - 3912

GRAFICA = {
    "id": "grafica", "largura": 560, "altura": 240, "fundo": "fundo_grafica", "gabriel": "(80, 160)",
    "portas": [porta_interna("grafica_mezanino", 0, "limao", "segundo_andar", "mezanino_grafica")],
    "objetos": [
        ("plotter_grande", 180, 206), ("copiadora", 365, 206), ("estante_resmas", 268, 156), ("impressora_3d", 452, 160),
        ("guilhotina", 62, 226), ("balcao_grafica", 275, 234), ("mesa_corte", 478, 228), ("rolo_papel", 56, 186),
    ],
    "itens": [("pedra", 400, 184), ("pedra", 110, 192), ("pilha", 520, 196)],
    "documentos": [
        ("ordem_impressao_grafica", 275, 216, "Ler a ordem de impressão"),
        ("etiqueta_trava_plotter", 140, 214, "Ler a etiqueta do plotter"),
    ],
    "paineis": [{
        "nome": "TravaDoPlotter", "cena": "painel_bits", "x": 180, "y": 212, "premio": ("clarao", 1),
        "campos": [
            'texto_acao = "Mexer na trava do plotter"', 'titulo = "PLOTTER QX-9: TRAVA"', 'marca = "plotter_destravado"',
            f"alvo = {CODIGO_DA_TRAVA_DO_PLOTTER}", "quantidade_chaves = 7",
            'aviso_liberado = "A gaveta de insumos do plotter abriu: tinha uma cápsula de clarão."',
            'aviso_ja_liberado = "A gaveta do plotter já está aberta."',
        ],
    }],
    "nichos": [(520, 128)],
    "luzes": [
        ("luz_tubo", 180, 36, "energy = 0.55"),
        ("luz_tubo", 400, 36, "energy = 0.5"),
        ("luz_fria", 300, 100, "color = Color(0.85, 1, 0.3, 1)", "energy = 0.35"),
    ],
    "zonas_piso": [(0, 112, 560, 128, 1.0, "concreto polido")],
    "escuridao": (0.28, 0.3, 0.28, 1),
}

# O cofre do cinema fica na cabine de projeção (a salinha atrás da tela): o
# lanterninha diz que o código são as poltronas do Léo (4), da Bia (7) e do Caio
# (2), numa ordem embaralhada. A ordem certa é Bia, Caio, Léo.
CODIGO_DO_COFRE_DO_CINEMA = "724"

CINEMA = {
    "id": "cinema", "largura": 1040, "altura": 320, "fundo": "fundo_cinema", "gabriel": "(80, 160)",
    "portas": [
        porta_interna("cinema_mezanino", 0, "violeta", "segundo_andar", "mezanino_cinema"),
        porta_interna("cinema_cabine", 12, "ciano", "cinema_cabine", "cabine_cinema"),
    ],
    "objetos": [
        ("balcao_pipoca", 190, 158), ("bilheteria_balcao", 120, 216), ("cordao_fila", 250, 214), ("cordao_fila", 320, 214, True),
        ("standee_filme", 38, 204), ("standee_filme", 600, 236, True), ("jardineira", 284, 156),
        ("fliperama", 346, 154), ("fliperama", 386, 154), ("sofa_veludo", 520, 182), ("luminaria_chao", 470, 232),
        ("poltronas_1", 690, 188), ("poltronas_5", 800, 188), ("poltronas_9", 880, 188), ("poltronas_13", 990, 188),
        ("poltronas_1", 690, 240), ("poltronas_5", 800, 240), ("poltronas_9", 880, 240), ("poltronas_13", 990, 240),
        ("poltronas_1", 690, 292), ("poltronas_5", 800, 292), ("poltronas_9", 880, 292), ("poltronas_13", 990, 292),
    ],
    "animados": [("tela_cinema", 725, 18, "chiado")],
    "itens": [("pilha", 60, 290), ("pedra", 520, 284), ("pedra", 930, 150)],
    "documentos": [
        ("ingresso_cine_andromeda", 160, 236, "Ler o canhoto do ingresso"),
        ("bilhete_lanterninha_cofre", 190, 176, "Ler o bilhete do lanterninha"),
        ("canhoto_leo", 470, 268, "Ler o canhoto"),
        ("canhoto_bia", 780, 266, "Ler o canhoto"),
    ],
    "nichos": [(440, 128)],
    "luzes": [
        ("luz_lampada", 150, 90, "energy = 0.7"),
        ("luz_fria", 280, 100, "color = Color(0.7, 0.5, 1, 1)", "energy = 0.45"),
        ("luz_fria", 420, 100, "color = Color(1, 0.7, 0.3, 1)", "energy = 0.4"),
        ("luz_fria", 560, 120, "color = Color(0.7, 0.5, 1, 1)", "energy = 0.45", "scale = Vector2(5, 3)"),
        ("luz_fria", 840, 150, "color = Color(0.8, 0.85, 1, 1)", "energy = 0.55", "scale = Vector2(7, 4)"),
    ],
    "zonas_piso": [(0, 112, 1040, 208, 0.5, "carpete de veludo")],
    "escuridao": (0.24, 0.2, 0.3, 1),
}

PRACA["portas"] += PORTAS_ESCADA_DA_PRACA
PRACA["luzes"].append(("luz_fria", base.COLUNA_ESCADA_PRACA * PECA + X_PORTA, 150, f"color = {COR_NEON_LUZ['ciano']}", "energy = 0.45", "scale = Vector2(2.6, 1.6)"))

CINEMA_CABINE = {
    "id": "cinema_cabine", "largura": 400, "altura": 220, "fundo": "fundo_cabine", "gabriel": "(80, 160)",
    "portas": [porta_interna("cabine_cinema", 0, "ciano", "cinema", "cinema_cabine")],
    "objetos": [
        ("projetor_cinema", 196, 160), ("mesa_lanterninha", 120, 208), ("caixas_rolos", 52, 198), ("caixas_rolos", 362, 208),
    ],
    "documentos": [("canhoto_caio", 160, 196, "Ler o canhoto")],
    "cofres": [(340, 152, CODIGO_DO_COFRE_DO_CINEMA, "clarao", 1, "cofre_cinema_aberto",
                "O cofre abriu: caiu uma cápsula de clarão.")],
    "itens": [("pilha", 262, 196)],
    "luzes": [
        ("luz_lampada", 200, 90, "energy = 0.7"),
        ("luz_fria", 130, 100, "color = Color(0.7, 0.5, 1, 1)", "energy = 0.5"),
        ("luz_fria", 330, 120, "color = Color(0.45, 0.9, 1, 1)", "energy = 0.4"),
    ],
    "zonas_piso": [(0, 112, 400, 108, 1.0, "concreto")],
    "escuridao": (0.26, 0.22, 0.32, 1),
}

SALAS = [PASSARELA, PRACA, LOJA_1, LOJA_2, CAMARA_FRIA, LOJA_3, LOJA_4, MEZANINO, LOJA_UNI, GRAFICA, CINEMA, CINEMA_CABINE]
