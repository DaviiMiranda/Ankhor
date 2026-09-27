class_name LuzPulsante
extends PointLight2D

@export var variacao: float = 0.25
@export var periodo: float = 3.0

var _energia_base: float
var _fase: float
var _tempo := 0.0


func _ready() -> void:
	_energia_base = energy
	_fase = fmod(global_position.x * 0.37 + global_position.y * 0.11, TAU)


func _process(delta: float) -> void:
	_tempo += delta
	energy = _energia_base * (1.0 + variacao * sin(TAU * _tempo / periodo + _fase))
