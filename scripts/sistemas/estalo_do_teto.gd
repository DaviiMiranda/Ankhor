class_name EstaloDoTeto
extends Node2D

@export var segundos_minimos: float = 12.0
@export var segundos_maximos: float = 28.0
@export var distancia_para_ouvir: float = 280.0
@export var atraso_da_poeira: float = 0.9

var _espera := 0.0

@onready var som: AudioStreamPlayer2D = $Som
@onready var poeira: CPUParticles2D = $Poeira


func _ready() -> void:
	poeira.emitting = false
	_sortear_espera()


func _process(delta: float) -> void:
	_espera -= delta
	if _espera > 0.0:
		return
	_sortear_espera()
	var gabriel := get_tree().get_first_node_in_group("jogador") as Node2D
	if gabriel and absf(gabriel.global_position.x - global_position.x) < distancia_para_ouvir:
		estalar()


func estalar() -> void:
	som.pitch_scale = randf_range(0.85, 1.1)
	som.play()
	get_tree().create_timer(atraso_da_poeira).timeout.connect(poeira.restart)


func _sortear_espera() -> void:
	_espera = randf_range(segundos_minimos, segundos_maximos)
