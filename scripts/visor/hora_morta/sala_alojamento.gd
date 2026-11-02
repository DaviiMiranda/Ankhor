class_name SalaAlojamento
extends SalaDaNave


func _decorar() -> void:
	lampada_de_teto(Vector3(0.0, tamanho.y, 0.6), LampadaDaNave.Estado.ACESA, 3.5, COR_QUENTE, 2.0)
	for lado: float in [-1.0, 1.0]:
		_beliche(lado * 2.45)
	bloco_solido(Vector3(1.1, 0.75, 0.7), Vector3(0.0, 0.375, 2.55), material("parede_escura"))
	bloco(Vector3(1.14, 0.03, 0.74), Vector3(0.0, 0.76, 2.55), material("moldura"))
	placa("ALOJAMENTO", Vector3(0.0, 1.9, tamanho.z / 2.0 - 0.012), PI)


func _beliche(x: float) -> void:
	for y: float in [0.45, 1.35]:
		bloco_solido(Vector3(0.9, 0.1, 2.0), Vector3(x, y, 1.2), material("moldura"))
		bloco(Vector3(0.82, 0.12, 1.9), Vector3(x, y + 0.1, 1.2), material("veludo"))
	for z: float in [0.22, 2.18]:
		tubo(0.025, 1.7, Vector3(x, 0.85, z), material("corrimao"), Vector3.UP)
