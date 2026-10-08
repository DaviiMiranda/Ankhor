# Gabriel — visual

Os sprites deste personagem ficam nesta mesma pasta. Todos saem do
`assets/modelagem/personagens/pixelar_gabriel.py`, a partir das referências em
`assets/modelagem/personagens/gabriel_referencia/`. Para mudar o visual, troque a
referência e rode de novo:

```bash
python assets/modelagem/personagens/pixelar_gabriel.py
```

Não rode o `gerar_gabriel.py` (o modelo 3D antigo): ele sobrescreve estes sprites.

## Presente
Estudante de 2026 numa noite de estudo: moletom **vermelho** de capuz, com cordões
cinza e bolso canguru, calça jeans azul, tênis cinza-escuro. Cabelo castanho curto,
com volume em cima. Sem mochila.

## Sonho
_A definir._

## Paleta
40 cores, iguais em todas as vistas e animações (escolhidas pelo k-médias a partir
das referências). Contorno de 1 pixel num tom escuro da própria parte (vinho no
moletom, azul-marinho na calça, marrom no cabelo). Os retratos têm uma paleta própria,
de 48 cores, igual nos cinco.

## Tamanho do sprite
Quadro de 96 × 112 (resolução dobrada, escala 0,5 no Godot). O Gabriel ocupa 99 px de
altura, da linha 8 à 106; o pé fica sempre na linha 106 e o centro do corpo na coluna 47.
Retratos de 80 × 80, mostrados em 40 × 40 na caixa de diálogo.

## Animações
| Arquivo | Quadros | Como é feita |
|---|---|---|
| `gabriel_<vista>.png` | 1 | lado e frente vêm da referência; as costas são montadas a partir da frente; os dois 3/4 são o boneco da pose de passo (cabeça, tronco e braços da pose, pernas da vista de lado) com os membros retos |
| `gabriel_andar_<vista>.png` | 12 | de lado e nos dois 3/4: braços, coxas, canelas e pés giram nas juntas (boneco recortado); de frente e de costas: quatro poses desenhadas, cada uma em 3 quadros, com o cabelo e a calça repintados nos tons do Gabriel parado. Em todas os braços balançam ao contrário das pernas |
| `gabriel_parado_<vista>.png` | 8 | respiração: o peito sobe 2 px e a cabeça vai junto, atrasada |
| `gabriel_retrato_<nome>.png` | 1 | `normal`, `preocupado`, `surpreso`, `bravo`, `envergonhado` |

Vistas: `lado`, `frente`, `tres_quartos`, `costas`, `tres_quartos_costas`.

## Referências
`assets/modelagem/personagens/gabriel_referencia/`: `frente.png` (de frente, em alta
resolução), `vistas.webp` (lado, frente e lado), `expressoes.webp` (as cinco expressões) e
`andar_diagonal.webp` (um passo de 3/4 de frente e um de 3/4 de costas), `andar_frente.webp` e
`andar_costas.webp` (quatro poses andando, de frente e de costas).
