extends Sala

const AVISO_INICIO := "A porta trancou atrás de você. Quatro salas, quatro mecanismos: alinhe todos antes que o relógio zere."

@onready var relogio: RelogioDoCorredor = $RelogioDoCorredor
@onready var porta_saida: Porta = $PortaSaida
@onready var bilhete: Node2D = $Objetos/Bilhete


func _ready() -> void:
	super()
	if Engine.is_editor_hint():
		return
	relogio.comecou.connect(_ao_comecar)
	relogio.vencido.connect(_trancar_saida)
	if not RelogioDoCorredor.foi_vencido():
		bilhete.queue_free()
	_trancar_saida()
	if not RelogioDoCorredor.esta_correndo() and not RelogioDoCorredor.foi_vencido():
		await get_tree().create_timer(duracao_entrada).timeout
		relogio.comecar()


func _ao_comecar() -> void:
	_trancar_saida()
	Inventario.aviso.emit(AVISO_INICIO)


func _trancar_saida() -> void:
	porta_saida.bloqueada = RelogioDoCorredor.esta_correndo()
