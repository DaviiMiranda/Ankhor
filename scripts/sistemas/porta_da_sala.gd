class_name PortaDaSala
extends Interagivel

const CAMADAS_BLOQUEIO := 1 | 8
const ALTURA_PAREDE := 40.0
const LUZ_SO_NAS_PAREDES := 2
const MARGEM_ALCANCE := 24.0
const MARGEM_ROBO := 14.0
const ESCALA_RECOLHIDA := 0.12
const TAMANHO_LAMPADA := Vector2(4, 4)
const COR_TOPO := Color("#4a5663")
const COR_FRENTE := Color("#343e49")
const COR_RISCO := Color("#1b2229")
const COR_FECHADA := Color("#b7302a")
const COR_ABERTA := Color("#3fbf6e")
const ALTURA_SOM_ABRINDO := 1.0
const ALTURA_SOM_FECHANDO := 0.8

@export var tamanho := Vector2(64, 32)
@export var frente_visivel := true
@export var area_da_sala := Rect2()
@export var segundos_animando: float = 0.35
@export var segundos_aberta: float = 1.2

var aberta := false
var conteudo: Array[Node2D] = []

var _animacao: Tween
var _ocupantes: Array[Node2D] = []
var _escondidos: Array[Node2D] = []
var _folhas: Array[Node2D] = []
var _lampadas: Array[Polygon2D] = []
var _material_sem_luz := CanvasItemMaterial.new()
var _revelando := false
var _mostrando := true

@onready var _bloqueio: StaticBody2D = $Bloqueio
@onready var _forma_bloqueio: CollisionShape2D = $Bloqueio/Forma
@onready var _alcance: CollisionShape2D = $Alcance
@onready var _oclusor: LightOccluder2D = $Oclusor
@onready var _som: AudioStreamPlayer2D = $Som
@onready var _espera: Timer = $Espera


func _ready() -> void:
	super()
	_material_sem_luz.light_mode = CanvasItemMaterial.LIGHT_MODE_UNSHADED
	_preparar_formas()
	_montar_folhas()
	_espera.timeout.connect(fechar)
	_atualizar_conteudo()


func _physics_process(_delta: float) -> void:
	if not aberta:
		for corpo in _ocupantes:
			if is_instance_valid(corpo) and corpo is Robo and _perto_da_pegada(corpo.global_position, MARGEM_ROBO):
				abrir()
				break
	_atualizar_conteudo()


func pode_interagir() -> bool:
	return not aberta


func interagir() -> void:
	abrir()


func abrir() -> void:
	if aberta:
		return
	aberta = true
	_revelando = true
	_espera.stop()
	_bloqueio.set_deferred("collision_layer", 0)
	_oclusor.visible = false
	_tocar(ALTURA_SOM_ABRINDO)
	_animar(true)
	_atualizar_conteudo()


func fechar() -> void:
	if not aberta or not _ocupantes.is_empty():
		return
	aberta = false
	_bloqueio.set_deferred("collision_layer", CAMADAS_BLOQUEIO)
	_oclusor.visible = true
	_tocar(ALTURA_SOM_FECHANDO)
	_animar(false)
	_animacao.chain().tween_callback(_terminar_fechamento)


func _ao_entrar(corpo: Node2D) -> void:
	super(corpo)
	if corpo is Gabriel or corpo is Robo:
		if not _ocupantes.has(corpo):
			_ocupantes.append(corpo)
		_espera.stop()


func _ao_sair(corpo: Node2D) -> void:
	super(corpo)
	_ocupantes.erase(corpo)
	if aberta and _ocupantes.is_empty() and _espera.is_inside_tree():
		_espera.start(segundos_aberta)


func _terminar_fechamento() -> void:
	_revelando = false
	_atualizar_conteudo()


func _animar(abrindo: bool) -> void:
	if _animacao:
		_animacao.kill()
	_animacao = create_tween().set_parallel()
	var alvo := _escala_recolhida() if abrindo else Vector2.ONE
	for folha in _folhas:
		_animacao.tween_property(folha, "scale", alvo, segundos_animando) \
				.set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	for lampada in _lampadas:
		lampada.color = COR_ABERTA if abrindo else COR_FECHADA


func _escala_recolhida() -> Vector2:
	if _e_vertical():
		return Vector2(1.0, ESCALA_RECOLHIDA)
	return Vector2(ESCALA_RECOLHIDA, 1.0)


func _e_vertical() -> bool:
	return tamanho.y > tamanho.x


func _tocar(altura_do_som: float) -> void:
	_som.pitch_scale = altura_do_som
	_som.play()


func _pegada_global() -> Rect2:
	return Rect2(global_position + Vector2(-tamanho.x / 2.0, -tamanho.y), tamanho)


func _perto_da_pegada(ponto: Vector2, margem: float) -> bool:
	return _pegada_global().grow(margem).has_point(ponto)


func _jogador_na_sala() -> bool:
	var gabriel := get_tree().get_first_node_in_group("jogador") as Node2D
	return gabriel != null and area_da_sala.has_point(gabriel.global_position)


func _atualizar_conteudo() -> void:
	var mostrar := _revelando or _jogador_na_sala()
	if mostrar == _mostrando:
		return
	_mostrando = mostrar
	for no in conteudo:
		if is_instance_valid(no):
			no.visible = mostrar
	if mostrar:
		_devolver_robos()
	else:
		_esconder_robos()


func _esconder_robos() -> void:
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Node2D
		if robo and area_da_sala.has_point(robo.global_position):
			robo.visible = false
			_escondidos.append(robo)


func _devolver_robos() -> void:
	for robo in _escondidos:
		if is_instance_valid(robo):
			robo.visible = true
	_escondidos.clear()


func _preparar_formas() -> void:
	var pegada := Rect2(Vector2(-tamanho.x / 2.0, -tamanho.y), tamanho)
	var bloqueio := RectangleShape2D.new()
	bloqueio.size = tamanho
	_forma_bloqueio.shape = bloqueio
	_forma_bloqueio.position = pegada.get_center()
	var zona := RectangleShape2D.new()
	zona.size = tamanho + Vector2.ONE * MARGEM_ALCANCE * 2.0
	_alcance.shape = zona
	_alcance.position = pegada.get_center()
	var poligono := OccluderPolygon2D.new()
	poligono.polygon = _cantos(pegada)
	_oclusor.occluder = poligono


func _montar_folhas() -> void:
	for lado in 2:
		var folha := Node2D.new()
		folha.name = "Folha_%d" % lado
		add_child(folha)
		_folhas.append(folha)
		if _e_vertical():
			_desenhar_folha_vertical(folha, lado)
		else:
			_desenhar_folha_horizontal(folha, lado)


func _desenhar_folha_horizontal(folha: Node2D, lado: int) -> void:
	var largura := tamanho.x / 2.0
	var x_inicial := 0.0 if lado == 0 else -largura
	var x_do_risco := largura - 1.0 if lado == 0 else -largura
	var x_da_lampada := largura - TAMANHO_LAMPADA.x - 2.0 if lado == 0 else -largura + 2.0
	folha.position = Vector2(-tamanho.x / 2.0 if lado == 0 else tamanho.x / 2.0, 0.0)
	var y_do_topo := -tamanho.y - ALTURA_PAREDE
	_retangulo(folha, Rect2(x_inicial, y_do_topo, largura, tamanho.y), COR_TOPO)
	_retangulo(folha, Rect2(x_do_risco, y_do_topo, 1.0, tamanho.y), COR_RISCO)
	if frente_visivel:
		_retangulo(folha, Rect2(x_inicial, -ALTURA_PAREDE, largura, ALTURA_PAREDE), COR_FRENTE)
		_retangulo(folha, Rect2(x_inicial, -ALTURA_PAREDE + 12.0, largura, 1.0), COR_RISCO)
		_retangulo(folha, Rect2(x_inicial, -ALTURA_PAREDE + 26.0, largura, 1.0), COR_RISCO)
		_retangulo(folha, Rect2(x_do_risco, -ALTURA_PAREDE, 1.0, ALTURA_PAREDE), COR_RISCO)
		_acender_lampada(folha, Vector2(x_da_lampada, -ALTURA_PAREDE + 5.0))
	else:
		_acender_lampada(folha, Vector2(x_da_lampada, y_do_topo + 4.0))


func _desenhar_folha_vertical(folha: Node2D, lado: int) -> void:
	var altura := tamanho.y / 2.0
	var x_inicial := -tamanho.x / 2.0
	var y_inicial := 0.0 if lado == 0 else -altura
	var y_do_risco := altura - 1.0 if lado == 0 else -altura
	var y_da_lampada := altura - TAMANHO_LAMPADA.y - 2.0 if lado == 0 else -altura + 2.0
	folha.position = Vector2(0.0, -tamanho.y - ALTURA_PAREDE if lado == 0 else -ALTURA_PAREDE)
	_retangulo(folha, Rect2(x_inicial, y_inicial, tamanho.x, altura), COR_TOPO)
	_retangulo(folha, Rect2(x_inicial, y_do_risco, tamanho.x, 1.0), COR_RISCO)
	_acender_lampada(folha, Vector2(-TAMANHO_LAMPADA.x / 2.0, y_da_lampada))
	if lado == 1 and frente_visivel:
		_retangulo(folha, Rect2(x_inicial, 0.0, tamanho.x, ALTURA_PAREDE), COR_FRENTE)
		_retangulo(folha, Rect2(x_inicial, 12.0, tamanho.x, 1.0), COR_RISCO)
		_retangulo(folha, Rect2(x_inicial, 26.0, tamanho.x, 1.0), COR_RISCO)


func _acender_lampada(pai: Node2D, posicao: Vector2) -> void:
	var lampada := _retangulo(pai, Rect2(posicao, TAMANHO_LAMPADA), COR_FECHADA)
	lampada.material = _material_sem_luz
	_lampadas.append(lampada)


func _retangulo(pai: Node2D, area: Rect2, cor: Color) -> Polygon2D:
	var forma := Polygon2D.new()
	forma.polygon = _cantos(area)
	forma.color = cor
	forma.light_mask = LUZ_SO_NAS_PAREDES
	pai.add_child(forma)
	return forma


func _cantos(area: Rect2) -> PackedVector2Array:
	return PackedVector2Array([area.position, Vector2(area.end.x, area.position.y),
			area.end, Vector2(area.position.x, area.end.y)])
