class_name ZonaDeGas
extends ColorRect

const SHADER_GAS := preload("res://shaders/gas.gdshader")
const SOM_TOSSE := preload("res://assets/audio/efeitos/objetos/tosse.wav")
const SOM_SIBILO := preload("res://assets/audio/efeitos/objetos/gas_sibilo.wav")
const AVISO_GAS := "Esse ar queima a garganta. Sem máscara, não dá para ficar aqui."
const AVISO_VENTILACAO := "Os exaustores ligaram. O gás do setor B está saindo."
const ALCANCE_TOSSE := 10
const PASSOS_INICIAIS := 300
const INTERVALO_PASSO := 0.1

@export var marca_ventilacao: String = "bunker_energia"
@export var tamanho_celula: int = 16
@export var fontes: PackedVector2Array = PackedVector2Array()
@export var difusao: float = 0.22
@export var perda: float = 0.002
@export var perda_com_exaustor: float = 0.08
@export var densidade_que_fere: float = 0.25
@export var segundos_por_coracao: float = 5.0

var _largura_grade := 0
var _altura_grade := 0
var _densidade := PackedFloat32Array()
var _imagem: Image
var _textura: ImageTexture
var _tempo_passo := 0.0
var _tempo_no_gas := 0.0
var _ventilando := false
var _avisou := false
var _sibilo: AudioStreamPlayer2D


func _ready() -> void:
	if Progresso.tem(marca_ventilacao):
		queue_free()
		return
	z_index = 4
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_largura_grade = ceili(size.x / tamanho_celula)
	_altura_grade = ceili(size.y / tamanho_celula)
	_densidade.resize(_largura_grade * _altura_grade)
	_densidade.fill(0.0)
	for i in PASSOS_INICIAIS:
		_passo_de_difusao()
	_criar_textura()
	_tocar_sibilo()
	Progresso.mudou.connect(_ao_marcar)


func densidade_em(ponto: Vector2) -> float:
	var local := (ponto - global_position) / tamanho_celula
	var x := int(floor(local.x))
	var y := int(floor(local.y))
	if x < 0 or y < 0 or x >= _largura_grade or y >= _altura_grade:
		return 0.0
	return _densidade[y * _largura_grade + x]


func _criar_textura() -> void:
	_imagem = Image.create_empty(_largura_grade, _altura_grade, false, Image.FORMAT_RF)
	_copiar_para_imagem()
	_textura = ImageTexture.create_from_image(_imagem)
	var pintura := ShaderMaterial.new()
	pintura.shader = SHADER_GAS
	pintura.set_shader_parameter("densidade", _textura)
	material = pintura


func _tocar_sibilo() -> void:
	_sibilo = AudioStreamPlayer2D.new()
	_sibilo.stream = SOM_SIBILO
	_sibilo.bus = &"Efeitos"
	_sibilo.volume_db = -16.0
	_sibilo.max_distance = 500.0
	if not fontes.is_empty():
		_sibilo.position = fontes[0] * tamanho_celula
	add_child(_sibilo)
	_sibilo.finished.connect(_sibilo.play)
	_sibilo.play()


func _copiar_para_imagem() -> void:
	for y in _altura_grade:
		for x in _largura_grade:
			_imagem.set_pixel(x, y, Color(_densidade[y * _largura_grade + x], 0, 0))


func _passo_de_difusao() -> void:
	var nova := _densidade.duplicate()
	var perda_atual := perda_com_exaustor if _ventilando else perda
	for y in _altura_grade:
		for x in _largura_grade:
			var i := y * _largura_grade + x
			var aqui := _densidade[i]
			var esquerda := _densidade[i - 1] if x > 0 else 0.0
			var direita := _densidade[i + 1] if x < _largura_grade - 1 else 0.0
			var cima := _densidade[i - _largura_grade] if y > 0 else aqui
			var baixo := _densidade[i + _largura_grade] if y < _altura_grade - 1 else aqui
			var laplaciano := esquerda + direita + cima + baixo - 4.0 * aqui
			nova[i] = maxf(aqui + difusao * laplaciano - perda_atual * aqui, 0.0)
	_densidade = nova
	if _ventilando:
		return
	for fonte in fontes:
		_densidade[int(fonte.y) * _largura_grade + int(fonte.x)] = 1.0


func _process(delta: float) -> void:
	_tempo_passo += delta
	if _tempo_passo >= INTERVALO_PASSO:
		_tempo_passo = 0.0
		_passo_de_difusao()
		_copiar_para_imagem()
		_textura.update(_imagem)
		if _ventilando and _densidade[_densidade.size() / 2] < 0.002 and _maior_densidade() < 0.01:
			queue_free()


func _maior_densidade() -> float:
	var maior := 0.0
	for valor in _densidade:
		maior = maxf(maior, valor)
	return maior


func _physics_process(delta: float) -> void:
	var gabriel := get_tree().get_first_node_in_group("jogador") as Gabriel
	if gabriel == null or Inventario.estado_de("mascara_gas").get("aceso", false):
		_tempo_no_gas = 0.0
		return
	if densidade_em(gabriel.global_position) < densidade_que_fere:
		_tempo_no_gas = maxf(_tempo_no_gas - delta, 0.0)
		return
	if not _avisou:
		_avisou = true
		Inventario.aviso.emit(AVISO_GAS)
	_tempo_no_gas += delta
	if _tempo_no_gas >= segundos_por_coracao:
		_tempo_no_gas = 0.0
		Vida.receber_dano(1, gabriel.global_position)
		_tossir(gabriel)


func _tossir(gabriel: Gabriel) -> void:
	var som := AudioStreamPlayer.new()
	som.stream = SOM_TOSSE
	som.bus = &"Efeitos"
	som.finished.connect(som.queue_free)
	add_child(som)
	som.play()
	Robo.fazer_barulho(get_tree(), gabriel.global_position, ALCANCE_TOSSE)


func _ao_marcar(marca: String) -> void:
	if marca != marca_ventilacao:
		return
	_ventilando = true
	if _sibilo:
		_sibilo.stop()
	Inventario.aviso.emit(AVISO_VENTILACAO)
