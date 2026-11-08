class_name EsconderijoCabine
extends Interagivel

const SOM_ENGASGO := preload("res://assets/audio/efeitos/objetos/tosse.wav")
const AVISO_DENTRO := "Na cabine. E: sair."
const AVISO_RESPIRAR := "Prenda a respiração: E na faixa verde."
const AVISO_ENGASGO := "Você engasgou. Ele ouviu."
const LARGURA_BARRA := 44.0
const ALTURA_BARRA := -78.0
const COR_FUNDO := Color(0.03, 0.04, 0.06)
const COR_ZONA := Color(0.35, 1.0, 0.55)
const COR_CURSOR := Color(1.0, 1.0, 0.9)
const COR_FALHA := Color(1.0, 0.3, 0.25)

static var _ja_ensinou := false

@export var raio_perigo: float = 110.0
@export var pulsos_para_acalmar: int = 3
@export var falhas_permitidas: int = 2
@export var largura_zona: float = 0.34
@export var fator_zona_cansado: float = 0.75
@export var velocidade: float = 0.9
@export var segundos_de_folga: float = 2.5

var _gabriel_dentro: Gabriel
var _camada := 0
var _no_microgame := false
var _fase := 0.0
var _zona := 0.5
var _largura := 0.3
var _acertos := 0
var _falhas := 0
var _voltas_sem_apertar := 0.0
var _folga := 0.0
var _sorteio := RandomNumberGenerator.new()


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	z_index = 20
	var sem_luz := CanvasItemMaterial.new()
	sem_luz.light_mode = CanvasItemMaterial.LIGHT_MODE_UNSHADED
	material = sem_luz
	_sorteio.randomize()


func pode_interagir() -> bool:
	return _gabriel_dentro == null


func dentro() -> bool:
	return _gabriel_dentro != null


func interagir() -> void:
	var gabriel := get_tree().get_first_node_in_group("jogador") as Gabriel
	if gabriel == null:
		return
	_gabriel_dentro = gabriel
	gabriel.andar_sozinho(Vector2.ZERO)
	gabriel.global_position = global_position
	gabriel.modulate.a = 0.0
	gabriel.esconder(true)
	_camada = gabriel.collision_layer
	gabriel.collision_layer = 0
	_folga = 0.0
	Inventario.aviso.emit(AVISO_DENTRO)


func _unhandled_input(evento: InputEvent) -> void:
	if _gabriel_dentro == null or not evento.is_action_pressed("interagir"):
		return
	get_viewport().set_input_as_handled()
	if _no_microgame:
		_tentar_pulso()
	else:
		_sair()


func _physics_process(delta: float) -> void:
	if Engine.is_editor_hint() or _gabriel_dentro == null:
		return
	_folga = maxf(_folga - delta, 0.0)
	var perigo := _robo_perto() != null
	if perigo and not _no_microgame and _folga <= 0.0:
		_comecar_microgame()
	elif not perigo and _no_microgame:
		_terminar_microgame()
	if _no_microgame:
		_avancar_microgame(delta)


func _robo_perto() -> Robo:
	var melhor: Robo = null
	var menor := raio_perigo
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo == null or robo.estado == Robo.Estado.ATORDOADO:
			continue
		var distancia := global_position.distance_to(robo.global_position)
		if distancia < menor:
			menor = distancia
			melhor = robo
	return melhor


func _comecar_microgame() -> void:
	_no_microgame = true
	_acertos = 0
	_falhas = 0
	_voltas_sem_apertar = 0.0
	_fase = 0.0
	_sortear_zona()
	if not _ja_ensinou:
		_ja_ensinou = true
		Inventario.aviso.emit(AVISO_RESPIRAR)
	queue_redraw()


func _sortear_zona() -> void:
	_largura = largura_zona
	if _gabriel_dentro.fadiga and _gabriel_dentro.fadiga.esta_cansado():
		_largura *= fator_zona_cansado
	_zona = _sorteio.randf_range(_largura / 2.0, 1.0 - _largura / 2.0)


func _avancar_microgame(delta: float) -> void:
	_fase += delta * velocidade
	_voltas_sem_apertar += delta * velocidade
	if _voltas_sem_apertar >= 2.0:
		_voltas_sem_apertar = 0.0
		_falhar()
	queue_redraw()


func _cursor() -> float:
	return pingpong(_fase, 1.0)


func _tentar_pulso() -> void:
	_voltas_sem_apertar = 0.0
	if absf(_cursor() - _zona) > _largura / 2.0:
		_falhar()
		return
	_acertos += 1
	if _acertos >= pulsos_para_acalmar:
		_folga = segundos_de_folga
		_terminar_microgame()
	else:
		_sortear_zona()


func _falhar() -> void:
	_falhas += 1
	if _falhas >= falhas_permitidas:
		_engasgar()


func _engasgar() -> void:
	var robo := _robo_perto()
	var som := AudioStreamPlayer.new()
	som.stream = SOM_ENGASGO
	som.bus = &"Efeitos"
	som.finished.connect(som.queue_free)
	get_tree().current_scene.add_child(som)
	som.play()
	Inventario.aviso.emit(AVISO_ENGASGO)
	_sair()
	if robo:
		robo.denunciar()


func _terminar_microgame() -> void:
	_no_microgame = false
	queue_redraw()


func _sair() -> void:
	_terminar_microgame()
	var gabriel := _gabriel_dentro
	_gabriel_dentro = null
	gabriel.modulate.a = 1.0
	gabriel.esconder(false)
	gabriel.collision_layer = _camada
	gabriel.global_position = global_position + Vector2(0, 14)
	gabriel.devolver_controle()


func _draw() -> void:
	if not _no_microgame:
		return
	var inicio := Vector2(-LARGURA_BARRA / 2.0, ALTURA_BARRA)
	draw_rect(Rect2(inicio - Vector2.ONE, Vector2(LARGURA_BARRA + 2, 6)), COR_FUNDO)
	var zona_x := (_zona - _largura / 2.0) * LARGURA_BARRA
	draw_rect(Rect2(inicio + Vector2(zona_x, 0), Vector2(_largura * LARGURA_BARRA, 4)), COR_ZONA)
	draw_rect(Rect2(inicio + Vector2(_cursor() * LARGURA_BARRA - 0.5, -1), Vector2(1, 6)), COR_CURSOR)
	for i in _falhas:
		draw_rect(Rect2(inicio + Vector2(i * 3, 6), Vector2(2, 2)), COR_FALHA)
	for i in _acertos:
		draw_rect(Rect2(inicio + Vector2(LARGURA_BARRA - 2 - i * 3, 6), Vector2(2, 2)), COR_ZONA)
