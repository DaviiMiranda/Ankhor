@tool
class_name PapelNoMundo
extends DocumentoNoMundo

@export var textura: Texture2D:
	set(valor):
		textura = valor
		_mostrar_desenho()

@onready var sprite: Sprite2D = $Sprite2D


func _ready() -> void:
	_mostrar_desenho()
	if Engine.is_editor_hint():
		return
	super()


func _mostrar_desenho() -> void:
	var s := get_node_or_null("Sprite2D") as Sprite2D
	if s == null:
		return
	s.texture = textura
	if textura:
		s.offset = Vector2(-floorf(textura.get_width() / 2.0), -textura.get_height())
