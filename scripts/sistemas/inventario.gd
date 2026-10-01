extends Node

signal mudou
signal item_pego(item: Item)
signal aviso(texto: String)

const LINHAS := 3
const COLUNAS := 4
const ESPACOS_GADGET := 3

var grade: Array = []
var gadgets: Array = []
var estado: Dictionary = {}
var pegos: Dictionary = {}


func _ready() -> void:
	limpar()


func limpar() -> void:
	grade = []
	for linha in LINHAS:
		var colunas := []
		colunas.resize(COLUNAS)
		grade.append(colunas)
	gadgets = []
	gadgets.resize(ESPACOS_GADGET)
	estado = {}
	pegos = {}
	mudou.emit()


func adicionar(item: Item) -> bool:
	if item.maximo_unidades > 0 and tem(item.id):
		return _somar_unidade(item)
	for linha in LINHAS:
		for coluna in COLUNAS:
			if grade[linha][coluna] == null:
				grade[linha][coluna] = item
				if item.maximo_unidades > 0:
					definir_unidades(item, 1)
				if item.equipavel and espaco_do_gadget(item) == -1:
					var livre := gadgets.find(null)
					if livre != -1:
						gadgets[livre] = item
				item_pego.emit(item)
				mudou.emit()
				return true
	return false


func item_em(linha: int, coluna: int) -> Item:
	return grade[linha][coluna]


func tem(id: String) -> bool:
	for linha in grade:
		for item in linha:
			if item != null and item.id == id:
				return true
	return false


func equipar(item: Item, espaco: int) -> void:
	if item == null or not item.equipavel:
		return
	var antigo := espaco_do_gadget(item)
	if antigo != -1:
		gadgets[antigo] = null
	gadgets[espaco] = item
	mudou.emit()


func desequipar(espaco: int) -> void:
	gadgets[espaco] = null
	mudou.emit()


func espaco_do_gadget(item: Item) -> int:
	return gadgets.find(item)


func estado_de(id: String) -> Dictionary:
	if not estado.has(id):
		estado[id] = {}
	return estado[id]


func unidades(id: String) -> int:
	return estado_de(id).get("unidades", 0)


func definir_unidades(item: Item, quantas: int) -> void:
	var estado_item := estado_de(item.id)
	estado_item["unidades"] = quantas
	estado_item["carga"] = float(quantas) / item.maximo_unidades


func _somar_unidade(item: Item) -> bool:
	var atual := unidades(item.id)
	if atual >= item.maximo_unidades:
		aviso.emit("%s: no máximo %d" % [item.nome, item.maximo_unidades])
		return false
	definir_unidades(item, atual + 1)
	item_pego.emit(item)
	mudou.emit()
	return true
