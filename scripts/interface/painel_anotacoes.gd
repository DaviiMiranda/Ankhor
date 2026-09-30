class_name PainelAnotacoes
extends Control

const LINHAS_LISTA := 8
const LINHAS_TEXTO := 7
const MARCA_NOVA := "• "
const COR_ESCOLHIDA := Color(0.64, 0.9, 0.85, 1)
const COR_NOVA := Color(0.95, 0.88, 0.7, 1)
const COR_NORMAL := Color(0.55, 0.56, 0.52, 1)

var _indice := 0
var _pagina := 0
var _rolagem := 0
var _linhas: Array[Label] = []

@onready var lista: VBoxContainer = $Lista
@onready var titulo: Label = $Titulo
@onready var numero_pagina: Label = $NumeroPagina
@onready var texto: Label = $Texto
@onready var som_papel: AudioStreamPlayer = $SomPapel


func _ready() -> void:
	for i in LINHAS_LISTA:
		lista.add_child(_criar_linha(i))
	texto.max_lines_visible = LINHAS_TEXTO
	Caderno.mudou.connect(atualizar)
	visibility_changed.connect(atualizar)


func mostrar_mais_recente() -> void:
	_indice = maxi(0, Caderno.anotacoes.size() - 1)
	_pagina = 0
	atualizar()


func tratar_entrada(evento: InputEvent) -> void:
	if evento.is_action_pressed("mover_cima") or evento.is_action_pressed("ui_up"):
		_escolher(_indice - 1)
	elif evento.is_action_pressed("mover_baixo") or evento.is_action_pressed("ui_down"):
		_escolher(_indice + 1)
	elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
		_virar(1)
	elif evento.is_action_pressed("mover_esquerda") or evento.is_action_pressed("ui_left"):
		_virar(-1)


func atualizar() -> void:
	if not is_node_ready():
		return
	_indice = clampi(_indice, 0, maxi(0, Caderno.anotacoes.size() - 1))
	_rolagem = clampi(_rolagem, maxi(0, _indice - LINHAS_LISTA + 1), _indice)
	_mostrar_lista()
	_mostrar_texto()
	if is_visible_in_tree():
		Caderno.marcar_lida(_indice)


func _criar_linha(posicao: int) -> Label:
	var linha := Label.new()
	linha.clip_text = true
	linha.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	linha.mouse_filter = Control.MOUSE_FILTER_STOP
	linha.gui_input.connect(_ao_clicar_linha.bind(posicao))
	_linhas.append(linha)
	return linha


func _mostrar_lista() -> void:
	for i in LINHAS_LISTA:
		var numero := _rolagem + i
		var linha := _linhas[i]
		if numero >= Caderno.anotacoes.size():
			linha.text = ""
			continue
		var anotacao: Dictionary = Caderno.anotacoes[numero]
		var nova: bool = not anotacao["lida"]
		linha.text = (MARCA_NOVA if nova else "") + str(anotacao["titulo"])
		var cor := COR_NOVA if nova else COR_NORMAL
		linha.add_theme_color_override("font_color", COR_ESCOLHIDA if numero == _indice else cor)


func _mostrar_texto() -> void:
	if Caderno.anotacoes.is_empty():
		titulo.text = "Nada anotado ainda."
		texto.text = "Leia os bilhetes e ouça o rádio: o que for útil fica anotado aqui."
		texto.lines_skipped = 0
		numero_pagina.text = ""
		return
	var anotacao: Dictionary = Caderno.anotacoes[_indice]
	titulo.text = anotacao["titulo"]
	texto.text = anotacao["texto"]
	_pagina = clampi(_pagina, 0, _total_paginas() - 1)
	texto.lines_skipped = _pagina * LINHAS_TEXTO
	numero_pagina.text = "%d/%d" % [_pagina + 1, _total_paginas()] if _total_paginas() > 1 else ""


func _total_paginas() -> int:
	return maxi(1, ceili(texto.get_line_count() / float(LINHAS_TEXTO)))


func _escolher(novo: int) -> void:
	novo = clampi(novo, 0, maxi(0, Caderno.anotacoes.size() - 1))
	if novo == _indice:
		return
	_indice = novo
	_pagina = 0
	som_papel.play()
	atualizar()


func _virar(passo: int) -> void:
	var nova := clampi(_pagina + passo, 0, _total_paginas() - 1)
	if nova == _pagina:
		return
	_pagina = nova
	som_papel.play()
	atualizar()


func _ao_clicar_linha(evento: InputEvent, posicao: int) -> void:
	if evento is InputEventMouseButton and evento.pressed and evento.button_index == MOUSE_BUTTON_LEFT:
		_escolher(_rolagem + posicao)
