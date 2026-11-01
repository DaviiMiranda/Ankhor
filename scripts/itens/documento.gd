class_name Documento
extends Resource

@export var id: String = ""
@export var titulo: String = ""
@export var autor: String = ""
@export_enum("pergaminho", "caderno_clarice", "caderno_gabriel", "carta", "carta_faroleiro", "jornal") var papel: String = "caderno_gabriel"
@export var conta_historia: bool = true
@export var imagem: Texture2D
@export_multiline var legenda: String = ""
@export_multiline var nota_na_margem: String = ""
@export_multiline var paginas: PackedStringArray = PackedStringArray()
@export_multiline var anotacao: String = ""
