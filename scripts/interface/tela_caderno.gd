extends CanvasLayer

var aberto := false
var _indice := 0

@onready var titulo: Label = $Papel/Titulo
@onready var texto: Label = $Papel/Texto
@onready var numero_pagina: Label = $Papel/NumeroPagina
@onready var som_papel: AudioStreamPlayer = $SomPapel


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false


func _unhandled_input(evento: InputEvent) -> void:
	if evento.is_action_pressed("caderno") or (aberto and evento.is_action_pressed("ui_cancel")):
		if not aberto and get_tree().paused:
			return
		_abrir(not aberto)
		get_viewport().set_input_as_handled()
		return
	if not aberto:
		return
	if evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right") \
			or evento.is_action_pressed("interagir"):
		_folhear(1)
	elif evento.is_action_pressed("mover_esquerda") or evento.is_action_pressed("ui_left"):
		_folhear(-1)
	get_viewport().set_input_as_handled()


func _abrir(abrir: bool) -> void:
	aberto = abrir
	visible = abrir
	get_tree().paused = abrir
	som_papel.play()
	if abrir:
		_indice = maxi(0, Caderno.anotacoes.size() - 1)
		_mostrar()


func _folhear(passo: int) -> void:
	var novo := clampi(_indice + passo, 0, maxi(0, Caderno.anotacoes.size() - 1))
	if novo == _indice:
		return
	_indice = novo
	som_papel.play()
	_mostrar()


func _mostrar() -> void:
	if Caderno.anotacoes.is_empty():
		titulo.text = "Caderno"
		texto.text = "Nada anotado ainda."
		numero_pagina.text = ""
		return
	var anotacao: Dictionary = Caderno.anotacoes[_indice]
	titulo.text = anotacao["titulo"]
	texto.text = anotacao["texto"]
	numero_pagina.text = "%d/%d" % [_indice + 1, Caderno.anotacoes.size()]
