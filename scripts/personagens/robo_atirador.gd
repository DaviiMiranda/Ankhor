class_name RoboAtirador
extends Robo

const CENA_RAIO := preload("res://cenas/sistemas/raio_atirado.tscn")
const ALTURA_DA_ARMA := Vector2(0, -4)
const ALTURA_DO_PEITO := Vector2(0, -26)
const COR_MIRA := Color(1.0, 0.25, 0.2, 0.55)
const COR_MIRA_TRAVADA := Color(1.0, 0.95, 0.9, 0.95)

@export_group("Tiro")
@export var distancia_de_tiro: float = 130.0
@export var distancia_ideal: float = 95.0
@export var alcance_da_mira: float = 220.0
@export var segundos_mirando: float = 0.7
@export var segundos_travado: float = 0.4
@export var segundos_de_recarga: float = 2.2

var _mirando := false
var _tempo_mirando := 0.0
var _recarga := 0.0
var _direcao_da_mira := Vector2.RIGHT

@onready var linha_da_mira: Line2D = $LinhaDaMira
@onready var som_carga: AudioStreamPlayer2D = $SomCarga
@onready var som_tiro: AudioStreamPlayer2D = $SomTiro


func _physics_process(delta: float) -> void:
	_recarga = maxf(_recarga - delta, 0.0)
	if grade != null:
		_atualizar_mira(delta)
	super(delta)


func _velocidade() -> float:
	if _mirando or _deve_manter_distancia():
		return 0.0
	return super()


func _deve_manter_distancia() -> bool:
	return estado == Estado.PERSEGUINDO and _gabriel != null \
			and global_position.distance_to(_gabriel.global_position) < distancia_ideal and _ve_o_jogador()


func _atualizar_mira(delta: float) -> void:
	if _mirando:
		_continuar_mira(delta)
	elif _pode_comecar_a_mirar():
		_comecar_a_mirar()
	_desenhar_mira()


func _pode_comecar_a_mirar() -> bool:
	return estado == Estado.PERSEGUINDO and _recarga <= 0.0 and _gabriel != null \
			and global_position.distance_to(_gabriel.global_position) <= distancia_de_tiro and _ve_o_jogador()


func _comecar_a_mirar() -> void:
	_mirando = true
	_tempo_mirando = 0.0
	_direcao_da_mira = global_position.direction_to(_gabriel.global_position)
	som_carga.play()


func _continuar_mira(delta: float) -> void:
	if estado == Estado.ATORDOADO or not Vida.esta_viva() or _gabriel.escondido:
		_cancelar_mira()
		return
	_tempo_mirando += delta
	if _tempo_mirando < segundos_mirando:
		_direcao_da_mira = global_position.direction_to(_gabriel.global_position)
	direcao_olhar = _direcao_da_mira
	if _tempo_mirando >= segundos_mirando + segundos_travado:
		_atirar()


func _cancelar_mira() -> void:
	_mirando = false
	som_carga.stop()


func _atirar() -> void:
	_mirando = false
	_recarga = segundos_de_recarga
	var raio := CENA_RAIO.instantiate() as RaioAtirado
	get_parent().add_child(raio)
	raio.disparar(global_position + ALTURA_DA_ARMA, _direcao_da_mira)
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
	linha_da_mira.add_point(ALTURA_DO_PEITO + _direcao_da_mira * _alcance_livre())


func _alcance_livre() -> float:
	var de := global_position + ALTURA_DA_ARMA
	var consulta := PhysicsRayQueryParameters2D.create(de, de + _direcao_da_mira * alcance_da_mira, CAMADA_PAREDES)
	var batida := get_world_2d().direct_space_state.intersect_ray(consulta)
	if batida.is_empty():
		return alcance_da_mira
	return de.distance_to(batida["position"])
