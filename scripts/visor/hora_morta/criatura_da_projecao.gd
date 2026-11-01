class_name CriaturaDaProjecao
extends Node3D

signal tocou_o_jogador

enum Estado { RONDA, CACA, PARADA }

@export var velocidade_da_ronda: float = 0.9
@export var velocidade_da_caca: float = 2.3
@export var alcance_da_visao: float = 9.0
@export var distancia_do_toque: float = 0.85
@export var metros_por_passo: float = 0.8
@export var quadros_por_segundo: float = 7.0
@export var segundos_parada_na_ponta: float = 2.0
@export var limite_da_ronda: float = 11.0
@export var distancia_ao_aparecer: float = 2.6
@export var distancia_final_ao_aparecer: float = 1.15
@export var distancia_do_ataque: float = 0.6
@export var tremor_do_quadro: float = 0.025

var estado := Estado.RONDA
var _alvo_z := 0.0
var _z_real := 0.0
var _ate_o_quadro := 0.0
var _andado_desde_o_passo := 0.0
var _espera_na_ponta := 0.0
var _sentido_da_ronda := 1.0
var _quadro := 0
var _existe := false

@onready var imagem: Sprite3D = $Imagem
@onready var passos: AudioStreamPlayer3D = $Passos


func _ready() -> void:
	_z_real = position.z
	imagem.visible = false


func existir(na_luz: bool) -> void:
	_existe = na_luz
	imagem.visible = na_luz


func existe() -> bool:
	return _existe


func notar_jogador(jogador_na_luz: bool, jogador_z: float) -> void:
	if estado == Estado.PARADA:
		return
	var perto := absf(jogador_z - _z_real) <= alcance_da_visao
	estado = Estado.CACA if jogador_na_luz and perto else Estado.RONDA
	_alvo_z = jogador_z


func parar() -> void:
	estado = Estado.PARADA
	_alvo_z = _z_real
	passos.stop()


func aparecer_perto(jogador_z: float, lado_preferido: float) -> void:
	var cabe := absf(jogador_z + lado_preferido * distancia_ao_aparecer) <= limite_da_ronda
	var lado := lado_preferido if cabe else -lado_preferido
	_z_real = jogador_z + lado * distancia_ao_aparecer
	_alvo_z = jogador_z + lado * distancia_final_ao_aparecer
	position.z = _z_real


func voltar_a_ronda(jogador_z: float) -> void:
	_z_real = -limite_da_ronda * signf(jogador_z) if not is_zero_approx(jogador_z) else limite_da_ronda
	_sentido_da_ronda = -signf(_z_real)
	_espera_na_ponta = segundos_parada_na_ponta
	position.z = _z_real
	estado = Estado.RONDA


func atacar(jogador_z: float, lado: float) -> void:
	estado = Estado.PARADA
	_z_real = jogador_z + lado * distancia_do_ataque
	position.z = _z_real
	existir(true)
	passos.stop()


func _physics_process(delta: float) -> void:
	match estado:
		Estado.RONDA:
			_andar_na_ronda(delta)
		Estado.CACA:
			_andar_ate(_alvo_z, velocidade_da_caca, delta)
			_conferir_toque()
		Estado.PARADA:
			_z_real = move_toward(_z_real, _alvo_z, velocidade_da_ronda * delta)
	_avancar_quadro(delta)


func _andar_na_ronda(delta: float) -> void:
	if _espera_na_ponta > 0.0:
		_espera_na_ponta -= delta
		return
	var destino := limite_da_ronda * _sentido_da_ronda
	_andar_ate(destino, velocidade_da_ronda, delta)
	if is_equal_approx(_z_real, destino):
		_sentido_da_ronda = -_sentido_da_ronda
		_espera_na_ponta = segundos_parada_na_ponta
	_conferir_toque()


func _andar_ate(destino: float, velocidade: float, delta: float) -> void:
	var antes := _z_real
	_z_real = move_toward(_z_real, destino, velocidade * delta)
	_andado_desde_o_passo += absf(_z_real - antes)
	if _andado_desde_o_passo >= metros_por_passo:
		_andado_desde_o_passo = 0.0
		passos.pitch_scale = randf_range(0.62, 0.74)
		passos.play()


func _conferir_toque() -> void:
	if _existe and absf(_alvo_z - _z_real) <= distancia_do_toque and estado == Estado.CACA:
		tocou_o_jogador.emit()


func _avancar_quadro(delta: float) -> void:
	_ate_o_quadro -= delta
	if _ate_o_quadro > 0.0:
		return
	_ate_o_quadro = 1.0 / quadros_por_segundo
	position.z = _z_real
	_quadro = (_quadro + 1) % imagem.hframes
	imagem.frame = _quadro
	imagem.position.x = randf_range(-tremor_do_quadro, tremor_do_quadro)
	imagem.modulate.a = randf_range(0.82, 1.0)
