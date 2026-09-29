class_name SaidaFase
extends Area2D

@export_file("*.tscn") var cena_destino: String = "res://cenas/menu_principal.tscn"
@export var espera: float = 3.5

var _saiu := false

@onready var tela: CanvasLayer = $Tela
@onready var fundo: ColorRect = $Tela/Fundo
@onready var titulo: Label = $Tela/Titulo


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	tela.visible = false
	body_entered.connect(_ao_entrar)


func _ao_entrar(corpo: Node2D) -> void:
	if _saiu or not corpo is Gabriel:
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
