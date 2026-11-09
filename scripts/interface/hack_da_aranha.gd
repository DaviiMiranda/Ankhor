class_name HackDaAranha
extends CanvasLayer

signal resolvido

const NIVEIS: Array[Dictionary] = [
	{"colunas": 5, "linhas": 3, "minimo": 7, "maximo": 9, "segundos": 18.0},
	{"colunas": 5, "linhas": 4, "minimo": 8, "maximo": 11, "segundos": 18.0},
	{"colunas": 6, "linhas": 4, "minimo": 9, "maximo": 13, "segundos": 17.0},
	{"colunas": 6, "linhas": 4, "minimo": 10, "maximo": 14, "segundos": 16.0},
]
const LARGURA_DA_TELA := 320.0
const LARGURA_DO_CHIP := 26.0
const MARGEM := 8.0
const ALTURA_DO_CABECALHO := 14.0
const ALTURA_DA_BARRA := 18.0
const ALTURA_DO_RODAPE := 14.0
const SEGUNDOS_DO_GIRO := 0.12
const SEGUNDOS_DE_PERIGO := 5.0
const SEGUNDOS_DO_RESULTADO := 0.9
const COR_PAINEL := Color(0.05, 0.012, 0.02, 0.96)
const COR_BORDA := Color(0.55, 0.1, 0.12)
const COR_CABECALHO := Color(0.42, 0.06, 0.08)
const COR_TEXTO := Color(1.0, 0.84, 0.8)
const COR_CELULA := Color(0.09, 0.025, 0.035)
const COR_GRADE := Color(0.22, 0.07, 0.09)
const COR_TRILHA := Color(0.5, 0.15, 0.12)
const COR_SINAL := Color(0.45, 1.0, 0.95)
const COR_NUCLEO := Color(1.0, 0.18, 0.12)
const COR_PERIGO := Color(1.0, 0.32, 0.2)
const COR_CURSOR := Color(1.0, 0.95, 0.9)

var _grade: GradeDeCabos
var _cursor := Vector2i.ZERO
var _tempo := 0.0
var _total := 1.0
var _restante := 1.0
var _segundo_do_tique := -1
var _giro_em: Array[float] = []
var _encerrado := false
var _resultado := false
var _tremor := Vector2.ZERO

@onready var desenho: Control = $Desenho
@onready var som_giro: AudioStreamPlayer = $SomGiro
@onready var som_ligou: AudioStreamPlayer = $SomLigou
@onready var som_tique: AudioStreamPlayer = $SomTique


static func nivel(numero: int) -> Dictionary:
	return NIVEIS[clampi(numero - 1, 0, NIVEIS.size() - 1)]


func _ready() -> void:
	desenho.draw.connect(_desenhar)


func iniciar(dados: Dictionary, segundos: float) -> void:
	_grade = GradeDeCabos.new(dados["colunas"], dados["linhas"], dados["minimo"], dados["maximo"])
	_cursor = Vector2i(0, _grade.entrada)
	_total = maxf(segundos, 0.1)
	_restante = _total
	_giro_em.clear()
	_giro_em.resize(_grade.pecas.size())
	_giro_em.fill(-100.0)
	_encerrado = false
	desenho.queue_redraw()


func atualizar_tempo(restante: float) -> void:
	_restante = restante


func mostrar_resultado(sucesso: bool) -> void:
	if _encerrado:
		return
	_encerrado = true
	_resultado = sucesso
	desenho.queue_redraw()
	await get_tree().create_timer(SEGUNDOS_DO_RESULTADO).timeout
	queue_free()


func _process(delta: float) -> void:
	_tempo += delta
	_tremor = Vector2.ZERO
	if _restante < SEGUNDOS_DE_PERIGO and not _encerrado:
		_tremor = Vector2(randi_range(-1, 1), 0)
		_tocar_tique()
	desenho.queue_redraw()


func _tocar_tique() -> void:
	var segundo := ceili(_restante)
	if segundo != _segundo_do_tique:
		_segundo_do_tique = segundo
		som_tique.play()


func _unhandled_input(evento: InputEvent) -> void:
	if _grade == null:
		return
	if not _encerrado:
		var passo := _passo_pedido(evento)
		if passo != Vector2i.ZERO:
			_mover(passo)
		elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
			_girar()
	get_viewport().set_input_as_handled()


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
	_cursor = Vector2i(clampi(_cursor.x + passo.x, 0, _grade.colunas - 1), clampi(_cursor.y + passo.y, 0, _grade.linhas - 1))


func _girar() -> void:
	if not _grade.girar(_cursor):
		return
	_giro_em[_grade.indice(_cursor)] = _tempo
	som_giro.play()
	if _grade.ligada():
		som_ligou.play()
		mostrar_resultado(true)
		resolvido.emit()


func _lado() -> float:
	return 22.0 if _grade.linhas <= 3 else 18.0


func _painel() -> Rect2:
	var lado := _lado()
	var largura := _grade.colunas * lado + 2.0 * LARGURA_DO_CHIP + 2.0 * MARGEM
	var altura := ALTURA_DO_CABECALHO + ALTURA_DA_BARRA + _grade.linhas * lado + ALTURA_DO_RODAPE + MARGEM
	return Rect2(Vector2((LARGURA_DA_TELA - largura) / 2.0, 0.0), Vector2(largura, altura))


func _origem_da_grade() -> Vector2:
	return _painel().position + Vector2(MARGEM + LARGURA_DO_CHIP, ALTURA_DO_CABECALHO + ALTURA_DA_BARRA)


func _perigo() -> bool:
	return _restante < SEGUNDOS_DE_PERIGO and not _encerrado


func _desenhar() -> void:
	if _grade == null:
		return
	desenho.draw_set_transform(_tremor, 0.0, Vector2.ONE)
	var painel := _painel()
	desenho.draw_rect(painel, COR_PAINEL)
	desenho.draw_rect(painel, COR_PERIGO if _perigo() and fmod(_tempo, 0.4) < 0.2 else COR_BORDA, false, 1.0)
	_desenhar_cabecalho(painel)
	_desenhar_barra(painel)
	var origem := _origem_da_grade()
	_desenhar_chips(origem)
	for y in _grade.linhas:
		for x in _grade.colunas:
			_desenhar_celula(origem, Vector2i(x, y))
	if not _encerrado:
		_desenhar_cursor(origem)
	_texto("Setas: escolher o cabo     E: girar", Vector2(painel.position.x, painel.end.y - 4.0), COR_GRADE.lightened(0.45), painel.size.x)
	if _encerrado:
		_desenhar_resultado(painel, origem)
	desenho.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _texto(texto: String, posicao: Vector2, cor: Color, largura: float, alinhamento := HORIZONTAL_ALIGNMENT_CENTER) -> void:
	desenho.draw_string(desenho.get_theme_default_font(), posicao, texto, alinhamento, largura, 8, cor)


func _desenhar_cabecalho(painel: Rect2) -> void:
	desenho.draw_rect(Rect2(painel.position, Vector2(painel.size.x, ALTURA_DO_CABECALHO)), COR_CABECALHO)
	_texto("INTRUSÃO // ARANHA 07", painel.position + Vector2(MARGEM, 10.0), COR_TEXTO, painel.size.x, HORIZONTAL_ALIGNMENT_LEFT)
	var cor := COR_PERIGO if _perigo() else COR_TEXTO
	_texto("%04.1f s" % maxf(_restante, 0.0), painel.position + Vector2(-MARGEM, 10.0), cor, painel.size.x, HORIZONTAL_ALIGNMENT_RIGHT)


func _desenhar_barra(painel: Rect2) -> void:
	var trilho := Rect2(painel.position + Vector2(MARGEM, ALTURA_DO_CABECALHO + 7.0), Vector2(painel.size.x - 2.0 * MARGEM, 5.0))
	desenho.draw_rect(trilho, COR_CELULA)
	desenho.draw_rect(trilho, COR_GRADE, false, 1.0)
	var chegada := clampf(1.0 - _restante / _total, 0.0, 1.0)
	var cor := COR_TRILHA.lerp(COR_PERIGO, chegada)
	if _perigo() and fmod(_tempo, 0.4) < 0.2:
		cor = COR_TEXTO
	var enchimento := Rect2(trilho.position, Vector2(trilho.size.x * chegada, trilho.size.y))
	desenho.draw_rect(enchimento, cor)
	for i in range(1, 10):
		var x := trilho.position.x + trilho.size.x * i / 10.0
		desenho.draw_line(Vector2(x, trilho.end.y - 1.0), Vector2(x, trilho.end.y + 1.0), COR_GRADE, 1.0)
	var olho := Vector2(enchimento.end.x, trilho.get_center().y)
	desenho.draw_circle(olho, 3.5, COR_CELULA)
	desenho.draw_circle(olho, 2.5, COR_NUCLEO)
	desenho.draw_circle(olho, 1.0, COR_TEXTO)
	var alvo := Vector2(trilho.end.x + 1.0, trilho.get_center().y)
	desenho.draw_rect(Rect2(alvo - Vector2(1.0, 4.0), Vector2(2.0, 8.0)), COR_SINAL)


func _desenhar_chips(origem: Vector2) -> void:
	var lado := _lado()
	var meio_entrada := origem.y + (_grade.entrada + 0.5) * lado
	var chip_entrada := Rect2(Vector2(origem.x - LARGURA_DO_CHIP + 2.0, meio_entrada - lado / 2.0 + 2.0), Vector2(LARGURA_DO_CHIP - 10.0, lado - 4.0))
	desenho.draw_line(Vector2(chip_entrada.end.x, meio_entrada), Vector2(origem.x, meio_entrada), COR_SINAL, 2.0)
	desenho.draw_rect(chip_entrada, COR_CELULA)
	desenho.draw_rect(chip_entrada, COR_SINAL, false, 1.0)
	var centro := chip_entrada.get_center()
	desenho.draw_colored_polygon(PackedVector2Array([centro + Vector2(1, -5), centro + Vector2(-3, 1), centro + Vector2(0, 1), centro + Vector2(-1, 5), centro + Vector2(3, -1), centro + Vector2(0, -1)]), COR_SINAL)
	var ligada := _grade.ligada()
	var cor_saida := COR_SINAL if ligada else COR_NUCLEO
	var meio_saida := origem.y + (_grade.saida + 0.5) * lado
	var borda_direita := origem.x + _grade.colunas * lado
	var chip_saida := Rect2(Vector2(borda_direita + 8.0, meio_saida - lado / 2.0 + 2.0), Vector2(LARGURA_DO_CHIP - 10.0, lado - 4.0))
	desenho.draw_line(Vector2(borda_direita, meio_saida), Vector2(chip_saida.position.x, meio_saida), COR_SINAL if ligada else COR_TRILHA, 2.0)
	desenho.draw_rect(chip_saida, COR_CELULA)
	desenho.draw_rect(chip_saida, cor_saida, false, 1.0)
	var pulso := 0.7 + 0.3 * sin(_tempo * 8.0)
	desenho.draw_circle(chip_saida.get_center(), 4.5, Color(cor_saida, 0.3 * pulso))
	desenho.draw_circle(chip_saida.get_center(), 2.8, cor_saida)
	desenho.draw_circle(chip_saida.get_center(), 1.0, COR_TEXTO)


func _desenhar_celula(origem: Vector2, celula: Vector2i) -> void:
	var lado := _lado()
	var i := _grade.indice(celula)
	var caixa := Rect2(origem + Vector2(celula) * lado, Vector2(lado, lado))
	desenho.draw_rect(caixa, COR_CELULA)
	desenho.draw_rect(caixa, COR_GRADE, false, 1.0)
	var peca := _grade.pecas[i]
	if peca == 0:
		desenho.draw_rect(Rect2(caixa.get_center() - Vector2.ONE, Vector2(2.0, 2.0)), COR_GRADE)
		return
	var energizada := _grade.energizadas[i]
	var cor := COR_TRILHA
	if energizada:
		var onda := 0.5 + 0.5 * sin(_tempo * 9.0 - _grade.distancias[i] * 1.1)
		cor = COR_SINAL.lerp(Color.WHITE, 0.45 * onda)
	var progresso := clampf((_tempo - _giro_em[i]) / SEGUNDOS_DO_GIRO, 0.0, 1.0)
	var desvio := -PI / 2.0 * (1.0 - progresso) * (1.0 - progresso)
	desenho.draw_set_transform(_tremor + caixa.get_center(), desvio, Vector2.ONE)
	var lados := _lados_da_peca(peca)
	if energizada:
		_tracar(lados, lado / 2.0, Color(cor, 0.28), 5.0)
	_tracar(lados, lado / 2.0, cor, 2.0)
	desenho.draw_set_transform(_tremor, 0.0, Vector2.ONE)


func _lados_da_peca(peca: int) -> Array[Vector2]:
	var lados: Array[Vector2] = []
	for lado in GradeDeCabos.DIRECOES:
		if (peca & lado) != 0:
			lados.append(Vector2(GradeDeCabos.VETORES[lado]))
	return lados


func _tracar(lados: Array[Vector2], meio: float, cor: Color, espessura: float) -> void:
	if lados.size() == 2:
		var a := lados[0]
		var b := lados[1]
		if is_zero_approx(a.dot(b)):
			desenho.draw_polyline(PackedVector2Array([a * meio, a * meio * 0.35, b * meio * 0.35, b * meio]), cor, espessura)
		else:
			desenho.draw_line(a * meio, b * meio, cor, espessura)
		return
	for direcao in lados:
		desenho.draw_line(Vector2.ZERO, direcao * meio, cor, espessura)
	var ponto := maxf(espessura * 1.5, 3.0)
	desenho.draw_rect(Rect2(Vector2(-ponto / 2.0, -ponto / 2.0), Vector2(ponto, ponto)), cor)


func _desenhar_cursor(origem: Vector2) -> void:
	var lado := _lado()
	var caixa := Rect2(origem + Vector2(_cursor) * lado, Vector2(lado, lado)).grow(-1.0)
	var cor := Color(COR_CURSOR, 0.7 + 0.3 * sin(_tempo * 10.0))
	var canto := 5.0
	var cantos := [
		[caixa.position, Vector2.RIGHT, Vector2.DOWN],
		[Vector2(caixa.end.x, caixa.position.y), Vector2.LEFT, Vector2.DOWN],
		[caixa.end, Vector2.LEFT, Vector2.UP],
		[Vector2(caixa.position.x, caixa.end.y), Vector2.RIGHT, Vector2.UP],
	]
	for dados in cantos:
		var ponto: Vector2 = dados[0]
		desenho.draw_line(ponto, ponto + (dados[1] as Vector2) * canto, cor, 2.0)
		desenho.draw_line(ponto, ponto + (dados[2] as Vector2) * canto, cor, 2.0)


func _desenhar_resultado(painel: Rect2, origem: Vector2) -> void:
	var faixa := Rect2(Vector2(painel.position.x, origem.y + _grade.linhas * _lado() / 2.0 - 11.0), Vector2(painel.size.x, 22.0))
	desenho.draw_rect(faixa, Color(0, 0, 0, 0.85))
	var cor := COR_SINAL if _resultado else COR_PERIGO
	var texto := "NÚCLEO 07 DOMINADO" if _resultado else "SEM TEMPO"
	_texto(texto, faixa.position + Vector2(0.0, 14.0), cor, faixa.size.x)
