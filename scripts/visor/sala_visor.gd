extends Control

enum Estado { ENTRANDO, ANDANDO, MOVENDO_CAMERA, NA_TELA, SAINDO }

const DICA_ANDANDO := "Esc: tirar os óculos"
const DICA_PERTO := "[E] Usar a tela"
const DICA_NA_TELA := "W/S: escolher   E: confirmar   Esc: afastar"

@export var alcance_da_tela: float = 1.5
@export var cosseno_do_olhar: float = 0.8
@export var ocupacao_da_tela: float = 0.8
@export var segundos_movendo_camera: float = 0.6
@export var segundos_escurecendo: float = 0.6

var _estado := Estado.ENTRANDO
var _camera_ao_andar: Transform3D

@onready var jogador: JogadorVisor = $Imagem/Mundo/JogadorVisor
@onready var tela: MeshInstance3D = $Imagem/Mundo/Modelo/Tela
@onready var imagem_da_tela: SubViewport = $Imagem/Mundo/ImagemDaTela
@onready var menu: MenuVisor = $Imagem/Mundo/ImagemDaTela/MenuVisor
@onready var efeito_crt: ColorRect = $EfeitoCRT
@onready var escuro: ColorRect = $Escuro
@onready var dica: Label = $Dica


func _ready() -> void:
	_pintar_a_tela()
	menu.salvar_pedido.connect(_salvar)
	menu.voltar_pedido.connect(_sair)
	Configuracoes.mudou.connect(_ao_mudar_configuracoes)
	_ao_mudar_configuracoes()
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	jogador.controlando = false
	escuro.color.a = 1.0
	var entrada := create_tween()
	entrada.tween_property(escuro, "color:a", 0.0, segundos_escurecendo)
	entrada.tween_callback(_comecar_a_andar)


func _process(_delta: float) -> void:
	if _estado == Estado.ANDANDO:
		dica.text = DICA_PERTO if _pode_usar_a_tela() else DICA_ANDANDO


func _unhandled_input(evento: InputEvent) -> void:
	if _estado == Estado.ANDANDO:
		_entrada_andando(evento)
	elif _estado == Estado.NA_TELA:
		_entrada_na_tela(evento)


func _entrada_andando(evento: InputEvent) -> void:
	if evento is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		jogador.girar(evento.screen_relative)
	elif evento is InputEventMouseButton and evento.pressed:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	elif evento.is_action_pressed("interagir") and _pode_usar_a_tela():
		_ir_ate_a_tela()
	elif evento.is_action_pressed("pausar"):
		_sair()
	else:
		return
	get_viewport().set_input_as_handled()


func _entrada_na_tela(evento: InputEvent) -> void:
	if evento.is_action_pressed("pausar"):
		_voltar_a_andar()
	elif evento is InputEventKey:
		imagem_da_tela.push_input(evento)
	else:
		return
	get_viewport().set_input_as_handled()


func _pintar_a_tela() -> void:
	var material := StandardMaterial3D.new()
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	material.albedo_texture = imagem_da_tela.get_texture()
	tela.material_override = material


func _centro_da_tela() -> Vector3:
	return tela.global_transform * tela.get_aabb().get_center()


func _pode_usar_a_tela() -> bool:
	var ate_a_tela := _no_chao(_centro_da_tela() - jogador.global_position)
	if ate_a_tela.length() > alcance_da_tela:
		return false
	var olhar := _no_chao(jogador.direcao_do_olhar())
	return olhar.normalized().dot(ate_a_tela.normalized()) >= cosseno_do_olhar


func _no_chao(vetor: Vector3) -> Vector3:
	return Vector3(vetor.x, 0.0, vetor.z)


func _camera_diante_da_tela() -> Transform3D:
	var centro := _centro_da_tela()
	var frente := (tela.global_basis * Vector3.BACK).normalized()
	var altura := tela.get_aabb().size.y * tela.global_basis.get_scale().y
	var meio_angulo := deg_to_rad(jogador.camera.fov) / 2.0
	var distancia := (altura / ocupacao_da_tela) / (2.0 * tan(meio_angulo))
	return Transform3D(Basis(), centro + frente * distancia).looking_at(centro, Vector3.UP)


func _comecar_a_andar() -> void:
	jogador.controlando = true
	_mudar_estado(Estado.ANDANDO)


func _ir_ate_a_tela() -> void:
	_mudar_estado(Estado.MOVENDO_CAMERA)
	jogador.controlando = false
	_camera_ao_andar = jogador.camera.transform
	var movimento := _mover_camera(jogador.camera.global_transform, _camera_diante_da_tela())
	movimento.tween_callback(_chegar_na_tela)


func _chegar_na_tela() -> void:
	_mudar_estado(Estado.NA_TELA)
	menu.focar()


func _voltar_a_andar() -> void:
	menu.soltar()
	_mudar_estado(Estado.MOVENDO_CAMERA)
	var destino := jogador.cabeca.global_transform * _camera_ao_andar
	var movimento := _mover_camera(jogador.camera.global_transform, destino)
	movimento.tween_callback(_soltar_camera)


func _soltar_camera() -> void:
	jogador.camera.transform = _camera_ao_andar
	_comecar_a_andar()


func _mover_camera(inicio: Transform3D, fim: Transform3D) -> Tween:
	var movimento := create_tween().set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	movimento.tween_method(_posicionar_camera.bind(inicio, fim), 0.0, 1.0, segundos_movendo_camera)
	return movimento


func _posicionar_camera(peso: float, inicio: Transform3D, fim: Transform3D) -> void:
	jogador.camera.global_transform = inicio.interpolate_with(fim, peso)


func _salvar() -> void:
	menu.mostrar_resultado(Visor.salvar())


func _sair() -> void:
	if _estado == Estado.SAINDO:
		return
	menu.soltar()
	jogador.controlando = false
	_mudar_estado(Estado.SAINDO)
	var saida := create_tween()
	saida.tween_property(escuro, "color:a", 1.0, segundos_escurecendo)
	saida.tween_callback(Visor.fechar)


func _mudar_estado(novo: Estado) -> void:
	_estado = novo
	match novo:
		Estado.ANDANDO:
			dica.text = DICA_ANDANDO
		Estado.NA_TELA:
			dica.text = DICA_NA_TELA
		_:
			dica.text = ""


func _ao_mudar_configuracoes() -> void:
	efeito_crt.visible = Configuracoes.efeito_crt
