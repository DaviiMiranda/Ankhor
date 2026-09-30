class_name PilhaNoChao
extends Interagivel

const ID_LANTERNA := "lanterna"
const SOM_TROCA := preload("res://assets/audio/efeitos/objetos/pilha_troca.wav")


func _ready() -> void:
	texto_acao = "Trocar a pilha"
	if Engine.is_editor_hint():
		return
	super()
	if Inventario.pegos.has(_id_unico()):
		queue_free()


func pode_interagir() -> bool:
	if not Inventario.tem(ID_LANTERNA):
		return false
	return Inventario.estado_de(ID_LANTERNA).get("carga", 1.0) < 0.95


func interagir() -> void:
	Inventario.estado_de(ID_LANTERNA)["carga"] = 1.0
	Inventario.pegos[_id_unico()] = true
	Inventario.aviso.emit("Pilha trocada: lanterna carregada")
	_tocar_som()
	queue_free()


func _tocar_som() -> void:
	var som := AudioStreamPlayer.new()
	som.stream = SOM_TROCA
	som.bus = &"Efeitos"
	som.finished.connect(som.queue_free)
	get_tree().current_scene.add_child(som)
	som.play()


func _id_unico() -> String:
	var sala := owner if owner else get_tree().current_scene
	return "%s:%s" % [sala.scene_file_path, sala.get_path_to(self)]
