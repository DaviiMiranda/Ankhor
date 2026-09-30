extends CanvasLayer

enum Aba { ITENS, ANOTACOES }

const CENA_ESPACO := preload("res://cenas/interface/espaco_item.tscn")
const COR_ABA_ATIVA := Color(0.95, 0.88, 0.7, 1)
const COR_ABA_INATIVA := Color(0.55, 0.56, 0.52, 1)
const MARCA_NOVA := " •"
const DICAS := {
	Aba.ITENS: "Q: anotações   Setas: escolher   1-3: equipar   Tab: fechar",
	Aba.ANOTACOES: "Q: itens   Setas: escolher e folhear   Tab: fechar",
}

var aberto := false
var _aba := Aba.ITENS
var _cursor := Vector2i(0, 0)
var _espacos_grade: Array[EspacoItem] = []
var _espacos_gadget: Array[EspacoItem] = []

@onready var aba_itens: Label = $Janela/Abas/AbaItens
@onready var aba_anotacoes: Label = $Janela/Abas/AbaAnotacoes
@onready var marcador: ColorRect = $Janela/Marcador
@onready var painel_itens: Control = $Janela/Itens
@onready var painel_anotacoes: PainelAnotacoes = $Janela/Anotacoes
@onready var dica: Label = $Janela/Dica
@onready var grade: GridContainer = $Janela/Itens/Grade
@onready var caixa_gadgets: HBoxContainer = $Janela/Itens/Gadgets
@onready var nome: Label = $Janela/Itens/Nome
@onready var descricao: Label = $Janela/Itens/Descricao
@onready var situacao: Label = $Janela/Itens/Situacao
@onready var som_abrir: AudioStreamPlayer = $SomAbrir
@onready var som_fechar: AudioStreamPlayer = $SomFechar
@onready var som_aba: AudioStreamPlayer = $SomAba


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_criar_espacos()
	aba_itens.gui_input.connect(_ao_clicar_aba.bind(Aba.ITENS))
	aba_anotacoes.gui_input.connect(_ao_clicar_aba.bind(Aba.ANOTACOES))
	Inventario.mudou.connect(_atualizar)
	Caderno.mudou.connect(_atualizar_abas)
	visible = false


func _criar_espacos() -> void:
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


func _unhandled_input(evento: InputEvent) -> void:
	if evento.is_action_pressed("inventario"):
		_tratar_atalho(Aba.ITENS)
		return
	if evento.is_action_pressed("caderno"):
		_tratar_atalho(Aba.ANOTACOES)
		return
	if not aberto:
		return
	if evento.is_action_pressed("ui_cancel"):
		_abrir(false)
	elif evento.is_action_pressed("trocar_aba"):
		_mostrar_aba(Aba.ANOTACOES if _aba == Aba.ITENS else Aba.ITENS)
		som_aba.play()
	elif _aba == Aba.ITENS:
		_tratar_itens(evento)
	else:
		painel_anotacoes.tratar_entrada(evento)
	get_viewport().set_input_as_handled()


func _tratar_atalho(aba: Aba) -> void:
	if not aberto and get_tree().paused:
		return
	_alternar(aba)
	get_viewport().set_input_as_handled()


func _alternar(aba: Aba) -> void:
	if not aberto:
		_abrir(true)
		_mostrar_aba(aba)
		if aba == Aba.ANOTACOES:
			painel_anotacoes.mostrar_mais_recente()
	elif aba == _aba or aba == Aba.ITENS:
		_abrir(false)
	else:
		_mostrar_aba(aba)
		som_aba.play()


func _tratar_itens(evento: InputEvent) -> void:
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


func _abrir(abrir: bool) -> void:
	aberto = abrir
	visible = abrir
	get_tree().paused = abrir
	if abrir:
		som_fechar.stop()
		som_abrir.play()
	else:
		som_abrir.stop()
		som_fechar.play()
	_atualizar()


func _mostrar_aba(aba: Aba) -> void:
	_aba = aba
	painel_itens.visible = aba == Aba.ITENS
	painel_anotacoes.visible = aba == Aba.ANOTACOES
	dica.text = DICAS[aba]
	_atualizar_abas()


func _atualizar_abas() -> void:
	if not is_node_ready():
		return
	aba_anotacoes.text = "ANOTAÇÕES" + (MARCA_NOVA if Caderno.tem_nao_lidas() else "")
	aba_itens.add_theme_color_override("font_color", COR_ABA_ATIVA if _aba == Aba.ITENS else COR_ABA_INATIVA)
	aba_anotacoes.add_theme_color_override("font_color", COR_ABA_ATIVA if _aba == Aba.ANOTACOES else COR_ABA_INATIVA)
	_posicionar_marcador.call_deferred()


func _posicionar_marcador() -> void:
	var aba_ativa := aba_itens if _aba == Aba.ITENS else aba_anotacoes
	var area := aba_ativa.get_global_rect()
	marcador.global_position.x = area.position.x - 2.0
	marcador.size.x = area.size.x + 4.0


func _ao_clicar_aba(evento: InputEvent, aba: Aba) -> void:
	if evento is InputEventMouseButton and evento.pressed and evento.button_index == MOUSE_BUTTON_LEFT \
			and aba != _aba:
		_mostrar_aba(aba)
		som_aba.play()


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
