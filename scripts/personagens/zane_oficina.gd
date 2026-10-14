class_name ZaneOficina
extends ConversaNpc

const NOTEBOOK := preload("res://dados/itens/notebook.tres")
const MARCA_NOTEBOOK_ENTREGUE := "labirinto_notebook_entregue"
const MARCA_ALCAPAO_REVELADO := "labirinto_alcapao_revelado"

@export_file("*.json") var conversa_do_notebook: String = ""
@export_file("*.json") var conversa_do_alcapao: String = ""
@export_file("*.json") var conversa_depois_do_alcapao: String = ""


func interagir() -> void:
	if Progresso.tem(MARCA_ALCAPAO_REVELADO) and not conversa_depois_do_alcapao.is_empty():
		Dialogos.iniciar(conversa_depois_do_alcapao)
		return
	if Progresso.tem(RedeDoLabirinto.MARCA_REDE_INVADIDA) and not conversa_do_alcapao.is_empty():
		Dialogos.iniciar(conversa_do_alcapao)
		if Dialogos.ativo:
			Dialogos.terminou.connect(_revelar_alcapao, CONNECT_ONE_SHOT)
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


func _revelar_alcapao(_caminho: String) -> void:
	Progresso.marcar(MARCA_ALCAPAO_REVELADO)
	Inventario.aviso.emit("O Zane abriu o alçapão da oficina")
