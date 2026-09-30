extends Node2D

const ALTURA_BARRA := -44.0
const LARGURA_BARRA := 16.0
const COR_FUNDO := Color(0.05, 0.08, 0.1)
const COR_PROGRESSO := Color(0.45, 0.9, 1.0)

@export var alcance: float = 44.0
@export var segundos_hack: float = 2.5
@export var gasto_por_hack: float = 0.25
@export var segundos_robo_desligado: float = 8.0

var item: Item
var _estado: Dictionary
var _alvo: Node2D
var _progresso := 0.0

@onready var tela: PointLight2D = $Tela
@onready var som: AudioStreamPlayer = $Som


func _ready() -> void:
	_estado = Inventario.estado_de(item.id if item else "notebook")
	if not _estado.has("carga"):
		_estado["carga"] = 1.0
	_estado["aceso"] = false
	tela.visible = false
	Vida.dano_recebido.connect(_ao_receber_dano)


func usar() -> void:
	if _alvo:
		return
	if _estado["carga"] < gasto_por_hack - 0.001:
		Inventario.aviso.emit("Notebook sem bateria")
		return
	var alvo := _procurar_alvo()
	if alvo == null:
		Inventario.aviso.emit("Nada para hackear. Robôs, só por trás")
		return
	_comecar(alvo)


func ao_desequipar() -> void:
	if _alvo:
		_parar()


func _procurar_alvo() -> Node2D:
	var dono := _dono()
	var melhor: Node2D = null
	var menor := alcance
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		var d := dono.global_position.distance_to(robo.global_position)
		if d < menor and robo.pode_ser_hackeado_de(dono.global_position):
			menor = d
			melhor = robo
	for no in get_tree().get_nodes_in_group("portas"):
		var porta := no as Porta
		var d := dono.global_position.distance_to(porta.global_position)
		if d < menor and porta.trancada and not porta.bloqueada:
			menor = d
			melhor = porta
	return melhor


func _comecar(alvo: Node2D) -> void:
	_alvo = alvo
	_progresso = 0.0
	_estado["aceso"] = true
	tela.visible = true
	som.play()
	_dono().andar_sozinho(Vector2.ZERO)
	if alvo is Robo:
		(alvo as Robo).atordoar(segundos_hack + 0.2)


func _process(delta: float) -> void:
	if _alvo == null:
		return
	_progresso += delta
	queue_redraw()
	if _progresso >= segundos_hack:
		_concluir()


func _concluir() -> void:
	_estado["carga"] = maxf(_estado["carga"] - gasto_por_hack, 0.0)
	if _alvo is Robo:
		(_alvo as Robo).atordoar(segundos_robo_desligado)
		Inventario.aviso.emit("Robô desligado por %d segundos" % int(segundos_robo_desligado))
	elif _alvo is Porta:
		(_alvo as Porta).destrancar()
	_parar()


func _ao_receber_dano(_origem: Vector2) -> void:
	if _alvo:
		som.stop()
		Inventario.aviso.emit("Hack interrompido")
		_parar()


func _parar() -> void:
	_alvo = null
	_estado["aceso"] = false
	tela.visible = false
	_dono().devolver_controle()
	queue_redraw()


func _dono() -> Gabriel:
	return get_parent().get_parent() as Gabriel


func _draw() -> void:
	if _alvo == null:
		return
	var inicio := Vector2(-LARGURA_BARRA / 2.0, ALTURA_BARRA)
	draw_rect(Rect2(inicio - Vector2.ONE, Vector2(LARGURA_BARRA + 2, 4)), COR_FUNDO)
	draw_rect(Rect2(inicio, Vector2(LARGURA_BARRA * _progresso / segundos_hack, 2)), COR_PROGRESSO)
