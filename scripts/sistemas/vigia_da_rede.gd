class_name VigiaDaRede
extends Node

const PREFIXO_ROTA := "Vigia_"

@export var robo: NodePath


func _ready() -> void:
	var guarda := get_node_or_null(robo) as Robo
	var rota := rota_de_vigia()
	if guarda and rota:
		guarda.rota = guarda.get_path_to(rota)


func rota_de_vigia() -> Node:
	var caminho: PackedStringArray = RedeEnergiaDtec.caminho_de_agora().caminho
	for i in range(caminho.size() - 1, -1, -1):
		var rota := get_parent().get_node_or_null(PREFIXO_ROTA + caminho[i])
		if rota:
			return rota
	return null
