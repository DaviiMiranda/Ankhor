@tool
class_name ColoniaFungos
extends Interagivel

const ID_POTE := "pote_fungos"


func _ready() -> void:
	texto_acao = "Recarregar pote"
	super()


func pode_interagir() -> bool:
	if not Inventario.tem(ID_POTE):
		return false
	return Inventario.estado_de(ID_POTE).get("carga", 1.0) < 1.0


func interagir() -> void:
	Inventario.estado_de(ID_POTE)["carga"] = 1.0
