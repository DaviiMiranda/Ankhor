class_name SalaCinema
extends SalaDaNave

const FILEIRAS: Array[float] = [5.1, 3.5, 1.9, -1.9, -3.5]
const POLTRONAS_POR_LADO := 5
const X_DA_PRIMEIRA_POLTRONA := 1.7
const ESPACO_ENTRE_POLTRONAS := 0.72

var _tela: StandardMaterial3D
var _tempo := 0.0


func _process(delta: float) -> void:
	_tempo += delta
	_tela.emission_energy_multiplier = 0.55 + 0.25 * sin(_tempo * 7.0) * sin(_tempo * 2.3)


func _decorar() -> void:
	_tela = cor_acesa(Color(0.75, 0.1, 0.07), 0.6)
	var z := tamanho.z / 2.0 - 0.12
	bloco(Vector3(9.4, 2.0, 0.06), Vector3(0.0, 3.25, -z), material("borracha"))
	var quadro := bloco(Vector3(9.0, 1.7, 0.04), Vector3(0.0, 3.25, -z + 0.04), _tela)
	quadro.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	for fileira in FILEIRAS:
		for lado: float in [-1.0, 1.0]:
			_montar_fileira(fileira, lado)
	lampada_de_teto(Vector3(0.0, tamanho.y, -4.9), LampadaDaNave.Estado.ACESA, 2.6, Color(1.0, 0.3, 0.2), 2.4)
	for lugar: Vector3 in [Vector3(-5.5, tamanho.y, 3.5), Vector3(5.5, tamanho.y, 3.5), Vector3(-5.5, tamanho.y, -3.5), Vector3(5.5, tamanho.y, -3.5), Vector3(0.0, tamanho.y, 2.8)]:
		lampada_de_teto(lugar, LampadaDaNave.Estado.MORTA, 3.6, COR_QUENTE, 2.4)
	placa("CINEMA DE BORDO", Vector3(-tamanho.x / 2.0 + 0.012, 3.0, 0.0), PI / 2.0, 0.03)


func _montar_fileira(z: float, lado: float) -> void:
	var meio := X_DA_PRIMEIRA_POLTRONA + ESPACO_ENTRE_POLTRONAS * float(POLTRONAS_POR_LADO - 1) / 2.0
	var largura := ESPACO_ENTRE_POLTRONAS * float(POLTRONAS_POR_LADO)
	forma(Vector3(largura, 0.95, 0.75), Vector3(lado * meio, 0.475, z))
	for indice in POLTRONAS_POR_LADO:
		var x := lado * (X_DA_PRIMEIRA_POLTRONA + ESPACO_ENTRE_POLTRONAS * float(indice))
		bloco(Vector3(0.6, 0.42, 0.56), Vector3(x, 0.21, z), material("veludo"))
		bloco(Vector3(0.6, 0.9, 0.14), Vector3(x, 0.47, z + 0.3), material("veludo"))
		bloco(Vector3(0.08, 0.2, 0.5), Vector3(x + 0.34, 0.5, z), material("moldura"))
