extends CanvasLayer

const TOM_VOZ := {"Gabriel": 0.85}
const PAUSA_PONTUACAO := {".": 0.22, "!": 0.22, "?": 0.22, ",": 0.08, "…": 0.3}

@export var letras_por_segundo: float = 36.0
@export var letras_por_bip: int = 3
@export var duracao_fade: float = 0.25

var _tempo := 0.0
var _pausa := 0.0
var _quem := ""
var _fade: Tween

@onready var faixa: Control = $Faixa
@onready var texto: Label = $Faixa/Texto
@onready var dica: Label = $Faixa/Dica
@onready var bip: AudioStreamPlayer = $Bip


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	faixa.modulate.a = 0.0
	faixa.visible = false
	Dialogos.fala_mostrada.connect(_mostrar_fala)
	Dialogos.terminou.connect(_fechar)


func _mostrar_fala(quem: String, fala: String, _retrato: Texture2D) -> void:
	_quem = quem
	texto.text = fala
	texto.visible_characters = 0
	_tempo = 0.0
	_pausa = 0.0
	faixa.visible = true
	_animar_transparencia(1.0)


func _fechar(_caminho: String) -> void:
	_animar_transparencia(0.0).tween_callback(faixa.hide)


func _animar_transparencia(alvo: float) -> Tween:
	if _fade:
		_fade.kill()
	_fade = create_tween()
	_fade.tween_property(faixa, "modulate:a", alvo, duracao_fade)
	return _fade


func _process(delta: float) -> void:
	if not faixa.visible:
		return
	dica.visible = _terminou_de_escrever() and int(Time.get_ticks_msec() / 400.0) % 2 == 0
	if _terminou_de_escrever():
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
	if not faixa.visible or not Dialogos.ativo:
		return
	if evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		if _terminou_de_escrever():
			Dialogos.avancar()
		else:
			texto.visible_characters = -1
		get_viewport().set_input_as_handled()
