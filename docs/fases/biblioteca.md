# Fase 1 — Biblioteca

> **Status:** Primeira fase confirmada. Planejamento aprovado em 2026-10-07 e **implementado** (seção 8).
> **Área:** Biblioteca da Unifor
> **Ponto de partida:** Gabriel acorda nesta fase depois de ser puxado de uma madrugada de 2026 para 3026 pela fenda da Âncora.
> **História:** o que a Biblioteca conta segue o [Enredo Principal](../historia/enredo_principal.md) (Ato 1), que é a lei do projeto.

---

## 1. Visão geral

- **Nome do local:** Biblioteca Central da Unifor, no ano de 3026.
- **Ambientação:** o campus mil anos depois, em ruínas. Vegetação dentro do prédio, poeira, feixes de luz natural pelos buracos do teto, estantes caídas e vazias, uma árvore no meio do salão.
- **Ideia da fase:** uma fase no estilo *Resident Evil*. Várias salas ligadas entre si, portas trancadas e um caminho que obriga o jogador a ir e voltar: buscar uma coisa numa sala para abrir outra. O jogador aprende aqui todas as regras do jogo (silêncio, luz, esconderijos, bateria, robôs) e descobre que **não está sozinho**.

### 1.1 No Godot

A Biblioteca é uma cena por sala, em `cenas/salas/biblioteca/`. O jogo começa na cabine (`cabine.tscn`), depois da cutscene `seg_acordar`.

| Cena | Sala | Como foi feita |
|---|---|---|
| `cabine.tscn` | 1, cabine de estudo | Peças (como o Bloco de salas), 320 × 180 |
| `salao.tscn` | 2, salão principal | A arte pintada da antiga `biblioteca.tscn`, x de 0 a 960 (o resto virou a ala leste) |
| `balcao.tscn` | 3, balcão | Peças, 400 × 260 |
| `acervo.tscn` | 4, acervo sul | Peças, 560 × 420, três fileiras de estantes |
| `corredor_servico.tscn` | corredor de serviço | Peças, 480 × 180 |
| `manutencao.tscn` | 5, manutenção (sala segura) | Peças, 400 × 240 |
| `ala_leste.tscn` | 7, ala leste | A arte pintada, x de 960 a 1440 |
| `terminais.tscn` | 8, sala de terminais | Peças, 400 × 260 |

A sala 9 (obras raras) não tem cena: a porta fica barrada nesta fase.

---|---|---|
| **Formato** | Uma cena só, `cenas/salas/biblioteca.tscn`, de 1440 × 420 px (salão, acervo sul e ala leste com a saída) | **Várias salas ligadas por portas** (seção 2) |
| **Robôs** | Nenhum | Sentinela no salão e Rastreador no acervo sul (seção 4) |
| **Registros** | Diário do Baltazar, bilhete da Clarice e duas transmissões do rádio (a voz do Henrique), já funcionando | Os mesmos, em salas novas (seção 6) |
| **Itens** | Lanterna e três pilhas | Também a chave da manutenção e uma cápsula de clarão (seção 3.3) |

Detalhes da cena atual: script `scripts/salas/biblioteca.gd`; parte sul com profundidade y-sort de 122 a 416; a **ala leste** (x de 960 a 1440) é a sala de periódicos, com um terceiro buraco no teto, mesas, cabines e um segundo acervo; doze lampiões de emergência e seis luminárias de parede.

---

## 2. Salas e conexões

### 2.1 Mapa

```
 [1 CABINE]──[2 SALÃO PRINCIPAL]════[GRADE]════[7 ALA LESTE]──► saída (Bloco de salas)
                │      │      │                      │
       [3 BALCÃO]  [4 ACERVO SUL]  [corredor de serviço]  [acervo leste]
                │                        │
     [8 SALA DE TERMINAIS]       [5 MANUTENÇÃO] (sala segura)

     [9 OBRAS RARAS] (porta barrada por dentro: não abre nesta fase)
```

O **salão principal (2)** é o centro da fase: quase todo caminho passa por ele. Por isso ele é a sala mais vigiada, e o jogador atravessa o salão várias vezes, cada vez de um jeito diferente.

### 2.2 As salas

| Nº | Sala | O que tem | Conexões | Esconderijos | Ameaça |
|---|---|---|---|---|---|
| 1 | **Cabine de estudo** | Onde Gabriel acorda. A **lanterna** | 2 | A própria cabine | Nenhuma (tutorial) |
| 2 | **Salão principal** | A árvore, o **acampamento do Baltazar** e o **diário**. Mesas e estantes caídas | 1, 3, 4, 9, corredor de serviço, grade da ala leste | Atrás das estantes caídas, entre as raízes | **Sentinela** |
| 3 | **Balcão de atendimento** | Catraca, **telefone**, o **rádio** na base de carregamento da segurança e o **quadro de chaves** com um gancho vazio | 2, 8 | Atrás do balcão | Nenhuma |
| 4 | **Acervo sul** | Corredores de estantes, uma **pilha** e a **chave da manutenção** num carrinho de devolução de livros | 2 | Os corredores entre as estantes | **Rastreador** |
| 5 | **Sala de manutenção** | O **quadro de energia**, uma **cápsula de clarão** e uma **pilha**. Fechada e escura: é a **sala segura** | Corredor de serviço | Não precisa: robôs não entram | Nenhuma |
| 7 | **Ala leste** (periódicos) | Mesas, cabines, o acervo leste (uma **pilha**) e a **porta de saída** | 2 (pela grade), saída | Corredores do acervo leste | Robôs com rota nova (passo 6) |
| 8 | **Sala de terminais** | O **terminal** com o **bilhete da Clarice** e um **disquete** dela | 3 | Debaixo das mesas | Nenhuma |
| 9 | **Obras raras** | Porta **barrada por dentro**. Às vezes se ouve alguém do outro lado | 2 | — | — |

A sala 6 (mezanino) saiu do planejamento.

---

## 3. Objetivos e progressão

**Objetivo:** sair da Biblioteca pela porta da ala leste, rumo ao Bloco de salas.

**O obstáculo:** entre o salão e a ala leste há uma **grade de segurança** de aço, descida e sem energia. Para abri-la, o jogador precisa de **energia** e de um **código**. E a porta de saída, no fim da ala leste, só abre por fora, pelo sistema.

### 3.1 Passo a passo

1. **Acordar (sala 1).** Gabriel acorda na cabine (cutscene `seg_acordar`) e pega a **lanterna**.
   - *O que o jogador aprende:* andar, pegar itens, ligar a lanterna.
2. **O salão (sala 2).** O lado escuro do salão pede lanterna, e a **Sentinela** patrulha ali. No acampamento entre as raízes, o **diário do Baltazar** ensina o ponto cego dos robôs de um olho só (não veem quem passa pelas costas ou pelo lado) e que luz forte no olho os cega por um instante.
   - *O que o jogador aprende:* luz acesa faz o robô enxergar de longe; passar pelas costas; esconder-se.
3. **O balcão (sala 3).** Gabriel pega o **rádio**, sintonizado na frequência do grupo, e a voz do **Henrique** dá a primeira dica ("Antes de virar, ele dá um bipe. Ouviu o bipe, se esconde."). No **quadro de chaves**, falta a chave da manutenção. A etiqueta do gancho diz "Devolvida ao acervo".
   - *O que o jogador aprende:* os robôs têm rotina e avisos; existe alguém do outro lado do rádio.
4. **O acervo sul (sala 4).** Gabriel procura a **chave da manutenção** num carrinho de devolução de livros, enquanto o **Rastreador**, que escuta, patrulha os corredores. Nos corredores, o rádio dá a segunda fala do Henrique ("Tá no acervo? Boa. No meio das estantes ninguém te vê. Só não corre, viu?").
   - *O que o jogador aprende:* **andar em vez de correr**; o barulho atrai robôs de longe.
5. **A manutenção (sala 5).** A chave abre a porta do corredor de serviço. No **quadro de energia**, Gabriel religa os **disjuntores na ordem certa**, anotada num papel colado do lado de dentro da porta. Aqui também estão uma **cápsula de clarão** e uma pilha. Esta sala é a **sala segura** (seção 5).
   - **Quando a energia volta, três coisas mudam:**
     - a **grade da ala leste** ganha energia, mas pede um **código** no painel;
     - o **terminal** da sala de terminais liga;
     - as **luzes de emergência** acendem pelo salão. É o "não confie nas luzes" da Clarice: as luzes ajudam a ver, mas também deixam os robôs verem você.
6. **Os terminais (sala 8).** Com o terminal ligado, além do **bilhete da Clarice**, o **disquete** dela mostra o **código da grade**. No bilhete, ela conta que guardava senhas nos disquetes: a pista estava ali desde o começo.
7. **A volta pelo salão (sala 2).** Com as luzes acesas, a **rota da Sentinela muda**, e o salão que o jogador já conhecia fica diferente e mais perigoso. Gabriel atravessa até a grade, digita o código e a **grade sobe**.
   - *O que o jogador aprende:* um lugar conhecido pode mudar; voltar faz parte do jogo.
8. **O telefone.** Na ala leste (sala 7), a porta de saída está **trancada eletronicamente**. Nesse momento, o **telefone do balcão toca**. Gabriel precisa atravessar o salão de novo para atender. É o **Zane**, na primeira ligação do jogo. Do computador do bunker, ele destranca a porta de saída pelo sistema.
9. **Saída.** Gabriel volta à ala leste e sai para o **Bloco de salas**.

### 3.2 Grafo de dependências

Cada passo depende do anterior. Para abrir a saída, o jogador precisa, nesta ordem:

```
lanterna → rádio → chave da manutenção → energia → terminal ligado → código da grade → grade aberta → telefone → porta de saída
```

Para a apresentação da disciplina: as salas são **vértices** e as portas são **arestas** de um grafo, e cada cadeado é uma condição numa aresta. A ordem de solução da fase é uma **ordenação topológica** desse grafo de dependências. Ver [`../computacao/grafos_e_navegacao.md`](../computacao/grafos_e_navegacao.md).

### 3.3 Itens

| Item | Onde | Para quê |
|---|---|---|
| Lanterna | Sala 1 | Ver no escuro (e ser visto) |
| Rádio | Sala 3 | Ouvir as dicas do Henrique |
| Chave da manutenção | Sala 4 | Abrir o corredor de serviço |
| Cápsula de clarão | Sala 5 | Primeira defesa: atordoar um robô |
| Pilhas (4) | Salão (2, no lado escuro), sala 4, sala 5, ala leste | Recarregar a lanterna |
| Código da grade | Sala 8 (disquete) | Abrir a grade da ala leste |

---

## 4. Robôs e ameaças

| Robô | Onde | Sentido forte | O que o jogador aprende |
|---|---|---|---|
| **Sentinela** | Salão principal (2) | Visão: cone de 60°, enxerga mais longe com a lanterna acesa | Apagar a lanterna, passar pelas costas, esconder-se. Dá um **bipe antes de virar** (dica do Rafael) |
| **Rastreador** | Acervo sul (4) | Audição: ouve passos de longe | Andar em vez de correr; usar a pedra para distrair |

- **Antes da energia:** a Sentinela faz uma ronda curta no lado iluminado pelo sol.
- **Depois da energia:** as luzes de emergência acendem, e a Sentinela passa a cobrir também o caminho entre o corredor de serviço e a grade. A volta pelo salão (passos 7 e 8) fica mais difícil que a ida.
- **Salas sem robôs:** cabine, balcão, terminais e manutenção. São respiros entre as partes tensas.
- Ser pego dá game over e volta ao último checkpoint.

Os dois robôs já existem no jogo, no Labirinto. Ver [`../historia/personagens/robos.md`](../historia/personagens/robos.md).

---

## 5. Sala segura e sonho

- **Sala segura:** a **sala de manutenção (5)**. Fechada, escura e com porta: os robôs não entram. Gabriel pode dormir e salvar aqui.
- **Por que aqui:** fica no meio da fase, logo depois da primeira parte difícil (acervo sul) e antes da volta pelo salão iluminado.
- **O sonho:** o que os sonhos mostram está pendente no Enredo Principal (seção 12.4).

---

## 6. Registros dos outros personagens

| Registro | Onde (planejado) | Hoje (no Godot) |
|---|---|---|
| **Acampamento e diário do Baltazar** | Salão (2), entre as raízes da árvore | Implementado, no salão |
| **Rádio e 1ª transmissão do Henrique** | Balcão (3) | Implementado, no salão |
| **2ª transmissão do Henrique** | Acervo sul (4) | Implementado, no acervo |
| **Bilhete da Clarice** | Sala de terminais (8), no terminal | Implementado, num terminal no salão |
| **Disquete da Clarice com o código** | Sala de terminais (8) | Não existe |
| **Primeira ligação, do Zane** | Balcão (3), passo 8 | Não existe |

Posições, gatilhos e como os registros funcionam: [`../mecanicas/registros_e_caderno.md`](../mecanicas/registros_e_caderno.md).

O Baltazar **não aparece** nesta fase: só o acampamento que ele deixou (Enredo Principal, Ato 1).

---

## 7. A sala de obras raras

A porta da sala 9 fica **barrada por dentro** durante toda a fase, e às vezes se ouve alguém do outro lado. Ela só abre quando Gabriel voltar à Biblioteca, mais adiante no jogo. É o gancho para o jogador querer voltar, como as portas que só se abrem mais tarde em *Resident Evil*.

**Sugestão, não decisão:** o Enredo diz que o esconderijo do Baltazar fica dentro da Biblioteca, mas o lugar exato está pendente (seção 12.3). A sala de obras raras é uma boa candidata.

---

## 8. Como foi implementado

Tudo o que esta seção listava para construir já está no jogo. Como cada peça funciona:

| O quê | Onde | Como funciona |
|---|---|---|
| **Marcas da fase** | autoload `Progresso` (`scripts/sistemas/progresso.gd`) | Guarda o que já aconteceu: `energia`, `codigo_grade`, `grade_aberta`, `saida_tentada`, `saida_destrancada`. Avisa por sinal (`mudou`) quem precisa reagir. Zera no "Novo jogo" |
| **Portas** | `scripts/sistemas/porta.gd` | Novos campos: `chave` (a porta trancada abre se o Gabriel tem o item), `liberada_por` (fica fechada até a marca existir) e `marca_ao_tentar` (tentar abrir cria uma marca) |
| **Chave da manutenção** | `dados/itens/chave_manutencao.tres`, no carrinho do acervo | Abre a porta de serviço do salão |
| **Quadro de energia** | `cenas/sistemas/quadro_energia.tscn`, na manutenção | Tela com quatro disjuntores. Na ordem do aviso da porta (3, 1, 4, 2) marca `energia`; fora dela, todos caem |
| **Luzes que acendem** | `scripts/sistemas/visivel_com_marca.gd` | Um nó que aparece (piscando) quando a marca chega. No salão, as luzes de emergência também **revelam o Gabriel**: perto delas, os robôs enxergam mais longe, como com a lanterna acesa |
| **Terminal e disquete** | `cenas/sistemas/terminal_com_energia.tscn` e `dados/itens/disquete_clarice.tres`, na sala de terminais | Com energia e com o disquete, o terminal mostra `SENHAS.TXT`, com o código |
| **Painel de código e grade** | `cenas/sistemas/painel_codigo.tscn` e `grade_seguranca.tscn`, no salão | Com energia, o painel aceita o código (0394) e marca `grade_aberta`; a grade sobe e a porta para a ala leste abre |
| **Telefone** | `cenas/sistemas/telefone.tscn`, no balcão | Tentar a porta de saída marca `saida_tentada` e o telefone toca (e se ouve de longe no salão e na ala leste, `toque_distante.tscn`). Atender toca a ligação `zane_01` na legenda do rádio e marca `saida_destrancada` |
| **Obras raras** | porta barrada no salão e `som_do_outro_lado.tscn` | De vez em quando, batidas do outro lado |
| **Robôs** | Sentinela no salão, Rastreador no acervo | Patrulham uma **rota fixa** (pontos `Marker2D` na sala). A Sentinela troca para a rota nova quando a energia volta e dá um **bipe** antes de virar. O nó `RobosDaSala` monta o mapa do chão da sala (células de 16 px, livres onde não há estante), que o A* e a audição por BFS usam |

**Esconderijos:** as estantes das salas com robô estão na camada 4 de colisão (`collision_layer = 9`), a mesma das paredes do labirinto. Elas cortam a visão dos robôs e saem do mapa do chão.

Sons e arte novos (placeholders): `assets/modelagem/audio/gerar_efeitos_biblioteca.py` e `assets/modelagem/cenario/gerar_objetos_biblioteca.py`.

**Pendente:** o texto da ligação do Zane (`dados/transmissoes/zane_01.tres`) e o do disquete são rascunho e precisam da revisão do roteiro. A tabela da seção 2.2 fala em "robôs com rota nova" na ala leste; por enquanto ela não tem robô.
