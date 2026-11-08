extends Node2D

enum Fase { OCIOSO, ESTENDENDO, INVADINDO, RECOLHENDO }

const TELA_HACKEAMENTO := preload("res://cenas/interface/tela_hackeamento.tscn")
const MAOS_HACK: Dictionary = preload("res://scripts/personagens/maos_do_zane.gd").MAOS_HACK
const QUADROS := 12
const CAMADA_PAREDES := 8
const FALHAS_PARA_BLOQUEAR := 3
const META_FALHAS := &"falhas_de_hack"
const FOLGA_DO_ALCANCE := 50.0
const ALTURA_DO_ALVO := Vector2(0, -26)
const COR_RAIO := Color(0.35, 0.95, 0.85)
const COR_NUCLEO := Color(0.85, 1.0, 0.95)
const SEGMENTOS_DO_RAIO := 14
const COR_CALOR := Color(1.0, 0.22, 0.1)
const COR_BRASA := Color(1.0, 0.68, 0.32)
const COR_FUMACA := Color(0.62, 0.58, 0.58)
const COR_ROBO_ENERGIZADO := Color(0.6, 1.3, 1.25)
const FAISCAS_NA_MAO := 5
const FAISCAS_NO_ROBO := 8
const FAISCAS_POR_SEGUNDO := 18.0
const AREA_DA_MAO := Vector2(2.5, 2.5)
const AREA_DO_ROBO := Vector2(10.0, 16.0)
const FIOS_DE_FUMACA := 3
const TIRAS := {
	"lado": preload("res://assets/sprites/personagens/zane/zane_hack_lado.png"),
	"frente": preload("res://assets/sprites/personagens/zane/zane_hack_frente.png"),
	"tres_quartos": preload("res://assets/sprites/personagens/zane/zane_hack_tres_quartos.png"),
	"costas": preload("res://assets/sprites/personagens/zane/zane_hack_costas.png"),
	"tres_quartos_costas": preload("res://assets/sprites/personagens/zane/zane_hack_tres_quartos_costas.png"),
}
const DIFICULDADE_POR_ROBO := {
	"Ronda": Hackeamento.Dificuldade.FACIL,
	"Sentinela": Hackeamento.Dificuldade.MEDIO,
	"Mariposa": Hackeamento.Dificuldade.MEDIO,
	"Rastreador": Hackeamento.Dificuldade.DIFICIL,
	"Caçador": Hackeamento.Dificuldade.DIFICIL,
	"Escafandro": Hackeamento.Dificuldade.DIFICIL,
	"Atirador": Hackeamento.Dificuldade.DIFICIL,
}

@export var alcance: float = 170.0
@export var segundos_estendendo: float = 0.55
@export var segundos_recolhendo: float = 0.4
@export var segundos_desligado: float = 15.0
@export var segundos_recarga: float = 6.0
@export var multiplicador_andando: float = 0.3
@export var lentidao_do_robo: float = 0.3
@export var ruido_ao_falhar: int = 14

var item: Item
var _fase := Fase.OCIOSO
var _alvo: Robo
var _janela: TelaHackeamento
var _progresso := 0.0
var _recarga := 0.0
var _tempo := 0.0
var _cor_original_do_alvo := Color.WHITE

@onready var luz_da_mao: PointLight2D = $LuzDaMao
@onready var luz_do_robo: PointLight2D = $LuzDoRobo


func _ready() -> void:
	Vida.dano_recebido.connect(_ao_receber_dano)


func usar() -> void:
	if _fase != Fase.OCIOSO:
		return
	if _recarga > 0.0:
		Inventario.aviso.emit("Implante esfriando: %d s" % ceili(_recarga))
		return
	var alvo := _procurar_alvo()
	if alvo == null:
		var aviso := "Esse robô bloqueou o acesso" if _ha_robo_bloqueado_perto() else "Nenhum robô ao alcance, em linha reta"
		Inventario.aviso.emit(aviso)
		return
	_comecar(alvo)


func ao_desequipar() -> void:
	if _fase != Fase.OCIOSO:
		_terminar()


func _dono() -> Gabriel:
	return get_parent().get_parent() as Gabriel


func _procurar_alvo() -> Robo:
	var dono := _dono()
	var melhor: Robo = null
	var menor := alcance
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo == null or not robo.visible or _falhas_de(robo) >= FALHAS_PARA_BLOQUEAR:
			continue
		var distancia := dono.global_position.distance_to(robo.global_position)
		if distancia < menor and _linha_livre(dono.global_position, robo.global_position):
			menor = distancia
			melhor = robo
	return melhor


func _ha_robo_bloqueado_perto() -> bool:
	var dono := _dono()
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo and _falhas_de(robo) >= FALHAS_PARA_BLOQUEAR and dono.global_position.distance_to(robo.global_position) < alcance:
			return true
	return false


func _falhas_de(robo: Robo) -> int:
	return robo.get_meta(META_FALHAS, 0)


func _linha_livre(de: Vector2, ate: Vector2) -> bool:
	var consulta := PhysicsRayQueryParameters2D.create(de + Vector2(0, -4), ate + Vector2(0, -4), CAMADA_PAREDES)
	return get_world_2d().direct_space_state.intersect_ray(consulta).is_empty()


func _comecar(alvo: Robo) -> void:
	var dono := _dono()
	_alvo = alvo
	_cor_original_do_alvo = alvo.modulate
	_alvo.fator_de_velocidade = lentidao_do_robo
	_fase = Fase.ESTENDENDO
	_progresso = 0.0
	dono.olhar_travado = false
	dono.olhar_para(dono.global_position.direction_to(alvo.global_position))
	dono.olhar_travado = true
	dono.multiplicador_de_velocidade = multiplicador_andando
	dono.tocar_tira(TIRAS[dono.vista], QUADROS)
	dono.mostrar_quadro_tira(0)


func _process(delta: float) -> void:
	_tempo += delta
	_recarga = maxf(_recarga - delta, 0.0)
	_mostrar_no_hud()
	match _fase:
		Fase.ESTENDENDO:
			_progresso = minf(_progresso + delta / segundos_estendendo, 1.0)
			_mostrar_quadro()
			if _progresso >= 1.0:
				_abrir_minigame()
		Fase.INVADINDO:
			_conferir_conexao()
		Fase.RECOLHENDO:
			_progresso = maxf(_progresso - delta / segundos_recolhendo, 0.0)
			_mostrar_quadro()
			if _progresso <= 0.0:
				_terminar()
	_atualizar_brilho()
	queue_redraw()


func _conferir_conexao() -> void:
	var dono := _dono()
	if not is_instance_valid(_alvo):
		_soltar("Hack cancelado")
		return
	var longe := dono.global_position.distance_to(_alvo.global_position) > alcance + FOLGA_DO_ALCANCE
	if longe or not _linha_livre(dono.global_position, _alvo.global_position):
		_soltar("Conexão perdida")


func _soltar(aviso: String) -> void:
	if is_instance_valid(_janela):
		_janela.interromper()
	Inventario.aviso.emit(aviso)
	_recolher()


func _mostrar_quadro() -> void:
	_dono().mostrar_quadro_tira(roundi(_progresso * (QUADROS - 1)))


func _abrir_minigame() -> void:
	_fase = Fase.INVADINDO
	var janela := TELA_HACKEAMENTO.instantiate() as TelaHackeamento
	get_tree().current_scene.add_child(janela)
	janela.concluido.connect(_ao_terminar_minigame)
	janela.cancelado.connect(_ao_cancelar_minigame)
	_janela = janela
	var nivel: Hackeamento.Dificuldade = DIFICULDADE_POR_ROBO.get(_alvo.nome_tipo, Hackeamento.Dificuldade.MEDIO)
	janela.abrir(nivel, Hackeamento.Tipo.SINCRONIA, false)


func _ao_terminar_minigame(sucesso: bool) -> void:
	if sucesso and is_instance_valid(_alvo):
		_alvo.atordoar(segundos_desligado)
		Inventario.aviso.emit("%s desligado por %d segundos" % [_alvo.nome_tipo, int(segundos_desligado)])
	else:
		_registrar_falha()
	_recolher()


func _registrar_falha() -> void:
	Robo.fazer_barulho(get_tree(), _dono().global_position, ruido_ao_falhar)
	if not is_instance_valid(_alvo):
		Inventario.aviso.emit("Hack falhou: o robô ouviu")
		return
	var falhas := _falhas_de(_alvo) + 1
	_alvo.set_meta(META_FALHAS, falhas)
	if falhas >= FALHAS_PARA_BLOQUEAR:
		Inventario.aviso.emit("Hack falhou pela %dª vez: o robô bloqueou o acesso" % falhas)
	else:
		Inventario.aviso.emit("Hack falhou (%d de %d): o robô ouviu" % [falhas, FALHAS_PARA_BLOQUEAR])


func _ao_cancelar_minigame() -> void:
	Inventario.aviso.emit("Hack cancelado")
	_recolher()


func _recolher() -> void:
	_soltar_alvo()
	_fase = Fase.RECOLHENDO
	_recarga = segundos_recarga


func _ao_receber_dano(_origem: Vector2) -> void:
	if _fase == Fase.OCIOSO:
		return
	if is_instance_valid(_janela):
		_janela.interromper()
	Inventario.aviso.emit("Hack interrompido")
	_recolher()


func _terminar() -> void:
	var dono := _dono()
	_soltar_alvo()
	_fase = Fase.OCIOSO
	_progresso = 0.0
	if dono:
		dono.terminar_tira()
		dono.multiplicador_de_velocidade = 1.0
		dono.olhar_travado = false
	queue_redraw()


func _soltar_alvo() -> void:
	if is_instance_valid(_alvo):
		_alvo.fator_de_velocidade = 1.0
		_alvo.modulate = _cor_original_do_alvo
	_alvo = null


func _mostrar_no_hud() -> void:
	if item == null:
		return
	var estado := Inventario.estado_de(item.id)
	estado["carga"] = 1.0 - _recarga / segundos_recarga
	estado["aceso"] = _fase != Fase.OCIOSO


func _calor() -> float:
	return _recarga / segundos_recarga


func _energizado() -> bool:
	return is_instance_valid(_alvo) and (_fase == Fase.ESTENDENDO or _fase == Fase.INVADINDO)


func _posicao_da_mao() -> Vector2:
	var dono := _dono()
	if _fase == Fase.OCIOSO:
		return dono.to_global(dono.posicao_da_mao())
	var quadros: Array = MAOS_HACK[dono.vista]
	return dono.to_global(dono.ponto_do_quadro(quadros[roundi(_progresso * (QUADROS - 1))]))


func _pulso(rapidez: float) -> float:
	return 0.5 + 0.5 * sin(_tempo * rapidez)


func _atualizar_brilho() -> void:
	if _dono() == null:
		return
	luz_da_mao.global_position = _posicao_da_mao()
	luz_do_robo.energy = 0.0
	if _energizado():
		luz_da_mao.color = COR_RAIO
		luz_da_mao.energy = 0.8 + 0.5 * _pulso(18.0)
		luz_do_robo.global_position = _alvo.global_position + ALTURA_DO_ALVO
		luz_do_robo.energy = (0.6 + 0.6 * _pulso(14.0)) * _progresso
		_alvo.modulate = _cor_original_do_alvo * Color.WHITE.lerp(COR_ROBO_ENERGIZADO, _progresso * _pulso(14.0))
	elif _calor() > 0.0:
		luz_da_mao.color = COR_CALOR
		luz_da_mao.energy = _calor() * (1.0 + 0.25 * _pulso(5.0))
	else:
		luz_da_mao.energy = 0.0


func _draw() -> void:
	if _dono() == null:
		return
	var mao := to_local(_posicao_da_mao())
	if _energizado():
		_desenhar_brilho(mao, COR_RAIO, COR_NUCLEO, 4.0)
		_desenhar_faiscas(mao, AREA_DA_MAO, 7.0, FAISCAS_NA_MAO, 1)
		_desenhar_raio(mao)
		if _fase == Fase.INVADINDO:
			_desenhar_faiscas(to_local(_alvo.global_position + ALTURA_DO_ALVO), AREA_DO_ROBO, 6.0, FAISCAS_NO_ROBO, 2)
	elif _calor() > 0.0:
		_desenhar_calor(mao, _calor())


func _desenhar_brilho(centro: Vector2, cor: Color, nucleo: Color, raio: float) -> void:
	draw_circle(centro, raio * (0.85 + 0.3 * _pulso(18.0)), Color(cor, 0.22))
	draw_circle(centro, raio * 0.55, Color(cor, 0.45))
	draw_circle(centro, 1.2, nucleo)


func _desenhar_faiscas(centro: Vector2, area: Vector2, comprimento: float, quantas: int, semente: int) -> void:
	var sorteio := RandomNumberGenerator.new()
	for i in quantas:
		sorteio.seed = hash(Vector3i(semente, i, floori(_tempo * FAISCAS_POR_SEGUNDO + i * 0.37)))
		if sorteio.randf() < 0.3:
			continue
		var inicio := centro + Vector2(sorteio.randf_range(-area.x, area.x), sorteio.randf_range(-area.y, area.y))
		var direcao := Vector2.from_angle(sorteio.randf() * TAU)
		var fim := inicio + direcao * comprimento * sorteio.randf_range(0.6, 1.0)
		var meio := (inicio + fim) * 0.5 + direcao.orthogonal() * sorteio.randf_range(-2.5, 2.5)
		var pontos := PackedVector2Array([inicio, meio, fim])
		draw_polyline(pontos, COR_RAIO, 1.0)
		draw_circle(fim, 0.6, COR_NUCLEO)


func _desenhar_calor(centro: Vector2, calor: float) -> void:
	draw_circle(centro, 3.0 + 2.0 * calor, Color(COR_CALOR, 0.3 * calor))
	draw_circle(centro, 2.0, Color(COR_CALOR, 0.75 * calor))
	draw_circle(centro, 1.0, Color(COR_BRASA, calor))
	for i in FIOS_DE_FUMACA:
		var subida := fposmod(_tempo * 0.7 + float(i) / FIOS_DE_FUMACA, 1.0)
		var ponto := centro + Vector2(sin(_tempo * 3.0 + i * 2.1) * 1.5, -2.0 - subida * 11.0)
		draw_circle(ponto, 0.8 + subida * 1.6, Color(COR_FUMACA, (1.0 - subida) * 0.45 * calor))


func _desenhar_raio(mao: Vector2) -> void:
	var alvo := to_local(_alvo.global_position + ALTURA_DO_ALVO)
	var alcance_do_raio := mao.distance_to(alvo) * _progresso
	var direcao := mao.direction_to(alvo)
	var lado := direcao.orthogonal()
	var pontos := PackedVector2Array()
	for i in SEGMENTOS_DO_RAIO + 1:
		var t := float(i) / SEGMENTOS_DO_RAIO
		var tremor := sin(_tempo * 40.0 + i * 1.9) * 2.2 * sin(t * PI)
		pontos.append(mao + direcao * alcance_do_raio * t + lado * tremor)
	draw_polyline(pontos, COR_RAIO, 2.0)
	draw_polyline(pontos, COR_NUCLEO, 1.0)
	if _fase == Fase.INVADINDO:
		draw_arc(alvo, 9.0 + sin(_tempo * 12.0) * 2.0, 0.0, TAU, 20, COR_RAIO, 1.0)
