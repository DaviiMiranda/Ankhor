class_name PainelExame
extends Control

const ESCALA_DETALHE := 0.5
const LADO_ICONE_AMPLIADO := 64.0

@onready var area: Control = $Area
@onready var imagem: TextureRect = $Area/Imagem
@onready var nome: Label = $Nome
@onready var descricao: Label = $Descricao


func mostrar(item: Item) -> void:
	nome.text = item.nome
	descricao.text = item.descricao
	imagem.texture = item.imagem_detalhe if item.imagem_detalhe else item.icone
	if imagem.texture:
		imagem.size = imagem.texture.get_size() * _escala(item)
		imagem.position = ((area.size - imagem.size) / 2.0).round()


func _escala(item: Item) -> float:
	if item.imagem_detalhe:
		return ESCALA_DETALHE
	return LADO_ICONE_AMPLIADO / item.icone.get_width()
