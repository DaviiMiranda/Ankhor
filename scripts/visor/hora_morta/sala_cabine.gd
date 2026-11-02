class_name SalaCabine
extends SalaDaNave

var chave: ObjetoDaNave
var _peca_da_chave: MeshInstance3D


func _montar_parede_leste() -> void:
	janelas_a_leste(2.2)


func _decorar() -> void:
	lampada_de_teto(Vector3(0.0, tamanho.y, 0.0), LampadaDaNave.Estado.MORTA, 3.6, COR_FRIA, 2.2)
	bloco_solido(Vector3(1.0, 0.75, 2.4), Vector3(1.0, 0.375, 0.0), material("parede_escura"))
	bloco(Vector3(1.05, 0.04, 2.45), Vector3(1.0, 0.77, 0.0), material("moldura"))
	bloco_solido(Vector3(0.5, 0.5, 0.5), Vector3(0.0, 0.25, 0.0), material("veludo"))
	bloco(Vector3(0.5, 0.7, 0.1), Vector3(-0.25, 0.8, 0.0), material("veludo")).rotation.y = PI / 2.0
	_peca_da_chave = bloco(Vector3(0.16, 0.02, 0.07), Vector3(0.9, 0.8, 0.5), cor_acesa(Color(1.0, 0.75, 0.2), 1.8))
	chave = novo_objeto("Pegar a chave do hangar", Vector3(0.9, 0.82, 0.5), 1.0)
	placa("COMANDANTE", Vector3(-tamanho.x / 2.0 + 0.012, 1.9, 1.7), PI / 2.0)


func tirar_a_chave() -> void:
	_peca_da_chave.visible = false
	chave.texto_acao = ""
