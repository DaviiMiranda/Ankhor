extends CanvasLayer

const CORES_NOMES := {
	"Clarice": Color(0.45, 0.86, 0.82),
	"Gabriel": Color(0.93, 0.55, 0.47),
}
const COR_NOME_PADRAO := Color(0.95, 0.88, 0.7)
const COR_ESCOLHA := Color(0.95, 0.88, 0.7)
const COR_ESCOLHA_APAGADA := Color(0.55, 0.53, 0.5)
const TOM_VOZ := {"Clarice": 1.3, "Gabriel": 0.85}
const PAUSA_PONTUACAO := {".": 0.22, "!": 0.22, "?": 0.22, ",": 0.08, "…": 0.3}

@export var letras_por_segundo: float = 42.0
@export var letras_por_bip: int = 2

var _tempo := 0.0
var _pausa := 0.0
var _opcoes: Array = []
var _escolhida := 0
var _quem := ""

@onready var janela: NinePatchRect = $Janela
@onready var moldura_retrato: ColorRect = $Janela/MolduraRetrato
@onready var retrato: TextureRect = $Janela/MolduraRetrato/Retrato
@onready var nome: Label = $Janela/Nome
@onready var texto: Label = $Janela/Texto
@onready var lista_escolhas: VBoxContainer = $Janela/Escolhas
@onready var dica: Label = $Janela/Dica
@onready var bip: AudioStreamPlayer = $Bip


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false
	Dialogos.fala_mostrada.connect(_mostrar_fala)
	Dialogos.escolhas_mostradas.connect(_mostrar_escolhas)
	Dialogos.terminou.connect(_fechar)


func _mostrar_fala(quem: String, fala: String, imagem: Texture2D) -> void:
	visible = true
	_quem = quem
	_opcoes = []
	lista_escolhas.visible = false
	texto.visible = true
	moldura_retrato.visible = imagem != null
	retrato.texture = imagem
	var margem := 52.0 if imagem else 8.0
	nome.position.x = margem
	texto.position.x = margem
	texto.size.x = janela.size.x - margem - 8.0
	nome.text = quem
	nome.add_theme_color_override("font_color", CORES_NOMES.get(quem, COR_NOME_PADRAO))
	texto.text = fala
	texto.visible_characters = 0
	_tempo = 0.0
	_pausa = 0.0


func _mostrar_escolhas(opcoes: Array) -> void:
	_opcoes = opcoes
	_escolhida = 0
	texto.visible = false
	lista_escolhas.visible = true
	lista_escolhas.position.x = texto.position.x
	for filho in lista_escolhas.get_children():
		lista_escolhas.remove_child(filho)
		filho.queue_free()
	for opcao: String in opcoes:
		var rotulo := Label.new()
		rotulo.text = opcao
		lista_escolhas.add_child(rotulo)
	_pintar_escolhas()


func _pintar_escolhas() -> void:
	for i in _opcoes.size():
		var rotulo := lista_escolhas.get_child(i) as Label
		if rotulo == null:
			continue
		var marcada := i == _escolhida
		rotulo.text = ("> " if marcada else "  ") + str(_opcoes[i])
		rotulo.add_theme_color_override("font_color", COR_ESCOLHA if marcada else COR_ESCOLHA_APAGADA)


func _fechar(_caminho: String) -> void:
	visible = false


func _process(delta: float) -> void:
	if not visible:
		return
	dica.visible = _terminou_de_escrever() and _opcoes.is_empty() and int(Time.get_ticks_msec() / 400.0) % 2 == 0
	if _terminou_de_escrever() or not _opcoes.is_empty():
		return
	if _pausa > 0.0:
		_pausa -= delta
		return
	_tempo += delta * letras_por_segundo
	while _tempo >= 1.0 and not _terminou_de_escrever():
		_tempo -= 1.0
		texto.visible_characters += 1
		var letra := texto.text[texto.visible_characters - 1]
		if texto.visible_characters % letras_por_bip == 0 and letra != " ":
			bip.pitch_scale = TOM_VOZ.get(_quem, 1.0) * randf_range(0.95, 1.05)
			bip.play()
		if PAUSA_PONTUACAO.has(letra):
			_pausa = PAUSA_PONTUACAO[letra]
			_tempo = 0.0
			break


func _terminou_de_escrever() -> bool:
	return texto.visible_characters < 0 or texto.visible_characters >= texto.text.length()


func _unhandled_input(evento: InputEvent) -> void:
	if not visible or not Dialogos.ativo:
		return
	if not _opcoes.is_empty():
		if evento.is_action_pressed("mover_cima") or evento.is_action_pressed("ui_up"):
			_escolhida = posmod(_escolhida - 1, _opcoes.size())
			_pintar_escolhas()
		elif evento.is_action_pressed("mover_baixo") or evento.is_action_pressed("ui_down"):
			_escolhida = posmod(_escolhida + 1, _opcoes.size())
			_pintar_escolhas()
		elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
			Dialogos.escolher(_escolhida)
		get_viewport().set_input_as_handled()
		return
	if evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		if _terminou_de_escrever():
			Dialogos.avancar()
		else:
			texto.visible_characters = -1
		get_viewport().set_input_as_handled()
