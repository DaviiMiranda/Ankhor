class_name JogadorVisor
extends CharacterBody3D

@export var velocidade: float = 1.8
@export var sensibilidade: float = 0.0025
@export var limite_olhar_graus: float = 80.0

var controlando := true

@onready var cabeca: Node3D = $Cabeca
@onready var camera: Camera3D = $Cabeca/Camera3D


func girar(movimento_do_mouse: Vector2) -> void:
	if not controlando:
		return
	rotate_y(-movimento_do_mouse.x * sensibilidade)
	var limite := deg_to_rad(limite_olhar_graus)
	cabeca.rotation.x = clampf(cabeca.rotation.x - movimento_do_mouse.y * sensibilidade, -limite, limite)


func direcao_do_olhar() -> Vector3:
	return -camera.global_basis.z


func _physics_process(delta: float) -> void:
	var entrada := Vector2.ZERO
	if controlando:
		entrada = Input.get_vector("mover_esquerda", "mover_direita", "mover_cima", "mover_baixo")
	var direcao := global_basis * Vector3(entrada.x, 0.0, entrada.y)
	velocity.x = direcao.x * velocidade
	velocity.z = direcao.z * velocidade
	if is_on_floor():
		velocity.y = 0.0
	else:
		velocity += get_gravity() * delta
	move_and_slide()
