class_name MusicaLabirinto
extends Node

@export var volume_tensao_db: float = -10.0
@export var volume_perseguicao_db: float = -6.0
@export var segundos_para_subir: float = 0.8
@export var segundos_para_descer: float = 4.0
@export var duracao_fade_inicial: float = 3.0

var perigo := 0.0
var _nivel := 0.0

@onready var tensao: AudioStreamPlayer = $Tensao
@onready var perseguicao: AudioStreamPlayer = $Perseguicao


func _ready() -> void:
	for camada in [tensao, perseguicao]:
		if camada.stream:
			camada.stream.set("loop", true)
	tensao.volume_db = -60.0
	perseguicao.volume_db = -80.0
	tensao.play()
	perseguicao.play()
	create_tween().tween_property(tensao, "volume_db", volume_tensao_db, duracao_fade_inicial)


func _process(delta: float) -> void:
	var tempo := segundos_para_subir if perigo > _nivel else segundos_para_descer
	_nivel = move_toward(_nivel, perigo, delta / tempo)
	perseguicao.volume_db = linear_to_db(maxf(_nivel, 0.0001)) + volume_perseguicao_db
