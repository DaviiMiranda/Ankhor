extends Node2D

enum Fase { OCIOSO, ESTENDENDO, INVADINDO, RECOLHENDO }

const TELA_HACKEAMENTO := preload("res://cenas/interface/tela_hackeamento.tscn")
const MAOS_HACK: Dictionary = preload("res://scripts/personagens/maos_do_zane.gd").MAOS_HACK
const QUADROS := 12
const CAMADA_PAREDES := 8
const ALTURA_DO_ALVO := Vector2(0, -26)
const COR_RAIO := Color(0.35, 0.95, 0.85)
const COR_NUCLEO := Color(0.85, 1.0, 0.95)
const SEGMENTOS_DO_RAIO := 14
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
@export var ruido_ao_falhar: int = 14

var item: Item
var _fase := Fase.OCIOSO
var _alvo: Robo
var _janela: TelaHackeamento
var _progresso := 0.0
var _recarga := 0.0
var _tempo := 0.0


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
		Inventario.aviso.emit("Nenhum robô ao alcance, em linha reta")
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
		if robo == null or not robo.visible:
			continue
		var distancia := dono.global_position.distance_to(robo.global_position)
		if distancia < menor and _linha_livre(dono.global_position, robo.global_position):
			menor = distancia
			melhor = robo
	return melhor


func _linha_livre(de: Vector2, ate: Vector2) -> bool:
	var consulta := PhysicsRayQueryParameters2D.create(de + Vector2(0, -4), ate + Vector2(0, -4), CAMADA_PAREDES)
	return get_world_2d().direct_space_state.intersect_ray(consulta).is_empty()


func _comecar(alvo: Robo) -> void:
	var dono := _dono()
	_alvo = alvo
	_fase = Fase.ESTENDENDO
	_progresso = 0.0
	dono.andar_sozinho(Vector2.ZERO)
	dono.olhar_para(dono.global_position.direction_to(alvo.global_position))
	dono.tocar_tira(TIRAS[dono.vista], QUADROS)
	dono.mostrar_quadro_tira(0)


func _process(delta: float) -> void:
	_tempo += delta
	_recarga = maxf(_recarga - delta, 0.0)
	match _fase:
		Fase.ESTENDENDO:
			_progresso = minf(_progresso + delta / segundos_estendendo, 1.0)
			_mostrar_quadro()
			if _progresso >= 1.0:
				_abrir_minigame()
		Fase.RECOLHENDO:
			_progresso = maxf(_progresso - delta / segundos_recolhendo, 0.0)
			_mostrar_quadro()
			if _progresso <= 0.0:
				_terminar()
	queue_redraw()


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
	janela.abrir(nivel, Hackeamento.Tipo.ALEATORIO, false)


func _ao_terminar_minigame(sucesso: bool) -> void:
	if sucesso and is_instance_valid(_alvo):
		_alvo.atordoar(segundos_desligado)
		Inventario.aviso.emit("%s desligado por %d segundos" % [_alvo.nome_tipo, int(segundos_desligado)])
	else:
		Inventario.aviso.emit("Hack falhou: o robô ouviu")
		Robo.fazer_barulho(get_tree(), _dono().global_position, ruido_ao_falhar)
	_recolher()


func _ao_cancelar_minigame() -> void:
	Inventario.aviso.emit("Hack cancelado")
	_recolher()


func _recolher() -> void:
	_alvo = null
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
	_alvo = null
	_fase = Fase.OCIOSO
	_progresso = 0.0
	if dono:
		dono.terminar_tira()
		dono.devolver_controle()
	queue_redraw()


func _draw() -> void:
	if _alvo == null or not is_instance_valid(_alvo) or _fase == Fase.OCIOSO or _fase == Fase.RECOLHENDO:
		return
	var dono := _dono()
	var quadros: Array = MAOS_HACK[dono.vista]
	var mao := to_local(dono.to_global(dono.ponto_do_quadro(quadros[roundi(_progresso * (QUADROS - 1))])))
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
