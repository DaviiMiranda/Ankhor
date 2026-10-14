extends Sala

const CENA_SENTINELA := preload("res://cenas/personagens/robo_sentinela.tscn")
const CENA_RASTREADOR := preload("res://cenas/personagens/robo_rastreador.tscn")
const CENA_CHECKPOINT := preload("res://cenas/sistemas/checkpoint.tscn")
const CENA_LAMPADA := preload("res://cenas/cenario/objetos/lampada.tscn")
const CENA_PILHA := preload("res://cenas/itens/pilha_no_chao.tscn")
const CENA_ITEM := preload("res://cenas/itens/item_no_chao.tscn")
const CENA_SAIDA := preload("res://cenas/sistemas/saida_fase.tscn")
const CENA_NO := preload("res://cenas/sistemas/no_hackeavel.tscn")
const CENA_ZANE := preload("res://cenas/personagens/zane_na_oficina.tscn")
const LANTERNA := preload("res://dados/itens/lanterna.tres")
const PROPS := {
	"b": preload("res://cenas/cenario/dtec/objetos/bancada_eletronica.tscn"),
	"c": preload("res://cenas/cenario/dtec/objetos/console.tscn"),
	"m": preload("res://cenas/cenario/dtec/objetos/mesa_computador.tscn"),
	"x": preload("res://cenas/cenario/dtec/objetos/robo_desmontado.tscn"),
	"r": preload("res://cenas/cenario/dtec/objetos/rack_dtec.tscn"),
	"k": preload("res://cenas/cenario/dtec/objetos/caixas_lab.tscn"),
	"a": preload("res://cenas/cenario/dtec/objetos/braco_robotico.tscn"),
	"u": preload("res://cenas/cenario/dtec/objetos/cadeira_escritorio.tscn"),
	"h": preload("res://cenas/cenario/objetos/holograma_onda.tscn"),
	"i": preload("res://cenas/cenario/objetos/holograma_barras.tscn"),
	"j": preload("res://cenas/cenario/objetos/holograma_codigo.tscn"),
}
const LETRAS_LARGAS := "bcmxN"
const DIFICULDADES_DOS_NOS := [Hackeamento.Dificuldade.FACIL, Hackeamento.Dificuldade.MEDIO, Hackeamento.Dificuldade.DIFICIL]
const COR_SAIDA_TRANCADA := Color(1.0, 0.25, 0.2)
const COR_SAIDA_LIBERADA := Color(0.3, 1.0, 0.5)
const ENERGIA_SAIDA_TRANCADA := 0.6
const ENERGIA_SAIDA_LIBERADA := 0.9
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
@export var quantidade_decalques: int = 70
@export var componentes: Array[Texture2D] = []
@export var quantidade_componentes: int = 26
@export var semente: int = 26
@export var transmissao_da_rede: Transmissao
@export_file("*.tscn") var cena_da_saida: String = ""
@export var titulo_da_saida: String = ""
@export var subtitulo_da_saida: String = ""

var grade: GradeLabirinto
var _perseguindo := {}
var _saida: SaidaFase
var _luz_saida: PointLight2D
var _numero_do_no := 0

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
	_espalhar_componentes()
	_colocar_marcadores()
	_montar_rede()
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
	_luz_saida = luz


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


func _espalhar_componentes() -> void:
	var area := mapa.area_oficina
	if componentes.is_empty() or area.size == Vector2i.ZERO:
		return
	var sorteio := RandomNumberGenerator.new()
	sorteio.seed = semente + 7
	for i in quantidade_componentes:
		var celula := Vector2i(area.position.x + sorteio.randi() % area.size.x,
				area.position.y + sorteio.randi() % area.size.y)
		var peca := Sprite2D.new()
		peca.texture = componentes[sorteio.randi() % componentes.size()]
		peca.position = grade.centro(celula) + Vector2(sorteio.randf_range(-10, 10), sorteio.randf_range(-8, 8))
		peca.flip_h = sorteio.randf() < 0.5
		no_decalques.add_child(peca)


func _montar_rede() -> void:
	var total := _contar_nos()
	if total == 0:
		return
	var rede := RedeDoLabirinto.new()
	rede.name = "RedeDoLabirinto"
	rede.total_de_nos = total
	rede.transmissao = transmissao_da_rede
	add_child(rede)
	rede.liberada.connect(_liberar_saida)


func _contar_nos() -> int:
	var total := 0
	for celula in mapa.celulas_com("N"):
		if _comeca_sequencia(celula, "N"):
			total += 1
	return total


func _liberar_saida() -> void:
	if _saida:
		_saida.set_deferred("monitoring", true)
	if _luz_saida:
		_luz_saida.color = COR_SAIDA_LIBERADA
		_luz_saida.energy = ENERGIA_SAIDA_LIBERADA


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
					_colocar_saida(posicao + Vector2(mapa.tamanho_bloco / 2.0, 0))
				"Z":
					var zane := CENA_ZANE.instantiate()
					zane.name = "Zane"
					_colocar(zane, posicao)
				"N":
					if _comeca_sequencia(celula, "N"):
						_colocar_no(_posicao_da_sequencia(celula, "N"))
				"V", "R":
					numero += 1
					_colocar_robo(mapa.letra(celula), posicao, numero)
				_:
					_colocar_prop(celula)


func _colocar_saida(posicao: Vector2) -> void:
	var saida: SaidaFase = CENA_SAIDA.instantiate()
	saida.name = "Saida"
	if _contar_nos() > 0:
		saida.monitoring = false
		_luz_saida.color = COR_SAIDA_TRANCADA
		_luz_saida.energy = ENERGIA_SAIDA_TRANCADA
	if not cena_da_saida.is_empty():
		saida.cena_destino = cena_da_saida
	_saida = saida
	_colocar(saida, posicao)
	if not titulo_da_saida.is_empty():
		(saida.get_node("Tela/Titulo") as Label).text = titulo_da_saida
	if not subtitulo_da_saida.is_empty():
		(saida.get_node("Tela/Titulo/Subtitulo") as Label).text = subtitulo_da_saida


func _colocar_no(posicao: Vector2) -> void:
	_numero_do_no += 1
	var no: NoHackeavel = CENA_NO.instantiate()
	no.name = "No_%d" % _numero_do_no
	no.id = "%s%d" % [RedeDoLabirinto.PREFIXO_DA_MARCA, _numero_do_no]
	no.marca_ao_destrancar = no.id
	no.dificuldade_hack = DIFICULDADES_DOS_NOS[mini(_numero_do_no - 1, DIFICULDADES_DOS_NOS.size() - 1)]
	_colocar(no, posicao)


func _colocar_prop(celula: Vector2i) -> void:
	var letra := mapa.letra(celula)
	if not PROPS.has(letra):
		return
	var largo := LETRAS_LARGAS.contains(letra)
	if largo and not _comeca_sequencia(celula, letra):
		return
	var prop: Node2D = PROPS[letra].instantiate()
	prop.name = "Prop_%s_%d_%d" % [letra, celula.x, celula.y]
	_colocar(prop, _posicao_da_sequencia(celula, letra) if largo else grade.centro(celula))


func _comeca_sequencia(celula: Vector2i, letra: String) -> bool:
	return mapa.letra(celula + Vector2i.LEFT) != letra


func _posicao_da_sequencia(celula: Vector2i, letra: String) -> Vector2:
	var tamanho := 1
	while mapa.letra(celula + Vector2i(tamanho, 0)) == letra:
		tamanho += 1
	return grade.centro(celula) + Vector2((tamanho - 1) * mapa.tamanho_bloco / 2.0, 0)


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
