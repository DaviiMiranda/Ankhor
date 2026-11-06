extends SalaDoZane

const MARCAS_DAS_TRAVAS: Array[String] = [
	"escritorio_trava_arquivo",
	"escritorio_trava_reunioes",
	"escritorio_trava_seguranca",
]
const MARCA_TRES_TRAVAS := "escritorio_tres_travas"

@onready var lampadas: Node2D = $Travas


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	_acender_lampadas()


func _acender_lampadas() -> void:
	var soltas := 0
	for i in MARCAS_DAS_TRAVAS.size():
		var solta := Progresso.tem(MARCAS_DAS_TRAVAS[i])
		(lampadas.get_child(i) as CanvasItem).visible = solta
		if solta:
			soltas += 1
	if soltas == MARCAS_DAS_TRAVAS.size():
		Progresso.marcar(MARCA_TRES_TRAVAS)
