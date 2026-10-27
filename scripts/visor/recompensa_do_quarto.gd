class_name RecompensaDoQuarto
extends FocoVisor

@export var colecao: Colecao
@export var direcao_da_camera := Vector3(1.0, 0.7, 0.0)
@export var altura_ao_examinar: float = 0.08
@export var graus_por_segundo: float = 140.0
@export var sensibilidade_do_mouse: float = 0.008
@export var segundos_de_movimento: float = 0.3
@export var energia_da_luz_de_exame: float = 0.5

var _examinando := false
var _giro := Basis.IDENTITY
var _altura := 0.0
var _centro_local := Vector3.ZERO
var _pivo: Node3D
var _luz_de_exame: OmniLight3D
var _movimento: Tween


func _init() -> void:
	alcance = 1.1
	ocupacao = 0.5
	dica_focado = "WASD ou mouse: girar   Esc: afastar"


func _ready() -> void:
	visible = colecao != null and Colecionaveis.completa(colecao)
	set_process(visible)
	if not visible:
		return
	super()
	texto_acao = "Examinar: " + colecao.nome_da_recompensa
	_montar_pivo()
	_montar_luz_de_exame()


func _process(delta: float) -> void:
	if not _examinando:
		return
	var entrada := Input.get_vector("mover_esquerda", "mover_direita", "mover_cima", "mover_baixo")
	if entrada != Vector2.ZERO:
		_girar(entrada * deg_to_rad(graus_por_segundo) * delta)


func centro() -> Vector3:
	return global_transform * _centro_local


func frente() -> Vector3:
	var horizontal := Vector3(direcao_da_camera.x, 0.0, direcao_da_camera.z)
	var elevacao := Vector3.UP * direcao_da_camera.y
	return (horizontal + elevacao).normalized()


func cima() -> Vector3:
	return Vector3.UP


func camera_diante(campo_de_visao: float, proporcao: float) -> Transform3D:
	return super(campo_de_visao, proporcao).translated(Vector3.UP * altura_ao_examinar)


func titulo_focado() -> String:
	return colecao.nome_da_recompensa


func descricao_focada() -> String:
	return colecao.descricao_da_recompensa


func focar() -> void:
	_examinando = true
	_luz_de_exame.visible = true
	_animar(_levantar, 0.0, 1.0)


func soltar() -> void:
	_examinando = false
	_luz_de_exame.visible = false
	_animar(_devolver.bind(_giro, _altura), 1.0, 0.0)


func receber(evento: InputEvent) -> void:
	if evento is InputEventMouseMotion:
		_girar(evento.screen_relative * sensibilidade_do_mouse)


func _montar_pivo() -> void:
	var modelo := $Modelo as Node3D
	var caixa := _caixa_do_modelo(modelo)
	_centro_local = caixa.get_center()
	var diagonal := caixa.size.length() * global_basis.get_scale().x
	tamanho = Vector2.ONE * diagonal
	_pivo = Node3D.new()
	_pivo.position = _centro_local
	add_child(_pivo)
	modelo.reparent(_pivo, false)
	modelo.position -= _centro_local


func _montar_luz_de_exame() -> void:
	_luz_de_exame = OmniLight3D.new()
	_luz_de_exame.top_level = true
	_luz_de_exame.visible = false
	_luz_de_exame.light_color = Color(1.0, 0.95, 0.85)
	_luz_de_exame.light_energy = energia_da_luz_de_exame
	_luz_de_exame.omni_range = 1.5
	add_child(_luz_de_exame)
	_luz_de_exame.global_position = centro() + frente() * 0.35 + Vector3.UP * 0.25


func _caixa_do_modelo(modelo: Node3D) -> AABB:
	var para_local := global_transform.affine_inverse()
	var caixa := AABB()
	var primeiro := true
	for no in modelo.find_children("*", "MeshInstance3D", true, false):
		var malha := no as MeshInstance3D
		var da_malha_para_local := para_local * malha.global_transform
		for vertice in malha.mesh.get_faces():
			var ponto := da_malha_para_local * vertice
			if primeiro:
				caixa = AABB(ponto, Vector3.ZERO)
				primeiro = false
			else:
				caixa = caixa.expand(ponto)
	return caixa


func _eixo_da_direita() -> Vector3:
	return Vector3.UP.cross(frente()).normalized()


func _girar(angulos: Vector2) -> void:
	var inclinacao := Basis(_eixo_da_direita(), angulos.y)
	var volta := Basis(Vector3.UP, angulos.x)
	_giro = (volta * inclinacao * _giro).orthonormalized()
	_aplicar()


func _aplicar() -> void:
	var base := global_basis.orthonormalized()
	_pivo.basis = base.inverse() * _giro * base
	_pivo.position = _centro_local + global_basis.inverse() * (Vector3.UP * _altura)


func _animar(metodo: Callable, de: float, ate: float) -> void:
	if _movimento:
		_movimento.kill()
	_movimento = create_tween().set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_movimento.tween_method(metodo, de, ate, segundos_de_movimento)


func _levantar(peso: float) -> void:
	_altura = altura_ao_examinar * peso
	_aplicar()


func _devolver(peso: float, giro_inicial: Basis, altura_inicial: float) -> void:
	_giro = Basis.IDENTITY.slerp(giro_inicial, peso)
	_altura = altura_inicial * peso
	_aplicar()
