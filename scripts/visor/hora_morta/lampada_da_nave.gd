class_name LampadaDaNave
extends OmniLight3D

enum Estado { ACESA, QUEBRADA, MORTA }

const ALCANCE_NO_CORREDOR := 1.7
const BRILHO_DO_VIDRO := 2.2
const SEGUNDOS_APAGADA_MIN := 2.5
const SEGUNDOS_APAGADA_MAX := 7.0
const SEGUNDOS_PISCANDO_MIN := 0.06
const SEGUNDOS_PISCANDO_MAX := 0.22

var estado := Estado.ACESA
var materiais_do_vidro: Array[StandardMaterial3D] = []
var _com_energia := true
var _piscando := false
var _ate_mudar := 0.0


func _ready() -> void:
	_ate_mudar = randf_range(SEGUNDOS_APAGADA_MIN, SEGUNDOS_APAGADA_MAX)
	_atualizar()


func _process(delta: float) -> void:
	if estado != Estado.QUEBRADA or not _com_energia:
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
	return visible and absf(lugar.z - global_position.z) <= ALCANCE_NO_CORREDOR


func cortar_energia() -> void:
	_com_energia = false
	_atualizar()


func religar() -> void:
	_com_energia = true
	_atualizar()


func _atualizar() -> void:
	var acesa := _com_energia and (estado == Estado.ACESA or (estado == Estado.QUEBRADA and _piscando))
	visible = acesa
	for material in materiais_do_vidro:
		material.emission_energy_multiplier = BRILHO_DO_VIDRO if acesa else 0.0
