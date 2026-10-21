class_name PainelBits
extends Interagivel

const COR_LIGADA := Color("7cf09a")
const COR_DESLIGADA := Color("3a3f48")
const COR_ESCOLHIDA := Color("f0d148")
const COR_TEXTO := Color("d8dee6")
const COR_ERRO := Color("ff5a3a")

@export var alvo: int = 22
@export var quantidade_chaves: int = 5
@export var marca: String = "painel_bits_liberado"
@export var titulo: String = "TRAVA DE MANUTENÇÃO"
@export var aviso_liberado: String = "A trava soltou."
@export var aviso_ja_liberado: String = "A trava já está solta."
@export var item_premio: Item
@export var cena_premio: PackedScene
@export var quantidade_premio: int = 1

var _aberto := false
var _ligadas: Array[bool] = []
var _cursor := 0
var _chaves: Array[ColorRect] = []
var _bits: Array[Label] = []
var _pesos: Array[Label] = []

@onready var tela: CanvasLayer = $Tela
@onready var fila: HBoxContainer = $Tela/Painel/Chaves
@onready var rotulo_titulo: Label = $Tela/Painel/Titulo
@onready var visor: Label = $Tela/Painel/Visor
@onready var dica: Label = $Tela/Dica
@onready var som_clique: AudioStreamPlayer = $Tela/SomClique
@onready var som_erro: AudioStreamPlayer = $Tela/SomErro


func _ready() -> void:
	super()
	process_mode = Node.PROCESS_MODE_ALWAYS
	tela.visible = false
	rotulo_titulo.text = titulo
	_montar_chaves()
	if Progresso.tem(marca):
		_soltar_premio.call_deferred()


func pode_interagir() -> bool:
	return not _aberto


func interagir() -> void:
	if Progresso.tem(marca):
		Inventario.aviso.emit(aviso_ja_liberado)
		return
	_abrir()


func _peso(indice: int) -> int:
	return 1 << (quantidade_chaves - 1 - indice)


func _valor() -> int:
	var soma := 0
	for i in quantidade_chaves:
		if _ligadas[i]:
			soma += _peso(i)
	return soma


func _montar_chaves() -> void:
	for i in quantidade_chaves:
		_ligadas.append(false)
		var coluna := VBoxContainer.new()
		coluna.alignment = BoxContainer.ALIGNMENT_CENTER
		var bit := Label.new()
		bit.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		var chave := ColorRect.new()
		chave.custom_minimum_size = Vector2(12, 24)
		var peso := Label.new()
		peso.text = str(_peso(i))
		peso.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		coluna.add_child(bit)
		coluna.add_child(chave)
		coluna.add_child(peso)
		fila.add_child(coluna)
		_bits.append(bit)
		_chaves.append(chave)
		_pesos.append(peso)


func _abrir() -> void:
	_aberto = true
	tela.visible = true
	get_tree().paused = true
	_cursor = 0
	visor.text = "AJUSTE AS CHAVES"
	visor.add_theme_color_override("font_color", COR_TEXTO)
	dica.text = "Lados: chave     Cima/baixo: liga/desliga     E: confirmar     Esc: sair"
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
		_cursor = posmod(_cursor - 1, quantidade_chaves)
		_mostrar()
	elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
		_cursor = posmod(_cursor + 1, quantidade_chaves)
		_mostrar()
	elif evento.is_action_pressed("mover_cima") or evento.is_action_pressed("ui_up"):
		_virar(true)
	elif evento.is_action_pressed("mover_baixo") or evento.is_action_pressed("ui_down"):
		_virar(false)
	elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		_confirmar()
	get_viewport().set_input_as_handled()


func _virar(ligada: bool) -> void:
	if _ligadas[_cursor] == ligada:
		return
	_ligadas[_cursor] = ligada
	som_clique.play()
	visor.text = "AJUSTE AS CHAVES"
	visor.add_theme_color_override("font_color", COR_TEXTO)
	_mostrar()


func _confirmar() -> void:
	if _valor() != alvo:
		som_erro.play()
		visor.text = "CÓDIGO RECUSADO"
		visor.add_theme_color_override("font_color", COR_ERRO)
		return
	som_clique.play()
	visor.text = "TRAVA LIBERADA"
	visor.add_theme_color_override("font_color", COR_LIGADA)
	Progresso.marcar(marca)
	_soltar_premio()
	await get_tree().create_timer(0.8, true).timeout
	_fechar()
	Inventario.aviso.emit(aviso_liberado)


func _mostrar() -> void:
	for i in quantidade_chaves:
		_chaves[i].color = COR_LIGADA if _ligadas[i] else COR_DESLIGADA
		_bits[i].text = "1" if _ligadas[i] else "0"
		var cor := COR_ESCOLHIDA if i == _cursor else COR_TEXTO
		_bits[i].add_theme_color_override("font_color", cor)
		_pesos[i].add_theme_color_override("font_color", cor)


func _soltar_premio() -> void:
	Recompensa.soltar(self, item_premio, cena_premio, quantidade_premio)
