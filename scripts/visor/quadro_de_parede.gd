class_name QuadroDeParede
extends FocoVisor

@export var colecao: Colecao


func _init() -> void:
	alcance = 2.4
	ocupacao = 0.8


func _ready() -> void:
	visible = colecao != null and Colecionaveis.completa(colecao)
	if not visible:
		return
	super()
	texto_acao = "Olhar: " + colecao.nome_da_recompensa


func titulo_focado() -> String:
	return colecao.nome_da_recompensa


func descricao_focada() -> String:
	return colecao.descricao_da_recompensa
