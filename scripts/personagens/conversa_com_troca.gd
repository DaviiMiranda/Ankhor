class_name ConversaComTroca
extends Interagivel

@export_file("*.json") var conversa_pedido: String = ""
@export_file("*.json") var conversa_pedido_de_novo: String = ""
@export_file("*.json") var conversa_troca: String = ""
@export_file("*.json") var conversa_depois: String = ""
@export var item_pedido: String = ""
@export var item_dado: Item
@export var marca_troca: String = ""


func pode_interagir() -> bool:
	return not Dialogos.ativo


func interagir() -> void:
	if Progresso.tem(marca_troca):
		Dialogos.iniciar(conversa_depois)
	elif Inventario.tem(item_pedido):
		Dialogos.iniciar(conversa_troca)
		if Dialogos.ativo:
			Dialogos.terminou.connect(_trocar, CONNECT_ONE_SHOT)
	elif Dialogos.ja_viu(conversa_pedido):
		Dialogos.iniciar(conversa_pedido_de_novo)
	else:
		Dialogos.iniciar(conversa_pedido)


func _trocar(_caminho: String) -> void:
	Inventario.remover(item_pedido)
	if item_dado:
		Inventario.adicionar(item_dado)
	Progresso.marcar(marca_troca)
