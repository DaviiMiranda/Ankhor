class_name Transmissao
extends Resource

@export var id: String = ""
@export var falante: String = ""
@export_multiline var falas: PackedStringArray = PackedStringArray()
@export var vozes: Array[AudioStream] = []
@export var titulo_anotacao: String = ""
@export_multiline var anotacao: String = ""
