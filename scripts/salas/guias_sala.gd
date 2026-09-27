@tool
extends Node2D


func _ready() -> void:
	visible = Engine.is_editor_hint()


func _draw() -> void:
	var sala := get_parent() as Sala
	if sala == null:
		return
	var altura := sala.altura
	draw_rect(Rect2(0, 0, sala.largura, altura), Color(1, 0.85, 0.2, 0.9), false, 1.0)
	for x in range(320, sala.largura, 320):
		draw_line(Vector2(x, 0), Vector2(x, altura), Color(1, 0.85, 0.2, 0.35), 1.0)
	for y in range(180, altura, 180):
		draw_line(Vector2(0, y), Vector2(sala.largura, y), Color(1, 0.85, 0.2, 0.35), 1.0)
	var faixa := Rect2(sala.margem_lados, sala.chao_fundo,
			sala.largura - 2 * sala.margem_lados, sala.chao_frente - sala.chao_fundo)
	draw_rect(faixa, Color(0.3, 0.7, 1, 0.12), true)
	draw_rect(faixa, Color(0.3, 0.7, 1, 0.9), false, 1.0)
