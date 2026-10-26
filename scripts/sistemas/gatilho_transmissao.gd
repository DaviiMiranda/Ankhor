class_name GatilhoTransmissao
extends Area2D

@export var transmissao: Transmissao
@export var item_necessario: String = "radio"
@export var marca_necessaria: String = ""
@export var na_sala_inteira: bool = false
@export var depois_da_transmissao: String = ""
@export_file("*.json") var depois_do_dialogo: String = ""

var _dentro := false


func _ready() -> void:
	body_entered.connect(_ao_entrar)
	body_exited.connect(_ao_sair)
	Inventario.mudou.connect(_tentar)
	Progresso.mudou.connect(_tentar.unbind(1))
	Radio.transmissao_pedida.connect(_tentar.unbind(1))
	Dialogos.terminou.connect(_tentar.unbind(1))
	if na_sala_inteira:
		_dentro = true
		_tentar.call_deferred()


func _ao_entrar(corpo: Node2D) -> void:
	if corpo is Gabriel:
		_dentro = true
		_tentar()


func _ao_sair(corpo: Node2D) -> void:
	if corpo is Gabriel and not na_sala_inteira:
		_dentro = false


func _tentar() -> void:
	if _dentro and transmissao and Inventario.tem(item_necessario) and _marca_ok() and _ordem_ok():
		Radio.transmitir(transmissao)


func _marca_ok() -> bool:
	return marca_necessaria.is_empty() or Progresso.tem(marca_necessaria)


func _ordem_ok() -> bool:
	var transmissao_ok := depois_da_transmissao.is_empty() or Radio.ja_ouviu(depois_da_transmissao)
	var dialogo_ok := depois_do_dialogo.is_empty() or Dialogos.ja_viu(depois_do_dialogo)
	return transmissao_ok and dialogo_ok
