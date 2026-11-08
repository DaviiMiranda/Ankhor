class_name PilhaNoChao
extends Interagivel

const GADGETS_COM_PILHA := ["lanterna", "notebook"]
const LIMITE_PARA_TROCAR := 0.95
const SOM_TROCA := preload("res://assets/audio/efeitos/objetos/pilha_troca.wav")


func _ready() -> void:
	texto_acao = ""
	if Engine.is_editor_hint():
		return
	super()
	if Inventario.pegos.has(_id_unico()):
		queue_free()


func pode_interagir() -> bool:
	return not _gadget_mais_fraco().is_empty() or _pode_guardar()


func _pode_guardar() -> bool:
	return Inventario.pilhas() < Inventario.MAXIMO_PILHAS


func interagir() -> void:
	var id := _gadget_mais_fraco()
	if id.is_empty():
		Inventario.guardar_pilha()
		Inventario.aviso.emit("Pilha guardada (%d). Use na aba Criação" % Inventario.pilhas())
	else:
		Inventario.estado_de(id)["carga"] = 1.0
		Inventario.aviso.emit("Pilha trocada: lanterna carregada" if id == "lanterna" else "Pilha trocada: %s carregado" % id)
	Inventario.pegos[_id_unico()] = true
	_tocar_som()
	queue_free()


func _gadget_mais_fraco() -> String:
	var melhor := ""
	var menor := LIMITE_PARA_TROCAR
	for id in GADGETS_COM_PILHA:
		if not Inventario.tem(id):
			continue
		var carga: float = Inventario.estado_de(id).get("carga", 1.0)
		if carga < menor:
			menor = carga
			melhor = id
	return melhor


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
