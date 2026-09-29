extends CanvasLayer

@export var letras_por_segundo: float = 32.0
@export var pausa_depois_da_fala: float = 1.8

var _fila: Array[Transmissao] = []
var _atual: Transmissao
var _indice := 0
var _tempo := 0.0
var _duracao := 0.0

@onready var caixa: Control = $Caixa
@onready var falante: Label = $Caixa/Falante
@onready var fala: Label = $Caixa/Fala
@onready var chiado: AudioStreamPlayer = $Chiado
@onready var clique: AudioStreamPlayer = $Clique
@onready var voz: AudioStreamPlayer = $Voz


func _ready() -> void:
	Radio.transmissao_pedida.connect(_ao_pedir)
	caixa.hide()


func _process(delta: float) -> void:
	if _atual == null:
		return
	_tempo += delta
	fala.visible_characters = int(_tempo * letras_por_segundo)
	if _tempo < _duracao:
		return
	_indice += 1
	if _indice < _atual.falas.size():
		_mostrar_fala()
	else:
		_terminar()


func _ao_pedir(transmissao: Transmissao) -> void:
	_fila.append(transmissao)
	if _atual == null:
		_proxima_transmissao()


func _proxima_transmissao() -> void:
	if _fila.is_empty():
		_atual = null
		caixa.hide()
		chiado.stop()
		return
	_atual = _fila.pop_front()
	_indice = 0
	falante.text = _atual.falante
	caixa.show()
	clique.play()
	chiado.play()
	_mostrar_fala()


func _mostrar_fala() -> void:
	fala.text = _atual.falas[_indice]
	fala.visible_characters = 0
	_tempo = 0.0
	_duracao = fala.text.length() / letras_por_segundo + pausa_depois_da_fala
	voz.stop()
	if _indice < _atual.vozes.size() and _atual.vozes[_indice]:
		voz.stream = _atual.vozes[_indice]
		voz.play()
		_duracao = maxf(_duracao, voz.stream.get_length() + 0.4)


func _terminar() -> void:
	clique.play()
	Caderno.anotar(_atual.id, _atual.titulo_anotacao, _atual.anotacao)
	_proxima_transmissao()
