class_name NichoEsconderijo
extends Area2D

static var _ja_avisou := false

@export var segundos_para_esconder: float = 0.4
@export var aviso: String = "Parado no escuro do nicho, os robôs não me veem."

var _parado := 0.0
var _escondeu := false


func _physics_process(delta: float) -> void:
	var gabriel := get_tree().get_first_node_in_group("jogador") as Gabriel
	if gabriel == null:
		return
	if _pode_esconder(gabriel):
		_parado += delta
	else:
		_parado = 0.0
	var esconder := _parado >= segundos_para_esconder
	if esconder == _escondeu:
		return
	_escondeu = esconder
	gabriel.esconder(esconder)
	if esconder and not _ja_avisou:
		_ja_avisou = true
		Inventario.aviso.emit(aviso)


func _pode_esconder(gabriel: Gabriel) -> bool:
	return gabriel.jogador_controla and overlaps_body(gabriel) \
			and gabriel.velocity.length() < 2.0 and not Robo.luz_do_jogador_acesa()
