class_name ZumbidoDaCarga
extends AudioStreamPlayer

const SOM := preload("res://assets/audio/efeitos/objetos/celula_zumbido.wav")
const ALCANCE_RUIDO := 8
const INTERVALO_RUIDO := 1.5
const AVISO := "A Célula pesa e zumbe: sem correr, e os robôs ouvem. G larga no chão."
const AVISO_SEM_CORRER := "Com a Célula na mochila não dá para correr. G larga no chão."

static var _ja_avisou := false

var _proximo := 0.0


func _ready() -> void:
	stream = SOM
	bus = &"Efeitos"
	volume_db = -14.0
	finished.connect(play)


func _physics_process(delta: float) -> void:
	var carregando := Inventario.carregando_peso()
	if carregando != playing:
		if carregando:
			play()
			_avisar()
		else:
			stop()
	if not carregando:
		return
	if Input.is_action_just_pressed("correr") and _dono_controla():
		Inventario.aviso.emit(AVISO_SEM_CORRER)
	_proximo -= delta
	if _proximo <= 0.0:
		_proximo = INTERVALO_RUIDO
		var dono := get_parent() as Node2D
		Robo.fazer_barulho(get_tree(), dono.global_position, ALCANCE_RUIDO)


func _dono_controla() -> bool:
	var gabriel := get_parent() as Gabriel
	return gabriel == null or gabriel.jogador_controla


func _avisar() -> void:
	if not _ja_avisou:
		_ja_avisou = true
		Inventario.aviso.emit(AVISO)
