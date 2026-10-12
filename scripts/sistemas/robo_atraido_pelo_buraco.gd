class_name RoboAtraidoPeloBuraco
extends Node2D

const LONGE := Vector2(-1000, -1000)

@export var robo: NodePath
@export var dentro_da_sala := false
@export var saida_da_sala := Vector2.ZERO
@export var segundos_saindo: float = 4.0


func _ready() -> void:
	var alvo := get_node_or_null(robo) as Robo
	if alvo == null:
		return
	var restante := BuracoNoChao.segundos_com_robo_embaixo()
	if restante <= 0.0:
		if dentro_da_sala:
			alvo.remove_from_group("robos")
			alvo.queue_free()
		return
	if dentro_da_sala:
		_investigar_a_pedra.call_deferred(alvo, restante)
	else:
		_ficar_na_sala.call_deferred(alvo, restante)


func _investigar_a_pedra(alvo: Robo, restante: float) -> void:
	await get_tree().physics_frame
	await get_tree().physics_frame
	alvo.distrair(global_position, restante)
	await get_tree().create_timer(restante).timeout
	if not is_instance_valid(alvo):
		return
	alvo.distrair(saida_da_sala, segundos_saindo)
	await get_tree().create_timer(segundos_saindo).timeout
	if is_instance_valid(alvo):
		_sumir(alvo)


func _ficar_na_sala(alvo: Robo, restante: float) -> void:
	await get_tree().physics_frame
	await get_tree().physics_frame
	_sumir(alvo)
	await get_tree().create_timer(restante + segundos_saindo).timeout
	if not is_instance_valid(alvo):
		return
	alvo.global_position = global_position
	alvo.show()
	alvo.process_mode = Node.PROCESS_MODE_INHERIT
	alvo.distrair(global_position + Vector2(0, 16), 2.0)


func _sumir(alvo: Robo) -> void:
	alvo.hide()
	alvo.global_position = LONGE
	alvo.process_mode = Node.PROCESS_MODE_DISABLED
