class_name SalaSegura
extends Sala

const GRUPO := "sala_segura"


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	add_to_group(GRUPO)
	for no in get_tree().get_nodes_in_group("robos"):
		no.queue_free()
	get_tree().node_added.connect(_ao_entrar_no_arvore)


func _exit_tree() -> void:
	if Engine.is_editor_hint():
		return
	if get_tree() and get_tree().node_added.is_connected(_ao_entrar_no_arvore):
		get_tree().node_added.disconnect(_ao_entrar_no_arvore)


func _ao_entrar_no_arvore(no: Node) -> void:
	if no is Robo:
		no.queue_free()
