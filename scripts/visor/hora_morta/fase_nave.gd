extends Control

const CENA_DE_PARABENS := "res://cenas/visor/hora_morta/tela_de_parabens.tscn"
const TEXTO_DERROTA := "A SESSÃO ACABOU"
const PONTO_INICIAL_DA_CRIATURA := "c1_b"
const PONTO_DA_CRIATURA_NA_FUGA := "maq"
const AREAS_VIZINHAS := {
	"Alojamento": ["C1"],
	"C1": ["Alojamento", "Cinema"],
	"Cinema": ["C1", "C2", "C3", "C4", "Cabine"],
	"C2": ["Cinema", "Hangar"],
	"C3": ["Cinema", "Deposito"],
	"C4": ["Cinema", "Maquinas"],
	"Deposito": ["C3", "Maquinas"],
	"Maquinas": ["C4", "Deposito"],
	"Cabine": ["Cinema"],
	"Hangar": ["C2"],
}

@export var lugar_de_nascer := Vector3(0.0, 0.02, 15.3)
@export var z_da_primeira_varredura: float = -0.5
@export var segundos_ate_outra_varredura_min: float = 28.0
@export var segundos_ate_outra_varredura_max: float = 40.0
@export var segundos_ate_a_varredura_do_c2: float = 6.0
@export var segundos_escurecendo: float = 0.6
@export var segundos_queimando: float = 1.1
@export var segundos_de_texto_final: float = 1.8
@export var segundos_da_dica: float = 8.0
@export var segundos_da_mensagem: float = 3.5
@export var cosseno_da_lanterna: float = 0.9
@export var alcance_da_lanterna: float = 7.0
@export var cosseno_da_mira: float = 0.93
@export var campo_de_visao: float = 72.0
@export_range(0.25, 1.0) var resolucao_do_3d: float = 1.0

var _jogando := false
var _terminou := false
var _primeira_varredura_feita := false
var _passou_pelo_c2 := false
var _ate_outra_varredura := 999.0
var _areas: Array[KitDaNave] = []
var _objetos: Array[ObjetoDaNave] = []
var _area_atual: KitDaNave
var _mirado: ObjetoDaNave
var _segundos_usando := 0.0
var _esperando_soltar := false
var _mensagem_some: Tween

@onready var imagem: SubViewportContainer = $Imagem
@onready var mundo: SubViewport = $Imagem/Mundo
@onready var jogador: JogadorVisor = $Imagem/Mundo/JogadorVisor
@onready var criatura: CriaturaDaProjecao = $Imagem/Mundo/Criatura
@onready var lanterna: SpotLight3D = $Imagem/Mundo/Lanterna
@onready var varredura: Varredura = $Varredura
@onready var objetivos: ObjetivosDaNave = $Objetivos
@onready var dica: Label = $Dica
@onready var aviso: Label = $Aviso
@onready var objetivo: Label = $Objetivo
@onready var acao: Label = $Acao
@onready var mensagem: Label = $Mensagem
@onready var barra: ColorRect = $Barra
@onready var preenchimento: ColorRect = $Barra/Preenchimento
@onready var mira: ColorRect = $Mira
@onready var texto_final: Label = $TextoFinal
@onready var queima: ColorRect = $Queima
@onready var escuro: ColorRect = $Escuro
@onready var zumbido: AudioStreamPlayer = $Zumbido
@onready var sirene: AudioStreamPlayer = $Sirene
@onready var som_da_lanterna: AudioStreamPlayer = $SomDaLanterna
@onready var som_do_estalo: AudioStreamPlayer = $SomDoEstalo
@onready var som_do_ataque: AudioStreamPlayer = $SomDoAtaque
@onready var som_de_achar: AudioStreamPlayer = $SomDeAchar


func _ready() -> void:
	_ajustar_resolucao()
	get_window().size_changed.connect(_ajustar_resolucao)
	_coletar_o_mundo()
	jogador.camera.fov = campo_de_visao
	lanterna.reparent(jogador.camera, false)
	lanterna.visible = false
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	jogador.controlando = false
	jogador.position = lugar_de_nascer
	_esconder_interface()
	_ligar_sinais()
	criatura.preparar(GrafoDaNave.new(), PONTO_INICIAL_DA_CRIATURA)
	objetivos.comecar()
	_atualizar_area_atual()
	_entrar()


func _coletar_o_mundo() -> void:
	for area in $Imagem/Mundo/Areas.get_children():
		_areas.append(area as KitDaNave)
	_coletar_objetos($Imagem/Mundo)


func _coletar_objetos(no: Node) -> void:
	if no is ObjetoDaNave:
		_objetos.append(no)
	if no is PortaDaNave:
		no.alvo = jogador
	for filho in no.get_children():
		_coletar_objetos(filho)


func _esconder_interface() -> void:
	aviso.visible = false
	texto_final.visible = false
	queima.visible = false
	mensagem.visible = false
	barra.visible = false
	acao.text = ""
	_definir_queima(0.0)


func _ligar_sinais() -> void:
	criatura.tocou_o_jogador.connect(_perder)
	varredura.comecou.connect(_ao_comecar_varredura)
	varredura.vigia_comecou.connect(_ao_comecar_vigia)
	varredura.terminou.connect(_ao_terminar_varredura)
	varredura.jogador_se_mexeu.connect(_perder)
	objetivos.mensagem.connect(_mostrar_mensagem)
	objetivos.objetivo_mudou.connect(_mostrar_objetivo)
	objetivos.energia_ligada.connect(_ao_ligar_energia)
	objetivos.fuga_comecou.connect(_ao_comecar_fuga)
	objetivos.ruido.connect(criatura.ouvir)
	objetivos.venceu.connect(_vencer)


func _entrar() -> void:
	escuro.color.a = 1.0
	var entrada := create_tween()
	entrada.tween_property(escuro, "color:a", 0.0, segundos_escurecendo)
	entrada.tween_callback(_liberar)
	entrada.tween_interval(segundos_da_dica)
	entrada.tween_property(dica, "modulate:a", 0.0, 1.0)


func _liberar() -> void:
	jogador.controlando = true
	_jogando = true


func _physics_process(delta: float) -> void:
	if not _jogando:
		return
	_atualizar_area_atual()
	criatura.existir(_iluminado(criatura.lugar_real()))
	criatura.notar_jogador(_jogador_exposto(), jogador.global_position)
	_conferir_varredura(delta)


func _process(delta: float) -> void:
	if _jogando:
		_atualizar_mira(delta)


func _unhandled_input(evento: InputEvent) -> void:
	if not _jogando:
		return
	if evento is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		jogador.girar(evento.screen_relative)
		varredura.registrar_giro_do_mouse(evento.screen_relative)
	elif evento is InputEventMouseButton and evento.pressed:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
		_alternar_lanterna()
	elif evento.is_action_pressed("pausar"):
		_tirar_o_visor()
	else:
		return
	get_viewport().set_input_as_handled()


func _alternar_lanterna() -> void:
	lanterna.visible = not lanterna.visible
	som_da_lanterna.play()


func _atualizar_area_atual() -> void:
	for area in _areas:
		if area.contem(jogador.global_position):
			if area != _area_atual:
				_entrar_na_area(area)
			return


func _entrar_na_area(area: KitDaNave) -> void:
	_area_atual = area
	var vizinhas: Array = AREAS_VIZINHAS[area.name]
	for outra in _areas:
		outra.visible = outra == area or vizinhas.has(String(outra.name))
	if area.name == &"C2" and not _passou_pelo_c2:
		_passou_pelo_c2 = true
		_ate_outra_varredura = minf(_ate_outra_varredura, segundos_ate_a_varredura_do_c2)


func _iluminado(lugar: Vector3) -> bool:
	if varredura.clareando():
		return true
	if _alguma_lampada_ilumina(lugar):
		return true
	return _na_lanterna(lugar)


func _alguma_lampada_ilumina(lugar: Vector3) -> bool:
	for area in _areas:
		for lampada in area.lampadas:
			if lampada.ilumina(lugar):
				return true
	return false


func _na_lanterna(lugar: Vector3) -> bool:
	if not lanterna.visible:
		return false
	var ate_o_lugar := lugar + Vector3.UP - jogador.camera.global_position
	if ate_o_lugar.length() > alcance_da_lanterna:
		return false
	return jogador.direcao_do_olhar().dot(ate_o_lugar.normalized()) >= cosseno_da_lanterna


func _jogador_exposto() -> bool:
	if _area_atual and _area_atual.segura:
		return false
	return lanterna.visible or _alguma_lampada_ilumina(jogador.global_position)


func _conferir_varredura(delta: float) -> void:
	if varredura.em_curso() or objetivos.em_fuga or _area_atual == null or not _area_atual.tem_janelas:
		return
	if not _primeira_varredura_feita:
		if jogador.global_position.z <= z_da_primeira_varredura:
			_primeira_varredura_feita = true
			aviso.visible = true
			varredura.comecar()
		return
	_ate_outra_varredura -= delta
	if _ate_outra_varredura <= 0.0:
		varredura.comecar()


func _ao_comecar_varredura() -> void:
	criatura.parar()
	criatura.existir(false)
	zumbido.stop()
	som_do_estalo.play()
	for area in _areas:
		area.cortar_energia()


func _ao_comecar_vigia() -> void:
	var no_corredor := _area_atual != null and _area_atual.tem_janelas
	varredura.exigir_parado = no_corredor
	if not no_corredor:
		return
	var lado: float = _lado_do_olhar() if aviso.visible else [-1.0, 1.0].pick_random()
	var limite := _area_atual.global_position.z
	var meio := _area_atual.limites.size.z / 2.0
	criatura.aparecer_perto(jogador.global_position, lado, limite - meio + 0.6, limite + meio - 0.6)


func _lado_do_olhar() -> float:
	return -1.0 if jogador.direcao_do_olhar().z <= 0.0 else 1.0


func _ao_terminar_varredura() -> void:
	aviso.visible = false
	_religar_a_nave()
	criatura.voltar_longe(jogador.global_position)
	_ate_outra_varredura = randf_range(segundos_ate_outra_varredura_min, segundos_ate_outra_varredura_max)


func _religar_a_nave() -> void:
	zumbido.play()
	for area in _areas:
		area.religar()


func _ao_ligar_energia() -> void:
	som_de_achar.play()
	for area in _areas:
		area.receber_energia()


func _ao_comecar_fuga() -> void:
	varredura.interromper()
	aviso.visible = false
	_religar_a_nave()
	sirene.play()
	for area in _areas:
		area.definir_alarme(true)
	criatura.em_fuga = true
	if criatura.estado == CriaturaDaProjecao.Estado.PARADA or criatura.lugar_real().distance_to(jogador.global_position) < 20.0:
		criatura.preparar(criatura.grafo, PONTO_DA_CRIATURA_NA_FUGA)


func _atualizar_mira(delta: float) -> void:
	var novo := _objeto_mirado()
	if novo != _mirado:
		_mirado = novo
		_segundos_usando = 0.0
	acao.text = "" if _mirado == null else "E: " + _mirado.texto_acao
	var apertando := Input.is_action_pressed("interagir")
	if not apertando:
		_esperando_soltar = false
		_segundos_usando = 0.0
	if _mirado and apertando and not _esperando_soltar:
		_segundos_usando += delta
		if _segundos_usando >= _mirado.segundos_para_usar:
			_usar(_mirado)
	var mostrar_barra := _mirado != null and _mirado.segundos_para_usar > 0.0 and _segundos_usando > 0.0
	barra.visible = mostrar_barra
	if mostrar_barra:
		preenchimento.size.x = barra.size.x * minf(_segundos_usando / _mirado.segundos_para_usar, 1.0)


func _usar(objeto: ObjetoDaNave) -> void:
	_esperando_soltar = true
	_segundos_usando = 0.0
	som_de_achar.play()
	objeto.usar()


func _objeto_mirado() -> ObjetoDaNave:
	var olho := jogador.camera.global_position
	var olhar := jogador.direcao_do_olhar()
	var melhor: ObjetoDaNave = null
	var melhor_cosseno := cosseno_da_mira
	for objeto in _objetos:
		if not objeto.pode_mirar():
			continue
		var ate_ele := objeto.ponto_da_mira() - olho
		if ate_ele.length() > objeto.distancia_de_uso:
			continue
		var cosseno := olhar.dot(ate_ele.normalized())
		if cosseno >= melhor_cosseno:
			melhor = objeto
			melhor_cosseno = cosseno
	return melhor


func _mostrar_objetivo(texto: String) -> void:
	objetivo.text = texto


func _mostrar_mensagem(texto: String) -> void:
	mensagem.text = texto
	mensagem.visible = true
	mensagem.modulate.a = 1.0
	if _mensagem_some:
		_mensagem_some.kill()
	_mensagem_some = create_tween()
	_mensagem_some.tween_interval(segundos_da_mensagem)
	_mensagem_some.tween_property(mensagem, "modulate:a", 0.0, 0.5)


func _perder() -> void:
	if not _jogando:
		return
	_jogando = false
	jogador.controlando = false
	aviso.visible = false
	acao.text = ""
	barra.visible = false
	varredura.interromper()
	var direcao := criatura.atacar(jogador.global_position)
	som_do_ataque.play()
	var giro := atan2(-direcao.x, -direcao.z)
	var virar_a_cabeca := create_tween().set_parallel()
	virar_a_cabeca.tween_property(jogador, "rotation:y", jogador.rotation.y + wrapf(giro - jogador.rotation.y, -PI, PI), 0.12)
	virar_a_cabeca.tween_property(jogador.cabeca, "rotation:x", 0.32, 0.12)
	var queimar := create_tween()
	queimar.tween_interval(0.35)
	queimar.tween_callback(queima.show)
	queimar.tween_method(_definir_queima, 0.0, 1.0, segundos_queimando)
	queimar.tween_callback(_escurecer_com_texto.bind(TEXTO_DERROTA))
	queimar.tween_interval(segundos_de_texto_final)
	queimar.tween_callback(_renascer)


func _definir_queima(progresso: float) -> void:
	(queima.material as ShaderMaterial).set_shader_parameter("progresso", progresso)


func _escurecer_com_texto(texto: String) -> void:
	escuro.color.a = 1.0
	texto_final.text = texto
	texto_final.visible = true


func _renascer() -> void:
	queima.visible = false
	_definir_queima(0.0)
	texto_final.visible = false
	lanterna.visible = false
	jogador.position = lugar_de_nascer
	jogador.velocity = Vector3.ZERO
	jogador.rotation.y = 0.0
	jogador.cabeca.rotation.x = 0.0
	_religar_a_nave()
	if objetivos.em_fuga:
		_encerrar_alarme()
	criatura.voltar_longe(lugar_de_nascer)
	_ate_outra_varredura = randf_range(segundos_ate_outra_varredura_min, segundos_ate_outra_varredura_max)
	_atualizar_area_atual()
	_entrar_sem_dica()


func _encerrar_alarme() -> void:
	objetivos.encerrar_fuga()
	sirene.stop()
	criatura.em_fuga = false
	for area in _areas:
		area.definir_alarme(false)
	_mostrar_mensagem("O alarme parou. Você ainda está com a chave.")


func _entrar_sem_dica() -> void:
	var entrada := create_tween()
	entrada.tween_property(escuro, "color:a", 0.0, segundos_escurecendo)
	entrada.tween_callback(_liberar)


func _vencer() -> void:
	_jogando = false
	jogador.controlando = false
	sirene.stop()
	acao.text = ""
	barra.visible = false
	var saida := create_tween()
	saida.tween_property(escuro, "color:a", 1.0, segundos_escurecendo * 2.0)
	saida.tween_callback(Visor.trocar.bind(CENA_DE_PARABENS))


func _tirar_o_visor() -> void:
	_jogando = false
	jogador.controlando = false
	var saida := create_tween()
	saida.tween_property(escuro, "color:a", 1.0, segundos_escurecendo)
	saida.tween_callback(Visor.fechar)


func _ajustar_resolucao() -> void:
	var na_tela := get_viewport_rect().size
	var desenhada := (Vector2(get_window().size) * resolucao_do_3d).round().max(na_tela)
	imagem.stretch = false
	imagem.set_anchors_and_offsets_preset(Control.PRESET_TOP_LEFT)
	mundo.size = Vector2i(desenhada)
	imagem.size = desenhada
	imagem.scale = na_tela / desenhada
