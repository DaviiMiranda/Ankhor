class_name Criacao
extends RefCounted

const ARMA: Item = preload("res://dados/itens/arma_impulso.tres")
const PILHAS_POR_BALA := 3


static func balas() -> int:
	return Inventario.unidades(ARMA.id)


static func motivo_de_nao_criar() -> String:
	if not Inventario.tem(ARMA.id):
		return "Você ainda não tem a arma de impulso"
	if balas() >= ARMA.maximo_unidades:
		return "Balas no máximo"
	var faltam := PILHAS_POR_BALA - Inventario.pilhas()
	if faltam > 0:
		return "Faltam %d pilha%s" % [faltam, "" if faltam == 1 else "s"]
	return ""


static func criar_bala() -> bool:
	if not motivo_de_nao_criar().is_empty():
		return false
	Inventario.definir_pilhas(Inventario.pilhas() - PILHAS_POR_BALA)
	Inventario.definir_unidades(ARMA, balas() + 1)
	Inventario.mudou.emit()
	return true
