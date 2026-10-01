extends CanvasLayer

const CENA_MENU := "res://cenas/menu_principal.tscn"

var aberta := false
var _tocar_ao_passar := false

@onready var menu: VBoxContainer = $Janela/Menu
@onready var opcoes: VBoxContainer = $Janela/Opcoes
@onready var confirmar: VBoxContainer = $Janela/Confirmar
@onready var botao_continuar: Button = $Janela/Menu/BotaoContinuar
@onready var botao_opcoes: Button = $Janela/Menu/BotaoOpcoes
@onready var botao_menu: Button = $Janela/Menu/BotaoMenu
@onready var botao_sair: Button = $Janela/Menu/BotaoSair
@onready var botao_tela_cheia: Button = $Janela/Opcoes/BotaoTelaCheia
@onready var botao_volume_master: Button = $Janela/Opcoes/BotaoVolumeMaster
@onready var botao_volume_musica: Button = $Janela/Opcoes/BotaoVolumeMusica
@onready var botao_volume_efeitos: Button = $Janela/Opcoes/BotaoVolumeEfeitos
@onready var botao_voltar_opcoes: Button = $Janela/Opcoes/BotaoVoltar
@onready var botao_sim: Button = $Janela/Confirmar/BotaoSim
@onready var botao_cancelar: Button = $Janela/Confirmar/BotaoCancelar
@onready var som_passar: AudioStreamPlayer = $SomPassar
@onready var som_clique: AudioStreamPlayer = $SomClique


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false
	botao_continuar.pressed.connect(fechar)
	botao_opcoes.pressed.connect(_mostrar.bind(opcoes, botao_tela_cheia))
	botao_menu.pressed.connect(_mostrar.bind(confirmar, botao_cancelar))
	botao_sair.pressed.connect(get_tree().quit)
	botao_tela_cheia.pressed.connect(Tela.alternar)
	botao_voltar_opcoes.pressed.connect(_mostrar.bind(menu, botao_opcoes))
	botao_sim.pressed.connect(_voltar_ao_menu)
	botao_cancelar.pressed.connect(_mostrar.bind(menu, botao_menu))
	for par in [[botao_volume_master, "master"], [botao_volume_musica, "musica"], [botao_volume_efeitos, "efeitos"]]:
		par[0].pressed.connect(Configuracoes.ciclar_volume.bind(par[1]))
		par[0].gui_input.connect(_ao_input_volume.bind(par[1]))
	for lista in [menu, opcoes, confirmar]:
		_ligar_sons(lista)
	Configuracoes.mudou.connect(_atualizar_textos)
	Tela.modo_alterado.connect(func(_tela_cheia: bool) -> void: _atualizar_textos())


func _unhandled_input(evento: InputEvent) -> void:
	if not evento.is_action_pressed("pausar"):
		return
	if aberta:
		_voltar_um_passo()
		get_viewport().set_input_as_handled()
	elif _pode_pausar():
		abrir()
		get_viewport().set_input_as_handled()


func _notification(o_que: int) -> void:
	if o_que == NOTIFICATION_APPLICATION_FOCUS_OUT and not aberta and _pode_pausar():
		abrir()


func _pode_pausar() -> bool:
	return is_node_ready() and not get_tree().paused and get_tree().current_scene is Sala


func abrir() -> void:
	aberta = true
	visible = true
	get_tree().paused = true
	_mostrar(menu, botao_continuar)


func fechar() -> void:
	aberta = false
	visible = false
	get_tree().paused = false


func _voltar_um_passo() -> void:
	if opcoes.visible:
		_mostrar(menu, botao_opcoes)
	elif confirmar.visible:
		_mostrar(menu, botao_menu)
	else:
		fechar()


func _mostrar(painel: Control, foco: Button) -> void:
	_tocar_ao_passar = false
	for p: Control in [menu, opcoes, confirmar]:
		p.visible = p == painel
	_atualizar_textos()
	foco.grab_focus()
	set_deferred("_tocar_ao_passar", true)


func _voltar_ao_menu() -> void:
	fechar()
	Checkpoints.limpar()
	get_tree().change_scene_to_file(CENA_MENU)


func _atualizar_textos() -> void:
	botao_tela_cheia.text = "Tela cheia: %s" % ("Sim" if Tela.eh_tela_cheia() else "Não")
	botao_volume_master.text = Configuracoes.texto_volume("master")
	botao_volume_musica.text = Configuracoes.texto_volume("musica")
	botao_volume_efeitos.text = Configuracoes.texto_volume("efeitos")


func _ao_input_volume(evento: InputEvent, tipo: String) -> void:
	if not evento.is_pressed() or evento.is_echo():
		return
	var passo := 0.0
	if evento.is_action_pressed("ui_left") or evento.is_action_pressed("mover_esquerda"):
		passo = -0.1
	elif evento.is_action_pressed("ui_right") or evento.is_action_pressed("mover_direita"):
		passo = 0.1
	if passo != 0.0:
		Configuracoes.ajustar_volume(tipo, passo)
		som_passar.play()
		get_viewport().set_input_as_handled()


func _ligar_sons(lista: Control) -> void:
	for filho in lista.get_children():
		if filho is Button:
			filho.mouse_entered.connect(_ao_passar_mouse.bind(filho))
			filho.focus_entered.connect(_ao_focar)
			filho.pressed.connect(som_clique.play)


func _ao_passar_mouse(botao: Button) -> void:
	if not botao.has_focus():
		botao.grab_focus()


func _ao_focar() -> void:
	if _tocar_ao_passar:
		som_passar.play()
