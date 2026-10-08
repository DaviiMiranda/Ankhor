class_name RobosDaSala
extends Node

@export var tamanho_celula: int = 16
@export var folga_obstaculos: float = 4.0
@export var semente: int = 7

var grade: GradeLabirinto


func _ready() -> void:
	_configurar.call_deferred()


func _configurar() -> void:
	var sala := get_parent() as Sala
	if sala == null:
		return
	grade = GradeLabirinto.new(_mapa_da_sala(sala))
	var numero := 0
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo and sala.is_ancestor_of(robo):
			numero += 1
			robo.configurar(grade, semente * 100 + numero)


func _mapa_da_sala(sala: Sala) -> MapaLabirinto:
	var obstaculos := _obstaculos(sala)
	var linhas := PackedStringArray()
	for y in ceili(float(sala.altura) / tamanho_celula):
		var linha := ""
		for x in ceili(float(sala.largura) / tamanho_celula):
			var centro := (Vector2(x, y) + Vector2(0.5, 0.5)) * tamanho_celula
			linha += "." if _livre(sala, centro, obstaculos) else "#"
		linhas.append(linha)
	var mapa := MapaLabirinto.new()
	mapa.tamanho_bloco = tamanho_celula
	mapa.linhas = linhas
	return mapa


func _livre(sala: Sala, centro: Vector2, obstaculos: Array[Rect2]) -> bool:
	if centro.x < sala.margem_lados or centro.x > sala.largura - sala.margem_lados:
		return false
	if centro.y < sala.chao_fundo or centro.y > sala.chao_frente:
		return false
	for retangulo in obstaculos:
		if retangulo.has_point(centro):
			return false
	return true


func _obstaculos(sala: Sala) -> Array[Rect2]:
	var retangulos: Array[Rect2] = []
	for no in sala.find_children("*", "StaticBody2D", true, false):
		var corpo := no as StaticBody2D
		if corpo.collision_layer & Robo.CAMADA_PAREDES == 0:
			continue
		for filho in corpo.get_children():
			var forma := filho as CollisionShape2D
			if forma and forma.shape is RectangleShape2D:
				var tamanho: Vector2 = (forma.shape as RectangleShape2D).size * forma.global_scale.abs()
				retangulos.append(Rect2(forma.global_position - tamanho / 2.0, tamanho).grow(folga_obstaculos))
	return retangulos
