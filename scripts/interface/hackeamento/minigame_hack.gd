class_name MinigameHack
extends Control

signal terminou(sucesso: bool)

const COR_FUNDO := Color(0.04, 0.07, 0.09)
const COR_BORDA := Color(0.25, 0.55, 0.65)
const COR_APAGADO := Color(0.12, 0.2, 0.24)
const COR_ACESO := Color(0.45, 0.9, 1.0)
const COR_ACERTO := Color(0.4, 1.0, 0.55)
const COR_ERRO := Color(1.0, 0.35, 0.3)
const COR_TEXTO := Color(0.75, 0.95, 1.0)
const SEGUNDOS_RESULTADO := 0.9

var dificuldade := Hackeamento.Dificuldade.MEDIO
var titulo := ""
var instrucao := ""
var vidas := 1
var encerrado := false
var resultado_para_desenho := false


func iniciar(nivel: Hackeamento.Dificuldade) -> void:
	dificuldade = nivel
	encerrado = false
	preparar()
	queue_redraw()


func preparar() -> void:
	pass


func tratar_entrada(_evento: InputEvent) -> void:
	pass


func _por_nivel(valores: Array) -> Variant:
	return valores[dificuldade]


func finalizar(sucesso: bool) -> void:
	if encerrado:
		return
	encerrado = true
	resultado_para_desenho = sucesso
	queue_redraw()
	await get_tree().create_timer(SEGUNDOS_RESULTADO).timeout
	terminou.emit(sucesso)


func desenhar_texto(texto: String, posicao: Vector2, cor: Color = COR_TEXTO, largura: float = -1.0,
		alinhamento: HorizontalAlignment = HORIZONTAL_ALIGNMENT_LEFT) -> void:
	draw_string(get_theme_default_font(), posicao, texto, alinhamento, largura, 8, cor)


func desenhar_vidas(posicao: Vector2, maximo: int) -> void:
	for i in maximo:
		var cor := COR_ERRO if i < vidas else COR_APAGADO
		draw_rect(Rect2(posicao + Vector2(i * 10, 0), Vector2(7, 7)), cor)


func desenhar_resultado() -> void:
	if not encerrado:
		return
	var cor := COR_ACERTO if resultado_para_desenho else COR_ERRO
	var texto := "ACESSO CONCEDIDO" if resultado_para_desenho else "ACESSO NEGADO"
	draw_rect(Rect2(Vector2(0, size.y / 2.0 - 12), Vector2(size.x, 24)), Color(0, 0, 0, 0.8))
	desenhar_texto(texto, Vector2(0, size.y / 2.0 + 3), cor, size.x, HORIZONTAL_ALIGNMENT_CENTER)
