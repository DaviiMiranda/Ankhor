extends Control

const CENA_DO_MENU := "res://cenas/visor/menu_filme_vr.tscn"
const TEXTO_DERROTA := "A SESSÃO ACABOU"
const TEXTO_FIM := "FIM DO TRECHO"

@export var z_da_primeira_varredura: float = -0.5
@export var z_da_saida: float = -11.2
@export var segundos_ate_outra_varredura_min: float = 28.0
@export var segundos_ate_outra_varredura_max: float = 40.0
@export var segundos_escurecendo: float = 0.6
@export var segundos_queimando: float = 1.1
@export var segundos_de_texto_final: float = 1.8
@export var segundos_da_dica: float = 7.0
@export var cosseno_da_lanterna: float = 0.9
@export var alcance_da_lanterna: float = 7.0
@export var campo_de_visao: float = 72.0
@export_range(0.25, 1.0) var resolucao_do_3d: float = 1.0

var _jogando := false
var _primeira_varredura_feita := false
var _ate_outra_varredura := -1.0

@onready var imagem: SubViewportContainer = $Imagem
@onready var mundo: SubViewport = $Imagem/Mundo
@onready var jogador: JogadorVisor = $Imagem/Mundo/JogadorVisor
@onready var casco: CascoDoCorredor = $Imagem/Mundo/Casco
@onready var criatura: CriaturaDaProjecao = $Imagem/Mundo/Criatura
@onready var lanterna: SpotLight3D = $Imagem/Mundo/Lanterna
@onready var varredura: Varredura = $Varredura
@onready var dica: Label = $Dica
@onready var aviso: Label = $Aviso
@onready var texto_final: Label = $TextoFinal
@onready var queima: ColorRect = $Queima
@onready var escuro: ColorRect = $Escuro
@onready var zumbido: AudioStreamPlayer = $Zumbido
@onready var som_da_lanterna: AudioStreamPlayer = $SomDaLanterna
@onready var som_do_estalo: AudioStreamPlayer = $SomDoEstalo
@onready var som_do_ataque: AudioStreamPlayer = $SomDoAtaque


func _ready() -> void:
	_ajustar_resolucao()
	get_window().size_changed.connect(_ajustar_resolucao)
	jogador.camera.fov = campo_de_visao
	lanterna.reparent(jogador.camera, false)
	lanterna.visible = false
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	jogador.controlando = false
	aviso.visible = false
	texto_final.visible = false
	queima.visible = false
	_definir_queima(0.0)
	criatura.tocou_o_jogador.connect(_perder)
	varredura.comecou.connect(_ao_comecar_varredura)
	varredura.vigia_comecou.connect(_ao_comecar_vigia)
	varredura.terminou.connect(_ao_terminar_varredura)
	varredura.jogador_se_mexeu.connect(_perder)
	escuro.color.a = 1.0
	var entrada := create_tween()
	entrada.tween_property(escuro, "color:a", 0.0, segundos_escurecendo)
	entrada.tween_callback(_liberar)
	entrada.tween_interval(segundos_da_dica)
	entrada.tween_property(dica, "modulate:a", 0.0, 1.0)


func _physics_process(delta: float) -> void:
	if not _jogando:
		return
	criatura.existir(_iluminado(criatura.global_position))
	criatura.notar_jogador(_jogador_exposto(), jogador.global_position.z)
	_conferir_varredura(delta)
	if jogador.global_position.z <= z_da_saida:
		_chegar_na_saida()


func _unhandled_input(evento: InputEvent) -> void:
	if not _jogando:
		return
	if evento is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		jogador.girar(evento.screen_relative)
		varredura.registrar_giro_do_mouse(evento.screen_relative)
	elif evento is InputEventMouseButton and evento.pressed:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
		_alternar_lanterna()
	elif evento.is_action_pressed("interagir"):
		_alternar_lanterna()
	elif evento.is_action_pressed("pausar"):
		_tirar_o_visor()
	else:
		return
	get_viewport().set_input_as_handled()


func _liberar() -> void:
	jogador.controlando = true
	_jogando = true


func _alternar_lanterna() -> void:
	lanterna.visible = not lanterna.visible
	som_da_lanterna.play()


func _iluminado(lugar: Vector3) -> bool:
	if varredura.clareando():
		return true
	for lampada in casco.lampadas:
		if lampada.ilumina(lugar):
			return true
	return _na_lanterna(lugar)


func _na_lanterna(lugar: Vector3) -> bool:
	if not lanterna.visible:
		return false
	var ate_o_lugar := lugar + Vector3.UP - jogador.camera.global_position
	if ate_o_lugar.length() > alcance_da_lanterna:
		return false
	return jogador.direcao_do_olhar().dot(ate_o_lugar.normalized()) >= cosseno_da_lanterna


func _jogador_exposto() -> bool:
	if lanterna.visible:
		return true
	for lampada in casco.lampadas:
		if lampada.ilumina(jogador.global_position):
			return true
	return false


func _conferir_varredura(delta: float) -> void:
	if varredura.em_curso():
		return
	if not _primeira_varredura_feita:
		if jogador.global_position.z <= z_da_primeira_varredura:
			_primeira_varredura_feita = true
			aviso.visible = true
			varredura.comecar()
		return
	_ate_outra_varredura -= delta
	if _ate_outra_varredura <= 0.0:
		varredura.comecar()


func _ao_comecar_varredura() -> void:
	criatura.parar()
	criatura.existir(false)
	zumbido.stop()
	som_do_estalo.play()
	casco.cortar_energia()


func _ao_comecar_vigia() -> void:
	var lado: float = _lado_do_olhar() if aviso.visible else [-1.0, 1.0].pick_random()
	criatura.aparecer_perto(jogador.global_position.z, lado)


func _lado_do_olhar() -> float:
	return -1.0 if jogador.direcao_do_olhar().z <= 0.0 else 1.0


func _ao_terminar_varredura() -> void:
	aviso.visible = false
	zumbido.play()
	casco.religar()
	criatura.voltar_a_ronda(jogador.global_position.z)
	_ate_outra_varredura = randf_range(segundos_ate_outra_varredura_min, segundos_ate_outra_varredura_max)


func _perder() -> void:
	if not _jogando:
		return
	_jogando = false
	jogador.controlando = false
	aviso.visible = false
	var lado := signf(criatura.global_position.z - jogador.global_position.z)
	lado = lado if not is_zero_approx(lado) else -1.0
	criatura.atacar(jogador.global_position.z, lado)
	som_do_ataque.play()
	var virar_a_cabeca := create_tween().set_parallel()
	virar_a_cabeca.tween_property(jogador, "rotation:y", 0.0 if lado < 0.0 else PI, 0.12)
	virar_a_cabeca.tween_property(jogador.cabeca, "rotation:x", 0.32, 0.12)
	var queimar := create_tween()
	queimar.tween_interval(0.35)
	queimar.tween_callback(queima.show)
	queimar.tween_method(_definir_queima, 0.0, 1.0, segundos_queimando)
	queimar.tween_callback(_mostrar_texto_final.bind(TEXTO_DERROTA))


func _definir_queima(progresso: float) -> void:
	(queima.material as ShaderMaterial).set_shader_parameter("progresso", progresso)


func _chegar_na_saida() -> void:
	_jogando = false
	jogador.controlando = false
	var saida := create_tween()
	saida.tween_property(escuro, "color:a", 1.0, segundos_escurecendo)
	saida.tween_callback(_mostrar_texto_final.bind(TEXTO_FIM))


func _mostrar_texto_final(texto: String) -> void:
	escuro.color.a = 1.0
	texto_final.text = texto
	texto_final.visible = true
	var volta := create_tween()
	volta.tween_interval(segundos_de_texto_final)
	volta.tween_callback(Visor.trocar.bind(CENA_DO_MENU))


func _tirar_o_visor() -> void:
	_jogando = false
	jogador.controlando = false
	var saida := create_tween()
	saida.tween_property(escuro, "color:a", 1.0, segundos_escurecendo)
	saida.tween_callback(Visor.fechar)


func _ajustar_resolucao() -> void:
	var na_tela := get_viewport_rect().size
	var desenhada := (Vector2(get_window().size) * resolucao_do_3d).round().max(na_tela)
	imagem.stretch = false
	imagem.set_anchors_and_offsets_preset(Control.PRESET_TOP_LEFT)
	mundo.size = Vector2i(desenhada)
	imagem.size = desenhada
	imagem.scale = na_tela / desenhada
