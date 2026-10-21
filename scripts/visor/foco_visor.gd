class_name FocoVisor
extends Node3D

signal leitura_pedida(documento: Documento)

const GRUPO := "focos_do_visor"

@export var texto_acao: String = "Olhar"
@export var dica_focado: String = "Esc: afastar"
@export var tamanho := Vector2(1.0, 1.0)
@export var alcance: float = 1.5
@export var ocupacao: float = 0.85


func _ready() -> void:
	add_to_group(GRUPO)


func centro() -> Vector3:
	return global_position


func frente() -> Vector3:
	return global_basis.z.normalized()


func cima() -> Vector3:
	return global_basis.y.normalized()


func camera_diante(campo_de_visao: float, proporcao: float) -> Transform3D:
	var altura_vista := maxf(tamanho.y, tamanho.x / proporcao) / ocupacao
	var distancia := altura_vista / (2.0 * tan(deg_to_rad(campo_de_visao) / 2.0))
	return Transform3D(Basis(), centro() + frente() * distancia).looking_at(centro(), cima())


func focar() -> void:
	pass


func soltar() -> void:
	pass


func receber(_evento: InputEvent) -> void:
	pass
