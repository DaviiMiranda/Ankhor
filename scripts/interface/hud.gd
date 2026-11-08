extends CanvasLayer

const CENA_ESPACO := preload("res://cenas/interface/espaco_item.tscn")
const CORACAO_CHEIO := preload("res://assets/sprites/interface/coracao_cheio.png")
const CORACAO_VAZIO := preload("res://assets/sprites/interface/coracao_vazio.png")
const COR_ESTAMINA := Color(0.9, 0.8, 0.55, 1.0)
const COR_EXAUSTO := Color(0.85, 0.25, 0.2, 1.0)
const COR_CARGA := Color(0.45, 0.45, 0.5, 1.0)
const ROTULO_ESTAMINA := "ESTAMINA"
const ROTULO_CARGA := "CARGA: SEM CORRER [G]"

@export var duracao_mensagem: float = 3.5
@export var segundos_por_caractere: float = 0.05

var _espacos: Array[EspacoItem] = []
var _espaco_do_braco: EspacoItem
var _coracoes: Array[TextureRect] = []
var _tween_mensagem: Tween
var _tween_dano: Tween
var _jogador_conectado: Gabriel = null
var _barra_estamina_fundo: ColorRect
var _barra_estamina_preenchimento: ColorRect
var _rotulo_estamina: Label
var _exausto := false

@onready var caixa_gadgets: HBoxContainer = $Gadgets
@onready var aviso: Label = $Aviso
@onready var mensagem: Label = $Mensagem
@onready var caixa_coracoes: HBoxContainer = $Coracoes
@onready var flash_dano: ColorRect = $FlashDano
@onready var som_dano: AudioStreamPlayer = $SomDano


func _ready() -> void:
	for i in Inventario.ESPACOS_GADGET:
		var espaco := CENA_ESPACO.instantiate() as EspacoItem
		espaco.mouse_filter = Control.MOUSE_FILTER_IGNORE
		caixa_gadgets.add_child(espaco)
		_espacos.append(espaco)
	_espaco_do_braco = CENA_ESPACO.instantiate() as EspacoItem
	_espaco_do_braco.mouse_filter = Control.MOUSE_FILTER_IGNORE
	caixa_gadgets.add_child(_espaco_do_braco)
	for i in Vida.MAXIMA:
		var coracao := TextureRect.new()
		coracao.mouse_filter = Control.MOUSE_FILTER_IGNORE
		caixa_coracoes.add_child(coracao)
		_coracoes.append(coracao)
	Inventario.item_pego.connect(_ao_pegar_item)
	Inventario.aviso.connect(_mostrar_mensagem)
	Caderno.anotado.connect(_ao_anotar)
	Checkpoints.marcado.connect(_ao_marcar_checkpoint)
	Vida.mudou.connect(_atualizar_coracoes)
	Vida.dano_recebido.connect(_ao_receber_dano)
	_atualizar_coracoes(Vida.vida)
	_configurar_barra_estamina()
	Inventario.mudou.connect(_pintar_barra_estamina)
	_pintar_barra_estamina()
	flash_dano.color.a = 0.0
	mensagem.modulate.a = 0.0
	aviso.hide()


func _process(_delta: float) -> void:
	_atualizar_gadgets()
	_atualizar_aviso()
	_conectar_jogador()


func _atualizar_gadgets() -> void:
	for i in _espacos.size():
		_mostrar_no_espaco(_espacos[i], Inventario.gadgets[i], i + 1)
	_espaco_do_braco.visible = Inventario.braco != null
	if Inventario.braco:
		_mostrar_no_espaco(_espaco_do_braco, Inventario.braco, Inventario.TECLA_DO_BRACO)


func _mostrar_no_espaco(espaco: EspacoItem, item: Item, tecla: int) -> void:
	var carga := -1.0
	var aceso := false
	if item:
		var estado: Dictionary = Inventario.estado.get(item.id, {})
		carga = estado.get("carga", -1.0)
		aceso = estado.get("aceso", false)
	espaco.mostrar(item, aceso, str(tecla), carga)


func _atualizar_aviso() -> void:
	var jogador := get_tree().get_first_node_in_group("jogador") as Node2D
	var alvo: Interagivel = null
	if jogador:
		alvo = Interagivel.mais_perto(get_tree(), jogador.global_position)
	aviso.visible = alvo != null and not Hackeamento.tela_em_tempo_real
	if not aviso.visible:
		return
	var tecla := "[Segure E] " if alvo.segundos_de_espera() > 0.0 else "[E] "
	aviso.text = (tecla + alvo.texto_acao).strip_edges()
	aviso.reset_size()
	var topo := alvo.get_global_transform_with_canvas() * Vector2(0.0, -alvo.altura_aviso)
	var tela := get_viewport().get_visible_rect().size
	var pos := topo + Vector2(-aviso.size.x / 2.0, -aviso.size.y)
	pos.x = clampf(pos.x, 4.0, tela.x - 4.0 - aviso.size.x)
	pos.y = clampf(pos.y, 4.0, tela.y - 4.0 - aviso.size.y)
	aviso.position = pos.round()


func _ao_pegar_item(item: Item) -> void:
	var texto := "Você pegou: " + item.nome
	var espaco := Inventario.espaco_do_gadget(item)
	if espaco != -1:
		texto += "   [%d] usar" % (espaco + 1)
	texto += "   [Tab] inventário"
	_mostrar_mensagem(texto)


func _atualizar_coracoes(vida: int) -> void:
	for i in _coracoes.size():
		_coracoes[i].texture = CORACAO_CHEIO if i < vida else CORACAO_VAZIO


func _ao_receber_dano(_origem: Vector2) -> void:
	som_dano.play()
	if _tween_dano:
		_tween_dano.kill()
	flash_dano.color.a = 0.45
	_tween_dano = create_tween()
	_tween_dano.tween_property(flash_dano, "color:a", 0.0, 0.5)


func _ao_marcar_checkpoint(_id: String) -> void:
	_mostrar_mensagem("Checkpoint salvo")


func _ao_anotar(titulo: String) -> void:
	_mostrar_mensagem("Nova anotação: %s   [N] ver" % titulo)


func _mostrar_mensagem(texto: String) -> void:
	mensagem.text = texto
	if _tween_mensagem:
		_tween_mensagem.kill()
	mensagem.modulate.a = 1.0
	_tween_mensagem = create_tween()
	_tween_mensagem.tween_interval(maxf(duracao_mensagem, texto.length() * segundos_por_caractere))
	_tween_mensagem.tween_property(mensagem, "modulate:a", 0.0, 0.8)


func _configurar_barra_estamina() -> void:
	_barra_estamina_fundo = ColorRect.new()
	_barra_estamina_fundo.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_barra_estamina_fundo.color = Color(0.0, 0.0, 0.0, 0.65)
	_barra_estamina_fundo.position = Vector2(8.0, 28.0)
	_barra_estamina_fundo.size = Vector2(68.0, 8.0)
	add_child(_barra_estamina_fundo)

	_barra_estamina_preenchimento = ColorRect.new()
	_barra_estamina_preenchimento.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_barra_estamina_preenchimento.color = COR_ESTAMINA
	_barra_estamina_preenchimento.position = Vector2(2.0, 2.0)
	_barra_estamina_preenchimento.size = Vector2(64.0, 4.0)
	_barra_estamina_fundo.add_child(_barra_estamina_preenchimento)

	_rotulo_estamina = Label.new()
	_rotulo_estamina.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_rotulo_estamina.text = ROTULO_ESTAMINA
	_rotulo_estamina.position = Vector2(80.0, 26.0)
	_rotulo_estamina.add_theme_font_size_override("font_size", 8)
	add_child(_rotulo_estamina)


func _conectar_jogador() -> void:
	if _jogador_conectado and is_instance_valid(_jogador_conectado):
		return
	var jogador := get_tree().get_first_node_in_group("jogador") as Gabriel
	if jogador:
		_jogador_conectado = jogador
		_jogador_conectado.fadiga_mudou.connect(_ao_mudar_estamina)
		_jogador_conectado.exaustao_mudou.connect(_ao_mudar_exaustao)
		if _jogador_conectado.fadiga:
			_ao_mudar_estamina(_jogador_conectado.fadiga.estamina, _jogador_conectado.fadiga.estamina_maxima)


func _ao_mudar_estamina(atual: float, maxima: float) -> void:
	if maxima <= 0.0 or _barra_estamina_preenchimento == null:
		return
	var proporcao := clampf(atual / maxima, 0.0, 1.0)
	_barra_estamina_preenchimento.size.x = roundf(64.0 * proporcao)


func _ao_mudar_exaustao(esta_exausto: bool) -> void:
	_exausto = esta_exausto
	_pintar_barra_estamina()


func _pintar_barra_estamina() -> void:
	if _barra_estamina_preenchimento == null:
		return
	var carregando := Inventario.carregando_peso()
	if _exausto:
		_barra_estamina_preenchimento.color = COR_EXAUSTO
	elif carregando:
		_barra_estamina_preenchimento.color = COR_CARGA
	else:
		_barra_estamina_preenchimento.color = COR_ESTAMINA
	_rotulo_estamina.text = ROTULO_CARGA if carregando else ROTULO_ESTAMINA
