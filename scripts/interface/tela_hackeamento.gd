class_name TelaHackeamento
extends CanvasLayer

signal concluido(sucesso: bool)
signal cancelado

const CENAS := {
	Hackeamento.Tipo.SEQUENCIA: preload("res://cenas/interface/hackeamento/minigame_sequencia.tscn"),
	Hackeamento.Tipo.SINCRONIA: preload("res://cenas/interface/hackeamento/minigame_sincronia.tscn"),
}

var aberto := false
var _minigame: MinigameHack
var _pausava_antes := false

@onready var palco: Control = $Palco
@onready var titulo: Label = $Titulo
@onready var instrucao: Label = $Instrucao
@onready var dica: Label = $Dica


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false


func abrir(nivel: Hackeamento.Dificuldade, tipo: Hackeamento.Tipo = Hackeamento.Tipo.ALEATORIO) -> void:
	if aberto:
		return
	if tipo == Hackeamento.Tipo.ALEATORIO:
		tipo = CENAS.keys().pick_random()
	_minigame = CENAS[tipo].instantiate()
	palco.add_child(_minigame)
	_minigame.iniciar(nivel)
	_minigame.terminou.connect(_ao_terminar)
	titulo.text = "%s  [%s]" % [_minigame.titulo, Hackeamento.NOMES_DIFICULDADE[nivel]]
	instrucao.text = _minigame.instrucao
	dica.text = "Esc: cancelar"
	_pausava_antes = get_tree().paused
	get_tree().paused = true
	aberto = true
	visible = true


func _unhandled_input(evento: InputEvent) -> void:
	if not aberto:
		return
	if evento.is_action_pressed("ui_cancel"):
		_fechar()
		cancelado.emit()
	elif _minigame:
		_minigame.tratar_entrada(evento)
	get_viewport().set_input_as_handled()


func _ao_terminar(sucesso: bool) -> void:
	if not aberto:
		return
	_fechar()
	concluido.emit(sucesso)


func _fechar() -> void:
	aberto = false
	visible = false
	get_tree().paused = _pausava_antes
	queue_free()
