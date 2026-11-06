class_name TelaCarregandoVr
extends CanvasLayer

signal terminou

const ETAPAS := ["Ligando o visor", "Calibrando as lentes", "Montando o ambiente"]
const ETAPA_FINAL := "Pronto"
const PONTOS_POR_SEGUNDO := 3.0
const MAXIMO_ESPERANDO := 0.99
const PISCADAS_AO_LIGAR := [
	[0.0, 0.10], [1.0, 0.04], [0.0, 0.07], [0.7, 0.03], [0.0, 0.10], [1.0, 0.05], [0.25, 0.04],
]

@export var segundos: float = 3.0
@export var segundos_cheia: float = 0.35
@export var segundos_apagando: float = 0.12
@export var intervalo_das_falhas := Vector2(0.35, 0.9)
@export var segundos_de_falha: float = 0.05
@export var brilho_na_falha: float = 0.35

var cena_a_carregar := ""
var cena_carregada: PackedScene
var _carregou := false
var _tempo := 0.0
var _tempo_cheia := -1.0
var _progresso := 0.0
var _terminou := false
var _segundos_ligando := 0.0
var _proxima_falha := 0.0
var _fim_da_falha := 0.0
var _sorteio := RandomNumberGenerator.new()

@onready var fundo: Control = $Fundo
@onready var coluna: Control = $Fundo/Centro/Coluna
@onready var barra: ProgressBar = $Fundo/Centro/Coluna/Barra
@onready var porcentagem: Label = $Fundo/Centro/Coluna/Linha/Porcentagem
@onready var etapa: Label = $Fundo/Centro/Coluna/Linha/Etapa
@onready var som_ligando: AudioStreamPlayer = $SomLigando


func _ready() -> void:
	if cena_a_carregar.is_empty() or ResourceLoader.load_threaded_request(cena_a_carregar) != OK:
		_carregou = true
	_sorteio.randomize()
	for trecho in PISCADAS_AO_LIGAR:
		_segundos_ligando += trecho[1]
	_proxima_falha = _segundos_ligando + _sorteio.randf_range(intervalo_das_falhas.x, intervalo_das_falhas.y)
	_mostrar_progresso()
	_piscar()
	som_ligando.play()


func _process(delta: float) -> void:
	_tempo += delta
	_conferir_carga()
	_mostrar_progresso()
	_piscar()
	if _progresso >= 1.0 and _tempo_cheia < 0.0:
		_tempo_cheia = _tempo
	if _tempo_cheia >= 0.0 and _tempo - _tempo_cheia >= segundos_cheia and not _terminou:
		_terminou = true
		terminou.emit()


func _piscar() -> void:
	fundo.modulate.a = _brilho_da_tela()
	coluna.modulate.a = _brilho_do_texto()


func _brilho_da_tela() -> float:
	if _tempo < _segundos_ligando:
		var inicio := 0.0
		for trecho in PISCADAS_AO_LIGAR:
			if _tempo < inicio + trecho[1]:
				return trecho[0]
			inicio += trecho[1]
	if _tempo_cheia >= 0.0:
		var apagando := _tempo - _tempo_cheia - (segundos_cheia - segundos_apagando)
		return 1.0 - clampf(apagando / segundos_apagando, 0.0, 1.0)
	return 1.0


func _brilho_do_texto() -> float:
	if _progresso >= 1.0:
		return 1.0
	if _tempo >= _proxima_falha:
		_fim_da_falha = _tempo + segundos_de_falha
		_proxima_falha = _tempo + _sorteio.randf_range(intervalo_das_falhas.x, intervalo_das_falhas.y)
	return brilho_na_falha if _tempo < _fim_da_falha else 1.0


func _conferir_carga() -> void:
	if _carregou:
		return
	var estado := ResourceLoader.load_threaded_get_status(cena_a_carregar)
	if estado == ResourceLoader.THREAD_LOAD_IN_PROGRESS:
		return
	if estado == ResourceLoader.THREAD_LOAD_LOADED:
		cena_carregada = ResourceLoader.load_threaded_get(cena_a_carregar) as PackedScene
	_carregou = true


func _mostrar_progresso() -> void:
	var enchendo := maxf(segundos - _segundos_ligando - segundos_cheia, 0.1)
	var fracao := clampf((_tempo - _segundos_ligando) / enchendo, 0.0, 1.0)
	_progresso = _curva_de_carga(fracao)
	if not _carregou:
		_progresso = minf(_progresso, MAXIMO_ESPERANDO)
	barra.value = _progresso * barra.max_value
	porcentagem.text = "%d%%" % floori(_progresso * 100.0)
	_escrever_etapa()


func _curva_de_carga(fracao: float) -> float:
	var degraus := fracao + 0.035 * sin(fracao * TAU * 3.0)
	return clampf(ease(degraus, -1.6), 0.0, 1.0)


func _escrever_etapa() -> void:
	if _progresso >= 1.0:
		etapa.text = ETAPA_FINAL
		return
	var indice := mini(int(_progresso * ETAPAS.size()), ETAPAS.size() - 1)
	var pontos := ".".repeat(int(_tempo * PONTOS_POR_SEGUNDO) % 4)
	etapa.text = ETAPAS[indice] + pontos
