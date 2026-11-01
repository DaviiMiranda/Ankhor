class_name CascoDoCorredor
extends Node3D

const PASTA := "res://assets/sprites/cenario/hora_morta/%s.png"
const COMPRIMENTO_DO_VAO := 2.0
const VAOS := 12
const LARGURA := 1.7
const ALTURA := 2.25
const ESPESSURA := 0.2
const PEITORIL := 0.95
const VERGA := 1.75
const LARGURA_DA_JANELA := 1.3
const PROFUNDIDADE_DA_COSTELA := 0.1
const COR_DA_LAMPADA := Color(0.72, 0.84, 1.0)
const ESTADOS_DAS_LAMPADAS: Array[int] = [
	LampadaDaNave.Estado.ACESA,
	LampadaDaNave.Estado.QUEBRADA,
	LampadaDaNave.Estado.ACESA,
	LampadaDaNave.Estado.MORTA,
	LampadaDaNave.Estado.ACESA,
	LampadaDaNave.Estado.QUEBRADA,
]
const POSICOES_DAS_LAMPADAS: Array[float] = [10.0, 6.0, 2.0, -2.0, -6.0, -10.0]
const CAIXAS: Array[Dictionary] = [
	{"lugar": Vector3(-0.52, 0.4, 7.4), "tamanho": Vector3(0.5, 0.8, 0.9)},
	{"lugar": Vector3(0.52, 0.3, 3.9), "tamanho": Vector3(0.5, 0.6, 0.7)},
	{"lugar": Vector3(-0.54, 0.35, -3.6), "tamanho": Vector3(0.46, 0.7, 1.1)},
	{"lugar": Vector3(0.5, 0.45, -7.7), "tamanho": Vector3(0.54, 0.9, 0.8)},
]

var lampadas: Array[LampadaDaNave] = []
var _parede: StandardMaterial3D
var _chao: StandardMaterial3D
var _teto: StandardMaterial3D
var _porta: StandardMaterial3D
var _estrutura: StandardMaterial3D
var _caixa: StandardMaterial3D
var _vidro: StandardMaterial3D


func _ready() -> void:
	_criar_materiais()
	_montar_piso_e_teto()
	_montar_parede_cega()
	_montar_paredes_com_janelas()
	_montar_costelas()
	_montar_portas()
	_montar_caixas()
	_montar_lampadas()
	_montar_colisao()


func _criar_materiais() -> void:
	_parede = _metal("parede_nave", 1.2)
	_chao = _metal("chao_grade", 0.8)
	_teto = _metal("teto_nave", 1.2)
	_porta = _metal("porta_nave", 1.5)
	_estrutura = _metal("parede_nave", 0.6, Color(0.52, 0.55, 0.6))
	_caixa = _metal("parede_nave", 0.7, Color(0.68, 0.55, 0.36))
	_vidro = StandardMaterial3D.new()
	_vidro.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	_vidro.albedo_color = Color(0.45, 0.6, 0.8, 0.07)
	_vidro.roughness = 0.1


func _metal(nome: String, metros: float, tinta: Color = Color.WHITE) -> StandardMaterial3D:
	var material := StandardMaterial3D.new()
	material.albedo_texture = load(PASTA % nome)
	material.albedo_color = tinta
	material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	material.uv1_triplanar = true
	material.uv1_world_triplanar = true
	material.uv1_scale = Vector3.ONE / metros
	material.roughness = 0.6
	material.metallic = 0.2
	return material


func _montar_piso_e_teto() -> void:
	var comprimento := COMPRIMENTO_DO_VAO * VAOS
	var largura_externa := LARGURA + ESPESSURA * 2.0
	_bloco(Vector3(largura_externa, ESPESSURA, comprimento), Vector3(0.0, -ESPESSURA / 2.0, 0.0), _chao)
	_bloco(Vector3(largura_externa, ESPESSURA, comprimento), Vector3(0.0, ALTURA + ESPESSURA / 2.0, 0.0), _teto)
	_bloco(Vector3(0.34, 0.14, comprimento), Vector3(-0.42, ALTURA - 0.07, 0.0), _estrutura)


func _montar_parede_cega() -> void:
	var comprimento := COMPRIMENTO_DO_VAO * VAOS
	var x := -(LARGURA + ESPESSURA) / 2.0
	_bloco(Vector3(ESPESSURA, ALTURA, comprimento), Vector3(x, ALTURA / 2.0, 0.0), _parede)
	var encanamento := -LARGURA / 2.0 + 0.05
	_bloco(Vector3(0.1, 0.1, comprimento), Vector3(encanamento, 0.42, 0.0), _estrutura)
	_bloco(Vector3(0.07, 0.07, comprimento), Vector3(encanamento, 0.56, 0.0), _estrutura)
	_bloco(Vector3(0.08, 0.08, comprimento), Vector3(encanamento, 1.94, 0.0), _estrutura)


func _montar_paredes_com_janelas() -> void:
	for vao in VAOS:
		_montar_vao_com_janela(_centro_do_vao(vao))


func _montar_vao_com_janela(z: float) -> void:
	var x := (LARGURA + ESPESSURA) / 2.0
	var vao := COMPRIMENTO_DO_VAO
	var abertura := VERGA - PEITORIL
	var ombreira := (vao - LARGURA_DA_JANELA) / 2.0
	_bloco(Vector3(ESPESSURA, PEITORIL, vao), Vector3(x, PEITORIL / 2.0, z), _parede)
	_bloco(Vector3(ESPESSURA, ALTURA - VERGA, vao), Vector3(x, (ALTURA + VERGA) / 2.0, z), _parede)
	for lado: float in [-1.0, 1.0]:
		var centro := z + lado * (LARGURA_DA_JANELA + ombreira) / 2.0
		_bloco(Vector3(ESPESSURA, abertura, ombreira), Vector3(x, (PEITORIL + VERGA) / 2.0, centro), _parede)
	var vidro := _bloco(Vector3(0.02, abertura, LARGURA_DA_JANELA), Vector3(x, (PEITORIL + VERGA) / 2.0, z), _vidro)
	vidro.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF


func _montar_costelas() -> void:
	for indice in VAOS + 1:
		var z := COMPRIMENTO_DO_VAO * (float(indice) - float(VAOS) / 2.0)
		var profundidade := PROFUNDIDADE_DA_COSTELA
		for lado: float in [-1.0, 1.0]:
			var x := lado * (LARGURA / 2.0 - profundidade / 2.0)
			_bloco(Vector3(profundidade, ALTURA, 0.16), Vector3(x, ALTURA / 2.0, z), _estrutura)
		_bloco(Vector3(LARGURA, profundidade, 0.16), Vector3(0.0, ALTURA - profundidade / 2.0, z), _estrutura)


func _montar_portas() -> void:
	var z := COMPRIMENTO_DO_VAO * VAOS / 2.0
	for lado: float in [-1.0, 1.0]:
		var lugar := Vector3(0.0, ALTURA / 2.0, lado * (z + ESPESSURA / 2.0))
		_bloco(Vector3(LARGURA + ESPESSURA * 2.0, ALTURA + ESPESSURA * 2.0, ESPESSURA), lugar, _porta)


func _montar_caixas() -> void:
	for caixa in CAIXAS:
		_bloco(caixa["tamanho"], caixa["lugar"], _caixa)


func _montar_lampadas() -> void:
	for indice in POSICOES_DAS_LAMPADAS.size():
		lampadas.append(_nova_lampada(POSICOES_DAS_LAMPADAS[indice], ESTADOS_DAS_LAMPADAS[indice]))


func _nova_lampada(z: float, estado: int) -> LampadaDaNave:
	var material := StandardMaterial3D.new()
	material.albedo_color = Color(0.2, 0.22, 0.26)
	material.emission_enabled = true
	material.emission = COR_DA_LAMPADA
	_bloco(Vector3(0.3, 0.05, 0.7), Vector3(0.2, ALTURA - 0.03, z), material)
	var lampada := LampadaDaNave.new()
	lampada.estado = estado as LampadaDaNave.Estado
	lampada.material_do_vidro = material
	lampada.position = Vector3(0.1, ALTURA - 0.25, z)
	lampada.light_color = COR_DA_LAMPADA
	lampada.light_energy = 1.3
	lampada.omni_range = 3.4
	lampada.omni_attenuation = 1.4
	add_child(lampada)
	return lampada


func _montar_colisao() -> void:
	var corpo := StaticBody3D.new()
	add_child(corpo)
	var comprimento := COMPRIMENTO_DO_VAO * VAOS
	var folga := LARGURA / 2.0 - PROFUNDIDADE_DA_COSTELA + ESPESSURA / 2.0
	_forma(corpo, Vector3(LARGURA * 2.0, ESPESSURA, comprimento + 2.0), Vector3(0.0, -ESPESSURA / 2.0, 0.0))
	_forma(corpo, Vector3(LARGURA * 2.0, ESPESSURA, comprimento + 2.0), Vector3(0.0, ALTURA + ESPESSURA / 2.0, 0.0))
	for lado: float in [-1.0, 1.0]:
		_forma(corpo, Vector3(ESPESSURA, ALTURA, comprimento), Vector3(lado * folga, ALTURA / 2.0, 0.0))
		_forma(corpo, Vector3(LARGURA, ALTURA, ESPESSURA), Vector3(0.0, ALTURA / 2.0, lado * (comprimento + ESPESSURA) / 2.0))
	for caixa in CAIXAS:
		_forma(corpo, caixa["tamanho"], caixa["lugar"])


func _forma(corpo: StaticBody3D, tamanho: Vector3, lugar: Vector3) -> void:
	var caixa := BoxShape3D.new()
	caixa.size = tamanho
	var forma := CollisionShape3D.new()
	forma.shape = caixa
	forma.position = lugar
	corpo.add_child(forma)


func _bloco(tamanho: Vector3, lugar: Vector3, material: Material) -> MeshInstance3D:
	var malha := BoxMesh.new()
	malha.size = tamanho
	var bloco := MeshInstance3D.new()
	bloco.mesh = malha
	bloco.material_override = material
	bloco.position = lugar
	add_child(bloco)
	return bloco


func _centro_do_vao(vao: int) -> float:
	return COMPRIMENTO_DO_VAO * (float(vao) + 0.5 - float(VAOS) / 2.0)
