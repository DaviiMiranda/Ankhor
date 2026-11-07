extends "res://scripts/visor/texturas_do_quarto.gd"

const PASTA_MENU := "res://assets/sprites/menu/notebook/%s_%s.png"
const MATERIAIS_MENU := {
	"Tampo": ["madeira", 0.7, 1.0, 0.0],
	"Madeira": ["madeira", 0.4, 0.85, 0.0],
	"MadeiraEscura": ["madeira", 0.4, 0.48, 0.0],
	"Parede": ["parede", 1.0, 1.0, 0.0],
	"Cortina": ["tecido", 0.3, 1.0, 0.0],
	"MetalNotebook": ["metal", 0.18, 1.0, 0.65],
	"PlasticoNotebook": ["metal", 0.18, 0.42, 0.0],
	"TeclasNotebook": ["metal", 0.05, 0.36, 0.0],
}

var _materiais_detalhados := {}


func _ready() -> void:
	super._ready()
	for malha: MeshInstance3D in modelo.find_children("*", "MeshInstance3D", true, false):
		for superficie in malha.mesh.get_surface_count():
			var original := malha.mesh.surface_get_material(superficie)
			if original and MATERIAIS_MENU.has(original.resource_name):
				malha.set_surface_override_material(superficie, _material_detalhado(original.resource_name))


func _material_detalhado(nome: String) -> StandardMaterial3D:
	if _materiais_detalhados.has(nome):
		return _materiais_detalhados[nome]
	var dados: Array = MATERIAIS_MENU[nome]
	var material := StandardMaterial3D.new()
	var intensidade: float = dados[2]
	material.albedo_color = Color(intensidade, intensidade, intensidade)
	material.albedo_texture = load(PASTA_MENU % [dados[0], "cor"])
	material.roughness_texture = load(PASTA_MENU % [dados[0], "rugosidade"])
	material.roughness_texture_channel = BaseMaterial3D.TEXTURE_CHANNEL_RED
	material.metallic = dados[3]
	material.normal_enabled = true
	material.normal_texture = load(PASTA_MENU % [dados[0], "normal"])
	material.normal_scale = 0.3
	material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST_WITH_MIPMAPS
	material.uv1_triplanar = true
	material.uv1_world_triplanar = true
	material.uv1_scale = Vector3.ONE / float(dados[1])
	_materiais_detalhados[nome] = material
	return material
