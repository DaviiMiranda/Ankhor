class_name RoboDeCena
extends Node2D

const CENA_RAIO := preload("res://cenas/sistemas/raio_atirado.tscn")
const ALTURA_DA_ARMA := Vector2(0, -4)
const ALTURA_DO_PEITO := Vector2(0, -26)
const COR_MIRA := Color(1.0, 0.25, 0.2, 0.55)
const COR_MIRA_TRAVADA := Color(1.0, 0.95, 0.9, 0.95)
const ALCANCE_DA_MIRA := 300.0
const ALCANCE_DO_TOQUE := Vector2(16, 12)
const SEGUNDOS_ENTRE_TIROS := 0.8

static var _proximo_tiro_livre := 0.0

@export var quadros: int = 8
@export var px_por_quadro: float = 4.0
@export var velocidade: float = 92.0
@export var velocidade_vertical: float = 26.0
@export var faixa: float = -1.0
@export var distancia_do_gabriel: float = 0.0
@export var distancia_maxima: float = 75.0
@export var velocidade_de_alcance: float = 130.0
@export var aparece_depois_de_x: float = -1.0

@export_group("Tiro")
@export var atira := false
@export var segundos_mirando: float = 0.5
@export var segundos_travado: float = 0.35
@export var recarga_minima: float = 0.9
@export var recarga_maxima: float = 1.5

var correndo := false
var _andado := 0.0
var _recarga := 0.0
var _mirando := false
var _tempo_mirando := 0.0
var _direcao := Vector2.RIGHT
var _gabriel: Gabriel

@onready var corpo: Sprite2D = $Corpo
@onready var olhos: Sprite2D = $Olhos
@onready var linha_da_mira: Line2D = $LinhaDaMira
@onready var som_carga: AudioStreamPlayer2D = $SomCarga
@onready var som_tiro: AudioStreamPlayer2D = $SomTiro


func _ready() -> void:
	_recarga = randf_range(recarga_minima, recarga_maxima)
	linha_da_mira.visible = false
	visible = aparece_depois_de_x < 0.0


func parar() -> void:
	correndo = false
	_cancelar_mira()


func _physics_process(delta: float) -> void:
	if not correndo:
		return
	_gabriel = get_tree().get_first_node_in_group("jogador") as Gabriel
	if _gabriel == null:
		return
	if not visible:
		if _gabriel.global_position.x < aparece_depois_de_x:
			return
		visible = true
		global_position.x = _gabriel.global_position.x - distancia_maxima - 20.0
	_andar(delta)
	if atira:
		_atualizar_tiro(delta)


func _andar(delta: float) -> void:
	var alvo := _gabriel.global_position.x - distancia_do_gabriel
	var antes := global_position.x
	var ficou_para_tras := _gabriel.global_position.x - antes > distancia_maxima
	if alvo > antes:
		global_position.x = move_toward(antes, alvo, (velocidade_de_alcance if ficou_para_tras else velocidade) * delta)
	var altura := faixa if faixa >= 0.0 else _gabriel.global_position.y
	global_position.y = move_toward(global_position.y, altura, velocidade_vertical * delta)
	_andado += global_position.x - antes
	var quadro := int(_andado / px_por_quadro) % quadros
	corpo.frame = quadro
	olhos.frame = quadro
	var distancia := (_gabriel.global_position - global_position).abs()
	if distancia.x < ALCANCE_DO_TOQUE.x and distancia.y < ALCANCE_DO_TOQUE.y:
		Vida.receber_dano(1, global_position)


func _atualizar_tiro(delta: float) -> void:
	if _mirando:
		_continuar_mira(delta)
	else:
		_recarga -= delta
		var na_frente := _gabriel.global_position.x - global_position.x
		if _recarga <= 0.0 and na_frente > 0.0 and na_frente < ALCANCE_DA_MIRA and _agora() >= _proximo_tiro_livre:
			_comecar_a_mirar()
	_desenhar_mira()


func _comecar_a_mirar() -> void:
	_proximo_tiro_livre = _agora() + segundos_mirando + segundos_travado + SEGUNDOS_ENTRE_TIROS
	_mirando = true
	_tempo_mirando = 0.0
	som_carga.play()


func _continuar_mira(delta: float) -> void:
	_tempo_mirando += delta
	if _tempo_mirando < segundos_mirando:
		_direcao = global_position.direction_to(_gabriel.global_position)
	if _tempo_mirando >= segundos_mirando + segundos_travado:
		_atirar()


func _cancelar_mira() -> void:
	_mirando = false
	if is_node_ready():
		som_carga.stop()
		linha_da_mira.visible = false


func _atirar() -> void:
	_mirando = false
	_recarga = randf_range(recarga_minima, recarga_maxima)
	var raio := CENA_RAIO.instantiate() as RaioAtirado
	get_parent().add_child(raio)
	raio.disparar(global_position + ALTURA_DA_ARMA, _direcao)
	som_carga.stop()
	som_tiro.play()


func _desenhar_mira() -> void:
	linha_da_mira.visible = _mirando
	if not _mirando:
		return
	var travada := _tempo_mirando >= segundos_mirando
	linha_da_mira.default_color = COR_MIRA_TRAVADA if travada else COR_MIRA
	linha_da_mira.width = 2.0 if travada else 1.0
	linha_da_mira.clear_points()
	linha_da_mira.add_point(ALTURA_DO_PEITO)
	linha_da_mira.add_point(ALTURA_DO_PEITO + _direcao * ALCANCE_DA_MIRA)


func _agora() -> float:
	return Time.get_ticks_msec() / 1000.0
