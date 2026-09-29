extends Node2D

signal novo_jogo_pedido
signal continuar_pedido
signal opcoes_pedidas

@export var cena_novo_jogo: PackedScene
@export var fases: Array[Fase] = []
@export var energia_luz: float = 0.9
@export var oscilacao_luz: float = 0.15
@export var espera_clique: float = 0.18

@onready var luz: PointLight2D = $Mesa/Luz
@onready var menu: VBoxContainer = $Mesa/Menu
@onready var lista_fases: VBoxContainer = $Mesa/Fases
@onready var botao_fases: Button = $Mesa/Menu/BotaoFases
@onready var botao_novo_jogo: Button = $Mesa/Menu/BotaoNovoJogo
@onready var botao_continuar: Button = $Mesa/Menu/BotaoContinuar
@onready var botao_opcoes: Button = $Mesa/Menu/BotaoOpcoes
@onready var botao_sair: Button = $Mesa/Menu/BotaoSair
@onready var musica: AudioStreamPlayer = $Musica
@onready var som_passar: AudioStreamPlayer = $SomPassar
@onready var som_clique: AudioStreamPlayer = $SomClique

var _ruido := FastNoiseLite.new()
var _tempo := 0.0
var _tocar_ao_passar := false


func _ready() -> void:
	botao_novo_jogo.pressed.connect(_ao_apertar_novo_jogo)
	botao_fases.pressed.connect(_mostrar_fases.bind(true))
	botao_continuar.pressed.connect(_ao_apertar_continuar)
	botao_opcoes.pressed.connect(_ao_apertar_opcoes)
	botao_sair.pressed.connect(_ao_apertar_sair)

	botao_continuar.disabled = true
	_montar_lista_fases()
	lista_fases.hide()
	_ligar_sons(menu)
	_ligar_sons(lista_fases)
	botao_novo_jogo.grab_focus()
	_ruido.frequency = 0.05
	set_deferred("_tocar_ao_passar", true)

	if musica.stream:
		musica.stream.set("loop", true)


func _process(delta: float) -> void:
	_tempo += delta
	luz.energy = energia_luz + _ruido.get_noise_1d(_tempo * 60.0) * oscilacao_luz


func _unhandled_input(evento: InputEvent) -> void:
	if lista_fases.visible and evento.is_action_pressed("ui_cancel"):
		_mostrar_fases(false)
		get_viewport().set_input_as_handled()


func _montar_lista_fases() -> void:
	for fase in fases:
		var botao := Button.new()
		botao.text = fase.nome
		botao.disabled = not fase.pronta()
		botao.pressed.connect(_jogar_fase.bind(fase))
		lista_fases.add_child(botao)
	var voltar := Button.new()
	voltar.text = "Voltar"
	voltar.pressed.connect(_mostrar_fases.bind(false))
	lista_fases.add_child(voltar)


func _mostrar_fases(mostrar: bool) -> void:
	menu.visible = not mostrar
	lista_fases.visible = mostrar
	_tocar_ao_passar = false
	if not mostrar:
		botao_fases.grab_focus()
	else:
		for filho in lista_fases.get_children():
			if filho is Button and not filho.disabled:
				filho.grab_focus()
				break
	set_deferred("_tocar_ao_passar", true)


func _ligar_sons(lista: Control) -> void:
	for filho in lista.get_children():
		if filho is Button:
			filho.mouse_entered.connect(_ao_passar_mouse.bind(filho))
			filho.focus_entered.connect(_ao_focar)
			filho.pressed.connect(som_clique.play)


func _ao_passar_mouse(botao: Button) -> void:
	if not botao.disabled and not botao.has_focus():
		botao.grab_focus()


func _ao_focar() -> void:
	if _tocar_ao_passar:
		som_passar.play()


func _esperar_clique() -> void:
	await get_tree().create_timer(espera_clique).timeout


func _comecar_do_zero() -> void:
	Inventario.limpar()
	Caderno.limpar()
	Radio.limpar()
	Vida.limpar()
	Checkpoints.limpar()


func _jogar_fase(fase: Fase) -> void:
	_comecar_do_zero()
	await _esperar_clique()
	get_tree().change_scene_to_file(fase.cena)


func _ao_apertar_novo_jogo() -> void:
	novo_jogo_pedido.emit()
	_comecar_do_zero()
	await _esperar_clique()
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
	await _esperar_clique()
	get_tree().quit()
