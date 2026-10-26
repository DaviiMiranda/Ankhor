class_name ParedeFalsa
extends Interagivel

signal abriu

const ID_LANTERNA := "lanterna"
const ALTURA_PAREDE := 40.0
const MARGEM_ALCANCE := 24.0
const CAMADA_DAS_PAREDES := 8
const BRILHO_QUE_REVELA := 0.5

@export var tamanho := Vector2(64, 32)
@export var marca_descoberta: String = "esconderijo_baltazar_descoberto"
@export var alcance_da_lanterna: float = 120.0
@export var abertura_cheia_graus: float = 20.0
@export var abertura_borda_graus: float = 32.0
@export var velocidade_do_brilho: float = 4.0
@export var segundos_aberta: float = 1.2
@export var area_da_sala := Rect2()

var aberta := false

var _blocos: Array[Node2D] = []
var _cobertura: Array[Node2D] = []
var _conteudo: Array[Node2D] = []
var _brilho := 0.0
var _ocupantes: Array[Node2D] = []
var _mostrando_sala := true
var _camadas_do_bloqueio := 0

@onready var _bloqueio: StaticBody2D = $Bloqueio
@onready var _forma_bloqueio: CollisionShape2D = $Bloqueio/Forma
@onready var _alcance: CollisionShape2D = $Alcance
@onready var _oclusor: LightOccluder2D = $Oclusor
@onready var _marcas: Sprite2D = $Marcas
@onready var _painel_encostado: Sprite2D = $PainelEncostado
@onready var _som: AudioStreamPlayer2D = $Som
@onready var _espera: Timer = $Espera


func _ready() -> void:
	super()
	_camadas_do_bloqueio = _bloqueio.collision_layer
	_preparar_formas()
	_marcas.modulate.a = 0.0
	_painel_encostado.visible = false
	_espera.timeout.connect(fechar)


func ligar(blocos: Array[Node2D], cobertura: Array[Node2D], conteudo: Array[Node2D], area: Rect2) -> void:
	_blocos = blocos
	_cobertura = cobertura
	_conteudo = conteudo
	area_da_sala = area
	_mostrar_sala(_deve_mostrar_sala())


func _physics_process(delta: float) -> void:
	var alvo := 0.0 if aberta else _forca_da_lanterna()
	_brilho = move_toward(_brilho, alvo, velocidade_do_brilho * delta)
	_marcas.modulate.a = _brilho
	if _brilho >= BRILHO_QUE_REVELA:
		Progresso.marcar(marca_descoberta)
	var mostrar := _deve_mostrar_sala()
	if mostrar != _mostrando_sala:
		_mostrar_sala(mostrar)


func pode_interagir() -> bool:
	if aberta:
		return false
	return _brilho >= BRILHO_QUE_REVELA or Progresso.tem(marca_descoberta) or _jogador_na_sala()


func interagir() -> void:
	abrir()


func abrir() -> void:
	if aberta:
		return
	aberta = true
	Progresso.marcar(marca_descoberta)
	_espera.stop()
	_bloqueio.set_deferred("collision_layer", 0)
	_oclusor.visible = false
	_mostrar_parede(false)
	_som.play()
	abriu.emit()


func fechar() -> void:
	if not aberta or not _ocupantes.is_empty():
		return
	aberta = false
	_bloqueio.set_deferred("collision_layer", _camadas_do_bloqueio)
	_oclusor.visible = true
	_mostrar_parede(true)
	_som.play()


func _ao_entrar(corpo: Node2D) -> void:
	super(corpo)
	if corpo is Gabriel and not _ocupantes.has(corpo):
		_ocupantes.append(corpo)
		_espera.stop()


func _ao_sair(corpo: Node2D) -> void:
	super(corpo)
	_ocupantes.erase(corpo)
	if aberta and _ocupantes.is_empty() and _espera.is_inside_tree():
		_espera.start(segundos_aberta)


func _forca_da_lanterna() -> float:
	if not Inventario.estado_de(ID_LANTERNA).get("aceso", false):
		return 0.0
	var gabriel := get_tree().get_first_node_in_group("jogador") as Gabriel
	if gabriel == null:
		return 0.0
	var origem := gabriel.to_global(gabriel.posicao_da_mao())
	var ate_a_parede := global_position + Vector2(0, -ALTURA_PAREDE / 2.0) - origem
	var distancia := ate_a_parede.length()
	if distancia > alcance_da_lanterna or distancia < 0.001:
		return 0.0
	if _tem_parede_no_caminho(origem, gabriel):
		return 0.0
	var cosseno := gabriel.direcao_olhar.normalized().dot(ate_a_parede / distancia)
	var no_feixe := smoothstep(cos(deg_to_rad(abertura_borda_graus)), cos(deg_to_rad(abertura_cheia_graus)), cosseno)
	var perto := 1.0 - smoothstep(alcance_da_lanterna * 0.6, alcance_da_lanterna, distancia)
	return no_feixe * perto


func _tem_parede_no_caminho(origem: Vector2, gabriel: Gabriel) -> bool:
	var consulta := PhysicsRayQueryParameters2D.create(origem, global_position + Vector2(0, -2), CAMADA_DAS_PAREDES)
	consulta.exclude = [_bloqueio.get_rid(), gabriel.get_rid()]
	return not get_world_2d().direct_space_state.intersect_ray(consulta).is_empty()


func _jogador_na_sala() -> bool:
	var gabriel := get_tree().get_first_node_in_group("jogador") as Node2D
	return gabriel != null and area_da_sala.has_point(gabriel.global_position)


func _deve_mostrar_sala() -> bool:
	return aberta or _jogador_na_sala()


func _mostrar_sala(mostrar: bool) -> void:
	_mostrando_sala = mostrar
	for no in _conteudo:
		if is_instance_valid(no):
			no.visible = mostrar
	for no in _cobertura:
		if is_instance_valid(no):
			no.visible = not mostrar


func _mostrar_parede(mostrar: bool) -> void:
	for bloco in _blocos:
		if is_instance_valid(bloco):
			bloco.visible = mostrar
	_painel_encostado.visible = not mostrar


func _preparar_formas() -> void:
	var pegada := Rect2(Vector2(-tamanho.x / 2.0, -tamanho.y), tamanho)
	var bloqueio := RectangleShape2D.new()
	bloqueio.size = tamanho
	_forma_bloqueio.shape = bloqueio
	_forma_bloqueio.position = pegada.get_center()
	var zona := RectangleShape2D.new()
	zona.size = tamanho + Vector2.ONE * MARGEM_ALCANCE * 2.0
	_alcance.shape = zona
	_alcance.position = pegada.get_center()
	var poligono := OccluderPolygon2D.new()
	poligono.polygon = PackedVector2Array([pegada.position, Vector2(pegada.end.x, pegada.position.y),
			pegada.end, Vector2(pegada.position.x, pegada.end.y)])
	_oclusor.occluder = poligono
