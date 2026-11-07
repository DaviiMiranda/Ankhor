extends Node2D

const COR_ONDA := Color(0.35, 0.92, 1.0)
const COR_MIRA := Color(0.35, 0.92, 1.0, 0.16)
const COR_BORDA_DA_MIRA := Color(0.35, 0.92, 1.0, 0.75)
const COR_TRAVADA := Color(1.0, 0.95, 0.75, 0.95)
const AVISO_TRAVADA := "Mira travada. Aperte de novo para atirar. Shift cancela"
const AVISO_LIVRE := "Nenhum robô por perto: aponte com WASD. Aperte de novo para atirar. Shift cancela"
const ALTURA_DO_CHAO := Vector2(0, -2)
const PASSOS_DO_ARCO := 14
const TIRA_DO_BRACO := preload("res://assets/sprites/personagens/gabriel/gabriel_arma_lado.png")
const BOCAIS := preload("res://scripts/personagens/quadros_arma_gabriel.gd").QUADROS
const QUADRO_MIRANDO := 1
const QUADRO_ATIRANDO := 2
const POSICAO_DO_FLASH := Vector2(0, -22)

static var _avisou_travada := false
static var _avisou_livre := false

@export var alcance: float = 150.0
@export var alcance_da_trava: float = 150.0
@export_range(1.0, 120.0) var abertura_graus: float = 30.0
@export var velocidade_maxima: float = 400.0
@export var velocidade_minima: float = 170.0
@export var segundos_atordoado: float = 0.9
@export var segundos_entre_disparos: float = 0.45
@export var segundos_da_onda: float = 0.3
@export var energia_flash: float = 2.6
@export var segundos_do_braco_no_disparo: float = 0.25
@export_range(0.05, 1.0) var fator_de_lentidao: float = 0.35
@export var segundos_de_lentidao: float = 15.0

var item: Item

var _gabriel: Gabriel
var _alvo: Robo
var _mirando := false
var _direcao_da_mira := Vector2.RIGHT
var _direcao_da_onda := Vector2.RIGHT
var _tempo_da_onda := -1.0
var _tempo_desde_disparo := 99.0
var _braco_no_ar := false
var _segundos_do_braco := 0.0

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
	elif _braco_no_ar:
		_segurar_braco_do_disparo(delta)
	if _tempo_da_onda >= 0.0:
		_tempo_da_onda += delta
		if _tempo_da_onda > segundos_da_onda:
			_tempo_da_onda = -1.0
	queue_redraw()


func usar() -> void:
	if _mirando:
		_soltar()
		return
	if _tempo_desde_disparo < segundos_entre_disparos:
		return
	if not ModoCombate.ativo and Inventario.unidades(item.id) <= 0:
		Inventario.aviso.emit("Sem balas: crie mais no inventário (3 pilhas cada)")
		return
	_gabriel.mirando = true
	_mirando = true
	_direcao_da_mira = _gabriel.direcao_olhar.normalized()
	_alvo = null
	_manter_alvo()
	_avisar()


func _avisar() -> void:
	if _alvo != null and not _avisou_travada:
		_avisou_travada = true
		Inventario.aviso.emit(AVISO_TRAVADA)
	elif _alvo == null and not _avisou_livre:
		_avisou_livre = true
		Inventario.aviso.emit(AVISO_LIVRE)


func _apontar() -> void:
	if Input.is_action_just_pressed("correr") or not Vida.esta_viva():
		_parar_de_mirar()
		return
	_manter_alvo()
	if _alvo != null:
		_direcao_da_mira = _gabriel.global_position.direction_to(_alvo.global_position)
	else:
		var entrada := Input.get_vector("mover_esquerda", "mover_direita", "mover_cima", "mover_baixo")
		if entrada != Vector2.ZERO:
			_direcao_da_mira = entrada.normalized()
	_gabriel.olhar_para(_direcao_da_mira)
	_mostrar_braco(QUADRO_MIRANDO)


func _segurar_braco_do_disparo(delta: float) -> void:
	_segundos_do_braco -= delta
	if _segundos_do_braco <= 0.0 or _gabriel.get_real_velocity().length() > 1.0:
		_baixar_braco()


func _mostrar_braco(quadro: int) -> void:
	if _gabriel.vista != "lado":
		_baixar_braco()
		return
	if not _braco_no_ar:
		if _gabriel.tira_especial:
			return
		_gabriel.tocar_tira(TIRA_DO_BRACO, BOCAIS.size())
		_braco_no_ar = true
	_gabriel.mostrar_quadro_tira(quadro)
	flash.global_position = _gabriel.to_global(_gabriel.ponto_do_quadro(BOCAIS[quadro]))


func _baixar_braco() -> void:
	flash.position = POSICAO_DO_FLASH
	if not _braco_no_ar:
		return
	_braco_no_ar = false
	if is_instance_valid(_gabriel):
		_gabriel.terminar_tira()


func _manter_alvo() -> void:
	if _alvo != null and not _alvo_ainda_vale():
		_alvo = null
	if _alvo == null:
		_alvo = _robo_mais_perto()


func _alvo_ainda_vale() -> bool:
	if not is_instance_valid(_alvo) or not _alvo.is_inside_tree():
		return false
	return _gabriel.global_position.distance_to(_alvo.global_position) <= alcance_da_trava * 1.3


func _robo_mais_perto() -> Robo:
	var melhor: Robo = null
	var menor := alcance_da_trava
	for no in get_tree().get_nodes_in_group("robos"):
		var distancia := _gabriel.global_position.distance_to((no as Robo).global_position)
		if distancia <= menor:
			menor = distancia
			melhor = no as Robo
	return melhor


func _soltar() -> void:
	_parar_de_mirar(false)
	if not Vida.esta_viva():
		_baixar_braco()
		return
	if not ModoCombate.ativo:
		Inventario.definir_unidades(item, maxi(Inventario.unidades(item.id) - 1, 0))
	_tempo_desde_disparo = 0.0
	_tempo_da_onda = 0.0
	_direcao_da_onda = _direcao_da_mira
	som.play()
	_piscar()
	_afastar_robos()
	_segundos_do_braco = segundos_do_braco_no_disparo
	_mostrar_braco(QUADRO_ATIRANDO)


func _parar_de_mirar(baixar_o_braco := true) -> void:
	if _mirando and is_instance_valid(_gabriel):
		_gabriel.mirando = false
	_mirando = false
	_alvo = null
	if baixar_o_braco:
		_baixar_braco()


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
		robo.deixar_lento(fator_de_lentidao, segundos_de_lentidao)


func _piscar() -> void:
	flash.energy = energia_flash
	create_tween().tween_property(flash, "energy", 0.0, segundos_da_onda)


func _draw() -> void:
	if _mirando:
		_desenhar_cone(_direcao_da_mira)
		_desenhar_trava()
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


func _desenhar_trava() -> void:
	if _alvo == null or not is_instance_valid(_alvo):
		return
	var centro := to_local(_alvo.global_position) + ALTURA_DO_CHAO
	var pulso := 1.0 + 0.15 * sin(Time.get_ticks_msec() / 90.0)
	draw_arc(centro, 11.0 * pulso, 0.0, TAU, 24, COR_TRAVADA, 1.0)
	for i in 4:
		var ponta := Vector2.from_angle(i * TAU / 4.0 + PI / 4.0)
		draw_line(centro + ponta * 9.0 * pulso, centro + ponta * 15.0 * pulso, COR_TRAVADA, 1.0)


func _desenhar_cone(direcao: Vector2) -> void:
	var arco := _pontos_do_arco(direcao, alcance)
	var origem := to_local(_gabriel.global_position) + ALTURA_DO_CHAO
	var contorno := PackedVector2Array([origem])
	contorno.append_array(arco)
	draw_colored_polygon(contorno, COR_MIRA)
	contorno.append(origem)
	draw_polyline(contorno, COR_TRAVADA if _alvo != null else COR_BORDA_DA_MIRA, 1.0)


func _desenhar_onda() -> void:
	var avanco := _tempo_da_onda / segundos_da_onda
	var raio := alcance * (1.0 - pow(1.0 - avanco, 3.0))
	var cor := COR_ONDA
	cor.a = 1.0 - avanco
	draw_polyline(_pontos_do_arco(_direcao_da_onda, raio), cor, 2.0)
	draw_polyline(_pontos_do_arco(_direcao_da_onda, raio * 0.7), Color(cor.r, cor.g, cor.b, cor.a * 0.5), 1.0)
