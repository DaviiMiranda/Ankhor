class_name MenuVisor
extends Control

signal salvar_pedido(espaco: int)
signal voltar_pedido

const SEM_DATA := "Espaço livre"
const SALVO := "Jogo salvo no espaço %d"
const FALHOU := "Não foi possível salvar"
const PERGUNTA := "Gravar por cima do espaço %d?"
const COR_DETALHE := Color(0.45, 0.85, 0.95, 1)
const COR_RESULTADO := Color(0.89, 0.95, 0.35, 1)

var _tocar_ao_focar := false
var _espaco_a_confirmar := 0
var _botoes_dos_espacos: Array[Button] = []

@onready var espacos: VBoxContainer = $Conteudo/Espacos
@onready var confirmar: VBoxContainer = $Conteudo/Confirmar
@onready var pergunta: Label = $Conteudo/Confirmar/Pergunta
@onready var botao_sim: Button = $Conteudo/Confirmar/BotaoSim
@onready var botao_nao: Button = $Conteudo/Confirmar/BotaoNao
@onready var botao_voltar: Button = $Conteudo/Espacos/BotaoVoltar
@onready var detalhe: Label = $Conteudo/Detalhe
@onready var efeito_crt: ColorRect = $EfeitoCRT
@onready var som_passar: AudioStreamPlayer = $SomPassar
@onready var som_clique: AudioStreamPlayer = $SomClique
@onready var som_salvar: AudioStreamPlayer = $SomSalvar


func _ready() -> void:
	_criar_botoes_dos_espacos()
	botao_voltar.pressed.connect(voltar_pedido.emit)
	botao_sim.pressed.connect(_confirmar_sobrescrever)
	botao_nao.pressed.connect(_cancelar_sobrescrever)
	for botao: Button in _todos_os_botoes():
		botao.focus_entered.connect(_ao_focar.bind(botao))
		botao.pressed.connect(som_clique.play)
	Configuracoes.mudou.connect(_ao_mudar_configuracoes)
	_ao_mudar_configuracoes()
	atualizar()


func focar() -> void:
	_mostrar_espacos(Salvamento.espaco_sugerido())


func soltar() -> void:
	_tocar_ao_focar = false
	get_viewport().gui_release_focus()


func voltar() -> bool:
	if not confirmar.visible:
		return false
	_cancelar_sobrescrever()
	return true


func atualizar() -> void:
	for i in _botoes_dos_espacos.size():
		_botoes_dos_espacos[i].text = Salvamento.texto_do_espaco(i + 1)


func mostrar_resultado(espaco: int, deu_certo: bool) -> void:
	atualizar()
	_mostrar_espacos(espaco)
	_escrever_detalhe(SALVO % espaco if deu_certo else FALHOU, COR_RESULTADO)
	if deu_certo:
		som_salvar.play()


func _criar_botoes_dos_espacos() -> void:
	for espaco in Salvamento.espacos():
		var botao := Button.new()
		botao.alignment = HORIZONTAL_ALIGNMENT_LEFT
		botao.clip_text = true
		botao.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
		botao.pressed.connect(_escolher.bind(espaco))
		espacos.add_child(botao)
		espacos.move_child(botao, botao_voltar.get_index())
		_botoes_dos_espacos.append(botao)


func _todos_os_botoes() -> Array[Button]:
	var botoes: Array[Button] = _botoes_dos_espacos.duplicate()
	botoes.append_array([botao_voltar, botao_sim, botao_nao])
	return botoes


func _escolher(espaco: int) -> void:
	if not Salvamento.ocupado(espaco):
		salvar_pedido.emit(espaco)
		return
	_espaco_a_confirmar = espaco
	pergunta.text = PERGUNTA % espaco
	_trocar_painel(confirmar, botao_nao)


func _confirmar_sobrescrever() -> void:
	salvar_pedido.emit(_espaco_a_confirmar)


func _cancelar_sobrescrever() -> void:
	_mostrar_espacos(_espaco_a_confirmar)


func _mostrar_espacos(espaco: int) -> void:
	_trocar_painel(espacos, _botoes_dos_espacos[clampi(espaco, 1, _botoes_dos_espacos.size()) - 1])


func _trocar_painel(painel: Control, foco: Button) -> void:
	_tocar_ao_focar = false
	espacos.visible = painel == espacos
	confirmar.visible = painel == confirmar
	foco.grab_focus()
	_ao_focar(foco)
	set_deferred("_tocar_ao_focar", true)


func _ao_focar(botao: Button) -> void:
	if _tocar_ao_focar:
		som_passar.play()
	var espaco := _botoes_dos_espacos.find(botao) + 1
	if espaco == 0 and confirmar.visible:
		espaco = _espaco_a_confirmar
	if espaco == 0:
		_escrever_detalhe("", COR_DETALHE)
		return
	var data := Salvamento.data_salva(espaco)
	_escrever_detalhe(SEM_DATA if data.is_empty() else data, COR_DETALHE)


func _escrever_detalhe(texto: String, cor: Color) -> void:
	detalhe.text = texto
	detalhe.add_theme_color_override("font_color", cor)


func _unhandled_input(evento: InputEvent) -> void:
	var foco := get_viewport().gui_get_focus_owner()
	if foco == null:
		return
	if evento.is_action_pressed("mover_cima"):
		foco.find_prev_valid_focus().grab_focus()
	elif evento.is_action_pressed("mover_baixo"):
		foco.find_next_valid_focus().grab_focus()
	elif evento.is_action_pressed("interagir") and foco is Button:
		(foco as Button).pressed.emit()
	else:
		return
	get_viewport().set_input_as_handled()


func _ao_mudar_configuracoes() -> void:
	efeito_crt.visible = Configuracoes.efeito_crt
