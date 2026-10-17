class_name PainelComutacao
extends Interagivel

const CORES := [
	Color("3a3f48"),
	Color("4da6ff"),
	Color("f0d148"),
	Color("ff5c5c")
]
const NOMES_FASES := ["DESL", "FASE A", "FASE B", "FASE C"]
const NOMES_SETORES := ["NORTE", "LESTE", "SUL", "OESTE"]
const ARESTAS := [
	[0, 1],
	[1, 2],
	[2, 3],
	[3, 0],
	[0, 2]
]
const COR_ESCOLHIDO := Color("f0d148")
const COR_TEXTO := Color("d8dee6")
const COR_OK := Color("7cf09a")
const COR_CONFLITO := Color("ff5c5c")

@export var item_requerido: String = "celula_energia"
@export var marca: String = "convivencia_energia"
@export var aviso_sem_item: String = "Comutador sem carga primária. Falta a Célula de Energia de Alta Densidade."
@export var aviso_ligado: String = "Comutador armado! A energia foi enviada para o elevador de carga."
@export var aviso_ja_ligado: String = "O comutador já está armado e alimentando o elevador de carga."

var _aberto := false
var _cursor := 0
var _fases: Array[int] = [1, 1, 2, 1]
var _caixas: Array[ColorRect] = []
var _rotulos_setor: Array[Label] = []
var _rotulos_fase: Array[Label] = []

@onready var tela: CanvasLayer = $Tela
@onready var fila: HBoxContainer = $Tela/Painel/Setores
@onready var status_arestas: Label = $Tela/Painel/StatusArestas
@onready var dica: Label = $Tela/Dica
@onready var som_clique: AudioStreamPlayer = $Tela/SomClique
@onready var som_desarme: AudioStreamPlayer = $Tela/SomDesarme


func _ready() -> void:
	super()
	process_mode = Node.PROCESS_MODE_ALWAYS
	tela.visible = false
	_montar_setores()


func pode_interagir() -> bool:
	return not _aberto


func interagir() -> void:
	if Progresso.tem(marca):
		Inventario.aviso.emit(aviso_ja_ligado)
		return
	if not item_requerido.is_empty() and not Inventario.tem(item_requerido):
		Inventario.aviso.emit(aviso_sem_item)
		som_desarme.play()
		return
	_abrir()


func _montar_setores() -> void:
	for i in NOMES_SETORES.size():
		var coluna := VBoxContainer.new()
		coluna.alignment = BoxContainer.ALIGNMENT_CENTER
		var setor := Label.new()
		setor.text = NOMES_SETORES[i]
		setor.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		var caixa := ColorRect.new()
		caixa.custom_minimum_size = Vector2(28, 22)
		var fase := Label.new()
		fase.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		coluna.add_child(setor)
		coluna.add_child(caixa)
		coluna.add_child(fase)
		fila.add_child(coluna)
		_rotulos_setor.append(setor)
		_caixas.append(caixa)
		_rotulos_fase.append(fase)


func _abrir() -> void:
	_aberto = true
	tela.visible = true
	get_tree().paused = true
	_cursor = 0
	dica.text = "Setas: escolher setor     E: trocar fase     Esc: fechar"
	_mostrar()


func _fechar() -> void:
	_aberto = false
	tela.visible = false
	get_tree().paused = false


func _unhandled_input(evento: InputEvent) -> void:
	if not _aberto:
		return
	if evento.is_action_pressed("ui_cancel"):
		_fechar()
	elif evento.is_action_pressed("mover_esquerda") or evento.is_action_pressed("ui_left"):
		_cursor = posmod(_cursor - 1, NOMES_SETORES.size())
		_mostrar()
	elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
		_cursor = posmod(_cursor + 1, NOMES_SETORES.size())
		_mostrar()
	elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		_trocar_fase(_cursor)
	get_viewport().set_input_as_handled()


func _trocar_fase(indice: int) -> void:
	som_clique.play()
	_fases[indice] = (_fases[indice] % 3) + 1
	_mostrar()
	if _sem_conflitos():
		_concluir()


func _sem_conflitos() -> bool:
	for f in _fases:
		if f <= 0:
			return false
	for par in ARESTAS:
		if _fases[par[0]] == _fases[par[1]]:
			return false
	return true


func _conflitos_atuais() -> Array[String]:
	var lista: Array[String] = []
	for par in ARESTAS:
		var a: int = par[0]
		var b: int = par[1]
		if _fases[a] > 0 and _fases[a] == _fases[b]:
			lista.append("%s-%s" % [NOMES_SETORES[a][0], NOMES_SETORES[b][0]])
	return lista


func _concluir() -> void:
	dica.text = "Fases sincronizadas sem ressonância!"
	Progresso.marcar(marca)
	await get_tree().create_timer(0.9, true).timeout
	_fechar()
	Inventario.aviso.emit(aviso_ligado)


func _mostrar() -> void:
	for i in _caixas.size():
		_caixas[i].color = CORES[_fases[i]]
		_rotulos_fase[i].text = NOMES_FASES[_fases[i]]
		_rotulos_setor[i].add_theme_color_override("font_color", COR_ESCOLHIDO if i == _cursor else COR_TEXTO)
		_rotulos_fase[i].add_theme_color_override("font_color", COR_ESCOLHIDO if i == _cursor else COR_TEXTO)
	var conflitos := _conflitos_atuais()
	if conflitos.is_empty():
		status_arestas.text = "Ligações (N-L, L-S, S-O, O-N, N-S): OK"
		status_arestas.add_theme_color_override("font_color", COR_OK)
	else:
		status_arestas.text = "Conflito de fase em: " + ", ".join(conflitos)
		status_arestas.add_theme_color_override("font_color", COR_CONFLITO)
