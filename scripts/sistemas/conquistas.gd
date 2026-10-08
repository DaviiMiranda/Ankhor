extends Node

signal desbloqueada(conquista: Conquista)

const CAMINHO_SALVO := "user://conquistas.cfg"
const SECAO := "desbloqueadas"

var todas: Array[Conquista] = [
	preload("res://dados/conquistas/01_luz_no_escuro.tres"),
	preload("res://dados/conquistas/02_sintonia.tres"),
	preload("res://dados/conquistas/03_um_segundo_de_dia.tres"),
	preload("res://dados/conquistas/04_arquivos_do_futuro.tres"),
	preload("res://dados/conquistas/05_primeira_pagina.tres"),
	preload("res://dados/conquistas/06_rato_de_biblioteca.tres"),
	preload("res://dados/conquistas/07_fim_da_linha.tres"),
	preload("res://dados/conquistas/08_fora_da_biblioteca.tres"),
	preload("res://dados/conquistas/09_fenda_fechada.tres"),
]

var _desbloqueadas := {}


func _ready() -> void:
	_carregar()
	Inventario.item_pego.connect(_ao_pegar_item)
	Vida.morreu.connect(_ao_morrer)
	Caderno.anotado.connect(_ao_anotar)


func desbloquear(id: String) -> void:
	var conquista := buscar(id)
	if conquista == null or esta_desbloqueada(id):
		return
	_desbloqueadas[id] = Time.get_unix_time_from_system()
	_salvar()
	desbloqueada.emit(conquista)


func esta_desbloqueada(id: String) -> bool:
	return _desbloqueadas.has(id)


func total_desbloqueadas() -> int:
	return _desbloqueadas.size()


func buscar(id: String) -> Conquista:
	for conquista in todas:
		if conquista.id == id:
			return conquista
	return null


func _desbloquear_por(gatilho: Conquista.Gatilho, alvo: String = "", quantidade: int = 0) -> void:
	for conquista in todas:
		if conquista.gatilho != gatilho:
			continue
		if not conquista.alvo.is_empty() and conquista.alvo != alvo:
			continue
		if quantidade < conquista.quantidade and gatilho == Conquista.Gatilho.ANOTACOES:
			continue
		desbloquear(conquista.id)


func _ao_pegar_item(item: Item) -> void:
	_desbloquear_por(Conquista.Gatilho.ITEM, item.id)


func _ao_morrer() -> void:
	_desbloquear_por(Conquista.Gatilho.MORTE)


func _ao_anotar(_titulo: String) -> void:
	_desbloquear_por(Conquista.Gatilho.ANOTACOES, "", Caderno.anotacoes.size())


func _carregar() -> void:
	var arquivo := ConfigFile.new()
	if arquivo.load(CAMINHO_SALVO) != OK or not arquivo.has_section(SECAO):
		return
	for id in arquivo.get_section_keys(SECAO):
		_desbloqueadas[id] = arquivo.get_value(SECAO, id)


func _salvar() -> void:
	var arquivo := ConfigFile.new()
	for id in _desbloqueadas:
		arquivo.set_value(SECAO, id, _desbloqueadas[id])
	arquivo.save(CAMINHO_SALVO)
