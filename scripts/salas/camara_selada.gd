extends Sala

const DIALOGO_PRESO := "res://dados/dialogos/camara_gabriel_preso.json"
const DIALOGO_RESGATE := "res://dados/dialogos/camara_zane_resgate.json"
const DIALOGO_REGISTRO := "res://dados/dialogos/camara_plano_carlos.json"
const CENA_PASSAGEM := "res://cenas/salas/labirinto/passagem_do_zane.tscn"
const MARCA_PRESO := "camara_gabriel_preso"
const MARCA_PASSAGEM_CONCLUIDA := "zane_passagem_concluida"
const MARCA_CELA_ABERTA := "camara_cela_aberta"
const MARCA_REGISTRO_LIDO := "camara_registro_lido"
const SEGUNDOS_ESPERA := 0.6
const SEGUNDOS_ESCURECENDO := 1.0

@onready var zane: Node2D = $Objetos/Zane
@onready var terminal: ConversaNpc = $Objetos/Terminal


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	zane.visible = Progresso.tem(MARCA_PASSAGEM_CONCLUIDA)
	terminal.primeira_conversa = DIALOGO_REGISTRO if Progresso.tem(MARCA_CELA_ABERTA) else ""
	Dialogos.terminou.connect(_ao_terminar_dialogo)
	_comecar_cena.call_deferred()


func _comecar_cena() -> void:
	await get_tree().create_timer(duracao_entrada + SEGUNDOS_ESPERA).timeout
	if Progresso.tem(MARCA_CELA_ABERTA):
		return
	if Progresso.tem(MARCA_PASSAGEM_CONCLUIDA):
		Dialogos.iniciar(DIALOGO_RESGATE)
	elif Progresso.tem(MARCA_PRESO):
		_ir_para_passagem()
	else:
		Dialogos.iniciar(DIALOGO_PRESO)


func _ao_terminar_dialogo(caminho: String) -> void:
	match caminho:
		DIALOGO_PRESO:
			Progresso.marcar(MARCA_PRESO)
			_ir_para_passagem()
		DIALOGO_RESGATE:
			terminal.primeira_conversa = DIALOGO_REGISTRO
			Progresso.marcar(MARCA_CELA_ABERTA)
			Inventario.aviso.emit("A grade subiu. O terminal do fundo acendeu.")
		DIALOGO_REGISTRO:
			Progresso.marcar(MARCA_REGISTRO_LIDO)
			Inventario.aviso.emit("O duto de volta está livre.")


func _ir_para_passagem() -> void:
	var animacao := create_tween()
	animacao.tween_property(escuro, "color:a", 1.0, SEGUNDOS_ESCURECENDO)
	animacao.tween_callback(get_tree().change_scene_to_file.bind(CENA_PASSAGEM))
