@tool
class_name ColecionavelNoMundo
extends Interagivel

@export var colecao: Colecao:
	set(valor):
		colecao = valor
		_mostrar_desenho()
@export var numero: int = 1

@onready var sprite: Sprite2D = $Sprite2D


func _ready() -> void:
	_mostrar_desenho()
	if Engine.is_editor_hint():
		return
	super()
	texto_acao = ""
	if colecao == null or Colecionaveis.tem(colecao.id, numero):
		queue_free()


func interagir() -> void:
	Colecionaveis.coletar(colecao, numero)
	ItemNovo.mostrar_novo(colecao.item_com_progresso(Colecionaveis.quantidade(colecao.id)))
	queue_free()


func _mostrar_desenho() -> void:
	var s := get_node_or_null("Sprite2D") as Sprite2D
	if s == null:
		return
	var textura: Texture2D = null
	if colecao and colecao.item:
		textura = colecao.item.sprite_chao if colecao.item.sprite_chao else colecao.item.icone
	s.texture = textura
	if textura:
		s.offset = Vector2(-floorf(textura.get_width() / 2.0), -textura.get_height())
