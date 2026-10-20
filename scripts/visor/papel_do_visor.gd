class_name PapelDoVisor
extends Node3D

const FONTE := preload("res://cenas/interface/fonte_jogo.tres")
const COR_DESTAQUE := Color(0.25, 0.85, 0.95)
const BORDA_DESTAQUE := 0.02
const ALTURA_DESTACADO := 0.012
const LARGURA_DO_TEXTO := 0.84

var documento: Documento

var _destaque: MeshInstance3D
var _altura_normal := 0.0


func montar(textura: Texture2D, titulo: String, tinta: Color, tamanho: Vector2, pixel_do_texto: float) -> void:
	_altura_normal = position.z
	add_child(_folha(textura, tamanho))
	_destaque = _retangulo(tamanho + Vector2.ONE * BORDA_DESTAQUE, COR_DESTAQUE)
	_destaque.position.z = -0.001
	_destaque.visible = false
	add_child(_destaque)
	add_child(_rotulo(titulo, tinta, tamanho.x * LARGURA_DO_TEXTO / pixel_do_texto, pixel_do_texto))


func destacar(sim: bool) -> void:
	_destaque.visible = sim
	position.z = _altura_normal + (ALTURA_DESTACADO if sim else 0.0)


func _folha(textura: Texture2D, tamanho: Vector2) -> MeshInstance3D:
	var folha := _retangulo(tamanho, Color.WHITE)
	var material := folha.material_override as StandardMaterial3D
	material.albedo_texture = textura
	material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	return folha


func _retangulo(tamanho: Vector2, cor: Color) -> MeshInstance3D:
	var plano := QuadMesh.new()
	plano.size = tamanho
	var material := StandardMaterial3D.new()
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.albedo_color = cor
	var malha := MeshInstance3D.new()
	malha.mesh = plano
	malha.material_override = material
	return malha


func _rotulo(texto: String, tinta: Color, largura_em_pixels: float, pixel_do_texto: float) -> Label3D:
	var rotulo := Label3D.new()
	rotulo.font = FONTE
	rotulo.font_size = 8
	rotulo.pixel_size = pixel_do_texto
	rotulo.text = texto
	rotulo.modulate = tinta
	rotulo.outline_size = 0
	rotulo.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	rotulo.width = largura_em_pixels
	rotulo.double_sided = false
	rotulo.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	rotulo.alpha_cut = Label3D.ALPHA_CUT_DISCARD
	rotulo.position.z = 0.002
	return rotulo
