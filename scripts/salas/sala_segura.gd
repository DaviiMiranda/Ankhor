class_name SalaSegura
extends Sala

const GRUPO := "sala_segura"
const CENA_BAU := preload("res://cenas/sistemas/bau.tscn")

@export var posicao_bau := Vector2(261, 140)


func _enter_tree() -> void:
	if Engine.is_editor_hint():
		return
	get_tree().node_added.connect(_ao_entrar_no_arvore)


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	add_to_group(GRUPO)
	var bau := CENA_BAU.instantiate() as Node2D
	bau.position = posicao_bau
	$Objetos.add_child(bau)
	for no in get_tree().get_nodes_in_group("robos"):
		no.queue_free()


func _exit_tree() -> void:
	if Engine.is_editor_hint():
		return
	if get_tree() and get_tree().node_added.is_connected(_ao_entrar_no_arvore):
		get_tree().node_added.disconnect(_ao_entrar_no_arvore)


func _ao_entrar_no_arvore(no: Node) -> void:
	if no is Robo:
		no.queue_free()
