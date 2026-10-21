extends Node3D

const CORES_DAS_CADENTES := [Color(2.4, 2.4, 2.6), Color(1.6, 2.3, 2.8), Color(2.6, 2.2, 1.5)]
const CORES_DAS_LUZES := [
	Color(0.6, 2.3, 2.8), Color(2.6, 0.7, 2.1), Color(2.7, 1.6, 0.5),
	Color(1.3, 0.9, 2.8), Color(0.8, 2.6, 1.1), Color(2.7, 0.8, 0.8),
]
const PONTOS_NO_RASTRO := 22
const CHANCE_DE_CADENTE := 0.6

@export var intervalo := Vector2(1.0, 3.5)
@export var altura_minima: float = 3.4
@export var altura_maxima: float = 6.0
@export var raio_da_passagem: float = 2.2
@export var tamanho_do_ponto: float = 0.05

var _sorteio := RandomNumberGenerator.new()
var _relogio := Timer.new()


func _ready() -> void:
	_sorteio.randomize()
	_relogio.one_shot = true
	_relogio.timeout.connect(_lancar_a_proxima)
	add_child(_relogio)
	_relogio.start(_sorteio.randf_range(intervalo.x, intervalo.y))


func _lancar_a_proxima() -> void:
	if _sorteio.randf() < CHANCE_DE_CADENTE:
		_lancar(_escolher(CORES_DAS_CADENTES), _sorteio.randf_range(9.0, 14.0), _sorteio.randf_range(0.25, 0.5), 0.035, _sorteio.randf_range(0.5, 0.9))
	else:
		_lancar(_escolher(CORES_DAS_LUZES), _sorteio.randf_range(5.0, 8.0), _sorteio.randf_range(-0.08, 0.08), 0.025, _sorteio.randf_range(1.0, 1.8))
	_relogio.start(_sorteio.randf_range(intervalo.x, intervalo.y))


func _escolher(cores: Array) -> Color:
	return cores[_sorteio.randi() % cores.size()]


func _lancar(cor: Color, velocidade: float, queda: float, espacamento: float, duracao: float) -> void:
	var passagem := Vector3(
		_sorteio.randf_range(-raio_da_passagem, raio_da_passagem),
		_sorteio.randf_range(altura_minima + 0.6, altura_maxima),
		_sorteio.randf_range(-raio_da_passagem, raio_da_passagem))
	var angulo := _sorteio.randf() * TAU
	var direcao := Vector3(cos(angulo), -queda, sin(angulo)).normalized()
	if direcao.y < 0.0:
		duracao = minf(duracao, 2.0 * (passagem.y - altura_minima) / (-direcao.y * velocidade))
	var inicio := passagem - direcao * velocidade * duracao / 2.0
	var materiais: Array[StandardMaterial3D] = []
	var rastro := _rastro(cor, direcao, espacamento, materiais)
	rastro.position = inicio
	add_child(rastro)
	var voo := rastro.create_tween()
	voo.tween_property(rastro, "position", inicio + direcao * velocidade * duracao, duracao)
	voo.parallel().tween_method(_brilhar.bind(materiais), 0.0, 1.0, duracao)
	voo.tween_callback(rastro.queue_free)


func _rastro(cor: Color, direcao: Vector3, espacamento: float, materiais: Array[StandardMaterial3D]) -> Node3D:
	var rastro := Node3D.new()
	for i in PONTOS_NO_RASTRO:
		var resto := 1.0 - float(i) / PONTOS_NO_RASTRO
		var material := StandardMaterial3D.new()
		material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		material.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
		material.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
		material.albedo_color = Color(cor, 0.0)
		material.set_meta("alfa", resto)
		materiais.append(material)
		var plano := QuadMesh.new()
		plano.size = Vector2.ONE * tamanho_do_ponto * lerpf(0.3, 1.0, resto)
		var ponto := MeshInstance3D.new()
		ponto.mesh = plano
		ponto.material_override = material
		ponto.position = -direcao * espacamento * i
		rastro.add_child(ponto)
	return rastro


func _brilhar(progresso: float, materiais: Array[StandardMaterial3D]) -> void:
	var envelope := sin(PI * progresso)
	for material in materiais:
		material.albedo_color.a = envelope * float(material.get_meta("alfa"))
