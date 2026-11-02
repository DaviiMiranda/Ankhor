class_name BotaoDoMenuVr
extends Node3D

const COR_NORMAL := Color(0.09, 0.02, 0.03)
const COR_MIRADO := Color(0.62, 0.08, 0.06)
const TINTA_NORMAL := Color(0.75, 0.55, 0.52)
const TINTA_MIRADO := Color(1, 0.93, 0.88)

@export var texto: String = ""

var _material: StandardMaterial3D

@onready var fundo: MeshInstance3D = $Fundo
@onready var rotulo: Label3D = $Rotulo


func _ready() -> void:
	_material = (fundo.material_override as StandardMaterial3D).duplicate()
	fundo.material_override = _material
	rotulo.text = texto
	destacar(false)


func destacar(sim: bool) -> void:
	_material.albedo_color = COR_MIRADO if sim else COR_NORMAL
	rotulo.modulate = TINTA_MIRADO if sim else TINTA_NORMAL
