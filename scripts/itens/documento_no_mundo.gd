class_name DocumentoNoMundo
extends Interagivel

@export var documento: Documento


func interagir() -> void:
	if documento:
		Caderno.ler(documento)
