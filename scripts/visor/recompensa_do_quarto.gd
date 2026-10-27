class_name RecompensaDoQuarto
extends Node3D

@export var colecao: Colecao


func _ready() -> void:
	visible = colecao != null and Colecionaveis.completa(colecao)
