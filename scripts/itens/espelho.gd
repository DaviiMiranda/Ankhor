extends Node2D

const COR_RAIO := Color(1.0, 0.35, 0.25)

@export var segundos_de_janela: float = 0.5
@export var segundos_de_espera: float = 3.0
@export var segundos_atordoado: float = 4.0
@export var alcance_do_reflexo: float = 200.0
@export var abertura_do_reflexo_graus: float = 25.0

var item: Item
var _janela := 0.0
var _espera := 0.0
var _raio: Line2D
var _tempo_raio := 0.0

@onready var som: AudioStreamPlayer = $Som


func _ready() -> void:
	Inventario.estado_de(item.id if item else "espelho")["aceso"] = false
	_raio = Line2D.new()
	_raio.width = 2.0
	_raio.default_color = COR_RAIO
	_raio.top_level = true
	_raio.z_index = 20
	_raio.visible = false
	add_child(_raio)


func usar() -> void:
	if _espera > 0.0 or _janela > 0.0:
		return
	_janela = segundos_de_janela
	Inventario.estado_de(item.id)["aceso"] = true


func ao_desequipar() -> void:
	Inventario.estado_de(item.id)["aceso"] = false


func _physics_process(delta: float) -> void:
	_espera = maxf(_espera - delta, 0.0)
	_tempo_raio -= delta
	if _tempo_raio <= 0.0:
		_raio.visible = false
	if _janela <= 0.0:
		return
	_janela -= delta
	var dono := get_parent().get_parent() as Gabriel
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo and robo.farol and robo.estado != Robo.Estado.ATORDOADO and robo.ve_o_gabriel():
			if _rebater(dono, robo):
				_janela = 0.0
				break
	if _janela <= 0.0:
		_janela = 0.0
		_espera = segundos_de_espera
		Inventario.estado_de(item.id)["aceso"] = false


func _rebater(dono: Gabriel, fonte: Robo) -> bool:
	var incidente := fonte.global_position.direction_to(dono.global_position)
	var normal := dono.direcao_olhar
	if incidente.dot(normal) >= 0.0:
		return false
	var refletido := incidente - 2.0 * incidente.dot(normal) * normal
	_atordoar_na_linha(dono.global_position, refletido, fonte)
	_mostrar_raio(dono.global_position, refletido)
	som.play()
	return true


func _atordoar_na_linha(origem: Vector2, direcao: Vector2, fonte: Robo) -> void:
	var limite := cos(deg_to_rad(abertura_do_reflexo_graus))
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo == null:
			continue
		var para := robo.global_position - origem
		if para.length() <= alcance_do_reflexo and direcao.dot(para.normalized()) >= limite:
			robo.atordoar(segundos_atordoado * robo.fator_clarao)
	if fonte.estado != Robo.Estado.ATORDOADO and direcao.dot(origem.direction_to(fonte.global_position)) >= limite:
		fonte.atordoar(segundos_atordoado * fonte.fator_clarao)


func _mostrar_raio(origem: Vector2, direcao: Vector2) -> void:
	var altura := Vector2(0, -24)
	_raio.clear_points()
	_raio.add_point(origem + altura)
	_raio.add_point(origem + altura + direcao * alcance_do_reflexo)
	_raio.visible = true
	_tempo_raio = 0.25
