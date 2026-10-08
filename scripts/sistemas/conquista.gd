class_name Conquista
extends Resource

enum Gatilho { MANUAL, ITEM, MORTE, ANOTACOES }

@export var id: String = ""
@export var nome: String = ""
@export_multiline var descricao: String = ""
@export var secreta: bool = false
@export var gatilho: Gatilho = Gatilho.MANUAL
@export var alvo: String = ""
@export var quantidade: int = 1
