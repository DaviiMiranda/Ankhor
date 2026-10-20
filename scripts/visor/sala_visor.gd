extends Control

enum Estado { ENTRANDO, ANDANDO, MOVENDO_CAMERA, FOCADO, SAINDO }

const DICA_ANDANDO := "Esc: tirar os óculos"

@export var cosseno_do_olhar: float = 0.8
@export var segundos_movendo_camera: float = 0.6
@export var segundos_escurecendo: float = 0.6

var _estado := Estado.ENTRANDO
var _foco: FocoVisor
var _camera_ao_andar: Transform3D

@onready var mundo: SubViewport = $Imagem/Mundo
@onready var jogador: JogadorVisor = $Imagem/Mundo/JogadorVisor
@onready var tela: TelaDoVisor = $Imagem/Mundo/TelaDoVisor
@onready var tela_documento: CanvasLayer = $TelaDocumento
@onready var efeito_crt: ColorRect = $EfeitoCRT
@onready var escuro: ColorRect = $Escuro
@onready var dica: Label = $Dica


func _ready() -> void:
	tela.menu.salvar_pedido.connect(_salvar)
	tela.menu.voltar_pedido.connect(_sair)
	for foco in _focos():
		foco.leitura_pedida.connect(_ler)
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
		var foco := foco_a_frente()
		dica.text = "[E] " + foco.texto_acao if foco else DICA_ANDANDO


func _unhandled_input(evento: InputEvent) -> void:
	if _estado == Estado.ANDANDO:
		_entrada_andando(evento)
	elif _estado == Estado.FOCADO:
		_entrada_focado(evento)


func _entrada_andando(evento: InputEvent) -> void:
	if evento is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		jogador.girar(evento.screen_relative)
	elif evento is InputEventMouseButton and evento.pressed:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	elif evento.is_action_pressed("interagir") and foco_a_frente():
		_ir_ate(foco_a_frente())
	elif evento.is_action_pressed("pausar"):
		_sair()
	else:
		return
	get_viewport().set_input_as_handled()


func _entrada_focado(evento: InputEvent) -> void:
	if evento.is_action_pressed("pausar"):
		_voltar_a_andar()
	elif evento is InputEventKey:
		_foco.receber(evento)
	else:
		return
	get_viewport().set_input_as_handled()


func foco_a_frente() -> FocoVisor:
	var olhar := _no_chao(jogador.direcao_do_olhar()).normalized()
	var melhor: FocoVisor = null
	var melhor_cosseno := cosseno_do_olhar
	for foco in _focos():
		var ate_o_foco := _no_chao(foco.centro() - jogador.global_position)
		if ate_o_foco.length() > foco.alcance:
			continue
		var cosseno := olhar.dot(ate_o_foco.normalized())
		if cosseno >= melhor_cosseno:
			melhor = foco
			melhor_cosseno = cosseno
	return melhor


func _focos() -> Array[FocoVisor]:
	var focos: Array[FocoVisor] = []
	for no in get_tree().get_nodes_in_group(FocoVisor.GRUPO):
		focos.append(no as FocoVisor)
	return focos


func _no_chao(vetor: Vector3) -> Vector3:
	return Vector3(vetor.x, 0.0, vetor.z)


func _comecar_a_andar() -> void:
	jogador.controlando = true
	_mudar_estado(Estado.ANDANDO)


func _ir_ate(foco: FocoVisor) -> void:
	_foco = foco
	_mudar_estado(Estado.MOVENDO_CAMERA)
	jogador.controlando = false
	_camera_ao_andar = jogador.camera.transform
	var proporcao := float(mundo.size.x) / float(mundo.size.y)
	var destino := foco.camera_diante(jogador.camera.fov, proporcao)
	var movimento := _mover_camera(jogador.camera.global_transform, destino)
	movimento.tween_callback(_chegar_no_foco)


func _chegar_no_foco() -> void:
	_mudar_estado(Estado.FOCADO)
	_foco.focar()


func _voltar_a_andar() -> void:
	_foco.soltar()
	_mudar_estado(Estado.MOVENDO_CAMERA)
	var destino := jogador.cabeca.global_transform * _camera_ao_andar
	var movimento := _mover_camera(jogador.camera.global_transform, destino)
	movimento.tween_callback(_soltar_camera)


func _soltar_camera() -> void:
	jogador.camera.transform = _camera_ao_andar
	_foco = null
	_comecar_a_andar()


func _mover_camera(inicio: Transform3D, fim: Transform3D) -> Tween:
	var movimento := create_tween().set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	movimento.tween_method(_posicionar_camera.bind(inicio, fim), 0.0, 1.0, segundos_movendo_camera)
	return movimento


func _posicionar_camera(peso: float, inicio: Transform3D, fim: Transform3D) -> void:
	jogador.camera.global_transform = inicio.interpolate_with(fim, peso)


func _ler(documento: Documento) -> void:
	tela_documento.abrir(documento)


func _salvar() -> void:
	tela.menu.mostrar_resultado(Visor.salvar())


func _sair() -> void:
	if _estado == Estado.SAINDO:
		return
	if _foco:
		_foco.soltar()
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
		Estado.FOCADO:
			dica.text = _foco.dica_focado
		_:
			dica.text = ""


func _ao_mudar_configuracoes() -> void:
	efeito_crt.visible = Configuracoes.efeito_crt
