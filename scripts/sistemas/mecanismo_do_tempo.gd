class_name MecanismoDoTempo
extends Interagivel

const COR_TEXTO := Color("f0d9a0")
const COR_APAGADA := Color("4a4038")
const COR_ALVO := Color("7cf09a")
const COR_ERRO := Color("ff4a3a")
const COR_METAL := Color("b8b0a0")
const SEGUNDOS_CLARAO := 0.35

@export var id: String = ""
@export var titulo: String = ""
@export var instrucao: String = "E: travar no tempo certo"
@export var acertos_para_alinhar: int = 3
@export var segundos_de_castigo: float = 5.0

var _aberto := false
var _travado := false
var _acertos := 0
var _tempo := 0.0
var _clarao := 0.0
var _cor_clarao := COR_ALVO
var _gabriel: Gabriel

@onready var tela: CanvasLayer = $Tela
@onready var desenho: Control = $Tela/Painel/Desenho
@onready var rotulo_titulo: Label = $Tela/Painel/Titulo
@onready var visor: Label = $Tela/Painel/Visor
@onready var dica: Label = $Tela/Dica
@onready var som_acerto: AudioStreamPlayer = $Tela/SomAcerto
@onready var som_erro: AudioStreamPlayer = $Tela/SomErro


func _ready() -> void:
	super()
	tela.visible = false
	rotulo_titulo.text = titulo
	desenho.draw.connect(_ao_desenhar)


func pode_interagir() -> bool:
	return not _aberto


func interagir() -> void:
	if RelogioDoCorredor.foi_vencido():
		Inventario.aviso.emit("Parado. Já bate no tempo certo.")
	elif RelogioDoCorredor.ja_alinhado(id):
		Inventario.aviso.emit("Este já está alinhado. Faltam os outros.")
	elif RelogioDoCorredor.esta_correndo():
		_abrir()


func _abrir() -> void:
	_aberto = true
	_travado = false
	_acertos = 0
	_tempo = 0.0
	_clarao = 0.0
	tela.visible = true
	dica.text = instrucao + "     Esc: sair"
	_gabriel = get_tree().get_first_node_in_group("jogador") as Gabriel
	if _gabriel:
		_gabriel.jogador_controla = false
	_preparar()
	_mostrar_visor()


func _fechar() -> void:
	_aberto = false
	tela.visible = false
	if _gabriel and is_instance_valid(_gabriel):
		_gabriel.jogador_controla = true


func _process(delta: float) -> void:
	if not _aberto:
		return
	if not RelogioDoCorredor.esta_correndo():
		_fechar()
		return
	_tempo += delta
	_clarao = maxf(_clarao - delta, 0.0)
	if not _travado:
		_avancar(delta)
	desenho.queue_redraw()


func _unhandled_input(evento: InputEvent) -> void:
	if not _aberto or not (evento is InputEventKey or evento is InputEventJoypadButton):
		return
	if evento.is_action_pressed("ui_cancel"):
		_fechar()
	elif not _travado and (evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept")):
		_tentar()
	get_viewport().set_input_as_handled()


func _tentar() -> void:
	if _acertou():
		_acertos += 1
		_piscar(COR_ALVO)
		som_acerto.play()
		if _acertos >= acertos_para_alinhar:
			_alinhar()
			return
		_ao_acertar()
	else:
		_acertos = 0
		_piscar(COR_ERRO)
		som_erro.play()
		_relogio().penalizar(segundos_de_castigo)
		_ao_errar()
	_mostrar_visor()


func _alinhar() -> void:
	_travado = true
	visor.text = "ALINHADO"
	visor.add_theme_color_override("font_color", COR_ALVO)
	await get_tree().create_timer(0.7).timeout
	_fechar()
	_relogio().alinhar(id)


func _piscar(cor: Color) -> void:
	_cor_clarao = cor
	_clarao = SEGUNDOS_CLARAO


func _mostrar_visor() -> void:
	visor.text = "ACERTOS %d/%d" % [_acertos, acertos_para_alinhar]
	visor.add_theme_color_override("font_color", COR_TEXTO)


func _relogio() -> RelogioDoCorredor:
	return get_tree().get_first_node_in_group(RelogioDoCorredor.GRUPO) as RelogioDoCorredor


func _ao_desenhar() -> void:
	if _clarao > 0.0:
		var cor := _cor_clarao
		cor.a = 0.35 * _clarao / SEGUNDOS_CLARAO
		desenho.draw_rect(Rect2(Vector2.ZERO, desenho.size), cor)
	_desenhar(desenho.size / 2.0)


func _preparar() -> void:
	pass


func _avancar(_delta: float) -> void:
	pass


func _acertou() -> bool:
	return false


func _ao_acertar() -> void:
	pass


func _ao_errar() -> void:
	pass


func _desenhar(_centro: Vector2) -> void:
	pass


func _diferenca_angular(a: float, b: float) -> float:
	return absf(angle_difference(a, b))


func _desenhar_anel(centro: Vector2, raio: float, cor: Color, grossura: float = 1.0) -> void:
	desenho.draw_arc(centro, raio, 0.0, TAU, 48, cor, grossura)


func _desenhar_faixa(centro: Vector2, raio: float, angulo: float, largura: float, cor: Color, grossura: float) -> void:
	desenho.draw_arc(centro, raio, angulo - largura / 2.0, angulo + largura / 2.0, 16, cor, grossura)
