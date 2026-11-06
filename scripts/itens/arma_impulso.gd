extends Node2D

const COR_ONDA := Color(0.35, 0.92, 1.0)
const COR_MIRA := Color(0.35, 0.92, 1.0, 0.16)
const COR_BORDA_DA_MIRA := Color(0.35, 0.92, 1.0, 0.75)
const ALTURA_DO_CHAO := Vector2(0, -2)
const PASSOS_DO_ARCO := 14

@export var alcance: float = 150.0
@export_range(1.0, 120.0) var abertura_graus: float = 30.0
@export var velocidade_maxima: float = 400.0
@export var velocidade_minima: float = 170.0
@export var segundos_atordoado: float = 0.9
@export var segundos_entre_disparos: float = 0.45
@export var segundos_da_onda: float = 0.3
@export var energia_flash: float = 2.6

var item: Item

var _gabriel: Gabriel
var _mirando := false
var _direcao_da_mira := Vector2.RIGHT
var _direcao_da_onda := Vector2.RIGHT
var _tempo_da_onda := -1.0
var _tempo_desde_disparo := 99.0

@onready var flash: PointLight2D = $Flash
@onready var som: AudioStreamPlayer = $Som


func _ready() -> void:
	_gabriel = get_parent().get_parent() as Gabriel


func _exit_tree() -> void:
	_parar_de_mirar()


func _process(delta: float) -> void:
	_tempo_desde_disparo += delta
	if _mirando:
		_apontar()
	if _tempo_da_onda >= 0.0:
		_tempo_da_onda += delta
		if _tempo_da_onda > segundos_da_onda:
			_tempo_da_onda = -1.0
	queue_redraw()


func usar() -> void:
	if _mirando or _tempo_desde_disparo < segundos_entre_disparos:
		return
	if not ModoCombate.ativo and Inventario.unidades(item.id) <= 0:
		Inventario.aviso.emit("Sem balas: crie mais no inventário (3 pilhas cada)")
		return
	_gabriel.mirando = true
	_mirando = true
	_direcao_da_mira = _gabriel.direcao_olhar.normalized()


func _apontar() -> void:
	if not Input.is_action_pressed(_acao_do_espaco()) or not Vida.esta_viva():
		_soltar()
		return
	var entrada := Input.get_vector("mover_esquerda", "mover_direita", "mover_cima", "mover_baixo")
	if entrada != Vector2.ZERO:
		_direcao_da_mira = entrada.normalized()
	_gabriel.olhar_para(_direcao_da_mira)


func _acao_do_espaco() -> String:
	return "gadget_%d" % (Inventario.espaco_do_gadget(item) + 1)


func _soltar() -> void:
	_parar_de_mirar()
	if not Vida.esta_viva():
		return
	if not ModoCombate.ativo:
		Inventario.definir_unidades(item, maxi(Inventario.unidades(item.id) - 1, 0))
	_tempo_desde_disparo = 0.0
	_tempo_da_onda = 0.0
	_direcao_da_onda = _direcao_da_mira
	som.play()
	_piscar()
	_afastar_robos()


func _parar_de_mirar() -> void:
	if _mirando and is_instance_valid(_gabriel):
		_gabriel.mirando = false
	_mirando = false


func _afastar_robos() -> void:
	var meia_abertura := deg_to_rad(abertura_graus / 2.0)
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		var para := robo.global_position - _gabriel.global_position
		var distancia := para.length()
		if distancia > alcance:
			continue
		if distancia > 1.0 and absf(_direcao_da_onda.angle_to(para)) > meia_abertura:
			continue
		var forca := 1.0 - distancia / alcance
		var direcao := para.normalized() if distancia > 1.0 else _direcao_da_onda
		robo.empurrar(direcao, lerpf(velocidade_minima, velocidade_maxima, forca), segundos_atordoado)


func _piscar() -> void:
	flash.energy = energia_flash
	create_tween().tween_property(flash, "energy", 0.0, segundos_da_onda)


func _draw() -> void:
	if _mirando:
		_desenhar_cone(_direcao_da_mira)
	if _tempo_da_onda >= 0.0:
		_desenhar_onda()


func _pontos_do_arco(direcao: Vector2, raio: float) -> PackedVector2Array:
	var meia_abertura := deg_to_rad(abertura_graus / 2.0)
	var origem := to_local(_gabriel.global_position) + ALTURA_DO_CHAO
	var pontos := PackedVector2Array()
	for i in PASSOS_DO_ARCO + 1:
		var angulo := direcao.angle() + lerpf(-meia_abertura, meia_abertura, float(i) / PASSOS_DO_ARCO)
		pontos.append(origem + Vector2.from_angle(angulo) * raio)
	return pontos


func _desenhar_cone(direcao: Vector2) -> void:
	var arco := _pontos_do_arco(direcao, alcance)
	var origem := to_local(_gabriel.global_position) + ALTURA_DO_CHAO
	var contorno := PackedVector2Array([origem])
	contorno.append_array(arco)
	draw_colored_polygon(contorno, COR_MIRA)
	contorno.append(origem)
	draw_polyline(contorno, COR_BORDA_DA_MIRA, 1.0)


func _desenhar_onda() -> void:
	var avanco := _tempo_da_onda / segundos_da_onda
	var raio := alcance * (1.0 - pow(1.0 - avanco, 3.0))
	var cor := COR_ONDA
	cor.a = 1.0 - avanco
	draw_polyline(_pontos_do_arco(_direcao_da_onda, raio), cor, 2.0)
	draw_polyline(_pontos_do_arco(_direcao_da_onda, raio * 0.7), Color(cor.r, cor.g, cor.b, cor.a * 0.5), 1.0)
