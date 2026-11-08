extends Node2D

@export_multiline var texto: String = ""
@export var cor_do_texto := Color(1, 1, 1)

@onready var rotulo: Label = $Rotulo


func _ready() -> void:
	rotulo.text = texto
	rotulo.add_theme_color_override("font_color", cor_do_texto)
