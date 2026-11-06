extends Sala

const DIALOGO_ENCONTRO := "res://dados/dialogos/bunker_encontro.json"
const DIALOGO_SUMICO := "res://dados/dialogos/bunker_sumico.json"
const DIALOGO_FUGA := "res://dados/dialogos/bunker_fuga.json"
const CENA_FUGA := "res://cenas/salas/bunker/fuga.tscn"
const MARCA_ENERGIA := "bunker_energia"
const MARCA_CONFRONTO := "bunker_confronto_falado"
const MARCA_SUMIU := "bunker_henrique_sumiu"
const MARCA_COMPORTA := "bunker_comporta_aberta"
const VOZ_DO_CARLOS := "Voz nos alto-falantes"
const COR_DO_ALARME := Color(0.62, 0.2, 0.2, 1)
const ESCURECIMENTO_DO_PULSO := 0.4
const SEGUNDOS_DO_PULSO := 0.55
const SEGUNDOS_ENQUADRANDO := 0.8
const ALTURA_DO_ENQUADRAMENTO := 26.0
const ZOOM_NO_DISPOSITIVO := Vector2(5, 5)
const ALTURA_DA_QUEDA := 34.0
const DISTANCIA_DO_SUSTO := 12.0
const VELOCIDADE_DA_CORRIDA := 110.0
const SEGUNDOS_ANTES_DO_BRILHO := 0.5
const SEGUNDOS_ATE_O_SUSTO := 1.0
const SEGUNDOS_OLHANDO_O_DISPOSITIVO := 2.0
const SEGUNDOS_ENTRE_PASSOS := 0.32
const PASSOS_DOS_ROBOS := 5
const SEGUNDOS_CORRENDO_ANTES_DO_ESCURO := 0.9
const SEGUNDOS_ESCURECENDO := 0.6

var _alarme_ligado := false
var _enquadramento := Vector2.ZERO

@onready var henrique: PersonagemParado = $Objetos/Henrique/Henrique
@onready var conversa_henrique: Node = $Objetos/Henrique/Conversa
@onready var encontro: Node2D = $Objetos/Encontro
@onready var gatilho: GatilhoDialogo = $Objetos/GatilhoEncontro
@onready var dispositivo: Node2D = $Objetos/Dispositivo
@onready var sumico: SumicoDeEnergia = $Efeitos/SumicoDeEnergia
@onready var porta: Node2D = $Porta_central_dados
@onready var sirene: AudioStreamPlayer = $Sirene
@onready var som_queda: AudioStreamPlayer = $SomQueda
@onready var alerta_dos_robos: AudioStreamPlayer = $AlertaDosRobos
@onready var passo_de_robo: AudioStreamPlayer = $PassoDeRobo
@onready var escuridao: CanvasModulate = $Escuridao
@onready var gabriel: Gabriel = $Objetos/Gabriel
@onready var camera: Camera2D = $Objetos/Gabriel/Camera2D


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	dispositivo.visible = false
	if Progresso.tem(MARCA_SUMIU):
		_mostrar_depois_da_fuga()
		return
	if Progresso.tem(MARCA_ENERGIA):
		henrique.virar("frente", false)
	sirene.finished.connect(_repetir_sirene)
	Dialogos.comecou.connect(_ao_comecar_dialogo)
	Dialogos.terminou.connect(_ao_terminar_dialogo)
	Dialogos.fala_mostrada.connect(_ao_mostrar_fala)
	if Progresso.tem(MARCA_CONFRONTO):
		_retomar_depois_do_confronto.call_deferred()


func _mostrar_depois_da_fuga() -> void:
	henrique.visible = false
	conversa_henrique.queue_free()
	encontro.queue_free()
	gatilho.queue_free()
	dispositivo.visible = true
	dispositivo.global_position = _chao_do_henrique()


func _retomar_depois_do_confronto() -> void:
	await get_tree().create_timer(duracao_entrada).timeout
	_sumir_henrique()


func _ao_comecar_dialogo(caminho: String) -> void:
	if caminho == DIALOGO_ENCONTRO:
		gabriel.andar_sozinho(Vector2.ZERO)
		_enquadrar(_centro_da_cena(), SEGUNDOS_ENQUADRANDO)


func _centro_da_cena() -> Vector2:
	return Vector2((henrique.global_position.x + gabriel.global_position.x) / 2.0, henrique.global_position.y + ALTURA_DO_ENQUADRAMENTO)


func _ao_terminar_dialogo(caminho: String) -> void:
	match caminho:
		DIALOGO_ENCONTRO:
			_sumir_henrique()
		DIALOGO_SUMICO:
			_robos_chegando()
		DIALOGO_FUGA:
			_correr_para_a_porta()


func _ao_mostrar_fala(quem: String, _texto: String, _retrato: Texture2D) -> void:
	if quem == VOZ_DO_CARLOS and not _alarme_ligado:
		_ligar_alarme()


func _sumir_henrique() -> void:
	gabriel.andar_sozinho(Vector2.ZERO)
	_enquadrar(_centro_da_cena(), SEGUNDOS_ENQUADRANDO)
	await get_tree().create_timer(SEGUNDOS_ANTES_DO_BRILHO).timeout
	_assustar_o_grupo()
	await sumico.sumir(henrique)
	conversa_henrique.queue_free()
	_tremer_camera(0.5, 3.0)
	await _derrubar_dispositivo()
	await _olhar_o_dispositivo()
	Dialogos.iniciar(DIALOGO_SUMICO)


func _assustar_o_grupo() -> void:
	for filho in encontro.get_children():
		var pessoa := filho as Node2D
		if pessoa == null:
			continue
		var para_longe := (pessoa.global_position - henrique.global_position).normalized() * DISTANCIA_DO_SUSTO
		var susto := create_tween()
		susto.tween_interval(SEGUNDOS_ATE_O_SUSTO + randf() * 0.4)
		susto.tween_property(pessoa, "position", pessoa.position + para_longe, 0.35) \
				.set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)


func _chao_do_henrique() -> Vector2:
	return henrique.global_position + Vector2(0, 6)


func _derrubar_dispositivo() -> void:
	var chao := _chao_do_henrique()
	dispositivo.global_position = chao - Vector2(0, ALTURA_DA_QUEDA)
	dispositivo.visible = true
	var queda := create_tween()
	queda.tween_property(dispositivo, "global_position", chao, 0.8).set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_OUT)
	queda.parallel().tween_callback(som_queda.play).set_delay(0.3)
	await queda.finished


func _olhar_o_dispositivo() -> void:
	var zoom_de_antes := camera.zoom
	var enquadramento_de_antes := _enquadramento
	var aproximar := _enquadrar(dispositivo.global_position + Vector2(0, -7), 0.9)
	aproximar.parallel().tween_property(camera, "zoom", ZOOM_NO_DISPOSITIVO, 0.9)
	await aproximar.finished
	await get_tree().create_timer(SEGUNDOS_OLHANDO_O_DISPOSITIVO).timeout
	var voltar := _enquadrar(camera.global_position + enquadramento_de_antes, 0.7)
	voltar.parallel().tween_property(camera, "zoom", zoom_de_antes, 0.7)
	await voltar.finished


func _enquadrar(ponto: Vector2, segundos: float) -> Tween:
	var tween := create_tween().set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)
	tween.tween_method(_mudar_enquadramento, _enquadramento, ponto - camera.global_position, segundos)
	return tween


func _mudar_enquadramento(novo: Vector2) -> void:
	_enquadramento = novo
	camera.offset = novo


func _ligar_alarme() -> void:
	_alarme_ligado = true
	sirene.play()
	var pulso := create_tween().set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)
	pulso.tween_property(escuridao, "color", COR_DO_ALARME, 0.5)
	var piscar := create_tween().set_pause_mode(Tween.TWEEN_PAUSE_PROCESS).set_loops()
	piscar.tween_interval(0.5)
	piscar.tween_property(escuridao, "color", COR_DO_ALARME.darkened(ESCURECIMENTO_DO_PULSO), SEGUNDOS_DO_PULSO)
	piscar.tween_property(escuridao, "color", COR_DO_ALARME, SEGUNDOS_DO_PULSO)


func _repetir_sirene() -> void:
	if _alarme_ligado:
		sirene.play()


func _robos_chegando() -> void:
	alerta_dos_robos.play()
	_tremer_camera(0.4, 1.5)
	for i in PASSOS_DOS_ROBOS:
		passo_de_robo.pitch_scale = randf_range(0.85, 1.1)
		passo_de_robo.volume_db = -14.0 + i * 2.5
		passo_de_robo.play()
		await get_tree().create_timer(SEGUNDOS_ENTRE_PASSOS).timeout
	Dialogos.iniciar(DIALOGO_FUGA)


func _correr_para_a_porta() -> void:
	var saida := porta.global_position + Vector2(0, 26)
	var i := 0
	for filho in encontro.get_children():
		var pessoa := filho as PersonagemParado
		if pessoa:
			var destino: Vector2 = (pessoa.get_parent() as Node2D).to_local(saida + Vector2(i * 10, i * 6))
			AtorDeCena.andar_ate(pessoa, destino, VELOCIDADE_DA_CORRIDA)
			i += 1
	_enquadrar(camera.global_position, SEGUNDOS_ENQUADRANDO)
	gabriel.correr_sozinho = true
	gabriel.andar_sozinho((saida - gabriel.global_position).normalized())
	await get_tree().create_timer(SEGUNDOS_CORRENDO_ANTES_DO_ESCURO).timeout
	Progresso.marcar(MARCA_SUMIU)
	Progresso.marcar(MARCA_COMPORTA)
	var escurecer := create_tween()
	escurecer.tween_property(escuro, "color:a", 1.0, SEGUNDOS_ESCURECENDO)
	escurecer.tween_callback(get_tree().change_scene_to_file.bind(CENA_FUGA))


func _tremer_camera(segundos: float, forca: float) -> void:
	var tremor := create_tween()
	tremor.tween_method(func(resta: float) -> void:
		camera.offset = _enquadramento + Vector2(randf_range(-1, 1), randf_range(-1, 1)) * forca * resta, 1.0, 0.0, segundos)
	tremor.tween_callback(func() -> void: camera.offset = _enquadramento)
