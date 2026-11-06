extends Node

signal mudou
signal item_pego(item: Item)
signal item_novo(item: Item)
signal aviso(texto: String)

const LINHAS := 3
const COLUNAS := 4
const ESPACOS_GADGET := 3
const TECLA_DO_BRACO := 4

var grade: Array = []
var gadgets: Array = []
var braco: Item = null
var estado: Dictionary = {}
var pegos: Dictionary = {}
var vistos: Dictionary = {}
var largados: Dictionary = {}
var _reserva: Dictionary = {}


func _ready() -> void:
	limpar()


func emprestar_kit(kit: Array) -> void:
	if _reserva.is_empty():
		var copia_da_grade := []
		for linha in grade:
			copia_da_grade.append((linha as Array).duplicate())
		_reserva = {
			"grade": copia_da_grade,
			"gadgets": gadgets.duplicate(),
			"braco": braco,
			"estado": estado.duplicate(true),
			"vistos": vistos.duplicate(),
			"largados": largados.duplicate(true),
		}
	_esvaziar()
	for item: Item in kit:
		vistos[item.id] = true
		_guardar_na_primeira_vaga(item)
		if item.maximo_unidades > 0:
			definir_unidades(item, item.maximo_unidades)
	mudou.emit()


func devolver_kit() -> void:
	if _reserva.is_empty():
		return
	grade = _reserva["grade"]
	gadgets = _reserva["gadgets"]
	braco = _reserva["braco"]
	estado = _reserva["estado"]
	vistos = _reserva["vistos"]
	largados = _reserva["largados"]
	_reserva = {}
	mudou.emit()


func com_kit_emprestado() -> bool:
	return not _reserva.is_empty()


func _esvaziar() -> void:
	grade = []
	for linha in LINHAS:
		var colunas := []
		colunas.resize(COLUNAS)
		grade.append(colunas)
	gadgets = []
	gadgets.resize(ESPACOS_GADGET)
	braco = null
	estado = {}
	largados = {}


func _guardar_na_primeira_vaga(item: Item) -> void:
	for linha in LINHAS:
		for coluna in COLUNAS:
			if grade[linha][coluna] == null:
				grade[linha][coluna] = item
				if item.vai_no_espaco_do_braco:
					braco = item
				if item.equipavel and gadgets.find(null) != -1:
					gadgets[gadgets.find(null)] = item
				return


func limpar() -> void:
	grade = []
	for linha in LINHAS:
		var colunas := []
		colunas.resize(COLUNAS)
		grade.append(colunas)
	gadgets = []
	gadgets.resize(ESPACOS_GADGET)
	braco = null
	estado = {}
	pegos = {}
	vistos = {}
	largados = {}
	_reserva = {}
	mudou.emit()


func adicionar(item: Item) -> bool:
	largados.erase(item.id)
	if item.maximo_unidades > 0 and tem(item.id):
		return _somar_unidade(item)
	for linha in LINHAS:
		for coluna in COLUNAS:
			if grade[linha][coluna] == null:
				grade[linha][coluna] = item
				if item.maximo_unidades > 0:
					definir_unidades(item, 1)
				if item.vai_no_espaco_do_braco:
					braco = item
				if item.equipavel and espaco_do_gadget(item) == -1:
					var livre := gadgets.find(null)
					if livre != -1:
						gadgets[livre] = item
				item_pego.emit(item)
				_registrar_visto(item)
				mudou.emit()
				return true
	return false


func remover(id: String) -> void:
	for linha in LINHAS:
		for coluna in COLUNAS:
			var item: Item = grade[linha][coluna]
			if item != null and item.id == id:
				grade[linha][coluna] = null
				var espaco := espaco_do_gadget(item)
				if espaco != -1:
					gadgets[espaco] = null
				if braco == item:
					braco = null
				mudou.emit()
				return


func largar(item: Item, cena: String, posicao: Vector2) -> void:
	remover(item.id)
	largados[item.id] = {"cena": cena, "posicao": posicao}


func item_pesado() -> Item:
	for linha in grade:
		for item in linha:
			if item != null and item.carga_pesada:
				return item
	return null


func carregando_peso() -> bool:
	return item_pesado() != null


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


func _registrar_visto(item: Item) -> void:
	if vistos.has(item.id):
		return
	vistos[item.id] = true
	item_novo.emit(item)
