extends CanvasLayer

enum Aba { ITENS, CRIACAO, ANOTACOES, OBJETIVO }

const CENA_ESPACO := preload("res://cenas/interface/espaco_item.tscn")
const COR_ABA_ATIVA := Color(0.95, 0.88, 0.7, 1)
const COR_ABA_INATIVA := Color(0.55, 0.56, 0.52, 1)
const MARCA_NOVA := " •"
const DICAS := {
	Aba.ITENS: "Q: próxima aba   Setas: escolher   1-3: equipar   Tab: fechar",
	Aba.CRIACAO: "Q: próxima aba   E: criar   Tab: fechar",
	Aba.ANOTACOES: "Q: próxima aba   Setas: escolher e folhear   Tab: fechar",
	Aba.OBJETIVO: "Q: próxima aba   Tab: fechar",
}
const SEGUNDOS_ABRINDO_MOCHILA := 1.0
const SEGUNDOS_FECHANDO_MOCHILA := 0.6
const SEGUNDOS_FADE_JANELA := 0.1
const SEGUNDOS_FADE_TEXTO := 0.12
const QUADRO_FINAL_DO_GESTO := GestoMochila.QUADROS - 0.01

var aberto := false
var _aba := Aba.ITENS
var _cursor := Vector2i(0, 0)
var _espacos_grade: Array[EspacoItem] = []
var _espacos_gadget: Array[EspacoItem] = []
var _em_transicao := false
var _gabriel_no_gesto: Gabriel
var _fade_textos: Tween

@onready var fundo: ColorRect = $Fundo
@onready var janela: Control = $Janela
@onready var aba_itens: Label = $Janela/Abas/AbaItens
@onready var aba_criacao: Label = $Janela/Abas/AbaCriacao
@onready var aba_anotacoes: Label = $Janela/Abas/AbaAnotacoes
@onready var aba_objetivo: Label = $Janela/Abas/AbaObjetivo
@onready var marcador: ColorRect = $Janela/Marcador
@onready var painel_itens: Control = $Janela/Itens
@onready var painel_criacao: PainelCriacao = $Janela/Criacao
@onready var painel_anotacoes: PainelAnotacoes = $Janela/Anotacoes
@onready var painel_objetivo: PainelObjetivo = $Janela/Objetivo
@onready var dica: Label = $Janela/Dica
@onready var grade: GridContainer = $Janela/Itens/Grade
@onready var caixa_gadgets: HBoxContainer = $Janela/Itens/Gadgets
@onready var nome: Label = $Janela/Itens/Nome
@onready var descricao: Label = $Janela/Itens/Descricao
@onready var situacao: Label = $Janela/Itens/Situacao
@onready var dica_examinar: Label = $Janela/Itens/Examinar
@onready var som_abrir: AudioStreamPlayer = $SomAbrir
@onready var som_fechar: AudioStreamPlayer = $SomFechar
@onready var som_aba: AudioStreamPlayer = $SomAba
@onready var som_equipar: AudioStreamPlayer = $SomEquipar
@onready var som_desequipar: AudioStreamPlayer = $SomDesequipar


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_criar_espacos()
	aba_itens.gui_input.connect(_ao_clicar_aba.bind(Aba.ITENS))
	aba_criacao.gui_input.connect(_ao_clicar_aba.bind(Aba.CRIACAO))
	aba_anotacoes.gui_input.connect(_ao_clicar_aba.bind(Aba.ANOTACOES))
	aba_objetivo.gui_input.connect(_ao_clicar_aba.bind(Aba.OBJETIVO))
	Inventario.mudou.connect(_atualizar)
	Caderno.mudou.connect(_atualizar_abas)
	visible = false


func _criar_espacos() -> void:
	grade.columns = Inventario.COLUNAS
	for linha in Inventario.LINHAS:
		for coluna in Inventario.COLUNAS:
			var espaco := CENA_ESPACO.instantiate() as EspacoItem
			grade.add_child(espaco)
			espaco.clicado.connect(_escolher.bind(Vector2i(coluna, linha)))
			_espacos_grade.append(espaco)
	for i in Inventario.ESPACOS_GADGET:
		var espaco := CENA_ESPACO.instantiate() as EspacoItem
		caixa_gadgets.add_child(espaco)
		espaco.clicado.connect(_equipar_no_espaco.bind(i))
		_espacos_gadget.append(espaco)


func _unhandled_input(evento: InputEvent) -> void:
	if ItemNovo.aberto:
		return
	if _em_transicao:
		get_viewport().set_input_as_handled()
		return
	if evento.is_action_pressed("inventario"):
		_tratar_atalho(Aba.ITENS)
		return
	if evento.is_action_pressed("caderno"):
		_tratar_atalho(Aba.ANOTACOES)
		return
	if not aberto:
		return
	if evento.is_action_pressed("ui_cancel"):
		_abrir(false)
	elif evento.is_action_pressed("trocar_aba"):
		_mostrar_aba(((_aba + 1) % Aba.size()) as Aba)
		som_aba.play()
	elif _aba == Aba.ITENS:
		_tratar_itens(evento)
	elif _aba == Aba.CRIACAO:
		_tratar_criacao(evento)
	elif _aba == Aba.ANOTACOES:
		painel_anotacoes.tratar_entrada(evento)
	get_viewport().set_input_as_handled()


func _tratar_atalho(aba: Aba) -> void:
	if not aberto and (get_tree().paused or Hackeamento.tela_em_tempo_real):
		return
	_alternar(aba)
	get_viewport().set_input_as_handled()


func _alternar(aba: Aba) -> void:
	if not aberto:
		_abrir(true)
		_mostrar_aba(aba)
		if aba == Aba.ANOTACOES:
			painel_anotacoes.mostrar_mais_recente()
	elif aba == _aba or aba == Aba.ITENS:
		_abrir(false)
	else:
		_mostrar_aba(aba)
		som_aba.play()


func _tratar_itens(evento: InputEvent) -> void:
	var passo := Vector2i.ZERO
	if evento.is_action_pressed("mover_esquerda") or evento.is_action_pressed("ui_left"):
		passo = Vector2i.LEFT
	elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
		passo = Vector2i.RIGHT
	elif evento.is_action_pressed("mover_cima") or evento.is_action_pressed("ui_up"):
		passo = Vector2i.UP
	elif evento.is_action_pressed("mover_baixo") or evento.is_action_pressed("ui_down"):
		passo = Vector2i.DOWN
	if passo != Vector2i.ZERO:
		_escolher(Vector2i(posmod(_cursor.x + passo.x, Inventario.COLUNAS),
				posmod(_cursor.y + passo.y, Inventario.LINHAS)))
	for i in Inventario.ESPACOS_GADGET:
		if evento.is_action_pressed("gadget_%d" % (i + 1)):
			_equipar_no_espaco(i)
	if evento.is_action_pressed("interagir"):
		_examinar()


func _tratar_criacao(evento: InputEvent) -> void:
	if evento.is_action_pressed("interagir") and Criacao.criar_bala():
		som_equipar.play()
		Inventario.aviso.emit("Bala de impulso criada")


func _examinar() -> void:
	var item := Inventario.item_em(_cursor.y, _cursor.x)
	if item:
		ItemNovo.examinar(item)


func _abrir(abrir: bool) -> void:
	aberto = abrir
	_em_transicao = true
	_atualizar()
	if abrir:
		await _entrar()
	else:
		await _sair()
	_em_transicao = false


func _entrar() -> void:
	get_tree().paused = true
	som_fechar.stop()
	fundo.modulate.a = 0.0
	janela.modulate.a = 0.0
	visible = true
	_gabriel_no_gesto = _gabriel_livre()
	var segundos := 0.0
	var animacao := create_tween().set_parallel()
	if _gabriel_no_gesto:
		segundos = SEGUNDOS_ABRINDO_MOCHILA
		_gabriel_no_gesto.comecar_gesto_da_mochila()
		animacao.tween_method(_mostrar_quadro_do_gesto, 0.0, QUADRO_FINAL_DO_GESTO, segundos)
	animacao.tween_callback(som_abrir.play).set_delay(maxf(segundos - som_abrir.stream.get_length(), 0.0))
	animacao.tween_property(fundo, "modulate:a", 1.0, SEGUNDOS_FADE_JANELA).set_delay(segundos)
	animacao.tween_property(janela, "modulate:a", 1.0, SEGUNDOS_FADE_JANELA).set_delay(segundos)
	await animacao.finished


func _sair() -> void:
	som_abrir.stop()
	som_fechar.play()
	var segundos := SEGUNDOS_FECHANDO_MOCHILA if _gabriel_no_gesto else 0.0
	var animacao := create_tween().set_parallel()
	animacao.tween_property(janela, "modulate:a", 0.0, SEGUNDOS_FADE_JANELA)
	animacao.tween_property(fundo, "modulate:a", 0.0, SEGUNDOS_FADE_JANELA)
	if _gabriel_no_gesto:
		animacao.tween_method(_mostrar_quadro_do_gesto, QUADRO_FINAL_DO_GESTO, 0.0, segundos).set_delay(SEGUNDOS_FADE_JANELA)
	await animacao.finished
	visible = false
	if _gabriel_no_gesto:
		_gabriel_no_gesto.terminar_tira()
		_gabriel_no_gesto = null
	get_tree().paused = false


func _gabriel_livre() -> Gabriel:
	var gabriel := get_tree().get_first_node_in_group("jogador") as Gabriel
	return gabriel if gabriel and gabriel.pode_mexer_na_mochila() else null


func _mostrar_quadro_do_gesto(quadro: float) -> void:
	_gabriel_no_gesto.mostrar_quadro_tira(int(quadro))


func _mostrar_aba(aba: Aba) -> void:
	_aba = aba
	painel_itens.visible = aba == Aba.ITENS
	painel_criacao.visible = aba == Aba.CRIACAO
	painel_anotacoes.visible = aba == Aba.ANOTACOES
	painel_objetivo.visible = aba == Aba.OBJETIVO
	painel_objetivo.atualizar()
	painel_criacao.atualizar()
	dica.text = DICAS[aba]
	_atualizar_abas()


func _atualizar_abas() -> void:
	if not is_node_ready():
		return
	aba_anotacoes.text = "ANOTAÇÕES" + (MARCA_NOVA if Caderno.tem_nao_lidas() else "")
	for aba in Aba.values():
		_rotulo_da_aba(aba).add_theme_color_override("font_color", COR_ABA_ATIVA if _aba == aba else COR_ABA_INATIVA)
	_posicionar_marcador.call_deferred()


func _rotulo_da_aba(aba: Aba) -> Label:
	match aba:
		Aba.CRIACAO:
			return aba_criacao
		Aba.ANOTACOES:
			return aba_anotacoes
		Aba.OBJETIVO:
			return aba_objetivo
	return aba_itens


func _posicionar_marcador() -> void:
	var area := _rotulo_da_aba(_aba).get_global_rect()
	marcador.global_position.x = area.position.x - 2.0
	marcador.size.x = area.size.x + 4.0


func _ao_clicar_aba(evento: InputEvent, aba: Aba) -> void:
	if evento is InputEventMouseButton and evento.pressed and evento.button_index == MOUSE_BUTTON_LEFT \
			and aba != _aba:
		_mostrar_aba(aba)
		som_aba.play()


func _escolher(posicao: Vector2i) -> void:
	var outro_espaco := posicao != _cursor
	_cursor = posicao
	_atualizar()
	if outro_espaco:
		_destacar_selecao()


func _destacar_selecao() -> void:
	_espacos_grade[_cursor.y * Inventario.COLUNAS + _cursor.x].destacar()
	if _fade_textos:
		_fade_textos.kill()
	_fade_textos = create_tween().set_parallel()
	for texto in [nome, descricao, situacao, dica_examinar]:
		texto.modulate.a = 0.0
		_fade_textos.tween_property(texto, "modulate:a", 1.0, SEGUNDOS_FADE_TEXTO)


func _equipar_no_espaco(espaco: int) -> void:
	var item := Inventario.item_em(_cursor.y, _cursor.x)
	if item and item.equipavel:
		if Inventario.espaco_do_gadget(item) == espaco:
			_desequipar(espaco)
		else:
			Inventario.equipar(item, espaco)
			som_equipar.play()
			_espacos_gadget[espaco].destacar()
	elif item == null and Inventario.gadgets[espaco] != null:
		_desequipar(espaco)


func _desequipar(espaco: int) -> void:
	Inventario.desequipar(espaco)
	som_desequipar.play()


func _atualizar() -> void:
	if not is_node_ready():
		return
	painel_criacao.atualizar()
	var i := 0
	for linha in Inventario.LINHAS:
		for coluna in Inventario.COLUNAS:
			var item := Inventario.item_em(linha, coluna)
			var selecionado := Vector2i(coluna, linha) == _cursor
			var equipado := Inventario.espaco_do_gadget(item) if item else -1
			var texto := str(equipado + 1) if equipado != -1 else ""
			_espacos_grade[i].mostrar(item, selecionado, texto)
			i += 1
	for g in Inventario.ESPACOS_GADGET:
		_espacos_gadget[g].mostrar(Inventario.gadgets[g], false, str(g + 1))
	var escolhido := Inventario.item_em(_cursor.y, _cursor.x)
	nome.text = escolhido.nome if escolhido else ""
	descricao.text = escolhido.descricao if escolhido else ""
	dica_examinar.text = "E: examinar" if escolhido else ""
	situacao.text = ""
	if escolhido and escolhido.equipavel:
		var espaco := Inventario.espaco_do_gadget(escolhido)
		if espaco != -1:
			situacao.text = "Equipado na tecla %d" % (espaco + 1)
		else:
			situacao.text = "Aperte 1, 2 ou 3 para equipar"
