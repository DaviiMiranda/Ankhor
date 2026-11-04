extends Node2D

@export var gasto_por_uso: float = 0.25

var item: Item
var _estado: Dictionary


func _ready() -> void:
	_estado = Inventario.estado_de(item.id if item else "walkman")
	if not _estado.has("carga"):
		_estado["carga"] = 1.0


func usar() -> void:
	if _estado["carga"] < gasto_por_uso - 0.001:
		Inventario.aviso.emit("Walkman sem pilha")
		return
	_estado["carga"] = maxf(_estado["carga"] - gasto_por_uso, 0.0)
	var dono := get_parent().get_parent() as Gabriel
	var no := ItensLargados.soltar(get_tree(), item, dono.global_position)
	(no as WalkmanNoChao).tocar()
