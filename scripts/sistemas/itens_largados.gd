class_name ItensLargados
extends Node

const CENA_ITEM := preload("res://cenas/itens/item_no_chao.tscn")
const CAMINHO_ITEM := "res://dados/itens/%s.tres"


static func soltar(arvore: SceneTree, item: Item, posicao: Vector2) -> Node2D:
	Inventario.largar(item, arvore.current_scene.scene_file_path, posicao)
	return _criar(arvore, item, posicao)


func _ready() -> void:
	_restaurar.call_deferred()


func _restaurar() -> void:
	var cena_atual := get_tree().current_scene
	if cena_atual == null:
		return
	var caminho := cena_atual.scene_file_path
	for id in Inventario.largados.keys():
		var dados: Dictionary = Inventario.largados[id]
		var item := load(CAMINHO_ITEM % id) as Item
		if item == null:
			continue
		if dados["cena"] == caminho:
			_criar(get_tree(), item, dados["posicao"])
		elif String(dados["cena"]).get_base_dir() != caminho.get_base_dir():
			Inventario.adicionar(item)


static func _criar(arvore: SceneTree, item: Item, posicao: Vector2) -> Node2D:
	var no: Node2D = (item.cena_largado if item.cena_largado else CENA_ITEM).instantiate()
	no.name = "Largado_%s" % item.id
	no.set("item", item)
	if no is ItemNoChao:
		(no as ItemNoChao).reaparece = true
	var cena := arvore.current_scene
	var pai := cena.get_node_or_null("Objetos")
	(pai if pai else cena).add_child(no)
	no.global_position = posicao
	return no
