class_name GatilhoTransmissao
extends Area2D

@export var transmissao: Transmissao
@export var item_necessario: String = "radio"

var _dentro := false


func _ready() -> void:
	body_entered.connect(_ao_entrar)
	body_exited.connect(_ao_sair)
	Inventario.mudou.connect(_tentar)


func _ao_entrar(corpo: Node2D) -> void:
	if corpo is Gabriel:
		_dentro = true
		_tentar()


func _ao_sair(corpo: Node2D) -> void:
	if corpo is Gabriel:
		_dentro = false


func _tentar() -> void:
	if _dentro and transmissao and Inventario.tem(item_necessario):
		Radio.transmitir(transmissao)
