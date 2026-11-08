class_name Criacao
extends RefCounted

const ARMA: Item = preload("res://dados/itens/arma_impulso.tres")
const FLASH: Item = preload("res://dados/itens/clarao.tres")
const CHIPS: Item = preload("res://dados/itens/pedra.tres")
const PILHAS_POR_BALA := 3
const PILHAS_POR_FLASH := 1


static func balas() -> int:
	return Inventario.unidades(ARMA.id) if Inventario.tem(ARMA.id) else 0


static func flashes() -> int:
	return Inventario.unidades(FLASH.id) if Inventario.tem(FLASH.id) else 0


static func chips() -> int:
	return Inventario.unidades(CHIPS.id) if Inventario.tem(CHIPS.id) else 0


static func motivo_de_nao_criar_bala() -> String:
	if not Inventario.tem(ARMA.id):
		return "Você ainda não tem a arma de impulso"
	if balas() >= ARMA.maximo_unidades:
		return "Balas no máximo"
	return _motivo_por_ingredientes(PILHAS_POR_BALA)


static func motivo_de_nao_criar_flash() -> String:
	if flashes() >= FLASH.maximo_unidades:
		return "Flashes no máximo"
	var motivo := _motivo_por_ingredientes(PILHAS_POR_FLASH)
	if not motivo.is_empty():
		return motivo
	if not Inventario.tem(FLASH.id) and chips() > 1 and not _tem_vaga():
		return "Inventário cheio"
	return ""


static func _motivo_por_ingredientes(pilhas_necessarias: int) -> String:
	if chips() < 1:
		return "Falta 1 chip"
	var faltam := pilhas_necessarias - Inventario.pilhas()
	if faltam > 0:
		return "Faltam %d pilha%s" % [faltam, "" if faltam == 1 else "s"]
	return ""


static func _tem_vaga() -> bool:
	for linha in Inventario.grade:
		if null in linha:
			return true
	return false


static func _gastar_ingredientes(pilhas_necessarias: int) -> void:
	var restantes := chips() - 1
	if restantes == 0:
		Inventario.remover(CHIPS.id)
		Inventario.estado.erase(CHIPS.id)
	else:
		Inventario.definir_unidades(CHIPS, restantes)
	Inventario.definir_pilhas(Inventario.pilhas() - pilhas_necessarias)


static func criar_bala() -> bool:
	if not motivo_de_nao_criar_bala().is_empty():
		return false
	_gastar_ingredientes(PILHAS_POR_BALA)
	Inventario.definir_unidades(ARMA, balas() + 1)
	Inventario.mudou.emit()
	return true


static func criar_flash() -> bool:
	if not motivo_de_nao_criar_flash().is_empty():
		return false
	_gastar_ingredientes(PILHAS_POR_FLASH)
	if Inventario.tem(FLASH.id):
		Inventario.definir_unidades(FLASH, flashes() + 1)
	else:
		Inventario.adicionar(FLASH)
	Inventario.mudou.emit()
	return true
