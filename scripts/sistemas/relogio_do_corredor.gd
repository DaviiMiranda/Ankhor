class_name RelogioDoCorredor
extends CanvasLayer

signal comecou
signal vencido

const GRUPO := "relogio_do_corredor"
const MARCA_VENCIDO := "corredor_tempo_vencido"
const MECANISMOS := 4
const COR_CALMA := Color("f0d9a0")
const COR_CRITICA := Color("ff4a3a")

static var _restante := -1.0
static var _alinhados := {}

@export var segundos_totais: float = 120.0
@export var segundos_criticos: float = 15.0
@export var intervalo_tique_calmo: float = 1.0
@export var intervalo_tique_final: float = 0.22
@export var expoente_pressao: float = 1.6

var _ate_proximo_tique := 0.0
var _taque := false
var _esgotou := false

@onready var mostrador: Label = $Mostrador
@onready var contagem: Label = $Contagem
@onready var desconto: Label = $Desconto
@onready var som_tique: AudioStreamPlayer = $SomTique
@onready var som_trava: AudioStreamPlayer = $SomTrava
@onready var som_alinhado: AudioStreamPlayer = $SomAlinhado
@onready var som_vencido: AudioStreamPlayer = $SomVencido


static func esta_correndo() -> bool:
	return _restante >= 0.0


static func ja_alinhado(id: String) -> bool:
	return _alinhados.has(id)


static func foi_vencido() -> bool:
	return Progresso.tem(MARCA_VENCIDO)


func _ready() -> void:
	add_to_group(GRUPO)
	Vida.morreu.connect(_ao_morrer)
	desconto.visible = false
	_mostrar()


func comecar() -> void:
	if esta_correndo() or foi_vencido():
		return
	_restante = segundos_totais
	_alinhados.clear()
	_ate_proximo_tique = 0.0
	som_trava.play()
	comecou.emit()
	_mostrar()


func alinhar(id: String) -> void:
	if not esta_correndo() or _alinhados.has(id):
		return
	_alinhados[id] = true
	if _alinhados.size() >= MECANISMOS:
		_vencer()
	else:
		som_alinhado.play()
		Inventario.aviso.emit("%d de %d alinhados." % [_alinhados.size(), MECANISMOS])
	_mostrar()


func penalizar(segundos: float) -> void:
	if not esta_correndo():
		return
	_restante = maxf(_restante - segundos, 0.0)
	desconto.text = "-%d s" % roundi(segundos)
	desconto.visible = true
	desconto.modulate.a = 1.0
	var animacao := create_tween()
	animacao.tween_property(desconto, "modulate:a", 0.0, 0.9).set_delay(0.3)
	animacao.tween_callback(desconto.hide)
	_mostrar()


func _process(delta: float) -> void:
	if not esta_correndo() or _esgotou:
		return
	_restante = maxf(_restante - delta, 0.0)
	_aplicar_pressao(pow(_fracao_passada(), expoente_pressao))
	_tiquetaquear(delta)
	_mostrar()
	if _restante <= 0.0:
		_esgotar()


func _fracao_passada() -> float:
	return clampf(1.0 - _restante / segundos_totais, 0.0, 1.0)


func _tiquetaquear(delta: float) -> void:
	_ate_proximo_tique -= delta
	if _ate_proximo_tique > 0.0:
		return
	_ate_proximo_tique = lerpf(intervalo_tique_calmo, intervalo_tique_final, pow(_fracao_passada(), 1.3))
	_taque = not _taque
	som_tique.pitch_scale = 0.82 if _taque else 1.0
	som_tique.play()


func _esgotar() -> void:
	var gabriel := _gabriel()
	var origem := gabriel.global_position if gabriel else Vector2.ZERO
	if Vida.receber_dano(Vida.MAXIMA, origem):
		_esgotou = true


func _vencer() -> void:
	_restante = -1.0
	_alinhados.clear()
	Progresso.marcar(MARCA_VENCIDO)
	_aplicar_pressao(0.0)
	som_vencido.play()
	Inventario.aviso.emit("Os quatro tempos bateram juntos. O relógio parou e a porta do corredor destravou.")
	vencido.emit()


func _ao_morrer() -> void:
	_restante = -1.0
	_alinhados.clear()
	_aplicar_pressao(0.0)


func _aplicar_pressao(valor: float) -> void:
	var gabriel := _gabriel()
	if gabriel and gabriel.ansiedade:
		gabriel.ansiedade.definir_pressao(valor)


func _gabriel() -> Gabriel:
	return get_tree().get_first_node_in_group("jogador") as Gabriel


func _mostrar() -> void:
	var correndo := esta_correndo()
	mostrador.visible = correndo
	contagem.visible = correndo
	if not correndo:
		return
	var critico := _restante < segundos_criticos
	if critico:
		mostrador.text = "%.1f" % _restante
	else:
		var segundos := ceili(_restante)
		mostrador.text = "%d:%02d" % [floori(segundos / 60.0), segundos % 60]
	var piscando := critico and int(_restante * 4.0) % 2 == 0
	mostrador.add_theme_color_override("font_color", COR_CRITICA if critico else COR_CALMA.lerp(COR_CRITICA, _fracao_passada()))
	mostrador.modulate.a = 0.55 if piscando else 1.0
	contagem.text = "ALINHADOS %d/%d" % [_alinhados.size(), MECANISMOS]
