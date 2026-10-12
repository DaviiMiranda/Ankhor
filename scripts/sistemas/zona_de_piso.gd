@tool
class_name ZonaDePiso
extends Node2D

const GRUPO := "zonas_de_piso"
const COR_NO_EDITOR := Color(1.0, 0.6, 0.2, 0.15)

@export var tamanho := Vector2(640, 60):
	set(valor):
		tamanho = valor
		queue_redraw()
@export var fator_ruido: float = 1.0
@export var nome_piso: String = "lajota"


func _ready() -> void:
	add_to_group(GRUPO)


func contem(ponto: Vector2) -> bool:
	return Rect2(global_position, tamanho).has_point(ponto)


static func fator_em(arvore: SceneTree, ponto: Vector2) -> float:
	for no in arvore.get_nodes_in_group(GRUPO):
		var zona := no as ZonaDePiso
		if zona and zona.contem(ponto):
			return zona.fator_ruido
	return 1.0


func _draw() -> void:
	if Engine.is_editor_hint():
		draw_rect(Rect2(Vector2.ZERO, tamanho), COR_NO_EDITOR)
