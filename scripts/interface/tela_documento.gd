extends CanvasLayer

const LINHAS_POR_PAGINA := 8
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
	"carta": {
		"textura": preload("res://assets/sprites/interface/papel_carta.png"),
		"tinta": Color("26283a"),
	},
	"carta_faroleiro": {
		"textura": preload("res://assets/sprites/interface/papel_carta_faroleiro.png"),
		"tinta": Color("3b2614"),
	},
	"jornal": {
		"textura": preload("res://assets/sprites/interface/papel_jornal.png"),
		"tinta": Color("2a2722"),
	},
}
const TINTA_DA_MARGEM := Color("a3201f")
const LINHAS_DA_LEGENDA := 3
const TOPO_DO_TEXTO := 22.0
const TOPO_DA_LEGENDA := 100.0

var aberto := false
var _documento: Documento
var _pagina := 0
var _total_paginas := 1
var _tinta := Color.BLACK

@onready var papel: TextureRect = $Papel
@onready var titulo: Label = $Papel/Titulo
@onready var texto: Label = $Papel/Texto
@onready var numero_pagina: Label = $Papel/NumeroPagina
@onready var imagem: TextureRect = $Papel/Imagem
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
	_tinta = estilo["tinta"]
	for rotulo: Label in [titulo, numero_pagina]:
		rotulo.add_theme_color_override("font_color", _tinta)
	titulo.text = documento.titulo
	imagem.texture = documento.imagem
	_total_paginas = maxi(1, documento.paginas.size()) + _paginas_extras()
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


func _tem_pagina_da_imagem() -> bool:
	return _documento.imagem != null


func _tem_pagina_da_margem() -> bool:
	return not _documento.nota_na_margem.is_empty()


func _paginas_extras() -> int:
	return int(_tem_pagina_da_imagem()) + int(_tem_pagina_da_margem())


func _mostrar_pagina(numero: int) -> void:
	_pagina = numero
	var na_imagem := _tem_pagina_da_imagem() and numero == 0
	var na_margem := _tem_pagina_da_margem() and numero == _total_paginas - 1
	var indice_do_texto := numero - int(_tem_pagina_da_imagem())
	var limite := LINHAS_DA_LEGENDA if na_imagem else LINHAS_POR_PAGINA
	imagem.visible = na_imagem
	texto.offset_top = TOPO_DA_LEGENDA if na_imagem else TOPO_DO_TEXTO
	texto.max_lines_visible = limite
	texto.add_theme_color_override("font_color", TINTA_DA_MARGEM if na_margem else _tinta)
	if na_imagem:
		texto.text = _documento.legenda
	elif na_margem:
		texto.text = _documento.nota_na_margem
	else:
		texto.text = _documento.paginas[indice_do_texto] if indice_do_texto < _documento.paginas.size() else ""
	if texto.get_line_count() > limite:
		push_warning("Página %d de '%s' tem mais de %d linhas: o fim não aparece." % [numero + 1, _documento.id, limite])
	numero_pagina.text = "%d/%d" % [numero + 1, _total_paginas] if _total_paginas > 1 else ""
	if numero + 1 < _total_paginas:
		dica.text = "E: virar a página     Setas: folhear     Esc: fechar"
	else:
		dica.text = "E: fechar     Setas: folhear"
	som_papel.play()
