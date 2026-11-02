extends Control

@export var segundos_escurecendo: float = 0.8
@export var segundos_por_paragrafo: float = 1.6
@export var pausa_entre_paragrafos: float = 0.5

var _pode_sair := false
var _saindo := false

@onready var titulo: Label = $Titulo
@onready var subtitulo: Label = $Subtitulo
@onready var paragrafos: VBoxContainer = $Historia
@onready var dica: Label = $Dica
@onready var escuro: ColorRect = $Escuro
@onready var som_clique: AudioStreamPlayer = $SomClique


func _ready() -> void:
	titulo.modulate.a = 0.0
	subtitulo.modulate.a = 0.0
	dica.modulate.a = 0.0
	for paragrafo in paragrafos.get_children():
		paragrafo.modulate.a = 0.0
	_mostrar_aos_poucos()


func _unhandled_input(evento: InputEvent) -> void:
	if not _pode_sair or _saindo:
		return
	var escolheu: bool = evento.is_action_pressed("interagir") or evento.is_action_pressed("pausar")
	if evento is InputEventMouseButton and evento.pressed:
		escolheu = true
	if escolheu:
		get_viewport().set_input_as_handled()
		_tirar_o_visor()


func _mostrar_aos_poucos() -> void:
	var sequencia := create_tween()
	sequencia.tween_property(escuro, "color:a", 0.0, segundos_escurecendo)
	sequencia.tween_property(titulo, "modulate:a", 1.0, segundos_por_paragrafo)
	sequencia.tween_property(subtitulo, "modulate:a", 1.0, segundos_por_paragrafo)
	for paragrafo in paragrafos.get_children():
		sequencia.tween_interval(pausa_entre_paragrafos)
		sequencia.tween_property(paragrafo, "modulate:a", 1.0, segundos_por_paragrafo)
	sequencia.tween_interval(pausa_entre_paragrafos)
	sequencia.tween_callback(_liberar_saida)
	sequencia.tween_property(dica, "modulate:a", 1.0, segundos_por_paragrafo / 2.0)


func _liberar_saida() -> void:
	_pode_sair = true


func _tirar_o_visor() -> void:
	_saindo = true
	som_clique.play()
	var saida := create_tween()
	saida.tween_property(escuro, "color:a", 1.0, segundos_escurecendo)
	saida.tween_callback(Visor.fechar)
