class_name Fadiga
extends Node2D

signal mudou(estamina_atual: float, estamina_maxima: float)
signal exaustao_iniciada
signal exaustao_terminada
signal ofegante

@export var estamina_maxima: float = 100.0
@export var consumo_por_segundo: float = 12.5
@export var regeneracao_parado_por_segundo: float = 25.0
@export var regeneracao_andando_por_segundo: float = 12.5
@export var duracao_exaustao: float = 3.0
@export var fracao_para_voltar_a_correr: float = 0.3
@export var intervalo_som_ofegante: float = 1.0
@export var som_ofegante: AudioStream
@export var fracao_cansado: float = 0.3
@export var intervalo_som_cansado: float = 1.0
@export var volume_exausto_db: float = -6.0
@export var volume_cansado_db: float = -16.0
@export var intervalo_som_em_fuga: float = 1.1
@export var volume_em_fuga_db: float = -9.0
@export var variacao_tom_em_fuga: float = 0.08

var estamina := 100.0
var tempo_exaustao := 0.0
var em_fuga := false
var recuperando_folego := false
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
	elif em_fuga:
		_respirar_em_fuga(delta)
	elif esta_cansado():
		_respirar_cansado(delta)


func esta_exausto() -> bool:
	return tempo_exaustao > 0.0


func esta_cansado() -> bool:
	return estamina < estamina_maxima * fracao_cansado


func pode_correr() -> bool:
	return not esta_exausto() and not recuperando_folego and estamina > 0.0


func consumir(delta: float, multiplicador: float = 1.0) -> void:
	if esta_exausto():
		return
	estamina = maxf(estamina - consumo_por_segundo * delta * multiplicador, 0.0)
	mudou.emit(estamina, estamina_maxima)
	if estamina == 0.0:
		tempo_exaustao = duracao_exaustao
		recuperando_folego = true
		_tempo_ultimo_ofegante = intervalo_som_ofegante
		exaustao_iniciada.emit()


func regenerar(delta: float, parado: bool) -> void:
	if esta_exausto():
		return
	if estamina >= estamina_maxima:
		return
	var taxa := regeneracao_parado_por_segundo if parado else regeneracao_andando_por_segundo
	estamina = minf(estamina + taxa * delta, estamina_maxima)
	if estamina >= estamina_maxima * fracao_para_voltar_a_correr:
		recuperando_folego = false
	mudou.emit(estamina, estamina_maxima)


func reiniciar() -> void:
	estamina = estamina_maxima
	tempo_exaustao = 0.0
	recuperando_folego = false
	_tempo_ultimo_ofegante = 0.0
	mudou.emit(estamina, estamina_maxima)


func _tocar_som_ofegante(delta: float) -> void:
	_tempo_ultimo_ofegante += delta
	if _tempo_ultimo_ofegante >= intervalo_som_ofegante:
		_tempo_ultimo_ofegante = 0.0
		ofegante.emit()
		_tocar_respiracao(volume_exausto_db)


func _respirar_cansado(delta: float) -> void:
	_tempo_ultimo_ofegante += delta
	if _tempo_ultimo_ofegante >= intervalo_som_cansado:
		_tempo_ultimo_ofegante = 0.0
		_tocar_respiracao(volume_cansado_db)


func _respirar_em_fuga(delta: float) -> void:
	_tempo_ultimo_ofegante += delta
	if _tempo_ultimo_ofegante >= intervalo_som_em_fuga:
		_tempo_ultimo_ofegante = 0.0
		_tocar_respiracao(volume_em_fuga_db, 1.0 + randf_range(-variacao_tom_em_fuga, variacao_tom_em_fuga))


func _tocar_respiracao(volume_db: float, tom: float = 1.0) -> void:
	if reprodutor_ofegante and reprodutor_ofegante.stream:
		reprodutor_ofegante.volume_db = volume_db
		reprodutor_ofegante.pitch_scale = tom
		reprodutor_ofegante.play()
