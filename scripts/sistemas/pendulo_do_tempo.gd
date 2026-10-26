extends MecanismoDoTempo

const COMPRIMENTO := 72.0
const RAIO_PESO := 6.0

@export var amplitude: float = 1.0
@export var frequencia_inicial: float = 2.2
@export var meia_janela_inicial: float = 0.14
@export var aceleracao_por_acerto: float = 1.2
@export var encolhimento_por_acerto: float = 0.8

var _frequencia := 0.0
var _meia_janela := 0.0
var _alvo := 0.0
var _fase := 0.0


func _preparar() -> void:
	_frequencia = frequencia_inicial
	_meia_janela = meia_janela_inicial
	_fase = 0.0
	_sortear_alvo()


func _avancar(delta: float) -> void:
	_fase += _frequencia * delta


func _acertou() -> bool:
	return absf(_angulo() - _alvo) <= _meia_janela


func _ao_acertar() -> void:
	_frequencia *= aceleracao_por_acerto
	_meia_janela *= encolhimento_por_acerto
	_sortear_alvo()


func _ao_errar() -> void:
	_preparar()


func _sortear_alvo() -> void:
	_alvo = randf_range(-0.7, 0.7) * amplitude


func _angulo() -> float:
	return amplitude * sin(_fase)


func _desenhar(centro: Vector2) -> void:
	var piva := Vector2(centro.x, 4.0)
	var baixo := PI / 2.0
	desenho.draw_arc(piva, COMPRIMENTO, baixo - amplitude, baixo + amplitude, 32, COR_APAGADA, 3.0)
	desenho.draw_arc(piva, COMPRIMENTO, baixo - _alvo - _meia_janela, baixo - _alvo + _meia_janela, 8, COR_ALVO, 5.0)
	var peso := piva + Vector2.from_angle(baixo - _angulo()) * COMPRIMENTO
	desenho.draw_line(piva, peso, COR_METAL, 1.0)
	desenho.draw_circle(peso, RAIO_PESO, Color("c9a227"))
	desenho.draw_circle(peso, RAIO_PESO - 2.0, Color("e8c547"))
	desenho.draw_circle(piva, 2.0, COR_METAL)
