class_name ModoCombate
extends RefCounted

const ID_CHECKPOINT := "modo_combate"
const CENA_RETORNO := "res://cenas/salas/centro_de_convivencia/praca_central.tscn"
const PONTO_RETORNO := Vector2(1000, 330)
const SEGUNDOS_PROTEGIDO_AO_VOLTAR := 2.0

static var ativo := false


static func ativar() -> void:
	Checkpoints.limpar()
	ativo = true
	Checkpoints.marcar(ID_CHECKPOINT, CENA_RETORNO, PONTO_RETORNO)
	Vida.limpar()
