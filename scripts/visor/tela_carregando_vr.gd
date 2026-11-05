class_name TelaCarregandoVr
extends CanvasLayer

signal terminou

const ETAPAS := ["Ligando o visor", "Calibrando as lentes", "Montando o ambiente"]
const ETAPA_FINAL := "Pronto"
const PONTOS_POR_SEGUNDO := 3.0
const MAXIMO_ESPERANDO := 0.99

@export var segundos: float = 3.0
@export var segundos_aparecendo: float = 0.25
@export var segundos_cheia: float = 0.35

var cena_a_carregar := ""
var cena_carregada: PackedScene
var _carregou := false
var _tempo := 0.0
var _tempo_cheia := -1.0
var _progresso := 0.0
var _terminou := false

@onready var fundo: Control = $Fundo
@onready var barra: ProgressBar = $Fundo/Centro/Coluna/Barra
@onready var porcentagem: Label = $Fundo/Centro/Coluna/Linha/Porcentagem
@onready var etapa: Label = $Fundo/Centro/Coluna/Linha/Etapa


func _ready() -> void:
	if cena_a_carregar.is_empty() or ResourceLoader.load_threaded_request(cena_a_carregar) != OK:
		_carregou = true
	fundo.modulate.a = 0.0
	create_tween().tween_property(fundo, "modulate:a", 1.0, segundos_aparecendo)
	_mostrar_progresso()


func _process(delta: float) -> void:
	_tempo += delta
	_conferir_carga()
	_mostrar_progresso()
	if _progresso >= 1.0 and _tempo_cheia < 0.0:
		_tempo_cheia = _tempo
	if _tempo_cheia >= 0.0 and _tempo - _tempo_cheia >= segundos_cheia and not _terminou:
		_terminou = true
		terminou.emit()


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
	var enchendo := maxf(segundos - segundos_aparecendo - segundos_cheia, 0.1)
	var fracao := clampf((_tempo - segundos_aparecendo) / enchendo, 0.0, 1.0)
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
