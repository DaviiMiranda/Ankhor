class_name Fase
extends Resource

@export var nome: String = ""
@export_file("*.tscn") var cena: String = ""


func pronta() -> bool:
	return not cena.is_empty()
