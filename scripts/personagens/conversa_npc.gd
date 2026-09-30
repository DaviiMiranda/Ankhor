class_name ConversaNpc
extends Interagivel

@export_file("*.json") var primeira_conversa: String = ""
@export_file("*.json") var conversa_de_novo: String = ""


func pode_interagir() -> bool:
	return not Dialogos.ativo and not primeira_conversa.is_empty()


func interagir() -> void:
	var caminho := primeira_conversa
	if Dialogos.ja_viu(primeira_conversa) and not conversa_de_novo.is_empty():
		caminho = conversa_de_novo
	Dialogos.iniciar(caminho)
