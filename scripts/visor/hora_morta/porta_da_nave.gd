class_name PortaDaNave
extends ObjetoDaNave

const LARGURA := 1.5
const ALTURA := 2.1
const PROFUNDIDADE := 0.34
const DESLIZE := 0.72
const SEGUNDOS_ABRINDO := 0.45
const DISTANCIA_DE_ABRIR := 2.3
const COR_LIVRE := Color(0.2, 1.0, 0.4)
const COR_TRANCADA := Color(1.0, 0.12, 0.08)

@export var trancada := false
@export var texto_da_placa := ""

var alvo: Node3D
var _aberta := false
var _folhas: Array[MeshInstance3D] = []
var _bloqueio: CollisionShape3D
var _luz: StandardMaterial3D
var _movimento: Tween

@onready var som: AudioStreamPlayer3D = $Som


func _ready() -> void:
	_montar_folhas()
	_montar_batente()
	_montar_bloqueio()
	_montar_placa()
	_atualizar_luz()


func _process(_delta: float) -> void:
	if alvo == null:
		return
	var perto := global_position.distance_to(alvo.global_position) <= DISTANCIA_DE_ABRIR
	_definir_aberta(perto and not trancada)


func ponto_da_mira() -> Vector3:
	return global_position + Vector3.UP * 1.2


func pode_mirar() -> bool:
	return trancada and super.pode_mirar()


func destrancar() -> void:
	trancada = false
	_atualizar_luz()


func _definir_aberta(aberta: bool) -> void:
	if aberta == _aberta:
		return
	_aberta = aberta
	_bloqueio.set_deferred("disabled", aberta)
	som.play()
	if _movimento:
		_movimento.kill()
	_movimento = create_tween().set_parallel()
	for indice in _folhas.size():
		var lado := -1.0 if indice == 0 else 1.0
		var parada := lado * LARGURA / 4.0
		var destino := parada + lado * DESLIZE if aberta else parada
		_movimento.tween_property(_folhas[indice], "position:x", destino, SEGUNDOS_ABRINDO)


func _montar_folhas() -> void:
	for indice in 2:
		var acabamento := StandardMaterial3D.new()
		acabamento.albedo_texture = load(KitDaNave.PASTA % "porta_nave")
		acabamento.normal_enabled = true
		acabamento.normal_texture = load(KitDaNave.PASTA % "porta_nave_n")
		acabamento.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
		acabamento.roughness = 0.55
		acabamento.metallic = 0.35
		acabamento.cull_mode = BaseMaterial3D.CULL_DISABLED
		acabamento.uv1_scale = Vector3(0.5, 1.0, 1.0)
		acabamento.uv1_offset = Vector3(0.5 * float(indice), 0.0, 0.0)
		var malha := QuadMesh.new()
		malha.size = Vector2(LARGURA / 2.0, ALTURA)
		var folha := MeshInstance3D.new()
		folha.mesh = malha
		folha.material_override = acabamento
		folha.position = Vector3((float(indice) - 0.5) * LARGURA / 2.0, ALTURA / 2.0, 0.0)
		add_child(folha)
		_folhas.append(folha)


func _montar_batente() -> void:
	var metal: Material = _metal_do_batente()
	_peca(Vector3(0.12, ALTURA + 0.12, PROFUNDIDADE), Vector3(-LARGURA / 2.0 - 0.06, (ALTURA + 0.12) / 2.0, 0.0), metal)
	_peca(Vector3(0.12, ALTURA + 0.12, PROFUNDIDADE), Vector3(LARGURA / 2.0 + 0.06, (ALTURA + 0.12) / 2.0, 0.0), metal)
	_peca(Vector3(LARGURA, 0.12, PROFUNDIDADE), Vector3(0.0, ALTURA + 0.06, 0.0), metal)
	_peca(Vector3(LARGURA, 0.012, PROFUNDIDADE), Vector3(0.0, 0.006, 0.0), metal)
	_luz = StandardMaterial3D.new()
	_luz.emission_enabled = true
	_luz.emission_energy_multiplier = 2.4
	_peca(Vector3(0.1, 0.1, PROFUNDIDADE + 0.02), Vector3(LARGURA / 2.0 + 0.06, 1.3, 0.0), _luz)
	_peca(Vector3(0.1, 0.1, PROFUNDIDADE + 0.02), Vector3(-LARGURA / 2.0 - 0.06, 1.3, 0.0), _luz)


func _metal_do_batente() -> Material:
	var novo := StandardMaterial3D.new()
	novo.albedo_texture = load(KitDaNave.PASTA % "faixa_perigo")
	novo.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
	novo.uv1_triplanar = true
	novo.uv1_world_triplanar = true
	novo.uv1_scale = Vector3.ONE * 2.0
	novo.roughness = 0.6
	return novo


func _peca(medidas: Vector3, lugar: Vector3, acabamento: Material) -> void:
	var malha := BoxMesh.new()
	malha.size = medidas
	var nova := MeshInstance3D.new()
	nova.mesh = malha
	nova.material_override = acabamento
	nova.position = lugar
	add_child(nova)


func _montar_bloqueio() -> void:
	var corpo := StaticBody3D.new()
	add_child(corpo)
	var caixa := BoxShape3D.new()
	caixa.size = Vector3(LARGURA, ALTURA, PROFUNDIDADE)
	_bloqueio = CollisionShape3D.new()
	_bloqueio.shape = caixa
	_bloqueio.position = Vector3.UP * ALTURA / 2.0
	corpo.add_child(_bloqueio)
	for lado: float in [-1.0, 1.0]:
		var ombreira := BoxShape3D.new()
		ombreira.size = Vector3(0.12, ALTURA, PROFUNDIDADE)
		var forma := CollisionShape3D.new()
		forma.shape = ombreira
		forma.position = Vector3(lado * (LARGURA / 2.0 + 0.06), ALTURA / 2.0, 0.0)
		corpo.add_child(forma)


func _montar_placa() -> void:
	if texto_da_placa.is_empty():
		return
	for lado: float in [-1.0, 1.0]:
		var placa := Label3D.new()
		placa.text = texto_da_placa
		placa.font = load("res://cenas/interface/fonte_jogo.tres")
		placa.font_size = 16
		placa.outline_size = 0
		placa.pixel_size = 0.0105
		placa.modulate = Color(0.95, 0.42, 0.25, 1.0)
		placa.position = Vector3(0.0, ALTURA + 0.2, lado * (PROFUNDIDADE / 2.0 + 0.02))
		placa.rotation.y = 0.0 if lado > 0.0 else PI
		add_child(placa)


func _atualizar_luz() -> void:
	var cor := COR_TRANCADA if trancada else COR_LIVRE
	_luz.albedo_color = cor * 0.4
	_luz.emission = cor
