extends MecanismoDoTempo

const ANOS_DE_LANCAMENTO: Array[int] = [1985, 1989, 1990]
const OPCOES_DE_ANO: Array[int] = [1985, 1987, 1989, 1990, 1991]
const ESCALA := 2.0
const LARGURA_QUADRO := 22.0
const ALTURA_QUADRO := 30.0
const ESPACO_QUADRO := 12.0
const LARGURA_OPCAO := 30.0
const ESPACO_OPCAO := 4.0
const ALTURA_CAIXA := 13.0
const COR_ESCOLHA := Color("ffb347")
const COR_FUNDO_CAIXA := Color("140c06")
const DICA_QUADRO := "Lados: escolher o quadro     E: escolher     Esc: sair"
const DICA_ANO := "Lados: escolher o ano     E: confirmar     Esc: voltar"

@export var quadros: Array[Texture2D] = []

var _travados: Array[bool] = []
var _quadro := 0
var _opcao := 0
var _escolhendo_ano := false


func _preparar() -> void:
	acertos_para_alinhar = ANOS_DE_LANCAMENTO.size()
	_travados.clear()
	for i in ANOS_DE_LANCAMENTO.size():
		_travados.append(false)
	_quadro = 0
	_opcao = 0
	_escolher_quadro()


func _tratar_entrada(evento: InputEvent) -> bool:
	if evento.is_action_pressed("mover_esquerda") or evento.is_action_pressed("ui_left"):
		_mover(-1)
	elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
		_mover(1)
	elif _escolhendo_ano and evento.is_action_pressed("ui_cancel"):
		_escolher_quadro()
	elif not _escolhendo_ano and (evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept")):
		_escolher_ano()
	else:
		return false
	return true


func _acertou() -> bool:
	return OPCOES_DE_ANO[_opcao] == ANOS_DE_LANCAMENTO[_quadro]


func _ao_acertar() -> void:
	_travados[_quadro] = true
	_quadro = _proximo_quadro_livre(_quadro, 1)
	_escolher_quadro()


func _erro_zera_acertos() -> bool:
	return false


func _escolher_quadro() -> void:
	_escolhendo_ano = false
	dica.text = DICA_QUADRO


func _escolher_ano() -> void:
	_escolhendo_ano = true
	if _ano_usado(_opcao):
		_opcao = _proxima_opcao_livre(_opcao, 1)
	dica.text = DICA_ANO


func _mover(passo: int) -> void:
	if _escolhendo_ano:
		_opcao = _proxima_opcao_livre(_opcao, passo)
	else:
		_quadro = _proximo_quadro_livre(_quadro, passo)


func _proximo_quadro_livre(de: int, passo: int) -> int:
	var i := de
	for _volta in _travados.size():
		i = posmod(i + passo, _travados.size())
		if not _travados[i]:
			return i
	return de


func _proxima_opcao_livre(de: int, passo: int) -> int:
	var i := de
	for _volta in OPCOES_DE_ANO.size():
		i = posmod(i + passo, OPCOES_DE_ANO.size())
		if not _ano_usado(i):
			return i
	return de


func _ano_usado(opcao: int) -> bool:
	for i in _travados.size():
		if _travados[i] and ANOS_DE_LANCAMENTO[i] == OPCOES_DE_ANO[opcao]:
			return true
	return false


func _desenhar(centro: Vector2) -> void:
	var fonte := desenho.get_theme_default_font()
	_desenhar_quadros(centro, fonte)
	_desenhar_opcoes(centro, fonte)


func _desenhar_quadros(centro: Vector2, fonte: Font) -> void:
	var tamanho := Vector2(LARGURA_QUADRO, ALTURA_QUADRO) * ESCALA
	var largura_total := tamanho.x * quadros.size() + ESPACO_QUADRO * (quadros.size() - 1)
	for i in quadros.size():
		var canto := Vector2(centro.x - largura_total / 2.0 + i * (tamanho.x + ESPACO_QUADRO), 2.0)
		var travado := _travado or _travados[i]
		var escolhido := not travado and i == _quadro
		desenho.draw_texture_rect(quadros[i], Rect2(canto, tamanho), false, Color.WHITE if travado or escolhido else Color(1, 1, 1, 0.5))
		var borda := COR_ALVO if travado else (COR_ESCOLHA if escolhido else COR_APAGADA)
		desenho.draw_rect(Rect2(canto - Vector2.ONE, tamanho + Vector2(2, 2)), borda, false, 2.0 if escolhido else 1.0)
		var texto := "----"
		var cor := COR_APAGADA
		if travado:
			texto = str(ANOS_DE_LANCAMENTO[i])
			cor = COR_ALVO
		elif escolhido and _escolhendo_ano:
			texto = str(OPCOES_DE_ANO[_opcao])
			cor = COR_ESCOLHA
		var caixa := Rect2(canto + Vector2(0, tamanho.y + 3.0), Vector2(tamanho.x, ALTURA_CAIXA))
		_desenhar_caixa(caixa, texto, cor, borda, fonte)


func _desenhar_opcoes(centro: Vector2, fonte: Font) -> void:
	var largura_total := LARGURA_OPCAO * OPCOES_DE_ANO.size() + ESPACO_OPCAO * (OPCOES_DE_ANO.size() - 1)
	for i in OPCOES_DE_ANO.size():
		var canto := Vector2(centro.x - largura_total / 2.0 + i * (LARGURA_OPCAO + ESPACO_OPCAO), 82.0)
		var cor := COR_TEXTO if _escolhendo_ano else COR_APAGADA
		if _ano_usado(i) or _travado:
			cor = COR_APAGADA
		elif _escolhendo_ano and i == _opcao:
			cor = COR_ESCOLHA
		_desenhar_caixa(Rect2(canto, Vector2(LARGURA_OPCAO, ALTURA_CAIXA)), str(OPCOES_DE_ANO[i]), cor, cor, fonte)


func _desenhar_caixa(caixa: Rect2, texto: String, cor_texto: Color, cor_borda: Color, fonte: Font) -> void:
	desenho.draw_rect(caixa, COR_FUNDO_CAIXA)
	desenho.draw_rect(caixa, cor_borda, false, 1.0)
	desenho.draw_string(fonte, Vector2(caixa.position.x, caixa.position.y + 10.0), texto, HORIZONTAL_ALIGNMENT_CENTER, caixa.size.x, 8, cor_texto)
