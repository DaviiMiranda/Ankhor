# Diana — visual

Estagiária de arquitetura de uns 20 anos, de 1978. Quem ela é está na ficha [`docs/historia/personagens/diana.md`](../../../../docs/historia/personagens/diana.md), que faz parte do Enredo Principal (a lei do projeto).

![Folha de referência](diana_referencia.png)

## Quem ela é, no visual

- **Cabelo** castanho-claro, volumoso e repicado, no estilo dos anos 70, caindo até abaixo dos ombros.
- **Óculos grandes** de armação laranja, com lentes alaranjadas, e **argolas douradas**.
- **Jaqueta** marrom-caramelo de gola larga, com bolsos no peito e no quadril e punhos dobrados, por cima de uma **camiseta listrada** em amarelo, laranja e branco.
- **Calça jeans boca de sino**, azul, com cinto preto, e **botas de plataforma** marrons.
- **Cor de identificação:** a ficha ainda não define uma (a tabela do `resumo.md` está com "—"). A jaqueta e os óculos puxam para o laranja e o marrom.
- **Postura:** a ficha pede uma estagiária sempre em movimento e nervosa (olhando para os lados, mãos inquietas). Os sprites parados ainda não mostram isso; a folha enviada tem só as poses de caminhada.

A direção de arte da ficha falava em "roupa de canteiro de obras e um tubo de plantas". O visual desenhado é mais de estudante dos anos 70 do que de canteiro; o tubo de plantas não aparece.

## Sprites

Todos em `assets/sprites/personagens/diana/`. Os **retratos** e os **sprites parados** são pixel art feita a partir das folhas desenhadas em `assets/modelagem/personagens/diana_referencia/` (`expressoes.jpg` e `andar.jpg`), por dois scripts que só precisam de Python, Pillow e NumPy:

```bash
python assets/modelagem/personagens/pixelar_retratos.py diana
python assets/modelagem/personagens/pixelar_diana.py
```

| Arquivo | Tamanho | O que é |
|---|---|---|
| `diana_<vista>.png` | 96 × 112 | em pé, em cada vista: `lado`, `tres_quartos` e `tres_quartos_costas` |
| `diana_parado_<vista>.png` | 8 quadros de 96 × 112 | respirando, um arquivo por vista |
| `diana_retrato_<nome>.png` | 80 × 80 | retratos da caixa de diálogo (mostrados em 40 × 40): `normal`, `assustada`, `dramatica` (a mão no rosto, a boca aberta), `ansiosa` (roendo a unha, uma gota de suor), `irritada`, `determinada` e `aliviada` (de olhos fechados, sorrindo) |
| `diana_referencia.png` | — | as vistas em pé e os retratos, para conferir |

- **Escala:** a mesma de todos os personagens (1,75 m do Gabriel = 48 px na tela). Ela tem 92 px do alto do cabelo à sola da bota, o que dá uns 1,65 m de corpo mais o volume do cabelo.
- **Resolução dobrada:** como o Gabriel, a cena usa `scale = Vector2(0.5, 0.5)` e `offset = Vector2(-46, -108)`. Para a esquerda, o Godot espelha o sprite.
- **Paleta:** 48 cores para os sprites e 48 para os retratos.
- **Em pé:** todas as poses da folha estão no meio de um passo. Para ela ficar parada, uma perna fica como foi desenhada e a outra é trocada por uma cópia dela (no 3/4 de costas a perna que fica é girada antes, porque estava inclinada). A respiração é a do Gabriel: o peito sobe até 2 px e a cabeça vai junto.
- **3/4 de frente:** a folha vem virada para a esquerda e é espelhada, porque no jogo todos os sprites olham para a direita.

### O que ainda não existe

- **`frente` e `costas`:** a folha não tem Diana de frente nem de costas. A cena usa o 3/4 no lugar de `frente` e o 3/4 de costas no lugar de `costas`.
- **Caminhada (`diana_andar_<vista>.png`):** as poses da folha mostram sempre a mesma perna à frente (a sequência de três poses está desenhada duas vezes), então não há um ciclo de dois passos. Sem esses arquivos, ela **não entra na troca de personagem da sala de teste** (tecla `C`), que carrega os 15 arquivos de cada personagem.

## No jogo

`cenas/personagens/diana.tscn`: a Diana parada, respirando, com os pés sólidos (o Gabriel não atravessa). O script é o `scripts/personagens/personagem_parado.gd`, que escolhe a vista (`vista`) e se ela olha para a esquerda (`olhando_para_esquerda`). Por enquanto ela só aparece na sala de teste (`cenas/salas/sala_teste.tscn`). Na história ela fica na sala 103 do Bloco de salas, com a Clarice; essa cena ainda não a mostra.
