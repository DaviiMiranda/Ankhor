class_name CarlosChefe
extends Node2D

signal fase_mudou(fase: int)
signal alarme(posicao: Vector2)

const GRUPO_ATORDOAVEIS := "atordoaveis"
const COR_LUPA := Color(1.0, 0.16, 0.1)
const ALTURA_DO_RAIO := Vector2(0, -4)

@export var consoles: Array[NodePath] = []
@export var entradas_dos_robos: Array[NodePath] = []
@export var porta_que_trava: NodePath
@export var onda: NodePath
@export var robos_da_sala: NodePath
@export var cena_robo: PackedScene

@export_group("Lupa")
@export var alcance: float = 400.0
@export var abertura: float = 30.0
@export var angulo_centro: float = 90.0
@export var amplitude: float = 62.0
@export var achatamento: float = 0.6
@export var segundos_atordoado: float = 6.0

@export_group("Fases")
@export var periodo_varredura := PackedFloat32Array([7.0, 5.0, 3.5])
@export var segundos_para_alarme := PackedFloat32Array([0.8, 0.6, 0.4])
@export var maximo_de_robos := PackedInt32Array([2, 3, 3])
@export var segundos_entre_alarmes: float = 3.0

var fase := 0
var suspeita := 0.0
var _tempo := 0.0
var _atordoado := 0.0
var _espera_alarme := 0.0
var _proxima_entrada := 0
var _vendo := false

@onready var som_alarme: AudioStreamPlayer2D = $SomAlarme


func _ready() -> void:
	add_to_group(GRUPO_ATORDOAVEIS)
	material = CanvasItemMaterial.new()
	(material as CanvasItemMaterial).light_mode = CanvasItemMaterial.LIGHT_MODE_UNSHADED
	(material as CanvasItemMaterial).blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	Progresso.mudou.connect(_ao_marcar)
	var a_onda := get_node_or_null(onda) as OndaAncora
	if a_onda:
		a_onda.revelou.connect(_ao_revelar)
	_aplicar_fase.call_deferred(_consoles_invadidos(), false)


func atordoar(_segundos: float) -> void:
	_atordoado = maxf(_atordoado, segundos_atordoado)
	suspeita = 0.0


func esta_atordoado() -> bool:
	return _atordoado > 0.0


func direcao_da_lupa() -> Vector2:
	var periodo := periodo_varredura[fase]
	var angulo := angulo_centro + amplitude * sin(TAU * _tempo / periodo)
	return Vector2.from_angle(deg_to_rad(angulo))


func ve_o_ponto(ponto: Vector2) -> bool:
	var para := _no_chao(ponto - global_position)
	var distancia := para.length()
	if distancia > alcance or distancia < 1.0:
		return false
	if direcao_da_lupa().dot(para / distancia) < cos(deg_to_rad(abertura / 2.0)):
		return false
	var consulta := PhysicsRayQueryParameters2D.create(global_position + ALTURA_DO_RAIO, ponto + ALTURA_DO_RAIO, Robo.CAMADA_PAREDES)
	return get_world_2d().direct_space_state.intersect_ray(consulta).is_empty()


func _process(delta: float) -> void:
	_tempo += delta
	_espera_alarme = maxf(_espera_alarme - delta, 0.0)
	queue_redraw()
	if _atordoado > 0.0:
		_atordoado -= delta
		_vendo = false
		return
	var gabriel := get_tree().get_first_node_in_group("jogador") as Gabriel
	_vendo = gabriel != null and not gabriel.escondido and Vida.esta_viva() and ve_o_ponto(gabriel.global_position)
	if _vendo:
		suspeita += delta / segundos_para_alarme[fase]
	else:
		suspeita = maxf(suspeita - delta * 0.5, 0.0)
	if suspeita >= 1.0:
		suspeita = 0.0
		_dar_alarme(gabriel.global_position)


func _ao_revelar(posicao: Vector2) -> void:
	if _atordoado > 0.0:
		return
	if fase >= 2:
		_dar_alarme(posicao)
	else:
		suspeita = minf(suspeita + 0.6, 0.99)


func _dar_alarme(posicao: Vector2) -> void:
	if _espera_alarme > 0.0:
		return
	_espera_alarme = segundos_entre_alarmes
	som_alarme.play()
	alarme.emit(posicao)
	if _robos_na_sala().size() < maximo_de_robos[fase]:
		_chamar_robo()
	for robo in _robos_na_sala():
		robo.distrair(posicao, 2.5)


func _robos_na_sala() -> Array[Robo]:
	var sala := owner if owner else get_parent()
	var lista: Array[Robo] = []
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo and sala.is_ancestor_of(robo):
			lista.append(robo)
	return lista


func _chamar_robo() -> void:
	var gerente := get_node_or_null(robos_da_sala) as RobosDaSala
	if cena_robo == null or entradas_dos_robos.is_empty() or gerente == null or gerente.grade == null:
		return
	var entrada := get_node(entradas_dos_robos[_proxima_entrada % entradas_dos_robos.size()]) as Node2D
	_proxima_entrada += 1
	var robo := cena_robo.instantiate() as Robo
	robo.position = entrada.global_position
	get_parent().add_child(robo)
	robo.configurar(gerente.grade, 900 + _proxima_entrada)


func _consoles_invadidos() -> int:
	var total := 0
	for caminho in consoles:
		var console := get_node_or_null(caminho) as Porta
		if console and Progresso.tem(console.marca_ao_destrancar):
			total += 1
	return total


func _ao_marcar(_marca: String) -> void:
	var invadidos := _consoles_invadidos()
	if invadidos > fase:
		_aplicar_fase(invadidos, true)


func _aplicar_fase(nova: int, agora: bool) -> void:
	fase = clampi(nova, 0, periodo_varredura.size() - 1)
	var a_onda := get_node_or_null(onda) as OndaAncora
	if a_onda:
		a_onda.ativa = fase >= 1
	var porta := get_node_or_null(porta_que_trava) as Porta
	if porta and fase >= 1:
		porta.bloqueada = true
	if agora:
		_salvar_no_console(fase - 1)
		if porta and fase == 1:
			Inventario.aviso.emit(porta.aviso_bloqueada)
	fase_mudou.emit(fase)


func _salvar_no_console(indice: int) -> void:
	if indice < 0 or indice >= consoles.size():
		return
	var console := get_node_or_null(consoles[indice]) as Node2D
	var sala := get_tree().current_scene
	if console and sala:
		Checkpoints.marcar("dtec_console_%d" % (indice + 1), sala.scene_file_path, console.global_position + Vector2(0, 14))


func _no_chao(vetor: Vector2) -> Vector2:
	return Vector2(vetor.x, vetor.y / achatamento)


func _do_chao(vetor: Vector2) -> Vector2:
	return Vector2(vetor.x, vetor.y * achatamento)


func _draw() -> void:
	if _atordoado > 0.0:
		return
	var direcao := direcao_da_lupa()
	var meia := deg_to_rad(abertura / 2.0)
	var pontos := PackedVector2Array([Vector2.ZERO])
	for i in 13:
		var angulo := direcao.angle() - meia + 2.0 * meia * i / 12.0
		pontos.append(_do_chao(Vector2.from_angle(angulo) * alcance))
	var forca := 0.1 + 0.25 * suspeita + (0.1 if _vendo else 0.0)
	draw_colored_polygon(pontos, Color(COR_LUPA, forca))
