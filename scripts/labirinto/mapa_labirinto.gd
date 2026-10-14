class_name MapaLabirinto
extends Resource

const LETRAS_DE_OBSTACULO := "bcmxrkauhijNZ"

@export var tamanho_bloco: int = 32
@export var blocos_por_salinha: int = 3
@export var salinhas_seguras: Array[Rect2i] = []
@export var area_oficina: Rect2i = Rect2i()
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
	return l == "#" or l == "D"


func e_obstaculo(celula: Vector2i) -> bool:
	return LETRAS_DE_OBSTACULO.contains(letra(celula))


func salinha_segura(salinha: Vector2i) -> bool:
	for retangulo in salinhas_seguras:
		if retangulo.has_point(salinha):
			return true
	return false


func celulas_com(procurada: String) -> Array[Vector2i]:
	var achadas: Array[Vector2i] = []
	for y in altura():
		for x in largura():
			if linhas[y][x] == procurada:
				achadas.append(Vector2i(x, y))
	return achadas
