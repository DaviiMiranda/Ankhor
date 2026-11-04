class_name PecaNoChao
extends Interagivel

const SOM_PEGAR := preload("res://assets/audio/efeitos/objetos/painel_tecla.wav")

@export var marca: String = ""
@export var aviso_ao_pegar: String = ""
@export var textura: Texture2D

@onready var sprite: Sprite2D = $Sprite2D


func _ready() -> void:
	super()
	sprite.texture = textura
	if textura:
		sprite.offset = Vector2(-floorf(textura.get_width() / 2.0), -textura.get_height())
	if Progresso.tem(marca):
		queue_free()


func interagir() -> void:
	Progresso.marcar(marca)
	Inventario.aviso.emit(aviso_ao_pegar)
	_tocar_som()
	queue_free()


func _tocar_som() -> void:
	var som := AudioStreamPlayer.new()
	som.stream = SOM_PEGAR
	som.bus = &"Efeitos"
	som.finished.connect(som.queue_free)
	get_tree().current_scene.add_child(som)
	som.play()
