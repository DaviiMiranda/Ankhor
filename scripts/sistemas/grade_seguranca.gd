class_name GradeSeguranca
extends Node2D

@export var marca: String = "grade_aberta"
@export var segundos_subindo: float = 2.5
@export var altura_aberta: float = 3.0

var _altura_fechada := 0.0

@onready var grade: Sprite2D = $Grade
@onready var som: AudioStreamPlayer2D = $Som


func _ready() -> void:
	_altura_fechada = grade.texture.get_height()
	grade.region_enabled = true
	_mostrar_altura(altura_aberta if Progresso.tem(marca) else _altura_fechada)
	Progresso.mudou.connect(_ao_mudar)


func _ao_mudar(nova: String) -> void:
	if nova != marca:
		return
	som.play()
	var animacao := create_tween()
	animacao.tween_method(_mostrar_altura, _altura_fechada, altura_aberta, segundos_subindo)


func _mostrar_altura(altura: float) -> void:
	var largura := grade.texture.get_width()
	var visivel := roundf(altura)
	grade.region_rect = Rect2(0, _altura_fechada - visivel, largura, visivel)
