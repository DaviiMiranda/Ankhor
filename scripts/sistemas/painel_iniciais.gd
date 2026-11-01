class_name PainelIniciais
extends Interagivel

const COR_INICIAL := Color("f0d148")
const COR_RESTO := Color("8a93a6")
const COR_TEXTO := Color("d8dee6")
const COR_CAIXA := Color("2c3a5c")
const COR_CAIXA_ESCOLHIDA := Color("5c5230")
const COR_CAIXA_USADA := Color("171a24")
const COR_VAGA := Color("10121a")
const COR_CERTO := Color("7cf09a")
const COR_ERRADO := Color("ff5c5c")
const TEMPO_DO_ERRO := 1.0
const TEMPO_DO_ACERTO := 1.4

@export var nome_da_casa: String = "TAPIOCA ORBITAL"
@export var lanches: PackedStringArray = PackedStringArray()
@export var icones: Array[Texture2D] = []
@export var marca: String = "combo_tapioca_montado"
@export var pedido: String = "O COMBO DA CASA TEM O NOME DA CASA"
@export var aviso_vazio: String = "ESCOLHA OS LANCHES"
@export var aviso_errado: String = "ESSE NÃO É O COMBO DA CASA"
@export var aviso_certo: String = "COMBO DA CASA!"
@export var aviso_resolvido: String = "A gaveta da estufa destravou: duas pilhas."
@export var aviso_ja_resolvido: String = "A estufa já serviu o combo da casa."
@export var item_premio: Item
@export var cena_premio: PackedScene
@export var quantidade_premio: int = 1

var _aberto := false
var _conferindo := false
var _cursor := 0
var _palavras: PackedStringArray = PackedStringArray()
var _escolhidos: Array[int] = []
var _caixas_lanche: Array[ColorRect] = []
var _caixas_vaga: Array[ColorRect] = []

@onready var tela: CanvasLayer = $Tela
@onready var rotulo_pedido: Label = $Tela/Painel/Pedido
@onready var nome_e_vagas: HBoxContainer = $Tela/Painel/NomeEVagas
@onready var fila_lanches: HBoxContainer = $Tela/Painel/Lanches
@onready var visor: Label = $Tela/Painel/Visor
@onready var dica: Label = $Tela/Dica
@onready var som_clique: AudioStreamPlayer = $Tela/SomClique
@onready var som_erro: AudioStreamPlayer = $Tela/SomErro
@onready var som_pronto: AudioStreamPlayer = $Tela/SomPronto


func _ready() -> void:
	super()
	process_mode = Node.PROCESS_MODE_ALWAYS
	tela.visible = false
	rotulo_pedido.text = pedido
	_palavras = nome_da_casa.split(" ", false)
	_montar_nome_e_vagas()
	_montar_lanches()
	if Progresso.tem(marca):
		_soltar_premio.call_deferred()


func pode_interagir() -> bool:
	return not _aberto


func interagir() -> void:
	if Progresso.tem(marca):
		Inventario.aviso.emit(aviso_ja_resolvido)
		return
	_abrir()


static func combina(nome: String, escolhas: PackedStringArray) -> bool:
	var palavras := nome.split(" ", false)
	if palavras.size() != escolhas.size():
		return false
	for i in palavras.size():
		if palavras[i].left(1).to_upper() != escolhas[i].left(1).to_upper():
			return false
	return true


func _montar_nome_e_vagas() -> void:
	for palavra in _palavras:
		var coluna := VBoxContainer.new()
		coluna.add_theme_constant_override("separation", 2)
		coluna.add_child(_nova_palavra(palavra))
		var vaga := _nova_caixa(Vector2(84, 44))
		coluna.add_child(vaga)
		nome_e_vagas.add_child(coluna)
		_caixas_vaga.append(vaga)


func _nova_palavra(palavra: String) -> HBoxContainer:
	var linha := HBoxContainer.new()
	linha.alignment = BoxContainer.ALIGNMENT_CENTER
	linha.add_theme_constant_override("separation", 0)
	linha.add_child(_novo_pedaco(palavra.left(1), COR_INICIAL))
	linha.add_child(_novo_pedaco(palavra.substr(1), COR_RESTO))
	return linha


func _novo_pedaco(texto: String, cor: Color) -> Label:
	var pedaco := Label.new()
	pedaco.text = texto
	pedaco.add_theme_font_size_override("font_size", 16)
	pedaco.add_theme_color_override("font_color", cor)
	return pedaco


func _montar_lanches() -> void:
	for i in lanches.size():
		var caixa := _nova_caixa(Vector2(56, 44))
		_preencher(caixa, i)
		fila_lanches.add_child(caixa)
		_caixas_lanche.append(caixa)


func _nova_caixa(tamanho: Vector2) -> ColorRect:
	var caixa := ColorRect.new()
	caixa.custom_minimum_size = tamanho
	var conteudo := VBoxContainer.new()
	conteudo.name = "Conteudo"
	conteudo.alignment = BoxContainer.ALIGNMENT_CENTER
	conteudo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	conteudo.add_theme_constant_override("separation", 0)
	var icone := TextureRect.new()
	icone.name = "Icone"
	icone.stretch_mode = TextureRect.STRETCH_KEEP_CENTERED
	icone.custom_minimum_size = Vector2(24, 24)
	var rotulo := Label.new()
	rotulo.name = "Rotulo"
	rotulo.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	conteudo.add_child(icone)
	conteudo.add_child(rotulo)
	caixa.add_child(conteudo)
	return caixa


func _preencher(caixa: ColorRect, indice: int) -> void:
	var icone := caixa.get_node("Conteudo/Icone") as TextureRect
	var rotulo := caixa.get_node("Conteudo/Rotulo") as Label
	if indice < 0:
		icone.texture = null
		rotulo.text = ""
		return
	icone.texture = icones[indice] if indice < icones.size() else null
	rotulo.text = lanches[indice]


func _abrir() -> void:
	_aberto = true
	tela.visible = true
	get_tree().paused = true
	_cursor = 0
	dica.text = "Lados: escolher o lanche     E: pôr ou tirar     Esc: sair"
	_mostrar()


func _fechar() -> void:
	_aberto = false
	tela.visible = false
	get_tree().paused = false


func _unhandled_input(evento: InputEvent) -> void:
	if not _aberto:
		return
	if not _conferindo:
		if evento.is_action_pressed("ui_cancel"):
			_fechar()
		elif evento.is_action_pressed("mover_esquerda") or evento.is_action_pressed("ui_left"):
			_cursor = posmod(_cursor - 1, lanches.size())
			_mostrar()
		elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
			_cursor = posmod(_cursor + 1, lanches.size())
			_mostrar()
		elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
			_por_ou_tirar()
	get_viewport().set_input_as_handled()


func _por_ou_tirar() -> void:
	var posicao := _escolhidos.find(_cursor)
	if posicao >= 0:
		_escolhidos.remove_at(posicao)
	else:
		_escolhidos.append(_cursor)
	som_clique.play()
	_mostrar()
	if _escolhidos.size() == _palavras.size():
		_conferir()


func _conferir() -> void:
	var escolhas := PackedStringArray()
	for indice in _escolhidos:
		escolhas.append(lanches[indice])
	if combina(nome_da_casa, escolhas):
		_concluir()
	else:
		_recusar()


func _recusar() -> void:
	_conferindo = true
	_escrever_no_visor(aviso_errado, COR_ERRADO)
	som_erro.play()
	await get_tree().create_timer(TEMPO_DO_ERRO, true).timeout
	_escolhidos.clear()
	_conferindo = false
	_mostrar()


func _concluir() -> void:
	_conferindo = true
	_escrever_no_visor(aviso_certo, COR_CERTO)
	som_pronto.play()
	Progresso.marcar(marca)
	_soltar_premio()
	await get_tree().create_timer(TEMPO_DO_ACERTO, true).timeout
	_conferindo = false
	_fechar()
	Inventario.aviso.emit(aviso_resolvido)


func _escrever_no_visor(texto: String, cor: Color) -> void:
	visor.text = texto
	visor.add_theme_color_override("font_color", cor)


func _mostrar() -> void:
	_escrever_no_visor(aviso_vazio, COR_TEXTO)
	for i in _caixas_vaga.size():
		_caixas_vaga[i].color = COR_VAGA
		_preencher(_caixas_vaga[i], _escolhidos[i] if i < _escolhidos.size() else -1)
	for i in _caixas_lanche.size():
		_caixas_lanche[i].color = _cor_da_caixa(i)
		var rotulo := _caixas_lanche[i].get_node("Conteudo/Rotulo") as Label
		rotulo.add_theme_color_override("font_color", COR_INICIAL if i == _cursor else COR_TEXTO)


func _cor_da_caixa(indice: int) -> Color:
	if indice == _cursor:
		return COR_CAIXA_ESCOLHIDA
	return COR_CAIXA_USADA if _escolhidos.has(indice) else COR_CAIXA


func _soltar_premio() -> void:
	Recompensa.soltar(self, item_premio, cena_premio, quantidade_premio)
