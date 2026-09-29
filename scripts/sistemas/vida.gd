extends Node

signal mudou(vida: int)
signal dano_recebido(origem: Vector2)
signal morreu

const MAXIMA := 3

@export var segundos_invulneravel: float = 1.5

var vida := MAXIMA
var _invulneravel_ate := 0.0


func limpar() -> void:
	vida = MAXIMA
	_invulneravel_ate = 0.0
	mudou.emit(vida)


func esta_viva() -> bool:
	return vida > 0


func esta_invulneravel() -> bool:
	return _agora() < _invulneravel_ate


func receber_dano(quantidade: int, origem: Vector2) -> bool:
	if not esta_viva() or esta_invulneravel():
		return false
	vida = maxi(vida - quantidade, 0)
	_invulneravel_ate = _agora() + segundos_invulneravel
	mudou.emit(vida)
	dano_recebido.emit(origem)
	if vida == 0:
		morreu.emit()
	return true


func _agora() -> float:
	return Time.get_ticks_msec() / 1000.0
