extends Node

signal fechado(salvou: bool)

const CENA := "res://cenas/visor/sala_visor.tscn"
const ID_CHECKPOINT := "maquina_de_salvar"

var cena_do_save := ""
var posicao_do_save := Vector2.ZERO
var salvou := false
var _sala: Node
var _visor: Node
var _modo_do_mouse := Input.MOUSE_MODE_VISIBLE


func esta_aberto() -> bool:
	return _visor != null


func abrir(cena: String, posicao: Vector2) -> void:
	if esta_aberto():
		return
	cena_do_save = cena
	posicao_do_save = posicao
	salvou = false
	_modo_do_mouse = Input.mouse_mode
	_sala = get_tree().current_scene
	_visor = (load(CENA) as PackedScene).instantiate()
	_trocar_cena.call_deferred(_sala, _visor)


func salvar() -> bool:
	Vida.limpar()
	Checkpoints.marcar(ID_CHECKPOINT, cena_do_save, posicao_do_save)
	var deu_certo := Salvamento.salvar(cena_do_save, posicao_do_save)
	salvou = salvou or deu_certo
	return deu_certo


func fechar() -> void:
	if not esta_aberto():
		return
	_voltar_para_a_sala.call_deferred()


func _voltar_para_a_sala() -> void:
	var visor := _visor
	var sala := _sala
	_visor = null
	_sala = null
	_trocar_cena(visor, sala)
	visor.queue_free()
	Input.mouse_mode = _modo_do_mouse
	fechado.emit(salvou)


func _trocar_cena(sai: Node, entra: Node) -> void:
	var raiz := get_tree().root
	raiz.remove_child(sai)
	raiz.add_child(entra)
	get_tree().current_scene = entra


func _exit_tree() -> void:
	if is_instance_valid(_sala) and not _sala.is_inside_tree():
		_sala.free()
