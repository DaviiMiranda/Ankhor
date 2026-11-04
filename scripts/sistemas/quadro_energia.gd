class_name QuadroEnergia
extends Interagivel

const COR_LIGADO := Color("7cf09a")
const COR_DESLIGADO := Color("3a3f48")
const COR_ESCOLHIDO := Color("f0d148")
const COR_TEXTO := Color("d8dee6")

@export var ordem: PackedInt32Array = PackedInt32Array([3, 1, 4, 2])
@export var marca: String = "energia"
@export var aviso_ligado: String = "A energia voltou. Lá fora, algo zumbiu e acendeu."
@export var aviso_ja_ligado: String = "Os disjuntores estão ligados."
@export var titulo: String = ""
@export var nomes: PackedStringArray = PackedStringArray()
@export var ruido_ao_desarmar: int = 0
@export var item_premio: Item
@export var cena_premio: PackedScene
@export var quantidade_premio: int = 1

@export var pausa_o_jogo := true

var _aberto := false
var _ligados: Array[int] = []
var _cursor := 0
var _alavancas: Array[ColorRect] = []
var _numeros: Array[Label] = []

@onready var tela: CanvasLayer = $Tela
@onready var painel: ColorRect = $Tela/Painel
@onready var fila: HBoxContainer = $Tela/Painel/Alavancas
@onready var rotulo_titulo: Label = $Tela/Painel/Titulo
@onready var dica: Label = $Tela/Dica
@onready var som_clique: AudioStreamPlayer = $Tela/SomClique
@onready var som_desarme: AudioStreamPlayer = $Tela/SomDesarme


func _ready() -> void:
	super()
	process_mode = Node.PROCESS_MODE_ALWAYS
	tela.visible = false
	if not titulo.is_empty():
		rotulo_titulo.text = titulo
	if not nomes.is_empty():
		_alargar_painel()
	_montar_alavancas()
	if Progresso.tem(marca):
		_soltar_premio.call_deferred()


func pode_interagir() -> bool:
	return not _aberto


func interagir() -> void:
	if Progresso.tem(marca):
		Inventario.aviso.emit(aviso_ja_ligado)
		return
	_abrir()


func _montar_alavancas() -> void:
	for i in ordem.size():
		var coluna := VBoxContainer.new()
		coluna.alignment = BoxContainer.ALIGNMENT_CENTER
		var alavanca := ColorRect.new()
		alavanca.custom_minimum_size = Vector2(12, 30)
		var numero := Label.new()
		numero.text = str(i + 1) if nomes.is_empty() else "%d\n%s" % [i + 1, nomes[i]]
		numero.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		coluna.add_child(alavanca)
		coluna.add_child(numero)
		fila.add_child(coluna)
		_alavancas.append(alavanca)
		_numeros.append(numero)


func _abrir() -> void:
	_aberto = true
	tela.visible = true
	_travar_o_jogo()
	_cursor = 0
	dica.text = "Setas: escolher     E: ligar     Esc: fechar"
	_mostrar()


func _fechar() -> void:
	_aberto = false
	tela.visible = false
	_soltar_o_jogo()


func _travar_o_jogo() -> void:
	if pausa_o_jogo:
		get_tree().paused = true
		return
	Hackeamento.tela_em_tempo_real = true
	(get_tree().get_first_node_in_group("jogador") as Gabriel).andar_sozinho(Vector2.ZERO)
	Vida.dano_recebido.connect(_ao_receber_dano_aberto, CONNECT_ONE_SHOT)


func _soltar_o_jogo() -> void:
	if pausa_o_jogo:
		get_tree().paused = false
		return
	Hackeamento.tela_em_tempo_real = false
	if Vida.dano_recebido.is_connected(_ao_receber_dano_aberto):
		Vida.dano_recebido.disconnect(_ao_receber_dano_aberto)
	(get_tree().get_first_node_in_group("jogador") as Gabriel).devolver_controle()


func _ao_receber_dano_aberto(_origem: Vector2) -> void:
	if _aberto:
		_fechar()


func _unhandled_input(evento: InputEvent) -> void:
	if not _aberto:
		return
	if evento.is_action_pressed("ui_cancel"):
		_fechar()
	elif evento.is_action_pressed("mover_esquerda") or evento.is_action_pressed("ui_left"):
		_cursor = posmod(_cursor - 1, ordem.size())
		_mostrar()
	elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
		_cursor = posmod(_cursor + 1, ordem.size())
		_mostrar()
	elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		_ligar(_cursor)
	get_viewport().set_input_as_handled()


func _ligar(indice: int) -> void:
	if _ligados.has(indice):
		return
	som_clique.play()
	if indice + 1 != ordem[_ligados.size()]:
		_ligados.clear()
		som_desarme.play()
		_fazer_barulho()
		dica.text = "Desarmou! Todos os disjuntores caíram."
		_mostrar()
		return
	_ligados.append(indice)
	_mostrar()
	if _ligados.size() == ordem.size():
		_concluir()


func _concluir() -> void:
	dica.text = "Energia restabelecida."
	Progresso.marcar(marca)
	_soltar_premio()
	await get_tree().create_timer(0.8, true).timeout
	_fechar()
	Inventario.aviso.emit(aviso_ligado)


func _mostrar() -> void:
	for i in _alavancas.size():
		_alavancas[i].color = COR_LIGADO if _ligados.has(i) else COR_DESLIGADO
		_numeros[i].add_theme_color_override("font_color", COR_ESCOLHIDO if i == _cursor else COR_TEXTO)


func _alargar_painel() -> void:
	painel.offset_left = 60.0
	painel.offset_right = 260.0
	rotulo_titulo.offset_right = 200.0
	fila.offset_left = 8.0
	fila.offset_right = 192.0
	fila.add_theme_constant_override("separation", 6)


func _fazer_barulho() -> void:
	if ruido_ao_desarmar <= 0:
		return
	for no in get_tree().get_nodes_in_group("robos"):
		(no as Robo).ouvir_barulho(global_position, ruido_ao_desarmar)


func _soltar_premio() -> void:
	Recompensa.soltar(self, item_premio, cena_premio, quantidade_premio)
