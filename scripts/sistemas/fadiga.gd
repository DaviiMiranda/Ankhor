class_name Fadiga
extends Node2D

signal mudou(estamina_atual: float, estamina_maxima: float)
signal exaustao_iniciada
signal exaustao_terminada
signal ofegante

@export var estamina_maxima: float = 100.0
@export var consumo_por_segundo: float = 25.0
@export var regeneracao_parado_por_segundo: float = 25.0
@export var regeneracao_andando_por_segundo: float = 12.5
@export var duracao_exaustao: float = 3.0
@export var intervalo_som_ofegante: float = 1.0
@export var som_ofegante: AudioStream

var estamina := 100.0
var tempo_exaustao := 0.0
var _tempo_ultimo_ofegante := 0.0

@onready var reprodutor_ofegante: AudioStreamPlayer2D = $SomOfegante


func _ready() -> void:
	estamina = estamina_maxima
	if som_ofegante and reprodutor_ofegante:
		reprodutor_ofegante.stream = som_ofegante


func _physics_process(delta: float) -> void:
	if esta_exausto():
		tempo_exaustao = maxf(tempo_exaustao - delta, 0.0)
		_tocar_som_ofegante(delta)
		if tempo_exaustao == 0.0:
			exaustao_terminada.emit()
			mudou.emit(estamina, estamina_maxima)


func esta_exausto() -> bool:
	return tempo_exaustao > 0.0


func pode_correr() -> bool:
	return not esta_exausto() and estamina > 0.0


func consumir(delta: float) -> void:
	if esta_exausto():
		return
	estamina = maxf(estamina - consumo_por_segundo * delta, 0.0)
	mudou.emit(estamina, estamina_maxima)
	if estamina == 0.0:
		tempo_exaustao = duracao_exaustao
		_tempo_ultimo_ofegante = intervalo_som_ofegante
		exaustao_iniciada.emit()


func regenerar(delta: float, parado: bool) -> void:
	if esta_exausto():
		return
	if estamina >= estamina_maxima:
		return
	var taxa := regeneracao_parado_por_segundo if parado else regeneracao_andando_por_segundo
	estamina = minf(estamina + taxa * delta, estamina_maxima)
	mudou.emit(estamina, estamina_maxima)


func reiniciar() -> void:
	estamina = estamina_maxima
	tempo_exaustao = 0.0
	_tempo_ultimo_ofegante = 0.0
	mudou.emit(estamina, estamina_maxima)


func _tocar_som_ofegante(delta: float) -> void:
	_tempo_ultimo_ofegante += delta
	if _tempo_ultimo_ofegante >= intervalo_som_ofegante:
		_tempo_ultimo_ofegante = 0.0
		ofegante.emit()
		if reprodutor_ofegante and reprodutor_ofegante.stream:
			reprodutor_ofegante.play()
