# Gabriel — visual

Os sprites deste personagem ficam nesta mesma pasta. Todos saem do
`assets/modelagem/personagens/gerar_gabriel.py` (modelo 3D do Blender, o mesmo método dos
outros personagens), que roda sem abrir a janela:

```bash
blender -b --factory-startup --python assets/modelagem/personagens/gerar_gabriel.py
```

Não rode o `pixelar_gabriel.py` direto: ele é a versão em pixel art desenhada (#74), que foi
desfeita (ver `docs/decisoes.md`, 2026-10-15), e sobrescreveria estes sprites. Ele fica no
repositório só porque o `pixelar_clarice.py` e o `pixelar_seg_prologo.py` usam as ferramentas dele.

## Presente
Estudante de 2026 numa noite de estudo: moletom **vermelho-tijolo** de capuz, com cordões
claros e bolso canguru, calça jeans azul, tênis claro e mochila verde-escura nas costas.
Cabelo castanho curto e arrepiado. Ombros caídos e cabeça um pouco baixa: nada de herói.

## Sonho
_A definir._

## Paleta
Até 40 cores, iguais em todas as vistas e animações. O moletom é vermelho de propósito: os
cenários são verdes, bege, cinza e o escuro frio dos subsolos, e um tom quente faz o jogador
achar o Gabriel na tela.

## Tamanho do sprite
Quadro de 96 × 112 (resolução dobrada, escala 0,5 no Godot). O pé fica sempre na linha 106.
Retratos de 80 × 80, mostrados em 40 × 40 na caixa de diálogo.

## Animações
| Arquivo | Quadros | O que é |
|---|---|---|
| `gabriel_<vista>.png` | 1 | parado, em cada vista |
| `gabriel_andar_<vista>.png` | 12 | caminhada (dois passos), um arquivo por vista |
| `gabriel_parado_<vista>.png` | 8 | respiração |
| `gabriel_retrato_<nome>.png` | 1 | `normal`, `preocupado` e `surpreso` |

Vistas: `lado`, `frente`, `tres_quartos`, `costas`, `tres_quartos_costas`.

## Referências
`gabriel_referencia.png`: frente, 3/4, lado e costas, e os retratos.
