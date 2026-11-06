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
#   Laboratório. Esta cena é esse corredor, JOGÁVEL: o jogador corre com o
#   Gabriel (estamina infinita aqui) e desvia dos tiros saindo da linha deles.
#   Feita com as peças do kit do bunker, no vermelho do alarme.
#
# QUEM ESTÁ NELA
#   - o Gabriel (o do modelo de sala), com o jogador;
#   - o grupo (Clarice, Diana e Zane), que corre sempre um pouco à frente dele
#     (scripts/salas/fuga_do_bunker.gd);
#   - os robôs atrás (scripts/personagens/robo_de_cena.gd): o Ciborgue, que só
#     persegue, e atiradores (o corpo da Sentinela, como o robô atirador do
#     Centro de Convivência), que ficam a uma distância, miram e atiram. Alguns
#     só aparecem quando o Gabriel passa de um ponto do corredor, como se
#     saíssem de uma porta atrás dele.
#
# AS VELOCIDADES (px/s)
#   Quem só persegue (Ciborgue, Caçador) acompanha a altura do Gabriel a
#   60 px/s, para encostar nele; os atiradores, a 26, para a mira dar tempo
#   de desviar.
#   Gabriel andando 60, correndo 108 em linha reta e uns 76 na diagonal (a
#   direção é normalizada antes: desviar custa velocidade). Robôs de 82 a 88.
#   Andando, os robôs o alcançam; correndo reto, ele abre distância; correndo
#   e desviando o tempo todo, o Ciborgue encosta devagar. O grupo anda até 150, para
#   nunca ficar para trás.
#
# A GEOMETRIA
#   Peças de parede de 80 px e de chão de 128 px, como nas outras salas. A
#   comporta é a peça 38 (x = 3040): a porta dela fica em x = 3040 + 41, o
#   mesmo deslocamento das portas do bunker (montar_salas_bunker.py), e é o
#   X_DA_COMPORTA do script. Se mudar a peça de lugar, mude os dois.

import os

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.normpath(os.path.join(PASTA_SCRIPT, "..", "..", "..", ".."))
DESTINO = os.path.join(PASTA_PROJETO, "cenas", "salas", "bunker", "fuga.tscn")

BUNKER = "res://cenas/cenario/bunker"
ROBOS = "res://assets/sprites/personagens/robos"
PECA, CHAO = 80, 128
LARGURA = 3200
PECA_DA_COMPORTA = 38

# Um trecho de oito peças que se repete; a comporta entra na peça 38.
TRECHO = ["bunker_lisa", "bunker_emergencia", "bunker_canos", "bunker_porta_lacrada",
          "bunker_rachada", "bunker_emergencia", "bunker_painel", "bunker_canos"]
PAREDES = [TRECHO[i % len(TRECHO)] for i in range(LARGURA // PECA)]
PAREDES[PECA_DA_COMPORTA] = "bunker_comporta"
PAREDES[PECA_DA_COMPORTA + 1] = "bunker_lisa"

# (nome, cena, x, y): o grupo começa na frente do Gabriel (x = 240).
GRUPO = [("Clarice", "res://cenas/personagens/clarice_em_pe.tscn", 320, 158),
         ("Diana", "res://cenas/personagens/diana.tscn", 360, 140),
         ("Zane", "res://cenas/personagens/zane.tscn", 400, 152)]

# Os corpos dos robôs: (tira, quadros, escala, deslocamento, altura da luz)
CIBORGUE = ("ciborgue", 12, 0.5, (-56, -132), -56)
ATIRADOR = ("sentinela", 8, 1.0, (-36, -69), -40)
CACADOR = ("cacador", 8, 1.0, (-32, -44), -23)

# (nome, corpo, x, y, velocidade, distância que mantém do Gabriel, atira,
#  aparece quando o Gabriel passa de x; -1 = desde o começo)
ROBOS_DA_FUGA = [
    ("Ciborgue", CIBORGUE, 130, 150, 82.0, 0, False, -1),
    ("Atirador1", ATIRADOR, 80, 136, 86.0, 120, True, -1),
    ("Atirador2", ATIRADOR, 30, 166, 84.0, 160, True, -1),
    ("Atirador3", ATIRADOR, 1240, 150, 88.0, 130, True, 1500),
    ("Cacador", CACADOR, 1900, 160, 86.0, 0, False, 2150),
    ("Atirador4", ATIRADOR, 2300, 140, 88.0, 140, True, 2550),
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
    carga = m.recurso("AudioStream", "res://assets/audio/efeitos/robos/raio_carga.wav")
    tiro = m.recurso("AudioStream", "res://assets/audio/efeitos/robos/raio_disparo.wav")
    musica = m.recurso("AudioStream", "res://assets/audio/musica/perseguicao/labirinto_tensao.ogg")

    for i, peca in enumerate(PAREDES):
        m.instancia(f"Parede{i + 1:02d}", "Paredes", f"{BUNKER}/paredes/{peca}.tscn", [f"position = Vector2({i * PECA}, 0)"])
        if peca == "bunker_emergencia":
            m.instancia(f"Giroflex{i + 1:02d}", "Luzes", "res://cenas/cenario/luzes/luz_emergencia.tscn",
                        [f"position = Vector2({i * PECA + 40}, 30)"])
    m.instancia("PilarEsquerda", "Paredes", f"{BUNKER}/paredes/pilar_bunker.tscn", ["position = Vector2(0, 0)"])
    m.instancia("PilarDireita", "Paredes", f"{BUNKER}/paredes/pilar_bunker.tscn", [f"position = Vector2({LARGURA - 16}, 0)"])
    for c in range(-(-LARGURA // CHAO)):
        chao = "chao_bunker_faixa" if c * CHAO >= PECA_DA_COMPORTA * PECA - 160 else ("chao_bunker_agua" if c % 3 else "chao_bunker")
        m.instancia(f"Chao{c + 1}", "Chao", f"{BUNKER}/chao/{chao}.tscn", [f"position = Vector2({c * CHAO}, 0)"])

    m.no('[node name="Gabriel" parent="Objetos"]', ["position = Vector2(240, 150)"])
    m.no('[node name="Grupo" type="Node2D" parent="Objetos"]', ["y_sort_enabled = true"])
    for nome, cena, x, y in GRUPO:
        m.instancia(nome, "Objetos/Grupo", cena, [f"position = Vector2({x}, {y})", 'vista = "lado"'])

    m.no('[node name="Robos" type="Node2D" parent="Objetos"]', ["y_sort_enabled = true"])
    for nome, (tira, quadros, escala, (dx, dy), altura_luz), x, y, velocidade, distancia, atira, aparece in ROBOS_DA_FUGA:
        corpo = m.recurso("Texture2D", f"{ROBOS}/{tira}_andar_lado.png")
        olhos = m.recurso("Texture2D", f"{ROBOS}/{tira}_andar_lado_olhos.png")
        m.no(f'[node name="{nome}" type="Node2D" parent="Objetos/Robos"]', [
            f"position = Vector2({x}, {y})", f'script = ExtResource("{script_robo}")',
            f"quadros = {quadros}", f"velocidade = {velocidade}", f"distancia_do_gabriel = {float(distancia)}",
            f"aparece_depois_de_x = {float(aparece)}", f"atira = {'true' if atira else 'false'}",
            f"velocidade_vertical = {26.0 if atira else 60.0}"])
        for parte, textura, material in (("Corpo", corpo, None), ("Olhos", olhos, "SemLuz")):
            props = [f'texture = ExtResource("{textura}")', "centered = false",
                     f"scale = Vector2({escala}, {escala})", f"offset = Vector2({dx}, {dy})", f"hframes = {quadros}"]
            if material:
                props.insert(0, f'material = SubResource("{material}")')
            m.no(f'[node name="{parte}" type="Sprite2D" parent="Objetos/Robos/{nome}"]', props)
        m.no(f'[node name="LuzOlho" type="PointLight2D" parent="Objetos/Robos/{nome}"]', [
            f"position = Vector2(0, {altura_luz})", "color = Color(1, 0.28, 0.15, 1)", "energy = 0.6",
            f'texture = ExtResource("{luz}")', "texture_scale = 0.7"])
        m.no(f'[node name="LinhaDaMira" type="Line2D" parent="Objetos/Robos/{nome}"]', [
            'material = SubResource("SemLuz")', "width = 1.0", "default_color = Color(1, 0.25, 0.2, 0.55)"])
        m.no(f'[node name="SomCarga" type="AudioStreamPlayer2D" parent="Objetos/Robos/{nome}"]', [
            f'stream = ExtResource("{carga}")', 'bus = &"Efeitos"'])
        m.no(f'[node name="SomTiro" type="AudioStreamPlayer2D" parent="Objetos/Robos/{nome}"]', [
            f'stream = ExtResource("{tiro}")', 'bus = &"Efeitos"'])

    m.no('[node name="Escuridao" parent="."]', ["color = Color(0.34, 0.2, 0.22, 1)"])
    m.no('[node name="Sirene" type="AudioStreamPlayer" parent="."]', [
        f'stream = ExtResource("{sirene}")', "volume_db = -8.0", "autoplay = true", 'bus = &"Efeitos"'])
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
