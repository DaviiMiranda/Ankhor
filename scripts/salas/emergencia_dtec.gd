extends Sala

const DIALOGO_CHEGADA := "res://dados/dialogos/dtec_chegada.json"
const MARCA_VEIO_DA_FUGA := "bunker_henrique_sumiu"
const MARCA_SEPARADOS := "dtec_grupo_separado"
const AVISO_SOZINHO := "O Zane foi por outro caminho. Daqui em diante, você está sozinho."
const VELOCIDADE_DO_ZANE := 70.0
const SEGUNDOS_ANTES_DA_CONVERSA := 0.5
const SEGUNDOS_DA_TORCIDA := 0.25
const SEGUNDOS_SUMINDO := 0.4
const INCLINACAO_DA_DIANA := -0.14
const DESCIDA_DA_DIANA := 3.0

@onready var gabriel: Gabriel = $Objetos/Gabriel
@onready var zane: PersonagemParado = $Objetos/Zane
@onready var clarice: PersonagemParado = $Objetos/Clarice
@onready var diana: PersonagemParado = $Objetos/Diana
@onready var porta: Node2D = $Porta_emergencia_corredor


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	if not Progresso.tem(MARCA_VEIO_DA_FUGA):
		for pessoa in [zane, clarice, diana]:
			pessoa.queue_free()
		return
	if Progresso.tem(MARCA_SEPARADOS):
		zane.queue_free()
		_apoiar_diana(0.0)
		return
	Dialogos.terminou.connect(_ao_terminar_dialogo)
	gabriel.andar_sozinho(Vector2.ZERO)
	_comecar.call_deferred()


func _comecar() -> void:
	await get_tree().create_timer(duracao_entrada + SEGUNDOS_ANTES_DA_CONVERSA).timeout
	await _apoiar_diana(SEGUNDOS_DA_TORCIDA).finished
	Dialogos.iniciar(DIALOGO_CHEGADA)


func _apoiar_diana(segundos: float) -> Tween:
	diana.virar("frente", false)
	var torcida := create_tween().set_parallel().set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	torcida.tween_property(diana, "rotation", INCLINACAO_DA_DIANA, maxf(segundos, 0.01))
	torcida.tween_property(diana, "position:y", diana.position.y + DESCIDA_DA_DIANA, maxf(segundos, 0.01))
	return torcida


func _ao_terminar_dialogo(caminho: String) -> void:
	if caminho != DIALOGO_CHEGADA:
		return
	Progresso.marcar(MARCA_SEPARADOS)
	clarice.virar("tres_quartos", true)
	var saida := (zane.get_parent() as Node2D).to_local(porta.global_position + Vector2(0, 26))
	await AtorDeCena.andar_ate(zane, saida, VELOCIDADE_DO_ZANE).finished
	var sumir := create_tween().set_parallel()
	sumir.tween_property(zane, "modulate:a", 0.0, SEGUNDOS_SUMINDO)
	sumir.tween_property(zane, "position:y", zane.position.y - 10.0, SEGUNDOS_SUMINDO)
	await sumir.finished
	zane.queue_free()
	gabriel.devolver_controle()
	Inventario.aviso.emit(AVISO_SOZINHO)
