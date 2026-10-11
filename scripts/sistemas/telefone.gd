class_name Telefone
extends Interagivel

const SEGUNDOS_DO_CICLO := 6.0
const SEGUNDOS_TOCANDO := 2.4

@export var marca_toque: String = "saida_tentada"
@export var marca_ao_atender: String = "saida_destrancada"
@export var ligacao: Transmissao
@export var aviso_mudo: String = "O telefone está mudo. Mas a linha parece viva."

var _base := Vector2.ZERO

@onready var sprite: Sprite2D = $Sprite2D
@onready var toque: AudioStreamPlayer2D = $Toque


func _ready() -> void:
	super()
	_base = sprite.position
	Progresso.mudou.connect(_atualizar.unbind(1))
	_atualizar()


func tocando() -> bool:
	return Progresso.tem(marca_toque) and not Progresso.tem(marca_ao_atender)


func interagir() -> void:
	if not tocando():
		Inventario.aviso.emit(aviso_mudo)
		return
	Progresso.marcar(marca_ao_atender)
	Radio.transmitir(ligacao)


func _atualizar() -> void:
	texto_acao = "Atender" if tocando() else "Telefone"
	if tocando() and not toque.playing:
		toque.play()
	elif not tocando():
		toque.stop()


func _process(_delta: float) -> void:
	var tremendo := tocando() and fmod(toque.get_playback_position(), SEGUNDOS_DO_CICLO) < SEGUNDOS_TOCANDO
	sprite.position = _base + (Vector2(randi_range(-1, 1), 0) if tremendo else Vector2.ZERO)
