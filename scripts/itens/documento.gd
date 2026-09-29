class_name Documento
extends Resource

@export var id: String = ""
@export var titulo: String = ""
@export var autor: String = ""
@export_enum("pergaminho", "caderno_clarice", "caderno_gabriel") var papel: String = "caderno_gabriel"
@export_multiline var paginas: PackedStringArray = PackedStringArray()
@export_multiline var anotacao: String = ""
