class_name SalaReunioes
extends SalaDaNave

const MEIO_COMPRIMENTO_DA_MESA := 4.0
const MEIA_LARGURA_DA_MESA := 1.3
const CADEIRAS_POR_LADO := 6
const ALTURA_DA_MESA := 0.76

var _holograma: MeshInstance3D
var _tempo := 0.0


func _process(delta: float) -> void:
	_tempo += delta
	_holograma.rotation.y = _tempo * 0.4
	_holograma.position.y = ALTURA_DA_MESA + 0.62 + 0.03 * sin(_tempo * 1.3)


func _decorar() -> void:
	_montar_mesa()
	_montar_cadeiras()
	_montar_holograma()
	_montar_telas_de_parede()
	lampada_de_teto(Vector3(0.0, tamanho.y, -4.9), LampadaDaNave.Estado.ACESA, 2.6, COR_FRIA, 2.4)
	for lugar: Vector3 in [Vector3(-5.5, tamanho.y, 3.5), Vector3(5.5, tamanho.y, 3.5), Vector3(-5.5, tamanho.y, -3.5), Vector3(5.5, tamanho.y, -3.5), Vector3(0.0, tamanho.y, 0.0)]:
		lampada_de_teto(lugar, LampadaDaNave.Estado.MORTA, 3.6, COR_QUENTE, 2.4)
	placa("SALA DE REUNIÕES", Vector3(-tamanho.x / 2.0 + 0.012, 2.5, 0.0), PI / 2.0, 0.026)
	placa("NAVE 67", Vector3(0.0, 2.65, tamanho.z / 2.0 - 0.012), PI, 0.03)


func _montar_mesa() -> void:
	var y := ALTURA_DA_MESA
	forma(Vector3((MEIO_COMPRIMENTO_DA_MESA + MEIA_LARGURA_DA_MESA) * 2.0, 0.9, MEIA_LARGURA_DA_MESA * 2.0), Vector3(0.0, 0.45, 0.0))
	bloco(Vector3(MEIO_COMPRIMENTO_DA_MESA * 2.0, 0.06, MEIA_LARGURA_DA_MESA * 2.0), Vector3(0.0, y, 0.0), material("moldura"))
	for lado: float in [-1.0, 1.0]:
		tubo(MEIA_LARGURA_DA_MESA, 0.06, Vector3(lado * MEIO_COMPRIMENTO_DA_MESA, y, 0.0), material("moldura"), Vector3.UP, 32)
		bloco(Vector3(0.5, y, 1.5), Vector3(lado * 2.6, y / 2.0, 0.0), material("parede_escura"))
	var faixa_da_mesa := bloco(Vector3(MEIO_COMPRIMENTO_DA_MESA * 2.0 - 0.3, 0.012, 0.05), Vector3(0.0, y + 0.036, 0.0), material_das_faixas)
	faixa_da_mesa.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	for x: float in [-3.2, -1.1, 1.3, 3.0]:
		bloco(Vector3(0.28, 0.008, 0.36), Vector3(x, y + 0.035, 0.68), material("reflexo"))
		bloco(Vector3(0.3, 0.012, 0.22), Vector3(x + 0.35, y + 0.038, -0.72), material("borracha"))


func _montar_cadeiras() -> void:
	var distancia := MEIA_LARGURA_DA_MESA + 0.45
	var largura := 2.0 * MEIO_COMPRIMENTO_DA_MESA
	for lado: float in [-1.0, 1.0]:
		forma(Vector3(largura, 0.95, 0.5), Vector3(0.0, 0.475, lado * distancia))
		for indice in CADEIRAS_POR_LADO:
			var x := -MEIO_COMPRIMENTO_DA_MESA + largura * (float(indice) + 0.5) / float(CADEIRAS_POR_LADO)
			_cadeira(Vector3(x, 0.0, lado * distancia), lado)


func _cadeira(lugar: Vector3, lado: float) -> void:
	bloco(Vector3(0.48, 0.08, 0.46), lugar + Vector3.UP * 0.46, material("veludo"))
	bloco(Vector3(0.48, 0.6, 0.07), lugar + Vector3(0.0, 0.8, lado * 0.21), material("veludo"))
	tubo(0.03, 0.42, lugar + Vector3.UP * 0.22, material("cano"), Vector3.UP)
	bloco(Vector3(0.42, 0.03, 0.42), lugar + Vector3.UP * 0.02, material("borracha"))


func _montar_holograma() -> void:
	var azul := cor_acesa(Color(0.12, 0.42, 0.75), 0.4)
	azul.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	azul.albedo_color.a = 0.25
	var esfera := SphereMesh.new()
	esfera.radius = 0.42
	esfera.height = 0.84
	esfera.radial_segments = 24
	esfera.rings = 12
	_holograma = MeshInstance3D.new()
	_holograma.mesh = esfera
	_holograma.material_override = azul
	_holograma.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_holograma.position = Vector3(0.0, ALTURA_DA_MESA + 0.62, 0.0)
	add_child(_holograma)
	tubo(0.24, 0.05, Vector3(0.0, ALTURA_DA_MESA + 0.05, 0.0), material("borracha"), Vector3.UP)
	tubo(0.17, 0.012, Vector3(0.0, ALTURA_DA_MESA + 0.08, 0.0), azul, Vector3.UP)


func _montar_telas_de_parede() -> void:
	var z := tamanho.z / 2.0 - 0.13
	for x: float in [-4.0, 4.0]:
		_tela_de_parede(Vector3(x, 1.6, -z), Vector3(2.6, 1.3, 0.05))
		_tela_de_parede(Vector3(x, 1.6, z), Vector3(2.6, 1.3, 0.05))


func _tela_de_parede(lugar: Vector3, medidas: Vector3) -> void:
	bloco(medidas + Vector3(0.14, 0.14, 0.0), lugar, material("borracha"))
	var luz := bloco(medidas, lugar - Vector3(0.0, 0.0, signf(lugar.z) * 0.03), cor_acesa(Color(0.1, 0.32, 0.5), 0.35))
	luz.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
