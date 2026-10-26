extends MecanismoDoTempo

const RAIO_MOSTRADOR := 40.0
const BATIDAS_POR_VOLTA := 12

@export var periodo_inicial: float = 0.8
@export var encurtamento_por_acerto: float = 0.93
@export var tolerancia: float = 0.12

var _periodo := 0.0
var _inicio := 0.0
var _batida_anterior := -1
var _batida_acertada := -10

@onready var som_batida: AudioStreamPlayer = $Tela/SomBatida


func _preparar() -> void:
	_periodo = periodo_inicial
	_inicio = _tempo
	_batida_anterior = -1
	_batida_acertada = -10


func _avancar(_delta: float) -> void:
	var batida := _batida_atual()
	if batida == _batida_anterior:
		return
	_batida_anterior = batida
	som_batida.play()
	if _acertos > 0 and batida > _batida_acertada + 1:
		_acertos = 0
		_mostrar_visor()


func _acertou() -> bool:
	var proxima := roundi(_fase())
	var distancia := absf(_fase() - proxima) * _periodo
	if distancia > tolerancia or proxima == _batida_acertada:
		return false
	_batida_acertada = proxima
	return true


func _ao_acertar() -> void:
	var batida := _fase()
	_periodo *= encurtamento_por_acerto
	_inicio = _tempo - batida * _periodo
	_batida_acertada = roundi(batida)


func _ao_errar() -> void:
	_preparar()


func _fase() -> float:
	return (_tempo - _inicio) / _periodo


func _batida_atual() -> int:
	return floori(_fase())


func _desenhar(centro: Vector2) -> void:
	var pulso := clampf(1.0 - (_fase() - _batida_atual()) * 3.0, 0.0, 1.0)
	desenho.draw_circle(centro, RAIO_MOSTRADOR, Color("e8dcc0"))
	_desenhar_anel(centro, RAIO_MOSTRADOR, COR_APAGADA.lerp(COR_ALVO, pulso), 3.0)
	for i in BATIDAS_POR_VOLTA:
		var direcao := Vector2.from_angle(TAU * i / BATIDAS_POR_VOLTA - PI / 2.0)
		var tamanho := 6.0 if i % 3 == 0 else 3.0
		desenho.draw_line(centro + direcao * (RAIO_MOSTRADOR - tamanho), centro + direcao * (RAIO_MOSTRADOR - 1.0), Color("2a2622"), 1.0)
	desenho.draw_line(centro, centro + Vector2.from_angle(-PI / 2.0 + TAU * 10.0 / 12.0) * 18.0, Color("2a2622"), 3.0)
	desenho.draw_line(centro, centro + Vector2.from_angle(-PI / 2.0 + TAU * 2.0 / 12.0) * 28.0, Color("2a2622"), 2.0)
	var segundos := Vector2.from_angle(TAU * posmod(_batida_atual(), BATIDAS_POR_VOLTA) / BATIDAS_POR_VOLTA - PI / 2.0)
	desenho.draw_line(centro, centro + segundos * 34.0, Color("c0392b"), 1.0)
	desenho.draw_circle(centro, 2.0, Color("c0392b"))
