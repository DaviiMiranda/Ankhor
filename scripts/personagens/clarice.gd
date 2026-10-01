extends Node2D

const DIGITANDO := preload("res://assets/sprites/personagens/clarice/clarice_digitando.png")
const VIRANDO := preload("res://assets/sprites/personagens/clarice/clarice_virando.png")
const OLHANDO := preload("res://assets/sprites/personagens/clarice/clarice_olhando.png")
const QUADROS_DIGITANDO := 8
const QUADROS_VIRANDO := 5
const QUADROS_OLHANDO := 6

@export var distancia_para_virar: float = 80.0
@export var quadros_por_segundo_digitando: float = 8.0
@export var quadros_por_segundo_virando: float = 12.0
@export var quadros_por_segundo_olhando: float = 3.0

var _giro := 0.0
var _tempo := 0.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var teclado: AudioStreamPlayer2D = $Teclado


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_mostrar(DIGITANDO, QUADROS_DIGITANDO, 0)


func _process(delta: float) -> void:
	_tempo += delta
	var alvo := float(QUADROS_VIRANDO - 1) if _deve_olhar() else 0.0
	_giro = move_toward(_giro, alvo, quadros_por_segundo_virando * delta)
	if _giro <= 0.0:
		_mostrar(DIGITANDO, QUADROS_DIGITANDO, int(_tempo * quadros_por_segundo_digitando) % QUADROS_DIGITANDO)
	elif _giro >= QUADROS_VIRANDO - 1:
		_mostrar(OLHANDO, QUADROS_OLHANDO, int(_tempo * quadros_por_segundo_olhando) % QUADROS_OLHANDO)
	else:
		_mostrar(VIRANDO, QUADROS_VIRANDO, roundi(_giro))
	_tocar_teclado(_giro <= 0.0 and not get_tree().paused)


func _deve_olhar() -> bool:
	if Dialogos.ativo:
		return true
	var gabriel := get_tree().get_first_node_in_group("jogador") as Node2D
	return gabriel != null and gabriel.global_position.distance_to(global_position) < distancia_para_virar


func _mostrar(tira: Texture2D, quadros: int, quadro: int) -> void:
	if sprite.texture != tira:
		sprite.frame = 0
		sprite.texture = tira
		sprite.hframes = quadros
	sprite.frame = quadro


func _tocar_teclado(tocar: bool) -> void:
	if tocar and not teclado.playing:
		teclado.play()
	elif not tocar and teclado.playing:
		teclado.stop()
