class_name GradeDeCabos
extends RefCounted

const NORTE := 1
const LESTE := 2
const SUL := 4
const OESTE := 8
const LADOS := NORTE | LESTE | SUL | OESTE
const RETO := NORTE | SUL
const CURVA := NORTE | LESTE
const TE := NORTE | LESTE | SUL
const PONTA := NORTE
const DIRECOES: Array[int] = [NORTE, LESTE, SUL, OESTE]
const VETORES := {NORTE: Vector2i.UP, LESTE: Vector2i.RIGHT, SUL: Vector2i.DOWN, OESTE: Vector2i.LEFT}
const ENFEITES: Array[int] = [RETO, RETO, CURVA, CURVA, CURVA, TE, TE, LADOS, PONTA, PONTA, 0]
const TENTATIVAS_DE_CAMINHO := 80
const TENTATIVAS_DE_EMBARALHAR := 200
const MINIMO_DE_GIROS := 4
const MAXIMO_DE_GIROS_POR_PECA := 1.5

var colunas := 5
var linhas := 3
var minimo_de_celulas := 7
var maximo_de_celulas := 9
var pecas: Array[int] = []
var energizadas: Array[bool] = []
var distancias: Array[int] = []
var entrada := 0
var saida := 0
var caminho: Array[Vector2i] = []

var _certas: Array[int] = []
var _sorteio := RandomNumberGenerator.new()


func _init(novas_colunas: int, novas_linhas: int, minimo: int, maximo: int, semente := -1) -> void:
	colunas = novas_colunas
	linhas = novas_linhas
	minimo_de_celulas = minimo
	maximo_de_celulas = maximo
	if semente >= 0:
		_sorteio.seed = semente
	else:
		_sorteio.randomize()
	sortear()


static func girada(peca: int) -> int:
	return ((peca << 1) | (peca >> 3)) & LADOS


static func oposta(lado: int) -> int:
	return ((lado << 2) | (lado >> 2)) & LADOS


func sortear() -> void:
	_sortear_caminho()
	_montar_pecas()
	_embaralhar()


func indice(celula: Vector2i) -> int:
	return celula.y * colunas + celula.x


func dentro(celula: Vector2i) -> bool:
	return celula.x >= 0 and celula.x < colunas and celula.y >= 0 and celula.y < linhas


func girar(celula: Vector2i) -> bool:
	var i := indice(celula)
	if girada(pecas[i]) == pecas[i]:
		return false
	pecas[i] = girada(pecas[i])
	_calcular_energia()
	return true


func ligada() -> bool:
	var ultima := indice(Vector2i(colunas - 1, saida))
	return energizadas[ultima] and (pecas[ultima] & LESTE) != 0


func giros_para_resolver() -> int:
	var total := 0
	for celula in caminho:
		var i := indice(celula)
		total += _giros_ate(pecas[i], _certas[i])
	return total


func resolver_caminho() -> void:
	for celula in caminho:
		var i := indice(celula)
		pecas[i] = _certas[i]
	_calcular_energia()


func _giros_ate(atual: int, certa: int) -> int:
	var peca := atual
	for giros in range(4):
		if peca == certa:
			return giros
		peca = girada(peca)
	return 0


func _sortear_caminho() -> void:
	for _tentativa in TENTATIVAS_DE_CAMINHO:
		entrada = _sorteio.randi_range(0, linhas - 1)
		saida = _sorteio.randi_range(0, linhas - 1)
		caminho = [Vector2i(0, entrada)]
		if _estender():
			return
	entrada = 0
	saida = 0
	caminho.clear()
	for x in colunas:
		caminho.append(Vector2i(x, 0))


func _estender() -> bool:
	var ponta := caminho[-1]
	if ponta == Vector2i(colunas - 1, saida):
		return caminho.size() >= minimo_de_celulas
	var distancia_ate_a_saida := absi(colunas - 1 - ponta.x) + absi(saida - ponta.y)
	if caminho.size() + distancia_ate_a_saida > maximo_de_celulas:
		return false
	for lado in _lados_ao_acaso():
		var proxima: Vector2i = ponta + VETORES[lado]
		if dentro(proxima) and not caminho.has(proxima):
			caminho.append(proxima)
			if _estender():
				return true
			caminho.pop_back()
	return false


func _lados_ao_acaso() -> Array[int]:
	var lados: Array[int] = DIRECOES.duplicate()
	for i in range(lados.size() - 1, 0, -1):
		var j := _sorteio.randi_range(0, i)
		var guardado: int = lados[i]
		lados[i] = lados[j]
		lados[j] = guardado
	return lados


func _lado_para(de: Vector2i, para: Vector2i) -> int:
	for lado in DIRECOES:
		if VETORES[lado] == para - de:
			return lado
	return 0


func _montar_pecas() -> void:
	pecas.clear()
	for i in colunas * linhas:
		pecas.append(ENFEITES[_sorteio.randi_range(0, ENFEITES.size() - 1)])
	for i in caminho.size():
		var anterior := Vector2i(-1, caminho[i].y) if i == 0 else caminho[i - 1]
		var seguinte := Vector2i(colunas, caminho[i].y) if i == caminho.size() - 1 else caminho[i + 1]
		pecas[indice(caminho[i])] = _lado_para(caminho[i], anterior) | _lado_para(caminho[i], seguinte)
	_certas = pecas.duplicate()
	energizadas.resize(pecas.size())
	distancias.resize(pecas.size())


func _embaralhar() -> void:
	for _tentativa in TENTATIVAS_DE_EMBARALHAR:
		pecas = _certas.duplicate()
		for i in pecas.size():
			for _volta in _sorteio.randi_range(0, 3):
				pecas[i] = girada(pecas[i])
		_calcular_energia()
		if not ligada() and _giros_aceitaveis(giros_para_resolver()):
			return


func _giros_aceitaveis(giros: int) -> bool:
	return giros >= MINIMO_DE_GIROS and giros <= ceili(caminho.size() * MAXIMO_DE_GIROS_POR_PECA)


func _calcular_energia() -> void:
	energizadas.fill(false)
	distancias.fill(-1)
	var origem := Vector2i(0, entrada)
	if (pecas[indice(origem)] & OESTE) == 0:
		return
	energizadas[indice(origem)] = true
	distancias[indice(origem)] = 0
	var fila: Array[Vector2i] = [origem]
	while not fila.is_empty():
		var atual: Vector2i = fila.pop_front()
		for lado in DIRECOES:
			if (pecas[indice(atual)] & lado) == 0:
				continue
			var vizinha: Vector2i = atual + VETORES[lado]
			if not dentro(vizinha) or energizadas[indice(vizinha)]:
				continue
			if (pecas[indice(vizinha)] & oposta(lado)) == 0:
				continue
			energizadas[indice(vizinha)] = true
			distancias[indice(vizinha)] = distancias[indice(atual)] + 1
			fila.append(vizinha)
