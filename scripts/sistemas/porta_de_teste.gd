class_name PortaDeTeste
extends Porta

@export var com_combate := false
@export var marcas_ao_entrar: PackedStringArray = []
@export var marcas_apagadas_ao_entrar: PackedStringArray = []


func _trocar_de_cena() -> void:
	for marca in marcas_apagadas_ao_entrar:
		Progresso.desmarcar(marca)
	for marca in marcas_ao_entrar:
		Progresso.marcar(marca)
	add_child(TudoColetado.new())
	if com_combate:
		ModoCombate.ativar()
	else:
		Checkpoints.limpar()
		Vida.limpar()
	super()
