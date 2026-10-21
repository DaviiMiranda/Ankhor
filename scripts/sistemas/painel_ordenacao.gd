class_name PainelOrdenacao
extends Interagivel

const COR_PECA := Color("2c3a5c")
const COR_PECA_CERTA := Color("2f5a44")
const COR_ESCOLHIDA := Color("f0d148")
const COR_TEXTO := Color("d8dee6")
const COR_PRONTO := Color("7cf09a")

@export var ordem_certa: PackedStringArray = PackedStringArray(["PP", "P", "M", "G", "GG"])
@export var ordem_inicial: PackedInt32Array = PackedInt32Array([3, 0, 4, 2, 1])
@export var marca: String = "arara_ordenada"
@export var titulo: String = "ARARA INTELIGENTE"
@export var pedido: String = "ORGANIZE DO MENOR PARA O MAIOR"
@export var aviso_ordenado: String = "A arara está em ordem."
@export var aviso_ja_ordenado: String = "A arara já está em ordem."
@export var item_premio: Item
@export var cena_premio: PackedScene
@export var quantidade_premio: int = 1

var _aberto := false
var _pecas: Array[int] = []
var _inicial: Array[int] = []
var _cursor := 0
var _trocas := 0
var _caixas: Array[ColorRect] = []
var _rotulos: Array[Label] = []

@onready var tela: CanvasLayer = $Tela
@onready var fila: HBoxContainer = $Tela/Painel/Pecas
@onready var rotulo_titulo: Label = $Tela/Painel/Titulo
@onready var rotulo_pedido: Label = $Tela/Painel/Pedido
@onready var visor: Label = $Tela/Painel/Visor
@onready var dica: Label = $Tela/Dica
@onready var som_troca: AudioStreamPlayer = $Tela/SomTroca
@onready var som_pronto: AudioStreamPlayer = $Tela/SomPronto


func _ready() -> void:
	super()
	process_mode = Node.PROCESS_MODE_ALWAYS
	tela.visible = false
	rotulo_titulo.text = titulo
	rotulo_pedido.text = pedido
	for indice in ordem_inicial:
		_inicial.append(indice)
	_pecas = _inicial.duplicate()
	_montar_pecas()
	if Progresso.tem(marca):
		_soltar_premio.call_deferred()


func pode_interagir() -> bool:
	return not _aberto


func interagir() -> void:
	if Progresso.tem(marca):
		Inventario.aviso.emit(aviso_ja_ordenado)
		return
	_abrir()


static func inversoes(sequencia: Array[int]) -> int:
	var total := 0
	for i in sequencia.size():
		for j in range(i + 1, sequencia.size()):
			if sequencia[i] > sequencia[j]:
				total += 1
	return total


func _montar_pecas() -> void:
	for i in _pecas.size():
		var caixa := ColorRect.new()
		caixa.custom_minimum_size = Vector2(22, 22)
		var rotulo := Label.new()
		rotulo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		rotulo.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		rotulo.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		caixa.add_child(rotulo)
		fila.add_child(caixa)
		_caixas.append(caixa)
		_rotulos.append(rotulo)


func _abrir() -> void:
	_aberto = true
	tela.visible = true
	get_tree().paused = true
	_cursor = 0
	dica.text = "Lados: escolher o par     E: trocar     Esc: sair"
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
		_cursor = posmod(_cursor - 1, _pecas.size() - 1)
		_mostrar()
	elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
		_cursor = posmod(_cursor + 1, _pecas.size() - 1)
		_mostrar()
	elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		_trocar()
	get_viewport().set_input_as_handled()


func _trocar() -> void:
	if Progresso.tem(marca):
		return
	var guardada := _pecas[_cursor]
	_pecas[_cursor] = _pecas[_cursor + 1]
	_pecas[_cursor + 1] = guardada
	_trocas += 1
	som_troca.play()
	_mostrar()
	if inversoes(_pecas) == 0:
		_concluir()


func _concluir() -> void:
	var minimo := inversoes(_inicial)
	visor.text = "EM ORDEM: %d TROCAS (MÍNIMO %d)" % [_trocas, minimo]
	visor.add_theme_color_override("font_color", COR_PRONTO)
	som_pronto.play()
	Progresso.marcar(marca)
	_soltar_premio()
	await get_tree().create_timer(1.4, true).timeout
	_fechar()
	Inventario.aviso.emit(aviso_ordenado)


func _mostrar() -> void:
	if not Progresso.tem(marca):
		visor.text = "TROCAS: %d" % _trocas
		visor.add_theme_color_override("font_color", COR_TEXTO)
	for i in _pecas.size():
		_rotulos[i].text = ordem_certa[_pecas[i]]
		_caixas[i].color = COR_PECA_CERTA if _pecas[i] == i else COR_PECA
		var no_par := i == _cursor or i == _cursor + 1
		_rotulos[i].add_theme_color_override("font_color", COR_ESCOLHIDA if no_par else COR_TEXTO)


func _soltar_premio() -> void:
	Recompensa.soltar(self, item_premio, cena_premio, quantidade_premio)
