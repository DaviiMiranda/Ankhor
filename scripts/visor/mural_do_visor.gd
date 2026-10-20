class_name MuralDoVisor
extends FocoVisor

const PAPEL := preload("res://assets/sprites/interface/papel_caderno_gabriel.png")
const TINTA := Color("2e2e36")
const COR_DO_FIO := Color(0.78, 0.1, 0.12)
const COLUNAS := 6
const LINHAS := 4
const TAMANHO_CARTAO := Vector2(0.28, 0.19)
const PIXEL_DO_TEXTO := 0.0037
const RAIO_DO_ALFINETE := 0.012
const DESVIO := Vector2(0.025, 0.02)
const GIRO_MAXIMO := 4.0
const VAZIO := "Nada anotado ainda"

var _cartoes: Array[PapelDoVisor] = []
var _selecionado := 0


func _ready() -> void:
	super()
	_montar()


func focar() -> void:
	_destacar(_selecionado)


func soltar() -> void:
	_destacar(-1)


func receber(evento: InputEvent) -> void:
	if evento.is_action_pressed("mover_esquerda"):
		_mover(-1)
	elif evento.is_action_pressed("mover_direita"):
		_mover(1)
	elif evento.is_action_pressed("mover_cima"):
		_mover(-COLUNAS)
	elif evento.is_action_pressed("mover_baixo"):
		_mover(COLUNAS)
	elif evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept"):
		var cartao := _cartoes[_selecionado]
		if cartao.documento:
			leitura_pedida.emit(cartao.documento)


static func documento_da_anotacao(anotacao: Dictionary) -> Documento:
	var documento := Documento.new()
	documento.id = anotacao["id"]
	documento.titulo = anotacao["titulo"]
	documento.autor = anotacao["titulo"]
	documento.papel = "caderno_gabriel"
	documento.paginas = PackedStringArray(String(anotacao["texto"]).split("\n\n"))
	return documento


func _montar() -> void:
	var anotacoes := Caderno.anotacoes.slice(-COLUNAS * LINHAS)
	if anotacoes.is_empty():
		_criar_cartao(0, VAZIO, null, 0)
	for i in anotacoes.size():
		var anotacao: Dictionary = anotacoes[i]
		_criar_cartao(i, anotacao["titulo"], documento_da_anotacao(anotacao), hash(anotacao["id"]))
	_esticar_fio()


func _criar_cartao(indice: int, titulo: String, documento: Documento, semente: int) -> void:
	var sorteio := RandomNumberGenerator.new()
	sorteio.seed = semente
	var passo := tamanho / Vector2(COLUNAS, LINHAS)
	var coluna := indice % COLUNAS
	var linha := indice / COLUNAS
	var cartao := PapelDoVisor.new()
	cartao.position = Vector3(
		(coluna - (COLUNAS - 1) / 2.0) * passo.x + sorteio.randf_range(-DESVIO.x, DESVIO.x),
		((LINHAS - 1) / 2.0 - linha) * passo.y + sorteio.randf_range(-DESVIO.y, DESVIO.y),
		0.004 + indice * 0.0005)
	cartao.rotation.z = deg_to_rad(sorteio.randf_range(-GIRO_MAXIMO, GIRO_MAXIMO))
	cartao.documento = documento
	add_child(cartao)
	cartao.montar(PAPEL, titulo, TINTA, TAMANHO_CARTAO, PIXEL_DO_TEXTO)
	cartao.add_child(_alfinete())
	_cartoes.append(cartao)


func _alfinete() -> MeshInstance3D:
	var esfera := SphereMesh.new()
	esfera.radius = RAIO_DO_ALFINETE
	esfera.height = RAIO_DO_ALFINETE * 2.0
	var material := StandardMaterial3D.new()
	material.albedo_color = COR_DO_FIO
	var alfinete := MeshInstance3D.new()
	alfinete.mesh = esfera
	alfinete.material_override = material
	alfinete.position = Vector3(0.0, TAMANHO_CARTAO.y / 2.0 - 0.02, 0.01)
	return alfinete


func _esticar_fio() -> void:
	if _cartoes.size() < 2:
		return
	var linhas := ImmediateMesh.new()
	var material := StandardMaterial3D.new()
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.albedo_color = COR_DO_FIO
	linhas.surface_begin(Mesh.PRIMITIVE_LINES, material)
	for i in _cartoes.size() - 1:
		linhas.surface_add_vertex(_ponta_do_alfinete(_cartoes[i]))
		linhas.surface_add_vertex(_ponta_do_alfinete(_cartoes[i + 1]))
	linhas.surface_end()
	var fio := MeshInstance3D.new()
	fio.mesh = linhas
	add_child(fio)


func _ponta_do_alfinete(cartao: PapelDoVisor) -> Vector3:
	return cartao.transform * Vector3(0.0, TAMANHO_CARTAO.y / 2.0 - 0.02, 0.012)


func _mover(passo: int) -> void:
	var destino := _selecionado + passo
	if destino < 0 or destino >= _cartoes.size():
		return
	_selecionado = destino
	_destacar(_selecionado)


func _destacar(indice: int) -> void:
	for i in _cartoes.size():
		_cartoes[i].destacar(i == indice)
