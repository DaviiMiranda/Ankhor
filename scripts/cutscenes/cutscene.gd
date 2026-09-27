class_name Cutscene
extends Node2D

signal cutscene_terminou(id: String)

@export var id: String = ""
@export var proxima_cena: PackedScene
@export var pode_pular: bool = true

const CENA_BOTAO_PULAR := preload("res://cenas/cutscenes/botao_pular.tscn")

@onready var animacao: AnimationPlayer = $AnimationPlayer

var _terminou := false


func _ready() -> void:
	animacao.animation_finished.connect(_ao_terminar_animacao)
	animacao.play("principal")
	if pode_pular:
		var botao := CENA_BOTAO_PULAR.instantiate()
		botao.pular.connect(_terminar)
		add_child(botao)


func _unhandled_input(event: InputEvent) -> void:
	if pode_pular and event.is_action_pressed("ui_cancel"):
		_terminar()


func _ao_terminar_animacao(_nome: StringName) -> void:
	_terminar()


func _terminar() -> void:
	if _terminou:
		return
	_terminou = true
	cutscene_terminou.emit(id)
	if proxima_cena:
		get_tree().change_scene_to_packed(proxima_cena)
