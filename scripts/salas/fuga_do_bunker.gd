extends Sala

const CENA_SEGUINTE := "res://cenas/salas/bunker/fim_do_bunker.tscn"
const VELOCIDADE_DO_GRUPO := 108.0
const X_DA_COMPORTA := 1481.0
const Y_DA_COMPORTA := 128.0
const SEGUNDOS_ANTES_DE_CORRER := 0.5
const SEGUNDOS_ENTRANDO := 0.35
const SEGUNDOS_ESCURECENDO := 0.7
const SEGUNDOS_ENTRE_PASSOS := 0.3
const AVISO := "A comporta do núcleo, no fim do corredor. Corre!"

var _saindo := false
var _robos_correndo := false
var _tempo_do_passo := 0.0

@onready var gabriel: Gabriel = $Objetos/Gabriel
@onready var grupo: Node2D = $Objetos/Grupo
@onready var robos: Node2D = $Objetos/Robos
@onready var sirene: AudioStreamPlayer = $Sirene
@onready var passo_de_robo: AudioStreamPlayer = $PassoDeRobo


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	gabriel.andar_sozinho(Vector2.ZERO)
	sirene.finished.connect(sirene.play)
	_comecar.call_deferred()


func _comecar() -> void:
	await get_tree().create_timer(duracao_entrada * 0.5 + SEGUNDOS_ANTES_DE_CORRER).timeout
	Inventario.aviso.emit(AVISO)
	for robo in robos.get_children():
		(robo as RoboDeCena).correndo = true
	for filho in grupo.get_children():
		var pessoa := filho as PersonagemParado
		var corrida := AtorDeCena.andar_ate(pessoa, Vector2(X_DA_COMPORTA, pessoa.position.y), VELOCIDADE_DO_GRUPO)
		corrida.finished.connect(_entrar_na_comporta.bind(pessoa))
	gabriel.correr_sozinho = true
	gabriel.andar_sozinho(Vector2.RIGHT)
	_robos_correndo = true


func _physics_process(_delta: float) -> void:
	if _saindo or gabriel.global_position.x < X_DA_COMPORTA:
		return
	_saindo = true
	_entrar_na_comporta(gabriel)
	var escurecer := create_tween()
	escurecer.tween_interval(SEGUNDOS_ENTRANDO)
	escurecer.tween_property(escuro, "color:a", 1.0, SEGUNDOS_ESCURECENDO)
	escurecer.tween_callback(get_tree().change_scene_to_file.bind(CENA_SEGUINTE))


func _entrar_na_comporta(quem: Node2D) -> void:
	var entrar := create_tween().set_parallel()
	entrar.tween_property(quem, "position:y", Y_DA_COMPORTA, SEGUNDOS_ENTRANDO)
	entrar.tween_property(quem, "modulate:a", 0.0, SEGUNDOS_ENTRANDO)


func _process(delta: float) -> void:
	if not _robos_correndo or _saindo:
		return
	_tempo_do_passo -= delta
	if _tempo_do_passo <= 0.0:
		_tempo_do_passo = SEGUNDOS_ENTRE_PASSOS
		passo_de_robo.pitch_scale = randf_range(0.8, 1.15)
		passo_de_robo.play()
