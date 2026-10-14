class_name RedeDoLabirinto
extends Node

signal liberada

const MARCA_LIBERADA := "labirinto_saida_liberada"
const PREFIXO_DA_MARCA := "labirinto_no_"

@export var total_de_nos: int = 3
@export var transmissao: Transmissao


func _ready() -> void:
	Progresso.mudou.connect(_ao_marcar)
	if Progresso.tem(MARCA_LIBERADA):
		liberada.emit.call_deferred()


func nos_invadidos() -> int:
	var quantos := 0
	for numero in range(1, total_de_nos + 1):
		if Progresso.tem(PREFIXO_DA_MARCA + str(numero)):
			quantos += 1
	return quantos


func _ao_marcar(marca: String) -> void:
	if not marca.begins_with(PREFIXO_DA_MARCA):
		return
	var quantos := nos_invadidos()
	if quantos < total_de_nos:
		Inventario.aviso.emit("Nó %d de %d invadido" % [quantos, total_de_nos])
		return
	Progresso.marcar(MARCA_LIBERADA)
	Inventario.aviso.emit("Rede invadida. A saída foi liberada")
	Radio.transmitir(transmissao)
	liberada.emit()
