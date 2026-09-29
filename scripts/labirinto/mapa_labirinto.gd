class_name MapaLabirinto
extends Resource

@export var tamanho_bloco: int = 32
@export var blocos_por_salinha: int = 3
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


func celulas_com(procurada: String) -> Array[Vector2i]:
	var achadas: Array[Vector2i] = []
	for y in altura():
		for x in largura():
			if linhas[y][x] == procurada:
				achadas.append(Vector2i(x, y))
	return achadas
