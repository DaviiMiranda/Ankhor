extends MecanismoDoTempo

const CORES: Array[Color] = [Color("2ec24a"), Color("e0303a"), Color("2a6ae0"), Color("f0c828")]
const ACOES: Array[String] = ["mover_cima", "mover_direita", "mover_baixo", "mover_esquerda"]
const ACOES_UI: Array[String] = ["ui_up", "ui_right", "ui_down", "ui_left"]
const RAIO := 30.0
const GROSSURA := 20.0
const ESPERA_ANTES := 0.7
const SEGUNDOS_ACESO_JOGADOR := 0.22

@export var tamanho_inicial: int = 3
@export var segundos_aceso_inicial: float = 0.45
@export var segundos_apagado: float = 0.18
@export var aceleracao_por_rodada: float = 0.85
@export var sons: Array[AudioStream] = []

var _sequencia: Array[int] = []
var _posicao := 0
var _mostrando := true
var _inicio_mostra := 0.0
var _segundos_aceso := 0.0
var _passo_mostrado := -1
var _aceso_jogador := -1
var _apagar_em := 0.0
var _resposta_certa := false

@onready var som_cor: AudioStreamPlayer = $Tela/SomCor


func _preparar() -> void:
	_sequencia.clear()
	for i in tamanho_inicial:
		_sequencia.append(randi_range(0, CORES.size() - 1))
	_segundos_aceso = segundos_aceso_inicial
	_mostrar_sequencia()


func _mostrar_sequencia() -> void:
	_mostrando = true
	_posicao = 0
	_passo_mostrado = -1
	_inicio_mostra = _tempo + ESPERA_ANTES


func _avancar(_delta: float) -> void:
	if _aceso_jogador >= 0 and _tempo >= _apagar_em:
		_aceso_jogador = -1
	if not _mostrando or _tempo < _inicio_mostra:
		return
	var passo := floori((_tempo - _inicio_mostra) / (_segundos_aceso + segundos_apagado))
	if passo >= _sequencia.size():
		_mostrando = false
	elif passo != _passo_mostrado:
		_passo_mostrado = passo
		_tocar(_sequencia[passo])


func _cor_mostrada() -> int:
	if _aceso_jogador >= 0:
		return _aceso_jogador
	if not _mostrando or _passo_mostrado < 0:
		return -1
	var dentro := fmod(_tempo - _inicio_mostra, _segundos_aceso + segundos_apagado)
	return _sequencia[_passo_mostrado] if dentro < _segundos_aceso else -1


func _tratar_entrada(evento: InputEvent) -> bool:
	for i in ACOES.size():
		if evento.is_action_pressed(ACOES[i]) or evento.is_action_pressed(ACOES_UI[i]):
			_apertar(i)
			return true
	return evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept")


func _apertar(cor: int) -> void:
	if _mostrando:
		return
	_aceso_jogador = cor
	_apagar_em = _tempo + SEGUNDOS_ACESO_JOGADOR
	if cor != _sequencia[_posicao]:
		_resposta_certa = false
		_tentar()
		return
	_tocar(cor)
	_posicao += 1
	if _posicao == _sequencia.size():
		_resposta_certa = true
		_tentar()


func _acertou() -> bool:
	return _resposta_certa


func _ao_acertar() -> void:
	_sequencia.append(randi_range(0, CORES.size() - 1))
	_segundos_aceso *= aceleracao_por_rodada
	_mostrar_sequencia()


func _ao_errar() -> void:
	_mostrar_sequencia()


func _erro_zera_acertos() -> bool:
	return false


func _tocar(cor: int) -> void:
	if cor < sons.size():
		som_cor.stream = sons[cor]
		som_cor.play()


func _desenhar(centro: Vector2) -> void:
	var meio := centro + Vector2(0, -6)
	desenho.draw_circle(meio, RAIO + GROSSURA / 2.0 + 3.0, Color("141414"))
	var aceso := _cor_mostrada()
	for i in CORES.size():
		var angulo := -PI / 2.0 + i * PI / 2.0
		var cor := CORES[i].lightened(0.45) if i == aceso else CORES[i].darkened(0.55)
		desenho.draw_arc(meio, RAIO, angulo - PI / 4.0 + 0.12, angulo + PI / 4.0 - 0.12, 16, cor, GROSSURA)
	desenho.draw_circle(meio, RAIO - GROSSURA / 2.0 - 2.0, Color("141414"))
	var fonte := desenho.get_theme_default_font()
	var texto := "OUÇA" if _mostrando else "SUA VEZ"
	var cor_texto := COR_TEXTO if _mostrando else COR_ALVO
	desenho.draw_string(fonte, Vector2(0, desenho.size.y - 2.0), "%s - %d CORES" % [texto, _sequencia.size()], HORIZONTAL_ALIGNMENT_CENTER, desenho.size.x, 8, cor_texto)
