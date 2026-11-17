class_name CenaFinal
extends Node

const DIALOGO_CHEGADA := "res://dados/dialogos/final_chegada.json"
const DIALOGO_AMEACA := "res://dados/dialogos/final_ameaca.json"
const POSICOES_DOS_SIDERALIS := [Vector2(-100, -12), Vector2(100, -12), Vector2(-140, -50), Vector2(140, -50)]
const ZOOM_DO_PLANO := Vector2(0.9, 0.9)
const SUBIDA_PELA_CAIXA_DE_DIALOGO := Vector2(0, 70)
const SEGUNDOS_DO_PLANO := 1.0
const SEGUNDOS_ENTRE_APARICOES := 0.3
const SEGUNDOS_APARECENDO := 0.6
const SEGUNDOS_DO_CLARAO := 0.8
const SEGUNDOS_ANTES_DA_FALA := 1.2
const SEGUNDOS_ANTES_DA_MORTE := 0.4
const SEGUNDOS_DA_QUEDA := 0.9
const SEGUNDOS_DEPOIS_DA_QUEDA := 0.8
const SEGUNDOS_DA_MAQUINA := 2.4
const SEGUNDOS_DEPOIS_DA_MAQUINA := 0.6
const COR_DO_CLARAO := Color(0.7, 1.0, 1.0)
const COR_DA_MORTE := Color(1.0, 0.25, 0.2)
const COR_DO_CORPO := Color(0.45, 0.45, 0.55)
const GRAUS_DA_QUEDA := 88.0

@export var cena_sideralis: PackedScene

var _carlos: CarlosChefe
var _gabriel: Gabriel
var _camera: Camera2D
var _clarao: ColorRect
var _comecou := false

@onready var nucleo: Node2D = get_parent()
@onready var saida: SaidaFase = get_node("../SaidaFase")


func comecar(carlos: CarlosChefe) -> void:
	if _comecou:
		return
	_comecou = true
	_carlos = carlos
	_gabriel = get_tree().get_first_node_in_group("jogador") as Gabriel
	_camera = _gabriel.get_node_or_null("Camera2D") as Camera2D
	_congelar_a_sala()
	_criar_clarao()
	Dialogos.terminou.connect(_ao_terminar_dialogo)
	await _abrir_o_plano()
	await _sideralis_chegam()
	Dialogos.iniciar(DIALOGO_CHEGADA)


func _congelar_a_sala() -> void:
	_gabriel.andar_sozinho(Vector2.ZERO)
	for robo in get_tree().get_nodes_in_group("robos"):
		robo.process_mode = Node.PROCESS_MODE_DISABLED
	if _carlos:
		_carlos.atordoar(0.0)
		_carlos.set_process(false)
		_carlos.queue_redraw()


func _criar_clarao() -> void:
	var camada := CanvasLayer.new()
	camada.layer = 10
	_clarao = ColorRect.new()
	_clarao.set_anchors_preset(Control.PRESET_FULL_RECT)
	_clarao.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_clarao.color = Color(COR_DO_CLARAO, 0.0)
	camada.add_child(_clarao)
	add_child(camada)


func _abrir_o_plano() -> void:
	if _camera == null or _carlos == null:
		return
	var ponto := (_gabriel.global_position + _carlos.global_position) / 2.0 - SUBIDA_PELA_CAIXA_DE_DIALOGO
	var plano := create_tween().set_parallel().set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	plano.set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)
	plano.tween_property(_camera, "offset", ponto - _camera.global_position, SEGUNDOS_DO_PLANO)
	plano.tween_property(_camera, "zoom", ZOOM_DO_PLANO, SEGUNDOS_DO_PLANO)
	await plano.finished


func _sideralis_chegam() -> void:
	_piscar(COR_DO_CLARAO, 0.8, SEGUNDOS_DO_CLARAO)
	_tremer_camera(1.2, 3.0)
	for posicao in POSICOES_DOS_SIDERALIS:
		await get_tree().create_timer(SEGUNDOS_ENTRE_APARICOES).timeout
		_aparecer(posicao)
	await get_tree().create_timer(SEGUNDOS_ANTES_DA_FALA).timeout


func _aparecer(posicao: Vector2) -> void:
	var figura := cena_sideralis.instantiate() as Node2D
	nucleo.get_parent().add_child(figura)
	figura.global_position = nucleo.global_position + posicao
	figura.modulate = Color(3.0, 3.0, 3.0, 0.0)
	var surgir := create_tween().set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)
	surgir.tween_property(figura, "modulate", Color.WHITE, SEGUNDOS_APARECENDO)


func _ao_terminar_dialogo(caminho: String) -> void:
	match caminho:
		DIALOGO_CHEGADA:
			_matar_o_carlos()
		DIALOGO_AMEACA:
			saida.comecar_saida()


func _matar_o_carlos() -> void:
	await get_tree().create_timer(SEGUNDOS_ANTES_DA_MORTE).timeout
	_piscar(COR_DA_MORTE, 0.7, 0.5)
	_tremer_camera(0.5, 3.0)
	var corpo := _carlos.get_node("Carlos") as Node2D
	var queda := create_tween().set_parallel().set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
	queda.tween_property(corpo, "rotation", deg_to_rad(GRAUS_DA_QUEDA), SEGUNDOS_DA_QUEDA)
	queda.tween_property(corpo, "modulate", COR_DO_CORPO, SEGUNDOS_DA_QUEDA)
	await queda.finished
	await get_tree().create_timer(SEGUNDOS_DEPOIS_DA_QUEDA).timeout
	await _terminar_a_maquina()
	Dialogos.iniciar(DIALOGO_AMEACA)


func _terminar_a_maquina() -> void:
	_tremer_camera(SEGUNDOS_DA_MAQUINA, 4.0)
	var clarao := _piscar(COR_DO_CLARAO, 1.0, SEGUNDOS_DA_MAQUINA)
	await clarao.finished
	await get_tree().create_timer(SEGUNDOS_DEPOIS_DA_MAQUINA).timeout


func _piscar(cor: Color, pico: float, segundos: float) -> Tween:
	_clarao.color = Color(cor, 0.0)
	var piscar := create_tween().set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)
	piscar.tween_property(_clarao, "color:a", pico, segundos * 0.25)
	piscar.tween_property(_clarao, "color:a", 0.0, segundos * 0.75)
	return piscar


func _tremer_camera(segundos: float, forca: float) -> void:
	if _camera == null:
		return
	var base := _camera.offset
	var tremor := create_tween().set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)
	tremor.tween_method(func(resta: float) -> void:
		_camera.offset = base + Vector2(randf_range(-1, 1), randf_range(-1, 1)) * forca * resta, 1.0, 0.0, segundos)
	tremor.tween_callback(func() -> void: _camera.offset = base)
