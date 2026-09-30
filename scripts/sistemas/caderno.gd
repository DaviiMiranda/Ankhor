extends Node

signal leitura_pedida(documento: Documento)
signal anotado(titulo: String)
signal mudou

var anotacoes: Array[Dictionary] = []


func _ready() -> void:
	limpar()


func limpar() -> void:
	anotacoes = []
	mudou.emit()


func ler(documento: Documento) -> void:
	leitura_pedida.emit(documento)


func anotar(id: String, titulo: String, texto: String) -> void:
	if texto.is_empty() or tem_anotacao(id):
		return
	anotacoes.append({"id": id, "titulo": titulo, "texto": texto, "lida": false})
	anotado.emit(titulo)
	mudou.emit()


func tem_anotacao(id: String) -> bool:
	for anotacao in anotacoes:
		if anotacao["id"] == id:
			return true
	return false


func marcar_lida(indice: int) -> void:
	if indice < 0 or indice >= anotacoes.size() or anotacoes[indice]["lida"]:
		return
	anotacoes[indice]["lida"] = true
	mudou.emit()


func tem_nao_lidas() -> bool:
	for anotacao in anotacoes:
		if not anotacao["lida"]:
			return true
	return false
