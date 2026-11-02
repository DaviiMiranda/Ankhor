class_name GrafoDaNave
extends RefCounted

const PONTOS := {
	"c1_a": Vector3(0.0, 0.0, 11.0), "c1_m": Vector3(0.0, 0.0, 0.0), "c1_b": Vector3(0.0, 0.0, -11.0),
	"reu_s": Vector3(0.0, 0.0, -13.8), "reu_c": Vector3(0.0, 0.0, -19.3), "reu_n": Vector3(0.0, 0.0, -24.8),
	"reu_o3": Vector3(-6.8, 0.0, -15.8), "reu_o4": Vector3(-6.8, 0.0, -22.8), "reu_l": Vector3(6.8, 0.0, -19.3),
	"c3_a": Vector3(-9.3, 0.0, -15.8), "c3_b": Vector3(-15.3, 0.0, -15.8), "dep": Vector3(-19.5, 0.0, -15.8),
	"c4_a": Vector3(-9.3, 0.0, -22.8), "c4_b": Vector3(-15.3, 0.0, -22.8), "maq": Vector3(-19.5, 0.0, -22.8),
	"cab": Vector3(10.5, 0.0, -19.3),
	"c2_a": Vector3(0.0, 0.0, -27.6), "c2_m": Vector3(0.0, 0.0, -38.6), "c2_b": Vector3(0.0, 0.0, -49.6),
	"han_s": Vector3(0.0, 0.0, -52.5), "han_c": Vector3(0.0, 0.0, -55.0),
}
const ARESTAS: Array[Array] = [
	["c1_a", "c1_m"], ["c1_m", "c1_b"], ["c1_b", "reu_s"], ["reu_s", "reu_c"], ["reu_c", "reu_n"],
	["reu_n", "c2_a"], ["c2_a", "c2_m"], ["c2_m", "c2_b"], ["c2_b", "han_s"], ["han_s", "han_c"],
	["reu_c", "reu_o3"], ["reu_c", "reu_o4"], ["reu_c", "reu_l"], ["reu_l", "cab"],
	["reu_o3", "c3_a"], ["c3_a", "c3_b"], ["c3_b", "dep"], ["dep", "maq"], ["maq", "c4_b"], ["c4_b", "c4_a"], ["c4_a", "reu_o4"],
]
const PESO_DE_VOLTAR := 0.25

var _vizinhos: Dictionary = {}


func _init() -> void:
	for ponto: String in PONTOS:
		_vizinhos[ponto] = []
	for aresta in ARESTAS:
		_vizinhos[aresta[0]].append(aresta[1])
		_vizinhos[aresta[1]].append(aresta[0])


func lugar(ponto: String) -> Vector3:
	return PONTOS[ponto]


func vizinhos(ponto: String) -> Array:
	return _vizinhos[ponto]


func mais_perto(posicao: Vector3) -> String:
	var melhor := ""
	var menor := INF
	for ponto: String in PONTOS:
		var distancia := posicao.distance_squared_to(PONTOS[ponto])
		if distancia < menor:
			menor = distancia
			melhor = ponto
	return melhor


func rota(origem: String, destino: String) -> PackedStringArray:
	var abertos: Array[String] = [origem]
	var veio_de: Dictionary = {}
	var custo: Dictionary = {origem: 0.0}
	while not abertos.is_empty():
		var atual := _menor_estimativa(abertos, custo, destino)
		if atual == destino:
			return _refazer_caminho(veio_de, atual)
		abertos.erase(atual)
		for vizinho: String in _vizinhos[atual]:
			var novo_custo: float = custo[atual] + _distancia(atual, vizinho)
			if not custo.has(vizinho) or novo_custo < custo[vizinho]:
				custo[vizinho] = novo_custo
				veio_de[vizinho] = atual
				if not abertos.has(vizinho):
					abertos.append(vizinho)
	return PackedStringArray()


func comprimento_da_rota(caminho: PackedStringArray) -> float:
	var total := 0.0
	for indice in range(1, caminho.size()):
		total += _distancia(caminho[indice - 1], caminho[indice])
	return total


func proximo_na_ronda(atual: String, anterior: String, atracao: Vector3, forca_da_atracao: float) -> String:
	var pesos := PackedFloat32Array()
	var opcoes: Array = _vizinhos[atual]
	var distancia_atual: float = lugar(atual).distance_to(atracao)
	for vizinho: String in opcoes:
		var peso := PESO_DE_VOLTAR if vizinho == anterior else 1.0
		if lugar(vizinho).distance_to(atracao) < distancia_atual:
			peso += forca_da_atracao
		pesos.append(peso)
	return opcoes[_sortear(pesos)]


func _sortear(pesos: PackedFloat32Array) -> int:
	var total := 0.0
	for peso in pesos:
		total += peso
	var sorteio := randf() * total
	for indice in pesos.size():
		sorteio -= pesos[indice]
		if sorteio <= 0.0:
			return indice
	return pesos.size() - 1


func _menor_estimativa(abertos: Array[String], custo: Dictionary, destino: String) -> String:
	var melhor := abertos[0]
	var menor := INF
	for ponto in abertos:
		var estimativa: float = custo[ponto] + _distancia(ponto, destino)
		if estimativa < menor:
			menor = estimativa
			melhor = ponto
	return melhor


func _refazer_caminho(veio_de: Dictionary, fim: String) -> PackedStringArray:
	var caminho := PackedStringArray([fim])
	var atual := fim
	while veio_de.has(atual):
		atual = veio_de[atual]
		caminho.insert(0, atual)
	return caminho


func _distancia(a: String, b: String) -> float:
	return (PONTOS[a] as Vector3).distance_to(PONTOS[b])
