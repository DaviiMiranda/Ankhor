class_name Colecao
extends Resource

@export var id: String = ""
@export var nome: String = ""
@export var item: Item
@export var total: int = 3
@export_multiline var texto_completa: String = ""


func item_com_progresso(quantidade: int) -> Item:
	var copia := item.duplicate() as Item
	copia.descricao = "%s\n\n%d de %d." % [item.descricao, quantidade, total]
	if quantidade >= total and not texto_completa.is_empty():
		copia.descricao += " " + texto_completa
	return copia
