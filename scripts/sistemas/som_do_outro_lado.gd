class_name SomDoOutroLado
extends AudioStreamPlayer2D

@export var segundos_minimos: float = 10.0
@export var segundos_maximos: float = 26.0
@export var distancia_para_ouvir: float = 220.0

var _espera := 0.0


func _ready() -> void:
	_sortear_espera()


func _process(delta: float) -> void:
	_espera -= delta
	if _espera > 0.0:
		return
	_sortear_espera()
	var gabriel := get_tree().get_first_node_in_group("jogador") as Node2D
	if gabriel and gabriel.global_position.distance_to(global_position) < distancia_para_ouvir:
		pitch_scale = randf_range(0.85, 1.05)
		play()


func _sortear_espera() -> void:
	_espera = randf_range(segundos_minimos, segundos_maximos)
