class_name NoHackeavel
extends Porta

const COR_TRANCADO := Color(1.0, 0.3, 0.25)
const COR_INVADIDO := Color(0.35, 1.0, 0.6)

@export var gasto_hack: float = 0.0

@onready var luz: PointLight2D = get_node_or_null("Luz")


func _ready() -> void:
	super()
	_atualizar_luz()


func pode_interagir() -> bool:
	return trancada


func destrancar() -> void:
	super()
	_atualizar_luz()


func _atualizar_luz() -> void:
	if luz:
		luz.color = COR_TRANCADO if trancada else COR_INVADIDO
