class_name SalaHangar
extends SalaDaNave

const LUGAR_DA_NAVE := Vector3(0.0, 0.0, -2.4)

var nave_menor: ObjetoDaNave


func _montar_parede_leste() -> void:
	janelas_a_leste(2.2)


func _decorar() -> void:
	for lugar: Vector3 in [Vector3(-3.5, tamanho.y, 2.5), Vector3(3.5, tamanho.y, 2.5), Vector3(-3.5, tamanho.y, -3.5), Vector3(3.5, tamanho.y, -3.5)]:
		lampada_de_teto(lugar, LampadaDaNave.Estado.ACESA, 4.6, COR_FRIA, 3.0)
	_montar_nave_menor()
	caixote(Vector3(-5.8, 0.0, 3.4), Vector3(1.4, 1.2, 1.4))
	caixote(Vector3(-4.3, 0.0, 4.2), Vector3(1.0, 0.8, 1.0))
	caixote(Vector3(-5.6, 1.2, 3.5), Vector3(0.8, 0.7, 0.8))
	caixote(Vector3(5.6, 0.0, -4.8), Vector3(1.3, 1.0, 1.3))
	placa("HANGAR", Vector3(-tamanho.x / 2.0 + 0.012, 3.0, 0.0), PI / 2.0, 0.03)
	bloco(Vector3(6.0, 0.012, 0.16), Vector3(0.0, 0.01, LUGAR_DA_NAVE.z + 3.4), material("perigo"))


func _montar_nave_menor() -> void:
	var z := LUGAR_DA_NAVE.z
	forma(Vector3(3.0, 2.4, 6.0), Vector3(0.0, 1.2, z))
	bloco(Vector3(2.2, 1.5, 4.4), Vector3(0.0, 1.55, z), material("parede"))
	bloco(Vector3(1.5, 0.9, 1.3), Vector3(0.0, 1.5, z + 2.6), material("parede_escura"))
	bloco(Vector3(1.1, 0.5, 0.05), Vector3(0.0, 1.72, z + 3.26), cor_acesa(Color(0.2, 0.7, 1.0), 1.3))
	for lado: float in [-1.0, 1.0]:
		bloco(Vector3(3.0, 0.16, 2.2), Vector3(lado * 2.3, 1.3, z - 0.6), material("costela"))
		tubo(0.42, 1.2, Vector3(lado * 0.8, 1.6, z - 2.8), material("borracha"), Vector3.BACK)
		bloco(Vector3(0.14, 0.8, 0.14), Vector3(lado * 0.9, 0.4, z + 1.4), material("corrimao"))
		bloco(Vector3(0.14, 0.8, 0.14), Vector3(lado * 0.9, 0.4, z - 1.6), material("corrimao"))
	bloco(Vector3(0.9, 1.4, 0.06), Vector3(1.13, 1.2, z + 0.2), material("borracha")).rotation.y = PI / 2.0
	bloco(Vector3(0.08, 0.08, 0.08), Vector3(1.16, 1.5, z + 0.75), cor_acesa(Color(0.2, 1.0, 0.4), 2.4))
	placa("EMBARQUE", Vector3(1.14, 2.08, z + 0.2), PI / 2.0, 0.0105, Color(0.95, 0.42, 0.25, 1.0))
	nave_menor = novo_objeto("Entrar na nave e decolar", Vector3(1.5, 1.2, z + 0.2), 1.5)
