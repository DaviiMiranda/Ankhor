class_name PainelReligacao
extends Interagivel

const COR_CABO := Color("2c3a4a")
const COR_LIGADO := Color("e8c84a")
const COR_CURSOR := Color("7fd8ff")
const COR_PONTO := Color("8fa3b8")
const COR_PONTO_LIGADO := Color("e8c84a")
const COR_GERADOR := Color("ff9a3a")
const COR_TEXTO := Color("d8dee6")
const COR_PESO := Color("6d8099")
const COR_PRONTO := Color("7cf09a")
const COR_ERRO := Color("e0413a")

const PONTOS := {
	"gerador": ["Gerador", Vector2(60, 140)],
	"corredor_b": ["Corredor B", Vector2(220, 210)],
	"comporta": ["Comporta", Vector2(400, 230)],
	"elevador": ["Elevador", Vector2(200, 60)],
	"corredor_a": ["Corredor A", Vector2(330, 100)],
	"arsenal": ["Arsenal", Vector2(520, 50)],
	"dados": ["Sala de dados", Vector2(480, 150)],
}

const CABOS := [
	["gerador", "corredor_b", 2],
	["gerador", "comporta", 9],
	["gerador", "elevador", 6],
	["corredor_b", "comporta", 3],
	["corredor_b", "elevador", 4],
	["corredor_b", "corredor_a", 7],
	["elevador", "corredor_a", 1],
	["corredor_a", "arsenal", 5],
	["corredor_a", "dados", 8],
	["arsenal", "dados", 10],
	["comporta", "dados", 11],
	["elevador", "arsenal", 12],
]

@export var marca: String = "bunker_energia"
@export var carretel: int = 23
@export var aviso_ligado: String = "A energia voltou ao bunker."
@export var aviso_ja_ligado: String = "O quadro já está religado."
@export var transmissao: Transmissao

var _aberto := false
var _cursor := 0
var _ligados: Array[bool] = []

@onready var tela: CanvasLayer = $Tela
@onready var quadro: Control = $Tela/Quadro
@onready var visor: Label = $Tela/Visor
@onready var dica: Label = $Tela/Dica
@onready var som_cabo: AudioStreamPlayer = $Tela/SomCabo
@onready var som_pronto: AudioStreamPlayer = $Tela/SomPronto


func _ready() -> void:
	super()
	process_mode = Node.PROCESS_MODE_ALWAYS
	tela.visible = false
	quadro.draw.connect(_desenhar)
	for i in CABOS.size():
		_ligados.append(false)
	if Progresso.tem(marca):
		_ligar_arvore_minima()


func pode_interagir() -> bool:
	return not _aberto


func interagir() -> void:
	if Progresso.tem(marca):
		Inventario.aviso.emit(aviso_ja_ligado)
		return
	_aberto = true
	tela.visible = true
	get_tree().paused = true
	dica.text = "Lados: escolher o cabo     E: ligar ou desligar     Esc: sair"
	_mostrar()


static func arvore_minima() -> Array[int]:
	var ordem: Array = range(CABOS.size())
	ordem.sort_custom(func(a, b): return CABOS[a][2] < CABOS[b][2])
	var grupo := {}
	for ponto in PONTOS:
		grupo[ponto] = ponto
	var escolhidos: Array[int] = []
	for i in ordem:
		var raiz_a := _raiz(grupo, CABOS[i][0])
		var raiz_b := _raiz(grupo, CABOS[i][1])
		if raiz_a != raiz_b:
			grupo[raiz_a] = raiz_b
			escolhidos.append(i)
	return escolhidos


static func _raiz(grupo: Dictionary, ponto: String) -> String:
	while grupo[ponto] != ponto:
		ponto = grupo[ponto]
	return ponto


static func custo_minimo() -> int:
	var total := 0
	for i in arvore_minima():
		total += CABOS[i][2]
	return total


func cabo_usado() -> int:
	var total := 0
	for i in CABOS.size():
		if _ligados[i]:
			total += CABOS[i][2]
	return total


func pontos_alcancados() -> Dictionary:
	var alcancados := {"gerador": true}
	var mudou := true
	while mudou:
		mudou = false
		for i in CABOS.size():
			if not _ligados[i]:
				continue
			var a: String = CABOS[i][0]
			var b: String = CABOS[i][1]
			if alcancados.has(a) != alcancados.has(b):
				alcancados[a] = true
				alcancados[b] = true
				mudou = true
	return alcancados


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
		_cursor = posmod(_cursor - 1, CABOS.size())
		_mostrar()
	elif evento.is_action_pressed("mover_direita") or evento.is_action_pressed("ui_right"):
		_cursor = posmod(_cursor + 1, CABOS.size())
		_mostrar()
	elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		_alternar(_cursor)
	get_viewport().set_input_as_handled()


func _alternar(indice: int) -> void:
	if Progresso.tem(marca):
		return
	_ligados[indice] = not _ligados[indice]
	som_cabo.play()
	_mostrar()
	if pontos_alcancados().size() == PONTOS.size() and cabo_usado() <= carretel:
		_concluir()


func _concluir() -> void:
	visor.text = "TUDO LIGADO COM %d m DE CABO" % cabo_usado()
	visor.add_theme_color_override("font_color", COR_PRONTO)
	som_pronto.play()
	Progresso.marcar(marca)
	await get_tree().create_timer(1.6, true).timeout
	_fechar()
	Inventario.aviso.emit(aviso_ligado)
	if transmissao:
		Radio.transmitir(transmissao)


func _ligar_arvore_minima() -> void:
	for i in arvore_minima():
		_ligados[i] = true


func _mostrar() -> void:
	quadro.queue_redraw()
	if Progresso.tem(marca):
		return
	var usado := cabo_usado()
	var ligados := pontos_alcancados().size()
	visor.text = "Cabo: %d de %d m     Pontos com energia: %d de %d" % [usado, carretel, ligados, PONTOS.size()]
	visor.add_theme_color_override("font_color", COR_ERRO if usado > carretel else COR_TEXTO)


func _desenhar() -> void:
	var fonte := quadro.get_theme_default_font()
	var alcancados := pontos_alcancados()
	for i in CABOS.size():
		var a: Vector2 = PONTOS[CABOS[i][0]][1]
		var b: Vector2 = PONTOS[CABOS[i][1]][1]
		var cor := COR_LIGADO if _ligados[i] else COR_CABO
		var largura := 3.0 if _ligados[i] else 1.0
		if i == _cursor and _aberto:
			quadro.draw_line(a, b, COR_CURSOR, largura + 2.0)
		quadro.draw_line(a, b, cor, largura)
		var meio := (a + b) / 2.0 + Vector2(3, -3)
		quadro.draw_string(fonte, meio, "%d m" % CABOS[i][2], HORIZONTAL_ALIGNMENT_LEFT, -1, 8, COR_PESO)
	for ponto in PONTOS:
		var centro: Vector2 = PONTOS[ponto][1]
		var cor := COR_GERADOR if ponto == "gerador" else (COR_PONTO_LIGADO if alcancados.has(ponto) else COR_PONTO)
		quadro.draw_circle(centro, 8.0, Color(0.05, 0.07, 0.1))
		quadro.draw_circle(centro, 6.0, cor)
		quadro.draw_string(fonte, centro + Vector2(-60, 22), PONTOS[ponto][0], HORIZONTAL_ALIGNMENT_CENTER, 120, 8, COR_TEXTO)
