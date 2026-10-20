extends Node

signal salvou
signal carregou

const CAMINHO := "user://salvamento.cfg"
const VERSAO := 1
const CAMINHO_ITEM := "res://dados/itens/%s.tres"
const FORMATO_DATA := "%02d/%02d/%04d %02d:%02d"


func existe() -> bool:
	return FileAccess.file_exists(CAMINHO)


func cena_salva() -> String:
	var arquivo := _ler()
	if arquivo == null:
		return ""
	return arquivo.get_value("jogo", "cena", "")


func data_salva() -> String:
	var arquivo := _ler()
	if arquivo == null:
		return ""
	var data: Dictionary = arquivo.get_value("jogo", "data", {})
	if data.is_empty():
		return ""
	return FORMATO_DATA % [data.day, data.month, data.year, data.hour, data.minute]


func salvar(cena: String, posicao: Vector2) -> bool:
	var arquivo := ConfigFile.new()
	arquivo.set_value("jogo", "versao", VERSAO)
	arquivo.set_value("jogo", "cena", cena)
	arquivo.set_value("jogo", "data", Time.get_datetime_dict_from_system())
	arquivo.set_value("jogo", "posicao", posicao)
	arquivo.set_value("inventario", "grade", _ids_da_grade())
	arquivo.set_value("inventario", "gadgets", _ids_dos_gadgets())
	arquivo.set_value("inventario", "estado", Inventario.estado)
	arquivo.set_value("inventario", "pegos", Inventario.pegos)
	arquivo.set_value("inventario", "vistos", Inventario.vistos)
	arquivo.set_value("caderno", "anotacoes", Caderno.anotacoes)
	arquivo.set_value("radio", "ouvidas", Radio.ouvidas)
	arquivo.set_value("progresso", "marcas", Progresso.marcas)
	arquivo.set_value("progresso", "portas_destrancadas", Porta.destrancadas_salvas())
	arquivo.set_value("dialogos", "vistos", Dialogos.vistos)
	var resultado := arquivo.save(CAMINHO)
	if resultado != OK:
		push_error("Salvamento: nao foi possivel gravar %s (erro %d)" % [CAMINHO, resultado])
		return false
	salvou.emit()
	return true


func carregar() -> bool:
	var arquivo := _ler()
	if arquivo == null:
		return false
	var cena: String = arquivo.get_value("jogo", "cena", "")
	if cena.is_empty() or not ResourceLoader.exists(cena):
		push_error("Salvamento: cena salva nao existe: %s" % cena)
		return false
	Inventario.limpar()
	Caderno.limpar()
	Radio.limpar()
	Vida.limpar()
	Checkpoints.limpar()
	Progresso.limpar()
	_restaurar_inventario(arquivo)
	Caderno.anotacoes.assign(arquivo.get_value("caderno", "anotacoes", []))
	Caderno.mudou.emit()
	Radio.ouvidas = arquivo.get_value("radio", "ouvidas", {})
	Progresso.marcas = arquivo.get_value("progresso", "marcas", {})
	Porta.restaurar_destrancadas(arquivo.get_value("progresso", "portas_destrancadas", []))
	Dialogos.vistos = arquivo.get_value("dialogos", "vistos", {})
	Checkpoints.marcar("maquina_de_salvar", cena, arquivo.get_value("jogo", "posicao", Vector2.ZERO))
	get_tree().paused = false
	carregou.emit()
	get_tree().change_scene_to_file(cena)
	return true


func apagar() -> void:
	if existe():
		DirAccess.remove_absolute(ProjectSettings.globalize_path(CAMINHO))


func _ler() -> ConfigFile:
	var arquivo := ConfigFile.new()
	if arquivo.load(CAMINHO) != OK:
		return null
	if arquivo.get_value("jogo", "versao", 0) != VERSAO:
		return null
	return arquivo


func _ids_da_grade() -> Array:
	var linhas := []
	for linha in Inventario.grade:
		var ids := []
		for item in linha:
			ids.append(item.id if item != null else "")
		linhas.append(ids)
	return linhas


func _ids_dos_gadgets() -> Array:
	var ids := []
	for item in Inventario.gadgets:
		ids.append(item.id if item != null else "")
	return ids


func _restaurar_inventario(arquivo: ConfigFile) -> void:
	var linhas: Array = arquivo.get_value("inventario", "grade", [])
	for l in mini(linhas.size(), Inventario.LINHAS):
		for c in mini(linhas[l].size(), Inventario.COLUNAS):
			Inventario.grade[l][c] = _item_de(linhas[l][c])
	var ids_gadgets: Array = arquivo.get_value("inventario", "gadgets", [])
	for i in mini(ids_gadgets.size(), Inventario.ESPACOS_GADGET):
		Inventario.gadgets[i] = _item_de(ids_gadgets[i])
	Inventario.estado = arquivo.get_value("inventario", "estado", {})
	Inventario.pegos = arquivo.get_value("inventario", "pegos", {})
	Inventario.vistos = arquivo.get_value("inventario", "vistos", {})
	Inventario.mudou.emit()


func _item_de(id: String) -> Item:
	if id.is_empty():
		return null
	var caminho := CAMINHO_ITEM % id
	if not ResourceLoader.exists(caminho):
		push_warning("Salvamento: item sem arquivo, ignorado: %s" % id)
		return null
	return load(caminho) as Item
