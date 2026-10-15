extends CanvasLayer

const TEMPO_MINIMO := 0.45
const AREA_IMAGEM := Vector2(140, 104)
const CENTRO_IMAGEM := Vector2(80, 84)
const TAMANHO_NOME_GRANDE := 16
const TAMANHO_NOME_PEQUENO := 8
const TAMANHO_DESCRICAO := 8
const LINHAS_DESCRICAO := 7
const DURACAO_ENTRADA := 0.28
const AMPLITUDE_BALANCO := 1.5
const VELOCIDADE_BALANCO := 1.6
const ETIQUETA_NOVO := "Novo item"
const ETIQUETA_EXAMINAR := "Examinar"
const DICA_NOVO := "E: guardar"
const DICA_EXAMINAR := "E: voltar"

var aberto := false
var _examinando := false
var _opacidade_fundo := 1.0
var _fila: Array[Item] = []
var _tempo := 0.0
var _base_imagem := Vector2.ZERO
var _tween: Tween

@onready var fundo: ColorRect = $Fundo
@onready var luz: TextureRect = $Luz
@onready var imagem: TextureRect = $Imagem
@onready var etiqueta: Label = $Etiqueta
@onready var caixa_texto: VBoxContainer = $Texto
@onready var nome: Label = $Texto/Nome
@onready var descricao: Label = $Texto/Descricao
@onready var dica: Label = $Dica
@onready var som_abrir: AudioStreamPlayer = $SomAbrir
@onready var som_fechar: AudioStreamPlayer = $SomFechar


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false
	_opacidade_fundo = fundo.color.a
	Inventario.item_novo.connect(_ao_item_novo)


func _process(delta: float) -> void:
	if aberto:
		_tempo += delta
		_balancar()
	elif not _fila.is_empty() and not get_tree().paused:
		_abrir(_fila.pop_front())


func _unhandled_input(evento: InputEvent) -> void:
	if not aberto:
		return
	if _tempo >= TEMPO_MINIMO and (evento.is_action_pressed("ui_cancel") or evento.is_action_pressed("interagir")):
		_fechar()
	get_viewport().set_input_as_handled()


func examinar(item: Item) -> void:
	if not aberto:
		_abrir(item, true)


func _ao_item_novo(item: Item) -> void:
	_fila.append(item)


func _abrir(item: Item, examinando := false) -> void:
	_examinando = examinando
	etiqueta.text = ETIQUETA_EXAMINAR if examinando else ETIQUETA_NOVO
	dica.text = DICA_EXAMINAR if examinando else DICA_NOVO
	fundo.color.a = 1.0 if examinando else _opacidade_fundo
	_mostrar_imagem(item)
	_mostrar_texto(item)
	aberto = true
	visible = true
	_tempo = 0.0
	get_tree().paused = true
	som_abrir.play()
	_animar_entrada()


func _fechar() -> void:
	aberto = false
	visible = false
	if not _examinando:
		get_tree().paused = false
	som_fechar.play()


func _mostrar_imagem(item: Item) -> void:
	var textura := item.imagem_detalhe
	var escala: float
	if textura:
		imagem.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		escala = minf(AREA_IMAGEM.x / textura.get_width(), AREA_IMAGEM.y / textura.get_height())
	else:
		textura = item.icone
		imagem.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		escala = maxf(floorf(minf(AREA_IMAGEM.x / textura.get_width(), AREA_IMAGEM.y / textura.get_height())), 1.0)
	var tamanho := (Vector2(textura.get_size()) * escala).round()
	imagem.texture = textura
	imagem.size = tamanho
	imagem.pivot_offset = tamanho / 2.0
	_base_imagem = (CENTRO_IMAGEM - tamanho / 2.0).round()
	imagem.position = _base_imagem


func _mostrar_texto(item: Item) -> void:
	nome.text = item.nome
	descricao.text = item.descricao
	var cabe_numa_linha := _linhas_do_texto(nome, TAMANHO_NOME_GRANDE) <= 1
	nome.add_theme_font_size_override("font_size",
			TAMANHO_NOME_GRANDE if cabe_numa_linha else TAMANHO_NOME_PEQUENO)
	if _linhas_do_texto(descricao, TAMANHO_DESCRICAO) > LINHAS_DESCRICAO:
		push_warning("Descrição de '%s' tem mais de %d linhas: o fim não cabe na tela." \
				% [item.id, LINHAS_DESCRICAO])


func _linhas_do_texto(rotulo: Label, tamanho: int) -> int:
	var fonte := rotulo.get_theme_font("font")
	var medida := fonte.get_multiline_string_size(rotulo.text, HORIZONTAL_ALIGNMENT_LEFT,
			caixa_texto.size.x, tamanho)
	return roundi(medida.y / fonte.get_height(tamanho))


func _animar_entrada() -> void:
	if _tween:
		_tween.kill()
	fundo.modulate.a = 0.0
	luz.modulate.a = 0.0
	caixa_texto.modulate.a = 0.0
	etiqueta.modulate.a = 0.0
	dica.modulate.a = 0.0
	imagem.modulate.a = 0.0
	imagem.scale = Vector2(0.82, 0.82)
	_tween = create_tween().set_parallel(true)
	_tween.tween_property(fundo, "modulate:a", 1.0, DURACAO_ENTRADA)
	_tween.tween_property(luz, "modulate:a", 1.0, DURACAO_ENTRADA * 2.0)
	_tween.tween_property(imagem, "modulate:a", 1.0, DURACAO_ENTRADA)
	_tween.tween_property(imagem, "scale", Vector2.ONE, DURACAO_ENTRADA) \
			.set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	_tween.tween_property(etiqueta, "modulate:a", 1.0, DURACAO_ENTRADA)
	_tween.tween_property(caixa_texto, "modulate:a", 1.0, DURACAO_ENTRADA).set_delay(DURACAO_ENTRADA * 0.6)
	_tween.tween_property(dica, "modulate:a", 1.0, DURACAO_ENTRADA).set_delay(TEMPO_MINIMO)


func _balancar() -> void:
	imagem.position = _base_imagem + Vector2(0, sin(_tempo * VELOCIDADE_BALANCO) * AMPLITUDE_BALANCO).round()
	luz.scale = Vector2.ONE * (1.0 + 0.04 * sin(_tempo * VELOCIDADE_BALANCO * 0.8))
