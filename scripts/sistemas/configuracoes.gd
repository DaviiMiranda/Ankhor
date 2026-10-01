extends Node

signal mudou

const CAMINHO_CONFIG := "user://configuracoes.cfg"
const ROTULOS_VOLUME := {"master": "Volume geral", "musica": "Música", "efeitos": "Efeitos"}

var volume_master: float = 1.0:
	set(valor):
		volume_master = clampf(valor, 0.0, 1.0)
		_aplicar_volume("Master", volume_master)
		salvar()
		mudou.emit()

var volume_musica: float = 1.0:
	set(valor):
		volume_musica = clampf(valor, 0.0, 1.0)
		_aplicar_volume("Musica", volume_musica)
		salvar()
		mudou.emit()

var volume_efeitos: float = 1.0:
	set(valor):
		volume_efeitos = clampf(valor, 0.0, 1.0)
		_aplicar_volume("Efeitos", volume_efeitos)
		salvar()
		mudou.emit()

var efeito_crt: bool = true:
	set(valor):
		efeito_crt = valor
		salvar()
		mudou.emit()


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	carregar()


func carregar() -> void:
	var config := ConfigFile.new()
	if config.load(CAMINHO_CONFIG) == OK:
		volume_master = config.get_value("audio", "master", 1.0)
		volume_musica = config.get_value("audio", "musica", 1.0)
		volume_efeitos = config.get_value("audio", "efeitos", 1.0)
		efeito_crt = config.get_value("video", "crt", true)
	else:
		_aplicar_volume("Master", volume_master)
		_aplicar_volume("Musica", volume_musica)
		_aplicar_volume("Efeitos", volume_efeitos)


func salvar() -> void:
	var config := ConfigFile.new()
	config.set_value("audio", "master", volume_master)
	config.set_value("audio", "musica", volume_musica)
	config.set_value("audio", "efeitos", volume_efeitos)
	config.set_value("video", "crt", efeito_crt)
	config.save(CAMINHO_CONFIG)


func ciclar_volume(tipo: String) -> void:
	var prop := "volume_" + tipo
	var atual: float = get(prop)
	set(prop, fposmod(roundf(atual * 4.0) + 1.0, 5.0) / 4.0)


func ajustar_volume(tipo: String, passo: float) -> void:
	var prop := "volume_" + tipo
	var atual: float = get(prop)
	set(prop, clampf(snappedf(atual + passo, 0.05), 0.0, 1.0))


func texto_volume(tipo: String) -> String:
	var valor: float = get("volume_" + tipo)
	if valor <= 0.001:
		return "%s: Mudo" % ROTULOS_VOLUME[tipo]
	return "%s: %d%%" % [ROTULOS_VOLUME[tipo], roundi(valor * 100.0)]


func _aplicar_volume(bus_nome: String, linear: float) -> void:
	var idx := AudioServer.get_bus_index(bus_nome)
	if idx == -1:
		return
	if linear <= 0.001:
		AudioServer.set_bus_mute(idx, true)
	else:
		AudioServer.set_bus_mute(idx, false)
		AudioServer.set_bus_volume_db(idx, linear_to_db(linear))
