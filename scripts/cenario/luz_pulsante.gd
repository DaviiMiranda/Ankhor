class_name LuzPulsante
extends PointLight2D

@export var periodo: float = 2.4
@export var variacao: float = 0.3

var _energia_base: float
var _tempo := 0.0


func _ready() -> void:
	_energia_base = energy


func _process(delta: float) -> void:
	_tempo += delta
	energy = _energia_base * (1.0 + variacao * sin(TAU * _tempo / periodo))
