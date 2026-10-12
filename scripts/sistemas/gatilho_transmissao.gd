class_name GatilhoTransmissao
extends Area2D

@export var transmissao: Transmissao
@export var item_necessario: String = "radio"
@export var marca_necessaria: String = ""

var _dentro := false


func _ready() -> void:
	body_entered.connect(_ao_entrar)
	body_exited.connect(_ao_sair)
	Inventario.mudou.connect(_tentar)
	Progresso.mudou.connect(_tentar.unbind(1))


func _ao_entrar(corpo: Node2D) -> void:
	if corpo is Gabriel:
		_dentro = true
		_tentar()


func _ao_sair(corpo: Node2D) -> void:
	if corpo is Gabriel:
		_dentro = false


func _tentar() -> void:
	if _dentro and transmissao and Inventario.tem(item_necessario) and _marca_ok():
		Radio.transmitir(transmissao)


func _marca_ok() -> bool:
	return marca_necessaria.is_empty() or Progresso.tem(marca_necessaria)
