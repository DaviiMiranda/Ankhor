class_name PulsoSonar
extends CanvasLayer

const COR_ONDA := Color(0.45, 0.9, 1.0)
const COR_ROBO := Color(1.0, 0.25, 0.2)
const FOLGA_ROBO := 2.0

@export var px_por_segundo: float = 300.0
@export var segundos_de_rastro: float = 0.7
@export var opacidade: float = 0.28

var _grade: GradeLabirinto
var _distancias: Dictionary = {}
var _tempo := 0.0
var _maior := 0
var _marcas: Array[Dictionary] = []
var _tela: Node2D


func iniciar(grade: GradeLabirinto, origem: Vector2, alcance_px: float) -> void:
	_grade = grade
	var limite := ceili(alcance_px / grade.bloco)
	_distancias = grade.distancias(grade.livre_mais_perto(grade.celula(origem)), limite)
	for celula in _distancias:
		_maior = maxi(_maior, _distancias[celula])
	layer = 5
	follow_viewport_enabled = true
	_tela = Node2D.new()
	_tela.draw.connect(_desenhar)
	add_child(_tela)


func _process(delta: float) -> void:
	_tempo += delta
	_marcar_robos()
	_tela.queue_redraw()
	if _frente() > (_maior + 1) * _grade.bloco + segundos_de_rastro * px_por_segundo and _marcas_acabaram():
		queue_free()


func _frente() -> float:
	return _tempo * px_por_segundo


func _marcar_robos() -> void:
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo == null or _ja_marcado(robo):
			continue
		var celula := _grade.celula(robo.global_position)
		if _distancias.has(celula) and _distancias[celula] * _grade.bloco <= _frente():
			_marcas.append({"robo": robo, "posicao": robo.global_position, "desde": _tempo})


func _ja_marcado(robo: Robo) -> bool:
	for marca in _marcas:
		if marca["robo"] == robo:
			return true
	return false


func _marcas_acabaram() -> bool:
	for marca in _marcas:
		if _tempo - marca["desde"] < FOLGA_ROBO:
			return false
	return true


func _desenhar() -> void:
	for celula in _distancias:
		var desde_a_frente: float = (_frente() - _distancias[celula] * _grade.bloco) / px_por_segundo
		if desde_a_frente < 0.0 or desde_a_frente > segundos_de_rastro:
			continue
		var cor := COR_ONDA
		cor.a = opacidade * (1.0 - desde_a_frente / segundos_de_rastro)
		var retangulo := Rect2(Vector2(celula) * _grade.bloco, Vector2.ONE * _grade.bloco)
		_tela.draw_rect(retangulo, cor)
		cor.a *= 1.6
		_tela.draw_rect(retangulo, cor, false, 1.0)
	for marca in _marcas:
		var fracao: float = (_tempo - marca["desde"]) / FOLGA_ROBO
		if fracao < 1.0:
			var cor := COR_ROBO
			cor.a = 1.0 - fracao
			_tela.draw_rect(Rect2(marca["posicao"] - Vector2(3, 8), Vector2(6, 8)), cor)
