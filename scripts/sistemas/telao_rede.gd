class_name TelaoRede
extends Interagivel

const COR_CABO := Color("2a3b52")
const COR_CABO_ATIVO := Color("62e3ee")
const COR_RELE := Color("8fa3b8")
const COR_CORTADO := Color("e0413a")
const COR_GERADOR := Color("e8d36a")
const COR_ANCORA := Color("b6fbff")
const COR_PESO := Color("5d7088")
const COR_TEXTO := Color("d8dee6")
const RAIO := 6.0

const POSICOES := {
	"gerador_norte": Vector2(40, 50),
	"informatica": Vector2(170, 60),
	"servidores": Vector2(300, 30),
	"eletronica": Vector2(290, 150),
	"controle": Vector2(440, 40),
	"ancora": Vector2(510, 140),
	"gerador_sul": Vector2(40, 190),
	"quimica": Vector2(180, 222),
	"robotica": Vector2(330, 195),
}

var _aberto := false

@onready var tela: CanvasLayer = $Tela
@onready var quadro: Control = $Tela/Quadro
@onready var rodape: Label = $Tela/Rodape


func _ready() -> void:
	super()
	process_mode = Node.PROCESS_MODE_ALWAYS
	tela.visible = false
	quadro.draw.connect(_desenhar)


func pode_interagir() -> bool:
	return not _aberto


func interagir() -> void:
	_aberto = true
	tela.visible = true
	get_tree().paused = true
	_atualizar_rodape()
	quadro.queue_redraw()


func _fechar() -> void:
	_aberto = false
	tela.visible = false
	get_tree().paused = false


func _unhandled_input(evento: InputEvent) -> void:
	if not _aberto:
		return
	if evento.is_action_pressed("ui_cancel") or evento.is_action_pressed("interagir"):
		_fechar()
	get_viewport().set_input_as_handled()


func _atualizar_rodape() -> void:
	var ativo := RedeEnergiaDtec.caminho_de_agora()
	var cortados := RedeEnergiaDtec.reles_cortados().size()
	if ativo.caminho.is_empty():
		rodape.text = "SEM CAMINHO ATÉ A ÂNCORA.  Relés cortados: %d de %d" % [cortados, RedeEnergiaDtec.RELES.size()]
		rodape.add_theme_color_override("font_color", COR_CORTADO)
		return
	rodape.text = "Caminho ativo (%d m de cabo): %s" % [ativo.custo, RedeEnergiaDtec.caminho_em_texto(ativo.caminho)]
	rodape.add_theme_color_override("font_color", COR_CABO_ATIVO)


func _desenhar() -> void:
	var cortados := RedeEnergiaDtec.reles_cortados()
	var caminho: PackedStringArray = RedeEnergiaDtec.caminho_ativo(cortados).caminho
	var fonte := quadro.get_theme_default_font()
	for cabo in RedeEnergiaDtec.CABOS:
		var a: Vector2 = POSICOES[cabo[0]]
		var b: Vector2 = POSICOES[cabo[1]]
		var ativo := _cabo_no_caminho(cabo[0], cabo[1], caminho)
		quadro.draw_line(a, b, COR_CABO_ATIVO if ativo else COR_CABO, 2.0 if ativo else 1.0)
		var peso := str(RedeEnergiaDtec.CABOS[cabo])
		quadro.draw_string(fonte, (a + b) / 2.0 + Vector2(2, -2), peso, HORIZONTAL_ALIGNMENT_LEFT, -1, 8, COR_PESO)
	for no in POSICOES:
		_desenhar_no(no, POSICOES[no], no in cortados, no in caminho, fonte)


func _desenhar_no(no: String, centro: Vector2, cortado: bool, ativo: bool, fonte: Font) -> void:
	var cor := COR_RELE
	if no in RedeEnergiaDtec.GERADORES:
		cor = COR_GERADOR
	elif no == RedeEnergiaDtec.ANCORA:
		cor = COR_ANCORA
	elif cortado:
		cor = COR_CORTADO
	var raio := RAIO * (1.6 if no == RedeEnergiaDtec.ANCORA else 1.0)
	quadro.draw_circle(centro, raio + 2.0, Color(0.05, 0.07, 0.1))
	quadro.draw_circle(centro, raio, cor)
	if ativo:
		quadro.draw_arc(centro, raio + 3.0, 0.0, TAU, 24, COR_CABO_ATIVO, 1.0)
	if cortado:
		var d := Vector2(raio, raio)
		quadro.draw_line(centro - d, centro + d, Color.BLACK, 2.0)
		quadro.draw_line(centro + Vector2(-raio, raio), centro + Vector2(raio, -raio), Color.BLACK, 2.0)
	var nome: String = RedeEnergiaDtec.NOMES[no]
	quadro.draw_string(fonte, centro + Vector2(-60, raio + 14), nome, HORIZONTAL_ALIGNMENT_CENTER, 120, 8, COR_TEXTO)


func _cabo_no_caminho(a: String, b: String, caminho: PackedStringArray) -> bool:
	for i in caminho.size() - 1:
		if (caminho[i] == a and caminho[i + 1] == b) or (caminho[i] == b and caminho[i + 1] == a):
			return true
	return false
