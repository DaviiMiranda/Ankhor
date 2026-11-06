"""
Gera a cena da camara selada, a parte secreta do fim do Labirinto:

  cenas/salas/labirinto/camara_selada.tscn     (o Gabriel preso; depois, o resgate e o registro)

O caminho do Zane ate a camara (a ala do escritorio) sai de montar_escritorio.py, nesta pasta.

Uso (a partir da raiz do projeto):  python assets/modelagem/salas/labirinto/gerar_camaras.py

As paredes e o chao sao as pecas do bunker, em passos fixos: parede de 80 px e chao de 128 px.
Um nicho de esconderijo fica sempre no centro de uma peca de parede de nicho (x = 80 * k + 40).
"""
import os

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
PASTA = os.path.join(RAIZ, "cenas", "salas", "labirinto")

PASSO_PAREDE = 80
PASSO_CHAO = 128

RECURSOS = {
    "modelo": ("PackedScene", "res://cenas/salas/modelo_sala.tscn"),
    "lisa": ("PackedScene", "res://cenas/cenario/bunker/paredes/bunker_lisa.tscn"),
    "porta": ("PackedScene", "res://cenas/cenario/bunker/paredes/bunker_porta.tscn"),
    "luminaria": ("PackedScene", "res://cenas/cenario/bunker/paredes/bunker_luminaria.tscn"),
    "canos": ("PackedScene", "res://cenas/cenario/bunker/paredes/bunker_canos.tscn"),
    "armarios": ("PackedScene", "res://cenas/cenario/bunker/paredes/bunker_armarios.tscn"),
    "painel": ("PackedScene", "res://cenas/cenario/bunker/paredes/bunker_painel.tscn"),
    "rachada": ("PackedScene", "res://cenas/cenario/bunker/paredes/bunker_rachada.tscn"),
    "nicho_parede": ("PackedScene", "res://cenas/cenario/bunker/paredes/bunker_nicho.tscn"),
    "chao": ("PackedScene", "res://cenas/cenario/bunker/chao/chao_bunker.tscn"),
    "chao_grade": ("PackedScene", "res://cenas/cenario/bunker/chao/chao_bunker_grade.tscn"),
    "chao_faixa": ("PackedScene", "res://cenas/cenario/bunker/chao/chao_bunker_faixa.tscn"),
    "caixas": ("PackedScene", "res://cenas/cenario/bunker/objetos/caixas.tscn"),
    "tambor": ("PackedScene", "res://cenas/cenario/bunker/objetos/tambor.tscn"),
    "estante": ("PackedScene", "res://cenas/cenario/bunker/objetos/estante_metal.tscn"),
    "robo_desmontado": ("PackedScene", "res://cenas/cenario/objetos/robo_desmontado.tscn"),
    "luz_tubo": ("PackedScene", "res://cenas/cenario/luzes/luz_tubo.tscn"),
    "luz_emergencia": ("PackedScene", "res://cenas/cenario/luzes/luz_emergencia.tscn"),
    "porta_sala": ("PackedScene", "res://cenas/sistemas/porta.tscn"),
    "porta_som": ("AudioStream", "res://assets/audio/efeitos/objetos/porta_blindada.wav"),
    "grade": ("PackedScene", "res://cenas/sistemas/grade_com_colisao.tscn"),
    "nicho": ("PackedScene", "res://cenas/sistemas/nicho_esconderijo.tscn"),
    "checkpoint": ("PackedScene", "res://cenas/sistemas/checkpoint.tscn"),
    "painel_bits": ("PackedScene", "res://cenas/sistemas/painel_bits.tscn"),
    "painel_codigo": ("PackedScene", "res://cenas/sistemas/painel_codigo.tscn"),
    "aviso": ("PackedScene", "res://cenas/itens/aviso_no_mundo.tscn"),
    "gatilho": ("PackedScene", "res://cenas/sistemas/gatilho_dialogo.tscn"),
    "ronda": ("PackedScene", "res://cenas/personagens/robo_ronda.tscn"),
    "sentinela": ("PackedScene", "res://cenas/personagens/robo_sentinela.tscn"),
    "zane": ("PackedScene", "res://cenas/personagens/zane.tscn"),
    "alcapao": ("PackedScene", "res://cenas/sistemas/alcapao.tscn"),
    "alcapao_aberto": ("Texture2D", "res://assets/sprites/cenario/objetos/alcapao_aberto.png"),
    "script_robos": ("Script", "res://scripts/salas/robos_da_sala.gd"),
    "script_conversa": ("Script", "res://scripts/personagens/conversa_npc.gd"),
    "script_camara": ("Script", "res://scripts/salas/camara_selada.gd"),
}

PAREDES_DA_CAMARA = ["lisa", "canos", "painel", "lisa", "luminaria", "rachada", "canos", "lisa"]
CHAOS = ["chao", "chao", "chao_grade", "chao", "chao_faixa"]


class Cena:
    def __init__(self, raiz, script, largura, id_sala):
        self.ids = {}
        self.blocos = []
        self.raiz = raiz
        self.script = script
        self.largura = largura
        self.id_sala = id_sala
        self.usa("modelo")
        self.usa(script)

    def usa(self, chave):
        if chave not in self.ids:
            self.ids[chave] = "r%d" % (len(self.ids) + 1)
        return 'ExtResource("%s")' % self.ids[chave]

    def no(self, nome, pai, recurso=None, tipo=None, **props):
        if recurso:
            cabecalho = '[node name="%s" parent="%s" instance=%s]' % (nome, pai, self.usa(recurso))
        else:
            cabecalho = '[node name="%s" type="%s" parent="%s"]' % (nome, tipo, pai)
        linhas = [cabecalho]
        for chave, valor in props.items():
            linhas.append("%s = %s" % (chave, valor))
        self.blocos.append("\n".join(linhas))

    def texto(self):
        saida = ["[gd_scene format=3]", ""]
        for chave, indice in self.ids.items():
            tipo, caminho = RECURSOS[chave]
            saida.append('[ext_resource type="%s" path="%s" id="%s"]' % (tipo, caminho, indice))
        saida.append("")
        saida.append('[node name="%s" instance=%s]' % (self.raiz, self.usa("modelo")))
        saida.append("script = %s" % self.usa(self.script))
        saida.append('id = "%s"' % self.id_sala)
        saida.append("largura = %d" % self.largura)
        saida.append("")
        saida.append("\n\n".join(self.blocos))
        return "\n".join(saida) + "\n"


def v(x, y):
    return "Vector2(%s, %s)" % (x, y)


def s(texto):
    return '"%s"' % texto.replace('"', '\\"')


def paredes_e_chao(cena, paredes):
    for i, chave in enumerate(paredes):
        cena.no("Parede%02d" % (i + 1), "Paredes", chave, position=v(i * PASSO_PAREDE, 0))
    for i in range(cena.largura // PASSO_CHAO + 1):
        cena.no("Chao%d" % (i + 1), "Chao", CHAOS[i % len(CHAOS)], position=v(i * PASSO_CHAO, 0))


def clima(cena, luzes, escuridao):
    for i, (x, tipo) in enumerate(luzes):
        cena.no("Luz%d" % (i + 1), "Luzes", tipo, position=v(x, 34 if tipo == "luz_tubo" else 30))
    cena.blocos.append('[node name="Escuridao" parent="."]\ncolor = %s' % escuridao)


def gerar_camara():
    cena = Cena("CamaraSelada", "script_camara", 640, "labirinto_camara_selada")
    paredes_e_chao(cena, PAREDES_DA_CAMARA)
    clima(cena, [(100, "luz_tubo"), (420, "luz_tubo"), (560, "luz_emergencia")], "Color(0.2, 0.22, 0.3, 1)")

    cena.no("Caixas", "Objetos", "caixas", position=v(300, 134))
    cena.no("Estante", "Objetos", "estante", position=v(380, 132), espelhado="true")
    cena.no("RoboDesmontado", "Objetos", "robo_desmontado", position=v(230, 172))
    cena.blocos.append('[node name="Gabriel" parent="Objetos"]\nposition = %s' % v(60, 150))

    cena.no("Cela", ".", None, tipo="Node2D")
    cena.no("Grade", "Cela", "grade", position=v(158, 112), marca=s("camara_cela_aberta"))

    cena.no("Zane", "Objetos", "zane", position=v(250, 164), vista=s("tres_quartos"),
            olhando_para_esquerda="true")

    cena.no("Terminal", "Objetos", None, tipo="Area2D", position=v(470, 150), script=cena.usa("script_conversa"),
            texto_acao=s("Ouvir o registro"), altura_aviso="40.0")
    cena.no("Corpo", "Objetos/Terminal", None, tipo="ColorRect", offset_left="-9.0", offset_top="-26.0",
            offset_right="9.0", offset_bottom="0.0", mouse_filter="2", color="Color(0.15, 0.17, 0.21, 1)")
    cena.no("Tela", "Objetos/Terminal", None, tipo="ColorRect", offset_left="-7.0", offset_top="-22.0",
            offset_right="7.0", offset_bottom="-10.0", mouse_filter="2", color="Color(0.35, 0.9, 1, 1)")
    cena.blocos.append('[node name="Alcance" type="CollisionShape2D" parent="Objetos/Terminal"]\n'
                       'position = Vector2(0, -4)\nshape = SubResource("Alcance")')
    cena.no("Luz", "Objetos/Terminal", None, tipo="PointLight2D", position=v(0, -16), color="Color(0.35, 0.9, 1, 1)",
            energy="0.8")

    cena.no("Duto", "Objetos", "alcapao", position=v(580, 150), texto_acao=s("Subir"), altura_aviso="30.0",
            cena_destino=s("res://cenas/salas/centro_de_convivencia/passarela_acesso.tscn"),
            titulo=s("VOCÊ SAIU DO LABIRINTO"), subtitulo=s("Próxima fase: o Centro de Convivência"),
            marca_para_usar=s("camara_registro_lido"), textura_escondido=cena.usa("alcapao_aberto"),
            textura_aberto=cena.usa("alcapao_aberto"))
    texto = cena.texto()
    texto = texto.replace("[node name=\"CamaraSelada\"",
                          '[sub_resource type="CircleShape2D" id="Alcance"]\nradius = 22.0\n\n[node name="CamaraSelada"', 1)
    return texto


def main():
    for nome, texto in (("camara_selada.tscn", gerar_camara()),):
        with open(os.path.join(PASTA, nome), "w", encoding="utf-8", newline="\n") as f:
            f.write(texto)
        print("escrito", nome)


if __name__ == "__main__":
    main()
