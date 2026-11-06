class_name SumicoDeEnergia
extends Node2D

signal explodiu

@export var segundos_brilhando: float = 2.6
@export var altura_do_peito: float = 26.0
@export var brilho_maximo: Color = Color(2.2, 2.6, 2.8, 1.0)
@export var tremor_maximo: float = 1.6
@export var energia_da_luz: float = 2.4
@export var energia_do_estouro: float = 5.0
@export var segundos_do_clarao: float = 1.1

@onready var luz: PointLight2D = $Luz
@onready var faiscas: CPUParticles2D = $Faiscas
@onready var estouro: CPUParticles2D = $Estouro
@onready var som_carga: AudioStreamPlayer2D = $SomCarga
@onready var som_estouro: AudioStreamPlayer2D = $SomEstouro
@onready var clarao: ColorRect = $Clarao/Tela


func _ready() -> void:
	luz.energy = 0.0
	clarao.color.a = 0.0


func sumir(alvo: Node2D) -> void:
	global_position = alvo.global_position - Vector2(0, altura_do_peito)
	var origem := alvo.position
	faiscas.emitting = true
	som_carga.play()
	var brilho := create_tween().set_parallel()
	brilho.tween_property(luz, "energy", energia_da_luz, segundos_brilhando).set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_QUAD)
	brilho.tween_property(luz, "texture_scale", 1.8, segundos_brilhando)
	brilho.tween_property(alvo, "modulate", brilho_maximo, segundos_brilhando).set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_QUAD)
	brilho.tween_method(_tremer.bind(alvo, origem), 0.0, 1.0, segundos_brilhando)
	await brilho.finished
	_estourar(alvo, origem)


func _tremer(progresso: float, alvo: Node2D, origem: Vector2) -> void:
	var forca := progresso * progresso * tremor_maximo
	alvo.position = origem + Vector2(randf_range(-forca, forca), randf_range(-forca, forca) * 0.5)


func _estourar(alvo: Node2D, origem: Vector2) -> void:
	alvo.position = origem
	alvo.visible = false
	faiscas.emitting = false
	som_carga.stop()
	som_estouro.play()
	estouro.restart()
	clarao.color.a = 1.0
	luz.energy = energia_do_estouro
	var apagar := create_tween().set_parallel()
	apagar.tween_property(clarao, "color:a", 0.0, segundos_do_clarao).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_QUAD)
	apagar.tween_property(luz, "energy", 0.0, segundos_do_clarao * 1.3).set_ease(Tween.EASE_OUT)
	explodiu.emit()
