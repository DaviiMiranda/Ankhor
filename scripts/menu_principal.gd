extends Node2D

signal novo_jogo_pedido
signal continuar_pedido
signal opcoes_pedidas

const FASE_TESTE := preload("res://dados/fases/teste.tres")
const COR_TESTE := Color(1.0, 0.85, 0.2)
const SEM_DATA := "Espaço livre"

@export var cena_novo_jogo: PackedScene
@export var fases: Array[Fase] = []
@export var energia_luz: float = 0.9
@export var oscilacao_luz: float = 0.15
@export var espera_clique: float = 0.18
@onready var luz: PointLight2D = $Monitor/Luz
@onready var menu: VBoxContainer = $Monitor/Menu
@onready var lista_fases: VBoxContainer = $Monitor/Fases
@onready var rolagem_fases: ScrollContainer = $Monitor/Fases/Rolagem
@onready var botoes_fases: VBoxContainer = $Monitor/Fases/Rolagem/Lista
@onready var botao_fases: Button = $Monitor/Menu/BotaoFases
@onready var botao_novo_jogo: Button = $Monitor/Menu/BotaoNovoJogo
@onready var botao_continuar: Button = $Monitor/Menu/BotaoContinuar
@onready var botao_opcoes: Button = $Monitor/Menu/BotaoOpcoes
@onready var botao_sair: Button = $Monitor/Menu/LinhaFinal/BotaoSair
@onready var linha_final: HBoxContainer = $Monitor/Menu/LinhaFinal
@onready var botao_creditos: Button = $Monitor/Menu/LinhaFinal/BotaoCreditos
@onready var musica: AudioStreamPlayer = $Musica
@onready var som_passar: AudioStreamPlayer = $SomPassar
@onready var som_clique: AudioStreamPlayer = $SomClique

@onready var painel_carregar: VBoxContainer = $Monitor/Carregar
@onready var rolagem_carregar: ScrollContainer = $Monitor/Carregar/Rolagem
@onready var botoes_carregar: VBoxContainer = $Monitor/Carregar/Rolagem/Lista
@onready var botao_voltar_carregar: Button = $Monitor/Carregar/Rolagem/Lista/BotaoVoltarCarregar
@onready var detalhe_carregar: Label = $Monitor/Carregar/Detalhe

@onready var painel_opcoes: VBoxContainer = $Monitor/Opcoes
@onready var rolagem_opcoes: ScrollContainer = $Monitor/Opcoes/Rolagem
@onready var botoes_opcoes: VBoxContainer = $Monitor/Opcoes/Rolagem/Lista
@onready var botao_tela_cheia: Button = $Monitor/Opcoes/Rolagem/Lista/BotaoTelaCheia
@onready var botao_efeito_crt: Button = $Monitor/Opcoes/Rolagem/Lista/BotaoEfeitoCrt
@onready var botao_volume_master: Button = $Monitor/Opcoes/Rolagem/Lista/BotaoVolumeMaster
@onready var botao_volume_musica: Button = $Monitor/Opcoes/Rolagem/Lista/BotaoVolumeMusica
@onready var botao_volume_sfx: Button = $Monitor/Opcoes/Rolagem/Lista/BotaoVolumeSfx
@onready var botao_controles: Button = $Monitor/Opcoes/Rolagem/Lista/BotaoControles
@onready var botao_voltar_opcoes: Button = $Monitor/Opcoes/Rolagem/Lista/BotaoVoltarOpcoes

@onready var painel_controles: VBoxContainer = $Monitor/Controles
@onready var rolagem_controles: ScrollContainer = $Monitor/Controles/Rolagem
@onready var botoes_controles: VBoxContainer = $Monitor/Controles/Rolagem/Lista
@onready var botao_voltar_controles: Button = $Monitor/Controles/Rolagem/Lista/BotaoVoltarControles
@onready var painel_creditos: VBoxContainer = $Monitor/Creditos
@onready var rolagem_creditos: ScrollContainer = $Monitor/Creditos/Rolagem
@onready var botoes_creditos: VBoxContainer = $Monitor/Creditos/Rolagem/Lista
@onready var botao_voltar_creditos: Button = $Monitor/Creditos/Rolagem/Lista/BotaoVoltarCreditos
@onready var efeito_crt_rect: ColorRect = $Monitor/EfeitoCRT

var _ruido := FastNoiseLite.new()
var _tempo := 0.0
var _tocar_ao_passar := false
var _botoes_dos_espacos: Array[Button] = []


func _ready() -> void:
	TempoDeJogo.parar()
	botao_novo_jogo.pressed.connect(_ao_apertar_novo_jogo)
	botao_fases.pressed.connect(_mostrar_fases.bind(true))
	botao_continuar.pressed.connect(_mostrar_carregar.bind(true))
	botao_voltar_carregar.pressed.connect(_mostrar_carregar.bind(false))
	botao_opcoes.pressed.connect(_ao_apertar_opcoes)
	botao_creditos.pressed.connect(_mostrar_creditos.bind(true))
	botao_sair.pressed.connect(_ao_apertar_sair)

	botao_voltar_opcoes.pressed.connect(_mostrar_opcoes.bind(false))
	botao_controles.pressed.connect(_mostrar_controles.bind(true))
	botao_voltar_controles.pressed.connect(_mostrar_controles.bind(false))
	botao_voltar_creditos.pressed.connect(_mostrar_creditos.bind(false))

	botao_tela_cheia.pressed.connect(_ao_alternar_tela_cheia)
	botao_efeito_crt.pressed.connect(_ao_alternar_efeito_crt)

	botao_volume_master.pressed.connect(_ao_clicar_volume.bind("master"))
	botao_volume_musica.pressed.connect(_ao_clicar_volume.bind("musica"))
	botao_volume_sfx.pressed.connect(_ao_clicar_volume.bind("efeitos"))

	botao_volume_master.gui_input.connect(_ao_input_volume.bind("master"))
	botao_volume_musica.gui_input.connect(_ao_input_volume.bind("musica"))
	botao_volume_sfx.gui_input.connect(_ao_input_volume.bind("efeitos"))

	botao_continuar.disabled = not Salvamento.existe()
	_montar_lista_fases()
	_montar_lista_carregar()
	lista_fases.hide()
	painel_carregar.hide()
	painel_opcoes.hide()
	painel_controles.hide()
	painel_creditos.hide()

	_ligar_sons(menu)
	_ligar_sons(linha_final)
	_ligar_sons(botoes_fases)
	_ligar_sons(botoes_carregar)
	_ligar_sons(botoes_opcoes)
	_ligar_sons(botoes_controles)
	_ligar_sons(botoes_creditos)

	Tela.modo_alterado.connect(func(_tc: bool) -> void: _atualizar_textos_opcoes())
	Configuracoes.mudou.connect(_ao_mudar_configuracoes)
	_ao_mudar_configuracoes()

	for rolagem in [rolagem_fases, rolagem_carregar, rolagem_opcoes, rolagem_controles, rolagem_creditos]:
		rolagem.get_v_scroll_bar().custom_minimum_size.x = 4.0

	botao_novo_jogo.grab_focus()
	_ruido.frequency = 0.05
	set_deferred("_tocar_ao_passar", true)

	if musica.stream:
		musica.stream.set("loop", true)


func _process(delta: float) -> void:
	_tempo += delta
	luz.energy = energia_luz + _ruido.get_noise_1d(_tempo * 60.0) * oscilacao_luz


func _unhandled_input(evento: InputEvent) -> void:
	if not evento.is_action_pressed("ui_cancel"):
		return
	if painel_creditos.visible:
		_mostrar_creditos(false)
		get_viewport().set_input_as_handled()
	elif painel_controles.visible:
		_mostrar_controles(false)
		get_viewport().set_input_as_handled()
	elif painel_opcoes.visible:
		_mostrar_opcoes(false)
		get_viewport().set_input_as_handled()
	elif lista_fases.visible:
		_mostrar_fases(false)
		get_viewport().set_input_as_handled()
	elif painel_carregar.visible:
		_mostrar_carregar(false)
		get_viewport().set_input_as_handled()


func _montar_lista_fases() -> void:
	var lista := fases.duplicate()
	if OS.has_feature("editor"):
		lista.push_front(FASE_TESTE)
	for fase in lista:
		var botao := Button.new()
		botao.text = fase.nome
		botao.disabled = not fase.pronta()
		botao.pressed.connect(_jogar_fase.bind(fase))
		if fase == FASE_TESTE:
			_pintar(botao, COR_TESTE)
		botoes_fases.add_child(botao)
	var voltar := Button.new()
	voltar.text = "Voltar"
	voltar.pressed.connect(_mostrar_fases.bind(false))
	botoes_fases.add_child(voltar)


func _montar_lista_carregar() -> void:
	for espaco in Salvamento.espacos():
		var botao := Button.new()
		botao.alignment = HORIZONTAL_ALIGNMENT_LEFT
		botao.clip_text = true
		botao.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
		botao.pressed.connect(_carregar.bind(espaco))
		botao.focus_entered.connect(_mostrar_data_do_espaco.bind(espaco))
		botoes_carregar.add_child(botao)
		botoes_carregar.move_child(botao, botao_voltar_carregar.get_index())
		_botoes_dos_espacos.append(botao)
	botao_voltar_carregar.focus_entered.connect(_mostrar_data_do_espaco.bind(0))
	_atualizar_lista_carregar()


func _atualizar_lista_carregar() -> void:
	for i in _botoes_dos_espacos.size():
		_botoes_dos_espacos[i].text = Salvamento.texto_do_espaco(i + 1)
		_botoes_dos_espacos[i].disabled = not Salvamento.ocupado(i + 1)


func _mostrar_data_do_espaco(espaco: int) -> void:
	var data := Salvamento.data_salva(espaco) if espaco != 0 else ""
	detalhe_carregar.text = SEM_DATA if espaco != 0 and data.is_empty() else data


func _pintar(botao: Button, cor: Color) -> void:
	for estilo in ["font_color", "font_hover_color", "font_focus_color", "font_pressed_color", "font_hover_pressed_color"]:
		botao.add_theme_color_override(estilo, cor)


func _mostrar_fases(mostrar: bool) -> void:
	menu.visible = not mostrar
	lista_fases.visible = mostrar
	_tocar_ao_passar = false
	if not mostrar:
		botao_fases.grab_focus()
	else:
		for filho in botoes_fases.get_children():
			if filho is Button and not filho.disabled:
				filho.grab_focus()
				break
		rolagem_fases.set_deferred("scroll_vertical", 0)
	set_deferred("_tocar_ao_passar", true)


func _mostrar_carregar(mostrar: bool) -> void:
	menu.visible = not mostrar
	painel_carregar.visible = mostrar
	_tocar_ao_passar = false
	if not mostrar:
		botao_continuar.grab_focus()
	else:
		_atualizar_lista_carregar()
		var mais_recente := Salvamento.espaco_mais_recente()
		var foco := _botoes_dos_espacos[mais_recente - 1] if mais_recente != 0 else botao_voltar_carregar
		foco.grab_focus()
		rolagem_carregar.set_deferred("scroll_vertical", 0)
	set_deferred("_tocar_ao_passar", true)


func _mostrar_opcoes(mostrar: bool) -> void:
	menu.visible = not mostrar
	painel_opcoes.visible = mostrar
	_tocar_ao_passar = false
	if not mostrar:
		botao_opcoes.grab_focus()
	else:
		_atualizar_textos_opcoes()
		botao_tela_cheia.grab_focus()
		rolagem_opcoes.set_deferred("scroll_vertical", 0)
	set_deferred("_tocar_ao_passar", true)


func _mostrar_controles(mostrar: bool) -> void:
	painel_opcoes.visible = not mostrar
	painel_controles.visible = mostrar
	_tocar_ao_passar = false
	if not mostrar:
		botao_controles.grab_focus()
	else:
		botao_voltar_controles.grab_focus()
		rolagem_controles.set_deferred("scroll_vertical", 0)
	set_deferred("_tocar_ao_passar", true)


func _mostrar_creditos(mostrar: bool) -> void:
	menu.visible = not mostrar
	painel_creditos.visible = mostrar
	_tocar_ao_passar = false
	if not mostrar:
		botao_creditos.grab_focus()
	else:
		botao_voltar_creditos.grab_focus()
		rolagem_creditos.set_deferred("scroll_vertical", 0)
	set_deferred("_tocar_ao_passar", true)


func _ao_mudar_configuracoes() -> void:
	efeito_crt_rect.visible = Configuracoes.efeito_crt
	_atualizar_textos_opcoes()


func _ao_alternar_tela_cheia() -> void:
	Tela.alternar()
	_atualizar_textos_opcoes()


func _ao_alternar_efeito_crt() -> void:
	Configuracoes.efeito_crt = not Configuracoes.efeito_crt


func _ao_clicar_volume(tipo: String) -> void:
	Configuracoes.ciclar_volume(tipo)


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


func _atualizar_textos_opcoes() -> void:
	botao_tela_cheia.text = "Tela cheia: %s" % ("Sim" if Tela.eh_tela_cheia() else "Não")
	botao_efeito_crt.text = "Efeito CRT: %s" % ("Sim" if Configuracoes.efeito_crt else "Não")
	botao_volume_master.text = Configuracoes.texto_volume("master")
	botao_volume_musica.text = Configuracoes.texto_volume("musica")
	botao_volume_sfx.text = Configuracoes.texto_volume("efeitos")


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
	Progresso.limpar()
	Colecionaveis.limpar()
	Salvamento.esquecer_ultimo_espaco()
	TempoDeJogo.comecar()


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


func _carregar(espaco: int) -> void:
	continuar_pedido.emit()
	await _esperar_clique()
	if Salvamento.carregar(espaco):
		return
	_atualizar_lista_carregar()
	botao_continuar.disabled = not Salvamento.existe()
	if botao_continuar.disabled:
		_mostrar_carregar(false)
		botao_novo_jogo.grab_focus()
	else:
		botao_voltar_carregar.grab_focus()


func _ao_apertar_opcoes() -> void:
	opcoes_pedidas.emit()
	_mostrar_opcoes(true)


func _ao_apertar_sair() -> void:
	await _esperar_clique()
	get_tree().quit()
