# Personagens

Uma pasta por personagem. Cada pasta tem a ficha `visual.md` e os sprites daquele personagem.

| Pasta | Personagem |
|---|---|
| `gabriel/` | Gabriel |
| `vigia/` | O Vigia |
| `clarice/` | Clarice (1994), no bunker: sentada na estação de trabalho, retratos da caixa de diálogo |

**Resolução dobrada:** Gabriel e Clarice têm sprites com o dobro de pixels (o Gabriel tem 96 × 112 por quadro) e as cenas usam `scale = 0.5`. Os retratos da caixa de diálogo têm 80 × 80 e aparecem em 40 × 40. Os robôs e o Vigia continuam em 1×. Para um personagem novo em 2×: renderize com o dobro de `px_por_m` e de quadro, e ponha escala 0,5 no `Sprite2D` (o `offset` é em pixels da textura, então também dobra).

Quem cada personagem é está em `docs/gdd.md` (item 3) e em `docs/roteiro/`. Mudança de aparência que mexe na história passa pelo roteiro e vai para `docs/decisoes.md`.
