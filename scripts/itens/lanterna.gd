extends Node2D

const CORPO_DO_DONO := Rect2(-8.0, -24.0, 16.0, 44.0)

@export var duracao: float = 240.0
@export var energia_feixe: float = 1.3
@export var energia_nas_paredes: float = 1.0
@export var energia_halo: float = 0.45
@export var carga_fraca: float = 0.15
@export var distancia_da_lente: float = 3.75
@export var altura_da_sombra: float = 20.0

var item: Item
var _estado: Dictionary
var _tempo := 0.0

@onready var corpo: Sprite2D = $Corpo
@onready var feixe: PointLight2D = $Feixe
@onready var feixe_paredes: PointLight2D = $FeixeParedes
@onready var halo: PointLight2D = $Halo
@onready var clique: AudioStreamPlayer = $Clique


func _ready() -> void:
	_estado = Inventario.estado_de(item.id if item else "lanterna")
	if not _estado.has("carga"):
		_estado["carga"] = 1.0
	if not _estado.has("aceso"):
		_estado["aceso"] = false
	_atualizar_luz()
	var dono := _dono()
	if dono:
		dono.tira_especial_mudou.connect(_apontar)


func usar() -> void:
	if _estado["carga"] > 0.0:
		_estado["aceso"] = not _estado["aceso"]
		clique.play()
	_atualizar_luz()


func ao_desequipar() -> void:
	_estado["aceso"] = false


func _dono() -> Gabriel:
	return get_parent().get_parent() as Gabriel


func _process(delta: float) -> void:
	_tempo += delta
	var dono := _dono()
	var infinita := dono != null and dono.lanterna_infinita
	if _estado["aceso"] and not infinita:
		_estado["carga"] = maxf(_estado["carga"] - delta / duracao, 0.0)
		if _estado["carga"] <= 0.0:
			_estado["aceso"] = false
	_apontar()
	_atualizar_luz()


func _apontar() -> void:
	var dono := _dono()
	if dono:
		var angulo := dono.direcao_olhar.angle()
		var mao := to_local(dono.to_global(dono.posicao_da_mao()))
		var direcao := Vector2.from_angle(angulo)
		var lente := mao + direcao * distancia_da_lente
		var saida_do_feixe := lente + direcao * _distancia_ate_sair_do_corpo(lente, direcao)
		corpo.position = mao
		corpo.rotation = angulo
		corpo.flip_v = dono.direcao_olhar.x < 0.0
		corpo.visible = not dono.vista.ends_with("costas") and not dono.tira_especial
		corpo.self_modulate = dono.sprite.self_modulate
		corpo.modulate.a = dono.sprite.modulate.a
		feixe_paredes.position = saida_do_feixe
		halo.position = lente
		feixe.position = Vector2(0, altura_da_sombra)
		feixe.rotation = angulo
		feixe.offset = (saida_do_feixe - feixe.position).rotated(-feixe.rotation)
		feixe_paredes.rotation = angulo


func _distancia_ate_sair_do_corpo(ponto: Vector2, direcao: Vector2) -> float:
	if not CORPO_DO_DONO.has_point(ponto):
		return 0.0
	var distancia := INF
	if direcao.x != 0.0:
		var borda_x := CORPO_DO_DONO.end.x if direcao.x > 0.0 else CORPO_DO_DONO.position.x
		distancia = minf(distancia, (borda_x - ponto.x) / direcao.x)
	if direcao.y != 0.0:
		var borda_y := CORPO_DO_DONO.end.y if direcao.y > 0.0 else CORPO_DO_DONO.position.y
		distancia = minf(distancia, (borda_y - ponto.y) / direcao.y)
	return distancia


func _atualizar_luz() -> void:
	var aceso: bool = _estado["aceso"]
	feixe.visible = aceso
	feixe_paredes.visible = aceso
	halo.visible = aceso
	var carga: float = _estado["carga"]
	var forca := 0.35 + 0.65 * carga
	if carga < carga_fraca and sin(_tempo * 31.0) * sin(_tempo * 7.3) > 0.55:
		forca *= 0.2
	feixe.energy = energia_feixe * forca
	feixe_paredes.energy = energia_nas_paredes * forca
	halo.energy = energia_halo * forca
