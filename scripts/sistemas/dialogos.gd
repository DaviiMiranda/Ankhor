extends Node

signal comecou(caminho: String)
signal fala_mostrada(quem: String, texto: String, retrato: Texture2D)
signal escolhas_mostradas(opcoes: Array)
signal terminou(caminho: String)

const PASTA_RETRATOS := "res://assets/sprites/personagens/%s.png"

var ativo := false
var vistos: Dictionary = {}
var _caminho := ""
var _dados: Dictionary = {}
var _falas: Array = []
var _indice := 0
var _escolhas_do_trecho: Array = []
var _escolhas: Array = []
var _seguinte := ""


func iniciar(caminho: String) -> void:
	if ativo or get_tree().paused:
		return
	var dados: Variant = JSON.parse_string(FileAccess.get_file_as_string(caminho))
	if not dados is Dictionary:
		push_error("Dialogo invalido: " + caminho)
		return
	_caminho = caminho
	_dados = dados
	ativo = true
	get_tree().paused = true
	comecou.emit(caminho)
	_entrar(_dados.get("inicio", ""))


func ja_viu(caminho: String) -> bool:
	return vistos.has(caminho)


func esperando_escolha() -> bool:
	return not _escolhas.is_empty()


func avancar() -> void:
	if not ativo or esperando_escolha():
		return
	_indice += 1
	if _indice < _falas.size():
		_mostrar_fala()
	else:
		_fim_do_trecho()


func escolher(indice: int) -> void:
	if not ativo or indice < 0 or indice >= _escolhas.size():
		return
	var destino: String = _escolhas[indice].get("vai_para", "")
	_escolhas = []
	_entrar(destino)


func _entrar(id_trecho: String) -> void:
	var trechos: Dictionary = _dados.get("trechos", {})
	if not trechos.has(id_trecho):
		_terminar()
		return
	var trecho: Dictionary = trechos[id_trecho]
	_falas = trecho.get("falas", [])
	_escolhas_do_trecho = trecho.get("escolhas", [])
	_seguinte = trecho.get("vai_para", "")
	_indice = 0
	if _falas.is_empty():
		_fim_do_trecho()
	else:
		_mostrar_fala()


func _mostrar_fala() -> void:
	var fala: Dictionary = _falas[_indice]
	fala_mostrada.emit(fala.get("quem", ""), fala.get("texto", ""), _retrato(fala.get("retrato", "")))


func _fim_do_trecho() -> void:
	if not _escolhas_do_trecho.is_empty():
		_escolhas = _escolhas_do_trecho
		escolhas_mostradas.emit(_escolhas.map(func(escolha: Dictionary) -> String: return escolha.get("texto", "")))
	elif not _seguinte.is_empty():
		_entrar(_seguinte)
	else:
		_terminar()


func _terminar() -> void:
	vistos[_caminho] = true
	var nota: Dictionary = _dados.get("anotacao", {})
	if not nota.is_empty():
		Caderno.anotar(_dados.get("id", _caminho), nota.get("titulo", ""), nota.get("texto", ""))
	ativo = false
	_escolhas = []
	get_tree().paused = false
	terminou.emit(_caminho)


func _retrato(id_retrato: String) -> Texture2D:
	if id_retrato.is_empty():
		return null
	var caminho := PASTA_RETRATOS % id_retrato
	if not ResourceLoader.exists(caminho):
		push_warning("Retrato nao encontrado: " + caminho)
		return null
	return load(caminho)
