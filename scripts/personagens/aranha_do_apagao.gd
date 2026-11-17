class_name AranhaDoApagao
extends Node2D

signal chegou

const ESCALA_BASE := 0.5
const ESCALA_DE_LONGE := 0.45
const DISTANCIA_DO_CONTATO := 18.0
const SEGUNDOS_PARA_APARECER := 0.7
const SEGUNDOS_PARA_SUMIR := 0.5
const PASSOS_POR_SEGUNDO := 2.4
const ALTURA_DO_PASSO := 3.0
const BALANCO := 0.03
const ESCALA_DO_BOTE := 1.22

var _alvo: Node2D
var _velocidade := 1.0
var _distancia_inicial := 1.0
var _andando := false
var _tempo := 0.0
var _passos_dados := 0

@onready var gingado: Node2D = $Gingado
@onready var luz: PointLight2D = $Gingado/LuzDoOlhar
@onready var som_passos: AudioStreamPlayer2D = $Passos
@onready var som_alerta: AudioStreamPlayer2D = $Alerta


func iniciar(alvo: Node2D, segundos: float) -> void:
	_alvo = alvo
	_distancia_inicial = maxf(global_position.distance_to(alvo.global_position), DISTANCIA_DO_CONTATO + 1.0)
	_velocidade = (_distancia_inicial - DISTANCIA_DO_CONTATO) / maxf(segundos, 0.1)
	_atualizar_escala()
	_andando = true
	som_alerta.play()
	modulate.a = 0.0
	var aparecer := create_tween()
	aparecer.tween_property(self, "modulate:a", 0.25, 0.08)
	aparecer.tween_property(self, "modulate:a", 0.0, 0.08)
	aparecer.tween_property(self, "modulate:a", 1.0, SEGUNDOS_PARA_APARECER)


func segundos_restantes() -> float:
	if _alvo == null:
		return 0.0
	var falta := maxf(global_position.distance_to(_alvo.global_position) - DISTANCIA_DO_CONTATO, 0.0)
	return falta / maxf(_velocidade, 0.001)


func bote() -> void:
	_andando = false
	var tween := create_tween()
	tween.tween_property(self, "scale", scale * ESCALA_DO_BOTE, 0.1)
	tween.tween_property(self, "scale", scale, 0.2)


func sumir() -> void:
	_andando = false
	var tween := create_tween()
	for i in 3:
		tween.tween_property(self, "modulate:a", 0.2, 0.05)
		tween.tween_property(self, "modulate:a", 1.0, 0.05)
	tween.tween_property(self, "modulate:a", 0.0, SEGUNDOS_PARA_SUMIR)
	tween.tween_callback(queue_free)


func _process(delta: float) -> void:
	if not _andando:
		return
	_tempo += delta
	var para := _alvo.global_position - global_position
	var distancia := para.length()
	if distancia <= DISTANCIA_DO_CONTATO:
		_andando = false
		chegou.emit()
		return
	global_position += para / distancia * minf(_velocidade * delta, distancia)
	_atualizar_escala()
	_balancar()


func _atualizar_escala() -> void:
	var falta := maxf(global_position.distance_to(_alvo.global_position) - DISTANCIA_DO_CONTATO, 0.0)
	var perto := 1.0 - clampf(falta / maxf(_distancia_inicial - DISTANCIA_DO_CONTATO, 1.0), 0.0, 1.0)
	scale = Vector2.ONE * ESCALA_BASE * lerpf(ESCALA_DE_LONGE, 1.0, perto)


func _balancar() -> void:
	var fase := _tempo * PASSOS_POR_SEGUNDO * PI
	gingado.position.y = -absf(sin(fase)) * ALTURA_DO_PASSO
	gingado.rotation = sin(fase) * BALANCO
	var passos := int(_tempo * PASSOS_POR_SEGUNDO)
	if passos > _passos_dados:
		_passos_dados = passos
		som_passos.pitch_scale = randf_range(0.8, 0.95)
		som_passos.play()
