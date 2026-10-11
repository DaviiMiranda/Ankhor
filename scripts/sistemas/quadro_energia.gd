class_name QuadroEnergia
extends Interagivel

const COR_LIGADO := Color("7cf09a")
const COR_DESLIGADO := Color("3a3f48")
const COR_ESCOLHIDO := Color("f0d148")
const COR_TEXTO := Color("d8dee6")

@export var ordem: PackedInt32Array = PackedInt32Array([3, 1, 4, 2])
@export var marca: String = "energia"
@export var aviso_ligado: String = "A energia voltou. Lá fora, algo zumbiu e acendeu."
@export var aviso_ja_ligado: String = "Os disjuntores estão ligados."

var _aberto := false
var _ligados: Array[int] = []
var _cursor := 0
var _alavancas: Array[ColorRect] = []
var _numeros: Array[Label] = []

@onready var tela: CanvasLayer = $Tela
@onready var fila: HBoxContainer = $Tela/Painel/Alavancas
@onready var dica: Label = $Tela/Dica
@onready var som_clique: AudioStreamPlayer = $Tela/SomClique
@onready var som_desarme: AudioStreamPlayer = $Tela/SomDesarme


func _ready() -> void:
	super()
	process_mode = Node.PROCESS_MODE_ALWAYS
	tela.visible = false
	_montar_alavancas()


func pode_interagir() -> bool:
	return not _aberto


func interagir() -> void:
	if Progresso.tem(marca):
		Inventario.aviso.emit(aviso_ja_ligado)
		return
	_abrir()


func _montar_alavancas() -> void:
	for i in ordem.size():
		var coluna := VBoxContainer.new()
		coluna.alignment = BoxContainer.ALIGNMENT_CENTER
		var alavanca := ColorRect.new()
		alavanca.custom_minimum_size = Vector2(12, 30)
		var numero := Label.new()
		numero.text = str(i + 1)
		numero.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		coluna.add_child(alavanca)
		coluna.add_child(numero)
		fila.add_child(coluna)
		_alavancas.append(alavanca)
		_numeros.append(numero)


func _abrir() -> void:
	_aberto = true
	tela.visible = true
	get_tree().paused = true
	_cursor = 0
	dica.text = "Setas: escolher     E: ligar     Esc: fechar"
	_mostrar()


func _fechar() -> void:
	_aberto = false
	tela.visible = false
	get_tree().paused = false


func _unhandled_input(evento: InputEvent) -> void:
	if not _aberto:
		return
	if evento.is_action_pressed("ui_cancel"):
		_fechar()
	elif evento.is_action_pressed("mover_esquerda") or evento.is_action_pressed("ui_left"):
		_cursor = posmod(_cursor - 1, ordem.size())
		_mostrar()
	elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
		_cursor = posmod(_cursor + 1, ordem.size())
		_mostrar()
	elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		_ligar(_cursor)
	get_viewport().set_input_as_handled()


func _ligar(indice: int) -> void:
	if _ligados.has(indice):
		return
	som_clique.play()
	if indice + 1 != ordem[_ligados.size()]:
		_ligados.clear()
		som_desarme.play()
		dica.text = "Desarmou! Todos os disjuntores caíram."
		_mostrar()
		return
	_ligados.append(indice)
	_mostrar()
	if _ligados.size() == ordem.size():
		_concluir()


func _concluir() -> void:
	dica.text = "Energia restabelecida."
	Progresso.marcar(marca)
	await get_tree().create_timer(0.8, true).timeout
	_fechar()
	Inventario.aviso.emit(aviso_ligado)


func _mostrar() -> void:
	for i in _alavancas.size():
		_alavancas[i].color = COR_LIGADO if _ligados.has(i) else COR_DESLIGADO
		_numeros[i].add_theme_color_override("font_color", COR_ESCOLHIDO if i == _cursor else COR_TEXTO)
