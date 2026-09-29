extends Node

signal transmissao_pedida(transmissao: Transmissao)

var ouvidas: Dictionary = {}


func _ready() -> void:
	limpar()


func limpar() -> void:
	ouvidas = {}


func transmitir(transmissao: Transmissao) -> void:
	if transmissao == null or ja_ouviu(transmissao.id):
		return
	ouvidas[transmissao.id] = true
	transmissao_pedida.emit(transmissao)


func ja_ouviu(id: String) -> bool:
	return ouvidas.has(id)
