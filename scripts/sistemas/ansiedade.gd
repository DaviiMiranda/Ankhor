class_name Ansiedade
extends Node

signal mudou(atual: float, maxima: float)

@export var alcance_perigo: float = 240.0
@export var crescimento_por_segundo: float = 0.48
@export var recuperacao_por_segundo: float = 0.2
@export var multiplicador_maximo_estamina: float = 1.8

var valor := 0.0


func atualizar(posicao_jogador: Vector2, delta: float) -> void:
	var intensidade_perigo := _calcular_intensidade_perigo(posicao_jogador)
	var valor_anterior := valor
	if intensidade_perigo > 0.0:
		valor = minf(valor + crescimento_por_segundo * intensidade_perigo * delta, 1.0)
	else:
		valor = maxf(valor - recuperacao_por_segundo * delta, 0.0)
	if not is_equal_approx(valor, valor_anterior):
		mudou.emit(valor, 1.0)


func multiplicador_consumo_estamina() -> float:
	return lerpf(1.0, multiplicador_maximo_estamina, valor)


func _calcular_intensidade_perigo(posicao_jogador: Vector2) -> float:
	var maior_perigo := 0.0
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Node2D
		if robo == null:
			continue
		var distancia := posicao_jogador.distance_to(robo.global_position)
		var perigo := clampf(1.0 - distancia / alcance_perigo, 0.0, 1.0)
		maior_perigo = maxf(maior_perigo, perigo)
	return maior_perigo
