class_name MusicaFase
extends AudioStreamPlayer
## Trilha de fundo de uma fase. Instancie esta cena numa sala e ela toca sozinha.
##
## Entra com um fade-in de alguns segundos (a música não "estoura" no começo) e
## fica em loop. Para sozinha quando a sala sai da árvore, como a música do menu.
## A trilha padrão é a do gameplay (mistério, 48 BPM, 7/4), gerada por
## assets/modelagem/audio/gerar_trilha_gameplay.py.

## Volume final da música, em dB. Trilha de fundo: baixa, para não brigar com os passos.
@export var volume_final_db: float = -18.0
## Quanto tempo o fade-in leva, em segundos.
@export var duracao_fade: float = 4.0


func _ready() -> void:
	# Liga o loop pelo código (o mesmo que o menu faz), para não depender do painel Import.
	if stream:
		stream.set("loop", true)
	volume_db = -60.0
	play()
	var fade := create_tween()
	fade.tween_property(self, "volume_db", volume_final_db, duracao_fade)
