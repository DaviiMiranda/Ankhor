class_name MenuVisor
extends Control

signal salvar_pedido
signal voltar_pedido

const SEM_SAVE := "Nenhum jogo salvo"
const COM_SAVE := "Último save"
const SALVO := "Jogo salvo"
const FALHOU := "Não foi possível salvar"

var _tocar_ao_focar := false

@onready var ultimo_save: Label = $Conteudo/UltimoSave
@onready var data_do_save: Label = $Conteudo/DataDoSave
@onready var resultado: Label = $Conteudo/Resultado
@onready var botao_salvar: Button = $Conteudo/BotaoSalvar
@onready var botao_voltar: Button = $Conteudo/BotaoVoltar
@onready var efeito_crt: ColorRect = $EfeitoCRT
@onready var som_passar: AudioStreamPlayer = $SomPassar
@onready var som_clique: AudioStreamPlayer = $SomClique
@onready var som_salvar: AudioStreamPlayer = $SomSalvar


func _ready() -> void:
	botao_salvar.pressed.connect(salvar_pedido.emit)
	botao_voltar.pressed.connect(voltar_pedido.emit)
	for botao in [botao_salvar, botao_voltar]:
		botao.focus_entered.connect(_ao_focar)
		botao.pressed.connect(som_clique.play)
	Configuracoes.mudou.connect(_ao_mudar_configuracoes)
	_ao_mudar_configuracoes()
	atualizar()


func focar() -> void:
	_tocar_ao_focar = false
	botao_salvar.grab_focus()
	set_deferred("_tocar_ao_focar", true)


func soltar() -> void:
	_tocar_ao_focar = false
	get_viewport().gui_release_focus()


func atualizar() -> void:
	var data := Salvamento.data_salva()
	ultimo_save.text = SEM_SAVE if data.is_empty() else COM_SAVE
	data_do_save.text = data


func mostrar_resultado(deu_certo: bool) -> void:
	resultado.text = SALVO if deu_certo else FALHOU
	if deu_certo:
		som_salvar.play()
	atualizar()


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


func _ao_focar() -> void:
	if _tocar_ao_focar:
		som_passar.play()


func _ao_mudar_configuracoes() -> void:
	efeito_crt.visible = Configuracoes.efeito_crt
