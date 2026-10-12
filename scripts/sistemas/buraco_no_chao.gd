class_name BuracoNoChao
extends Node2D

const GRUPO := "buracos"

static var _robo_embaixo_ate_msec := 0

@export var raio: float = 24.0
@export var achatamento: float = 1.5
@export var segundos_robo_embaixo: float = 18.0
@export var aviso: String = "A pedra caiu pelo buraco e bateu lá embaixo, na 104."

@onready var som: AudioStreamPlayer2D = $Som


func _ready() -> void:
	add_to_group(GRUPO)


func engole(ponto: Vector2) -> bool:
	var distancia := ponto - global_position
	return Vector2(distancia.x, distancia.y * achatamento).length() <= raio


func receber_pedra() -> void:
	_robo_embaixo_ate_msec = Time.get_ticks_msec() + int(segundos_robo_embaixo * 1000.0)
	som.play()
	Inventario.aviso.emit(aviso)


static func segundos_com_robo_embaixo() -> float:
	return maxf(0.0, (_robo_embaixo_ate_msec - Time.get_ticks_msec()) / 1000.0)


static func esquecer() -> void:
	_robo_embaixo_ate_msec = 0
