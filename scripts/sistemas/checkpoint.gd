class_name Checkpoint
extends Area2D

@export var id: String = ""
@export var textura_apagado: Texture2D
@export var textura_aceso: Texture2D
@export var deslocamento_retorno := Vector2(0, 8)

@onready var sprite: Sprite2D = $Sprite2D
@onready var luz: PointLight2D = $Luz
@onready var som: AudioStreamPlayer2D = $Som


func _ready() -> void:
	body_entered.connect(_ao_entrar)
	Checkpoints.marcado.connect(_ao_marcar)
	_mostrar(_ativo())


func _ao_entrar(corpo: Node2D) -> void:
	if not corpo is Gabriel or _ativo():
		return
	Checkpoints.marcar(_id(), _cena(), global_position + deslocamento_retorno)
	Vida.limpar()
	som.play()


func _ao_marcar(_novo_id: String) -> void:
	_mostrar(_ativo())


func _mostrar(aceso: bool) -> void:
	sprite.texture = textura_aceso if aceso else textura_apagado
	luz.visible = aceso


func _ativo() -> bool:
	return Checkpoints.esta_ativo(_id(), _cena())


func _id() -> String:
	return id if not id.is_empty() else String(name)


func _cena() -> String:
	var sala := owner if owner else get_tree().current_scene
	return sala.scene_file_path if sala else ""
