extends MecanismoDoTempo

const NUMERO := "1876"
const DIGITOS := "1234567890"
const ANGULO_BATENTE := PI / 3.0
const PASSO := PI / 6.0
const RAIO_BASE := 44.0
const RAIO_DISCO := 38.0
const RAIO_FURO := 28.0
const TAMANHO_FURO := 6.0
const VELOCIDADE_IDA := 9.0
const SEGUNDOS_POR_PULSO := 0.1
const SEGUNDOS_MENSAGEM := 1.6
const COR_APARELHO := Color("8a1c1c")
const COR_DISCO := Color("e8dcc0")

var _discado := ""
var _furo := 0
var _furo_girando := -1
var _indo := false
var _giro := 0.0
var _resposta_certa := false
var _mensagem := ""
var _mensagem_ate := 0.0

@onready var som_pulso: AudioStreamPlayer = $Tela/SomPulso


func _preparar() -> void:
	acertos_para_alinhar = 1
	_discado = ""
	_furo = 0
	_furo_girando = -1
	_giro = 0.0


func _tratar_entrada(evento: InputEvent) -> bool:
	if evento.is_action_pressed("ui_cancel"):
		return false
	if _furo_girando >= 0:
		return true
	if evento.is_action_pressed("mover_esquerda") or evento.is_action_pressed("ui_left"):
		_furo = posmod(_furo - 1, DIGITOS.length())
	elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
		_furo = posmod(_furo + 1, DIGITOS.length())
	elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		_discar(_furo)
	elif evento is InputEventKey and (evento as InputEventKey).unicode >= 48 and (evento as InputEventKey).unicode <= 57:
		_furo = DIGITOS.find(String.chr((evento as InputEventKey).unicode))
		_discar(_furo)
	return true


func _discar(furo: int) -> void:
	_furo_girando = furo
	_indo = true


func _pulsos(furo: int) -> int:
	return furo + 1


func _avancar(delta: float) -> void:
	if _furo_girando < 0:
		return
	var alvo := _pulsos(_furo_girando) * PASSO
	if _indo:
		_giro = minf(_giro + VELOCIDADE_IDA * delta, alvo)
		_indo = _giro < alvo
		return
	var pulsos_antes := ceili(_giro / PASSO - 0.001)
	_giro = maxf(_giro - PASSO / SEGUNDOS_POR_PULSO * delta, 0.0)
	if ceili(_giro / PASSO - 0.001) < pulsos_antes:
		som_pulso.play()
	if _giro <= 0.0:
		_terminar_digito()


func _terminar_digito() -> void:
	_discado += DIGITOS[_furo_girando]
	_furo_girando = -1
	if _discado.length() == NUMERO.length():
		_resposta_certa = _discado == NUMERO
		_tentar()


func _acertou() -> bool:
	return _resposta_certa


func _ao_errar() -> void:
	_mensagem = "NÚMERO INEXISTENTE"
	_mensagem_ate = _tempo + SEGUNDOS_MENSAGEM
	_discado = ""


func _angulo_do_furo(furo: int) -> float:
	return ANGULO_BATENTE - _pulsos(furo) * PASSO


func _desenhar(centro: Vector2) -> void:
	var meio := Vector2(54.0, centro.y)
	var fonte := desenho.get_theme_default_font()
	desenho.draw_circle(meio, RAIO_BASE, COR_APARELHO)
	desenho.draw_circle(meio, RAIO_DISCO, COR_APARELHO.lightened(0.15))
	for i in DIGITOS.length():
		var fixo := meio + Vector2.from_angle(_angulo_do_furo(i)) * RAIO_FURO
		desenho.draw_string(fonte, fixo + Vector2(-4.0, 4.0), DIGITOS[i], HORIZONTAL_ALIGNMENT_CENTER, 8.0, 8, COR_DISCO)
	desenho.draw_arc(meio, RAIO_DISCO, 0.0, TAU, 48, COR_DISCO, 2.0)
	for i in DIGITOS.length():
		var furo := meio + Vector2.from_angle(_angulo_do_furo(i) + _giro) * RAIO_FURO
		var escolhido := _furo_girando < 0 and i == _furo
		desenho.draw_arc(furo, TAMANHO_FURO, 0.0, TAU, 16, COR_ALVO if escolhido else COR_DISCO, 2.0 if escolhido else 1.0)
	desenho.draw_circle(meio, 9.0, COR_DISCO)
	var batente := Vector2.from_angle(ANGULO_BATENTE)
	desenho.draw_line(meio + batente * (RAIO_FURO + 2.0), meio + batente * (RAIO_BASE + 3.0), COR_METAL, 3.0)
	_desenhar_numero(fonte)


func _desenhar_numero(fonte: Font) -> void:
	var x0 := 108.0
	desenho.draw_string(fonte, Vector2(x0, 22.0), "DISCANDO", HORIZONTAL_ALIGNMENT_LEFT, 70.0, 8, COR_TEXTO)
	for i in NUMERO.length():
		var caixa := Rect2(Vector2(x0 + i * 17.0, 30.0), Vector2(14.0, 16.0))
		desenho.draw_rect(caixa, Color("140c06"))
		desenho.draw_rect(caixa, COR_TEXTO if i == _discado.length() else COR_APAGADA, false, 1.0)
		if i < _discado.length():
			desenho.draw_string(fonte, caixa.position + Vector2(0.0, 12.0), _discado[i], HORIZONTAL_ALIGNMENT_CENTER, caixa.size.x, 8, COR_ALVO if _travado else COR_TEXTO)
	if _tempo >= _mensagem_ate:
		return
	var partes := _mensagem.split(" ")
	for j in partes.size():
		desenho.draw_string(fonte, Vector2(x0, 64.0 + j * 14.0), partes[j], HORIZONTAL_ALIGNMENT_LEFT, 72.0, 8, COR_ERRO)
