# Modelo de diálogo

Todo diálogo é um arquivo **JSON** em `dados/dialogos/<nome>.json` (nome em `snake_case`, sem acento). Como funciona no jogo: [`README.md`](README.md).

---

## 1. Formato

```json
{
	"id": "clarice_primeiro_encontro",
	"inicio": "abertura",
	"anotacao": {
		"titulo": "Clarice está viva",
		"texto": "O que o Gabriel anota no caderno quando a conversa termina (opcional)."
	},
	"trechos": {
		"abertura": {
			"falas": [
				{"quem": "Clarice", "retrato": "clarice/clarice_retrato_normal", "texto": "Uma fala."},
				{"quem": "Gabriel", "retrato": "gabriel/gabriel_retrato_surpreso", "texto": "Outra fala."}
			],
			"escolhas": [
				{"texto": "Primeira opção", "vai_para": "ramo_a"},
				{"texto": "Segunda opção", "vai_para": "ramo_b"}
			]
		},
		"ramo_a": {
			"falas": [{"quem": "Clarice", "retrato": "clarice/clarice_retrato_sorrindo", "texto": "..."}],
			"vai_para": "abertura"
		},
		"ramo_b": {
			"falas": [{"quem": "Clarice", "retrato": "clarice/clarice_retrato_seria", "texto": "Fim da conversa."}]
		}
	}
}
```

| Campo | O que é |
|---|---|
| `id` | Nome da conversa. É também o id da anotação no caderno |
| `inicio` | O trecho por onde a conversa começa |
| `anotacao` | Opcional. `titulo` e `texto` que vão para o Caderno do Gabriel no fim |
| `trechos` | Os pedaços da conversa, cada um com um nome |
| `falas` | As falas do trecho, em ordem. `quem` (nome que aparece), `texto` e, opcional, `retrato` |
| `escolhas` | Opcional. As opções que aparecem no fim do trecho. `vai_para` é o nome do trecho seguinte |
| `vai_para` (no trecho) | Opcional. Sem escolhas, a conversa segue direto para esse trecho |

Um trecho **sem escolhas e sem `vai_para`** encerra a conversa.

---

## 2. Tamanho do texto

A tela tem 320 × 180 e a caixa mostra **3 linhas** de ~50 letras (com retrato) ou ~60 (sem retrato). Na prática:

- uma fala com retrato cabe em **até ~130 letras**; se passar, o fim não aparece;
- no máximo **4 escolhas**, de até ~40 letras cada;
- para aspas dentro do texto, use `\"` (é JSON).

---

## 3. Checklist

- [ ] O arquivo é JSON válido (vírgulas, chaves, aspas)? Abra num site de validar JSON se tiver dúvida.
- [ ] Todo `vai_para` aponta para um trecho que existe?
- [ ] Existe pelo menos um caminho que chega a um trecho que encerra (para não prender o jogador)?
- [ ] Os retratos existem em `assets/sprites/personagens/`? Hoje: `clarice/clarice_retrato_{normal,sorrindo,seria}` e `gabriel/gabriel_retrato_{normal,surpreso,preocupado}`.
- [ ] Cada fala cabe em 3 linhas?
- [ ] A fala combina com a ficha do personagem em [`../historia/personagens/`](../historia/personagens/), que faz parte do Enredo Principal (a lei do projeto)? Na dúvida, peça para o agente `roteirista` revisar.
