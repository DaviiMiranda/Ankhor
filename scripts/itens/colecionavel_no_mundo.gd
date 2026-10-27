@tool
class_name ColecionavelNoMundo
extends Interagivel

@export var colecao: Colecao:
	set(valor):
		colecao = valor
		_mostrar_desenho()
@export var numero: int = 1
@export var marca_necessaria: String = ""

@onready var sprite: Sprite2D = $Sprite2D
@onready var destaque: Node2D = $DestaqueColetavel


func _ready() -> void:
	_mostrar_desenho()
	if Engine.is_editor_hint():
		return
	super()
	texto_acao = ""
	if colecao == null or Colecionaveis.tem(colecao.id, numero):
		queue_free()
		return
	Progresso.mudou.connect(_ao_mudar_progresso)
	_mostrar_se_liberado()


func pode_interagir() -> bool:
	return _liberado()


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


func _liberado() -> bool:
	return marca_necessaria.is_empty() or Progresso.tem(marca_necessaria)


func _ao_mudar_progresso(marca: String) -> void:
	if marca == marca_necessaria:
		_mostrar_se_liberado()


func _mostrar_se_liberado() -> void:
	var liberado := _liberado()
	sprite.visible = liberado
	destaque.visible = liberado
