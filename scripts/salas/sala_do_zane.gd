class_name SalaDoZane
extends Sala


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	_vestir_zane.call_deferred()


func _vestir_zane() -> void:
	var jogador := get_tree().get_first_node_in_group("jogador") as Gabriel
	if jogador:
		PerfilZane.aplicar(jogador)
