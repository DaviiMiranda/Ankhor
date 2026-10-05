extends MinigameHack

enum Fase { MOSTRANDO, ENTRADA }

const ACOES := ["mover_cima", "mover_direita", "mover_baixo", "mover_esquerda"]
const DIRECOES := [Vector2.UP, Vector2.RIGHT, Vector2.DOWN, Vector2.LEFT]
const TAMANHOS := [4, 6, 8]
const SEGUNDOS_ACESO := [0.7, 0.5, 0.32]
const VIDAS_POR_NIVEL := [3, 2, 1]
const ATRASO_INICIAL := 0.7
const LADO_CELULA := 26.0
const SEGUNDOS_FEEDBACK := 0.18

var _sequencia: Array[int] = []
var _fase := Fase.MOSTRANDO
var _tempo := 0.0
var _posicao := 0
var _vidas_maximas := 1
var _celula_apertada := -1
var _tempo_feedback := 0.0
var _feedback_erro := false


func preparar() -> void:
	titulo = "SEQUÊNCIA"
	instrucao = "Memorize e repita com as setas ou WASD"
	_vidas_maximas = _por_nivel(VIDAS_POR_NIVEL)
	vidas = _vidas_maximas
	_sequencia.clear()
	for i in _por_nivel(TAMANHOS) as int:
		_sequencia.append(randi() % 4)
	_mostrar_de_novo()


func _mostrar_de_novo() -> void:
	_fase = Fase.MOSTRANDO
	_tempo = -ATRASO_INICIAL
	_posicao = 0
	_celula_apertada = -1


func _process(delta: float) -> void:
	if encerrado:
		return
	if _tempo_feedback > 0.0:
		_tempo_feedback -= delta
		if _tempo_feedback <= 0.0:
			_celula_apertada = -1
	if _fase == Fase.MOSTRANDO:
		_tempo += delta
		if _indice_mostrado() >= _sequencia.size():
			_fase = Fase.ENTRADA
	queue_redraw()


func _segundos_aceso() -> float:
	return _por_nivel(SEGUNDOS_ACESO)


func _ciclo() -> float:
	return _segundos_aceso() * 1.45


func _indice_mostrado() -> int:
	if _tempo < 0.0:
		return -1
	return int(_tempo / _ciclo())


func _celula_acesa() -> int:
	if _fase != Fase.MOSTRANDO or _tempo < 0.0:
		return -1
	var indice := _indice_mostrado()
	if indice >= _sequencia.size() or fmod(_tempo, _ciclo()) > _segundos_aceso():
		return -1
	return _sequencia[indice]


func tratar_entrada(evento: InputEvent) -> void:
	if encerrado or _fase != Fase.ENTRADA:
		return
	for i in ACOES.size():
		if evento.is_action_pressed(ACOES[i]):
			_apertar(i)
			return


func _apertar(direcao: int) -> void:
	_celula_apertada = direcao
	_tempo_feedback = SEGUNDOS_FEEDBACK
	if direcao == _sequencia[_posicao]:
		_feedback_erro = false
		_posicao += 1
		if _posicao >= _sequencia.size():
			finalizar(true)
		return
	_feedback_erro = true
	vidas -= 1
	if vidas <= 0:
		finalizar(false)
	else:
		_mostrar_de_novo()


func _draw() -> void:
	var centro := Vector2(size.x / 2.0, 50.0)
	var acesa := _celula_acesa()
	for i in DIRECOES.size():
		var cor := COR_APAGADO
		if i == acesa:
			cor = COR_ACESO
		elif i == _celula_apertada:
			cor = COR_ERRO if _feedback_erro else COR_ACERTO
		_desenhar_celula(centro + DIRECOES[i] * (LADO_CELULA + 2.0), DIRECOES[i], cor)
	for i in _sequencia.size():
		var cor := COR_APAGADO
		if i < _posicao:
			cor = COR_ACERTO
		draw_rect(Rect2(Vector2(size.x / 2.0 - _sequencia.size() * 5.0 + i * 10, 96), Vector2(7, 4)), cor)
	var estado := "OBSERVE" if _fase == Fase.MOSTRANDO else "REPITA"
	desenhar_texto(estado, Vector2(8, 10), COR_TEXTO)
	desenhar_texto("FALHAS", Vector2(size.x - 62, 10), COR_TEXTO)
	desenhar_vidas(Vector2(size.x - 38, 3), _vidas_maximas)
	desenhar_resultado()


func _desenhar_celula(centro: Vector2, direcao: Vector2, cor: Color) -> void:
	var metade := LADO_CELULA / 2.0
	draw_rect(Rect2(centro - Vector2(metade, metade), Vector2(LADO_CELULA, LADO_CELULA)), cor.darkened(0.55))
	draw_rect(Rect2(centro - Vector2(metade, metade), Vector2(LADO_CELULA, LADO_CELULA)), cor, false, 1.0)
	var lateral := Vector2(-direcao.y, direcao.x)
	var ponta := centro + direcao * 7.0
	var base := centro - direcao * 6.0
	draw_colored_polygon(PackedVector2Array([ponta, base + lateral * 7.0, base - lateral * 7.0]), cor)
