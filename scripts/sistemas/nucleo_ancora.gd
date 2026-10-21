class_name NucleoAncora
extends Node2D

@export var chefe: NodePath
@export var fase_que_abre: int = 2

@onready var saida: SaidaFase = $SaidaFase
@onready var luz: PointLight2D = $Luz


func _ready() -> void:
	_abrir(false)
	var carlos := get_node_or_null(chefe) as CarlosChefe
	if carlos:
		carlos.fase_mudou.connect(func(fase: int): _abrir.call_deferred(fase >= fase_que_abre))


func _abrir(aberto: bool) -> void:
	saida.set_deferred("monitoring", aberto)
	luz.visible = aberto
