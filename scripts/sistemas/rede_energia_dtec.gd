class_name RedeEnergiaDtec
extends RefCounted

const MARCA_REDE_CORTADA := "dtec_rede_cortada"
const PREFIXO_RELE := "dtec_rele_"
const ANCORA := "ancora"
const GERADORES: Array[String] = ["gerador_norte", "gerador_sul"]
const RELES: Array[String] = ["eletronica", "informatica", "servidores", "quimica", "robotica", "controle"]

const CABOS := {
	["gerador_norte", "informatica"]: 3,
	["gerador_norte", "eletronica"]: 6,
	["gerador_norte", "servidores"]: 7,
	["informatica", "eletronica"]: 4,
	["informatica", "servidores"]: 2,
	["servidores", "controle"]: 1,
	["servidores", "ancora"]: 5,
	["controle", "ancora"]: 2,
	["eletronica", "ancora"]: 5,
	["gerador_sul", "quimica"]: 2,
	["gerador_sul", "robotica"]: 6,
	["quimica", "robotica"]: 2,
	["robotica", "ancora"]: 3,
}

const NOMES := {
	"gerador_norte": "Gerador Norte",
	"gerador_sul": "Gerador Sul",
	"eletronica": "Eletrônica",
	"informatica": "Informática",
	"servidores": "Servidores",
	"quimica": "Química",
	"robotica": "Robótica",
	"controle": "Controle",
	"ancora": "Âncora",
}


static func nos() -> Array[String]:
	var lista: Array[String] = []
	lista.append_array(GERADORES)
	lista.append_array(RELES)
	lista.append(ANCORA)
	return lista


static func vizinhos(no: String) -> Dictionary:
	var resultado := {}
	for cabo in CABOS:
		if cabo[0] == no:
			resultado[cabo[1]] = CABOS[cabo]
		elif cabo[1] == no:
			resultado[cabo[0]] = CABOS[cabo]
	return resultado


static func marca_do_rele(rele: String) -> String:
	return PREFIXO_RELE + rele


static func reles_cortados() -> Array[String]:
	var cortados: Array[String] = []
	for rele in RELES:
		if Progresso.tem(marca_do_rele(rele)):
			cortados.append(rele)
	return cortados


static func caminho_ativo(cortados: Array[String]) -> Dictionary:
	var distancia := {ANCORA: 0}
	var anterior := {}
	var visitados := {}
	while true:
		var atual := ""
		for no in distancia:
			if not visitados.has(no) and (atual.is_empty() or distancia[no] < distancia[atual]):
				atual = no
		if atual.is_empty():
			return {"caminho": PackedStringArray(), "custo": -1}
		if atual in GERADORES:
			return {"caminho": _refazer(atual, anterior), "custo": distancia[atual]}
		visitados[atual] = true
		var arestas := vizinhos(atual)
		for vizinho in arestas:
			if vizinho in cortados or visitados.has(vizinho):
				continue
			var nova: int = distancia[atual] + arestas[vizinho]
			if not distancia.has(vizinho) or nova < distancia[vizinho]:
				distancia[vizinho] = nova
				anterior[vizinho] = atual
	return {}


static func _refazer(gerador: String, anterior: Dictionary) -> PackedStringArray:
	var caminho := PackedStringArray([gerador])
	while caminho[-1] != ANCORA:
		caminho.append(anterior[caminho[-1]])
	return caminho


static func caminho_de_agora() -> Dictionary:
	return caminho_ativo(reles_cortados())


static func caminho_em_texto(caminho: PackedStringArray) -> String:
	var nomes := PackedStringArray()
	for no in caminho:
		nomes.append(NOMES[no])
	return " > ".join(nomes)
