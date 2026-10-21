class_name ReleRede
extends NoHackeavel

@export var rele: String = "eletronica"


func _ready() -> void:
	id = "rele_" + rele
	marca_ao_destrancar = RedeEnergiaDtec.marca_do_rele(rele)
	super()


func destrancar() -> void:
	var antes := RedeEnergiaDtec.caminho_de_agora()
	var cortados := RedeEnergiaDtec.reles_cortados()
	cortados.append(rele)
	var depois := RedeEnergiaDtec.caminho_ativo(cortados)
	aviso_destrancada = _aviso(antes, depois)
	super()
	if depois.caminho.is_empty():
		Progresso.marcar(RedeEnergiaDtec.MARCA_REDE_CORTADA)


func _aviso(antes: Dictionary, depois: Dictionary) -> String:
	if depois.caminho.is_empty():
		return "A rede caiu. A grade do Lab Central perdeu a trava."
	if depois.caminho == antes.caminho:
		return "Relé cortado. A energia nem passava por aqui."
	return "Relé cortado. A energia desviou: " + RedeEnergiaDtec.caminho_em_texto(depois.caminho)
