extends Node

signal transmissao_pedida(transmissao: Transmissao)

var ouvidas: Dictionary = {}
var pendentes: Array[Transmissao] = []


func _ready() -> void:
	limpar()


func limpar() -> void:
	ouvidas = {}
	pendentes = []


func transmitir(transmissao: Transmissao) -> void:
	if transmissao == null or ja_ouviu(transmissao.id):
		return
	ouvidas[transmissao.id] = true
	pendentes.append(transmissao)
	transmissao_pedida.emit(transmissao)


func concluir(transmissao: Transmissao) -> void:
	pendentes.erase(transmissao)


func ja_ouviu(id: String) -> bool:
	return ouvidas.has(id)
