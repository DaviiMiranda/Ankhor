extends Node

const PASTA := "res://assets/sprites/cenario/visor/%s.png"
const TEXTURAS := {
	"Chao": {"imagem": "piso_madeira", "metros": 0.8, "rugosidade": 0.75},
	"Parede": {"imagem": "parede", "metros": 1.0, "rugosidade": 0.95},
	"Madeira": {"imagem": "madeira", "metros": 0.4, "rugosidade": 0.7},
	"MadeiraEscura": {"imagem": "madeira_escura", "metros": 0.4, "rugosidade": 0.7},
	"Tampo": {"imagem": "tampo_mesa", "metros": 0.7, "rugosidade": 0.55},
	"Porta": {"imagem": "porta", "metros": 0.5, "rugosidade": 0.7},
	"Movel": {"imagem": "movel", "metros": 0.4, "rugosidade": 0.7},
	"Cortica": {"imagem": "cortica", "metros": 0.3, "rugosidade": 1.0},
	"Tapete": {"imagem": "tapete", "metros": 0.5, "rugosidade": 1.0},
	"TapeteBorda": {"imagem": "tapete_borda", "metros": 0.2, "rugosidade": 1.0},
	"Cobertor": {"imagem": "cobertor", "metros": 0.5, "rugosidade": 1.0},
	"Lencol": {"imagem": "lencol", "metros": 0.12, "rugosidade": 0.9},
	"Cortina": {"imagem": "cortina", "metros": 0.25, "rugosidade": 1.0},
	"Quadro": {"imagem": "quadro", "metros": 1.3, "rugosidade": 0.25},
	"Moletom": {"imagem": "moletom", "metros": 0.12, "rugosidade": 0.95},
	"Mochila": {"imagem": "mochila", "metros": 0.08, "rugosidade": 0.9},
	"Papelao": {"imagem": "papelao", "metros": 0.4, "rugosidade": 0.95},
	"Paginas": {"imagem": "paginas", "metros": 0.05, "rugosidade": 0.9},
	"Teclado": {"imagem": "teclado_notebook", "uv": true, "rugosidade": 0.5},
	"TelaNotebook": {"imagem": "tela_notebook", "uv": true, "rugosidade": 0.3, "brilho": 1.1},
	"Despertador": {"imagem": "despertador", "uv": true, "rugosidade": 0.3, "brilho": 1.6},
	"Marcas": {"imagem": "marcas_das_caixas", "uv": true, "rugosidade": 0.9, "recorte": true},
}

@export var modelo: Node3D

var _materiais := {}


func _ready() -> void:
	for malha: MeshInstance3D in modelo.find_children("*", "MeshInstance3D", true, false):
		for superficie in malha.mesh.get_surface_count():
			var original := malha.mesh.surface_get_material(superficie)
			if original and TEXTURAS.has(original.resource_name):
				malha.set_surface_override_material(superficie, _material(original.resource_name))


func _material(nome: String) -> StandardMaterial3D:
	if _materiais.has(nome):
		return _materiais[nome]
	var dados: Dictionary = TEXTURAS[nome]
	var textura: Texture2D = load(PASTA % dados["imagem"])
	var material := StandardMaterial3D.new()
	material.albedo_texture = textura
	material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST_WITH_MIPMAPS
	material.roughness = dados["rugosidade"]
	if not dados.get("uv", false):
		material.uv1_triplanar = true
		material.uv1_world_triplanar = true
		material.uv1_scale = Vector3.ONE / float(dados["metros"])
	if dados.has("brilho"):
		material.emission_enabled = true
		material.emission_texture = textura
		material.emission_energy_multiplier = dados["brilho"]
	if dados.get("recorte", false):
		material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
		material.alpha_scissor_threshold = 0.5
	_materiais[nome] = material
	return material
