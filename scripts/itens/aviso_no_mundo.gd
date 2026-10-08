class_name AvisoNoMundo
extends Interagivel

@export_multiline var texto: String = ""


func interagir() -> void:
	Inventario.aviso.emit(texto)
