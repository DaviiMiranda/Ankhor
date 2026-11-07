extends Node

signal salvou
signal carregou

const QUANTIDADE_DE_ESPACOS := 6
const CAMINHO_ESPACO := "user://salvamento_%d.cfg"
const CAMINHO_ANTIGO := "user://salvamento.cfg"
const VERSAO := 1
const CAMINHO_ITEM := "res://dados/itens/%s.tres"
const FORMATO_DATA := "%02d/%02d/%04d %02d:%02d"
const FORMATO_ESPACO := "%d  %s  %s"
const FORMATO_ESPACO_VAZIO := "%d  Vazio"
const FASE_DESCONHECIDA := "?"

var ultimo_espaco := 0


func _ready() -> void:
	_trazer_save_antigo()


func espacos() -> Array:
	return range(1, QUANTIDADE_DE_ESPACOS + 1)


func existe() -> bool:
	return espaco_mais_recente() != 0


func ocupado(espaco: int) -> bool:
	return _ler(espaco) != null


func espaco_mais_recente() -> int:
	var mais_recente := 0
	var momento_mais_recente := -1.0
	for espaco in espacos():
		var arquivo := _ler(espaco)
		if arquivo == null:
			continue
		var momento := _momento(arquivo, espaco)
		if momento > momento_mais_recente:
			mais_recente = espaco
			momento_mais_recente = momento
	return mais_recente


func espaco_sugerido() -> int:
	if ultimo_espaco != 0:
		return ultimo_espaco
	for espaco in espacos():
		if not ocupado(espaco):
			return espaco
	return 1


func data_salva(espaco: int = 0) -> String:
	var arquivo := _ler(espaco if espaco != 0 else espaco_mais_recente())
	if arquivo == null:
		return ""
	var data: Dictionary = arquivo.get_value("jogo", "data", {})
	if data.is_empty():
		return ""
	return FORMATO_DATA % [data.day, data.month, data.year, data.hour, data.minute]


func tempo_salvo(espaco: int) -> float:
	var arquivo := _ler(espaco)
	if arquivo == null:
		return 0.0
	return arquivo.get_value("jogo", "tempo", 0.0)


func texto_do_espaco(espaco: int) -> String:
	var arquivo := _ler(espaco)
	if arquivo == null:
		return FORMATO_ESPACO_VAZIO % espaco
	var fase := Fase.nome_da_cena(arquivo.get_value("jogo", "cena", ""))
	var tempo := TempoDeJogo.formatar(arquivo.get_value("jogo", "tempo", 0.0))
	return FORMATO_ESPACO % [espaco, tempo, FASE_DESCONHECIDA if fase.is_empty() else fase]


func salvar(espaco: int, cena: String, posicao: Vector2) -> bool:
	var arquivo := ConfigFile.new()
	arquivo.set_value("jogo", "versao", VERSAO)
	arquivo.set_value("jogo", "cena", cena)
	arquivo.set_value("jogo", "data", Time.get_datetime_dict_from_system())
	arquivo.set_value("jogo", "momento", Time.get_unix_time_from_system())
	arquivo.set_value("jogo", "tempo", TempoDeJogo.segundos)
	arquivo.set_value("jogo", "posicao", posicao)
	arquivo.set_value("inventario", "grade", _ids_da_grade())
	arquivo.set_value("inventario", "gadgets", _ids_dos_gadgets())
	arquivo.set_value("inventario", "estado", Inventario.estado)
	arquivo.set_value("inventario", "pegos", Inventario.pegos)
	arquivo.set_value("inventario", "vistos", Inventario.vistos)
	arquivo.set_value("inventario", "largados", Inventario.largados)
	arquivo.set_value("caderno", "anotacoes", Caderno.anotacoes)
	arquivo.set_value("radio", "ouvidas", Radio.ouvidas)
	arquivo.set_value("progresso", "marcas", Progresso.marcas)
	arquivo.set_value("progresso", "portas_destrancadas", Porta.destrancadas_salvas())
	arquivo.set_value("dialogos", "vistos", Dialogos.vistos)
	arquivo.set_value("colecionaveis", "pecas", Colecionaveis.pecas)
	var caminho := _caminho(espaco)
	var resultado := arquivo.save(caminho)
	if resultado != OK:
		push_error("Salvamento: nao foi possivel gravar %s (erro %d)" % [caminho, resultado])
		return false
	ultimo_espaco = espaco
	salvou.emit()
	return true


func carregar(espaco: int) -> bool:
	var arquivo := _ler(espaco)
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
	Colecionaveis.limpar()
	_restaurar_inventario(arquivo)
	Caderno.anotacoes.assign(arquivo.get_value("caderno", "anotacoes", []))
	Caderno.mudou.emit()
	Radio.ouvidas = arquivo.get_value("radio", "ouvidas", {})
	Progresso.marcas = arquivo.get_value("progresso", "marcas", {})
	Porta.restaurar_destrancadas(arquivo.get_value("progresso", "portas_destrancadas", []))
	Dialogos.vistos = arquivo.get_value("dialogos", "vistos", {})
	Colecionaveis.pecas = arquivo.get_value("colecionaveis", "pecas", {})
	Checkpoints.marcar("maquina_de_salvar", cena, arquivo.get_value("jogo", "posicao", Vector2.ZERO))
	TempoDeJogo.comecar(arquivo.get_value("jogo", "tempo", 0.0))
	ultimo_espaco = espaco
	get_tree().paused = false
	carregou.emit()
	get_tree().change_scene_to_file(cena)
	return true


func esquecer_ultimo_espaco() -> void:
	ultimo_espaco = 0


func _caminho(espaco: int) -> String:
	return CAMINHO_ESPACO % espaco


func _momento(arquivo: ConfigFile, espaco: int) -> float:
	if arquivo.has_section_key("jogo", "momento"):
		return arquivo.get_value("jogo", "momento")
	return FileAccess.get_modified_time(_caminho(espaco))


func _trazer_save_antigo() -> void:
	if not FileAccess.file_exists(CAMINHO_ANTIGO) or FileAccess.file_exists(_caminho(1)):
		return
	DirAccess.rename_absolute(ProjectSettings.globalize_path(CAMINHO_ANTIGO), ProjectSettings.globalize_path(_caminho(1)))


func _ler(espaco: int) -> ConfigFile:
	if espaco < 1 or espaco > QUANTIDADE_DE_ESPACOS or not FileAccess.file_exists(_caminho(espaco)):
		return null
	var arquivo := ConfigFile.new()
	if arquivo.load(_caminho(espaco)) != OK:
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
	Inventario.largados = arquivo.get_value("inventario", "largados", {})
	Inventario.mudou.emit()


func _item_de(id: String) -> Item:
	if id.is_empty():
		return null
	var caminho := CAMINHO_ITEM % id
	if not ResourceLoader.exists(caminho):
		push_warning("Salvamento: item sem arquivo, ignorado: %s" % id)
		return null
	return load(caminho) as Item
