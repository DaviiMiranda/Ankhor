class_name CamadaParalaxe
extends Node2D

@export var deslocamento_maximo: float = 4.0
@export var suavidade: float = 6.0

var _posicao_inicial: Vector2
var _posicao_atual: Vector2


func _ready() -> void:
	_posicao_inicial = position
	_posicao_atual = position


func _process(delta: float) -> void:
	var tamanho_tela := get_viewport_rect().size
	var mouse := get_viewport().get_mouse_position()

	var direcao := (mouse / tamanho_tela - Vector2(0.5, 0.5)) * 2.0
	direcao = direcao.clamp(Vector2(-1, -1), Vector2(1, 1))

	var alvo := _posicao_inicial - direcao * deslocamento_maximo
	_posicao_atual = _posicao_atual.lerp(alvo, 1.0 - exp(-suavidade * delta))
	position = _posicao_atual.round()
