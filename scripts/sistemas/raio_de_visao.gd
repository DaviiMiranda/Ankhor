class_name RaioDeVisao
extends CanvasLayer

@export var raio_livre: float = 56.0
@export var raio_escuro: float = 96.0
@export var deslocamento_do_centro: Vector2 = Vector2(0, -24)

var _alvo: Node2D

@onready var tela: ColorRect = $Tela


func _process(_delta: float) -> void:
	if not is_instance_valid(_alvo):
		_alvo = get_tree().get_first_node_in_group("jogador") as Node2D
		if _alvo == null:
			return
	var transformada_da_camera := get_viewport().get_canvas_transform()
	var zoom := transformada_da_camera.x.length()
	var material := tela.material as ShaderMaterial
	material.set_shader_parameter("centro", transformada_da_camera * (_alvo.global_position + deslocamento_do_centro))
	material.set_shader_parameter("raio_livre", raio_livre * zoom)
	material.set_shader_parameter("raio_escuro", raio_escuro * zoom)
	material.set_shader_parameter("tamanho", tela.size)
	material.set_shader_parameter("passo", zoom)
