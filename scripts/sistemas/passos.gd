class_name Passos
extends AudioStreamPlayer2D
## O som dos passos do Gabriel. Fica dentro da cena dele (gabriel.tscn) e
## toca um passo a cada sinal passo_dado.
##
## O som em si é um AudioStreamRandomizer (ver o painel Inspector, "Stream"):
## ele guarda as 6 variações de gabriel_passo_ceramica_XX.wav e, a cada
## play(), sorteia uma (sem repetir a anterior) e muda um pouco a altura e o
## volume. Assim os passos não soam como uma máquina.
## Os sons são gerados por assets/modelagem/audio/gerar_efeitos_gabriel.py.

## Volume de cada jeito de andar, em dB (0 = volume do arquivo).
@export var volume_andar_db: float = -10.0
@export var volume_correr_db: float = -3.0
## Agachado, os robôs não ouvem (docs/mecanicas/movimentacao_e_terreno.md),
## mas o jogador ouve bem baixinho, para sentir que está andando.
@export var volume_agachado_db: float = -24.0
## Correndo, o pé bate mais rápido e com mais força: a altura sobe um pouco.
@export var altura_correr: float = 1.08


## Ligado ao sinal passo_dado do Gabriel (a ligação está em gabriel.tscn).
func tocar(correndo: bool, agachado: bool) -> void:
	if agachado:
		volume_db = volume_agachado_db
		pitch_scale = 0.95
	elif correndo:
		volume_db = volume_correr_db
		pitch_scale = altura_correr
	else:
		volume_db = volume_andar_db
		pitch_scale = 1.0
	play()
