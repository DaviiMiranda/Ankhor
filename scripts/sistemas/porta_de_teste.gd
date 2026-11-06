class_name PortaDeTeste
extends Porta

@export var com_combate := false


func _trocar_de_cena() -> void:
	if com_combate:
		ModoCombate.ativar()
	else:
		Checkpoints.limpar()
		Vida.limpar()
	super()
