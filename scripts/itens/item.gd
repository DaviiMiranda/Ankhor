class_name Item
extends Resource

@export var id: String = ""
@export var nome: String = ""
@export_multiline var descricao: String = ""
@export var icone: Texture2D
@export var sprite_chao: Texture2D

@export_group("Gadget")
@export var equipavel: bool = false
@export var cena_gadget: PackedScene
@export var maximo_unidades: int = 0
