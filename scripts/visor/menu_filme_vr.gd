extends Control

const CENA_DO_JOGO := "res://cenas/visor/hora_morta/fase_nave.tscn"

@export var cosseno_da_mira: float = 0.978
@export var segundos_escurecendo: float = 0.6
@export var velocidade_do_giro: float = 0.004
@export_range(0.25, 1.0) var resolucao_do_3d: float = 1.0

var _saindo := false
var _pronto := false
var _mirado: BotaoDoMenuVr
var _tempo := 0.0

@onready var imagem: SubViewportContainer = $Imagem
@onready var mundo: SubViewport = $Imagem/Mundo
@onready var jogador: JogadorVisor = $Imagem/Mundo/JogadorVisor
@onready var ambiente: WorldEnvironment = $Imagem/Mundo/Ambiente
@onready var titulo: Label3D = $Imagem/Mundo/Titulo
@onready var botao_comecar: BotaoDoMenuVr = $Imagem/Mundo/BotaoComecar
@onready var botao_sair: BotaoDoMenuVr = $Imagem/Mundo/BotaoSair
@onready var escuro: ColorRect = $Escuro
@onready var som_passar: AudioStreamPlayer = $SomPassar
@onready var som_clique: AudioStreamPlayer = $SomClique


func _ready() -> void:
	_ajustar_resolucao()
	get_window().size_changed.connect(_ajustar_resolucao)
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	jogador.controlando = false
	escuro.color.a = 1.0
	var entrada := create_tween()
	entrada.tween_property(escuro, "color:a", 0.0, segundos_escurecendo)
	entrada.tween_callback(_liberar)


func _process(delta: float) -> void:
	_tempo += delta
	var tremor := 0.85 + 0.15 * sin(_tempo * 7.0) * sin(_tempo * 2.3)
	(ambiente.environment.sky.sky_material as ShaderMaterial).set_shader_parameter("giro", _tempo * velocidade_do_giro)
	titulo.modulate.a = tremor
	if _pronto and not _saindo:
		_mirar(botao_mirado())


func _unhandled_input(evento: InputEvent) -> void:
	if not _pronto or _saindo:
		return
	if evento is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		jogador.girar(evento.screen_relative)
	elif evento is InputEventMouseButton and evento.pressed:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
		_usar_mirado()
	elif evento.is_action_pressed("interagir"):
		_usar_mirado()
	elif evento.is_action_pressed("pausar"):
		_sair()
	else:
		return
	get_viewport().set_input_as_handled()


func botao_mirado() -> BotaoDoMenuVr:
	var olhar := jogador.direcao_do_olhar()
	var origem := jogador.camera.global_position
	var melhor: BotaoDoMenuVr = null
	var melhor_cosseno := cosseno_da_mira
	for botao: BotaoDoMenuVr in [botao_comecar, botao_sair]:
		var cosseno := olhar.dot((botao.global_position - origem).normalized())
		if cosseno >= melhor_cosseno:
			melhor = botao
			melhor_cosseno = cosseno
	return melhor


func _mirar(botao: BotaoDoMenuVr) -> void:
	if botao == _mirado:
		return
	if _mirado:
		_mirado.destacar(false)
	if botao:
		botao.destacar(true)
		som_passar.play()
	_mirado = botao


func _usar_mirado() -> void:
	if _mirado == null:
		return
	som_clique.play()
	if _mirado == botao_comecar:
		_comecar()
	elif _mirado == botao_sair:
		_sair()


func _liberar() -> void:
	jogador.controlando = true
	_pronto = true


func _comecar() -> void:
	_escurecer_e(Visor.trocar.bind(CENA_DO_JOGO))


func _sair() -> void:
	_escurecer_e(Visor.fechar)


func _escurecer_e(depois: Callable) -> void:
	_saindo = true
	jogador.controlando = false
	var saida := create_tween()
	saida.tween_property(escuro, "color:a", 1.0, segundos_escurecendo)
	saida.tween_callback(depois)


func _ajustar_resolucao() -> void:
	var na_tela := get_viewport_rect().size
	var desenhada := (Vector2(get_window().size) * resolucao_do_3d).round().max(na_tela)
	imagem.stretch = false
	imagem.set_anchors_and_offsets_preset(Control.PRESET_TOP_LEFT)
	mundo.size = Vector2i(desenhada)
	imagem.size = desenhada
	imagem.scale = na_tela / desenhada
