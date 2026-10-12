class_name Sirene
extends AudioStreamPlayer2D

static var disparada := false

@export var segundos_tocando: float = 20.0
@export var piscadas_por_segundo: float = 2.0

var _restante := 0.0

@onready var luz: PointLight2D = $Luz


func _ready() -> void:
	luz.visible = false
	if disparada:
		disparada = false
		_tocar.call_deferred()


func _process(delta: float) -> void:
	if _restante <= 0.0:
		return
	_restante -= delta
	luz.visible = fmod(_restante * piscadas_por_segundo, 1.0) < 0.5
	if _restante <= 0.0:
		luz.visible = false
		stop()


func _tocar() -> void:
	await get_tree().physics_frame
	await get_tree().physics_frame
	_restante = segundos_tocando
	play()
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo and robo.grade:
			robo.global_position = global_position
			robo.distrair(global_position, segundos_tocando)
