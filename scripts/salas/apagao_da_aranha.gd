class_name ApagaoDaAranha
extends Node

enum Fase { ESPERANDO, APAGANDO, APROXIMANDO, ENCERRANDO }

const CENA_ARANHA := preload("res://cenas/personagens/aranha_do_apagao.tscn")
const CENA_HACK := preload("res://cenas/interface/hack_da_aranha.tscn")
const COR_DO_APAGAO := Color(0.035, 0.04, 0.06)
const PREFIXO_DA_MARCA := "escritorio_aranha_"
const SEGUNDOS_DA_LUZ := 0.2
const SEGUNDOS_DO_RESULTADO := 0.9
const MARGEM_DO_CHAO := 6.0
const DIRECOES: Array[Vector2] = [
	Vector2(-1, 0), Vector2(1, 0), Vector2(-1, -0.35), Vector2(1, -0.35), Vector2(-1, 0.35), Vector2(1, 0.35),
]

static var _fim_do_ultimo := -1000.0

@export var segundos_minimos := 20.0
@export var segundos_maximos := 40.0
@export var segundos_entre_eventos := 25.0
@export var eventos_maximos := 4
@export var distancia_do_aparecimento := 150.0
@export var segundos_de_escuro_antes := 1.0
@export var marca_que_encerra := "escritorio_tres_travas"

var _fase := Fase.ESPERANDO
var _espera := 0.0
var _sala: Sala
var _gabriel: Gabriel
var _luzes: Node2D
var _escuridao: CanvasModulate
var _cor_original := Color.WHITE
var _aranha: AranhaDoApagao
var _hack: HackDaAranha
var _robos_parados: Dictionary = {}

@onready var som_apagao: AudioStreamPlayer = $SomApagao
@onready var som_religar: AudioStreamPlayer = $SomReligar


func _ready() -> void:
	if Engine.is_editor_hint():
		return
	_sala = get_parent() as Sala
	if _sala:
		_gabriel = _sala.get_node_or_null("Objetos/Gabriel") as Gabriel
	if _gabriel == null or _terminou_os_eventos():
		set_process(false)
		return
	_luzes = _sala.get_node_or_null("Luzes") as Node2D
	_escuridao = _sala.get_node_or_null("Escuridao") as CanvasModulate
	_espera = maxf(randf_range(segundos_minimos, segundos_maximos), _fim_do_ultimo + segundos_entre_eventos - _agora())
	Vida.morreu.connect(_abortar)


func _exit_tree() -> void:
	if _fase != Fase.ESPERANDO:
		Hackeamento.tela_em_tempo_real = false


func _process(delta: float) -> void:
	match _fase:
		Fase.ESPERANDO:
			if _terminou_os_eventos():
				set_process(false)
			elif _pode_esperar():
				_espera -= delta
				if _espera <= 0.0:
					_comecar()
		Fase.APROXIMANDO:
			if is_instance_valid(_aranha) and is_instance_valid(_hack):
				_hack.atualizar_tempo(_aranha.segundos_restantes())


func _agora() -> float:
	return Time.get_ticks_msec() / 1000.0


func _eventos_feitos() -> int:
	var total := 0
	while Progresso.tem(PREFIXO_DA_MARCA + str(total + 1)):
		total += 1
	return total


func _terminou_os_eventos() -> bool:
	return _eventos_feitos() >= eventos_maximos or Progresso.tem(marca_que_encerra)


func _pode_esperar() -> bool:
	return Vida.esta_viva() and _gabriel.jogador_controla and not Dialogos.ativo and not Hackeamento.tela_em_tempo_real and not _alguem_persegue()


func _robos_da_sala() -> Array[Robo]:
	var robos: Array[Robo] = []
	for no in get_tree().get_nodes_in_group("robos"):
		var robo := no as Robo
		if robo and _sala.is_ancestor_of(robo):
			robos.append(robo)
	return robos


func _alguem_persegue() -> bool:
	for robo in _robos_da_sala():
		if robo.esta_perseguindo():
			return true
	return false


func _comecar() -> void:
	_fase = Fase.APAGANDO
	var numero := _eventos_feitos() + 1
	Progresso.marcar(PREFIXO_DA_MARCA + str(numero))
	_parar_os_robos()
	_apagar_as_luzes()
	await get_tree().create_timer(segundos_de_escuro_antes, false).timeout
	if _fase != Fase.APAGANDO or not Vida.esta_viva():
		return
	_aparecer(numero)


func _aparecer(numero: int) -> void:
	var nivel := HackDaAranha.nivel(numero)
	var segundos: float = nivel["segundos"]
	_aranha = CENA_ARANHA.instantiate() as AranhaDoApagao
	_sala.get_node("Objetos").add_child(_aranha)
	_aranha.global_position = _ponto_de_aparecimento()
	_aranha.chegou.connect(_ao_chegar)
	_aranha.iniciar(_gabriel, segundos)
	_hack = CENA_HACK.instantiate() as HackDaAranha
	_sala.add_child(_hack)
	_hack.resolvido.connect(_ao_resolver)
	_hack.iniciar(nivel, segundos)
	Hackeamento.tela_em_tempo_real = true
	_gabriel.andar_sozinho(Vector2.ZERO)
	_fase = Fase.APROXIMANDO
	Inventario.aviso.emit("Apagão! Hackeie a Aranha antes que ela chegue.")


func _ponto_de_aparecimento() -> Vector2:
	var centro := _gabriel.global_position
	var direcoes := DIRECOES.duplicate()
	direcoes.shuffle()
	for fator: float in [1.0, 0.7, 0.45]:
		for direcao: Vector2 in direcoes:
			var ponto := centro + direcao.normalized() * distancia_do_aparecimento * fator
			if _no_chao(ponto):
				return ponto
	return _canto_mais_longe(centro)


func _no_chao(ponto: Vector2) -> bool:
	return ponto.x >= _sala.margem_lados + MARGEM_DO_CHAO and ponto.x <= _sala.largura - _sala.margem_lados - MARGEM_DO_CHAO \
			and ponto.y >= _sala.chao_fundo + MARGEM_DO_CHAO and ponto.y <= _sala.chao_frente - MARGEM_DO_CHAO


func _canto_mais_longe(centro: Vector2) -> Vector2:
	var melhor := centro
	for x: float in [_sala.margem_lados + MARGEM_DO_CHAO, _sala.largura - _sala.margem_lados - MARGEM_DO_CHAO]:
		for y: float in [_sala.chao_fundo + MARGEM_DO_CHAO, _sala.chao_frente - MARGEM_DO_CHAO]:
			var canto := Vector2(x, y)
			if canto.distance_to(centro) > melhor.distance_to(centro):
				melhor = canto
	return melhor


func _ao_resolver() -> void:
	if _fase != Fase.APROXIMANDO:
		return
	_fase = Fase.ENCERRANDO
	_hack.mostrar_resultado(true)
	_aranha.sumir()
	Inventario.aviso.emit("Aranha 07 desligada. A energia voltou.")
	await get_tree().create_timer(SEGUNDOS_DO_RESULTADO, false).timeout
	_terminar_o_evento()


func _ao_chegar() -> void:
	if _fase != Fase.APROXIMANDO:
		return
	_fase = Fase.ENCERRANDO
	_hack.mostrar_resultado(false)
	_aranha.bote()
	Inventario.aviso.emit("A Aranha 07 alcançou o Zane.")
	Vida.receber_dano(1, _aranha.global_position)
	if _fase != Fase.ENCERRANDO:
		return
	await get_tree().create_timer(SEGUNDOS_DO_RESULTADO, false).timeout
	if is_instance_valid(_aranha):
		_aranha.sumir()
	_terminar_o_evento()


func _terminar_o_evento() -> void:
	if _fase != Fase.ENCERRANDO:
		return
	Hackeamento.tela_em_tempo_real = false
	_gabriel.devolver_controle()
	_soltar_os_robos()
	_religar_as_luzes()
	_fim_do_ultimo = _agora()
	_fase = Fase.ESPERANDO
	_espera = maxf(randf_range(segundos_minimos, segundos_maximos), segundos_entre_eventos)


func _abortar() -> void:
	if _fase == Fase.ESPERANDO:
		return
	_fase = Fase.ESPERANDO
	set_process(false)
	Hackeamento.tela_em_tempo_real = false
	if is_instance_valid(_hack):
		_hack.queue_free()
	if is_instance_valid(_aranha):
		_aranha.queue_free()
	_soltar_os_robos()


func _parar_os_robos() -> void:
	_robos_parados.clear()
	for robo in _robos_da_sala():
		_robos_parados[robo] = robo.fator_de_velocidade
		robo.fator_de_velocidade = 0.0


func _soltar_os_robos() -> void:
	for robo in _robos_parados:
		if is_instance_valid(robo):
			robo.fator_de_velocidade = _robos_parados[robo]
	_robos_parados.clear()


func _apagar_as_luzes() -> void:
	som_apagao.play()
	if _escuridao == null:
		return
	_cor_original = _escuridao.color
	var tween := create_tween()
	tween.tween_property(_escuridao, "color", _cor_original.darkened(0.5), SEGUNDOS_DA_LUZ / 2.0)
	tween.tween_property(_escuridao, "color", _cor_original, SEGUNDOS_DA_LUZ / 2.0)
	tween.tween_property(_escuridao, "color", COR_DO_APAGAO, SEGUNDOS_DA_LUZ)
	if _luzes:
		tween.tween_callback(_luzes.hide)


func _religar_as_luzes() -> void:
	som_religar.play()
	if _luzes:
		_luzes.show()
	if _escuridao == null:
		return
	var tween := create_tween()
	tween.tween_property(_escuridao, "color", _cor_original.darkened(0.55), 0.06)
	tween.tween_property(_escuridao, "color", COR_DO_APAGAO, 0.06)
	tween.tween_property(_escuridao, "color", _cor_original.darkened(0.25), 0.08)
	tween.tween_property(_escuridao, "color", _cor_original, 0.35)
