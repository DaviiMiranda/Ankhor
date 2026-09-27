class_name MusicaFase
extends AudioStreamPlayer

@export var volume_final_db: float = -18.0
@export var duracao_fade: float = 4.0


func _ready() -> void:
	if stream:
		stream.set("loop", true)
	volume_db = -60.0
	play()
	var fade := create_tween()
	fade.tween_property(self, "volume_db", volume_final_db, duracao_fade)
