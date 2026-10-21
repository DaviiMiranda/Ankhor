# Cofres e puzzles de código

Um **cofre** guarda um prêmio atrás de um código de dígitos. O código nunca aparece escrito de uma vez: o jogador junta **pistas espalhadas pela sala** (documentos) e vai **testando as combinações** até acertar. O primeiro cofre está na cabine de projeção do Cine Andrômeda, no Centro de Convivência ([`../fases/centro_de_convivencia.md`](../fases/centro_de_convivencia.md), seção 7.5). O segundo é o **cofre do bufê** do Self Nebulosa, na mesma fase (seção 8.1 do mesmo documento).

## Como funciona

- **Abrir o painel:** perto do cofre, `E` abre um painel com os dígitos e **pausa o jogo**. Cima e baixo trocam o número da casa, os lados trocam de casa, `E` confirma e `Esc` sai.
- **Errar:** o visor avisa "CÓDIGO INVÁLIDO" e o painel continua aberto. Não há limite de tentativas nem castigo: o perigo da sala é outro.
- **Acertar:** o visor mostra "COFRE ABERTO", o painel fecha, o cofre muda para o desenho aberto e o prêmio **cai no chão** perto dele (um `ItemNoChao` por unidade). Assim o prêmio não se perde se o inventário estiver cheio no limite do item (por exemplo, 2 cápsulas de clarão): o jogador pega quando puder.
- **O prêmio no chão** vem do `Recompensa.soltar` (`scripts/sistemas/recompensa.gd`), que os outros puzzles com prêmio também usam (a trava do plotter, a arara e o quadro do bar). Ele aceita um `Item` (vira `ItemNoChao`) ou uma cena pronta, como a `pilha_no_chao.tscn`.
- **Persistência:** a abertura fica na marca `Progresso` do cofre. Ao voltar à sala, o cofre continua aberto e, se o prêmio ainda não foi pego, ele reaparece no chão; se já foi pego, não volta.

## Como montar um cofre numa sala

A cena é `cenas/sistemas/cofre.tscn` (script `scripts/sistemas/cofre.gd`, que herda do `PainelCodigo` da Biblioteca). Campos do Inspetor:

| Campo | Para quê |
|---|---|
| `codigo` | O código, com quantos dígitos quiser (cada casa vai de 0 a 9). |
| `marca` | A marca que registra que o cofre foi aberto. Uma por cofre. |
| `item_ao_abrir` | O `Item` do prêmio (`dados/itens/*.tres`). |
| `quantidade` | Quantas unidades caem. |
| `aviso_aberto` | A frase que aparece ao abrir. |
| `textura_apagado` e `textura_aberto` | O desenho fechado e o aberto. |

No Centro de Convivência o cofre entra pela lista `"cofres"` da sala em `assets/modelagem/salas/centro_de_convivencia/salas_convivencia.py` (posição, código, item, quantidade, marca e aviso).

## Como desenhar o puzzle

1. Escolha as **pistas**: um documento que explica a regra sem dar o código (ex.: "o código são as poltronas dos meus três amigos, sem a fileira") e os documentos que dão cada número.
2. Escolha **onde** esconder cada pista: uma à vista, outras onde o jogador precise procurar (embaixo de uma fileira de poltronas, num nicho).
3. Se o código for a junção de vários números, a **ordem** pode ficar de fora de propósito: com 3 números são só 6 tentativas.
4. Escreva a **anotação** de cada documento com o número, porque ela entra no Caderno e o jogador pode consultá-la fora do painel (`N`).
