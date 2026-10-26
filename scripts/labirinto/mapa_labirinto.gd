class_name MapaLabirinto
extends Resource

const LETRAS_DE_OBSTACULO := "bcmxrkauhijNZByenlv"

@export var tamanho_bloco: int = 32
@export var blocos_por_salinha: int = 3
@export var salinhas_seguras: Array[Rect2i] = []
@export var area_oficina: Rect2i = Rect2i()
@export var salas: Array[Rect2i] = []
@export var esconderijo: Rect2i = Rect2i()
@export var linhas: PackedStringArray = PackedStringArray()


func largura() -> int:
	return linhas[0].length() if not linhas.is_empty() else 0


func altura() -> int:
	return linhas.size()


func letra(celula: Vector2i) -> String:
	if celula.x < 0 or celula.y < 0 or celula.x >= largura() or celula.y >= altura():
		return "#"
	return linhas[celula.y][celula.x]


func e_parede(celula: Vector2i) -> bool:
	var l := letra(celula)
	return l == "#" or l == "D" or l == "Q" or l == "H" or l == "F"


func e_parede_falsa(celula: Vector2i) -> bool:
	return letra(celula) == "F"


func e_obstaculo(celula: Vector2i) -> bool:
	return LETRAS_DE_OBSTACULO.contains(letra(celula))


func salinha_segura(salinha: Vector2i) -> bool:
	for retangulo in salinhas_seguras:
		if retangulo.has_point(salinha):
			return true
	return false


func indice_da_sala(celula: Vector2i) -> int:
	for i in salas.size():
		if salas[i].has_point(celula):
			return i
	return -1


func entrada_da_sala(indice: int) -> Array[Vector2i]:
	var sala := salas[indice]
	var achadas: Array[Vector2i] = []
	for y in range(sala.position.y - 1, sala.end.y + 1):
		for x in range(sala.position.x - 1, sala.end.x + 1):
			var na_borda_x := x < sala.position.x or x >= sala.end.x
			var na_borda_y := y < sala.position.y or y >= sala.end.y
			if na_borda_x == na_borda_y:
				continue
			if not e_parede(Vector2i(x, y)):
				achadas.append(Vector2i(x, y))
	return achadas


func celulas_com(procurada: String) -> Array[Vector2i]:
	var achadas: Array[Vector2i] = []
	for y in altura():
		for x in largura():
			if linhas[y][x] == procurada:
				achadas.append(Vector2i(x, y))
	return achadas
