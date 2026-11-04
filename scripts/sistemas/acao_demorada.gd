class_name AcaoDemorada
extends Node2D

const ALTURA_BARRA := -56.0
const LARGURA_BARRA := 24.0
const COR_FUNDO := Color(0.05, 0.08, 0.1)
const COR_PROGRESSO := Color(0.95, 0.8, 0.35)
const INTERVALO_RUIDO := 1.0

var _alvo: Interagivel
var _total := 0.0
var _feito := 0.0
var _proximo_ruido := 0.0


func _ready() -> void:
	z_index = 20
	Vida.dano_recebido.connect(_ao_receber_dano.unbind(1))
	set_physics_process(false)


func ativa() -> bool:
	return _alvo != null


func comecar(alvo: Interagivel) -> void:
	_alvo = alvo
	_total = alvo.segundos_de_espera()
	_feito = 0.0
	_proximo_ruido = 0.0
	_gabriel().andar_sozinho(Vector2.ZERO)
	set_physics_process(true)
	queue_redraw()


func _physics_process(delta: float) -> void:
	if not is_instance_valid(_alvo) or not Input.is_action_pressed("interagir"):
		_parar()
		return
	_feito += delta
	_proximo_ruido -= delta
	if _proximo_ruido <= 0.0 and _alvo.ruido_ao_segurar > 0:
		_proximo_ruido = INTERVALO_RUIDO
		Robo.fazer_barulho(get_tree(), _gabriel().global_position, _alvo.ruido_ao_segurar)
	queue_redraw()
	if _feito >= _total:
		var alvo := _alvo
		_parar()
		alvo.interagir()


func _ao_receber_dano() -> void:
	if _alvo:
		_parar()


func _parar() -> void:
	_alvo = null
	set_physics_process(false)
	_gabriel().devolver_controle()
	queue_redraw()


func _gabriel() -> Gabriel:
	return get_parent() as Gabriel


func _draw() -> void:
	if _alvo == null:
		return
	var inicio := Vector2(-LARGURA_BARRA / 2.0, ALTURA_BARRA)
	draw_rect(Rect2(inicio - Vector2.ONE, Vector2(LARGURA_BARRA + 2, 4)), COR_FUNDO)
	draw_rect(Rect2(inicio, Vector2(LARGURA_BARRA * clampf(_feito / _total, 0.0, 1.0), 2)), COR_PROGRESSO)
