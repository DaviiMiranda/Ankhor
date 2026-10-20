class_name MaquinaDeSalvar
extends Interagivel

const TIRA := preload("res://assets/sprites/personagens/gabriel/gabriel_oculos_lado.png")
const QUADROS := preload("res://scripts/personagens/quadros_oculos_gabriel.gd").QUADROS
const ENERGIA_ATIVA := 1.5
const ALFA_OCIOSA := 0.55
const ESCALA_X_DOS_OCULOS := {"pedestal": 1.0, "mao": 0.45, "rosto": 0.3}
const CAMADA_GABRIEL := 1
const CAMADA_OCULOS := 2
const SEGUNDOS_ATE_O_LUGAR := 3.0
const DISTANCIA_CHEGADA := 1.5

@export var aviso_salvo: String = "Jogo salvo"
@export var deslocamento_retorno := Vector2(0, 14)
@export var segundos_escurecendo: float = 0.9
@export var segundos_por_quadro: float = 0.1

var _salvando := false
var _salvou := false
var _energia_ociosa: float
var _posicao_oculos: Vector2
var _escala_oculos: Vector2

@onready var camada_luz: Sprite2D = $CamadaLuz
@onready var oculos: Sprite2D = $OculosDoZane
@onready var luz: PointLight2D = $Luz


func _ready() -> void:
	super()
	_energia_ociosa = luz.energy
	_posicao_oculos = oculos.position
	_escala_oculos = oculos.scale
	camada_luz.modulate.a = ALFA_OCIOSA


func pode_interagir() -> bool:
	return not _salvando


func interagir() -> void:
	var gabriel := get_tree().get_first_node_in_group("jogador") as Gabriel
	if gabriel == null:
		return
	_salvando = true
	_sessao(gabriel)


func _sessao(gabriel: Gabriel) -> void:
	await _ir_ate_o_lugar(gabriel)
	gabriel.tocar_tira(TIRA, QUADROS.size())
	gabriel.z_index = CAMADA_GABRIEL
	oculos.z_index = CAMADA_OCULOS
	await _tocar_quadros(gabriel, range(QUADROS.size()))
	await _usar_o_visor()
	await _tocar_quadros(gabriel, range(QUADROS.size() - 1, -1, -1))
	_terminar(gabriel)


func _ir_ate_o_lugar(gabriel: Gabriel) -> void:
	var destino := _lugar_do_gabriel()
	var limite := SEGUNDOS_ATE_O_LUGAR
	while limite > 0.0 and gabriel.global_position.distance_to(destino) > DISTANCIA_CHEGADA:
		gabriel.andar_sozinho((destino - gabriel.global_position).normalized())
		await get_tree().physics_frame
		limite -= get_physics_process_delta_time()
	gabriel.andar_sozinho(Vector2.ZERO)
	gabriel.global_position = destino
	gabriel.olhar_para(Vector2.RIGHT)
	await get_tree().physics_frame


func _lugar_do_gabriel() -> Vector2:
	var gabriel := get_tree().get_first_node_in_group("jogador") as Gabriel
	var primeiro_na_mao := 0
	for i in QUADROS.size():
		if QUADROS[i]["fase"] == "mao":
			primeiro_na_mao = i
			break
	var centro_dos_oculos := global_position + _posicao_oculos + _tamanho_dos_oculos(_escala_oculos) / 2.0
	var estava_virado := gabriel.sprite.flip_h
	gabriel.sprite.flip_h = false
	var mao := gabriel.ponto_do_quadro(QUADROS[primeiro_na_mao]["ponto"])
	gabriel.sprite.flip_h = estava_virado
	return centro_dos_oculos - mao


func _tocar_quadros(gabriel: Gabriel, indices: Array) -> void:
	for i in indices:
		gabriel.mostrar_quadro_tira(i)
		_posicionar_oculos(gabriel, QUADROS[i])
		await get_tree().create_timer(segundos_por_quadro).timeout


func _posicionar_oculos(gabriel: Gabriel, quadro: Dictionary) -> void:
	var fase: String = quadro["fase"]
	if fase == "pedestal":
		oculos.position = _posicao_oculos
		oculos.scale = _escala_oculos
		return
	oculos.scale = Vector2(_escala_oculos.x * ESCALA_X_DOS_OCULOS[fase], _escala_oculos.y)
	var centro := gabriel.global_position + gabriel.ponto_do_quadro(quadro["ponto"])
	oculos.global_position = centro - _tamanho_dos_oculos(oculos.scale) / 2.0


func _tamanho_dos_oculos(escala: Vector2) -> Vector2:
	return oculos.texture.get_size() * escala


func _usar_o_visor() -> void:
	var escuro := get_tree().current_scene.get_node_or_null("Transicao/Escuro") as ColorRect
	var acender := create_tween()
	acender.tween_property(luz, "energy", ENERGIA_ATIVA, 0.5)
	acender.parallel().tween_property(camada_luz, "modulate:a", 1.0, 0.5)
	if escuro:
		acender.tween_property(escuro, "color:a", 1.0, segundos_escurecendo)
	await acender.finished
	Visor.abrir(_cena(), global_position + deslocamento_retorno)
	_salvou = await Visor.fechado
	if escuro:
		var clarear := create_tween()
		clarear.tween_property(escuro, "color:a", 0.0, segundos_escurecendo)
		await clarear.finished


func _terminar(gabriel: Gabriel) -> void:
	gabriel.terminar_tira()
	gabriel.z_index = 0
	oculos.z_index = 0
	gabriel.devolver_controle()
	var apagar := create_tween().set_parallel()
	apagar.tween_property(luz, "energy", _energia_ociosa, 0.6)
	apagar.tween_property(camada_luz, "modulate:a", ALFA_OCIOSA, 0.6)
	if _salvou:
		Inventario.aviso.emit(aviso_salvo)
	_salvando = false


func _cena() -> String:
	var sala := owner if owner else get_tree().current_scene
	return sala.scene_file_path if sala else ""
