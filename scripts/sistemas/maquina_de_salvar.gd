class_name MaquinaDeSalvar
extends Interagivel

const ENERGIA_ATIVA := 1.5
const ALFA_OCIOSA := 0.55

@export var aviso_salvo: String = "Jogo salvo"
@export var aviso_falha: String = "Não foi possível salvar"
@export var deslocamento_retorno := Vector2(0, 14)
@export var segundos_escurecendo: float = 0.9
@export var segundos_conectado: float = 1.2

var _salvando := false
var _salvou := false
var _energia_ociosa: float

@onready var camada_luz: Sprite2D = $CamadaLuz
@onready var luz: PointLight2D = $Luz
@onready var som: AudioStreamPlayer = $Som


func _ready() -> void:
	super()
	_energia_ociosa = luz.energy
	camada_luz.modulate.a = ALFA_OCIOSA


func pode_interagir() -> bool:
	return not _salvando


func interagir() -> void:
	var gabriel := get_tree().get_first_node_in_group("jogador") as Gabriel
	if gabriel == null:
		return
	_salvando = true
	gabriel.andar_sozinho(Vector2.ZERO)
	var escuro := get_tree().current_scene.get_node_or_null("Transicao/Escuro") as ColorRect
	som.play()
	var sessao := create_tween()
	sessao.tween_property(luz, "energy", ENERGIA_ATIVA, 0.5)
	sessao.parallel().tween_property(camada_luz, "modulate:a", 1.0, 0.5)
	if escuro:
		sessao.tween_property(escuro, "color:a", 1.0, segundos_escurecendo)
	sessao.tween_interval(segundos_conectado)
	sessao.tween_callback(_gravar)
	if escuro:
		sessao.tween_property(escuro, "color:a", 0.0, segundos_escurecendo)
	sessao.tween_property(luz, "energy", _energia_ociosa, 0.6)
	sessao.parallel().tween_property(camada_luz, "modulate:a", ALFA_OCIOSA, 0.6)
	sessao.tween_callback(_terminar.bind(gabriel))


func _gravar() -> void:
	var posicao := global_position + deslocamento_retorno
	Vida.limpar()
	Checkpoints.marcar("maquina_de_salvar", _cena(), posicao)
	_salvou = Salvamento.salvar(_cena(), posicao)


func _terminar(gabriel: Gabriel) -> void:
	gabriel.devolver_controle()
	Inventario.aviso.emit(aviso_salvo if _salvou else aviso_falha)
	_salvando = false


func _cena() -> String:
	var sala := owner if owner else get_tree().current_scene
	return sala.scene_file_path if sala else ""
