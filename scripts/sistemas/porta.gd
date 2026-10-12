class_name Porta
extends Interagivel

const SOM_ABRIR := preload("res://assets/audio/efeitos/objetos/porta_abrir.wav")
const SOM_EMPERRADA := preload("res://assets/audio/efeitos/objetos/porta_emperrada.wav")
const LARGURA_PECA_PAREDE := 80.0
const TOLERANCIA_FOLHA := 12.0
const DESLIZE_ESPIANDO := 130.0
const AVISO_ESPIANDO := "Espiando pela fresta. E: sair. Para trás: voltar."

static var _chegada := ""
static var _destrancadas := {}
static var _espiar_em := ""

@export var id: String = ""
@export_file("*.tscn") var cena_destino: String = ""
@export var porta_destino: String = ""
@export var direcao_entrar := Vector2.UP
@export var segundos_andando: float = 0.8
@export var trancada := false
@export var chave: String = ""
@export var aviso_trancada: String = "Trancada. Talvez dê para hackear"
@export var aviso_destrancada: String = "Porta destrancada"
@export var marca_ao_destrancar: String = ""
@export var atravessa_ao_destrancar := true
@export var trinco_deste_lado := false
@export var bloqueada := false
@export var dificuldade_hack := Hackeamento.Dificuldade.MEDIO
@export var minigame_hack := Hackeamento.Tipo.ALEATORIO
@export var liberada_por: String = ""
@export var marca_ao_tentar: String = ""
@export var aviso_bloqueada: String = "A porta não abre."
@export var som_abrir: AudioStream = SOM_ABRIR
@export var som_destrancar: AudioStream

var _atravessando := false
var _folha: FolhaPorta
var _vai_espiar := false
var _espiando := false
var _camada_gabriel := 0
var _olhar: Tween


func _ready() -> void:
	super()
	add_to_group("portas")
	_folha = _encontrar_folha()
	if _destrancadas.has(id) or (not marca_ao_destrancar.is_empty() and Progresso.tem(marca_ao_destrancar)):
		trancada = false
	if not id.is_empty() and _chegada == id:
		_chegada = ""
		if _espiar_em == id:
			_espiar_em = ""
			_comecar_espiada.call_deferred()
		else:
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
	if trancada and (trinco_deste_lado or (not chave.is_empty() and Inventario.tem(chave))):
		destrancar()
		if not atravessa_ao_destrancar:
			return
	if trancada:
		Inventario.aviso.emit(aviso_trancada)
		return
	var gabriel := _gabriel()
	if gabriel == null:
		return
	_atravessando = true
	_tocar(_som_de_abrir())
	_abrir_folha()
	gabriel.andar_sozinho(direcao_entrar)
	var animacao := create_tween().set_parallel()
	animacao.tween_property(gabriel, "modulate", Color(0, 0, 0, 0), segundos_andando)
	var escuro := get_tree().current_scene.get_node_or_null("Transicao/Escuro") as ColorRect
	if escuro:
		animacao.tween_property(escuro, "color:a", 1.0, segundos_andando / 2.0).set_delay(segundos_andando / 2.0)
	animacao.chain().tween_callback(_trocar_de_cena)


func espiar() -> void:
	_vai_espiar = not esta_bloqueada() and not trancada
	interagir()


func destrancar() -> void:
	trancada = false
	if not id.is_empty():
		_destrancadas[id] = true
	Inventario.aviso.emit(aviso_destrancada)
	if som_destrancar:
		_tocar(som_destrancar)
	Progresso.marcar(marca_ao_destrancar)


func _encontrar_folha() -> FolhaPorta:
	for candidata in get_tree().get_nodes_in_group("folhas_de_porta"):
		var centro := (candidata as Node2D).global_position.x + LARGURA_PECA_PAREDE / 2.0
		if absf(centro - global_position.x) <= TOLERANCIA_FOLHA:
			return candidata as FolhaPorta
	return null


func _som_de_abrir() -> AudioStream:
	if _folha and _folha.som_abrir:
		return _folha.som_abrir
	return som_abrir


func _escala_folha() -> float:
	var quadros := _folha.sprite_frames
	var duracao := quadros.get_frame_count(&"abrir") / quadros.get_animation_speed(&"abrir")
	return maxf(duracao / segundos_andando, 0.1)


func _abrir_folha() -> void:
	if _folha:
		_folha.play(&"abrir", _escala_folha())


func _fechar_folha() -> void:
	if _folha:
		_folha.play(&"abrir", -_escala_folha(), true)


func _tocar(stream: AudioStream) -> void:
	var som := AudioStreamPlayer.new()
	som.stream = stream
	som.bus = &"Efeitos"
	som.finished.connect(som.queue_free)
	get_tree().root.add_child(som)
	som.play()


func _trocar_de_cena() -> void:
	_chegada = porta_destino
	_espiar_em = porta_destino if _vai_espiar else ""
	get_tree().change_scene_to_file(cena_destino)


func _sair_pela_porta() -> void:
	var gabriel := _gabriel()
	if gabriel == null:
		return
	_atravessando = true
	_fechar_folha()
	gabriel.global_position = global_position
	var camera := gabriel.get_node_or_null("Camera2D") as Camera2D
	if camera:
		camera.reset_smoothing()
	gabriel.modulate = Color(0, 0, 0, 0)
	gabriel.andar_sozinho(-direcao_entrar)
	var animacao := create_tween()
	animacao.tween_property(gabriel, "modulate", Color.WHITE, segundos_andando)
	animacao.tween_callback(_devolver_controle.bind(gabriel))


func _comecar_espiada() -> void:
	var gabriel := _gabriel()
	if gabriel == null:
		return
	_atravessando = true
	_espiando = true
	gabriel.global_position = global_position
	gabriel.modulate = Color(0, 0, 0, 0)
	gabriel.andar_sozinho(Vector2.ZERO)
	_camada_gabriel = gabriel.collision_layer
	gabriel.collision_layer = 0
	gabriel.esconder(true)
	Inventario.aviso.emit(AVISO_ESPIANDO)
	var camera := gabriel.get_node_or_null("Camera2D") as Camera2D
	if camera == null:
		return
	camera.reset_smoothing()
	_olhar = create_tween().set_loops()
	_olhar.tween_property(camera, "offset:x", -DESLIZE_ESPIANDO, 1.6).set_trans(Tween.TRANS_SINE)
	_olhar.tween_property(camera, "offset:x", DESLIZE_ESPIANDO, 3.2).set_trans(Tween.TRANS_SINE)
	_olhar.tween_property(camera, "offset:x", 0.0, 1.6).set_trans(Tween.TRANS_SINE)


func _unhandled_input(evento: InputEvent) -> void:
	if not _espiando:
		return
	if evento.is_action_pressed("interagir") or evento.is_action_pressed(_acao_de(-direcao_entrar)):
		get_viewport().set_input_as_handled()
		_terminar_espiada(true)
	elif evento.is_action_pressed(_acao_de(direcao_entrar)):
		get_viewport().set_input_as_handled()
		_terminar_espiada(false)


func _acao_de(direcao: Vector2) -> StringName:
	if absf(direcao.x) > absf(direcao.y):
		return &"mover_direita" if direcao.x > 0.0 else &"mover_esquerda"
	return &"mover_baixo" if direcao.y > 0.0 else &"mover_cima"


func _terminar_espiada(sair: bool) -> void:
	_espiando = false
	if _olhar:
		_olhar.kill()
	var gabriel := _gabriel()
	if gabriel == null:
		return
	gabriel.esconder(false)
	gabriel.collision_layer = _camada_gabriel
	var camera := gabriel.get_node_or_null("Camera2D") as Camera2D
	if camera:
		create_tween().tween_property(camera, "offset:x", 0.0, 0.3)
	if sair:
		_sair_pela_porta()
	else:
		_atravessando = false
		interagir()


func _devolver_controle(gabriel: Gabriel) -> void:
	gabriel.devolver_controle()
	_atravessando = false


func _gabriel() -> Gabriel:
	return get_tree().get_first_node_in_group("jogador") as Gabriel
