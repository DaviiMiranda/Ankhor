class_name Gabriel
extends CharacterBody2D

signal passo_dado(correndo: bool)

@export var velocidade_andar: float = 60.0
@export var fator_profundidade: float = 0.65
@export var multiplicador_correr: float = 1.8
@export var forca_empurrao: float = 170.0

@export_group("Sprites")
@export var sprite_lado: Texture2D
@export var sprite_frente: Texture2D
@export var sprite_tres_quartos: Texture2D
@export var sprite_costas: Texture2D
@export var sprite_tres_quartos_costas: Texture2D

@export_group("Caminhada")
@export var andar_lado: Texture2D
@export var andar_frente: Texture2D
@export var andar_tres_quartos: Texture2D
@export var andar_costas: Texture2D
@export var andar_tres_quartos_costas: Texture2D
@export var quadros_andar: int = 12
@export var px_por_quadro: float = 2.8

@export_group("Parado")
@export var parado_lado: Texture2D
@export var parado_frente: Texture2D
@export var parado_tres_quartos: Texture2D
@export var parado_costas: Texture2D
@export var parado_tres_quartos_costas: Texture2D
@export var quadros_parado: int = 8
@export var segundos_por_quadro_parado: float = 0.3

var jogador_controla := true
var direcao_automatica := Vector2.ZERO
var correndo := false

var vista := "lado"
var direcao_olhar := Vector2.RIGHT
var _empurrao := Vector2.ZERO
var _distancia := 0.0
var _tempo_parado := 0.0
var _passos := 0
var _mascara_colisao := 0

@onready var sprite: Sprite2D = $Sprite2D
@onready var no_gadgets: Node2D = $Gadgets


func _ready() -> void:
	motion_mode = CharacterBody2D.MOTION_MODE_FLOATING
	add_to_group("jogador")
	Inventario.mudou.connect(_atualizar_gadgets)
	Vida.dano_recebido.connect(_ao_receber_dano)
	_atualizar_gadgets()


func _unhandled_input(evento: InputEvent) -> void:
	if not jogador_controla:
		return
	if evento.is_action_pressed("interagir"):
		var alvo := Interagivel.mais_perto(get_tree(), global_position)
		if alvo:
			alvo.interagir()
			get_viewport().set_input_as_handled()
	for i in Inventario.ESPACOS_GADGET:
		if evento.is_action_pressed("gadget_%d" % (i + 1)):
			usar_gadget(i)


func usar_gadget(espaco: int) -> void:
	var item: Item = Inventario.gadgets[espaco]
	if item == null:
		return
	var efeito := no_gadgets.get_node_or_null(NodePath(item.id))
	if efeito and efeito.has_method("usar"):
		efeito.usar()


func _atualizar_gadgets() -> void:
	var equipados := {}
	for item in Inventario.gadgets:
		if item != null and item.cena_gadget:
			equipados[item.id] = item
	for efeito in no_gadgets.get_children():
		if not equipados.has(String(efeito.name)):
			if efeito.has_method("ao_desequipar"):
				efeito.ao_desequipar()
			no_gadgets.remove_child(efeito)
			efeito.queue_free()
	for id in equipados:
		if no_gadgets.has_node(NodePath(id)):
			continue
		var efeito := (equipados[id] as Item).cena_gadget.instantiate()
		efeito.name = id
		efeito.set("item", equipados[id])
		no_gadgets.add_child(efeito)


func _physics_process(delta: float) -> void:
	var direcao := direcao_automatica
	if jogador_controla:
		direcao = Input.get_vector("mover_esquerda", "mover_direita", "mover_cima", "mover_baixo")

	correndo = false
	var velocidade := velocidade_andar
	if jogador_controla and Input.is_action_pressed("correr") and direcao != Vector2.ZERO:
		velocidade *= multiplicador_correr
		correndo = true

	velocity = Vector2(direcao.x, direcao.y * fator_profundidade) * velocidade + _empurrao
	_empurrao = _empurrao.move_toward(Vector2.ZERO, forca_empurrao * 4.0 * delta)
	move_and_slide()

	_virar(direcao)
	_animar(get_real_velocity().length() * delta, delta)

	_piscar()


func andar_sozinho(direcao: Vector2) -> void:
	if jogador_controla:
		_mascara_colisao = collision_mask
	jogador_controla = false
	direcao_automatica = direcao
	collision_mask = 0


func devolver_controle() -> void:
	jogador_controla = true
	direcao_automatica = Vector2.ZERO
	collision_mask = _mascara_colisao


func _ao_receber_dano(origem: Vector2) -> void:
	_empurrao = (global_position - origem).normalized() * forca_empurrao


func _piscar() -> void:
	var apagado := Vida.esta_invulneravel() and int(Time.get_ticks_msec() / 90.0) % 2 == 0
	sprite.modulate.a = 0.3 if apagado else 1.0


func _virar(direcao: Vector2) -> void:
	if direcao == Vector2.ZERO:
		return
	direcao_olhar = direcao.normalized()
	if direcao.x == 0.0:
		vista = "frente" if direcao.y > 0.0 else "costas"
	elif direcao.y > 0.0:
		vista = "tres_quartos"
	elif direcao.y < 0.0:
		vista = "tres_quartos_costas"
	else:
		vista = "lado"
	if direcao.x != 0.0:
		sprite.flip_h = direcao.x < 0.0


func _animar(andou: float, delta: float) -> void:
	var andando := {"lado": andar_lado, "frente": andar_frente,
			"tres_quartos": andar_tres_quartos, "costas": andar_costas,
			"tres_quartos_costas": andar_tres_quartos_costas}
	var respirando := {"lado": parado_lado, "frente": parado_frente,
			"tres_quartos": parado_tres_quartos, "costas": parado_costas,
			"tres_quartos_costas": parado_tres_quartos_costas}
	var imovel := {"lado": sprite_lado, "frente": sprite_frente,
			"tres_quartos": sprite_tres_quartos, "costas": sprite_costas,
			"tres_quartos_costas": sprite_tres_quartos_costas}
	if andou > 0.01 and andando[vista]:
		_tempo_parado = 0.0
		_distancia += andou
		_mostrar(andando[vista], quadros_andar, int(_distancia / px_por_quadro) % quadros_andar)
		_contar_passos()
	elif respirando[vista]:
		_distancia = 0.0
		_passos = 0
		_tempo_parado += delta
		_mostrar(respirando[vista], quadros_parado,
				int(_tempo_parado / segundos_por_quadro_parado) % quadros_parado)
	elif imovel[vista]:
		_distancia = 0.0
		_passos = 0
		_mostrar(imovel[vista], 1, 0)


func _contar_passos() -> void:
	var px_por_passo := px_por_quadro * quadros_andar / 2.0
	var passos := int((_distancia + px_por_passo / 2.0) / px_por_passo)
	if passos > _passos:
		_passos = passos
		passo_dado.emit(correndo)


func _mostrar(tira: Texture2D, quadros: int, quadro: int) -> void:
	sprite.frame = 0
	sprite.texture = tira
	sprite.hframes = quadros
	sprite.frame = quadro
