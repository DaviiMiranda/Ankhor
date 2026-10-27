class_name FarolDaMesa
extends RecompensaDoQuarto

@export var periodo_pulso: float = 3.2
@export var energia_minima: float = 0.45
@export var energia_maxima: float = 0.85

var _tempo := 0.0

@onready var luz: OmniLight3D = $Luz


func _process(delta: float) -> void:
	super(delta)
	_tempo += delta
	var onda := (1.0 - cos(_tempo * TAU / periodo_pulso)) / 2.0
	luz.light_energy = lerpf(energia_minima, energia_maxima, onda)
