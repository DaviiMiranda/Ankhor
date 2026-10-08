class_name PainelCodigo
extends Interagivel

const COR_DIGITO := Color("7cf09a")
const COR_ESCOLHIDO := Color("f0d148")
const COR_ERRO := Color("ff5a3a")

@export var codigo: String = "0394"
@export var marca_energia: String = "energia"
@export var marca: String = "grade_aberta"
@export var textura_apagado: Texture2D
@export var textura_aceso: Texture2D
@export var aviso_sem_energia: String = "O painel está apagado. Sem energia."
@export var aviso_aberto: String = "Código aceito. A grade está subindo."
@export var aviso_ja_aberto: String = "A grade já está aberta."

var _aberto := false
var _digitos: Array[int] = []
var _cursor := 0
var _rotulos: Array[Label] = []

@onready var sprite: Sprite2D = $Sprite2D
@onready var tela: CanvasLayer = $Tela
@onready var fila: HBoxContainer = $Tela/Painel/Digitos
@onready var visor: Label = $Tela/Painel/Visor
@onready var dica: Label = $Tela/Dica
@onready var som_tecla: AudioStreamPlayer = $Tela/SomTecla
@onready var som_erro: AudioStreamPlayer = $Tela/SomErro


func _ready() -> void:
	super()
	process_mode = Node.PROCESS_MODE_ALWAYS
	tela.visible = false
	for i in codigo.length():
		var rotulo := Label.new()
		rotulo.custom_minimum_size = Vector2(14, 0)
		rotulo.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		rotulo.add_theme_font_size_override("font_size", 16)
		fila.add_child(rotulo)
		_rotulos.append(rotulo)
	Progresso.mudou.connect(_ao_mudar.unbind(1))
	_ao_mudar()


func pode_interagir() -> bool:
	return not _aberto


func interagir() -> void:
	if Progresso.tem(marca):
		Inventario.aviso.emit(aviso_ja_aberto)
	elif not Progresso.tem(marca_energia):
		Inventario.aviso.emit(aviso_sem_energia)
	else:
		_abrir()


func _ao_mudar() -> void:
	sprite.texture = textura_aceso if Progresso.tem(marca_energia) else textura_apagado


func _abrir() -> void:
	_aberto = true
	tela.visible = true
	get_tree().paused = true
	_digitos.clear()
	for i in codigo.length():
		_digitos.append(0)
	_cursor = 0
	visor.text = "DIGITE O CÓDIGO"
	visor.add_theme_color_override("font_color", COR_DIGITO)
	dica.text = "Cima/baixo: número     Lados: casa     E: confirmar     Esc: sair"
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
	elif evento.is_action_pressed("mover_cima") or evento.is_action_pressed("ui_up"):
		_girar(1)
	elif evento.is_action_pressed("mover_baixo") or evento.is_action_pressed("ui_down"):
		_girar(-1)
	elif evento.is_action_pressed("mover_esquerda") or evento.is_action_pressed("ui_left"):
		_cursor = posmod(_cursor - 1, _digitos.size())
		_mostrar()
	elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
		_cursor = posmod(_cursor + 1, _digitos.size())
		_mostrar()
	elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		_confirmar()
	get_viewport().set_input_as_handled()


func _girar(passo: int) -> void:
	_digitos[_cursor] = posmod(_digitos[_cursor] + passo, 10)
	som_tecla.play()
	_mostrar()


func _digitado() -> String:
	var texto := ""
	for digito in _digitos:
		texto += str(digito)
	return texto


func _confirmar() -> void:
	som_tecla.play()
	if _digitado() != codigo:
		som_erro.play()
		visor.text = "CÓDIGO INVÁLIDO"
		visor.add_theme_color_override("font_color", COR_ERRO)
		return
	visor.text = "ACESSO LIBERADO"
	visor.add_theme_color_override("font_color", COR_DIGITO)
	Progresso.marcar(marca)
	await get_tree().create_timer(0.8, true).timeout
	_fechar()
	Inventario.aviso.emit(aviso_aberto)


func _mostrar() -> void:
	for i in _rotulos.size():
		_rotulos[i].text = str(_digitos[i])
		_rotulos[i].add_theme_color_override("font_color", COR_ESCOLHIDO if i == _cursor else COR_DIGITO)
