class_name RoboDeCena
extends Node2D

@export var quadros: int = 8
@export var quadros_por_segundo: float = 10.0
@export var velocidade: float = 100.0

var correndo := false
var _tempo := 0.0

@onready var corpo: Sprite2D = $Corpo
@onready var olhos: Sprite2D = $Olhos


func _process(delta: float) -> void:
	if not correndo:
		return
	position.x += velocidade * delta
	_tempo += delta
	var quadro := int(_tempo * quadros_por_segundo) % quadros
	corpo.frame = quadro
	olhos.frame = quadro
