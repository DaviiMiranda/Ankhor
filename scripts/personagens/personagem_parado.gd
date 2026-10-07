class_name PersonagemParado
extends StaticBody2D

@export_enum("lado", "frente", "tres_quartos", "costas", "tres_quartos_costas") var vista := "frente"
@export var olhando_para_esquerda := false

@export_group("Parado")
@export var parado_lado: Texture2D
@export var parado_frente: Texture2D
@export var parado_tres_quartos: Texture2D
@export var parado_costas: Texture2D
@export var parado_tres_quartos_costas: Texture2D
@export var quadros_parado: int = 8
@export var segundos_por_quadro_parado: float = 0.3

var _tempo_parado := 0.0

@onready var sprite: Sprite2D = $Sprite2D


func _ready() -> void:
	sprite.frame = 0
	sprite.texture = _tira_da_vista()
	sprite.hframes = quadros_parado
	sprite.flip_h = olhando_para_esquerda
	_tempo_parado = randf() * quadros_parado * segundos_por_quadro_parado


func _process(delta: float) -> void:
	_tempo_parado += delta
	sprite.frame = int(_tempo_parado / segundos_por_quadro_parado) % quadros_parado


func _tira_da_vista() -> Texture2D:
	var tiras := {"lado": parado_lado, "frente": parado_frente,
			"tres_quartos": parado_tres_quartos, "costas": parado_costas,
			"tres_quartos_costas": parado_tres_quartos_costas}
	return tiras[vista]
