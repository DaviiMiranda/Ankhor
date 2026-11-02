class_name SalaDaNave
extends KitDaNave

const ESPACO_DAS_COSTELAS := 4.0
const ESPESSURA_DA_COSTELA := 0.22
const RECUO_DA_COSTELA := 0.1
const FORRO_RECUADO := 0.22

@export var tamanho := Vector3(8.0, 2.7, 8.0)
@export var portas_norte := PackedFloat32Array()
@export var portas_sul := PackedFloat32Array()
@export var portas_leste := PackedFloat32Array()
@export var portas_oeste := PackedFloat32Array()


func _montar() -> void:
	limites = AABB(Vector3(-tamanho.x / 2.0, 0.0, -tamanho.z / 2.0), tamanho)
	_montar_chao()
	_montar_paredes()
	_montar_teto()
	_montar_costelas()
	_montar_faixas()
	_montar_colisao_do_piso()
	_decorar()


func _decorar() -> void:
	pass


func _montar_chao() -> void:
	var x := tamanho.x / 2.0
	var z := tamanho.z / 2.0
	var margem := minf(0.7, x * 0.3)
	quadrilatero(Vector3(-x, 0.0, -z), Vector3(x, 0.0, -z), Vector3(x, 0.0, z), Vector3(-x, 0.0, z), material("grade"))
	var y := 0.004
	quadrilatero(Vector3(-x + margem, y, -z + margem), Vector3(x - margem, y, -z + margem), Vector3(x - margem, y, z - margem), Vector3(-x + margem, y, z - margem), material("chapa"))


func _montar_paredes() -> void:
	var x := tamanho.x / 2.0
	var z := tamanho.z / 2.0
	var y := tamanho.y
	parede(Vector3(-x, 0.0, -z), Vector3(x, 0.0, -z), y, portas_norte, material("parede"))
	parede(Vector3(-x, 0.0, z), Vector3(x, 0.0, z), y, portas_sul, material("parede"))
	parede(Vector3(-x, 0.0, -z), Vector3(-x, 0.0, z), y, portas_oeste, material("parede"))
	_montar_parede_leste()


func _montar_parede_leste() -> void:
	var x := tamanho.x / 2.0
	var z := tamanho.z / 2.0
	parede(Vector3(x, 0.0, -z), Vector3(x, 0.0, z), tamanho.y, portas_leste, material("parede"))


func _montar_teto() -> void:
	var x := tamanho.x / 2.0
	var z := tamanho.z / 2.0
	var fundo := tamanho.y + FORRO_RECUADO
	quadrilatero(Vector3(-x, fundo, -z), Vector3(x, fundo, -z), Vector3(x, fundo, z), Vector3(-x, fundo, z), material("forro"))
	var borda := 0.5
	for lado: float in [-1.0, 1.0]:
		bloco(Vector3(tamanho.x, FORRO_RECUADO, borda), Vector3(0.0, tamanho.y + FORRO_RECUADO / 2.0, lado * (z - borda / 2.0)), material("parede_escura"))
		bloco(Vector3(borda, FORRO_RECUADO, tamanho.z), Vector3(lado * (x - borda / 2.0), tamanho.y + FORRO_RECUADO / 2.0, 0.0), material("parede_escura"))
	var linhas := int(tamanho.x / 1.1)
	for indice in linhas:
		var lugar_x := -x + (float(indice) + 0.5) * tamanho.x / float(linhas)
		var raio := 0.03 + 0.03 * float(indice % 3) / 2.0
		tubo(raio, tamanho.z, Vector3(lugar_x, fundo - 0.08, 0.0), material("costela"), Vector3.BACK)
	var travessas := int(tamanho.z / 1.6)
	for indice in travessas:
		var lugar_z := -z + (float(indice) + 0.5) * tamanho.z / float(travessas)
		bloco(Vector3(tamanho.x, 0.09, 0.09), Vector3(0.0, fundo - 0.15, lugar_z), material("parede_escura"))
	forma(Vector3(tamanho.x, 0.4, tamanho.z), Vector3(0.0, tamanho.y + 0.2, 0.0))


func _montar_costelas() -> void:
	var x := tamanho.x / 2.0
	var z := tamanho.z / 2.0
	var y := tamanho.y
	for lugar_x in _posicoes_das_costelas(tamanho.x, portas_norte):
		_costela(Vector3(lugar_x, y / 2.0, -z + RECUO_DA_COSTELA / 2.0), Vector3(ESPESSURA_DA_COSTELA, y, RECUO_DA_COSTELA))
	for lugar_x in _posicoes_das_costelas(tamanho.x, portas_sul):
		_costela(Vector3(lugar_x, y / 2.0, z - RECUO_DA_COSTELA / 2.0), Vector3(ESPESSURA_DA_COSTELA, y, RECUO_DA_COSTELA))
	for lugar_z in _posicoes_das_costelas(tamanho.z, portas_oeste):
		_costela(Vector3(-x + RECUO_DA_COSTELA / 2.0, y / 2.0, lugar_z), Vector3(RECUO_DA_COSTELA, y, ESPESSURA_DA_COSTELA))
	for lugar_z in _posicoes_das_costelas(tamanho.z, portas_leste):
		_costela(Vector3(x - RECUO_DA_COSTELA / 2.0, y / 2.0, lugar_z), Vector3(RECUO_DA_COSTELA, y, ESPESSURA_DA_COSTELA))
	for lado: float in [-1.0, 1.0]:
		bloco(Vector3(tamanho.x, 0.2, RECUO_DA_COSTELA), Vector3(0.0, y - 0.1, lado * (z - RECUO_DA_COSTELA / 2.0)), material("costela"))
		bloco(Vector3(RECUO_DA_COSTELA, 0.2, tamanho.z), Vector3(lado * (x - RECUO_DA_COSTELA / 2.0), y - 0.1, 0.0), material("costela"))


func _posicoes_das_costelas(comprimento: float, portas: PackedFloat32Array) -> PackedFloat32Array:
	var posicoes := PackedFloat32Array()
	var total := int(comprimento / ESPACO_DAS_COSTELAS)
	for indice in total + 1:
		var lugar := -comprimento / 2.0 + comprimento * float(indice) / float(maxi(total, 1))
		var livre := true
		for porta in portas:
			livre = livre and absf(lugar - porta) > LARGURA_DA_PORTA / 2.0 + 0.15
		if livre:
			posicoes.append(lugar)
	return posicoes


func _costela(lugar: Vector3, medidas: Vector3) -> void:
	bloco(medidas, lugar, material("costela"))


func _montar_faixas() -> void:
	var x := tamanho.x / 2.0 - 0.09
	var z := tamanho.z / 2.0 - 0.09
	_faixa_no_rodape(Vector3(-x, 0.02, -z), Vector3(x, 0.02, -z), portas_norte)
	_faixa_no_rodape(Vector3(-x, 0.02, z), Vector3(x, 0.02, z), portas_sul)
	_faixa_no_rodape(Vector3(-x, 0.02, -z), Vector3(-x, 0.02, z), portas_oeste)
	_faixa_no_rodape(Vector3(x, 0.02, -z), Vector3(x, 0.02, z), portas_leste)


func _faixa_no_rodape(inicio: Vector3, fim: Vector3, portas: PackedFloat32Array) -> void:
	var direcao := (fim - inicio).normalized()
	var comprimento := inicio.distance_to(fim)
	var ordenadas := portas.duplicate()
	ordenadas.sort()
	var cursor := 0.0
	for porta in ordenadas:
		var centro := comprimento / 2.0 + porta
		_pedaco_de_faixa(inicio, direcao, cursor, centro - LARGURA_DA_PORTA / 2.0 - 0.2)
		cursor = centro + LARGURA_DA_PORTA / 2.0 + 0.2
	_pedaco_de_faixa(inicio, direcao, cursor, comprimento)


func _pedaco_de_faixa(inicio: Vector3, direcao: Vector3, de: float, ate: float) -> void:
	if ate - de <= 0.01:
		return
	var eixo := Vector3(absf(direcao.x), 0.0, absf(direcao.z))
	var medidas := eixo * (ate - de) + (Vector3.ONE - eixo - Vector3.UP) * 0.06 + Vector3.UP * 0.024
	var nova := bloco(medidas, inicio + direcao * (de + ate) / 2.0, material_das_faixas)
	nova.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


func _montar_colisao_do_piso() -> void:
	forma(Vector3(tamanho.x, 0.4, tamanho.z), Vector3(0.0, -0.2, 0.0))


func novo_objeto(texto: String, lugar: Vector3, segundos: float = 0.0) -> ObjetoDaNave:
	var novo := ObjetoDaNave.new()
	novo.texto_acao = texto
	novo.segundos_para_usar = segundos
	novo.position = lugar
	add_child(novo)
	return novo


func caixote(lugar: Vector3, medidas: Vector3) -> void:
	bloco_solido(medidas, lugar + Vector3.UP * medidas.y / 2.0, metal_de_caixote())
	bloco(Vector3(medidas.x + 0.01, 0.06, medidas.z + 0.01), lugar + Vector3.UP * medidas.y * 0.7, material("perigo"))


func metal_de_caixote() -> Material:
	return material("parede_escura")


func janelas_a_leste(y_topo: float) -> void:
	var x := tamanho.x / 2.0
	var z := tamanho.z / 2.0
	var quantas := int(tamanho.z / 4.0)
	var sobra := (tamanho.z - 4.0 * float(quantas)) / 2.0
	for indice in quantas:
		janela_em_x(x, -z + sobra + 2.0 + 4.0 * float(indice), 4.0, 0.0, y_topo)
	if sobra > 0.001:
		for lado: float in [-1.0, 1.0]:
			_trecho(Vector3(x, 0.0, lado * z), Vector3(0.0, 0.0, -lado), 0.0, sobra, 0.0, y_topo, material("parede"))
	if tamanho.y > y_topo:
		_trecho(Vector3(x, 0.0, -z), Vector3(0.0, 0.0, 1.0), 0.0, tamanho.z, y_topo, tamanho.y, material("parede"))
