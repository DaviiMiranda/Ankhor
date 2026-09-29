extends CanvasLayer

const LINHAS_POR_PAGINA := 9
const PAPEIS := {
	"pergaminho": {
		"textura": preload("res://assets/sprites/interface/papel_pergaminho.png"),
		"tinta": Color("3a2210"),
	},
	"caderno_clarice": {
		"textura": preload("res://assets/sprites/interface/papel_caderno_clarice.png"),
		"tinta": Color("22306e"),
	},
	"caderno_gabriel": {
		"textura": preload("res://assets/sprites/interface/papel_caderno_gabriel.png"),
		"tinta": Color("2e2e36"),
	},
}

var aberto := false
var _documento: Documento
var _pagina := 0
var _total_paginas := 1

@onready var papel: TextureRect = $Papel
@onready var titulo: Label = $Papel/Titulo
@onready var texto: Label = $Papel/Texto
@onready var numero_pagina: Label = $Papel/NumeroPagina
@onready var dica: Label = $Dica
@onready var som_papel: AudioStreamPlayer = $SomPapel


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	Caderno.leitura_pedida.connect(abrir)
	visible = false


func abrir(documento: Documento) -> void:
	if aberto or get_tree().paused:
		return
	_documento = documento
	var estilo: Dictionary = PAPEIS.get(documento.papel, PAPEIS["caderno_gabriel"])
	papel.texture = estilo["textura"]
	for rotulo: Label in [titulo, texto, numero_pagina]:
		rotulo.add_theme_color_override("font_color", estilo["tinta"])
	titulo.text = documento.titulo
	texto.max_lines_visible = LINHAS_POR_PAGINA
	_total_paginas = maxi(1, documento.paginas.size())
	aberto = true
	visible = true
	get_tree().paused = true
	_mostrar_pagina(0)


func fechar() -> void:
	aberto = false
	visible = false
	get_tree().paused = false
	som_papel.play()
	Caderno.anotar(_documento.id, _documento.autor, _documento.anotacao)


func _unhandled_input(evento: InputEvent) -> void:
	if not aberto:
		return
	if evento.is_action_pressed("ui_cancel"):
		fechar()
	elif evento.is_action_pressed("interagir"):
		if _pagina + 1 < _total_paginas:
			_mostrar_pagina(_pagina + 1)
		else:
			fechar()
	elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
		if _pagina + 1 < _total_paginas:
			_mostrar_pagina(_pagina + 1)
	elif evento.is_action_pressed("mover_esquerda") or evento.is_action_pressed("ui_left"):
		if _pagina > 0:
			_mostrar_pagina(_pagina - 1)
	get_viewport().set_input_as_handled()


func _mostrar_pagina(numero: int) -> void:
	_pagina = numero
	texto.text = _documento.paginas[numero] if numero < _documento.paginas.size() else ""
	if texto.get_line_count() > LINHAS_POR_PAGINA:
		push_warning("Página %d de '%s' tem mais de %d linhas: o fim não aparece." \
				% [numero + 1, _documento.id, LINHAS_POR_PAGINA])
	numero_pagina.text = "%d/%d" % [numero + 1, _total_paginas] if _total_paginas > 1 else ""
	if numero + 1 < _total_paginas:
		dica.text = "E: virar a página     Setas: folhear     Esc: fechar"
	else:
		dica.text = "E: fechar     Setas: folhear"
	som_papel.play()
