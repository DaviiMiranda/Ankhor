# Fase — Labirinto (subsolo)

> **Status:** Jogável (primeira versão)  
> **Área:** subsolo escuro do centro de pesquisa da Âncora  
> **Ordem na história:** a definir. Não é necessariamente a fase depois da Biblioteca. Por enquanto se entra pelo menu **Fases**.

---

## 1. Visão geral

Um labirinto de corredores de concreto no escuro. O Gabriel começa no canto de baixo à esquerda, com uma lanterna no chão ao lado, e precisa chegar à **porta de SAÍDA** (placa verde) no alto à direita, fugindo de três robôs.

- **Cena:** `cenas/salas/labirinto.tscn` · **Script:** `scripts/salas/labirinto.gd` (herda de `Sala`)
- **Mapa:** `dados/labirinto/mapa_labirinto.tres` (texto, uma letra por bloco)
- **Arte e mapa gerados por:** `assets/modelagem/salas/labirinto/gerar_labirinto.py`
- **Trilha:** `cenas/sistemas/musica_labirinto.tscn` (ver seção 5)

---

## 2. Como o mapa é feito

O labirinto é **sorteado uma vez** (semente fixa, sempre o mesmo) pelo gerador em Python e salvo como texto. Duas grades:

- **Lógica (12 × 8 salinhas):** é onde o labirinto é sorteado por **busca em profundidade com volta atrás**, e é o **grafo** da patrulha dos robôs.
- **De blocos (37 × 25, blocos de 32 px):** cada salinha vira 2 × 2 blocos de chão; paredes têm 1 bloco. É nela que rodam o **A\*** e a **BFS**.

A busca em profundidade gera uma árvore (um só caminho entre dois pontos). Depois, **18% das paredes internas são derrubadas** para criar ciclos: sempre dá para dar a volta num quarteirão e despistar.

Legenda do mapa:

| Letra | O que é |
|---|---|
| `#` | parede |
| `.` | chão |
| `G` | onde o Gabriel começa |
| `T` | a lanterna (só aparece se ele ainda não tem) |
| `C` | checkpoint (2: a 40% e a 75% do caminho mais curto até a saída) |
| `P` | pilha (3, em becos sem saída) |
| `L` | lampião de emergência (8, em cruzamentos) |
| `V` | Sentinela · `R` Rastreador (nascem longe do início) |
| `D` | porta de saída (na parede de cima) · `S` gatilho da saída |

Para mudar o mapa: altere o `.tres` à mão (mantendo o formato) ou mude `SEMENTE`/`FRACAO_CICLOS` no gerador e rode `python assets/modelagem/salas/labirinto/gerar_labirinto.py` (com `PREVIA=1` ele salva uma imagem do mapa inteiro).

### Por que corredores de 2 blocos
Na vista do jogo (lateral com profundidade), a parede tem 40 px de altura e cobre o que está logo atrás dela. Com corredor de 1 bloco, a parede de baixo cobriria o corredor inteiro. Com 2 blocos, sobra uma faixa de chão visível, e quem anda rente à parede de baixo some da cintura para baixo. Por isso **os itens ficam sempre na fileira de cima** de cada corredor.

### Como a sala se monta
`labirinto.gd` lê o mapa ao carregar e cria: o chão (uma textura repetida), um nó por bloco de parede (topo + face da frente, no y-sort), a colisão (retângulos juntando blocos vizinhos da mesma fileira), os oclusores de luz, os detalhes do chão (marcas de garra, poças, papéis) e os marcadores.

---

## 3. Robôs

| | Sentinela | Rastreador |
|---|---|---|
| Quantos | 2 | 1 |
| Aparência | 2,1 m, curvada, braços longos, um olho-farol vermelho | quadrúpede baixo, três olhos, antenas parabólicas |
| Sentido forte | **Visão**: cone de 60° até 170 px (×1,7 com a lanterna acesa); o farol mostra para onde ela olha | **Audição**: ouve passos pelos corredores (×1,8); visão curta (80 px) e larga (100°) |
| Velocidade (patrulha / perseguição) | 22 / 44 px/s | 30 / 62 px/s |
| Como escapar | apagar a lanterna, agachar (alcance ×0,6) e sair do cone | andar agachado (não faz barulho) e não correr perto dele |

O Gabriel anda a 45 px/s e corre a 81 px/s: consegue fugir correndo, mas correr faz barulho e o Rastreador escuta de longe.

A IA (máquina de estados, cone por produto escalar, BFS do som, A\*, Markov) está em [`../computacao/ia_e_perseguicao.md`](../computacao/ia_e_perseguicao.md) e [`../personagens/robos.md`](../personagens/robos.md).

---

## 4. Luz e escuridão

- `CanvasModulate` quase preto (0,13): sem luz, só se vê a silhueta das paredes.
- A lanterna do Gabriel, os 8 lampiões, o farol vermelho da Sentinela, os olhos dos robôs (desenhados **sem luz**, sempre acesos) e a placa verde da saída.
- **De onde sai a luz:** o feixe da lanterna sai da mão do Gabriel e o farol da Sentinela sai da testa (as posições da testa de cada vista estão no Inspetor do robô, grupo *Testa*). A **sombra**, porém, é calculada a partir de um ponto no chão, e só a textura da luz é deslocada até a mão ou a testa (`offset` da `PointLight2D`). Sem isso, um robô encostado numa parede teria a testa "dentro" da sombra da parede e o farol apagaria.
- **Sombras:** cada fileira de parede tem um `LightOccluder2D`; a lanterna e o farol projetam sombra. As paredes em si ficam numa camada de luz separada (`light_mask = 2`), acesa por um segundo feixe sem sombra, para o bloco atingido pela luz aparecer.

---

## 5. Trilha adaptativa

Duas camadas, **mesmo andamento e mesma duração** (100 BPM, 38,4 s, Ré frígio), tocando juntas desde o início:

- **Tensão** (sempre): drone grave, coração, metal arrastado, máquinas ao longe, cordas agudas crescendo.
- **Perseguição** (começa muda): tambores, baixo martelando o meio-tom Ré–Mi♭, golpes de metal, tom de Shepard subindo sem parar e o alarme dos robôs.

Quando um robô vê o Gabriel, a camada de perseguição sobe em 0,8 s; quando todos desistem, desce em 4 s. Como as duas estão sincronizadas, a música "acorda" em vez de trocar. Composição e matemática em `assets/modelagem/audio/gerar_trilha_labirinto.py`.

---

## 6. Ainda não feito

- Esconderijos (armários) e distrações (arremesso) do GDD.
- Ligar o labirinto ao resto do campus (de onde se entra, para onde a saída leva). Hoje a saída volta ao menu.
- Rotina de patrulha por grade horária (coloração de grafos): hoje a patrulha é só a cadeia de Markov.
