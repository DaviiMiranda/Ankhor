class_name ToqueDistante
extends AudioStreamPlayer

@export var marca_toque: String = "saida_tentada"
@export var marca_fim: String = "saida_destrancada"
@export var aviso: String = "Um telefone começou a tocar, longe. Parece vir do balcão."


func _ready() -> void:
	Progresso.mudou.connect(_ao_mudar)
	if _tocando():
		play()


func _ao_mudar(nova: String) -> void:
	if nova == marca_toque and _tocando():
		Inventario.aviso.emit(aviso)
		play()
	elif nova == marca_fim:
		stop()


func _tocando() -> bool:
	return Progresso.tem(marca_toque) and not Progresso.tem(marca_fim)
