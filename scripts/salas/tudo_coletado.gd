class_name TudoColetado
extends Node

const PASTA_ITENS := "res://dados/itens/"
const PASTA_TRANSMISSOES := "res://dados/transmissoes/"
const PASTA_DIALOGOS := "res://dados/dialogos/"
const PRIORIDADE_DOS_GADGETS := ["arma_impulso", "clarao"]
const PRIORIDADE_DAS_FERRAMENTAS := ["radio", "modulo_pulso", "mapa_diana", "alicate"]


func _ready() -> void:
	if Engine.is_editor_hint():
		return
	_pegar_itens()
	_completar_colecoes()
	_anotar_transmissoes()
	_anotar_dialogos()
	_anotar_documentos()


func _pegar_itens() -> void:
	var itens_de_colecao := {}
	for colecao in Colecionaveis.todas():
		itens_de_colecao[colecao.item.id] = true
	var itens: Array[Item] = []
	for arquivo in ResourceLoader.list_directory(PASTA_ITENS):
		if not arquivo.ends_with(".tres"):
			continue
		var item := load(PASTA_ITENS + arquivo) as Item
		if item == null or itens_de_colecao.has(item.id) or item.carga_pesada or item.exclusivo_do_zane:
			continue
		itens.append(item)
	itens.sort_custom(func(a: Item, b: Item) -> bool: return _peso(a) < _peso(b))
	for item in itens:
		_pegar(item)
	Inventario.definir_pilhas(Inventario.MAXIMO_PILHAS)
	Inventario.mudou.emit()


func _peso(item: Item) -> int:
	if item.id in PRIORIDADE_DOS_GADGETS:
		return PRIORIDADE_DOS_GADGETS.find(item.id)
	if item.equipavel:
		return 10
	if item.id in PRIORIDADE_DAS_FERRAMENTAS:
		return 20 + PRIORIDADE_DAS_FERRAMENTAS.find(item.id)
	return 100


func _pegar(item: Item) -> void:
	if not Inventario.tem(item.id):
		Inventario.vistos[item.id] = true
		if not Inventario.adicionar(item):
			push_warning("TudoColetado: sem espaco no inventario para %s" % item.id)
			return
	if item.maximo_unidades > 0:
		Inventario.definir_unidades(item, item.maximo_unidades)


func _completar_colecoes() -> void:
	for colecao in Colecionaveis.todas():
		for numero in range(1, colecao.total + 1):
			Colecionaveis.coletar(colecao, numero)


func _anotar_documentos() -> void:
	for documento in MesaDoVisor.todos_os_documentos():
		_anotar(documento.id, documento.autor, documento.anotacao)


func _anotar_transmissoes() -> void:
	for arquivo in ResourceLoader.list_directory(PASTA_TRANSMISSOES):
		if not arquivo.ends_with(".tres"):
			continue
		var transmissao := load(PASTA_TRANSMISSOES + arquivo) as Transmissao
		if transmissao == null:
			continue
		Radio.ouvidas[transmissao.id] = true
		_anotar(transmissao.id, transmissao.titulo_anotacao, transmissao.anotacao)


func _anotar_dialogos() -> void:
	for arquivo in ResourceLoader.list_directory(PASTA_DIALOGOS):
		if not arquivo.ends_with(".json"):
			continue
		var caminho := PASTA_DIALOGOS + arquivo
		var dados: Variant = JSON.parse_string(FileAccess.get_file_as_string(caminho))
		if not dados is Dictionary:
			continue
		var nota: Dictionary = dados.get("anotacao", {})
		_anotar(dados.get("id", caminho), nota.get("titulo", ""), nota.get("texto", ""))


func _anotar(id: String, titulo: String, texto: String) -> void:
	if texto.is_empty() or Caderno.tem_anotacao(id):
		return
	Caderno.anotacoes.append({"id": id, "titulo": titulo, "texto": texto, "lida": true})
	Caderno.mudou.emit()
