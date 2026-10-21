class_name Recompensa
extends RefCounted

const CENA_ITEM := preload("res://cenas/itens/item_no_chao.tscn")


static func soltar(perto_de: Node2D, item: Item, cena: PackedScene, quantidade: int) -> void:
	if item == null and cena == null:
		return
	for i in quantidade:
		var recompensa := (cena if cena else CENA_ITEM).instantiate() as Node2D
		recompensa.name = "Recompensa%d" % (i + 1)
		if recompensa is ItemNoChao:
			(recompensa as ItemNoChao).item = item
		recompensa.position = perto_de.position + Vector2(-8 + 16 * i - 8 * (quantidade - 1), 12)
		perto_de.get_parent().add_child(recompensa)
