extends MinigameHack

const ACERTOS_NECESSARIOS := [3, 4, 5]
const LARGURA_ZONA := [0.24, 0.15, 0.09]
const VELOCIDADE := [0.9, 1.3, 1.8]
const VIDAS_POR_NIVEL := [3, 2, 1]
const ACELERACAO_POR_ACERTO := 1.12
const LARGURA_BARRA := 200.0
const ALTURA_BARRA := 14.0
const MARGEM_ZONA := 0.05
const SEGUNDOS_FEEDBACK := 0.25

var _acertos := 0
var _fase_cursor := 0.0
var _velocidade := 1.0
var _zona_inicio := 0.0
var _vidas_maximas := 1
var _tempo_feedback := 0.0
var _feedback_erro := false


func preparar() -> void:
	titulo = "SINCRONIA"
	instrucao = "Pare o cursor na zona verde com E"
	_vidas_maximas = _por_nivel(VIDAS_POR_NIVEL)
	vidas = _vidas_maximas
	_acertos = 0
	_fase_cursor = 0.0
	_velocidade = _por_nivel(VELOCIDADE)
	_sortear_zona()


func _sortear_zona() -> void:
	var largura: float = _por_nivel(LARGURA_ZONA)
	_zona_inicio = randf_range(MARGEM_ZONA, 1.0 - largura - MARGEM_ZONA)


func _cursor() -> float:
	return pingpong(_fase_cursor, 1.0)


func _process(delta: float) -> void:
	if encerrado:
		return
	_fase_cursor += _velocidade * delta
	_tempo_feedback = maxf(_tempo_feedback - delta, 0.0)
	queue_redraw()


func tratar_entrada(evento: InputEvent) -> void:
	if encerrado:
		return
	if evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		_tentar()


func _tentar() -> void:
	var largura: float = _por_nivel(LARGURA_ZONA)
	var posicao := _cursor()
	_tempo_feedback = SEGUNDOS_FEEDBACK
	if posicao >= _zona_inicio and posicao <= _zona_inicio + largura:
		_feedback_erro = false
		_acertos += 1
		_velocidade *= ACELERACAO_POR_ACERTO
		if _acertos >= _por_nivel(ACERTOS_NECESSARIOS):
			finalizar(true)
		else:
			_sortear_zona()
		return
	_feedback_erro = true
	vidas -= 1
	if vidas <= 0:
		finalizar(false)


func _draw() -> void:
	var largura_zona: float = _por_nivel(LARGURA_ZONA)
	var inicio := Vector2((size.x - LARGURA_BARRA) / 2.0, 44.0)
	var moldura := Rect2(inicio - Vector2.ONE, Vector2(LARGURA_BARRA + 2, ALTURA_BARRA + 2))
	draw_rect(moldura, COR_BORDA)
	draw_rect(Rect2(inicio, Vector2(LARGURA_BARRA, ALTURA_BARRA)), COR_FUNDO)
	draw_rect(Rect2(inicio + Vector2(_zona_inicio * LARGURA_BARRA, 0),
			Vector2(largura_zona * LARGURA_BARRA, ALTURA_BARRA)), COR_ACERTO.darkened(0.35))
	var cor_cursor := COR_ACESO
	if _tempo_feedback > 0.0:
		cor_cursor = COR_ERRO if _feedback_erro else COR_ACERTO
	draw_rect(Rect2(inicio + Vector2(_cursor() * LARGURA_BARRA - 1, -4), Vector2(3, ALTURA_BARRA + 8)), cor_cursor)
	var necessarios: int = _por_nivel(ACERTOS_NECESSARIOS)
	for i in necessarios:
		var cor := COR_ACERTO if i < _acertos else COR_APAGADO
		draw_rect(Rect2(Vector2(size.x / 2.0 - necessarios * 6.0 + i * 12, 80), Vector2(9, 5)), cor)
	desenhar_texto("ACERTOS %d/%d" % [_acertos, necessarios], Vector2(8, 10), COR_TEXTO)
	desenhar_texto("FALHAS", Vector2(size.x - 62, 10), COR_TEXTO)
	desenhar_vidas(Vector2(size.x - 38, 3), _vidas_maximas)
	desenhar_resultado()
