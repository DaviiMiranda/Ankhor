extends Node

const FORMATO := "%02d:%02d:%02d"
const MICROSSEGUNDOS_POR_SEGUNDO := 1000000.0
const SEGUNDOS_POR_HORA := 3600.0
const SEGUNDOS_POR_MINUTO := 60.0

var segundos := 0.0
var contando := true
var _ultimo_tique := 0


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_ultimo_tique = Time.get_ticks_usec()


func _process(_delta: float) -> void:
	var agora := Time.get_ticks_usec()
	if _correndo():
		segundos += (agora - _ultimo_tique) / MICROSSEGUNDOS_POR_SEGUNDO
	_ultimo_tique = agora


func comecar(de: float = 0.0) -> void:
	segundos = maxf(de, 0.0)
	contando = true
	_ultimo_tique = Time.get_ticks_usec()


func parar() -> void:
	contando = false


func texto() -> String:
	return formatar(segundos)


static func formatar(total: float) -> String:
	var horas := floori(total / SEGUNDOS_POR_HORA)
	var minutos := floori(fmod(total, SEGUNDOS_POR_HORA) / SEGUNDOS_POR_MINUTO)
	var resto := floori(fmod(total, SEGUNDOS_POR_MINUTO))
	return FORMATO % [horas, minutos, resto]


func _correndo() -> bool:
	return contando and not Pausa.aberta
