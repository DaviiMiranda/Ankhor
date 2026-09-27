extends Node2D

signal novo_jogo_pedido
signal continuar_pedido
signal opcoes_pedidas

@export var cena_novo_jogo: PackedScene
@export var energia_luz: float = 0.9
@export var oscilacao_luz: float = 0.15

@onready var luz: PointLight2D = $Mesa/Luz
@onready var botao_novo_jogo: Button = $Mesa/Menu/BotaoNovoJogo
@onready var botao_continuar: Button = $Mesa/Menu/BotaoContinuar
@onready var botao_opcoes: Button = $Mesa/Menu/BotaoOpcoes
@onready var botao_sair: Button = $Mesa/Menu/BotaoSair
@onready var musica: AudioStreamPlayer = $Musica

var _ruido := FastNoiseLite.new()
var _tempo := 0.0


func _ready() -> void:
	botao_novo_jogo.pressed.connect(_ao_apertar_novo_jogo)
	botao_continuar.pressed.connect(_ao_apertar_continuar)
	botao_opcoes.pressed.connect(_ao_apertar_opcoes)
	botao_sair.pressed.connect(_ao_apertar_sair)

	botao_continuar.disabled = true
	botao_novo_jogo.grab_focus()
	_ruido.frequency = 0.05

	if musica.stream:
		musica.stream.set("loop", true)


func _process(delta: float) -> void:
	_tempo += delta
	luz.energy = energia_luz + _ruido.get_noise_1d(_tempo * 60.0) * oscilacao_luz


func _ao_apertar_novo_jogo() -> void:
	novo_jogo_pedido.emit()
	Inventario.limpar()
	if cena_novo_jogo:
		get_tree().change_scene_to_packed(cena_novo_jogo)
	else:
		print("Menu: ainda não há cena de novo jogo configurada.")


func _ao_apertar_continuar() -> void:
	continuar_pedido.emit()


func _ao_apertar_opcoes() -> void:
	opcoes_pedidas.emit()
	print("Menu: tela de opções ainda não existe.")


func _ao_apertar_sair() -> void:
	get_tree().quit()
