extends CanvasLayer

const CENA_ESPACO := preload("res://cenas/interface/espaco_item.tscn")

var aberto := false
var _cursor := Vector2i(0, 0)
var _espacos_grade: Array[EspacoItem] = []
var _espacos_gadget: Array[EspacoItem] = []

@onready var grade: GridContainer = $Janela/Grade
@onready var caixa_gadgets: HBoxContainer = $Janela/Gadgets
@onready var nome: Label = $Janela/Nome
@onready var descricao: Label = $Janela/Descricao
@onready var situacao: Label = $Janela/Situacao
## O zíper da mochila abrindo e fechando (gerados por
## assets/modelagem/audio/gerar_efeitos_gabriel.py). Tocam mesmo com o jogo
## pausado: eles herdam o process_mode Sempre desta tela.
@onready var som_abrir: AudioStreamPlayer = $SomAbrir
@onready var som_fechar: AudioStreamPlayer = $SomFechar


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	grade.columns = Inventario.COLUNAS
	for linha in Inventario.LINHAS:
		for coluna in Inventario.COLUNAS:
			var espaco := CENA_ESPACO.instantiate() as EspacoItem
			grade.add_child(espaco)
			espaco.clicado.connect(_escolher.bind(Vector2i(coluna, linha)))
			_espacos_grade.append(espaco)
	for i in Inventario.ESPACOS_GADGET:
		var espaco := CENA_ESPACO.instantiate() as EspacoItem
		caixa_gadgets.add_child(espaco)
		espaco.clicado.connect(_equipar_no_espaco.bind(i))
		_espacos_gadget.append(espaco)
	Inventario.mudou.connect(_atualizar)
	visible = false


func _unhandled_input(evento: InputEvent) -> void:
	if evento.is_action_pressed("inventario") or (aberto and evento.is_action_pressed("ui_cancel")):
		_abrir(not aberto)
		get_viewport().set_input_as_handled()
		return
	if not aberto:
		return
	var passo := Vector2i.ZERO
	if evento.is_action_pressed("mover_esquerda") or evento.is_action_pressed("ui_left"):
		passo = Vector2i.LEFT
	elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
		passo = Vector2i.RIGHT
	elif evento.is_action_pressed("mover_cima") or evento.is_action_pressed("ui_up"):
		passo = Vector2i.UP
	elif evento.is_action_pressed("mover_baixo") or evento.is_action_pressed("ui_down"):
		passo = Vector2i.DOWN
	if passo != Vector2i.ZERO:
		_escolher(Vector2i(posmod(_cursor.x + passo.x, Inventario.COLUNAS),
				posmod(_cursor.y + passo.y, Inventario.LINHAS)))
	for i in Inventario.ESPACOS_GADGET:
		if evento.is_action_pressed("gadget_%d" % (i + 1)):
			_equipar_no_espaco(i)
	get_viewport().set_input_as_handled()


func _abrir(abrir: bool) -> void:
	aberto = abrir
	visible = abrir
	get_tree().paused = abrir
	# Abrir e fechar rápido: um som corta o outro, para não tocarem juntos.
	if abrir:
		som_fechar.stop()
		som_abrir.play()
	else:
		som_abrir.stop()
		som_fechar.play()
	_atualizar()


func _escolher(posicao: Vector2i) -> void:
	_cursor = posicao
	_atualizar()


func _equipar_no_espaco(espaco: int) -> void:
	var item := Inventario.item_em(_cursor.y, _cursor.x)
	if item and item.equipavel:
		if Inventario.espaco_do_gadget(item) == espaco:
			Inventario.desequipar(espaco)
		else:
			Inventario.equipar(item, espaco)
	elif item == null and Inventario.gadgets[espaco] != null:
		Inventario.desequipar(espaco)


func _atualizar() -> void:
	if not is_node_ready():
		return
	var i := 0
	for linha in Inventario.LINHAS:
		for coluna in Inventario.COLUNAS:
			var item := Inventario.item_em(linha, coluna)
			var selecionado := Vector2i(coluna, linha) == _cursor
			var equipado := Inventario.espaco_do_gadget(item) if item else -1
			var texto := str(equipado + 1) if equipado != -1 else ""
			_espacos_grade[i].mostrar(item, selecionado, texto)
			i += 1
	for g in Inventario.ESPACOS_GADGET:
		_espacos_gadget[g].mostrar(Inventario.gadgets[g], false, str(g + 1))
	var escolhido := Inventario.item_em(_cursor.y, _cursor.x)
	nome.text = escolhido.nome if escolhido else ""
	descricao.text = escolhido.descricao if escolhido else ""
	situacao.text = ""
	if escolhido and escolhido.equipavel:
		var espaco := Inventario.espaco_do_gadget(escolhido)
		if espaco != -1:
			situacao.text = "Equipado na tecla %d" % (espaco + 1)
		else:
			situacao.text = "Aperte 1, 2 ou 3 para equipar"
