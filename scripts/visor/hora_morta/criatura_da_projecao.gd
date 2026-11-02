class_name CriaturaDaProjecao
extends Node3D

signal tocou_o_jogador

enum Estado { RONDA, CACA, PARADA }

@export var velocidade_da_ronda: float = 0.9
@export var velocidade_da_caca: float = 2.3
@export var velocidade_da_fuga: float = 1.7
@export var alcance_da_visao: float = 14.0
@export var distancia_do_toque: float = 0.85
@export var metros_por_passo: float = 0.8
@export var quadros_por_segundo: float = 7.0
@export var segundos_parada_num_ponto: float = 1.5
@export var segundos_entre_decisoes: float = 0.4
@export var atracao_normal: float = 0.5
@export var atracao_com_ruido: float = 4.0
@export var segundos_lembrando_o_ruido: float = 15.0
@export var distancia_minima_ao_voltar: float = 18.0
@export var distancia_ao_aparecer: float = 2.6
@export var distancia_final_ao_aparecer: float = 1.15
@export var distancia_do_ataque: float = 0.6
@export var tremor_do_quadro: float = 0.025

var estado := Estado.RONDA
var em_fuga := false
var grafo: GrafoDaNave
var _lugar := Vector3.ZERO
var _rota := PackedVector3Array()
var _ponto_atual := ""
var _ponto_anterior := ""
var _lugar_do_jogador := Vector3.ZERO
var _jogador_exposto := false
var _lugar_do_ruido := Vector3.ZERO
var _tempo_do_ruido := 0.0
var _ate_decidir := 0.0
var _espera := 0.0
var _ate_o_quadro := 0.0
var _andado_desde_o_passo := 0.0
var _quadro := 0
var _existe := false

@onready var imagem: Sprite3D = $Imagem
@onready var passos: AudioStreamPlayer3D = $Passos


func _ready() -> void:
	imagem.visible = false


func preparar(novo_grafo: GrafoDaNave, ponto: String) -> void:
	grafo = novo_grafo
	_ir_para_o_ponto(ponto)


func existir(na_luz: bool) -> void:
	_existe = na_luz
	imagem.visible = na_luz


func existe() -> bool:
	return _existe


func lugar_real() -> Vector3:
	return _lugar


func notar_jogador(exposto: bool, lugar: Vector3) -> void:
	_jogador_exposto = exposto
	_lugar_do_jogador = lugar


func ouvir(lugar: Vector3) -> void:
	_lugar_do_ruido = lugar
	_tempo_do_ruido = segundos_lembrando_o_ruido


func parar() -> void:
	estado = Estado.PARADA
	_rota = PackedVector3Array()
	passos.stop()


func aparecer_perto(jogador: Vector3, lado_preferido: float, z_minimo: float, z_maximo: float) -> void:
	var z_preferido := jogador.z + lado_preferido * distancia_ao_aparecer
	var lado := lado_preferido if z_preferido >= z_minimo and z_preferido <= z_maximo else -lado_preferido
	_lugar = Vector3(0.0, 0.0, jogador.z + lado * distancia_ao_aparecer)
	_rota = PackedVector3Array([Vector3(0.0, 0.0, jogador.z + lado * distancia_final_ao_aparecer)])
	position = _lugar


func voltar_longe(jogador: Vector3) -> void:
	var opcoes: Array[String] = []
	for ponto: String in GrafoDaNave.PONTOS:
		if grafo.lugar(ponto).distance_to(jogador) >= distancia_minima_ao_voltar:
			opcoes.append(ponto)
	_ir_para_o_ponto(opcoes.pick_random() if not opcoes.is_empty() else "maq")


func atacar(jogador: Vector3) -> Vector3:
	estado = Estado.PARADA
	var direcao := _lugar - jogador
	direcao.y = 0.0
	direcao = direcao.normalized() if direcao.length() > 0.01 else Vector3.FORWARD
	_lugar = jogador + direcao * distancia_do_ataque
	_lugar.y = 0.0
	position = _lugar
	existir(true)
	passos.stop()
	return direcao


func _ir_para_o_ponto(ponto: String) -> void:
	_ponto_atual = ponto
	_ponto_anterior = ""
	_lugar = grafo.lugar(ponto)
	_rota = PackedVector3Array()
	_espera = segundos_parada_num_ponto
	position = _lugar
	estado = Estado.RONDA


func _physics_process(delta: float) -> void:
	if grafo == null:
		return
	_tempo_do_ruido = maxf(0.0, _tempo_do_ruido - delta)
	_ate_decidir -= delta
	if _ate_decidir <= 0.0:
		_ate_decidir = segundos_entre_decisoes
		_decidir()
	match estado:
		Estado.RONDA:
			_rondar(delta)
		Estado.CACA:
			_seguir_rota(velocidade_da_fuga if em_fuga else velocidade_da_caca, delta)
			_conferir_toque()
		Estado.PARADA:
			_seguir_rota(velocidade_da_ronda, delta, false)
	_avancar_quadro(delta)


func _decidir() -> void:
	if estado == Estado.PARADA:
		return
	if not _jogador_exposto:
		_desistir_da_caca()
		return
	var caminho := grafo.rota(grafo.mais_perto(_lugar), grafo.mais_perto(_lugar_do_jogador))
	if not em_fuga and grafo.comprimento_da_rota(caminho) > alcance_da_visao:
		_desistir_da_caca()
		return
	estado = Estado.CACA
	_rota = _pontos_da_caca(caminho)


func _desistir_da_caca() -> void:
	if estado != Estado.CACA:
		return
	estado = Estado.RONDA
	_ponto_atual = grafo.mais_perto(_lugar)
	_rota = PackedVector3Array([grafo.lugar(_ponto_atual)])


func _pontos_da_caca(caminho: PackedStringArray) -> PackedVector3Array:
	var pontos := PackedVector3Array()
	for ponto in caminho:
		pontos.append(grafo.lugar(ponto))
	if pontos.size() >= 2 and _esta_entre(_lugar, pontos[0], pontos[1]):
		pontos.remove_at(0)
	if pontos.size() >= 2 and _esta_entre(_lugar_do_jogador, pontos[pontos.size() - 1], pontos[pontos.size() - 2]):
		pontos.remove_at(pontos.size() - 1)
	if pontos.size() == 1 and _lugar.distance_to(_lugar_do_jogador) < _lugar.distance_to(pontos[0]):
		pontos.clear()
	pontos.append(Vector3(_lugar_do_jogador.x, 0.0, _lugar_do_jogador.z))
	return pontos


func _esta_entre(lugar: Vector3, a: Vector3, b: Vector3) -> bool:
	var trecho := b - a
	var parte := (lugar - a).dot(trecho)
	return parte > 0.0 and parte < trecho.length_squared()


func _rondar(delta: float) -> void:
	if _espera > 0.0:
		_espera -= delta
		return
	if _rota.is_empty():
		var atracao := _lugar_do_ruido if _tempo_do_ruido > 0.0 else _lugar_do_jogador
		var forca := atracao_com_ruido if _tempo_do_ruido > 0.0 else atracao_normal
		var proximo := grafo.proximo_na_ronda(_ponto_atual, _ponto_anterior, atracao, forca)
		_ponto_anterior = _ponto_atual
		_ponto_atual = proximo
		_rota = PackedVector3Array([grafo.lugar(proximo)])
	_seguir_rota(velocidade_da_ronda, delta)
	if _rota.is_empty():
		_espera = segundos_parada_num_ponto


func _seguir_rota(velocidade: float, delta: float, com_passos: bool = true) -> void:
	var restante := velocidade * delta
	while restante > 0.0 and not _rota.is_empty():
		var destino := _rota[0]
		var distancia := _lugar.distance_to(destino)
		if distancia > restante:
			_lugar = _lugar.move_toward(destino, restante)
			_contar_passo(restante, com_passos)
			return
		_lugar = destino
		_contar_passo(distancia, com_passos)
		restante -= distancia
		_rota.remove_at(0)


func _contar_passo(metros: float, com_passos: bool) -> void:
	if not com_passos:
		return
	_andado_desde_o_passo += metros
	if _andado_desde_o_passo >= metros_por_passo:
		_andado_desde_o_passo = 0.0
		passos.pitch_scale = randf_range(0.62, 0.74)
		passos.play()


func _conferir_toque() -> void:
	var diferenca := _lugar_do_jogador - _lugar
	diferenca.y = 0.0
	if _existe and diferenca.length() <= distancia_do_toque:
		tocou_o_jogador.emit()


func _avancar_quadro(delta: float) -> void:
	_ate_o_quadro -= delta
	if _ate_o_quadro > 0.0:
		return
	_ate_o_quadro = 1.0 / quadros_por_segundo
	position = _lugar
	_quadro = (_quadro + 1) % imagem.hframes
	imagem.frame = _quadro
	imagem.position.x = randf_range(-tremor_do_quadro, tremor_do_quadro)
	imagem.modulate.a = randf_range(0.82, 1.0)
