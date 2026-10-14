class_name ZaneOficina
extends ConversaNpc

const NOTEBOOK := preload("res://dados/itens/notebook.tres")
const MARCA_NOTEBOOK_ENTREGUE := "labirinto_notebook_entregue"
const MARCA_SAIDA_LIBERADA := "labirinto_saida_liberada"

@export_file("*.json") var conversa_concluida: String = ""
@export_file("*.json") var conversa_do_notebook: String = ""


func interagir() -> void:
	if Progresso.tem(MARCA_SAIDA_LIBERADA) and not conversa_concluida.is_empty():
		Dialogos.iniciar(conversa_concluida)
		return
	if Dialogos.ja_viu(primeira_conversa) and not Progresso.tem(MARCA_NOTEBOOK_ENTREGUE):
		Dialogos.iniciar(conversa_do_notebook)
		_entregar_ao_terminar()
		return
	var primeira_vez := not Dialogos.ja_viu(primeira_conversa)
	super()
	if primeira_vez and Dialogos.ativo:
		_entregar_ao_terminar()


func _entregar_ao_terminar() -> void:
	if Dialogos.ativo:
		Dialogos.terminou.connect(_entregar_notebook, CONNECT_ONE_SHOT)


func _entregar_notebook(_caminho: String) -> void:
	if Inventario.tem(NOTEBOOK.id) or Inventario.adicionar(NOTEBOOK):
		Progresso.marcar(MARCA_NOTEBOOK_ENTREGUE)
		Inventario.aviso.emit("Notebook do Zane recebido")
	else:
		Inventario.aviso.emit("Inventário cheio: libere um espaço e fale com o Zane")
