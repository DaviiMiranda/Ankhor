class_name WalkmanNoChao
extends Interagivel

const ALCANCE_RUIDO := 20
const INTERVALO_RUIDO := 1.0

@export var segundos_tocando: float = 15.0

var item: Item
var _restante := 0.0
var _proximo_ruido := 0.0

@onready var musica: AudioStreamPlayer2D = $Musica
@onready var sprite: Sprite2D = $Sprite2D


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	if item:
		sprite.texture = item.sprite_chao
	musica.finished.connect(_repetir)


func tocar() -> void:
	_restante = segundos_tocando
	_proximo_ruido = 0.0
	musica.play()
	texto_acao = "Pegar o walkman"


func _physics_process(delta: float) -> void:
	if Engine.is_editor_hint() or _restante <= 0.0:
		return
	_restante -= delta
	_proximo_ruido -= delta
	if _proximo_ruido <= 0.0:
		_proximo_ruido = INTERVALO_RUIDO
		Robo.fazer_barulho(get_tree(), global_position, ALCANCE_RUIDO)
	if _restante <= 0.0:
		musica.stop()


func interagir() -> void:
	if Inventario.adicionar(item):
		queue_free()


func _repetir() -> void:
	if _restante > 0.0:
		musica.play()
