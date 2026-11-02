class_name SalaDeposito
extends SalaDaNave

const TEXTO_DO_ARMARIO := "Vasculhar o armário"
const SEGUNDOS_VASCULHANDO := 3.0
const LUGARES_DOS_ARMARIOS: Array[Vector3] = [Vector3(-3.65, 0.0, -2.0), Vector3(-3.65, 0.0, 1.3), Vector3(2.4, 0.0, 3.1)]

var armarios: Array[ObjetoDaNave] = []


func _decorar() -> void:
	lampada_de_teto(Vector3(0.0, tamanho.y, 0.0), LampadaDaNave.Estado.QUEBRADA, 2.4)
	for lugar in LUGARES_DOS_ARMARIOS:
		_montar_armario(lugar)
	_montar_prateleira(Vector3(-1.2, 0.0, 3.05))
	_montar_prateleira(Vector3(2.4, 0.0, -2.9))
	caixote(Vector3(-1.5, 0.0, -0.8), Vector3(1.0, 0.8, 0.9))
	caixote(Vector3(-1.4, 0.8, -0.85), Vector3(0.6, 0.5, 0.6))
	caixote(Vector3(1.2, 0.0, 1.7), Vector3(0.9, 1.1, 1.0))
	placa("DEPÓSITO", Vector3(0.0, 2.1, tamanho.z / 2.0 - 0.012), PI)


func _montar_armario(lugar: Vector3) -> void:
	var no_sul := lugar.z > 2.0
	var medidas := Vector3(0.9, 1.9, 0.55) if no_sul else Vector3(0.55, 1.9, 0.9)
	bloco_solido(medidas, lugar + Vector3.UP * 0.95, material("parede_escura"))
	var frente := Vector3(0.0, 0.0, -0.285) if no_sul else Vector3(0.285, 0.0, 0.0)
	bloco(Vector3(0.05, 0.2, 0.05), lugar + frente + Vector3.UP * 1.1, material("corrimao"))
	bloco(Vector3(0.05, 0.05, 0.05), lugar + frente + Vector3.UP * 1.65, material("perigo"))
	var novo := novo_objeto(TEXTO_DO_ARMARIO, lugar + frente + Vector3.UP * 1.1, SEGUNDOS_VASCULHANDO)
	armarios.append(novo)


func _montar_prateleira(lugar: Vector3) -> void:
	bloco_solido(Vector3(2.0, 1.9, 0.5), lugar + Vector3.UP * 0.95, material("borracha"))
	for y: float in [0.4, 1.0, 1.6]:
		bloco(Vector3(2.06, 0.05, 0.56), lugar + Vector3.UP * y, material("moldura"))
		bloco(Vector3(0.5, 0.3, 0.4), lugar + Vector3(-0.5, y + 0.17, 0.0), material("parede_escura"))
		bloco(Vector3(0.35, 0.22, 0.34), lugar + Vector3(0.4, y + 0.13, 0.0), material("cabo_vermelho"))
