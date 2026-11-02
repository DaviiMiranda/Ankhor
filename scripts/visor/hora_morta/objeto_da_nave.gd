class_name ObjetoDaNave
extends Node3D

signal usado

@export var texto_acao := ""
@export var segundos_para_usar := 0.0
@export var distancia_de_uso := 2.4


func pode_mirar() -> bool:
	return not texto_acao.is_empty()


func usar() -> void:
	usado.emit()


func ponto_da_mira() -> Vector3:
	return global_position
