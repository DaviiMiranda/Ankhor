@tool
class_name ObjetoCenario
extends StaticBody2D

@export var espelhado: bool = false:
	set(valor):
		espelhado = valor
		_aplicar_espelho()

var _offset_original: Vector2
var _pegada_x_original: float
var _pronto := false


func _ready() -> void:
	_aplicar_espelho()


func _aplicar_espelho() -> void:
	var sprite := get_node_or_null("Sprite2D") as Sprite2D
	if sprite == null or sprite.texture == null:
		return
	var pegada := get_node_or_null("Pegada") as Node2D
	if not _pronto:
		_offset_original = sprite.offset
		_pegada_x_original = pegada.position.x if pegada else 0.0
		_pronto = true
	sprite.flip_h = espelhado
	var largura := sprite.texture.get_width()
	if espelhado:
		sprite.offset.x = -largura - _offset_original.x
	else:
		sprite.offset.x = _offset_original.x
	if pegada:
		pegada.position.x = -_pegada_x_original if espelhado else _pegada_x_original
