# Zane — visual

Rapaz de uns 20 anos, de 2123, que cuida das comunicações do grupo no computador do bunker. Quem ele é está na ficha [`docs/historia/personagens/zane.md`](../../../../docs/historia/personagens/zane.md), que faz parte do Enredo Principal (a lei do projeto).

![Folha de referência](zane_referencia.png)

## Quem ele é, no visual

Desde 2026-10-17 o corpo segue os retratos desenhados pela equipe (`assets/modelagem/personagens/zane_referencia/expressoes.jpg`).

- **Implantes à vista.** O **braço direito** inteiro é uma prótese de metal, com a junta do cotovelo à mostra e **linhas de luz** no antebraço. Um **visor verde** cobre os dois olhos (uma faixa escura com a lente que brilha). Uma **peça de metal na orelha e na têmpora** (dois pontos de luz), uma **placa de metal na mandíbula** e uma **porta de conexão na nuca**. A luz é o ciano-esverdeado da interface holográfica dos áudios dele.
- **Roupa de um futuro que ninguém reconhece.** Jaqueta técnica **grafite escuro** com **gola alta aberta em duas abas** de borda cinza, painéis cinza nos lados, **zíper na diagonal**, ombreira no ombro esquerdo, linhas de luz e um **hexágono** no peito; a manga do braço de metal é cortada no ombro. Embaixo, a **camiseta preta comprida** aparece. Calça larga e reta com tiras, **botas de sola branca grossa** com um friso de luz.
- **Cabelo branco**, bagunçado: cai na testa, cobre as orelhas e chega até a nuca. A silhueta mais alta e pontuda do grupo.
- **Cor de identificação: grafite com luz verde-ciano.** Nenhum outro personagem é tão escuro, e a luz o separa do cenário. O amarelo-ácido da ficha (e do desenho antigo) continua só na cor do nome dele na caixa de diálogo.
- **Postura:** o contrário do Gabriel cansado. Peito aberto, queixo erguido, braços um pouco afastados e um passo largo e saltado.
- Os implantes ficam do lado **direito** dele, o lado virado para a câmera nas vistas de lado e de 3/4.

## Sprites

Todos em `assets/sprites/personagens/zane/`, gerados por `assets/modelagem/personagens/gerar_zane.py` (Blender, sem abrir a janela). São os mesmos arquivos e tamanhos do Gabriel:

| Arquivo | Tamanho | O que é |
|---|---|---|
| `zane_<vista>.png` | 96 × 112 | parado, em cada vista: `lado`, `frente`, `tres_quartos`, `costas`, `tres_quartos_costas` |
| `zane_andar_<vista>.png` | 12 quadros de 96 × 112 | caminhada (dois passos), um arquivo por vista |
| `zane_parado_<vista>.png` | 8 quadros de 96 × 112 | respirando, um arquivo por vista |
| `zane_retrato_normal.png` | 80 × 80 | retrato da caixa de diálogo (mostrado em 40 × 40): boca reta, o visor verde |
| `zane_retrato_confiante.png` | 80 × 80 | sorriso de lado e um brilho no visor |
| `zane_retrato_assustado.png` | 80 × 80 | boca aberta, uma gota de suor e o visor falhando: o medo que ele não admite |
| `zane_retrato_empolgado.png` | 80 × 80 | sorriso aberto e faíscas verdes em volta do visor |
| `zane_retrato_desconfiado.png` | 80 × 80 | cenho franzido e a boca torta |
| `zane_retrato_concentrado.png` | 80 × 80 | uma moldura de varredura em volta do rosto: ele está invadindo algo |
| `zane_retrato_frustrado.png` | 80 × 80 | dentes cerrados e o visor com falhas de imagem |
| `zane_referencia.png` | — | frente, 3/4, lado e costas, e os retratos antigos (os três primeiros) |

Os **retratos** não vêm mais do `gerar_zane.py`: saem do `assets/modelagem/personagens/pixelar_retratos.py` (`python assets/modelagem/personagens/pixelar_retratos.py zane`), a partir da folha desenhada em `assets/modelagem/personagens/zane_referencia/expressoes.jpg`. O `gerar_zane.py` só desenha os retratos do Blender na folha de referência e **não** grava os `zane_retrato_*.png`, então pode ser rodado sem perder os novos. O corpo dos sprites (`gerar_zane.py`) segue o mesmo desenho dos retratos: cabelo branco, visor verde e jaqueta escura com linhas de luz.

- **Escala:** a mesma de todos os personagens (1,75 m do Gabriel = 48 px na tela). O corpo dele tem 1,80 m, e o topete passa disso.
- **Resolução dobrada:** como o Gabriel, os sprites saem com o dobro de pixels e a cena usa `scale = Vector2(0.5, 0.5)`. Para a esquerda, o Godot espelha o sprite de lado.
- **Caminhada e respiração:** as do `comum.py`, com amplitudes próprias (`PASSO` e `RESPIRAR` no script).
- **Paleta:** 48 cores para tudo.

## No jogo

`cenas/personagens/zane.tscn`: o Zane parado, respirando, com os pés sólidos (o Gabriel não atravessa). O script é o `scripts/personagens/personagem_parado.gd`, que escolhe a vista (`vista`) e se ele olha para a esquerda (`olhando_para_esquerda`). Por enquanto ele só aparece na sala de teste (`cenas/salas/sala_teste.tscn`). Onde ele aparece na história e a função dele na jogabilidade estão pendentes na ficha.

## Para mudar

Edite `gerar_zane.py` (cores em `criar_materiais`, peças em `montar` e `cabeca`, expressões em `expressao`, jeito de andar em `PASSO`) e rode:

```
blender -b --factory-startup --python assets/modelagem/personagens/gerar_zane.py
```

Leva uns 4 minutos e sobrescreve os PNGs dos sprites (menos os retratos) e o `zane.blend`.
