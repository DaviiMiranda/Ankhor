class_name Fase
extends Resource

@export var nome: String = ""
@export_file("*.tscn") var cena: String = ""


const PASTA := "res://dados/fases/"
const PASTA_DAS_SALAS := "res://cenas/salas"


func pronta() -> bool:
	return not cena.is_empty()


func pasta_das_salas() -> String:
	var pasta := cena.get_base_dir()
	return cena.get_basename() if pasta == PASTA_DAS_SALAS else pasta


func tem_a_cena(caminho_da_cena: String) -> bool:
	return pronta() and (caminho_da_cena == cena or caminho_da_cena.get_base_dir() == pasta_das_salas())


static func nome_da_cena(caminho_da_cena: String) -> String:
	for arquivo in ResourceLoader.list_directory(PASTA):
		var fase := load(PASTA + arquivo) as Fase
		if fase and fase.tem_a_cena(caminho_da_cena):
			return fase.nome
	return ""
