@tool
class_name CadeiraVR
extends ObjetoCenario

@export var lente_acesa: bool = false:
	set(valor):
		lente_acesa = valor
		_atualizar_lente()


func _ready() -> void:
	super()
	_atualizar_lente()


func _aplicar_espelho() -> void:
	super()
	var lente := get_node_or_null("Lente") as Sprite2D
	var base := get_node_or_null("Sprite2D") as Sprite2D
	if lente == null or base == null:
		return
	lente.flip_h = base.flip_h
	lente.offset = base.offset


func _atualizar_lente() -> void:
	var lente := get_node_or_null("Lente") as Sprite2D
	if lente:
		lente.visible = lente_acesa
