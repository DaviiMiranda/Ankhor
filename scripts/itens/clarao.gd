extends Node2D

@export var raio: float = 110.0
@export var segundos_atordoado: float = 3.5
@export var energia_flash: float = 4.0
@export var segundos_flash: float = 0.6

var item: Item

@onready var flash: PointLight2D = $Flash
@onready var som: AudioStreamPlayer = $Som


func usar() -> void:
	var restantes := Inventario.unidades(item.id)
	if restantes <= 0:
		Inventario.aviso.emit("Acabaram as cápsulas")
		return
	Inventario.definir_unidades(item, restantes - 1)
	som.play()
	_piscar()
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		if global_position.distance_to(robo.global_position) <= raio:
			robo.atordoar(segundos_atordoado * robo.fator_clarao)


func _piscar() -> void:
	flash.energy = energia_flash
	var animacao := create_tween()
	animacao.tween_property(flash, "energy", 0.0, segundos_flash)
