extends MecanismoDoTempo

const ANGULO_TRAVA := -PI / 2.0
const RAIOS: Array[float] = [40.0, 30.0, 20.0]

@export var velocidades: Array[float] = [1.7, -2.4, 3.2]
@export var largura_fenda: float = 0.55
@export var folga: float = 0.7

var _angulos: Array[float] = [0.0, 0.0, 0.0]


func _preparar() -> void:
	acertos_para_alinhar = RAIOS.size()
	for i in RAIOS.size():
		_angulos[i] = randf() * TAU


func _avancar(delta: float) -> void:
	for i in range(_acertos, RAIOS.size()):
		_angulos[i] = wrapf(_angulos[i] + velocidades[i] * delta, 0.0, TAU)


func _acertou() -> bool:
	return _diferenca_angular(_angulos[_acertos], ANGULO_TRAVA) <= largura_fenda * folga / 2.0


func _ao_acertar() -> void:
	_angulos[_acertos - 1] = ANGULO_TRAVA


func _ao_errar() -> void:
	_preparar()


func _desenhar(centro: Vector2) -> void:
	desenho.draw_circle(centro, RAIOS[0] + 5.0, Color("141210"))
	for i in RAIOS.size():
		var travado := i < _acertos
		var atual := i == _acertos
		var cor := COR_ALVO if travado else (COR_TEXTO if atual else COR_APAGADA)
		var inicio := _angulos[i] + largura_fenda / 2.0
		desenho.draw_arc(centro, RAIOS[i], inicio, inicio + TAU - largura_fenda, 48, cor, 4.0)
	var trava := centro + Vector2.from_angle(ANGULO_TRAVA) * (RAIOS[0] + 8.0)
	desenho.draw_line(trava, centro + Vector2.from_angle(ANGULO_TRAVA) * (RAIOS[RAIOS.size() - 1] - 6.0), COR_ERRO.darkened(0.3), 1.0)
	desenho.draw_rect(Rect2(trava - Vector2(3, 3), Vector2(6, 4)), COR_ERRO)
	desenho.draw_circle(centro, 6.0, COR_METAL)
