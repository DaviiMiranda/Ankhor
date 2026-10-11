class_name Robo
extends CharacterBody2D

signal jogador_detectado(robo: Robo)
signal jogador_perdido(robo: Robo)
signal estado_mudou(robo: Robo, novo_estado: Estado)

enum Estado { PATRULHA, INVESTIGANDO, PERSEGUINDO, PROCURANDO, ATACOU, ATORDOADO }

const CAMADA_PAREDES := 8
const ALCANCE_SOM_CORRENDO := 14
const ALCANCE_SOM_ANDANDO := 5
const INTERVALO_NOVO_CAMINHO := 0.35
const DISTANCIA_CHEGOU := 4.0
const ORIGEM_DA_SOMBRA := Vector2(0, -4)
const RAIO_LUZ_QUE_REVELA := 56.0
const SOM_BIPE := preload("res://assets/audio/efeitos/robos/robo_bipe.wav")

@export var nome_tipo: String = "Robô"

@export_group("Movimento")
@export var velocidade_patrulha: float = 24.0
@export var velocidade_investigando: float = 34.0
@export var velocidade_perseguicao: float = 50.0
@export var fator_profundidade: float = 0.8
@export var giro_olhar: float = 6.0

@export_group("Visão")
@export var alcance_visao: float = 140.0
@export var angulo_visao: float = 70.0
@export var fator_lanterna: float = 1.6
@export var alcance_sentir: float = 20.0

@export_group("Audição")
@export var fator_audicao: float = 1.0

@export_group("Gadgets")
@export var fator_clarao: float = 1.0

@export_group("Rota")
@export var rota: NodePath
@export var rota_com_marca: NodePath
@export var marca_da_rota: String = "energia"
@export var pausa_no_ponto: float = 1.4
@export var bipa_antes_de_virar := false

@export_group("Memória")
@export var segundos_memoria: float = 1.5
@export var segundos_olhando_em_volta: float = 2.5
@export var segundos_procurando: float = 4.0
@export var segundos_depois_do_ataque: float = 1.3

@export_group("Sprites")
@export var andar_lado: Texture2D
@export var andar_frente: Texture2D
@export var andar_costas: Texture2D
@export var olhos_lado: Texture2D
@export var olhos_frente: Texture2D
@export var olhos_costas: Texture2D
@export var quadros: int = 8
@export var px_por_quadro: float = 4.0
@export var px_por_passo: float = 16.0

@export_group("Testa")
@export var testa_lado := Vector2(19, -54)
@export var testa_frente := Vector2(0, -55)
@export var testa_costas := Vector2(0, -53)

var estado: Estado = Estado.PATRULHA
var grade: GradeLabirinto
var direcao_olhar := Vector2.RIGHT

var _gabriel: Gabriel
var _caminho := PackedVector2Array()
var _destino := Vector2.ZERO
var _salinha := Vector2i.ZERO
var _salinha_anterior := Vector2i(-1, -1)
var _ultima_vista := Vector2.ZERO
var _tempo_sem_ver := 0.0
var _tempo_no_estado := 0.0
var _tempo_novo_caminho := 0.0
var _tempo_parado := 0.0
var _tempo_desde_chegada := 0.0
var _distancia := 0.0
var _passos := 0
var _segundos_atordoado := 0.0
var _vista := "lado"
var _sorteio := RandomNumberGenerator.new()
var _indice_rota := -1
var _bipou := false
var _som_bipe: AudioStreamPlayer2D

@onready var sprite: Sprite2D = $Sprite2D
@onready var olhos: Sprite2D = $Olhos
@onready var farol: PointLight2D = get_node_or_null("Farol")
@onready var luz_olho: PointLight2D = get_node_or_null("LuzOlho")
@onready var garra: Area2D = $Garra
@onready var som_passo: AudioStreamPlayer2D = $Passos
@onready var som_alerta: AudioStreamPlayer2D = $Alerta


func configurar(nova_grade: GradeLabirinto, semente: int) -> void:
	grade = nova_grade
	_sorteio.seed = semente
	_salinha = grade.salinha(global_position)
	_indice_rota = _indice_do_ponto_mais_perto() - 1
	Progresso.mudou.connect(_ao_mudar_progresso)
	_patrulhar()


func _ready() -> void:
	motion_mode = CharacterBody2D.MOTION_MODE_FLOATING
	add_to_group("robos")
	_gabriel = get_tree().get_first_node_in_group("jogador") as Gabriel
	if _gabriel:
		_gabriel.passo_dado.connect(_ao_ouvir_passo)
	if bipa_antes_de_virar:
		_som_bipe = AudioStreamPlayer2D.new()
		_som_bipe.stream = SOM_BIPE
		_som_bipe.bus = &"Efeitos"
		_som_bipe.max_distance = 360.0
		add_child(_som_bipe)
	_mostrar_quadro()


func _physics_process(delta: float) -> void:
	if grade == null:
		return
	_tempo_no_estado += delta
	_decidir(delta)
	_andar(delta)
	_tentar_atacar()
	_animar(delta)


func _decidir(delta: float) -> void:
	var vendo := estado != Estado.ATORDOADO and _ve_o_jogador()
	match estado:
		Estado.PATRULHA, Estado.INVESTIGANDO, Estado.PROCURANDO:
			if vendo:
				_perseguir()
		Estado.PERSEGUINDO:
			if vendo:
				_ultima_vista = _gabriel.global_position
				_tempo_sem_ver = 0.0
			else:
				_tempo_sem_ver += delta
				if _tempo_sem_ver > segundos_memoria:
					_procurar()
			_tempo_novo_caminho -= delta
			if _tempo_novo_caminho <= 0.0:
				_tempo_novo_caminho = INTERVALO_NOVO_CAMINHO
				_ir_para(_ultima_vista)
		Estado.ATACOU:
			if _tempo_no_estado > segundos_depois_do_ataque:
				if vendo:
					_perseguir()
				else:
					_procurar()
		Estado.ATORDOADO:
			if _tempo_no_estado > _segundos_atordoado:
				_ultima_vista = global_position
				_procurar()


func _mudar_estado(novo: Estado) -> void:
	estado = novo
	_tempo_no_estado = 0.0
	estado_mudou.emit(self, novo)


func _patrulhar() -> void:
	_mudar_estado(Estado.PATRULHA)
	_bipou = false
	var pontos := _pontos_da_rota()
	if not pontos.is_empty():
		_indice_rota = posmod(_indice_rota + 1, pontos.size())
		_ir_para(pontos[_indice_rota])
		return
	var proxima := grade.proxima_salinha(_salinha, _salinha_anterior, _sorteio)
	_salinha_anterior = _salinha
	_salinha = proxima
	_ir_para(grade.centro_salinha(proxima))


func atordoar(segundos: float) -> void:
	if grade == null:
		return
	if estado == Estado.PERSEGUINDO or estado == Estado.ATACOU:
		jogador_perdido.emit(self)
	_segundos_atordoado = segundos
	_caminho.clear()
	velocity = Vector2.ZERO
	_mudar_estado(Estado.ATORDOADO)


func pode_ser_hackeado_de(ponto: Vector2) -> bool:
	if estado == Estado.ATORDOADO:
		return true
	if estado == Estado.PERSEGUINDO or estado == Estado.ATACOU:
		return false
	return direcao_olhar.dot(global_position.direction_to(ponto)) < 0.0


func ouvir_barulho(origem: Vector2, alcance_base: int) -> void:
	if grade == null or estado in [Estado.PERSEGUINDO, Estado.ATACOU, Estado.ATORDOADO]:
		return
	var alcance := int(alcance_base * fator_audicao)
	if alcance <= 0:
		return
	var ondas := grade.distancias(grade.livre_mais_perto(grade.celula(origem)), alcance)
	if ondas.has(grade.celula(global_position)):
		_investigar(origem)


func _investigar(onde: Vector2) -> void:
	_mudar_estado(Estado.INVESTIGANDO)
	_ir_para(onde)


func _perseguir() -> void:
	var ja_perseguia := estado == Estado.PERSEGUINDO or estado == Estado.ATACOU
	_mudar_estado(Estado.PERSEGUINDO)
	_ultima_vista = _gabriel.global_position
	_tempo_sem_ver = 0.0
	_tempo_novo_caminho = 0.0
	if not ja_perseguia:
		som_alerta.play()
		jogador_detectado.emit(self)


func _procurar() -> void:
	_mudar_estado(Estado.PROCURANDO)
	_ir_para(_ultima_vista)


func _desistir() -> void:
	jogador_perdido.emit(self)
	_salinha = grade.salinha(global_position)
	_salinha_anterior = Vector2i(-1, -1)
	_indice_rota = _indice_do_ponto_mais_perto() - 1
	_patrulhar()


func _pontos_da_rota() -> PackedVector2Array:
	var caminho := rota
	if not rota_com_marca.is_empty() and Progresso.tem(marca_da_rota):
		caminho = rota_com_marca
	var pontos := PackedVector2Array()
	var no := get_node_or_null(caminho) if not caminho.is_empty() else null
	if no == null:
		return pontos
	for filho in no.get_children():
		if filho is Node2D:
			pontos.append(filho.global_position)
	return pontos


func _indice_do_ponto_mais_perto() -> int:
	var pontos := _pontos_da_rota()
	var melhor := 0
	for i in pontos.size():
		if global_position.distance_squared_to(pontos[i]) < global_position.distance_squared_to(pontos[melhor]):
			melhor = i
	return melhor


func _ao_mudar_progresso(marca: String) -> void:
	if marca != marca_da_rota or rota_com_marca.is_empty() or estado != Estado.PATRULHA:
		return
	_indice_rota = _indice_do_ponto_mais_perto() - 1
	_patrulhar()


func _ir_para(alvo: Vector2) -> void:
	_destino = alvo
	_caminho = grade.caminho(global_position, alvo)
	_tempo_desde_chegada = 0.0


func _ao_chegar() -> void:
	match estado:
		Estado.PATRULHA:
			if _pontos_da_rota().is_empty():
				if _tempo_desde_chegada > 0.4:
					_patrulhar()
				return
			if _som_bipe and not _bipou and _tempo_desde_chegada > pausa_no_ponto - 0.6:
				_bipou = true
				_som_bipe.play()
			if _tempo_desde_chegada > pausa_no_ponto:
				_patrulhar()
		Estado.INVESTIGANDO:
			if _tempo_desde_chegada > segundos_olhando_em_volta:
				_salinha = grade.salinha(global_position)
				_patrulhar()
		Estado.PROCURANDO:
			if _tempo_desde_chegada > segundos_procurando:
				_desistir()


func _velocidade() -> float:
	match estado:
		Estado.PERSEGUINDO:
			return velocidade_perseguicao
		Estado.INVESTIGANDO, Estado.PROCURANDO:
			return velocidade_investigando
		Estado.ATACOU, Estado.ATORDOADO:
			return 0.0
	return velocidade_patrulha


func _andar(delta: float) -> void:
	while not _caminho.is_empty() and global_position.distance_to(_caminho[0]) < DISTANCIA_CHEGOU:
		_caminho.remove_at(0)
	if _caminho.is_empty():
		velocity = Vector2.ZERO
		if estado == Estado.PERSEGUINDO:
			if _ve_o_jogador():
				velocity = _para_o_gabriel() * _velocidade()
				_virar_para(velocity.normalized(), delta)
		elif estado != Estado.ATACOU and estado != Estado.ATORDOADO:
			_tempo_desde_chegada += delta
			_olhar_em_volta(delta)
			_ao_chegar()
		move_and_slide()
		return
	var direcao := global_position.direction_to(_caminho[0])
	velocity = Vector2(direcao.x, direcao.y * fator_profundidade) * _velocidade()
	if velocity.length() > 1.0:
		_virar_para(direcao, delta)
	move_and_slide()
	_evitar_ficar_preso(delta)


func _para_o_gabriel() -> Vector2:
	var direcao := global_position.direction_to(_gabriel.global_position)
	return Vector2(direcao.x, direcao.y * fator_profundidade)


func _evitar_ficar_preso(delta: float) -> void:
	if velocity.length() > 5.0 and get_real_velocity().length() < 2.0:
		_tempo_parado += delta
		if _tempo_parado > 0.6:
			_tempo_parado = 0.0
			if not _caminho.is_empty():
				_caminho.remove_at(0)
	else:
		_tempo_parado = 0.0


func _virar_para(direcao: Vector2, delta: float) -> void:
	var angulo := lerp_angle(direcao_olhar.angle(), direcao.angle(), clampf(giro_olhar * delta, 0.0, 1.0))
	direcao_olhar = Vector2.from_angle(angulo)


func _olhar_em_volta(delta: float) -> void:
	direcao_olhar = direcao_olhar.rotated(delta * 1.6 * sin(_tempo_desde_chegada * 1.3))


func _ve_o_jogador() -> bool:
	if _gabriel == null or not Vida.esta_viva():
		return false
	var para := _gabriel.global_position - global_position
	var distancia := para.length()
	if distancia <= alcance_sentir:
		return true
	var alcance := alcance_visao
	if _lanterna_acesa() or _jogador_iluminado():
		alcance *= fator_lanterna
	if distancia > alcance:
		return false
	if direcao_olhar.dot(para / distancia) < cos(deg_to_rad(angulo_visao / 2.0)):
		return false
	return _linha_livre(_gabriel.global_position)


func _linha_livre(ate: Vector2) -> bool:
	var altura := Vector2(0, -4)
	var consulta := PhysicsRayQueryParameters2D.create(global_position + altura, ate + altura, CAMADA_PAREDES)
	return get_world_2d().direct_space_state.intersect_ray(consulta).is_empty()


func _lanterna_acesa() -> bool:
	return Inventario.estado_de("lanterna").get("aceso", false) or Inventario.estado_de("notebook").get("aceso", false)


func _jogador_iluminado() -> bool:
	for luz in get_tree().get_nodes_in_group(VisivelComMarca.GRUPO_LUZ_QUE_REVELA):
		var no := luz as Node2D
		if no and no.is_visible_in_tree() and no.global_position.distance_to(_gabriel.global_position) < RAIO_LUZ_QUE_REVELA:
			return true
	return false


func _ao_ouvir_passo(correndo: bool) -> void:
	ouvir_barulho(_gabriel.global_position, ALCANCE_SOM_CORRENDO if correndo else ALCANCE_SOM_ANDANDO)


func _tentar_atacar() -> void:
	if estado == Estado.ATACOU or estado == Estado.ATORDOADO or _gabriel == null or not garra.overlaps_body(_gabriel):
		return
	if Vida.receber_dano(1, global_position):
		if estado != Estado.PERSEGUINDO:
			jogador_detectado.emit(self)
		_ultima_vista = _gabriel.global_position
		_mudar_estado(Estado.ATACOU)


func _animar(delta: float) -> void:
	var movimento := get_real_velocity()
	if movimento.length() > 1.0:
		if absf(movimento.x) >= absf(movimento.y) * 1.2:
			_vista = "lado"
			sprite.flip_h = movimento.x < 0.0
		elif movimento.y > 0.0:
			_vista = "frente"
		else:
			_vista = "costas"
		_distancia += movimento.length() * delta
		var passos := int(_distancia / px_por_passo)
		if passos > _passos:
			_passos = passos
			som_passo.pitch_scale = _sorteio.randf_range(0.9, 1.1)
			som_passo.play()
	_mostrar_quadro()
	_luzes_na_testa()
	_apagar_se_atordoado()


func _apagar_se_atordoado() -> void:
	var ligado := estado != Estado.ATORDOADO
	olhos.visible = ligado
	if farol:
		farol.visible = ligado
	if luz_olho:
		luz_olho.visible = ligado


func _luzes_na_testa() -> void:
	var testa: Vector2 = {"lado": testa_lado, "frente": testa_frente, "costas": testa_costas}[_vista]
	if _vista == "lado" and sprite.flip_h:
		testa.x = -testa.x
	if luz_olho:
		luz_olho.position = testa
	if farol:
		farol.position = ORIGEM_DA_SOMBRA
		farol.rotation = direcao_olhar.angle()
		farol.offset = (testa - farol.position).rotated(-farol.rotation)


func _mostrar_quadro() -> void:
	var corpos := {"lado": andar_lado, "frente": andar_frente, "costas": andar_costas}
	var brilhos := {"lado": olhos_lado, "frente": olhos_frente, "costas": olhos_costas}
	var quadro := int(_distancia / px_por_quadro) % quadros
	for par in [[sprite, corpos[_vista]], [olhos, brilhos[_vista]]]:
		var alvo: Sprite2D = par[0]
		alvo.frame = 0
		alvo.texture = par[1]
		alvo.hframes = quadros
		alvo.frame = quadro
	olhos.flip_h = sprite.flip_h
