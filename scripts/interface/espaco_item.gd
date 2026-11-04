class_name EspacoItem
extends Control

signal clicado

const MOLDURA := preload("res://assets/sprites/interface/espaco.png")
const MOLDURA_ACESA := preload("res://assets/sprites/interface/espaco_selecionado.png")
const COR_ICONE_VAZIO := Color(0.3, 0.3, 0.3)
const COR_ALERTA := Color(1.0, 0.3, 0.25)
const ESCALA_DESTAQUE := Vector2(1.25, 1.25)
const OPACIDADE_INICIAL_MOLDURA := 0.4
const SEGUNDOS_CRESCENDO := 0.06
const SEGUNDOS_VOLTANDO := 0.12

var _destaque: Tween

@onready var moldura: TextureRect = $Moldura
@onready var icone: TextureRect = $Icone
@onready var numero: Label = $Numero
@onready var carga: ColorRect = $Carga
@onready var quantidade: Label = $Quantidade


func _ready() -> void:
	gui_input.connect(_ao_receber_input)


func mostrar(item: Item, aceso: bool = false, texto_numero: String = "", valor_carga: float = -1.0) -> void:
	moldura.texture = MOLDURA_ACESA if aceso else MOLDURA
	icone.texture = item.icone if item else null
	numero.text = texto_numero
	carga.visible = valor_carga >= 0.0
	carga.size.x = roundf(16.0 * clampf(valor_carga, 0.0, 1.0))
	_mostrar_quantidade(item)


func destacar() -> void:
	if _destaque:
		_destaque.kill()
	icone.pivot_offset = icone.size / 2.0
	icone.scale = Vector2.ONE
	moldura.modulate.a = OPACIDADE_INICIAL_MOLDURA
	_destaque = create_tween().set_parallel()
	_destaque.tween_property(moldura, "modulate:a", 1.0, SEGUNDOS_CRESCENDO + SEGUNDOS_VOLTANDO)
	_destaque.tween_property(icone, "scale", ESCALA_DESTAQUE, SEGUNDOS_CRESCENDO)
	_destaque.tween_property(icone, "scale", Vector2.ONE, SEGUNDOS_VOLTANDO).set_delay(SEGUNDOS_CRESCENDO)


func _mostrar_quantidade(item: Item) -> void:
	var empilha := item != null and item.maximo_unidades > 0
	var vazio: bool = item != null and Inventario.estado.get(item.id, {}).get("carga", -1.0) == 0.0
	icone.modulate = COR_ICONE_VAZIO if vazio else Color.WHITE
	quantidade.visible = empilha or vazio
	quantidade.text = str(Inventario.unidades(item.id)) if empilha else "0"
	quantidade.modulate = COR_ALERTA if vazio else Color.WHITE


func _ao_receber_input(evento: InputEvent) -> void:
	if evento is InputEventMouseButton and evento.pressed and evento.button_index == MOUSE_BUTTON_LEFT:
		clicado.emit()
