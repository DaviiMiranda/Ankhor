class_name PoeiraDosPes
extends CPUParticles2D

@export var segundos_soltando: float = 0.07

var _tempo_restante := 0.0


func soltar(correndo: bool) -> void:
	if correndo:
		_tempo_restante = segundos_soltando
		emitting = true


func _process(delta: float) -> void:
	if _tempo_restante > 0.0:
		_tempo_restante -= delta
		if _tempo_restante <= 0.0:
			emitting = false
