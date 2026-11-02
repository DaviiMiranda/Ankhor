class_name ObjetivosDaNave
extends Node

signal mensagem(texto: String)
signal objetivo_mudou(texto: String)
signal energia_ligada
signal fuga_comecou
signal ruido(lugar: Vector3)
signal venceu

const INICIAL := "Chegue ao hangar, no fim da nave."
const ACHAR_A_CHAVE := "Pegue a chave do hangar na cabine do comandante."
const RELIGAR := "Religue a energia na sala de máquinas."
const ACHAR_FUSIVEL := "Procure um fusível nos armários do depósito."
const LEVAR_FUSIVEL := "Leve o fusível ao quadro da sala de máquinas."
const PEGAR_NA_CABINE := "A cabine abriu. Pegue a chave."
const CORRER := "Corra para o hangar!"
const ABRIR_O_HANGAR := "Abra o hangar com a chave."
const ENTRAR_NA_NAVE := "Entre na nave menor."
const TEXTO_DA_PORTA_DO_HANGAR := "Porta do hangar"
const TEXTO_DA_PORTA_DA_CABINE := "Porta da cabine do comandante"
const TEXTO_DE_USAR_A_CHAVE := "Abrir com a chave"
const SEGUNDOS_ABRINDO_O_HANGAR := 4.0
const SEGUNDOS_NO_QUADRO := 2.0

@export var porta_do_hangar: PortaDaNave
@export var porta_da_cabine: PortaDaNave
@export var deposito: SalaDeposito
@export var maquinas: SalaMaquinas
@export var cabine: SalaCabine
@export var hangar: SalaHangar

var tem_fusivel := false
var tem_energia := false
var tem_chave := false
var em_fuga := false
var _armario_do_fusivel: ObjetoDaNave


func _ready() -> void:
	_armario_do_fusivel = deposito.armarios.pick_random()
	porta_do_hangar.texto_acao = TEXTO_DA_PORTA_DO_HANGAR
	porta_da_cabine.texto_acao = TEXTO_DA_PORTA_DA_CABINE
	porta_do_hangar.usado.connect(_usar_porta_do_hangar)
	porta_da_cabine.usado.connect(_usar_porta_da_cabine)
	for armario in deposito.armarios:
		armario.usado.connect(_vasculhar.bind(armario))
	maquinas.quadro.usado.connect(_usar_quadro)
	cabine.chave.usado.connect(_pegar_a_chave)
	hangar.nave_menor.usado.connect(venceu.emit)


func comecar() -> void:
	objetivo_mudou.emit(INICIAL)


func encerrar_fuga() -> void:
	em_fuga = false
	objetivo_mudou.emit(ABRIR_O_HANGAR)


func _usar_porta_do_hangar() -> void:
	if tem_chave:
		porta_do_hangar.destrancar()
		ruido.emit(porta_do_hangar.global_position)
		mensagem.emit("A porta do hangar abriu.")
		objetivo_mudou.emit(ENTRAR_NA_NAVE)
		return
	mensagem.emit("Trancada. O painel pede a chave do comandante.")
	if not tem_energia:
		objetivo_mudou.emit(ACHAR_A_CHAVE)


func _usar_porta_da_cabine() -> void:
	mensagem.emit("Sem energia. A porta não abre.")
	objetivo_mudou.emit(LEVAR_FUSIVEL if tem_fusivel else RELIGAR)


func _vasculhar(armario: ObjetoDaNave) -> void:
	armario.texto_acao = ""
	ruido.emit(armario.global_position)
	if armario != _armario_do_fusivel:
		mensagem.emit("Vazio.")
		return
	tem_fusivel = true
	maquinas.quadro.texto_acao = "Encaixar o fusível"
	maquinas.quadro.segundos_para_usar = SEGUNDOS_NO_QUADRO
	mensagem.emit("Um fusível!")
	objetivo_mudou.emit(LEVAR_FUSIVEL)


func _usar_quadro() -> void:
	if not tem_fusivel:
		mensagem.emit("Falta um fusível no quadro.")
		objetivo_mudou.emit(ACHAR_FUSIVEL)
		return
	tem_energia = true
	maquinas.quadro.texto_acao = ""
	maquinas.ligar_quadro()
	porta_da_cabine.destrancar()
	ruido.emit(maquinas.quadro.global_position)
	mensagem.emit("A energia voltou. Parte da nave acendeu.")
	objetivo_mudou.emit(PEGAR_NA_CABINE)
	energia_ligada.emit()


func _pegar_a_chave() -> void:
	tem_chave = true
	em_fuga = true
	cabine.tirar_a_chave()
	porta_do_hangar.texto_acao = TEXTO_DE_USAR_A_CHAVE
	porta_do_hangar.segundos_para_usar = SEGUNDOS_ABRINDO_O_HANGAR
	mensagem.emit("O alarme disparou!")
	objetivo_mudou.emit(CORRER)
	fuga_comecou.emit()
