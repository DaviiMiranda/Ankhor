extends Node2D

const ALCANCE_RESPIRACAO := 6
const INTERVALO_RESPIRACAO := 2.0

@export var segundos_por_filtro: float = 45.0

var item: Item
var _estado: Dictionary
var _proxima_respiracao := 0.0

@onready var respiracao: AudioStreamPlayer = $Respiracao


func _ready() -> void:
	_estado = Inventario.estado_de(item.id if item else "mascara_gas")
	_estado["aceso"] = false
	if not _estado.has("segundos_do_filtro"):
		_estado["segundos_do_filtro"] = segundos_por_filtro


func usar() -> void:
	if _estado["aceso"]:
		_estado["aceso"] = false
		return
	if Inventario.unidades(item.id) <= 0:
		Inventario.aviso.emit("Sem filtro para a máscara")
		return
	_estado["aceso"] = true
	_proxima_respiracao = 0.0


func ao_desequipar() -> void:
	_estado["aceso"] = false


func _physics_process(delta: float) -> void:
	if not _estado["aceso"]:
		return
	_estado["segundos_do_filtro"] -= delta
	if _estado["segundos_do_filtro"] <= 0.0:
		_trocar_filtro()
		if not _estado["aceso"]:
			return
	_proxima_respiracao -= delta
	if _proxima_respiracao <= 0.0:
		_proxima_respiracao = INTERVALO_RESPIRACAO
		respiracao.play()
		var dono := get_parent().get_parent() as Node2D
		Robo.fazer_barulho(get_tree(), dono.global_position, ALCANCE_RESPIRACAO)


func _trocar_filtro() -> void:
	var restantes := Inventario.unidades(item.id) - 1
	Inventario.definir_unidades(item, maxi(restantes, 0))
	_estado["segundos_do_filtro"] = segundos_por_filtro
	if restantes <= 0:
		_estado["aceso"] = false
		Inventario.aviso.emit("O último filtro acabou")
	else:
		Inventario.aviso.emit("Filtro trocado. Restam %d" % restantes)
