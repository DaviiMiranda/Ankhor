extends Node

signal mudou(marca: String)

var marcas: Dictionary = {}


func _ready() -> void:
	limpar()


func limpar() -> void:
	marcas = {}


func marcar(marca: String) -> void:
	if marca.is_empty() or tem(marca):
		return
	marcas[marca] = true
	mudou.emit(marca)


func tem(marca: String) -> bool:
	return marcas.has(marca)
