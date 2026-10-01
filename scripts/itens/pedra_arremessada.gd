class_name PedraArremessada
extends Node2D

const CAMADA_PAREDES := 8
const ALCANCE_SOM := 12
const COR := Color(0.55, 0.55, 0.5)

@export var segundos_voo: float = 0.5
@export var altura_arco: float = 14.0

var _inicio := Vector2.ZERO
var _fim := Vector2.ZERO
var _altura := 0.0

@onready var impacto: AudioStreamPlayer2D = $Impacto


func lancar(de: Vector2, deslocamento: Vector2) -> void:
	_inicio = de
	_fim = _ate_a_parede(de, de + deslocamento)
	global_position = de
	var voo := create_tween()
	voo.tween_method(_voar, 0.0, 1.0, segundos_voo)
	voo.tween_callback(_cair)


func _ate_a_parede(de: Vector2, ate: Vector2) -> Vector2:
	var consulta := PhysicsRayQueryParameters2D.create(de, ate, CAMADA_PAREDES)
	var batida := get_world_2d().direct_space_state.intersect_ray(consulta)
	if batida.is_empty():
		return ate
	return batida.position - de.direction_to(ate) * 4.0


func _voar(t: float) -> void:
	global_position = _inicio.lerp(_fim, t)
	_altura = sin(t * PI) * altura_arco
	queue_redraw()


func _cair() -> void:
	_altura = 0.0
	queue_redraw()
	impacto.play()
	impacto.finished.connect(queue_free)
	for no in get_tree().get_nodes_in_group("robos"):
		(no as Robo).ouvir_barulho(global_position, ALCANCE_SOM)


func _draw() -> void:
	draw_rect(Rect2(Vector2(-1, -2 - _altura), Vector2(2, 2)), COR)
