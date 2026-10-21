class_name OndaAncora
extends Node2D

signal revelou(posicao: Vector2)

const COR := Color(0.38, 0.89, 0.93)
const ALTURA_DO_RAIO := Vector2(0, -4)

@export var periodo: float = 2.4
@export var inicio: float = 0.25
@export var fim: float = 0.8
@export var raio_inicial: float = 24.0
@export var raio_final: float = 440.0
@export var achatamento: float = 0.5
@export var largura_faixa: float = 16.0
@export var ativa := false

var _tempo := 0.0
var _revelou_neste_ciclo := false


func _ready() -> void:
	material = CanvasItemMaterial.new()
	(material as CanvasItemMaterial).light_mode = CanvasItemMaterial.LIGHT_MODE_UNSHADED
	(material as CanvasItemMaterial).blend_mode = CanvasItemMaterial.BLEND_MODE_ADD


func _process(delta: float) -> void:
	_tempo += delta
	queue_redraw()
	var fase := fposmod(_tempo / periodo, 1.0)
	if fase < inicio:
		_revelou_neste_ciclo = false
	if not ativa or fase < inicio or fase > fim or _revelou_neste_ciclo:
		return
	var gabriel := get_tree().get_first_node_in_group("jogador") as Gabriel
	if gabriel == null or gabriel.escondido:
		return
	if absf(distancia_no_chao(gabriel.global_position) - raio_agora()) > largura_faixa:
		return
	if _linha_livre(gabriel.global_position):
		_revelou_neste_ciclo = true
		revelou.emit(gabriel.global_position)


func progresso() -> float:
	return (fposmod(_tempo / periodo, 1.0) - inicio) / (fim - inicio)


func raio_agora() -> float:
	return lerpf(raio_inicial, raio_final, clampf(progresso(), 0.0, 1.0))


func distancia_no_chao(ponto: Vector2) -> float:
	var para := ponto - global_position
	return Vector2(para.x, para.y / achatamento).length()


func _linha_livre(ate: Vector2) -> bool:
	var consulta := PhysicsRayQueryParameters2D.create(global_position + ALTURA_DO_RAIO, ate + ALTURA_DO_RAIO, Robo.CAMADA_PAREDES)
	return get_world_2d().direct_space_state.intersect_ray(consulta).is_empty()


func _draw() -> void:
	var u := progresso()
	if not ativa or u < 0.0 or u > 1.0:
		return
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(1.0, achatamento))
	var cor := Color(COR, 0.55 * (1.0 - u))
	draw_arc(Vector2.ZERO, raio_agora(), 0.0, TAU, 72, cor, 2.0 / achatamento)
	draw_set_transform(Vector2.ZERO)
