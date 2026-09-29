class_name LuzTremula
extends PointLight2D

@export var tremor: float = 0.08
@export var piscadas_por_segundo: float = 0.25
@export var duracao_piscada: float = 0.12

var _energia_base: float
var _tempo := 0.0
var _apagada_ate := 0.0
var _ruido := FastNoiseLite.new()
var _sorteio := RandomNumberGenerator.new()


func _ready() -> void:
	_energia_base = energy
	_ruido.frequency = 2.0
	_ruido.seed = int(global_position.x * 7.0 + global_position.y * 13.0)
	_sorteio.seed = _ruido.seed


func _process(delta: float) -> void:
	_tempo += delta
	if _tempo < _apagada_ate:
		energy = _energia_base * 0.1
		return
	if _sorteio.randf() < piscadas_por_segundo * delta:
		_apagada_ate = _tempo + duracao_piscada * _sorteio.randf_range(0.5, 2.0)
	energy = _energia_base * (1.0 + tremor * _ruido.get_noise_1d(_tempo * 20.0))
