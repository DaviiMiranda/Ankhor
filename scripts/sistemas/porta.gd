class_name Porta
extends Interagivel

const SOM_ABRIR := preload("res://assets/audio/efeitos/objetos/porta_abrir.wav")
const SOM_EMPERRADA := preload("res://assets/audio/efeitos/objetos/porta_emperrada.wav")

static var _chegada := ""
static var _destrancadas := {}

@export var id: String = ""
@export_file("*.tscn") var cena_destino: String = ""
@export var porta_destino: String = ""
@export var direcao_entrar := Vector2.UP
@export var segundos_andando: float = 0.8
@export var trancada := false
@export var chave: String = ""
@export var aviso_trancada: String = "Trancada. Talvez dê para hackear"
@export var bloqueada := false
@export var dificuldade_hack := Hackeamento.Dificuldade.MEDIO
@export var minigame_hack := Hackeamento.Tipo.ALEATORIO
@export var liberada_por: String = ""
@export var marca_ao_tentar: String = ""
@export var aviso_bloqueada: String = "A porta não abre."
@export var som_abrir: AudioStream = SOM_ABRIR

var _atravessando := false


func _ready() -> void:
	super()
	add_to_group("portas")
	if _destrancadas.has(id):
		trancada = false
	if not id.is_empty() and _chegada == id:
		_chegada = ""
		_sair_pela_porta.call_deferred()


func pode_interagir() -> bool:
	return not _atravessando and (esta_bloqueada() or not cena_destino.is_empty())


func esta_bloqueada() -> bool:
	return bloqueada or (not liberada_por.is_empty() and not Progresso.tem(liberada_por))


func interagir() -> void:
	if esta_bloqueada():
		Inventario.aviso.emit(aviso_bloqueada)
		_tocar(SOM_EMPERRADA)
		Progresso.marcar(marca_ao_tentar)
		return
	if trancada and not chave.is_empty() and Inventario.tem(chave):
		destrancar()
	if trancada:
		Inventario.aviso.emit(aviso_trancada)
		return
	var gabriel := _gabriel()
	if gabriel == null:
		return
	_atravessando = true
	_tocar(som_abrir)
	gabriel.andar_sozinho(direcao_entrar)
	var animacao := create_tween().set_parallel()
	animacao.tween_property(gabriel, "modulate", Color(0, 0, 0, 0), segundos_andando)
	var escuro := get_tree().current_scene.get_node_or_null("Transicao/Escuro") as ColorRect
	if escuro:
		animacao.tween_property(escuro, "color:a", 1.0, segundos_andando / 2.0).set_delay(segundos_andando / 2.0)
	animacao.chain().tween_callback(_trocar_de_cena)


func destrancar() -> void:
	trancada = false
	if not id.is_empty():
		_destrancadas[id] = true
	Inventario.aviso.emit("Porta destrancada")


func _tocar(stream: AudioStream) -> void:
	var som := AudioStreamPlayer.new()
	som.stream = stream
	som.bus = &"Efeitos"
	som.finished.connect(som.queue_free)
	get_tree().root.add_child(som)
	som.play()


func _trocar_de_cena() -> void:
	_chegada = porta_destino
	get_tree().change_scene_to_file(cena_destino)


func _sair_pela_porta() -> void:
	var gabriel := _gabriel()
	if gabriel == null:
		return
	_atravessando = true
	gabriel.global_position = global_position
	var camera := gabriel.get_node_or_null("Camera2D") as Camera2D
	if camera:
		camera.reset_smoothing()
	gabriel.modulate = Color(0, 0, 0, 0)
	gabriel.andar_sozinho(-direcao_entrar)
	var animacao := create_tween()
	animacao.tween_property(gabriel, "modulate", Color.WHITE, segundos_andando)
	animacao.tween_callback(_devolver_controle.bind(gabriel))


func _devolver_controle(gabriel: Gabriel) -> void:
	gabriel.devolver_controle()
	_atravessando = false


func _gabriel() -> Gabriel:
	return get_tree().get_first_node_in_group("jogador") as Gabriel
