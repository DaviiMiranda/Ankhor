# Personagens

Uma pasta por personagem. Cada pasta tem a ficha `visual.md` e os sprites daquele personagem.

| Pasta | Personagem |
|---|---|
| `gabriel/` | Gabriel |
| `vigia/` | O Vigia |
| `clarice/` | Clarice (1994): sentada na estação de trabalho do bunker, em pé (vistas, caminhada e respiração, como o Gabriel) e retratos |
| `diana/` | Diana (1978): vistas em pé (`lado`, `tres_quartos` e `tres_quartos_costas`), respiração e retratos, feitos a partir de folhas desenhadas (`pixelar_diana.py` e `pixelar_retratos.py`). Ainda sem `frente`, `costas` e caminhada |
| `zane/` | Zane (2123): vistas, caminhada, respiração e retratos, como o Gabriel |
| `baltazar/` | Baltazar (~1750): vistas, caminhada, respiração e retratos, como o Gabriel |
| `rafael/` | **Arte guardada.** Rafael (2008) saiu da história em 2026-10-11 (ver `docs/decisoes.md`): vistas, caminhada, respiração e retratos, como o Gabriel. Não é usada em nenhuma fase |
| `henrique/` | Henrique (2019), o pesquisador: vistas, caminhada, respiração e retratos, como o Gabriel |
| `carlos/` | Carlos (3026), o antagonista: vistas, caminhada, respiração e retratos, como o Gabriel |

**Resolução dobrada:** Gabriel, Clarice, Diana, Zane, Baltazar, Henrique e Carlos têm sprites com o dobro de pixels (o Gabriel tem 96 × 112 por quadro) e as cenas usam `scale = 0.5`. Os retratos da caixa de diálogo têm 80 × 80 e aparecem em 40 × 40. Os robôs e o Vigia continuam em 1×. Para um personagem novo em pé: monte o modelo com as juntas do Gabriel e chame `comum.gerar_em_pe` (ver `gerar_rafael.py`, o exemplo mais curto); ele já sai em 2×. Na cena, escala 0,5 no `Sprite2D` (o `offset` é em pixels da textura, então também dobra).

Quem cada personagem é está em `docs/gdd.md` (item 3) e em `docs/roteiro/`. Mudança de aparência que mexe na história passa pelo roteiro e vai para `docs/decisoes.md`.
