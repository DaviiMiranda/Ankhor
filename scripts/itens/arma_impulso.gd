extends Node2D

const COR_ONDA := Color(0.35, 0.92, 1.0)
const ALTURA_DO_PEITO := -22.0

@export var raio: float = 120.0
@export var velocidade_maxima: float = 400.0
@export var velocidade_minima: float = 170.0
@export var segundos_atordoado: float = 0.9
@export var segundos_entre_disparos: float = 0.45
@export var segundos_por_carga: float = 7.0
@export var segundos_da_onda: float = 0.35
@export var energia_flash: float = 2.6

var item: Item

var _tempo_da_onda := -1.0
var _tempo_desde_disparo := 99.0
var _tempo_de_recarga := 0.0

@onready var flash: PointLight2D = $Flash
@onready var som: AudioStreamPlayer = $Som


func _ready() -> void:
	var estado := Inventario.estado_de(item.id)
	if not estado.get("iniciada", false):
		estado["iniciada"] = true
		Inventario.definir_unidades(item, item.maximo_unidades)


func _process(delta: float) -> void:
	_tempo_desde_disparo += delta
	_recarregar(delta)
	if _tempo_da_onda >= 0.0:
		_tempo_da_onda += delta
		if _tempo_da_onda > segundos_da_onda:
			_tempo_da_onda = -1.0
		queue_redraw()


func usar() -> void:
	if _tempo_desde_disparo < segundos_entre_disparos:
		return
	if not ModoCombate.ativo:
		var restantes := Inventario.unidades(item.id)
		if restantes <= 0:
			Inventario.aviso.emit("Sem carga na arma de impulso")
			return
		Inventario.definir_unidades(item, restantes - 1)
	_tempo_desde_disparo = 0.0
	_tempo_da_onda = 0.0
	som.play()
	_piscar()
	_afastar_robos()


func _afastar_robos() -> void:
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		var distancia := global_position.distance_to(robo.global_position)
		if distancia > raio:
			continue
		var forca := 1.0 - distancia / raio
		var para_longe := global_position.direction_to(robo.global_position)
		if distancia < 1.0:
			para_longe = Vector2.RIGHT
		robo.empurrar(para_longe, lerpf(velocidade_minima, velocidade_maxima, forca), segundos_atordoado)


func _recarregar(delta: float) -> void:
	var atuais := Inventario.unidades(item.id)
	if ModoCombate.ativo or atuais >= item.maximo_unidades:
		_tempo_de_recarga = 0.0
		return
	_tempo_de_recarga += delta
	if _tempo_de_recarga >= segundos_por_carga:
		_tempo_de_recarga = 0.0
		Inventario.definir_unidades(item, atuais + 1)


func _piscar() -> void:
	flash.energy = energia_flash
	create_tween().tween_property(flash, "energy", 0.0, segundos_da_onda)


func _draw() -> void:
	if _tempo_da_onda < 0.0:
		return
	var avanco := _tempo_da_onda / segundos_da_onda
	var tamanho := raio * (1.0 - pow(1.0 - avanco, 3.0))
	var cor := COR_ONDA
	cor.a = 1.0 - avanco
	var centro := Vector2(0, ALTURA_DO_PEITO)
	draw_set_transform(centro, 0.0, Vector2(1.0, 0.45))
	draw_arc(Vector2.ZERO, tamanho, 0.0, TAU, 48, cor, 2.0)
	draw_arc(Vector2.ZERO, tamanho * 0.7, 0.0, TAU, 40, Color(cor.r, cor.g, cor.b, cor.a * 0.5), 1.0)
