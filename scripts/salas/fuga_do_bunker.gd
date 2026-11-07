extends Sala

const CENA_SEGUINTE := "res://cenas/salas/bunker/fim_do_bunker.tscn"
const ID_CHECKPOINT := "bunker_fuga"
const X_DA_COMPORTA := 3081.0
const Y_DA_COMPORTA := 128.0
const FOLGA_DA_SAIDA := 16.0
const VELOCIDADE_DO_GRUPO := 150.0
const FOLGA_DO_PRIMEIRO := 40.0
const FOLGA_ENTRE_ELES := 25.0
const CAMERA_OLHANDO_PARA_TRAS := Vector2(-90, 0)
const SEGUNDOS_ANTES_DOS_ROBOS := 1.2
const SEGUNDOS_ENTRANDO := 0.35
const SEGUNDOS_ESCURECENDO := 0.7
const SEGUNDOS_PROTEGIDO_NO_FIM := 5.0
const AVISO := "Corre até a comporta (Shift)! Saia da linha dos tiros."

var _saindo := false
var _andado := {}
var _correndo := {}
var _dentro := {}

@onready var gabriel: Gabriel = $Objetos/Gabriel
@onready var grupo: Node2D = $Objetos/Grupo
@onready var robos: Node2D = $Objetos/Robos
@onready var sirene: AudioStreamPlayer = $Sirene
@onready var camera: Camera2D = $Objetos/Gabriel/Camera2D


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	sirene.finished.connect(sirene.play)
	gabriel.estamina_infinita = true
	camera.offset = CAMERA_OLHANDO_PARA_TRAS
	for pessoa in grupo.get_children():
		(pessoa as CollisionObject2D).collision_layer = 0
	if not Checkpoints.esta_ativo(ID_CHECKPOINT, scene_file_path):
		Checkpoints.marcar(ID_CHECKPOINT, scene_file_path, gabriel.global_position)
	_comecar.call_deferred()


func _comecar() -> void:
	Inventario.aviso.emit(AVISO)
	await get_tree().create_timer(duracao_entrada + SEGUNDOS_ANTES_DOS_ROBOS).timeout
	for robo in _os_robos():
		robo.correndo = true


func _physics_process(delta: float) -> void:
	if _saindo:
		return
	_mover_grupo(delta)
	if gabriel.global_position.x >= X_DA_COMPORTA - FOLGA_DA_SAIDA:
		_sair()


func _mover_grupo(delta: float) -> void:
	var folga := FOLGA_DO_PRIMEIRO
	for filho in grupo.get_children():
		var pessoa := filho as PersonagemParado
		if pessoa and not _dentro.has(pessoa):
			_mover(pessoa, minf(gabriel.global_position.x + folga, X_DA_COMPORTA), delta)
		folga += FOLGA_ENTRE_ELES


func _mover(pessoa: PersonagemParado, alvo: float, delta: float) -> void:
	var antes := pessoa.global_position.x
	if alvo > antes:
		pessoa.global_position.x = move_toward(antes, alvo, VELOCIDADE_DO_GRUPO * delta)
	var andou := pessoa.global_position.x - antes
	if andou > 0.05:
		_andado[pessoa] = _andado.get(pessoa, 0.0) + andou
		_correndo[pessoa] = true
		AtorDeCena.mostrar_corrida(pessoa, _andado[pessoa])
	elif _correndo.get(pessoa, false):
		_correndo[pessoa] = false
		AtorDeCena.parar(pessoa)
	if pessoa.global_position.x >= X_DA_COMPORTA - 0.5:
		_dentro[pessoa] = true
		_entrar_na_comporta(pessoa).finished.connect(pessoa.queue_free)


func _sair() -> void:
	_saindo = true
	Vida.proteger(SEGUNDOS_PROTEGIDO_NO_FIM)
	for robo in _os_robos():
		robo.parar()
	gabriel.andar_sozinho(Vector2.ZERO)
	_entrar_na_comporta(gabriel)
	var escurecer := create_tween()
	escurecer.tween_interval(SEGUNDOS_ENTRANDO)
	escurecer.tween_property(escuro, "color:a", 1.0, SEGUNDOS_ESCURECENDO)
	escurecer.tween_callback(get_tree().change_scene_to_file.bind(CENA_SEGUINTE))


func _entrar_na_comporta(quem: Node2D) -> Tween:
	var entrar := create_tween().set_parallel()
	entrar.tween_property(quem, "global_position:y", Y_DA_COMPORTA, SEGUNDOS_ENTRANDO)
	entrar.tween_property(quem, "modulate:a", 0.0, SEGUNDOS_ENTRANDO)
	return entrar


func _os_robos() -> Array[RoboDeCena]:
	var lista: Array[RoboDeCena] = []
	for filho in robos.get_children():
		if filho is RoboDeCena:
			lista.append(filho)
	return lista
