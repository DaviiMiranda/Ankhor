class_name GatilhoDialogo
extends Area2D

@export_file("*.json") var dialogo: String = ""
@export var marca_necessaria: String = ""
@export var marca_ao_terminar: String = ""
@export var aviso_ao_terminar: String = ""

var _dentro := false


func _ready() -> void:
	body_entered.connect(_ao_entrar)
	body_exited.connect(_ao_sair)
	Progresso.mudou.connect(_tentar.unbind(1))
	Dialogos.terminou.connect(_ao_terminar)


func _ao_entrar(corpo: Node2D) -> void:
	if corpo is Gabriel:
		_dentro = true
		_tentar.call_deferred()


func _ao_sair(corpo: Node2D) -> void:
	if corpo is Gabriel:
		_dentro = false


func _tentar() -> void:
	if not _dentro or dialogo.is_empty() or Dialogos.ativo or get_tree().paused:
		return
	if not marca_necessaria.is_empty() and not Progresso.tem(marca_necessaria):
		return
	if not marca_ao_terminar.is_empty() and Progresso.tem(marca_ao_terminar):
		return
	Dialogos.iniciar(dialogo)


func _ao_terminar(caminho: String) -> void:
	if caminho != dialogo:
		return
	Progresso.marcar(marca_ao_terminar)
	if not aviso_ao_terminar.is_empty():
		Inventario.aviso.emit(aviso_ao_terminar)
