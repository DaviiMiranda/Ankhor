class_name Gabriel
extends CharacterBody2D

signal passo_dado(correndo: bool)
signal fadiga_mudou(estamina: float, maxima: float)
signal exaustao_mudou(esta_exausto: bool)
signal ansiedade_mudou(valor: float, maxima: float)
signal tira_especial_mudou

const COR_ESCONDIDO := Color(0.45, 0.45, 0.6)
const LARGURA_QUADRO := 96.0
const SETORES_OLHAR := 8
const MAOS := preload("res://scripts/personagens/maos_do_gabriel.gd").MAOS
const MAOS_CORRENDO := preload("res://scripts/personagens/maos_correndo_gabriel.gd").MAOS_CORRENDO
const CENA_ANSIEDADE := preload("res://cenas/sistemas/ansiedade.tscn")
const PEITO_NO_QUADRO := {
	"lado": Vector2(54, 40),
	"frente": Vector2(47, 40),
	"tres_quartos": Vector2(44, 40),
	"costas": Vector2(47, 40),
	"tres_quartos_costas": Vector2(45, 40),
}

@export var velocidade_andar: float = 60.0
@export var fator_profundidade: float = 0.65
@export var multiplicador_correr: float = 1.8
@export var multiplicador_exaustao: float = 0.4
@export var forca_empurrao: float = 170.0
@export var segundos_ofegando_depois_da_fuga: float = 3.0

@export_group("Conducao")
@export var aceleracao_inicial: float = 640.0
@export var aceleracao_final: float = 300.0
@export var aceleracao_corrida: float = 240.0
@export var desaceleracao: float = 760.0
@export var taxa_virada: float = 1600.0
@export var margem_virada_graus: float = 8.0
@export var segundos_para_virar: float = 0.06

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
@export var px_por_quadro_correndo: float = 5.0
@export var quadros_por_segundo_assentando: float = 36.0
@export var balanco_andar: float = 0.5
@export var inclinacao_andando: float = 0.03
@export var inclinacao_freando: float = 0.12
@export var rapidez_inclinacao: float = 20.0

@export_group("Corrida")
@export var correr_lado: Texture2D
@export var correr_frente: Texture2D
@export var correr_tres_quartos: Texture2D
@export var correr_costas: Texture2D
@export var correr_tres_quartos_costas: Texture2D
@export var quadros_correr: int = 24
@export var fracao_para_tira_de_correr: float = 0.3

@export_group("Parado")
@export var parado_lado: Texture2D
@export var parado_frente: Texture2D
@export var parado_tres_quartos: Texture2D
@export var parado_costas: Texture2D
@export var parado_tres_quartos_costas: Texture2D
@export var quadros_parado: int = 8
@export var segundos_por_quadro_parado: float = 0.3

var jogador_controla := true
var mirando := false
var direcao_automatica := Vector2.ZERO
var correr_sozinho := false
var estamina_infinita := false
var correndo := false
var escondido := false
var tira_especial := false

var vista := "lado"
var direcao_olhar := Vector2.RIGHT
var _empurrao := Vector2.ZERO
var _velocidade_propria := Vector2.ZERO
var _setor_olhar := 0
var _tempo_mudando_olhar := 0.0
var _fase_passada := 0.0
var _tempo_parado := 0.0
var _passos := 0
var _tira_da_mao := "imovel"
var _mascara_colisao := 0
var _segundos_ofegando := 0.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var no_gadgets: Node2D = $Gadgets
@onready var fadiga: Fadiga = $Fadiga
var ansiedade: Ansiedade
var acao_demorada: AcaoDemorada


func _ready() -> void:
	motion_mode = CharacterBody2D.MOTION_MODE_FLOATING
	add_to_group("jogador")
	ansiedade = CENA_ANSIEDADE.instantiate() as Ansiedade
	add_child(ansiedade)
	ansiedade.mudou.connect(_ao_mudar_ansiedade)
	acao_demorada = AcaoDemorada.new()
	add_child(acao_demorada)
	add_child(ItensLargados.new())
	add_child(ZumbidoDaCarga.new())
	Inventario.mudou.connect(_atualizar_gadgets)
	Vida.dano_recebido.connect(_ao_receber_dano)
	if fadiga:
		fadiga.mudou.connect(_ao_mudar_fadiga)
		fadiga.exaustao_iniciada.connect(_ao_iniciar_exaustao)
		fadiga.exaustao_terminada.connect(_ao_terminar_exaustao)
	_atualizar_gadgets()


func _unhandled_input(evento: InputEvent) -> void:
	if not jogador_controla:
		return
	if evento.is_action_pressed("interagir"):
		var alvo := Interagivel.mais_perto(get_tree(), global_position)
		if alvo:
			if alvo.segundos_de_espera() > 0.0:
				acao_demorada.comecar(alvo)
			else:
				alvo.interagir()
			get_viewport().set_input_as_handled()
	if evento.is_action_pressed("largar"):
		_largar_carga()
	for i in Inventario.ESPACOS_GADGET:
		if evento.is_action_pressed("gadget_%d" % (i + 1)):
			usar_gadget(i)


func _largar_carga() -> void:
	var item := Inventario.item_pesado()
	if item:
		ItensLargados.soltar(get_tree(), item, global_position)
		Inventario.aviso.emit("%s no chão. E para pegar de novo." % item.nome)


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

	if mirando:
		direcao = Vector2.ZERO
	correndo = false
	var velocidade := velocidade_andar
	var pode_correr := (fadiga.pode_correr() if fadiga else true) and not Inventario.carregando_peso()
	var quer_correr := correr_sozinho or (jogador_controla and Input.is_action_pressed("correr"))
	if quer_correr and direcao != Vector2.ZERO and (pode_correr or correr_sozinho):
		velocidade *= multiplicador_correr
		correndo = true
		if fadiga and not correr_sozinho and not estamina_infinita:
			fadiga.consumir(delta, ansiedade.multiplicador_consumo_estamina())
	elif fadiga:
		fadiga.regenerar(delta, direcao == Vector2.ZERO)

	if fadiga and fadiga.esta_exausto():
		velocidade *= multiplicador_exaustao

	var alvo := Vector2(direcao.x, direcao.y * fator_profundidade) * velocidade
	_velocidade_propria = _conduzir(alvo, delta)
	velocity = _velocidade_propria + _empurrao
	_empurrao = _empurrao.move_toward(Vector2.ZERO, forca_empurrao * 4.0 * delta)
	move_and_slide()

	_virar_com_folga(direcao, delta)
	if not tira_especial:
		_animar(get_real_velocity().length() * delta, delta)
		_ajustar_corpo(direcao, delta)

	_piscar()
	ansiedade.atualizar(global_position, delta)
	_atualizar_respiracao_de_fuga(delta)


func _atualizar_respiracao_de_fuga(delta: float) -> void:
	if fadiga == null:
		return
	if _algum_robo_perseguindo():
		_segundos_ofegando = segundos_ofegando_depois_da_fuga
	else:
		_segundos_ofegando = maxf(_segundos_ofegando - delta, 0.0)
	fadiga.em_fuga = _segundos_ofegando > 0.0 and not escondido


func _algum_robo_perseguindo() -> bool:
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo and robo.esta_perseguindo():
			return true
	return false


func _conduzir(alvo: Vector2, delta: float) -> Vector2:
	if alvo == Vector2.ZERO:
		return _velocidade_propria.move_toward(Vector2.ZERO, desaceleracao * delta)
	var eixo := alvo.normalized()
	var ao_longo := _velocidade_propria.dot(eixo)
	var de_lado := _velocidade_propria - eixo * ao_longo
	de_lado = de_lado.move_toward(Vector2.ZERO, taxa_virada * delta)
	var taxa := _taxa_ao_longo(ao_longo, alvo.length())
	return eixo * move_toward(ao_longo, alvo.length(), taxa * delta) + de_lado


func _taxa_ao_longo(atual: float, final: float) -> float:
	if atual < 0.0:
		return taxa_virada
	if atual > final:
		return desaceleracao
	if correndo and atual >= final / multiplicador_correr:
		return aceleracao_corrida
	return lerpf(aceleracao_inicial, aceleracao_final, atual / final)


func fracao_de_corrida() -> float:
	var plano := Vector2(_velocidade_propria.x, _velocidade_propria.y / fator_profundidade)
	var maxima := velocidade_andar * multiplicador_correr
	return clampf(inverse_lerp(velocidade_andar, maxima, plano.length()), 0.0, 1.0)


func esconder(sim: bool) -> void:
	escondido = sim
	sprite.self_modulate = COR_ESCONDIDO if sim else Color.WHITE


func posicao_do_peito() -> Vector2:
	var pixel: Vector2 = PEITO_NO_QUADRO[vista]
	var x := pixel.x + 0.5
	if sprite.flip_h:
		x = LARGURA_QUADRO - x
	return sprite.transform * (Vector2(x, pixel.y + 0.5) + sprite.offset)


func posicao_da_mao() -> Vector2:
	var quadros: Array = MAOS_CORRENDO[vista] if _tira_da_mao == "correr" else MAOS[vista][_tira_da_mao]
	return ponto_do_quadro(quadros[mini(sprite.frame, quadros.size() - 1)])


func ponto_do_quadro(pixel: Vector2) -> Vector2:
	var x := pixel.x
	if sprite.flip_h:
		x = LARGURA_QUADRO - x
	return sprite.transform * (Vector2(x, pixel.y) + sprite.offset)


func olhar_para(direcao: Vector2) -> void:
	_virar(direcao)


func tocar_tira(tira: Texture2D, quadros: int) -> void:
	tira_especial = true
	sprite.position = Vector2.ZERO
	sprite.skew = 0.0
	_mostrar(tira, quadros, 0)
	tira_especial_mudou.emit()


func pode_mexer_na_mochila() -> bool:
	return jogador_controla and not tira_especial


func comecar_gesto_da_mochila() -> void:
	_velocidade_propria = Vector2.ZERO
	tocar_tira(GestoMochila.TIRAS[vista], GestoMochila.QUADROS)


func mostrar_quadro_tira(quadro: int) -> void:
	sprite.frame = quadro


func terminar_tira() -> void:
	tira_especial = false
	tira_especial_mudou.emit()


func andar_sozinho(direcao: Vector2) -> void:
	if jogador_controla:
		_mascara_colisao = collision_mask
	jogador_controla = false
	direcao_automatica = direcao
	collision_mask = 0


func devolver_controle() -> void:
	jogador_controla = true
	correr_sozinho = false
	direcao_automatica = Vector2.ZERO
	collision_mask = _mascara_colisao


func _ao_receber_dano(origem: Vector2) -> void:
	_empurrao = (global_position - origem).normalized() * forca_empurrao


func _ao_mudar_fadiga(atual: float, maxima: float) -> void:
	fadiga_mudou.emit(atual, maxima)


func _ao_mudar_ansiedade(atual: float, maxima: float) -> void:
	ansiedade_mudou.emit(atual, maxima)


func _ao_iniciar_exaustao() -> void:
	exaustao_mudou.emit(true)


func _ao_terminar_exaustao() -> void:
	exaustao_mudou.emit(false)


func _piscar() -> void:
	var apagado := Vida.esta_invulneravel() and int(Time.get_ticks_msec() / 90.0) % 2 == 0
	sprite.modulate.a = 0.3 if apagado else 1.0


func _virar(direcao: Vector2) -> void:
	if direcao == Vector2.ZERO:
		return
	direcao_olhar = direcao.normalized()
	_setor_olhar = posmod(roundi(direcao.angle() / TAU * SETORES_OLHAR), SETORES_OLHAR)
	var sentido := Vector2.RIGHT.rotated(_angulo_do_setor()).round()
	if sentido.x == 0.0:
		vista = "frente" if sentido.y > 0.0 else "costas"
	elif sentido.y > 0.0:
		vista = "tres_quartos"
	elif sentido.y < 0.0:
		vista = "tres_quartos_costas"
	else:
		vista = "lado"
	if sentido.x != 0.0:
		sprite.flip_h = sentido.x < 0.0


func _virar_com_folga(direcao: Vector2, delta: float) -> void:
	if direcao == Vector2.ZERO:
		_tempo_mudando_olhar = 0.0
	elif _continua_no_setor(direcao):
		_tempo_mudando_olhar = 0.0
		direcao_olhar = direcao.normalized()
	else:
		_tempo_mudando_olhar += delta
		if _tempo_mudando_olhar >= segundos_para_virar or direcao.dot(direcao_olhar) < 0.0:
			_tempo_mudando_olhar = 0.0
			_virar(direcao)


func _continua_no_setor(direcao: Vector2) -> bool:
	var limite := TAU / SETORES_OLHAR / 2.0 + deg_to_rad(margem_virada_graus)
	return absf(angle_difference(_angulo_do_setor(), direcao.angle())) <= limite


func _angulo_do_setor() -> float:
	return _setor_olhar * TAU / SETORES_OLHAR


func _ajustar_corpo(direcao: Vector2, delta: float) -> void:
	var peso_andando := clampf(_velocidade_propria.length() / velocidade_andar, 0.0, 1.0)
	var balanco := balanco_andar * peso_andando * (1.0 - fracao_de_corrida())
	var pes_juntos := absf(cos(TAU * _fase_passada / quadros_andar))
	sprite.position.y = -snappedf(balanco * pes_juntos, 0.5)
	var rapidez := _velocidade_propria.x / (velocidade_andar * multiplicador_correr)
	var inclinacao := rapidez * inclinacao_andando
	if direcao.x * _velocidade_propria.x <= 0.0:
		inclinacao = -rapidez * inclinacao_freando
	sprite.skew = lerpf(sprite.skew, inclinacao, 1.0 - exp(-rapidez_inclinacao * delta))


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
		_fase_passada += andou / lerpf(px_por_quadro, px_por_quadro_correndo, fracao_de_corrida())
		_mostrar_passada(andando[vista])
		_contar_passos()
	elif andando[vista] and int(_fase_passada) % (quadros_andar / 2) != 0:
		_fase_passada += quadros_por_segundo_assentando * delta
		_mostrar_passada(andando[vista])
	elif respirando[vista]:
		_fase_passada = 0.0
		_passos = 0
		_tempo_parado += delta
		_tira_da_mao = "parado"
		_mostrar(respirando[vista], quadros_parado,
				int(_tempo_parado / segundos_por_quadro_parado) % quadros_parado)
	elif imovel[vista]:
		_fase_passada = 0.0
		_passos = 0
		_tira_da_mao = "imovel"
		_mostrar(imovel[vista], 1, 0)


func _mostrar_passada(tira_de_andar: Texture2D) -> void:
	var correndo_tiras := {"lado": correr_lado, "frente": correr_frente,
			"tres_quartos": correr_tres_quartos, "costas": correr_costas,
			"tres_quartos_costas": correr_tres_quartos_costas}
	var tira: Texture2D = correndo_tiras[vista]
	if tira == null or fracao_de_corrida() <= fracao_para_tira_de_correr:
		_tira_da_mao = "andar"
		_mostrar(tira_de_andar, quadros_andar, int(_fase_passada) % quadros_andar)
	else:
		_tira_da_mao = "correr"
		var quadro := int(_fase_passada * quadros_correr / quadros_andar) % quadros_correr
		_mostrar(tira, quadros_correr, quadro)


func _contar_passos() -> void:
	var quadros_por_passo := quadros_andar / 2.0
	var passos := int((_fase_passada + quadros_por_passo / 2.0) / quadros_por_passo)
	if passos > _passos:
		_passos = passos
		passo_dado.emit(correndo)


func _mostrar(tira: Texture2D, quadros: int, quadro: int) -> void:
	sprite.frame = 0
	sprite.texture = tira
	sprite.hframes = quadros
	sprite.frame = quadro
