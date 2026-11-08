extends MecanismoDoTempo

const COLUNAS := 7
const LINHAS := 5
const LADO := 18.0
const MIN_CELULAS_DO_CAMINHO := 11
const MAX_CELULAS_DO_CAMINHO := 15
const SEGUNDOS_DO_GIRO := 0.14
const SEM_GIRO := -100.0
const NORTE := 1
const LESTE := 2
const SUL := 4
const OESTE := 8
const LADOS := NORTE | LESTE | SUL | OESTE
const RETO := NORTE | SUL
const CURVA := NORTE | LESTE
const TE := NORTE | LESTE | SUL
const PONTA := NORTE
const DIRECOES: Array[int] = [NORTE, LESTE, SUL, OESTE]
const VETORES := {NORTE: Vector2i.UP, LESTE: Vector2i.RIGHT, SUL: Vector2i.DOWN, OESTE: Vector2i.LEFT}
const ENFEITES: Array[int] = [RETO, RETO, RETO, CURVA, CURVA, CURVA, TE, TE, LADOS, PONTA, PONTA, 0]
const COR_ESCOLHA := Color("ffb347")
const COR_CELULA := Color("140c06")
const COR_CENTRAL := Color("3a4a5a")
const COR_APARELHO := Color("8a1c1c")
const COR_DISCO := Color("e8dcc0")

var _pecas: Array[int] = []
var _giro_em: Array[float] = []
var _energizadas: Array[bool] = []
var _entrada := 0
var _saida := 0
var _cursor := Vector2i.ZERO
var _resposta_certa := false

@onready var som_giro: AudioStreamPlayer = $Tela/SomGiro


func _ready() -> void:
	super()
	_montar_tabuleiro()


func _preparar() -> void:
	_cursor = Vector2i(0, _entrada)


func _montar_tabuleiro() -> void:
	var caminho := _sortear_caminho()
	_pecas.clear()
	for i in COLUNAS * LINHAS:
		_pecas.append(ENFEITES.pick_random())
	for i in caminho.size():
		var anterior := Vector2i(-1, caminho[i].y) if i == 0 else caminho[i - 1]
		var seguinte := Vector2i(COLUNAS, caminho[i].y) if i == caminho.size() - 1 else caminho[i + 1]
		_pecas[_indice(caminho[i])] = _lado_para(caminho[i], anterior) | _lado_para(caminho[i], seguinte)
	_giro_em.clear()
	_giro_em.resize(_pecas.size())
	_giro_em.fill(SEM_GIRO)
	_energizadas.resize(_pecas.size())
	_girar_tudo_ao_acaso()
	while _ligacao_completa():
		_girar_tudo_ao_acaso()


func _sortear_caminho() -> Array[Vector2i]:
	_entrada = randi_range(0, LINHAS - 1)
	_saida = randi_range(0, LINHAS - 1)
	var caminho: Array[Vector2i] = [Vector2i(0, _entrada)]
	_estender(caminho)
	return caminho


func _estender(caminho: Array[Vector2i]) -> bool:
	var ponta := caminho[-1]
	if ponta == Vector2i(COLUNAS - 1, _saida):
		return caminho.size() >= MIN_CELULAS_DO_CAMINHO
	var distancia_ate_a_saida := absi(COLUNAS - 1 - ponta.x) + absi(_saida - ponta.y)
	if caminho.size() + distancia_ate_a_saida > MAX_CELULAS_DO_CAMINHO:
		return false
	var lados := DIRECOES.duplicate()
	lados.shuffle()
	for lado: int in lados:
		var proxima: Vector2i = ponta + VETORES[lado]
		if _dentro(proxima) and not caminho.has(proxima):
			caminho.append(proxima)
			if _estender(caminho):
				return true
			caminho.pop_back()
	return false


func _lado_para(de: Vector2i, para: Vector2i) -> int:
	for lado in DIRECOES:
		if VETORES[lado] == para - de:
			return lado
	return 0


func _girar_tudo_ao_acaso() -> void:
	for i in _pecas.size():
		for _volta in randi_range(0, 3):
			_pecas[i] = _girada(_pecas[i])
	_calcular_energia()


func _girada(peca: int) -> int:
	return ((peca << 1) | (peca >> 3)) & LADOS


func _oposta(lado: int) -> int:
	return ((lado << 2) | (lado >> 2)) & LADOS


func _indice(celula: Vector2i) -> int:
	return celula.y * COLUNAS + celula.x


func _dentro(celula: Vector2i) -> bool:
	return celula.x >= 0 and celula.x < COLUNAS and celula.y >= 0 and celula.y < LINHAS


func _calcular_energia() -> void:
	_energizadas.fill(false)
	var origem := Vector2i(0, _entrada)
	if (_pecas[_indice(origem)] & OESTE) == 0:
		return
	_energizadas[_indice(origem)] = true
	var fila: Array[Vector2i] = [origem]
	while not fila.is_empty():
		var atual: Vector2i = fila.pop_front()
		for lado in DIRECOES:
			if (_pecas[_indice(atual)] & lado) == 0:
				continue
			var vizinha: Vector2i = atual + VETORES[lado]
			if not _dentro(vizinha) or _energizadas[_indice(vizinha)]:
				continue
			if (_pecas[_indice(vizinha)] & _oposta(lado)) == 0:
				continue
			_energizadas[_indice(vizinha)] = true
			fila.append(vizinha)


func _ligacao_completa() -> bool:
	var ultima := _indice(Vector2i(COLUNAS - 1, _saida))
	return _energizadas[ultima] and (_pecas[ultima] & LESTE) != 0


func _tratar_entrada(evento: InputEvent) -> bool:
	var passo := _passo_pedido(evento)
	if passo != Vector2i.ZERO:
		_mover(passo)
	elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		_girar_peca()
	else:
		return false
	return true


func _passo_pedido(evento: InputEvent) -> Vector2i:
	if _apertou(evento, "mover_esquerda", "ui_left"):
		return Vector2i.LEFT
	if _apertou(evento, "mover_direita", "ui_right"):
		return Vector2i.RIGHT
	if _apertou(evento, "mover_cima", "ui_up"):
		return Vector2i.UP
	if _apertou(evento, "mover_baixo", "ui_down"):
		return Vector2i.DOWN
	return Vector2i.ZERO


func _apertou(evento: InputEvent, acao: String, acao_de_menu: String) -> bool:
	return evento.is_action_pressed(acao, true) or evento.is_action_pressed(acao_de_menu, true)


func _mover(passo: Vector2i) -> void:
	_cursor = Vector2i(clampi(_cursor.x + passo.x, 0, COLUNAS - 1), clampi(_cursor.y + passo.y, 0, LINHAS - 1))


func _girar_peca() -> void:
	var i := _indice(_cursor)
	if _girada(_pecas[i]) == _pecas[i]:
		return
	_pecas[i] = _girada(_pecas[i])
	_giro_em[i] = _tempo
	som_giro.play()
	_calcular_energia()
	if _ligacao_completa():
		_resposta_certa = true
		_tentar()
	else:
		_mostrar_visor()


func _acertou() -> bool:
	return _resposta_certa


func _texto_do_visor() -> String:
	return "CABOS COM SINAL: %d" % _energizadas.count(true)


func _desenhar(centro: Vector2) -> void:
	var origem := centro - Vector2(COLUNAS, LINHAS) * LADO / 2.0
	_desenhar_central(origem)
	_desenhar_aparelho(origem)
	for y in LINHAS:
		for x in COLUNAS:
			_desenhar_peca(origem, Vector2i(x, y))
	var caixa := Rect2(origem + Vector2(_cursor) * LADO, Vector2(LADO, LADO))
	desenho.draw_rect(caixa.grow(-1.0), COR_ESCOLHA, false, 2.0)


func _desenhar_peca(origem: Vector2, celula: Vector2i) -> void:
	var i := _indice(celula)
	var caixa := Rect2(origem + Vector2(celula) * LADO, Vector2(LADO, LADO))
	desenho.draw_rect(caixa, COR_CELULA)
	desenho.draw_rect(caixa, COR_APAGADA, false, 1.0)
	var cor := COR_ALVO if _energizadas[i] else COR_METAL
	var meio := caixa.get_center()
	var progresso := clampf((_tempo - _giro_em[i]) / SEGUNDOS_DO_GIRO, 0.0, 1.0)
	var desvio := -PI / 2.0 * (1.0 - progresso) * (1.0 - progresso)
	var conexoes := 0
	for lado in DIRECOES:
		if (_pecas[i] & lado) != 0:
			conexoes += 1
			desenho.draw_line(meio, meio + Vector2(VETORES[lado]).rotated(desvio) * LADO / 2.0, cor, 3.0)
	if conexoes > 0:
		desenho.draw_circle(meio, 3.5 if conexoes != 2 else 1.5, cor)


func _desenhar_central(origem: Vector2) -> void:
	var meio := Vector2(origem.x - 12.0, origem.y + (_entrada + 0.5) * LADO)
	desenho.draw_line(meio, Vector2(origem.x, meio.y), COR_ALVO, 3.0)
	var caixa := Rect2(meio - Vector2(8.0, 8.0), Vector2(16.0, 16.0))
	desenho.draw_rect(caixa, COR_CENTRAL)
	desenho.draw_rect(caixa, COR_METAL, false, 1.0)
	for desvio_x in [-3.5, 3.5]:
		for desvio_y in [-3.5, 3.5]:
			desenho.draw_circle(meio + Vector2(desvio_x, desvio_y), 1.5, COR_ALVO)


func _desenhar_aparelho(origem: Vector2) -> void:
	var ligado := _ligacao_completa()
	var cor_do_fio := COR_ALVO if ligado else COR_METAL
	var meio := Vector2(origem.x + COLUNAS * LADO + 12.0, origem.y + (_saida + 0.5) * LADO)
	desenho.draw_line(Vector2(origem.x + COLUNAS * LADO, meio.y), meio, cor_do_fio, 3.0)
	var caixa := Rect2(meio - Vector2(8.0, 8.0), Vector2(16.0, 16.0))
	desenho.draw_rect(caixa, COR_APARELHO)
	desenho.draw_line(meio + Vector2(-8.0, -9.0), meio + Vector2(8.0, -9.0), COR_METAL, 2.0)
	desenho.draw_circle(meio, 5.5, COR_DISCO)
	desenho.draw_arc(meio, 6.5, 0.0, TAU, 16, cor_do_fio, 1.0)
	desenho.draw_circle(meio, 1.5, COR_APARELHO)
