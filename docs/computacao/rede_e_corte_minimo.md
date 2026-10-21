# A rede de energia da Âncora: Dijkstra e corte mínimo

O puzzle do Laboratório ([`../fases/dtec.md`](../fases/dtec.md), seção 3.1, parte 2) usa dois conteúdos de grafos: o **algoritmo de Dijkstra**, que decide por onde a energia corre, e o **corte mínimo de vértices**, que é a resposta do puzzle. O jogador vê os dois acontecerem: o telão da Sala de Controle desenha o grafo e o caminho ativo, e os robôs mudam de rota conforme o caminho muda.

---

## 1. O grafo

A rede é um **grafo não dirigido com pesos**. Os vértices são os dois geradores (no subsolo), os seis relés (um em cada sala de laboratório) e a Âncora. Cada aresta é um cabo, e o peso é o comprimento do cabo em metros.

O desenho do grafo é o do telão da Sala de Controle (`scripts/sistemas/telao_rede.gd`, posições em `POSICOES`). As arestas:

| Cabo | m | Cabo | m |
|---|---|---|---|
| Gerador Norte – Informática | 3 | Controle – Âncora | 2 |
| Gerador Norte – Eletrônica | 6 | Eletrônica – Âncora | 5 |
| Gerador Norte – Servidores | 7 | Gerador Sul – Química | 2 |
| Informática – Eletrônica | 4 | Gerador Sul – Robótica | 6 |
| Informática – Servidores | 2 | Química – Robótica | 2 |
| Servidores – Controle | 1 | Robótica – Âncora | 3 |
| Servidores – Âncora | 5 | | |

O jogador **corta relés** (com o notebook). Cortar um relé tira o vértice do grafo, com todos os cabos dele. Os geradores e a Âncora não podem ser cortados.

---

## 2. Por onde a energia corre: Dijkstra

**No jogo.** A energia sempre corre pelo **caminho mais curto** de um gerador até a Âncora, pelos relés que ainda estão de pé. Quando o jogador corta um relé desse caminho, a energia "desvia" para o próximo caminho mais curto, e o aviso mostra qual é. Esse é o caminho ativo, aceso em ciano no telão.

**A matemática.** O caminho mais curto num grafo com pesos não negativos sai do algoritmo de Dijkstra. Como há dois geradores, o algoritmo roda **ao contrário**, da Âncora para fora: o primeiro gerador que ele alcança é o mais perto, e o caminho até ele, lido de trás para a frente, é o caminho ativo. Isso é o mesmo que rodar Dijkstra com várias origens.

1. $d(\text{Âncora}) = 0$; todos os outros vértices começam sem distância.
2. Escolha o vértice $u$ ainda não visitado com a menor $d(u)$. Se $u$ é um gerador, pare.
3. Para cada vizinho $v$ de $u$ que não foi cortado: se $d(u) + w(u, v) < d(v)$, faça $d(v) = d(u) + w(u, v)$ e $\text{anterior}(v) = u$.
4. Marque $u$ como visitado e volte ao passo 2. Se não sobra vértice alcançável, **não há caminho**: a rede caiu.

Com 9 vértices, a versão simples (procurar o menor numa lista, $O(V^2)$) é a mais clara para ler e mais que rápida.

**Como a rede muda conforme os cortes** (resultado do próprio código):

| Relés cortados | Caminho ativo | m |
|---|---|---|
| nenhum | Gerador Sul > Química > Robótica > Âncora | 7 |
| Química (ou Robótica) | Gerador Norte > Informática > Servidores > Controle > Âncora | 8 |
| Robótica e Controle | Gerador Norte > Informática > Servidores > Âncora | 9 |
| Robótica e Servidores | Gerador Norte > Eletrônica > Âncora | 11 |
| Eletrônica, Servidores e Robótica | **nenhum: a rede caiu** | — |

**No código** (`scripts/sistemas/rede_energia_dtec.gd`): `caminho_ativo(cortados)` é o Dijkstra acima; `CABOS` é a lista de arestas com os pesos; `vizinhos(no)` monta a lista de adjacência a partir dela. Os relés cortados ficam no `Progresso` (marcas `dtec_rele_<relé>`), então o grafo é o mesmo em todas as salas e sobrevive à troca de cena.

---

## 3. A resposta do puzzle: o corte mínimo

**No jogo.** Para abrir o Lab Central, a Âncora tem que ficar **sem nenhum caminho** até um gerador. Cortar relés custa tempo e risco (os robôs vigiam), então o bom jogador procura o **menor conjunto de relés** que desliga tudo. Cortar um relé que não estava no caminho não muda nada, e o aviso diz isso: "A energia nem passava por aqui."

**A matemática.** Um conjunto de vértices cuja remoção separa a origem do destino é um **corte de vértices**. O teorema de **Menger** diz que o tamanho do menor corte é igual ao número máximo de caminhos **sem vértices em comum** (fora as pontas) entre a origem e o destino. É a versão em vértices do teorema do **fluxo máximo e corte mínimo**.

Neste grafo há três caminhos assim, cada um com um só relé no meio:

- Gerador Norte – **Eletrônica** – Âncora
- Gerador Norte – **Servidores** – Âncora
- Gerador Sul – **Robótica** – Âncora

1. **O corte precisa de pelo menos 3 relés:** cada um desses caminhos só morre se o seu único relé for cortado, e eles não dividem relé nenhum.
2. **3 bastam:** cortados Eletrônica, Servidores e Robótica, o Gerador Norte só alcança a Informática (cujos vizinhos são o gerador, a Eletrônica e os Servidores), o Gerador Sul só alcança a Química (vizinhos: o gerador e a Robótica), e o Controle só se liga aos Servidores e à Âncora. Nenhum gerador chega à Âncora.
3. **E é o único corte de 3:** pelo item 1, qualquer corte de 3 tem que conter os três relés do meio dos caminhos. O teste do jogo confere isso nas 63 combinações de relés.

Química, Informática e Controle são as **iscas**: estão em caminhos, mas sempre em paralelo com um dos três relés do gargalo. Cortar a Química, por exemplo, só empurra a energia para o norte.

---

## 4. Os robôs vigiam o caminho

**No jogo.** O robô de cada corredor larga a ronda e passa a vigiar a porta do relé que está no caminho ativo, se esse relé fica no corredor dele. Quando o caminho muda, o robô muda de porta. Com a rede cortada, os dois voltam à ronda de antes.

**No código** (`scripts/sistemas/vigia_da_rede.gd`): o corredor tem, para cada relé que vale vigiar, uma rota `Vigia_<relé>` (marcadores em volta da porta da sala). Quando a sala carrega, o `VigiaDaRede` pega o caminho ativo, anda nele **da Âncora para trás** e escolhe o primeiro relé que tem rota neste corredor: o relé mais perto da Âncora, o último que a energia atravessa. Essa rota vira a `rota` do robô antes de o `RobosDaSala` configurar a patrulha. Química e Informática não têm rota de vigia: sempre que estão no caminho, há outro relé depois delas, que é o vigiado.

| Estado | Corredor norte (Sentinela) | Corredor sul (Rastreador) |
|---|---|---|
| Nada cortado | ronda | vigia a Robótica |
| Química cortada | vigia os Servidores | vigia o Controle |
| Robótica e Servidores cortados | vigia a Eletrônica | ronda |
| Rede cortada | ronda | ronda |
