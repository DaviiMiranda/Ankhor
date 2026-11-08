class_name RaioAtirado
extends Area2D

const ALTURA_DO_PEITO := -26.0
const COR_NUCLEO := Color(0.85, 1.0, 1.0)
const COR_BRILHO := Color(0.3, 0.8, 1.0)
const COMPRIMENTO := 14.0

@export var velocidade: float = 310.0
@export var segundos_de_vida: float = 1.6

var _direcao := Vector2.RIGHT
var _origem_do_dano := Vector2.ZERO
var _vivo := 0.0


func disparar(de: Vector2, direcao: Vector2) -> void:
	global_position = de
	_direcao = direcao.normalized()
	_origem_do_dano = de
	queue_redraw()


func _physics_process(delta: float) -> void:
	_vivo += delta
	if _vivo > segundos_de_vida:
		queue_free()
		return
	global_position += _direcao * velocidade * delta
	for corpo in get_overlapping_bodies():
		if corpo is Gabriel:
			if Vida.receber_dano(1, _origem_do_dano):
				queue_free()
				return
		elif corpo is StaticBody2D:
			queue_free()
			return


func _draw() -> void:
	var altura := Vector2(0, ALTURA_DO_PEITO)
	var cauda := altura - _direcao * COMPRIMENTO
	var ponta := altura + _direcao * COMPRIMENTO * 0.4
	draw_line(cauda, ponta, COR_BRILHO, 4.0)
	draw_line(altura - _direcao * COMPRIMENTO * 0.7, ponta, COR_NUCLEO, 2.0)
