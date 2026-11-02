class_name LampadaDaNave
extends OmniLight3D

enum Estado { ACESA, QUEBRADA, MORTA }

const BRILHO_DO_VIDRO := 2.2
const COR_DO_ALARME := Color(1.0, 0.1, 0.06)
const SEGUNDOS_APAGADA_MIN := 2.5
const SEGUNDOS_APAGADA_MAX := 7.0
const SEGUNDOS_PISCANDO_MIN := 0.06
const SEGUNDOS_PISCANDO_MAX := 0.22

var estado := Estado.ACESA
var alcance := 2.0
var centro_local := Vector3.ZERO
var materiais_do_vidro: Array[StandardMaterial3D] = []
var _com_energia := true
var _piscando := false
var _em_alarme := false
var _ate_mudar := 0.0
var _cores_normais: Dictionary = {}


func _ready() -> void:
	_ate_mudar = randf_range(SEGUNDOS_APAGADA_MIN, SEGUNDOS_APAGADA_MAX)
	_guardar_cor(self)
	for filho in get_children():
		if filho is OmniLight3D:
			_guardar_cor(filho)
	_atualizar()


func _process(delta: float) -> void:
	if estado != Estado.QUEBRADA or not _com_energia or _em_alarme:
		return
	_ate_mudar -= delta
	if _ate_mudar > 0.0:
		return
	_piscando = not _piscando
	if _piscando:
		_ate_mudar = randf_range(SEGUNDOS_PISCANDO_MIN, SEGUNDOS_PISCANDO_MAX)
	else:
		_ate_mudar = randf_range(SEGUNDOS_APAGADA_MIN, SEGUNDOS_APAGADA_MAX)
	_atualizar()


func ilumina(lugar: Vector3) -> bool:
	if not visible:
		return false
	var diferenca := lugar - to_global(centro_local)
	diferenca.y = 0.0
	return diferenca.length() <= alcance


func cortar_energia() -> void:
	_com_energia = false
	_atualizar()


func religar() -> void:
	_com_energia = true
	_atualizar()


func acender_de_vez() -> void:
	estado = Estado.ACESA
	_atualizar()


func definir_alarme(ligado: bool) -> void:
	_em_alarme = ligado
	for luz: OmniLight3D in _cores_normais:
		luz.light_color = COR_DO_ALARME if ligado else _cores_normais[luz]
	for material in materiais_do_vidro:
		material.emission = COR_DO_ALARME if ligado else material.albedo_color / 0.4
	_atualizar()


func _guardar_cor(luz: OmniLight3D) -> void:
	_cores_normais[luz] = luz.light_color


func _atualizar() -> void:
	var funcionando := estado == Estado.ACESA or (estado == Estado.QUEBRADA and _piscando)
	var acesa := _com_energia and (funcionando or _em_alarme)
	visible = acesa
	for material in materiais_do_vidro:
		material.emission_energy_multiplier = BRILHO_DO_VIDRO if acesa else 0.0
