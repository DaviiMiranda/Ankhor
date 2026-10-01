@tool
class_name ItemNoChao
extends Interagivel

@export var item: Item:
	set(valor):
		item = valor
		_mostrar_desenho()

@onready var sprite: Sprite2D = $Sprite2D


func _ready() -> void:
	_mostrar_desenho()
	if Engine.is_editor_hint():
		return
	super()
	texto_acao = ""
	if Inventario.pegos.has(_id_unico()):
		queue_free()


func interagir() -> void:
	if Inventario.adicionar(item):
		Inventario.pegos[_id_unico()] = true
		queue_free()


func _id_unico() -> String:
	var sala := owner if owner else get_tree().current_scene
	return "%s:%s" % [sala.scene_file_path, sala.get_path_to(self)]


func _mostrar_desenho() -> void:
	var s := get_node_or_null("Sprite2D") as Sprite2D
	if s == null:
		return
	var textura: Texture2D = null
	if item:
		textura = item.sprite_chao if item.sprite_chao else item.icone
	s.texture = textura
	if textura:
		s.offset = Vector2(-floorf(textura.get_width() / 2.0), -textura.get_height())
