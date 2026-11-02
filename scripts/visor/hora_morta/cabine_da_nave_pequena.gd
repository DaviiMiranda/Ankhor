class_name CabineDaNavePequena
extends SalaDaNave

const JANELA := Vector4(3.3, 0.9, 1.45, 0.5)


func _montar_parede_leste() -> void:
	janela_em_x(tamanho.x / 2.0, 0.0, tamanho.z, 0.0, tamanho.y, JANELA)


func _decorar() -> void:
	lampada_de_teto(Vector3(-0.6, tamanho.y, 0.0), LampadaDaNave.Estado.ACESA, 3.0, COR_FRIA, 1.6)
	_montar_painel_frontal()
	for lado: float in [-1.0, 1.0]:
		_montar_painel_lateral(lado)
	placa("NAVE DE FUGA", Vector3(-tamanho.x / 2.0 + 0.012, 1.8, 0.0), -PI / 2.0, 0.02)


func _montar_painel_frontal() -> void:
	var x := tamanho.x / 2.0 - 0.6
	bloco_solido(Vector3(1.1, 0.72, tamanho.z - 0.6), Vector3(x, 0.36, 0.0), material("parede_escura"))
	bloco(Vector3(1.14, 0.03, tamanho.z - 0.56), Vector3(x, 0.735, 0.0), material("moldura"))
	for z: float in [-2.6, -1.3, 1.3, 2.6]:
		bloco(Vector3(0.5, 0.012, 0.8), Vector3(x, 0.755, z), cor_acesa(Color(0.08, 0.3, 0.5), 0.5))
	for indice in 12:
		var z := -0.55 + float(indice % 6) * 0.22
		var fileira := float(indice / 6) * 0.2
		var cor := Color(1.0, 0.65, 0.2) if indice % 3 == 0 else Color(0.25, 1.0, 0.45)
		bloco(Vector3(0.06, 0.016, 0.06), Vector3(x - 0.1 + fileira, 0.758, z), cor_acesa(cor, 1.8))


func _montar_painel_lateral(lado: float) -> void:
	var z := lado * (tamanho.z / 2.0 - 0.36)
	bloco_solido(Vector3(3.0, 1.0, 0.5), Vector3(0.2, 0.5, z), material("parede_escura"))
	bloco(Vector3(3.04, 0.03, 0.54), Vector3(0.2, 1.01, z), material("moldura"))
	bloco(Vector3(1.4, 0.7, 0.03), Vector3(0.2, 1.65, lado * (tamanho.z / 2.0 - 0.1)), cor_acesa(Color(0.12, 0.36, 0.55), 0.6))
	for y: float in [0.3, 0.42, 0.54]:
		tubo(0.022, tamanho.x, Vector3(0.0, y + 1.75, lado * (tamanho.z / 2.0 - 0.06)), material("cano"), Vector3.RIGHT)
