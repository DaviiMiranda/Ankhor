class_name TerminalComEnergia
extends Interagivel

@export var marca_energia: String = "energia"
@export var item_necessario: String = "disquete_clarice"
@export var documento: Documento
@export var marca_ao_ler: String = "codigo_grade"
@export var aviso_desligado: String = "O terminal está desligado. Sem energia, não liga."
@export var aviso_sem_item: String = "O terminal ligou. Pede um disquete."


func interagir() -> void:
	if not Progresso.tem(marca_energia):
		Inventario.aviso.emit(aviso_desligado)
	elif not Inventario.tem(item_necessario):
		Inventario.aviso.emit(aviso_sem_item)
	elif documento:
		Progresso.marcar(marca_ao_ler)
		Caderno.ler(documento)
