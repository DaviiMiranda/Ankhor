class_name SalaMaquinas
extends SalaDaNave

const COR_SEM_ENERGIA := Color(1.0, 0.12, 0.08)
const COR_COM_ENERGIA := Color(0.2, 1.0, 0.4)

var quadro: ObjetoDaNave
var _luz_do_quadro: StandardMaterial3D
var _zumbido: AudioStreamPlayer3D


func _decorar() -> void:
	lampada_de_teto(Vector3(2.4, tamanho.y, 1.6), LampadaDaNave.Estado.ACESA, 2.2)
	lampada_de_teto(Vector3(-1.5, tamanho.y, -1.6), LampadaDaNave.Estado.MORTA, 3.0, COR_QUENTE)
	for z: float in [-1.7, 1.2]:
		_montar_gerador(Vector3(-1.2, 0.0, z))
	_montar_quadro()
	for y: float in [1.9, 2.15]:
		tubo(0.08, tamanho.x, Vector3(0.0, y, -tamanho.z / 2.0 + 0.3), material("cano"), Vector3.RIGHT)
	_zumbido = AudioStreamPlayer3D.new()
	_zumbido.stream = load("res://assets/audio/efeitos/robos/robo_zumbido.wav")
	_zumbido.position = Vector3(-1.2, 1.0, 0.0)
	_zumbido.volume_db = 2.0
	_zumbido.unit_size = 2.0
	_zumbido.max_distance = 12.0
	_zumbido.pitch_scale = 0.6
	_zumbido.bus = &"Efeitos"
	_zumbido.autoplay = true
	add_child(_zumbido)
	placa("MÁQUINAS", Vector3(-tamanho.x / 2.0 + 0.012, 2.1, 1.5), PI / 2.0)


func ligar_quadro() -> void:
	_luz_do_quadro.albedo_color = COR_COM_ENERGIA * 0.4
	_luz_do_quadro.emission = COR_COM_ENERGIA


func _montar_gerador(lugar: Vector3) -> void:
	forma(Vector3(1.5, 2.0, 1.5), lugar + Vector3.UP)
	tubo(0.7, 2.0, lugar + Vector3.UP, material("parede_escura"), Vector3.UP)
	for y: float in [0.3, 1.0, 1.7]:
		tubo(0.74, 0.08, lugar + Vector3.UP * y, material("costela"), Vector3.UP)
	bloco(Vector3(0.1, 0.1, 0.1), lugar + Vector3(0.76, 1.3, 0.0), material("perigo"))


func _montar_quadro() -> void:
	var x := -tamanho.x / 2.0 + 0.2
	var z := 2.3
	bloco_solido(Vector3(0.3, 1.3, 1.0), Vector3(x, 1.1, z), material("parede_escura"))
	_luz_do_quadro = cor_acesa(COR_SEM_ENERGIA, 2.2)
	bloco(Vector3(0.02, 0.1, 0.1), Vector3(x + 0.16, 1.55, z - 0.3), _luz_do_quadro)
	for indice in 3:
		bloco(Vector3(0.03, 0.16, 0.14), Vector3(x + 0.16, 1.15, z - 0.3 + float(indice) * 0.3), material("borracha"))
	bloco(Vector3(0.012, 0.08, 0.7), Vector3(x + 0.155, 0.75, z), material("perigo"))
	quadro = novo_objeto("Abrir o quadro de energia", Vector3(x + 0.16, 1.15, z))
