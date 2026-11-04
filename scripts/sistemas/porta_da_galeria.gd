class_name PortaDaGaleria
extends Porta

@export var item_que_revela: String = "mapa_diana"


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	Inventario.mudou.connect(_atualizar)
	_atualizar()


func pode_interagir() -> bool:
	return Inventario.tem(item_que_revela) and super()


func _atualizar() -> void:
	visible = Inventario.tem(item_que_revela)
