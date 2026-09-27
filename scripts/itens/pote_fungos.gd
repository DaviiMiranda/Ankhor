extends Node2D

@export var duracao: float = 270.0
@export var energia_maxima: float = 1.4
@export var alcance_maximo: float = 3.2

var item: Item
var _estado: Dictionary
var _tempo := 0.0

@onready var luz: PointLight2D = $Luz


func _ready() -> void:
	_estado = Inventario.estado_de(item.id if item else "pote_fungos")
	if not _estado.has("carga"):
		_estado["carga"] = 1.0
	if not _estado.has("aceso"):
		_estado["aceso"] = false
	_atualizar_luz()


func usar() -> void:
	if _estado["carga"] > 0.0:
		_estado["aceso"] = not _estado["aceso"]
	_atualizar_luz()


func ao_desequipar() -> void:
	_estado["aceso"] = false


func _process(delta: float) -> void:
	_tempo += delta
	if _estado["aceso"]:
		_estado["carga"] = maxf(_estado["carga"] - delta / duracao, 0.0)
		if _estado["carga"] <= 0.0:
			_estado["aceso"] = false
	_atualizar_luz()


func _atualizar_luz() -> void:
	luz.visible = _estado["aceso"]
	var carga: float = _estado["carga"]
	var forca := 0.25 + 0.75 * carga
	var tremor := 1.0 + 0.05 * sin(_tempo * 2.3) + 0.03 * sin(_tempo * 5.1)
	luz.energy = energia_maxima * forca * tremor
	luz.texture_scale = alcance_maximo * (0.6 + 0.4 * carga)
