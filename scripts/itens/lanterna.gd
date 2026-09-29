extends Node2D

@export var duracao: float = 240.0
@export var energia_feixe: float = 1.3
@export var energia_nas_paredes: float = 1.0
@export var energia_halo: float = 0.45
@export var carga_fraca: float = 0.15
@export var distancia_da_mao: float = 6.0
@export var altura_da_mao: float = 2.0
@export var altura_da_sombra: float = 20.0

var item: Item
var _estado: Dictionary
var _tempo := 0.0

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


func usar() -> void:
	if _estado["carga"] > 0.0:
		_estado["aceso"] = not _estado["aceso"]
		clique.play()
	_atualizar_luz()


func ao_desequipar() -> void:
	_estado["aceso"] = false


func _process(delta: float) -> void:
	_tempo += delta
	if _estado["aceso"]:
		_estado["carga"] = maxf(_estado["carga"] - delta / duracao, 0.0)
		if _estado["carga"] <= 0.0:
			_estado["aceso"] = false
	_apontar()
	_atualizar_luz()


func _apontar() -> void:
	var dono := get_parent().get_parent() as Gabriel
	if dono:
		var mao := Vector2(dono.direcao_olhar.x * distancia_da_mao, altura_da_mao)
		feixe_paredes.position = mao
		halo.position = mao
		feixe.position = Vector2(0, altura_da_sombra)
		feixe.rotation = dono.direcao_olhar.angle()
		feixe.offset = (mao - feixe.position).rotated(-feixe.rotation)
		feixe_paredes.rotation = feixe.rotation


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
