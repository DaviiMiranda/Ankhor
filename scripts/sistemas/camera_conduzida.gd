class_name CameraConduzida
extends Node

@export var segundos_a_frente: float = 0.32
@export var rapidez_antecipacao: float = 2.5
@export var balanco_correndo: float = 0.75

var _posicao_base := Vector2.ZERO

@onready var _gabriel := get_parent() as Gabriel
@onready var _camera := get_parent().get_node_or_null("Camera2D") as Camera2D


func _ready() -> void:
	if _camera == null:
		set_physics_process(false)
		return
	_posicao_base = _camera.position
	_camera.process_callback = Camera2D.CAMERA2D_PROCESS_PHYSICS


func _physics_process(delta: float) -> void:
	var alvo := _posicao_base + _gabriel.get_real_velocity() * segundos_a_frente
	_camera.position = _camera.position.lerp(alvo, 1.0 - exp(-rapidez_antecipacao * delta))
	_camera.offset.y = balanco_correndo * _gabriel.fracao_de_corrida() * _gabriel.pulso_da_passada()
