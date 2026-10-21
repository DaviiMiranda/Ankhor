class_name MesaDoVisor
extends FocoVisor

const PASTA_DOCUMENTOS := "res://dados/documentos/"
const PAPEIS := {
	"pergaminho": [preload("res://assets/sprites/interface/papel_pergaminho.png"), Color("3a2210")],
	"caderno_clarice": [preload("res://assets/sprites/interface/papel_caderno_clarice.png"), Color("22306e")],
	"caderno_gabriel": [preload("res://assets/sprites/interface/papel_caderno_gabriel.png"), Color("2e2e36")],
	"carta": [preload("res://assets/sprites/interface/papel_carta.png"), Color("26283a")],
	"carta_faroleiro": [preload("res://assets/sprites/interface/papel_carta_faroleiro.png"), Color("3b2614")],
}
const COLUNAS := 5
const LINHAS := 3
const TAMANHO_PAPEL := Vector2(0.2, 0.126)
const PIXEL_DO_TEXTO := 0.0024
const DESVIO := 0.02
const GIRO_MAXIMO := 12.0

@export var area_dos_papeis := Vector2(0.96, 0.33)
@export var centro_dos_papeis := Vector2.ZERO

var _papeis: Array[PapelDoVisor] = []
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
	elif (evento.is_action_pressed("interagir") or evento.is_action_pressed("ui_accept")) and not _papeis.is_empty():
		leitura_pedida.emit(_papeis[_selecionado].documento)


static func documentos_lidos() -> Array[Documento]:
	var lidos: Array[Documento] = []
	for documento in todos_os_documentos():
		if Caderno.tem_anotacao(documento.id):
			lidos.append(documento)
	return lidos


static func todos_os_documentos() -> Array[Documento]:
	var documentos: Array[Documento] = []
	for arquivo in ResourceLoader.list_directory(PASTA_DOCUMENTOS):
		if not arquivo.ends_with(".tres"):
			continue
		var documento := load(PASTA_DOCUMENTOS + arquivo) as Documento
		if documento:
			documentos.append(documento)
	return documentos


func _montar() -> void:
	var tampo := Node3D.new()
	tampo.top_level = true
	add_child(tampo)
	var plano := _plano_do_tampo()
	tampo.global_transform = Transform3D(plano, global_position + plano * Vector3(centro_dos_papeis.x, centro_dos_papeis.y, 0.001))
	var lidos := documentos_lidos().slice(0, COLUNAS * LINHAS)
	for i in lidos.size():
		_criar_papel(tampo, i, lidos[i])


func _plano_do_tampo() -> Basis:
	var topo := Vector3(cima().x, 0.0, cima().z).normalized()
	return Basis(topo.cross(Vector3.UP), topo, Vector3.UP)


func _criar_papel(tampo: Node3D, indice: int, documento: Documento) -> void:
	var sorteio := RandomNumberGenerator.new()
	sorteio.seed = hash(documento.id)
	var passo := area_dos_papeis / Vector2(COLUNAS, LINHAS)
	var coluna := indice % COLUNAS
	var linha := indice / COLUNAS
	var papel := PapelDoVisor.new()
	papel.position = Vector3(
		(coluna - (COLUNAS - 1) / 2.0) * passo.x + sorteio.randf_range(-DESVIO, DESVIO),
		((LINHAS - 1) / 2.0 - linha) * passo.y + sorteio.randf_range(-DESVIO, DESVIO),
		0.002 + indice * 0.0015)
	papel.rotation.z = deg_to_rad(sorteio.randf_range(-GIRO_MAXIMO, GIRO_MAXIMO))
	papel.documento = documento
	tampo.add_child(papel)
	var estilo: Array = PAPEIS.get(documento.papel, PAPEIS["caderno_gabriel"])
	papel.montar(estilo[0], documento.titulo, estilo[1], TAMANHO_PAPEL, PIXEL_DO_TEXTO)
	_papeis.append(papel)


func _mover(passo: int) -> void:
	var destino := _selecionado + passo
	if destino < 0 or destino >= _papeis.size():
		return
	_selecionado = destino
	_destacar(_selecionado)


func _destacar(indice: int) -> void:
	for i in _papeis.size():
		_papeis[i].destacar(i == indice)
