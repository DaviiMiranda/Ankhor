extends Sala

const CENA_SENTINELA := preload("res://cenas/personagens/robo_sentinela.tscn")
const CENA_RASTREADOR := preload("res://cenas/personagens/robo_rastreador.tscn")
const CENA_CHECKPOINT := preload("res://cenas/sistemas/checkpoint.tscn")
const CENA_LAMPADA := preload("res://cenas/cenario/objetos/lampada.tscn")
const CENA_PILHA := preload("res://cenas/itens/pilha_no_chao.tscn")
const CENA_ITEM := preload("res://cenas/itens/item_no_chao.tscn")
const CENA_SAIDA := preload("res://cenas/sistemas/saida_fase.tscn")
const LANTERNA := preload("res://dados/itens/lanterna.tres")
const TEXTURA_LUZ := preload("res://assets/sprites/cenario/luzes/luz.png")
const ALTURA_PAREDE := 40
const CAMADAS_PAREDE := 1 | 8
const LUZ_SO_NAS_PAREDES := 2
const LUZ_EM_TUDO := 1 | 2

@export var mapa: MapaLabirinto
@export var topos: Array[Texture2D] = []
@export var frentes: Array[Texture2D] = []
@export var textura_porta: Texture2D
@export var decalques: Array[Texture2D] = []
@export var quantidade_decalques: int = 45
@export var semente: int = 26

var grade: GradeLabirinto
var _perseguindo := {}

@onready var chao: Sprite2D = $Chao
@onready var no_decalques: Node2D = $Decalques
@onready var objetos: Node2D = $Objetos
@onready var gabriel: Gabriel = $Objetos/Gabriel
@onready var luzes: Node2D = $Luzes
@onready var musica: MusicaLabirinto = $MusicaLabirinto


func _ready() -> void:
	if Engine.is_editor_hint():
		return
	var bloco := mapa.tamanho_bloco
	largura = mapa.largura() * bloco
	altura = mapa.altura() * bloco
	grade = GradeLabirinto.new(mapa)
	_montar_chao()
	_montar_paredes()
	_espalhar_decalques()
	_colocar_marcadores()
	super()


func _montar_chao() -> void:
	chao.region_enabled = true
	chao.region_rect = Rect2(0, 0, largura, altura)


func _montar_paredes() -> void:
	var corpo := StaticBody2D.new()
	corpo.name = "Paredes"
	corpo.collision_layer = CAMADAS_PAREDE
	corpo.collision_mask = 0
	add_child(corpo)
	var oclusores := Node2D.new()
	oclusores.name = "Oclusores"
	add_child(oclusores)
	var bloco := float(mapa.tamanho_bloco)
	for y in mapa.altura():
		var x := 0
		while x < mapa.largura():
			if not mapa.e_parede(Vector2i(x, y)):
				x += 1
				continue
			var inicio := x
			while x < mapa.largura() and mapa.e_parede(Vector2i(x, y)):
				_desenhar_bloco(Vector2i(x, y))
				x += 1
			var retangulo := Rect2(inicio * bloco, y * bloco, (x - inicio) * bloco, bloco)
			_adicionar_colisao(corpo, retangulo)
			_adicionar_oclusor(oclusores, retangulo)


func _desenhar_bloco(celula: Vector2i) -> void:
	var bloco := mapa.tamanho_bloco
	var no := Node2D.new()
	no.name = "Bloco_%d_%d" % [celula.x, celula.y]
	no.position = Vector2(celula.x * bloco, (celula.y + 1) * bloco)
	var topo := Sprite2D.new()
	topo.texture = topos[(celula.x * 5 + celula.y * 11) % topos.size()]
	topo.centered = false
	topo.position = Vector2(0, -bloco - ALTURA_PAREDE)
	topo.light_mask = LUZ_SO_NAS_PAREDES
	no.add_child(topo)
	var textura := _textura_da_frente(celula)
	if textura:
		var frente := Sprite2D.new()
		frente.texture = textura
		frente.centered = false
		frente.position = Vector2(0, -ALTURA_PAREDE)
		frente.light_mask = LUZ_SO_NAS_PAREDES
		no.add_child(frente)
	objetos.add_child(no)


func _textura_da_frente(celula: Vector2i) -> Texture2D:
	var abaixo := celula + Vector2i.DOWN
	if abaixo.y < mapa.altura() and mapa.e_parede(abaixo):
		return null
	if mapa.letra(celula) != "D":
		return frentes[(celula.x * 7 + celula.y * 3) % frentes.size()]
	if mapa.letra(celula + Vector2i.LEFT) == "D":
		return null
	_acender_placa_saida(celula)
	return textura_porta


func _adicionar_colisao(corpo: StaticBody2D, retangulo: Rect2) -> void:
	var forma := CollisionShape2D.new()
	var caixa := RectangleShape2D.new()
	caixa.size = retangulo.size
	forma.shape = caixa
	forma.position = retangulo.get_center()
	corpo.add_child(forma)


func _adicionar_oclusor(pai: Node2D, retangulo: Rect2) -> void:
	var oclusor := LightOccluder2D.new()
	var poligono := OccluderPolygon2D.new()
	poligono.polygon = PackedVector2Array([retangulo.position, Vector2(retangulo.end.x, retangulo.position.y),
			retangulo.end, Vector2(retangulo.position.x, retangulo.end.y)])
	oclusor.occluder = poligono
	pai.add_child(oclusor)


func _acender_placa_saida(celula: Vector2i) -> void:
	var bloco := mapa.tamanho_bloco
	var luz := PointLight2D.new()
	luz.texture = TEXTURA_LUZ
	luz.color = Color(0.3, 1.0, 0.5)
	luz.energy = 0.9
	luz.texture_scale = 1.6
	luz.range_item_cull_mask = LUZ_EM_TUDO
	luz.position = Vector2((celula.x + 1) * bloco, (celula.y + 1) * bloco - ALTURA_PAREDE + 8)
	luzes.add_child(luz)


func _espalhar_decalques() -> void:
	if decalques.is_empty():
		return
	var sorteio := RandomNumberGenerator.new()
	sorteio.seed = semente
	var livres := mapa.celulas_com(".")
	for i in mini(quantidade_decalques, livres.size()):
		var celula: Vector2i = livres[sorteio.randi() % livres.size()]
		var decalque := Sprite2D.new()
		decalque.texture = decalques[sorteio.randi() % decalques.size()]
		decalque.position = grade.centro(celula) + Vector2(sorteio.randf_range(-10, 10), sorteio.randf_range(-10, 10))
		decalque.flip_h = sorteio.randf() < 0.5
		no_decalques.add_child(decalque)


func _colocar_marcadores() -> void:
	var numero := 0
	for y in mapa.altura():
		for x in mapa.largura():
			var celula := Vector2i(x, y)
			var posicao := grade.centro(celula)
			match mapa.letra(celula):
				"G":
					gabriel.global_position = posicao
				"T":
					if not Inventario.tem(LANTERNA.id):
						var item := CENA_ITEM.instantiate()
						item.name = "Lanterna"
						item.item = LANTERNA
						_colocar(item, posicao)
				"C":
					var posto := CENA_CHECKPOINT.instantiate()
					posto.name = "Checkpoint_%d_%d" % [x, y]
					_colocar(posto, posicao)
				"P":
					var pilha := CENA_PILHA.instantiate()
					pilha.name = "Pilha_%d_%d" % [x, y]
					_colocar(pilha, posicao)
				"L":
					var lampada := CENA_LAMPADA.instantiate()
					lampada.name = "Lampada_%d_%d" % [x, y]
					_colocar(lampada, posicao + Vector2(-8, 0))
				"S":
					var saida := CENA_SAIDA.instantiate()
					saida.name = "Saida"
					_colocar(saida, posicao + Vector2(mapa.tamanho_bloco / 2.0, 0))
				"V", "R":
					numero += 1
					_colocar_robo(mapa.letra(celula), posicao, numero)


func _colocar(no: Node2D, posicao: Vector2) -> void:
	no.position = posicao
	objetos.add_child(no)


func _colocar_robo(letra: String, posicao: Vector2, numero: int) -> void:
	var robo: Robo = (CENA_SENTINELA if letra == "V" else CENA_RASTREADOR).instantiate()
	robo.name = "%s%d" % [robo.nome_tipo, numero]
	_colocar(robo, posicao)
	robo.configurar(grade, semente * 100 + numero)
	robo.jogador_detectado.connect(_ao_robo_detectar)
	robo.jogador_perdido.connect(_ao_robo_perder)


func _ao_robo_detectar(robo: Robo) -> void:
	_perseguindo[robo] = true
	musica.perigo = 1.0


func _ao_robo_perder(robo: Robo) -> void:
	_perseguindo.erase(robo)
	if _perseguindo.is_empty():
		musica.perigo = 0.0
