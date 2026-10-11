class_name SaidaFase
extends Area2D

@export_file("*.tscn") var cena_destino: String = "res://cenas/menu_principal.tscn"
@export var espera: float = 3.5
@export var sair_ao_carregar := false

var _saiu := false

@onready var tela: CanvasLayer = $Tela
@onready var fundo: ColorRect = $Tela/Fundo
@onready var titulo: Label = $Tela/Titulo


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	tela.visible = false
	body_entered.connect(_ao_entrar)
	if sair_ao_carregar:
		_comecar_saida.call_deferred()


func _ao_entrar(corpo: Node2D) -> void:
	if corpo is Gabriel:
		_comecar_saida()


func _comecar_saida() -> void:
	if _saiu:
		return
	_saiu = true
	get_tree().paused = true
	tela.visible = true
	fundo.color.a = 0.0
	titulo.modulate.a = 0.0
	var animacao := create_tween()
	animacao.tween_property(fundo, "color:a", 1.0, 1.2)
	animacao.tween_property(titulo, "modulate:a", 1.0, 0.8)
	animacao.tween_interval(espera - 2.0)
	animacao.tween_callback(_sair)


func _sair() -> void:
	get_tree().paused = false
	Checkpoints.limpar()
	get_tree().change_scene_to_file(cena_destino)
