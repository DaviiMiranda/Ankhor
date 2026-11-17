extends Interagivel

signal abriu


func pode_interagir() -> bool:
	var sala := get_tree().current_scene
	var gabriel := get_tree().get_first_node_in_group("jogador") as Gabriel
	return sala != null and sala.is_in_group("sala_segura") and not Inventario.com_kit_emprestado() \
			and gabriel != null and gabriel.pode_mexer_na_mochila() and not gabriel.mirando


func interagir() -> void:
	if not get_tree().paused and pode_interagir():
		abriu.emit()
