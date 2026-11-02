class_name Varredura
extends Node

signal comecou
signal vigia_comecou
signal terminou
signal jogador_se_mexeu

enum Etapa { PARADA, AVISO, VIGIA, SAIDA }

const YAW_NORMAL := PI / 2.0

@export var luz: DirectionalLight3D
@export var ceu: ShaderMaterial
@export var ambiente: Environment
@export var luz_ambiente_calma: float = 0.3
@export var luz_ambiente_no_clarao: float = 2.4
@export var jogador: JogadorVisor
@export var segundos_de_aviso: float = 2.0
@export var segundos_de_vigia: float = 7.0
@export var segundos_de_saida: float = 1.6
@export var energia_da_luz: float = 3.2
@export var abertura_do_giro: float = deg_to_rad(38.0)
@export var inclinacao: float = deg_to_rad(-20.0)
@export var giro_calmo: float = 0.012
@export var giro_na_varredura: float = 0.14
@export var tolerancia_do_mouse: float = 24.0
@export var mouse_que_se_perdoa_por_segundo: float = 8.0
@export var velocidade_tolerada: float = 0.05

var etapa := Etapa.PARADA
var exigir_parado := true
var _tempo := 0.0
var _giro := 0.0
var _mouse_acumulado := 0.0


func _ready() -> void:
	_aplicar_luz(0.0, 0.0)


func _process(delta: float) -> void:
	var ativa := etapa != Etapa.PARADA
	_giro += (giro_na_varredura if ativa else giro_calmo) * delta
	ceu.set_shader_parameter("giro", _giro)
	if ativa:
		_avancar(delta)


func em_curso() -> bool:
	return etapa != Etapa.PARADA


func clareando() -> bool:
	return etapa == Etapa.VIGIA


func comecar() -> void:
	if em_curso():
		return
	_mudar_para(Etapa.AVISO)
	comecou.emit()


func interromper() -> void:
	_mudar_para(Etapa.PARADA)
	_aplicar_luz(0.0, 0.0)


func registrar_giro_do_mouse(movimento: Vector2) -> void:
	if etapa == Etapa.VIGIA:
		_mouse_acumulado += movimento.length()


func _avancar(delta: float) -> void:
	_tempo += delta
	_aplicar_luz(_progresso_total(), _brilho_da_etapa())
	match etapa:
		Etapa.AVISO:
			if _tempo >= segundos_de_aviso:
				_mouse_acumulado = 0.0
				_mudar_para(Etapa.VIGIA)
				vigia_comecou.emit()
		Etapa.VIGIA:
			_vigiar(delta)
		Etapa.SAIDA:
			if _tempo >= segundos_de_saida:
				_mudar_para(Etapa.PARADA)
				_aplicar_luz(0.0, 0.0)
				terminou.emit()


func _vigiar(delta: float) -> void:
	_mouse_acumulado = maxf(0.0, _mouse_acumulado - mouse_que_se_perdoa_por_segundo * delta)
	var andando := Vector2(jogador.velocity.x, jogador.velocity.z).length() > velocidade_tolerada
	if exigir_parado and (andando or _mouse_acumulado > tolerancia_do_mouse):
		_mudar_para(Etapa.PARADA)
		jogador_se_mexeu.emit()
	elif _tempo >= segundos_de_vigia:
		_mudar_para(Etapa.SAIDA)


func _mudar_para(nova: Etapa) -> void:
	etapa = nova
	_tempo = 0.0


func _progresso_total() -> float:
	var total := segundos_de_aviso + segundos_de_vigia + segundos_de_saida
	match etapa:
		Etapa.AVISO:
			return _tempo / total
		Etapa.VIGIA:
			return (segundos_de_aviso + _tempo) / total
		_:
			return (segundos_de_aviso + segundos_de_vigia + _tempo) / total


func _brilho_da_etapa() -> float:
	match etapa:
		Etapa.AVISO:
			return smoothstep(0.0, segundos_de_aviso, _tempo)
		Etapa.VIGIA:
			return 1.0
		_:
			return 1.0 - smoothstep(0.0, segundos_de_saida, _tempo)


func _aplicar_luz(progresso: float, brilho: float) -> void:
	var yaw := YAW_NORMAL + lerpf(-abertura_do_giro, abertura_do_giro, progresso)
	luz.rotation = Vector3(inclinacao, yaw, 0.0)
	luz.light_energy = energia_da_luz * brilho
	luz.visible = brilho > 0.0
	ambiente.ambient_light_energy = lerpf(luz_ambiente_calma, luz_ambiente_no_clarao, brilho)
	ceu.set_shader_parameter("direcao_da_estrela", luz.global_basis.z)
	ceu.set_shader_parameter("brilho_da_estrela", brilho)
