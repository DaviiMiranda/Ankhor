extends Node

signal transmissao_pedida(transmissao: Transmissao)

var ouvidas: Dictionary = {}
var pendentes: Array[Transmissao] = []
var fala_em_andamento := 0
var tempo_em_andamento := 0.0


func _ready() -> void:
	limpar()


func limpar() -> void:
	ouvidas = {}
	pendentes = []
	_zerar_andamento()


func transmitir(transmissao: Transmissao) -> void:
	if transmissao == null or ja_ouviu(transmissao.id):
		return
	ouvidas[transmissao.id] = true
	pendentes.append(transmissao)
	transmissao_pedida.emit(transmissao)


func concluir(transmissao: Transmissao) -> void:
	pendentes.erase(transmissao)
	_zerar_andamento()


func guardar_andamento(transmissao: Transmissao, fala: int, tempo: float) -> void:
	if pendentes.has(transmissao):
		fala_em_andamento = fala
		tempo_em_andamento = tempo


func tem_andamento() -> bool:
	return fala_em_andamento > 0 or tempo_em_andamento > 0.0


func ja_ouviu(id: String) -> bool:
	return ouvidas.has(id)


func _zerar_andamento() -> void:
	fala_em_andamento = 0
	tempo_em_andamento = 0.0
