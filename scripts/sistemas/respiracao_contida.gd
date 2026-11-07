class_name RespiracaoContida
extends Node2D

signal falhou

const SOM_ENGASGO := preload("res://assets/audio/efeitos/objetos/tosse.wav")
const SOM_OFEGANTE := preload("res://assets/audio/efeitos/gabriel/gabriel_ofegante.wav")
const AVISO := "Ele está do lado de fora. Segure E para prender o ar, solte para respirar: fique no verde."
const LARGURA_BARRA := 48.0
const ALTURA_BARRA := -62.0
const COR_FUNDO := Color(0.16, 0.17, 0.21)
const COR_ZONA := Color(0.35, 1.0, 0.55)
const COR_CURSOR := Color(1.0, 1.0, 0.9)
const COR_RUIDO := Color(1.0, 0.3, 0.25)

static var _ja_ensinou := false

@export var largura_faixa_calmo: float = 0.28
@export var largura_faixa_ansioso: float = 0.18
@export var fator_faixa_cansado: float = 0.8
@export var subida_calmo: float = 0.18
@export var subida_ansioso: float = 0.28
@export var descida: float = 0.38
@export var tremor: float = 0.2
@export var ruido_fora_da_faixa: float = 0.65
@export var ruido_recuperado: float = 0.18

var nivel := 0.5
var ruido := 0.0

var _gabriel: Gabriel
var _largura := 0.28
var _tempo := 0.0
var _som_ofegante: AudioStreamPlayer


func acompanhar(gabriel: Gabriel) -> void:
	_gabriel = gabriel


func _ready() -> void:
	z_index = 20
	var sem_luz := CanvasItemMaterial.new()
	sem_luz.light_mode = CanvasItemMaterial.LIGHT_MODE_UNSHADED
	material = sem_luz
	_som_ofegante = AudioStreamPlayer.new()
	_som_ofegante.stream = SOM_OFEGANTE
	_som_ofegante.bus = &"Efeitos"
	_som_ofegante.volume_db = -6.0
	add_child(_som_ofegante)
	if not _ja_ensinou:
		_ja_ensinou = true
		Inventario.aviso.emit(AVISO)


func _input(evento: InputEvent) -> void:
	if evento.is_action("interagir"):
		get_viewport().set_input_as_handled()


func _physics_process(delta: float) -> void:
	if not is_instance_valid(_gabriel):
		queue_free()
		return
	global_position = _gabriel.global_position
	_tempo += delta
	var ansiedade := _gabriel.ansiedade.valor if _gabriel.ansiedade else 0.0
	_largura = lerpf(largura_faixa_calmo, largura_faixa_ansioso, ansiedade)
	if _gabriel.fadiga and _gabriel.fadiga.esta_cansado():
		_largura *= fator_faixa_cansado
	var passo := -descida if Input.is_action_pressed("interagir") else lerpf(subida_calmo, subida_ansioso, ansiedade)
	nivel = clampf(nivel + (passo + tremor * _oscilacao()) * delta, 0.0, 1.0)
	var fora := absf(nivel - 0.5) > _largura / 2.0
	ruido = clampf(ruido + (ruido_fora_da_faixa if fora else -ruido_recuperado) * delta, 0.0, 1.0)
	_ofegar(nivel > 0.5 + _largura / 2.0)
	if ruido >= 1.0:
		_engasgar()
		return
	queue_redraw()


func _oscilacao() -> float:
	return sin(_tempo * 2.1) * sin(_tempo * 0.63 + 1.0)


func _ofegar(alto: bool) -> void:
	if alto and not _som_ofegante.playing:
		_som_ofegante.play()


func _engasgar() -> void:
	var som := AudioStreamPlayer.new()
	som.stream = SOM_ENGASGO
	som.bus = &"Efeitos"
	som.finished.connect(som.queue_free)
	get_tree().current_scene.add_child(som)
	som.play()
	falhou.emit()
	queue_free()


func _draw() -> void:
	var inicio := Vector2(-LARGURA_BARRA / 2.0, ALTURA_BARRA)
	draw_rect(Rect2(inicio - Vector2.ONE, Vector2(LARGURA_BARRA + 2, 6)), COR_FUNDO)
	var zona_x := (0.5 - _largura / 2.0) * LARGURA_BARRA
	draw_rect(Rect2(inicio + Vector2(zona_x, 0), Vector2(_largura * LARGURA_BARRA, 4)), COR_ZONA)
	draw_rect(Rect2(inicio + Vector2(nivel * LARGURA_BARRA - 0.5, -1), Vector2(1, 6)), COR_CURSOR)
	draw_rect(Rect2(inicio + Vector2(-1, 6), Vector2(LARGURA_BARRA + 2, 3)), COR_FUNDO)
	draw_rect(Rect2(inicio + Vector2(0, 7), Vector2(ruido * LARGURA_BARRA, 1)), COR_RUIDO)
