extends Node


func _ready() -> void:
	_aplicar.call_deferred()


func _aplicar() -> void:
	var jogador := get_tree().get_first_node_in_group("jogador") as Gabriel
	if jogador != null:
		jogador.estamina_infinita = true
