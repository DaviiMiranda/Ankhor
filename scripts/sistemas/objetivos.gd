class_name Objetivos
extends RefCounted

const GERAL := {
	"nome": "OBJETIVO GERAL",
	"objetivo": "Encontrar os outros jovens puxados pela fenda, descobrir o que aconteceu e achar um jeito de todos voltarem.",
	"passos": [],
	"final": "Seguir em frente e procurar os outros.",
}

const FASES: Array[Dictionary] = [
	{
		"pasta": "/biblioteca/",
		"nome": "BIBLIOTECA",
		"objetivo": "Sair da Biblioteca pela porta da ala leste. A grade de segurança está sem energia e a porta de saída só abre pelo sistema.",
		"passos": [
			{"marcas": ["energia"], "texto": "Achar a chave da manutenção e religar os disjuntores no quadro de energia."},
			{"marcas": ["grade_aberta"], "texto": "Achar o código da grade nos terminais e abrir a grade do salão."},
			{"marcas": ["saida_destrancada"], "texto": "Atender o telefone do balcão: o Zane destranca a porta de saída."},
		],
		"final": "Sair pela porta da ala leste.",
	},
	{
		"pasta": "/bloco_de_salas/",
		"nome": "BLOCO DE SALAS",
		"objetivo": "Encontrar a Clarice, ganhar a confiança dela e sair do Bloco de salas pela porta corta-fogo do 1º andar.",
		"passos": [
			{"marcas": ["alarme_104"], "texto": "Ligar o teste de alarme na sala 104 para tirar o Rastreador da porta da 103."},
			{"marcas": ["molho_devolvido"], "texto": "Achar o molho de chaves perdido na areia da 102 e levar para a Clarice, na 103."},
			{"marcas": ["escada_destrancada"], "texto": "Abrir a grade da escada com a chave que a Clarice dá."},
			{"marcas": ["alicate"], "texto": "No 1º andar, achar o alicate no depósito (206)."},
			{"marcas": ["corrente_cortada"], "texto": "Cortar a corrente da porta corta-fogo com o alicate."},
		],
		"final": "Sair pela porta corta-fogo.",
	},
	{
		"pasta": "/labirinto",
		"nome": "LABIRINTO",
		"objetivo": "Pegar o notebook com o Zane e invadir os três nós de controle, espalhados em três salões. Seis robôs patrulham os corredores.",
		"passos": [],
		"final": "Invadir os três nós, voltar à oficina do Zane e descer pelo alçapão.",
	},
	{
		"pasta": "/centro_de_convivencia/",
		"nome": "CENTRO DE CONVIVÊNCIA",
		"objetivo": "Atravessar a praça, achar a Célula de Energia, ligar o quadro de comutação da cozinha da Pizzaria Quasar e descer pelo elevador de carga.",
		"passos": [
			{"marcas": ["convivencia_energia"], "ou_item": "celula_energia", "texto": "Achar a Célula de Energia na câmara fria do Self Nebulosa."},
			{"marcas": ["convivencia_energia"], "texto": "Resolver o quadro de comutação na cozinha da Pizzaria Quasar."},
		],
		"final": "Descer pelo elevador de carga do Churrasco Solar.",
	},
	{
		"pasta": "/bunker/",
		"nome": "BUNKER",
		"objetivo": "Religar o bunker e chegar à comporta do núcleo, no fim do Corredor B, que leva ao Laboratório.",
		"passos": [
			{"marcas": ["bunker_energia"], "texto": "Descer ao setor B e religar a energia no quadro do gerador, com os 23 m de cabo."},
			{"marcas": ["bunker_comporta_aberta"], "texto": "Ir até a sala de dados: o grupo está lá."},
		],
		"final": "Passar pela comporta do núcleo, no fim do Corredor B.",
	},
	{
		"pasta": "/dtec/",
		"nome": "LABORATÓRIO",
		"objetivo": "Chegar ao núcleo da Âncora, no Lab Central, sem ser pego pelos robôs nem pela lupa do Carlos.",
		"passos": [
			{"marcas": ["dtec_rede_cortada"], "texto": "Ler a rede no telão da Sala de Controle e cortar os três relés: Eletrônica, Servidores e Robótica."},
			{"marcas": ["dtec_console_1", "dtec_console_2"], "texto": "No Lab Central, invadir os dois consoles."},
		],
		"final": "Chegar ao núcleo da Âncora.",
	},
]


static func da_cena(caminho: String) -> Dictionary:
	for fase in FASES:
		if caminho.contains(fase["pasta"]):
			return fase
	return GERAL


static func passo_atual(fase: Dictionary) -> String:
	for passo in fase["passos"]:
		if not _feito(passo):
			return passo["texto"]
	return fase["final"]


static func _feito(passo: Dictionary) -> bool:
	if passo.has("ou_item") and Inventario.tem(passo["ou_item"]):
		return true
	for marca in passo["marcas"]:
		if not Progresso.tem(marca):
			return false
	return true
