extends MecanismoDoTempo

const ANGULO_AGULHA := -PI / 2.0
const RAIO_DISCO := 40.0
const RAIO_FAIXA := 31.0

@export var velocidade_inicial: float = 2.4
@export var largura_inicial: float = 0.9
@export var aceleracao_por_acerto: float = 1.35
@export var encolhimento_por_acerto: float = 0.75

var _angulo := 0.0
var _velocidade := 0.0
var _largura := 0.0
var _deslocamento := 0.0


func _preparar() -> void:
	_velocidade = velocidade_inicial
	_largura = largura_inicial
	_sortear_faixa()


func _avancar(delta: float) -> void:
	_angulo = wrapf(_angulo + _velocidade * delta, 0.0, TAU)


func _acertou() -> bool:
	return _diferenca_angular(_centro_da_faixa(), ANGULO_AGULHA) <= _largura / 2.0


func _ao_acertar() -> void:
	_velocidade *= aceleracao_por_acerto
	_largura *= encolhimento_por_acerto
	_sortear_faixa()


func _ao_errar() -> void:
	_preparar()


func _sortear_faixa() -> void:
	_deslocamento = randf() * TAU


func _centro_da_faixa() -> float:
	return _angulo + _deslocamento


func _desenhar(centro: Vector2) -> void:
	desenho.draw_circle(centro, RAIO_DISCO, Color("141210"))
	for raio in range(14, int(RAIO_DISCO), 4):
		_desenhar_anel(centro, raio, Color("2a2622"))
	_desenhar_faixa(centro, RAIO_FAIXA, _centro_da_faixa(), _largura, COR_ALVO, 5.0)
	desenho.draw_circle(centro, 10.0, Color("c0392b"))
	desenho.draw_line(centro, centro + Vector2.from_angle(_angulo) * 10.0, COR_TEXTO, 1.0)
	desenho.draw_circle(centro, 1.5, COR_METAL)
	var ponta := centro + Vector2.from_angle(ANGULO_AGULHA) * RAIO_FAIXA
	var base := centro + Vector2(RAIO_DISCO + 12.0, -RAIO_DISCO + 2.0)
	desenho.draw_line(base, ponta + Vector2(4, -4), COR_METAL, 2.0)
	desenho.draw_line(ponta + Vector2(4, -4), ponta, COR_METAL, 2.0)
	desenho.draw_circle(base, 4.0, COR_APAGADA)
