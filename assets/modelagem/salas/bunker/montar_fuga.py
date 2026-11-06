# montar_fuga.py — monta a cena da FUGA do fim do Bunker:
#   cenas/salas/bunker/fuga.tscn
#
# Como rodar (Python 3, sem bibliotecas):
#
#   python assets/modelagem/salas/bunker/montar_fuga.py
#
# O QUE É (Enredo Principal, seção 8, Ato 3)
#   Depois que o Henrique some e o Carlos fala pelos alto-falantes, o grupo
#   foge junto dos robôs por um corredor até a comporta do núcleo, que leva ao
#   Laboratório. Esta cena é esse corredor: uma animação (o jogador não
#   controla), feita com as peças do kit do bunker, no vermelho do alarme.
#
# QUEM ESTÁ NELA
#   - o Gabriel (o do modelo de sala), que corre sozinho para a direita;
#   - o grupo (Zane, Diana e Clarice) na frente dele, na mesma velocidade;
#   - os robôs atrás: o Ciborgue e mais dois, um pouco mais lentos que o grupo,
#     para a distância crescer devagar (a fuga dá certo).
#   O roteiro da cena (quando cada um corre e entra na comporta) está em
#   scripts/salas/fuga_do_bunker.gd.
#
# A GEOMETRIA
#   Peças de parede de 80 px e de chão de 128 px, como nas outras salas. A
#   comporta é a peça 18 (x = 1440): a porta dela fica em x = 1440 + 41, o
#   mesmo deslocamento das portas do bunker (montar_salas_bunker.py), e é o
#   X_DA_COMPORTA do script. Se mudar a peça de lugar, mude os dois.

import os

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "..", ".."))
DESTINO = os.path.join(PASTA_PROJETO, "cenas", "salas", "bunker", "fuga.tscn")

BUNKER = "res://cenas/cenario/bunker"
ROBOS = "res://assets/sprites/personagens/robos"
PECA, CHAO = 80, 128
LARGURA = 1600

PAREDES = ["bunker_lisa", "bunker_emergencia", "bunker_canos", "bunker_luminaria", "bunker_rachada",
           "bunker_emergencia", "bunker_porta_lacrada", "bunker_canos", "bunker_lisa", "bunker_emergencia",
           "bunker_rachada", "bunker_painel", "bunker_canos", "bunker_emergencia", "bunker_lisa",
           "bunker_porta_lacrada", "bunker_rachada", "bunker_emergencia", "bunker_comporta", "bunker_lisa"]

# (nome, cena, x, y): o grupo começa na frente do Gabriel (x = 220).
GRUPO = [("Clarice", "res://cenas/personagens/clarice_em_pe.tscn", 300, 156),
         ("Diana", "res://cenas/personagens/diana.tscn", 350, 146),
         ("Zane", "res://cenas/personagens/zane.tscn", 400, 152)]

# (nome, tira, quadros, escala, deslocamento, x, y, velocidade, altura da luz)
ROBOS_DA_FUGA = [
    ("Ciborgue", "ciborgue", 12, 0.5, (-56, -132), 120, 150, 104.0, -56),
    ("Cacador", "cacador", 8, 1.0, (-32, -44), 70, 140, 102.0, -23),
    ("Rastreador", "rastreador", 8, 1.0, (-32, -37), 30, 162, 103.0, -20),
]


class Montagem:
    def __init__(self):
        self.recursos = {}
        self.nos = []

    def recurso(self, tipo, caminho):
        if caminho not in self.recursos:
            self.recursos[caminho] = (tipo, f"r{len(self.recursos) + 1}")
        return self.recursos[caminho][1]

    def no(self, cabecalho, propriedades=()):
        self.nos.append((cabecalho, list(propriedades)))

    def instancia(self, nome, pai, caminho, propriedades=()):
        id_ = self.recurso("PackedScene", caminho)
        self.no(f'[node name="{nome}" parent="{pai}" instance=ExtResource("{id_}")]', propriedades)


def montar():
    m = Montagem()
    m.recurso("PackedScene", "res://cenas/salas/modelo_sala.tscn")
    script = m.recurso("Script", "res://scripts/salas/fuga_do_bunker.gd")
    script_robo = m.recurso("Script", "res://scripts/personagens/robo_de_cena.gd")
    luz = m.recurso("Texture2D", "res://assets/sprites/cenario/luzes/luz.png")
    sirene = m.recurso("AudioStream", "res://assets/audio/efeitos/objetos/sirene.wav")
    passo = m.recurso("AudioStream", "res://assets/audio/efeitos/robos/cacador_passo.wav")
    musica = m.recurso("AudioStream", "res://assets/audio/musica/perseguicao/labirinto_tensao.ogg")

    for i, peca in enumerate(PAREDES):
        m.instancia(f"Parede{i + 1:02d}", "Paredes", f"{BUNKER}/paredes/{peca}.tscn", [f"position = Vector2({i * PECA}, 0)"])
        if peca == "bunker_emergencia":
            m.instancia(f"Giroflex{i + 1:02d}", "Luzes", "res://cenas/cenario/luzes/luz_emergencia.tscn",
                        [f"position = Vector2({i * PECA + 40}, 30)"])
    m.instancia("PilarEsquerda", "Paredes", f"{BUNKER}/paredes/pilar_bunker.tscn", ["position = Vector2(0, 0)"])
    m.instancia("PilarDireita", "Paredes", f"{BUNKER}/paredes/pilar_bunker.tscn", [f"position = Vector2({LARGURA - 16}, 0)"])
    for c in range(-(-LARGURA // CHAO)):
        chao = "chao_bunker_faixa" if c * CHAO >= 1300 else ("chao_bunker_agua" if c % 3 else "chao_bunker")
        m.instancia(f"Chao{c + 1}", "Chao", f"{BUNKER}/chao/{chao}.tscn", [f"position = Vector2({c * CHAO}, 0)"])

    m.no('[node name="Gabriel" parent="Objetos"]', ["position = Vector2(220, 150)"])
    m.no('[node name="Grupo" type="Node2D" parent="Objetos"]', ["y_sort_enabled = true"])
    for nome, cena, x, y in GRUPO:
        m.instancia(nome, "Objetos/Grupo", cena, [f"position = Vector2({x}, {y})", 'vista = "lado"'])

    m.no('[node name="Robos" type="Node2D" parent="Objetos"]', ["y_sort_enabled = true"])
    for nome, tira, quadros, escala, (dx, dy), x, y, velocidade, altura_luz in ROBOS_DA_FUGA:
        corpo = m.recurso("Texture2D", f"{ROBOS}/{tira}_andar_lado.png")
        olhos = m.recurso("Texture2D", f"{ROBOS}/{tira}_andar_lado_olhos.png")
        m.no(f'[node name="{nome}" type="Node2D" parent="Objetos/Robos"]', [
            f"position = Vector2({x}, {y})", f'script = ExtResource("{script_robo}")',
            f"quadros = {quadros}", f"velocidade = {velocidade}"])
        for parte, textura, material in (("Corpo", corpo, None), ("Olhos", olhos, "SemLuz")):
            props = [f'texture = ExtResource("{textura}")', "centered = false",
                     f"scale = Vector2({escala}, {escala})", f"offset = Vector2({dx}, {dy})", f"hframes = {quadros}"]
            if material:
                props.insert(0, f'material = SubResource("{material}")')
            m.no(f'[node name="{parte}" type="Sprite2D" parent="Objetos/Robos/{nome}"]', props)
        m.no(f'[node name="LuzOlho" type="PointLight2D" parent="Objetos/Robos/{nome}"]', [
            f"position = Vector2(0, {altura_luz})", "color = Color(1, 0.28, 0.15, 1)", "energy = 0.6",
            f'texture = ExtResource("{luz}")', "texture_scale = 0.7"])

    m.no('[node name="Escuridao" parent="."]', ["color = Color(0.34, 0.2, 0.22, 1)"])
    m.no('[node name="Sirene" type="AudioStreamPlayer" parent="."]', [
        f'stream = ExtResource("{sirene}")', "volume_db = -8.0", "autoplay = true", 'bus = &"Efeitos"'])
    m.no('[node name="PassoDeRobo" type="AudioStreamPlayer" parent="."]', [
        f'stream = ExtResource("{passo}")', "volume_db = -6.0", 'bus = &"Efeitos"'])
    m.no('[node name="Musica" type="AudioStreamPlayer" parent="."]', [
        f'stream = ExtResource("{musica}")', "volume_db = -6.0", "autoplay = true", 'bus = &"Musica"'])

    linhas = ["[gd_scene format=3]", ""]
    for caminho, (tipo, id_) in m.recursos.items():
        linhas.append(f'[ext_resource type="{tipo}" path="{caminho}" id="{id_}"]')
    linhas += ["", '[sub_resource type="CanvasItemMaterial" id="SemLuz"]', "light_mode = 1", "",
               '[node name="Fuga" instance=ExtResource("r1")]', f'script = ExtResource("{script}")',
               'id = "bunker_fuga"', f"largura = {LARGURA}", "duracao_entrada = 0.6", ""]
    for cabecalho, propriedades in m.nos:
        linhas += [cabecalho] + propriedades + [""]
    with open(DESTINO, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(linhas))
    print(f"  sala: cenas/salas/bunker/fuga.tscn ({LARGURA} x 180)")


if __name__ == "__main__":
    montar()
