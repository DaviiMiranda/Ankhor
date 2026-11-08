# Difusão do gás e os outros cálculos das mecânicas de fase

## 1. A equação do gás

O gás do setor B do Bunker é a **equação da difusão** resolvida numa grade, com o método das diferenças finitas:

```
novo[x, y] = atual[x, y] + k · ∇²atual[x, y] − p · atual[x, y]

∇²atual[x, y] = esquerda + direita + cima + baixo − 4 · atual[x, y]
```

- **`∇²` é o laplaciano discreto:** compara a célula com a média das quatro vizinhas. Quem tem menos gás que os vizinhos recebe; quem tem mais, perde.
- **`k` é a difusão** (`difusao = 0,22`). O método só é estável com `k ≤ 0,25` na grade 2D; acima disso os valores oscilam e explodem.
- **`p` é a perda** (`perda = 0,002`). Com o exaustor ligado, sobe para `0,08`. Como o gás encolhe 8% a cada passo, em 6 s (60 passos) sobra `0,92⁶⁰ ≈ 0,7%`.
- **Fontes:** seis células do corredor (os vazamentos) ficam sempre em 1 enquanto não há energia.
- **Bordas:** nas pontas do corredor o valor de fora é 0, então o gás some aos poucos. Em cima e embaixo a parede devolve o próprio valor da célula: nada atravessa.
- **Passos:** a grade tem 94 × 12 células de 16 px e anda 10 vezes por segundo. Ao carregar a sala, rodam 300 passos para o gás já aparecer espalhado.

O código está em `scripts/sistemas/zona_de_gas.gd`.

## 2. Da grade para a imagem

A cada passo, a densidade vai para uma textura de 94 × 12 pixels (`Image.FORMAT_RF`). O shader `shaders/gas.gdshader` faz o resto:

1. **Interpolação linear** da GPU: a grade grossa vira uma mancha contínua.
2. **Ruído de valor em três oitavas (FBM):** dá o aspecto de nuvem, e as coordenadas andam com o tempo.
3. **`smoothstep`** da densidade para a opacidade.

O que fere é a densidade, não o desenho: `densidade_em(ponto)` lê a célula do Gabriel.

## 3. Outros cálculos

| Mecânica | Conteúdo | Onde |
|---|---|---|
| Perseguição entre salas | O tempo de chegada é `distância / velocidade`. O robô entra pela aresta (a porta) que o jogador usou no grafo de salas. | `scripts/sistemas/perseguicao_entre_salas.gd` |
| Sonar | BFS na grade da sala: `distancias(origem, limite)` dá o número de passos até cada célula, e a célula acende quando `passos · bloco ≤ velocidade · tempo`. É o mesmo cálculo do som dos robôs, agora visível. | `scripts/itens/pulso_sonar.gd` |
| Microgame da cabine | Onda triangular `pingpong(fase, 1)`. A largura da faixa é fixa e encolhe 25% se o Gabriel está cansado. | `scripts/sistemas/esconderijo_cabine.gd` |
| Barulho da máscara e da Célula | A BFS do som, repetida com o tempo. | `Robo.fazer_barulho` em `scripts/personagens/robo.gd` |
