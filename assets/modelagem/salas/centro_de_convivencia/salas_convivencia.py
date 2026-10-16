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
}

# ---------------------------------------------------------------------------
# Passarela
# ---------------------------------------------------------------------------

PASSARELA = {
    "id": "passarela_acesso", "largura": 640, "altura": 180, "fundo": "fundo_passarela", "gabriel": "(96, 152)",
    "portas": [
        {"id": "passarela_subsolo", "coluna": 0, "y_peca": 0, "x": X_PORTA, "y": Y_PORTA_INTERNA, "bloqueada": True,
         "aviso": "A escotilha de manutenção travou por trás na subida."},
        porta_interna("passarela_praca", 6, "ciano", "praca_central", "praca_passarela"),
    ],
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
    "letreiros": [letreiro_da_loja(f"loja_{i}") for i in (1, 2, 3, 4)] + [("letreiro_entrada", 800, 2)],
    "objetos": OBJETOS_PRACA,
    "itens": [("pedra", 520, 400), ("pedra", 1000, 480), ("pedra", 1460, 400)],
    "nichos": [(440, 192), (1560, 192)],
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

SALAS = [PASSARELA, PRACA, LOJA_1, LOJA_2, CAMARA_FRIA, LOJA_3, LOJA_4]
