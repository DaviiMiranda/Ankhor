class_name GradeComColisao
extends GradeSeguranca

@onready var forma: CollisionShape2D = $Corpo/Forma


func _ready() -> void:
	super()
	forma.set_deferred("disabled", Progresso.tem(marca))


func _ao_mudar(nova: String) -> void:
	super(nova)
	if nova == marca:
		forma.set_deferred("disabled", true)
