extends Node

signal coletado(colecao: Colecao, numero: int)
signal completada(colecao: Colecao)

const PASTA := "res://dados/colecoes/"

var pecas: Dictionary = {}


func limpar() -> void:
	pecas = {}


func coletar(colecao: Colecao, numero: int) -> void:
	var chave := _chave(colecao.id, numero)
	if pecas.has(chave):
		return
	pecas[chave] = true
	coletado.emit(colecao, numero)
	if completa(colecao):
		completada.emit(colecao)


func tem(id_colecao: String, numero: int) -> bool:
	return pecas.has(_chave(id_colecao, numero))


func quantidade(id_colecao: String) -> int:
	var prefixo := id_colecao + ":"
	var quantas := 0
	for chave in pecas:
		if chave.begins_with(prefixo):
			quantas += 1
	return quantas


func todas() -> Array[Colecao]:
	var colecoes: Array[Colecao] = []
	for arquivo in ResourceLoader.list_directory(PASTA):
		if not arquivo.ends_with(".tres"):
			continue
		var colecao := load(PASTA + arquivo) as Colecao
		if colecao:
			colecoes.append(colecao)
	return colecoes


func completa(colecao: Colecao) -> bool:
	return quantidade(colecao.id) >= colecao.total


func _chave(id_colecao: String, numero: int) -> String:
	return "%s:%d" % [id_colecao, numero]
