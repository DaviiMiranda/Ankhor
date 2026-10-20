class_name TelaDoVisor
extends FocoVisor

@export var tela: MeshInstance3D

@onready var imagem: SubViewport = $Imagem
@onready var menu: MenuVisor = $Imagem/MenuVisor


func _ready() -> void:
	super()
	var caixa := tela.get_aabb()
	tamanho = Vector2(caixa.size.x, caixa.size.y)
	_pintar()


func centro() -> Vector3:
	return tela.global_transform * tela.get_aabb().get_center()


func frente() -> Vector3:
	return (tela.global_basis * Vector3.BACK).normalized()


func cima() -> Vector3:
	return Vector3.UP


func focar() -> void:
	menu.focar()


func soltar() -> void:
	menu.soltar()


func receber(evento: InputEvent) -> void:
	if evento is InputEventKey:
		imagem.push_input(evento)


func _pintar() -> void:
	var material := StandardMaterial3D.new()
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	material.albedo_texture = imagem.get_texture()
	tela.material_override = material
