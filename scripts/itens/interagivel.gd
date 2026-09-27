@tool
class_name Interagivel
extends Area2D

const GRUPO_PERTO := "interagiveis_perto"

@export var texto_acao: String = "Interagir"
@export var altura_aviso: float = 18.0


func _ready() -> void:
	if Engine.is_editor_hint():
		return
	body_entered.connect(_ao_entrar)
	body_exited.connect(_ao_sair)


func pode_interagir() -> bool:
	return true


func interagir() -> void:
	pass


func _ao_entrar(corpo: Node2D) -> void:
	if corpo is Gabriel:
		add_to_group(GRUPO_PERTO)


func _ao_sair(corpo: Node2D) -> void:
	if corpo is Gabriel:
		remove_from_group(GRUPO_PERTO)


static func mais_perto(arvore: SceneTree, ponto: Vector2) -> Interagivel:
	var melhor: Interagivel = null
	var menor_distancia := INF
	for no in arvore.get_nodes_in_group(GRUPO_PERTO):
		var alvo := no as Interagivel
		if alvo == null or not alvo.pode_interagir():
			continue
		var d := ponto.distance_squared_to(alvo.global_position)
		if d < menor_distancia:
			menor_distancia = d
			melhor = alvo
	return melhor
