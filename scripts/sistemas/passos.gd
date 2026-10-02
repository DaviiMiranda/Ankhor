class_name Passos
extends AudioStreamPlayer2D

@export var volume_andar_db: float = -10.0
@export var volume_correr_db: float = -3.0
@export var altura_correr: float = 1.08


func tocar(correndo: bool) -> void:
	if correndo:
		volume_db = volume_correr_db
		pitch_scale = altura_correr
	else:
		volume_db = volume_andar_db
		pitch_scale = 1.0
	play()
