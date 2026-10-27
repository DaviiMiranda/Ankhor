class_name QuadroDoVisor
extends FocoVisor

const FONTE := preload("res://cenas/interface/fonte_jogo.tres")
const PASTA_FASES := "res://dados/fases/"
const PASTA_TRANSMISSOES := "res://dados/transmissoes/"
const TINTA_TITULO := Color("c02a2a")
const TINTA := Color("2a3a9a")
const PIXEL_DO_TEXTO := 0.0028
const ENTRELINHA := -4.5
const MARGEM := Vector2(0.07, 0.06)
const TITULO := "ATÉ AQUI"
const SEM_SAVE := "nenhum"
const FASE_DESCONHECIDA := "?"

var _linhas: Label3D


func _ready() -> void:
	super()
	_escrever(_rotulo(16, TINTA_TITULO), TITULO, MARGEM.y)
	_linhas = _rotulo(16, TINTA)
	_escrever(_linhas, "", MARGEM.y + 0.1)
	Salvamento.salvou.connect(atualizar)
	atualizar()


func atualizar() -> void:
	var data := Salvamento.data_salva()
	var linhas := [
		"Fase: %s" % _nome_da_fase(Visor.cena_do_save),
		"Documentos lidos: %d de %d" % [MesaDoVisor.documentos_lidos().size(), MesaDoVisor.todos_os_documentos().size()],
		"Transmissões ouvidas: %d de %d" % [Radio.ouvidas.size(), _contar(PASTA_TRANSMISSOES)],
		"Anotações no caderno: %d" % Caderno.anotacoes.size(),
		"Portas destrancadas: %d" % Porta.destrancadas_salvas().size(),
		"Itens na mochila: %d" % _itens_na_mochila(),
	]
	for colecao in Colecionaveis.todas():
		linhas.append("%s: %d de %d" % [colecao.nome, Colecionaveis.quantidade(colecao.id), colecao.total])
	linhas.append("Último save: %s" % (SEM_SAVE if data.is_empty() else data))
	_linhas.text = "\n".join(linhas)


func _rotulo(tamanho_da_fonte: int, tinta: Color) -> Label3D:
	var rotulo := Label3D.new()
	rotulo.font = FONTE
	rotulo.font_size = tamanho_da_fonte
	rotulo.pixel_size = PIXEL_DO_TEXTO
	rotulo.modulate = tinta
	rotulo.outline_size = 0
	rotulo.line_spacing = ENTRELINHA
	rotulo.double_sided = false
	rotulo.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	rotulo.alpha_cut = Label3D.ALPHA_CUT_DISCARD
	rotulo.horizontal_alignment = HORIZONTAL_ALIGNMENT_LEFT
	rotulo.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	rotulo.width = (tamanho.x - 2.0 * MARGEM.x) / PIXEL_DO_TEXTO
	rotulo.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	return rotulo


func _escrever(rotulo: Label3D, texto: String, do_alto: float) -> void:
	rotulo.text = texto
	rotulo.position = Vector3(-tamanho.x / 2.0 + MARGEM.x, tamanho.y / 2.0 - do_alto, 0.003)
	add_child(rotulo)


func _nome_da_fase(cena: String) -> String:
	for arquivo in ResourceLoader.list_directory(PASTA_FASES):
		var fase := load(PASTA_FASES + arquivo) as Fase
		if fase and fase.pronta() and fase.cena.get_base_dir() == cena.get_base_dir():
			return fase.nome
	return FASE_DESCONHECIDA


func _contar(pasta: String) -> int:
	var quantos := 0
	for arquivo in ResourceLoader.list_directory(pasta):
		if arquivo.ends_with(".tres"):
			quantos += 1
	return quantos


func _itens_na_mochila() -> int:
	var quantos := 0
	for linha in Inventario.grade:
		for item in linha:
			if item != null:
				quantos += 1
	return quantos
