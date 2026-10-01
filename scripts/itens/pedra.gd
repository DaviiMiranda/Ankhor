extends Node2D

const CENA_PEDRA := preload("res://cenas/itens/pedra_arremessada.tscn")

@export var distancia: float = 110.0

var item: Item


func usar() -> void:
	var restantes := Inventario.unidades(item.id)
	if restantes <= 0:
		Inventario.aviso.emit("Sem pedras para jogar")
		return
	Inventario.definir_unidades(item, restantes - 1)
	var dono := get_parent().get_parent() as Gabriel
	var pedra := CENA_PEDRA.instantiate() as PedraArremessada
	get_tree().current_scene.add_child(pedra)
	pedra.lancar(dono.global_position, dono.direcao_olhar * distancia)
