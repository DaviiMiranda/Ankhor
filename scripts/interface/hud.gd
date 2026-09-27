extends CanvasLayer

const CENA_ESPACO := preload("res://cenas/interface/espaco_item.tscn")

@export var duracao_mensagem: float = 3.5

var _espacos: Array[EspacoItem] = []
var _tween_mensagem: Tween

@onready var caixa_gadgets: HBoxContainer = $Gadgets
@onready var aviso: Label = $Aviso
@onready var mensagem: Label = $Mensagem


func _ready() -> void:
	for i in Inventario.ESPACOS_GADGET:
		var espaco := CENA_ESPACO.instantiate() as EspacoItem
		espaco.mouse_filter = Control.MOUSE_FILTER_IGNORE
		caixa_gadgets.add_child(espaco)
		_espacos.append(espaco)
	Inventario.item_pego.connect(_ao_pegar_item)
	mensagem.modulate.a = 0.0
	aviso.hide()


func _process(_delta: float) -> void:
	_atualizar_gadgets()
	_atualizar_aviso()


func _atualizar_gadgets() -> void:
	for i in _espacos.size():
		var item: Item = Inventario.gadgets[i]
		var carga := -1.0
		var aceso := false
		if item:
			var estado: Dictionary = Inventario.estado.get(item.id, {})
			carga = estado.get("carga", -1.0)
			aceso = estado.get("aceso", false)
		_espacos[i].mostrar(item, aceso, str(i + 1), carga)


func _atualizar_aviso() -> void:
	var jogador := get_tree().get_first_node_in_group("jogador") as Node2D
	var alvo: Interagivel = null
	if jogador:
		alvo = Interagivel.mais_perto(get_tree(), jogador.global_position)
	aviso.visible = alvo != null
	if alvo == null:
		return
	aviso.text = "[E] " + alvo.texto_acao
	aviso.reset_size()
	var na_tela := alvo.get_global_transform_with_canvas().origin
	var pos := na_tela + Vector2(-aviso.size.x / 2.0, -alvo.altura_aviso - aviso.size.y)
	pos.x = clampf(pos.x, 2.0, 318.0 - aviso.size.x)
	pos.y = clampf(pos.y, 2.0, 178.0 - aviso.size.y)
	aviso.position = pos.round()


func _ao_pegar_item(item: Item) -> void:
	var texto := "Você pegou: " + item.nome
	var espaco := Inventario.espaco_do_gadget(item)
	if espaco != -1:
		texto += "   [%d] usar" % (espaco + 1)
	texto += "   [Tab] inventário"
	mensagem.text = texto
	if _tween_mensagem:
		_tween_mensagem.kill()
	mensagem.modulate.a = 1.0
	_tween_mensagem = create_tween()
	_tween_mensagem.tween_interval(duracao_mensagem)
	_tween_mensagem.tween_property(mensagem, "modulate:a", 0.0, 0.8)
