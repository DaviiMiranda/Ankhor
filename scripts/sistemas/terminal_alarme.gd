class_name TerminalAlarme
extends Interagivel

@export var marca: String = "alarme_104"
@export_multiline var aviso: String = ""
@export var segundos_som: float = 4.0

@onready var som: AudioStreamPlayer = $Som


func interagir() -> void:
	Sirene.disparada = true
	Progresso.marcar(marca)
	Inventario.aviso.emit(aviso)
	som.play()
	get_tree().create_timer(segundos_som).timeout.connect(som.stop)
