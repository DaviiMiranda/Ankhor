extends CanvasLayer

@export var espera: float = 3.0

@onready var fundo: ColorRect = $Fundo
@onready var titulo: Label = $Titulo
@onready var subtitulo: Label = $Subtitulo
@onready var som: AudioStreamPlayer = $Som


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false
	Vida.morreu.connect(_ao_morrer)


func _ao_morrer() -> void:
	visible = true
	get_tree().paused = true
	som.play()
	fundo.color = Color(0.5, 0.0, 0.0, 0.0)
	titulo.modulate.a = 0.0
	subtitulo.modulate.a = 0.0
	var animacao := create_tween()
	animacao.tween_property(fundo, "color", Color(0.35, 0.0, 0.0, 0.85), 0.2)
	animacao.tween_property(fundo, "color", Color(0.0, 0.0, 0.0, 1.0), 0.9)
	animacao.parallel().tween_property(titulo, "modulate:a", 1.0, 0.6)
	animacao.tween_property(subtitulo, "modulate:a", 1.0, 0.4)
	animacao.tween_interval(maxf(espera - 1.5, 0.2))
	animacao.tween_callback(Checkpoints.voltar)
