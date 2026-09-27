extends CanvasLayer

signal pular

@export var espera: float = 1.0
@export var duracao_aparecer: float = 0.6

@onready var botao: Button = $Botao


func _ready() -> void:
	botao.pressed.connect(pular.emit)
	botao.modulate.a = 0.0
	var tween := create_tween()
	tween.tween_interval(espera)
	tween.tween_property(botao, "modulate:a", 1.0, duracao_aparecer)
