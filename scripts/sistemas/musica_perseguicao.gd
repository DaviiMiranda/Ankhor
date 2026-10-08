class_name MusicaPerseguicao
extends AudioStreamPlayer

## Toca a trilha de perseguição dinamicamente quando um robô persegue o jogador.
## Sobe o volume suavemente (fade in) durante a perseguição e desce (fade out)
## quando o jogador consegue escapar, reduzindo temporariamente o volume da
## trilha ambiente de exploração.

@export var volume_perseguicao_db: float = -6.0
@export var segundos_para_subir: float = 0.6
@export var segundos_para_descer: float = 3.5

var perigo: float = 0.0
var _nivel: float = 0.0
var _robos_perseguindo: Dictionary = {}
var _musica_ambiente: AudioStreamPlayer = null
var _volume_ambiente_original: float = -18.0


func _ready() -> void:
	bus = &"Musica"
	if stream:
		stream.set("loop", true)
	volume_db = -80.0
	play()
	_conectar_robos.call_deferred()
	_buscar_musica_ambiente.call_deferred()


func _buscar_musica_ambiente() -> void:
	var sala := get_parent()
	if sala:
		for filho in sala.get_children():
			if filho is AudioStreamPlayer and filho != self and filho.bus == &"Musica":
				_musica_ambiente = filho
				if "volume_final_db" in filho:
					_volume_ambiente_original = filho.volume_final_db
				else:
					_volume_ambiente_original = filho.volume_db
				break


func _conectar_robos() -> void:
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo:
			if not robo.jogador_detectado.is_connected(_ao_robo_detectar):
				robo.jogador_detectado.connect(_ao_robo_detectar)
			if not robo.jogador_perdido.is_connected(_ao_robo_perder):
				robo.jogador_perdido.connect(_ao_robo_perder)


func _ao_robo_detectar(robo: Robo) -> void:
	_robos_perseguindo[robo] = true
	perigo = 1.0


func _ao_robo_perder(robo: Robo) -> void:
	_robos_perseguindo.erase(robo)
	if _robos_perseguindo.is_empty():
		perigo = 0.0


func _process(delta: float) -> void:
	var tempo := segundos_para_subir if perigo > _nivel else segundos_para_descer
	_nivel = move_toward(_nivel, perigo, delta / tempo)
	volume_db = linear_to_db(maxf(_nivel, 0.0001)) + volume_perseguicao_db

	if _musica_ambiente and is_instance_valid(_musica_ambiente) and _nivel > 0.001:
		var vol_alvo: float = lerpf(_volume_ambiente_original, -45.0, _nivel)
		_musica_ambiente.volume_db = vol_alvo
