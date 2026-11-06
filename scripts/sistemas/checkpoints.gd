extends Node

signal marcado(id: String)

var cena := ""
var id := ""
var posicao := Vector2.ZERO


func limpar() -> void:
	ModoCombate.ativo = false
	cena = ""
	id = ""
	posicao = Vector2.ZERO


func marcar(novo_id: String, caminho_cena: String, nova_posicao: Vector2) -> void:
	if ModoCombate.ativo and novo_id != ModoCombate.ID_CHECKPOINT:
		return
	var mudou := novo_id != id or caminho_cena != cena
	id = novo_id
	cena = caminho_cena
	posicao = nova_posicao
	if mudou:
		marcado.emit(novo_id)


func esta_ativo(checkpoint_id: String, caminho_cena: String) -> bool:
	return id == checkpoint_id and cena == caminho_cena


func tem_checkpoint_em(caminho_cena: String) -> bool:
	return not id.is_empty() and cena == caminho_cena


func voltar() -> void:
	Vida.limpar()
	if ModoCombate.ativo:
		Vida.proteger(ModoCombate.SEGUNDOS_PROTEGIDO_AO_VOLTAR)
	get_tree().paused = false
	if cena.is_empty():
		get_tree().reload_current_scene()
	else:
		get_tree().change_scene_to_file(cena)
