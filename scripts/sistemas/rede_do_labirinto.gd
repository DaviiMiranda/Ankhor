class_name RedeDoLabirinto
extends Node

const MARCA_REDE_INVADIDA := "labirinto_rede_invadida"
const PREFIXO_DA_MARCA := "labirinto_no_"

@export var total_de_nos: int = 3
@export var transmissao: Transmissao


func _ready() -> void:
	Progresso.mudou.connect(_ao_marcar)


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
	Progresso.marcar(MARCA_REDE_INVADIDA)
	Inventario.aviso.emit("Rede invadida. Volte ao Zane")
	Radio.transmitir(transmissao)
