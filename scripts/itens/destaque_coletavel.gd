class_name DestaqueColetavel
extends Node2D

const TAMANHOS_BRILHO := [0, 1, 2, 1, 0]

@export var intensidade: float = 1.0
@export var periodo_pulso: float = 2.4
@export var energia_minima: float = 0.4
@export var energia_maxima: float = 1.0
@export var espera_brilho_minima: float = 1.2
@export var espera_brilho_maxima: float = 3.0
@export var duracao_quadro_brilho: float = 0.07
@export var cor_brilho: Color = Color(1, 0.96, 0.8, 1)

var _escala_base := 1.0
var _tempo := 0.0
var _espera := 0.0
var _quadro := -1
var _tempo_quadro := 0.0
var _ponto_brilho := Vector2.ZERO
var _textura_medida: Texture2D
var _area_desenhada := Rect2()

@onready var luz: PointLight2D = $Luz


func _ready() -> void:
	_escala_base = luz.texture_scale.x
	_tempo = randf() * periodo_pulso
	_espera = randf_range(0.3, espera_brilho_maxima)


func _process(delta: float) -> void:
	_tempo += delta
	_pulsar_luz()
	_avancar_brilho(delta)


func _pulsar_luz() -> void:
	var onda := (1.0 - cos(_tempo * TAU / periodo_pulso)) / 2.0
	luz.energy = lerpf(energia_minima, energia_maxima, onda) * intensidade
	luz.texture_scale = Vector2.ONE * _escala_base * sqrt(intensidade)
	luz.position = _area_do_desenho().get_center()


func _avancar_brilho(delta: float) -> void:
	if _quadro == -1:
		_espera -= delta
		if _espera <= 0.0:
			_comecar_brilho()
		return
	_tempo_quadro += delta
	if _tempo_quadro < duracao_quadro_brilho:
		return
	_tempo_quadro = 0.0
	_quadro += 1
	if _quadro >= TAMANHOS_BRILHO.size():
		_quadro = -1
		_espera = randf_range(espera_brilho_minima, espera_brilho_maxima) / intensidade
	queue_redraw()


func _comecar_brilho() -> void:
	var area := _area_do_desenho()
	_ponto_brilho = Vector2(
			randi_range(int(area.position.x) + 1, maxi(int(area.end.x) - 2, int(area.position.x) + 1)),
			randi_range(int(area.position.y), maxi(int(area.position.y + area.size.y / 2.0), int(area.position.y))))
	_quadro = 0
	_tempo_quadro = 0.0
	queue_redraw()


func _area_do_desenho() -> Rect2:
	var sprite := get_parent().get_node_or_null("Sprite2D") as Sprite2D
	if sprite == null or sprite.texture == null:
		return Rect2(-2, -4, 4, 4)
	if sprite.texture != _textura_medida:
		_textura_medida = sprite.texture
		_area_desenhada = Rect2(_textura_medida.get_image().get_used_rect())
	return Rect2(sprite.position + sprite.offset + _area_desenhada.position, _area_desenhada.size)


func _draw() -> void:
	if _quadro == -1:
		return
	var braco: int = TAMANHOS_BRILHO[_quadro]
	draw_rect(Rect2(_ponto_brilho, Vector2.ONE), cor_brilho)
	var cor_ponta := Color(cor_brilho, 0.55)
	for i in range(1, braco + 1):
		var cor := cor_brilho if i < braco else cor_ponta
		for direcao in [Vector2.LEFT, Vector2.RIGHT, Vector2.UP, Vector2.DOWN]:
			draw_rect(Rect2(_ponto_brilho + direcao * i, Vector2.ONE), cor)
