extends MecanismoDoTempo

const ANOS_DE_LANCAMENTO: Array[int] = [1985, 1989, 1990]
const PRIMEIRO_ANO := 1980
const QUANTIDADE_DE_ANOS := 16
const ESCALA := 2.0
const LARGURA_QUADRO := 22.0
const ALTURA_QUADRO := 30.0
const ESPACO := 12.0
const COR_VISOR := Color("ffb347")
const COR_FUNDO_VISOR := Color("140c06")

@export var quadros: Array[Texture2D] = []
@export var segundos_por_ano_inicial: float = 0.38
@export var aceleracao_por_acerto: float = 1.3

var _segundos_por_ano := 0.0
var _inicio := 0.0


func _preparar() -> void:
	acertos_para_alinhar = ANOS_DE_LANCAMENTO.size()
	_segundos_por_ano = segundos_por_ano_inicial
	_reiniciar_contador()


func _acertou() -> bool:
	return _ano_mostrado() == ANOS_DE_LANCAMENTO[_acertos]


func _ao_acertar() -> void:
	_segundos_por_ano /= aceleracao_por_acerto
	_reiniciar_contador()


func _ao_errar() -> void:
	_preparar()


func _reiniciar_contador() -> void:
	_inicio = _tempo - randi_range(0, QUANTIDADE_DE_ANOS - 1) * _segundos_por_ano


func _ano_mostrado() -> int:
	var passos := floori((_tempo - _inicio) / _segundos_por_ano)
	return PRIMEIRO_ANO + posmod(passos, QUANTIDADE_DE_ANOS)


func _desenhar(centro: Vector2) -> void:
	var tamanho := Vector2(LARGURA_QUADRO, ALTURA_QUADRO) * ESCALA
	var largura_total := tamanho.x * quadros.size() + ESPACO * (quadros.size() - 1)
	var fonte := desenho.get_theme_default_font()
	for i in quadros.size():
		var canto := Vector2(centro.x - largura_total / 2.0 + i * (tamanho.x + ESPACO), 2.0)
		var travado := i < _acertos
		var atual := i == _acertos
		desenho.draw_texture_rect(quadros[i], Rect2(canto, tamanho), false, Color.WHITE if travado or atual else Color(1, 1, 1, 0.45))
		var borda := COR_ALVO if travado else (COR_TEXTO if atual else COR_APAGADA)
		desenho.draw_rect(Rect2(canto - Vector2.ONE, tamanho + Vector2(2, 2)), borda, false, 1.0)
		var visor := Rect2(canto + Vector2(0, tamanho.y + 6.0), Vector2(tamanho.x, 16.0))
		desenho.draw_rect(visor, COR_FUNDO_VISOR)
		desenho.draw_rect(visor, borda, false, 1.0)
		var texto := "----"
		var cor := COR_APAGADA
		if travado:
			texto = str(ANOS_DE_LANCAMENTO[i])
			cor = COR_ALVO
		elif atual:
			texto = str(_ano_mostrado())
			cor = COR_VISOR
		desenho.draw_string(fonte, Vector2(visor.position.x, visor.position.y + 12.0), texto, HORIZONTAL_ALIGNMENT_CENTER, visor.size.x, 8, cor)
