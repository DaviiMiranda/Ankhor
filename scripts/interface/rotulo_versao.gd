class_name RotuloVersao
extends CanvasLayer

const TEXTO_SEM_VERSAO := "versão de desenvolvimento"

@onready var rotulo: Label = $Rotulo


func _ready() -> void:
	var versao: String = ProjectSettings.get_setting("application/config/version", "")
	rotulo.text = "v%s" % versao if not versao.is_empty() else TEXTO_SEM_VERSAO
