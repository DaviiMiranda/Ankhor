class_name FrestaDaBarricada
extends Interagivel

@export var porta: NodePath


func interagir() -> void:
	var alvo := get_node_or_null(porta) as Porta
	if alvo:
		alvo.espiar()
