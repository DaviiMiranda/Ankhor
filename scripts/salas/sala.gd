@tool
class_name Sala
extends Node2D

@export var id: String = ""
@export var duracao_entrada: float = 1.0

@export_group("Tamanho")
@export var largura: int = 960:
	set(valor):
		largura = valor
		_redesenhar_guias()
@export var altura: int = 180:
	set(valor):
		altura = valor
		_redesenhar_guias()
@export var chao_fundo: int = 120:
	set(valor):
		chao_fundo = valor
		_redesenhar_guias()
@export var chao_frente: int = 176:
	set(valor):
		chao_frente = valor
		_redesenhar_guias()
@export var margem_lados: int = 20:
	set(valor):
		margem_lados = valor
		_redesenhar_guias()
@export var criar_limites: bool = true

@onready var escuro: ColorRect = get_node_or_null("Transicao/Escuro")


func _ready() -> void:
	if Engine.is_editor_hint():
		return
	if criar_limites:
		_criar_limites()
	_posicionar_no_checkpoint()
	_ajustar_camera()
	if escuro:
		escuro.color.a = 1.0
		var tween := create_tween()
		tween.tween_property(escuro, "color:a", 0.0, duracao_entrada)


func _criar_limites() -> void:
	var corpo := StaticBody2D.new()
	corpo.name = "LimitesAutomaticos"
	var grossura := 40.0
	var larg := float(largura)
	var paredes := [
		[Vector2(larg / 2, chao_fundo - grossura / 2), Vector2(larg + 2 * grossura, grossura)],
		[Vector2(larg / 2, chao_frente + grossura / 2), Vector2(larg + 2 * grossura, grossura)],
		[Vector2(margem_lados - grossura / 2, altura / 2.0), Vector2(grossura, altura * 2)],
		[Vector2(larg - margem_lados + grossura / 2, altura / 2.0), Vector2(grossura, altura * 2)],
	]
	for p in paredes:
		var forma := CollisionShape2D.new()
		var ret := RectangleShape2D.new()
		ret.size = p[1]
		forma.shape = ret
		forma.position = p[0]
		corpo.add_child(forma)
	add_child(corpo)


func _posicionar_no_checkpoint() -> void:
	var gabriel := get_node_or_null("Objetos/Gabriel") as Node2D
	if gabriel and Checkpoints.tem_checkpoint_em(scene_file_path):
		gabriel.global_position = Checkpoints.posicao


func _ajustar_camera() -> void:
	var camera := get_node_or_null("Objetos/Gabriel/Camera2D") as Camera2D
	if camera:
		camera.limit_left = 0
		camera.limit_top = 0
		camera.limit_right = largura
		camera.limit_bottom = altura


func _redesenhar_guias() -> void:
	var guias := get_node_or_null("Guias") as CanvasItem
	if guias:
		guias.queue_redraw()
