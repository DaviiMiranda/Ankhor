class_name Transmissao
extends Resource

@export var id: String = ""
@export var falante: String = ""
@export_multiline var falas: PackedStringArray = PackedStringArray()
@export var falantes: PackedStringArray = PackedStringArray()
@export var vozes: Array[AudioStream] = []
@export var titulo_anotacao: String = ""
@export_multiline var anotacao: String = ""


func falante_da_fala(indice: int) -> String:
	if indice < falantes.size() and not falantes[indice].is_empty():
		return falantes[indice]
	return falante
