class_name VisivelComMarca
extends Node2D

const GRUPO_LUZ_QUE_REVELA := "luz_que_revela"

@export var marca: String = "energia"
@export var revela_quem_passa := false
@export var piscadas_ao_acender: int = 3

var _animacao: Tween


func _ready() -> void:
	visible = Progresso.tem(marca)
	if revela_quem_passa:
		for filho in get_children():
			if filho is PointLight2D:
				filho.add_to_group(GRUPO_LUZ_QUE_REVELA)
	Progresso.mudou.connect(_ao_mudar)


func _ao_mudar(nova: String) -> void:
	if nova == marca:
		_acender()


func _acender() -> void:
	if _animacao:
		_animacao.kill()
	_animacao = create_tween()
	for i in piscadas_ao_acender:
		_animacao.tween_callback(set_visible.bind(true))
		_animacao.tween_interval(0.06 + 0.04 * i)
		_animacao.tween_callback(set_visible.bind(false))
		_animacao.tween_interval(0.18)
	_animacao.tween_callback(set_visible.bind(true))
