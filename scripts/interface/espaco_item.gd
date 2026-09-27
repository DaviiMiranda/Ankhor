class_name EspacoItem
extends Control

signal clicado

const MOLDURA := preload("res://assets/sprites/interface/espaco.png")
const MOLDURA_ACESA := preload("res://assets/sprites/interface/espaco_selecionado.png")

@onready var moldura: TextureRect = $Moldura
@onready var icone: TextureRect = $Icone
@onready var numero: Label = $Numero
@onready var carga: ColorRect = $Carga


func _ready() -> void:
	gui_input.connect(_ao_receber_input)


func mostrar(item: Item, aceso: bool = false, texto_numero: String = "", valor_carga: float = -1.0) -> void:
	moldura.texture = MOLDURA_ACESA if aceso else MOLDURA
	icone.texture = item.icone if item else null
	numero.text = texto_numero
	carga.visible = valor_carga >= 0.0
	carga.size.x = roundf(16.0 * clampf(valor_carga, 0.0, 1.0))


func _ao_receber_input(evento: InputEvent) -> void:
	if evento is InputEventMouseButton and evento.pressed and evento.button_index == MOUSE_BUTTON_LEFT:
		clicado.emit()
