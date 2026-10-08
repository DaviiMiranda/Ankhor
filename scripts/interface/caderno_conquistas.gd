class_name CadernoConquistas
extends Control

signal fechar_pedido

const ICONE_CONQUISTADA := preload("res://assets/sprites/interface/conquistas/trofeu.png")
const ICONE_BLOQUEADA := preload("res://assets/sprites/interface/conquistas/trofeu_bloqueado.png")
const ICONE_SECRETA := preload("res://assets/sprites/interface/conquistas/secreta.png")
const COR_OURO := Color(1.0, 0.8, 0.35)
const ESTADOS_DO_ICONE := ["icon_normal_color", "icon_focus_color", "icon_hover_color", "icon_pressed_color", "icon_hover_pressed_color"]

@onready var grade: GridContainer = $PaginaDireita/Grade
@onready var progresso: Label = $PaginaDireita/Progresso
@onready var icone: TextureRect = $PaginaEsquerda/Icone
@onready var nome: Label = $PaginaEsquerda/Textos/Nome
@onready var descricao: Label = $PaginaEsquerda/Textos/Descricao
@onready var estado: Label = $PaginaEsquerda/Estado
@onready var botao_fechar: Button = $BotaoFechar

var _botoes: Array[Button] = []


func _ready() -> void:
	botao_fechar.pressed.connect(fechar_pedido.emit)
	Conquistas.desbloqueada.connect(func(_conquista: Conquista) -> void: atualizar())
	_montar_grade()
	atualizar()


func abrir() -> void:
	atualizar()
	if not _botoes.is_empty():
		_botoes[0].grab_focus()
		_mostrar(Conquistas.todas[0])


func atualizar() -> void:
	for i in _botoes.size():
		_pintar(_botoes[i], Conquistas.todas[i])
	progresso.text = "%d de %d" % [Conquistas.total_desbloqueadas(), Conquistas.todas.size()]


func _montar_grade() -> void:
	for conquista in Conquistas.todas:
		var botao := Button.new()
		botao.custom_minimum_size = Vector2(20, 20)
		botao.expand_icon = true
		botao.icon_alignment = HORIZONTAL_ALIGNMENT_CENTER
		botao.focus_entered.connect(_mostrar.bind(conquista))
		grade.add_child(botao)
		_botoes.append(botao)


func _pintar(botao: Button, conquista: Conquista) -> void:
	var conquistada := Conquistas.esta_desbloqueada(conquista.id)
	botao.icon = _icone_de(conquista, conquistada)
	for estado_do_icone in ESTADOS_DO_ICONE:
		botao.add_theme_color_override(estado_do_icone, COR_OURO if conquistada else Color.WHITE)


func _icone_de(conquista: Conquista, conquistada: bool) -> Texture2D:
	if conquistada:
		return ICONE_CONQUISTADA
	if conquista.secreta:
		return ICONE_SECRETA
	return ICONE_BLOQUEADA


func _mostrar(conquista: Conquista) -> void:
	var conquistada := Conquistas.esta_desbloqueada(conquista.id)
	icone.texture = _icone_de(conquista, conquistada)
	icone.modulate = COR_OURO if conquistada else Color.WHITE
	if conquista.secreta and not conquistada:
		nome.text = "???"
		descricao.text = "Conquista secreta."
	else:
		nome.text = conquista.nome
		descricao.text = conquista.descricao
	estado.text = "Conquistada!" if conquistada else "Ainda não."
