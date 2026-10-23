class_name PainelObjetivo
extends Control

@onready var fase: Label = $Fase
@onready var objetivo: Label = $Objetivo
@onready var agora: Label = $Agora


func _ready() -> void:
	visibility_changed.connect(atualizar)


func atualizar() -> void:
	if not is_node_ready() or not is_visible_in_tree():
		return
	var dados := Objetivos.da_cena(get_tree().current_scene.scene_file_path)
	fase.text = dados["nome"]
	objetivo.text = dados["objetivo"]
	agora.text = Objetivos.passo_atual(dados)
