class_name GradeLabirinto
extends RefCounted

const VIZINHOS: Array[Vector2i] = [Vector2i.RIGHT, Vector2i.LEFT, Vector2i.DOWN, Vector2i.UP]
const PESO_VOLTAR := 0.15

var mapa: MapaLabirinto
var bloco: float
var astar := AStarGrid2D.new()


func _init(novo_mapa: MapaLabirinto) -> void:
	mapa = novo_mapa
	bloco = mapa.tamanho_bloco
	astar.region = Rect2i(0, 0, mapa.largura(), mapa.altura())
	astar.cell_size = Vector2(bloco, bloco)
	astar.offset = Vector2(bloco, bloco) / 2.0
	astar.diagonal_mode = AStarGrid2D.DIAGONAL_MODE_ONLY_IF_NO_OBSTACLES
	astar.default_compute_heuristic = AStarGrid2D.HEURISTIC_OCTILE
	astar.default_estimate_heuristic = AStarGrid2D.HEURISTIC_OCTILE
	astar.update()
	for y in mapa.altura():
		for x in mapa.largura():
			if mapa.e_parede(Vector2i(x, y)):
				astar.set_point_solid(Vector2i(x, y))


func celula(posicao: Vector2) -> Vector2i:
	return Vector2i(floori(posicao.x / bloco), floori(posicao.y / bloco))


func centro(c: Vector2i) -> Vector2:
	return (Vector2(c) + Vector2(0.5, 0.5)) * bloco


func livre(c: Vector2i) -> bool:
	return astar.is_in_boundsv(c) and not astar.is_point_solid(c)


func caminho(de: Vector2, para: Vector2) -> PackedVector2Array:
	var origem := livre_mais_perto(celula(de))
	var destino := livre_mais_perto(celula(para))
	var pontos := astar.get_point_path(origem, destino)
	if not pontos.is_empty():
		pontos.remove_at(0)
	return pontos


func livre_mais_perto(c: Vector2i) -> Vector2i:
	if livre(c):
		return c
	for raio in range(1, 4):
		for dy in range(-raio, raio + 1):
			for dx in range(-raio, raio + 1):
				if livre(c + Vector2i(dx, dy)):
					return c + Vector2i(dx, dy)
	return c


func distancias(origem: Vector2i, limite: int) -> Dictionary:
	var dist := {origem: 0}
	var fila: Array[Vector2i] = [origem]
	var i := 0
	while i < fila.size():
		var atual := fila[i]
		i += 1
		if dist[atual] >= limite:
			continue
		for passo in VIZINHOS:
			var vizinho := atual + passo
			if livre(vizinho) and not dist.has(vizinho):
				dist[vizinho] = dist[atual] + 1
				fila.append(vizinho)
	return dist


func colunas() -> int:
	return (mapa.largura() - 1) / mapa.blocos_por_salinha


func fileiras() -> int:
	return (mapa.altura() - 1) / mapa.blocos_por_salinha


func salinha(posicao: Vector2) -> Vector2i:
	var c := celula(posicao)
	var n := mapa.blocos_por_salinha
	return Vector2i(clampi((c.x - 1) / n, 0, colunas() - 1), clampi((c.y - 1) / n, 0, fileiras() - 1))


func centro_salinha(s: Vector2i) -> Vector2:
	var n := mapa.blocos_por_salinha
	return Vector2((s.x * n + 2) * bloco, (s.y * n + 2) * bloco)


func vizinhas_da_salinha(s: Vector2i) -> Array[Vector2i]:
	var n := mapa.blocos_por_salinha
	var abertas: Array[Vector2i] = []
	var passagens := {
		Vector2i.RIGHT: Vector2i(s.x * n + n, s.y * n + 1),
		Vector2i.LEFT: Vector2i(s.x * n, s.y * n + 1),
		Vector2i.DOWN: Vector2i(s.x * n + 1, s.y * n + n),
		Vector2i.UP: Vector2i(s.x * n + 1, s.y * n),
	}
	for passo in passagens:
		var vizinha: Vector2i = s + passo
		if vizinha.x < 0 or vizinha.y < 0 or vizinha.x >= colunas() or vizinha.y >= fileiras():
			continue
		if livre(passagens[passo]):
			abertas.append(vizinha)
	return abertas


func proxima_salinha(atual: Vector2i, anterior: Vector2i, sorteio: RandomNumberGenerator) -> Vector2i:
	var opcoes := vizinhas_da_salinha(atual)
	if opcoes.is_empty():
		return atual
	var pesos: Array[float] = []
	var total := 0.0
	for opcao in opcoes:
		var peso := PESO_VOLTAR if opcao == anterior and opcoes.size() > 1 else 1.0
		pesos.append(peso)
		total += peso
	var escolha := sorteio.randf() * total
	for i in opcoes.size():
		escolha -= pesos[i]
		if escolha <= 0.0:
			return opcoes[i]
	return opcoes[-1]
