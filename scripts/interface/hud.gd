extends CanvasLayer

const CENA_ESPACO := preload("res://cenas/interface/espaco_item.tscn")
const CORACAO_CHEIO := preload("res://assets/sprites/interface/coracao_cheio.png")
const CORACAO_VAZIO := preload("res://assets/sprites/interface/coracao_vazio.png")

@export var duracao_mensagem: float = 3.5

var _espacos: Array[EspacoItem] = []
var _coracoes: Array[TextureRect] = []
var _tween_mensagem: Tween
var _tween_dano: Tween

@onready var caixa_gadgets: HBoxContainer = $Gadgets
@onready var aviso: Label = $Aviso
@onready var mensagem: Label = $Mensagem
@onready var caixa_coracoes: HBoxContainer = $Coracoes
@onready var flash_dano: ColorRect = $FlashDano
@onready var som_dano: AudioStreamPlayer = $SomDano


func _ready() -> void:
	for i in Inventario.ESPACOS_GADGET:
		var espaco := CENA_ESPACO.instantiate() as EspacoItem
		espaco.mouse_filter = Control.MOUSE_FILTER_IGNORE
		caixa_gadgets.add_child(espaco)
		_espacos.append(espaco)
	for i in Vida.MAXIMA:
		var coracao := TextureRect.new()
		coracao.mouse_filter = Control.MOUSE_FILTER_IGNORE
		caixa_coracoes.add_child(coracao)
		_coracoes.append(coracao)
	Inventario.item_pego.connect(_ao_pegar_item)
	Inventario.aviso.connect(_mostrar_mensagem)
	Caderno.anotado.connect(_ao_anotar)
	Checkpoints.marcado.connect(_ao_marcar_checkpoint)
	Vida.mudou.connect(_atualizar_coracoes)
	Vida.dano_recebido.connect(_ao_receber_dano)
	_atualizar_coracoes(Vida.vida)
	flash_dano.color.a = 0.0
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
	_mostrar_mensagem(texto)


func _atualizar_coracoes(vida: int) -> void:
	for i in _coracoes.size():
		_coracoes[i].texture = CORACAO_CHEIO if i < vida else CORACAO_VAZIO


func _ao_receber_dano(_origem: Vector2) -> void:
	som_dano.play()
	if _tween_dano:
		_tween_dano.kill()
	flash_dano.color.a = 0.45
	_tween_dano = create_tween()
	_tween_dano.tween_property(flash_dano, "color:a", 0.0, 0.5)


func _ao_marcar_checkpoint(_id: String) -> void:
	_mostrar_mensagem("Checkpoint salvo")


func _ao_anotar(titulo: String) -> void:
	_mostrar_mensagem("Nova anotação: %s   [N] ver" % titulo)


func _mostrar_mensagem(texto: String) -> void:
	mensagem.text = texto
	if _tween_mensagem:
		_tween_mensagem.kill()
	mensagem.modulate.a = 1.0
	_tween_mensagem = create_tween()
	_tween_mensagem.tween_interval(duracao_mensagem)
	_tween_mensagem.tween_property(mensagem, "modulate:a", 0.0, 0.8)
