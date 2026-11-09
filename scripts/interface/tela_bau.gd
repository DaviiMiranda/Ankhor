extends CanvasLayer

const PASTA_ITENS := "res://dados/itens/%s.tres"
const PILHAS := "Pilhas"
const ICONE_PILHAS := preload("res://assets/sprites/itens/pilha.png")

var _itens: Array[Item] = []
var _lado := 0

@onready var _listas: Array[ItemList] = [$Janela/Mochila, $Janela/Bau]
@onready var _botoes: Array[Button] = [$Janela/Guardar, $Janela/Retirar]
@onready var _mensagem: Label = $Janela/Mensagem


func _ready() -> void:
	for id in Inventario.ITENS_DO_BAU:
		_itens.append(load(PASTA_ITENS % id) as Item)
	for lado in _listas.size():
		_listas[lado].item_selected.connect(_ao_selecionar.bind(lado))
		_botoes[lado].pressed.connect(_transferir.bind(lado))
	$Janela/Fechar.pressed.connect(_fechar)


func abrir() -> void:
	_lado = 0
	_mensagem.text = "Conteúdo compartilhado entre as salas seguras."
	get_tree().paused = true
	show()
	_atualizar()


func _fechar() -> void:
	hide()
	get_tree().paused = false


func _input(evento: InputEvent) -> void:
	if not visible:
		return
	if evento.is_action_pressed("pausar") or evento.is_action_pressed("inventario"):
		_fechar()
	elif evento.is_action_pressed("mover_esquerda"):
		_selecionar(0, 0)
	elif evento.is_action_pressed("mover_direita"):
		_selecionar(1, 0)
	elif evento.is_action_pressed("mover_cima", true):
		_selecionar(_lado, _indice(_listas[_lado]) - 1)
	elif evento.is_action_pressed("mover_baixo", true):
		_selecionar(_lado, _indice(_listas[_lado]) + 1)
	elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		_transferir(_lado)
	else:
		return
	get_viewport().set_input_as_handled()


func _atualizar() -> void:
	var indice := _indice(_listas[_lado])
	for lista in _listas:
		lista.clear()
	for item in _itens:
		if Inventario.tem(item.id):
			_adicionar_linha(_listas[0], item, Inventario.unidades(item.id))
		if Inventario.bau.has(item.id):
			_adicionar_linha(_listas[1], item, Inventario.bau[item.id])
	var pilhas := Inventario.pilhas()
	var guardadas: int = Inventario.bau.get(Inventario.ID_PILHAS, 0)
	if pilhas > 0:
		_adicionar_linha(_listas[0], null, pilhas)
	if guardadas > 0:
		_adicionar_linha(_listas[1], null, guardadas)
	for lista in _listas:
		if lista.item_count == 0:
			lista.add_item("Vazio", null, false)
	_selecionar(_lado, indice)


func _adicionar_linha(lista: ItemList, item: Item, quantidade: int) -> void:
	var nome := item.nome if item else PILHAS
	var icone := item.icone if item else ICONE_PILHAS
	var sufixo := "  %d balas" % quantidade if item and item.id == Inventario.ID_ARMA else "  ×%d" % quantidade
	var indice := lista.add_item(nome + sufixo, icone)
	lista.set_item_metadata(indice, item if item else Inventario.ID_PILHAS)


func _indice(lista: ItemList) -> int:
	var selecionados := lista.get_selected_items()
	return selecionados[0] if not selecionados.is_empty() else 0


func _ao_selecionar(indice: int, lado: int) -> void:
	_selecionar(lado, indice)


func _selecionar(lado: int, indice: int) -> void:
	_lado = lado
	var lista := _listas[lado]
	_listas[1 - lado].deselect_all()
	lista.select(clampi(indice, 0, lista.item_count - 1))
	_botoes[lado].disabled = not lista.is_anything_selected()
	_botoes[1 - lado].disabled = true


func _transferir(lado: int) -> void:
	var lista := _listas[lado]
	if not lista.is_anything_selected():
		return
	var entrada: Variant = lista.get_item_metadata(_indice(lista))
	var guardar := lado == 0
	var erro := ""
	if entrada is Item:
		if guardar:
			if not Inventario.guardar_no_bau(entrada):
				erro = "Item indisponível"
		else:
			erro = Inventario.retirar_do_bau(entrada)
	else:
		erro = Inventario.transferir_pilhas(guardar)
	_mensagem.text = ("Guardado no baú." if guardar else "Transferido para a mochila.") if erro.is_empty() else erro
	_atualizar()
