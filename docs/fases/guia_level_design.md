# Guia de level design — Bloco de salas e Centro de Convivência

> **Para quem é:** quem vai projetar o level design das duas fases. Reúne, num lugar só, o contexto do jogo, os mapas como estão hoje, os itens, os personagens, as regras que o level design precisa respeitar e o que ainda está em aberto.
> **Escrito em:** 2026-10-12, a partir da `main` no commit `5254123` (PR #98) e do PR aberto #97 (proposta do Centro de Convivência).
> **Isto é um resumo.** As fontes são os documentos citados em cada seção. Se este guia e uma fonte discordarem, **vale a fonte**, e este guia deve ser corrigido.

**Em duas linhas:** o **Bloco de salas já está jogável** e recebeu as melhorias de level design em 2026-10-12, então o trabalho nele é revisar, ajustar e expandir. O **Centro de Convivência não existe ainda**: só o nome, a posição e uma proposta em PR aberto, que o Davi precisa aprovar.

---

## Sumário

1. [O que vale e o que não vale](#1-o-que-vale-e-o-que-não-vale)
2. [O jogo em um minuto](#2-o-jogo-em-um-minuto)
3. [Regras que o level design precisa respeitar](#3-regras-que-o-level-design-precisa-respeitar)
4. [O Gabriel: o que ele pode fazer](#4-o-gabriel-o-que-ele-pode-fazer)
5. [Os robôs](#5-os-robôs)
6. [Os mapas: como as fases estão hoje](#6-os-mapas-como-as-fases-estão-hoje)
7. [Os itens do jogo](#7-os-itens-do-jogo)
8. [Os personagens](#8-os-personagens)
9. [Como se monta uma sala no Godot](#9-como-se-monta-uma-sala-no-godot)
10. [Bloco de salas: o que existe e o que está em aberto](#10-bloco-de-salas-o-que-existe-e-o-que-está-em-aberto)
11. [Centro de Convivência: o ponto de partida](#11-centro-de-convivência-o-ponto-de-partida)
12. [Como trabalhar e entregar](#12-como-trabalhar-e-entregar)
13. [Onde ler mais](#13-onde-ler-mais)

---

## 1. O que vale e o que não vale

Ordem de autoridade (de cima para baixo):

1. **[`docs/historia/enredo_principal.md`](../historia/enredo_principal.md)** e as fichas de [`docs/historia/personagens/`](../historia/personagens/): a lei do projeto para história, mundo e personagens. Se algo contradiz o Enredo, o erro está no outro lugar.
2. **[`docs/decisoes.md`](../decisoes.md)**: o registro de decisões, o mais recente para mecânicas, técnica e arte.
3. Os documentos de cada módulo (`docs/fases/`, `docs/mecanicas/`, `docs/computacao/`).
4. **[`docs/gdd.md`](../gdd.md)**: o resumo geral. Está parcialmente desatualizado (parte vem da premissa antiga, dos "Calouros").

Duas regras de convivência:

- **O que o Enredo ainda não decidiu está na seção 12 dele ("Pendências"). Não invente resposta para uma pendência: pergunte ao Davi.** Mais abaixo (seções 10 e 11) estão as pendências que tocam estas duas fases.
- **O Enredo Principal só se edita quando o Davi pedir.** Ideias novas de história vão para [`docs/historia/outras_ideias.md`](../historia/outras_ideias.md).

**Vocabulário oficial** (para qualquer texto, placa, bilhete ou fala):

| Use | Não use |
|---|---|
| **Âncora** (a máquina) | "Ankhor" para a máquina (Ankhor é o nome do jogo) |
| **Fenda** | "portal" |
| **Robôs** (os inimigos) | "Insones", "Bibliotecária", "Calouros", "Vigia" |
| **Lanterna a pilha**, **luzes de emergência** | "fungos", "pote de fungos" |
| **Antecessores** (quem caiu antes do Gabriel) | "viajantes", "vítimas" |
| **Cápsula de clarão** | "granada" |
| **Caderno do Gabriel** | "diário" (o diário é o do Baltazar) |

---

## 2. O jogo em um minuto

- **Premissa:** em 3026 o pouco que sobrou da humanidade foi embora da Terra. Ficou o **Carlos**, um cientista obcecado pelos anos 80, que construiu a **Âncora** para ir viver lá. A máquina é imprecisa: a cada tentativa, abre uma **fenda** no chão da Biblioteca e puxa, por acaso, jovens de épocas diferentes. Um deles é **Gabriel Magalhães**, estudante de 2026. Ele precisa encontrar os outros, descobrir o que aconteceu e achar um jeito de todos voltarem. Os inimigos são **robôs** controlados pelo Carlos.
- **Onde:** a **Unifor, em Fortaleza**, mil anos depois: concreto rachado e desabado, árvores dentro das salas, dunas sobre os corredores, mato onde era estacionamento. Não há cidade em volta. Objetos do cotidiano (catraca, bebedouro, quadro de horários, cantina) viraram relíquias. O choque do jogo é perceber **quanto tempo passou**.
- **Tom:** terror atmosférico, fuga e esconderijo, defesa limitada. Inspirado em *Five Nights at Freddy's: Into the Pit*. Gabriel **não é combatente**: fugir e se esconder é a regra, defender-se é a exceção.
- **Visual:** pixel art em vista lateral com profundidade 2.5D. Resolução base **320×180**, escala inteira, filtro *Nearest*. A lógica e a interface ficam em 320×180. **Os personagens humanos têm sprites em resolução dobrada** (96 px de altura, mostrados com escala 0,5, então o Gabriel tem cerca de 48 px na tela); o cenário continua em 1×.
- **Luz e cor:** o presente é cinza de concreto, marrom, verde-musgo, areia e o âmbar fraco das luzes de emergência (o verde fica para checkpoints e saídas; o vermelho, para os olhos dos robôs). O passado (sonhos) é branco clínico, quente e plano.
- **Cutscenes:** prólogo ilustrado (`seg_prologo`) e o despertar na Biblioteca (`seg_acordar`, vídeo). Os cenários precisam mostrar **mais da tecnologia de 3026** misturada às ruínas (pedido do Davi, Enredo 12.5).
- **Requisito da disciplina:** o jogo precisa usar conteúdos de computação (grafos, BFS, A\*, cadeia de Markov, coloração de grafos, máquina de estados, produto escalar). Cada fase deve **mostrar** algum deles em jogo. Ver [`../computacao/`](../computacao/README.md).

---

## 3. Regras que o level design precisa respeitar

1. **Cada fase leva a um personagem e ao esconderijo dele** (Ato 2 do Enredo): Gabriel chega, ganha a confiança da pessoa e recebe a parte dela para consertar a Âncora.
2. **Toda área tem pelo menos uma sala segura**, com checkpoint. (Dormir e sonhar ainda não existem: ver seção 12.4 do Enredo.)
3. **Cada fase ensina algo novo.** Biblioteca: silêncio, luz, esconderijos, bateria, robôs. Bloco de salas: barulho como ferramenta, luar como perigo, o chão que muda o som, atalhos.
4. **Ir e voltar faz parte** (estilo *Resident Evil*): portas trancadas, chave em lugar vigiado, cadeado de segredo com a pista espalhada, atalho que se abre por dentro. Cada cadeado é uma condição numa aresta do grafo de salas.
5. **Os robôs têm rotina e dá para decorar.** Um lugar conhecido pode mudar (a "virada": uma marca de progresso troca a rota do robô).
6. **A eletricidade funciona normalmente** em 3026. Onde algo está apagado, é um circuito desligado ou quebrado, nunca "falta de energia".
7. **É noite** nas fases do Bloco de salas e do Centro de Convivência (na proposta). Luar e luzes de emergência são a luz do cenário.
8. **Esconderijos e cobertura:** hoje o único esconderijo com mecânica própria no código é o **nicho de parede**. Os outros "esconderijos" das tabelas das fases (atrás de carteiras, debaixo de mesas) são cobertura visual para quebrar a linha de visão. Armário, cabine e raízes com microgame estão só nos documentos (ver [`../mecanicas/furtividade_e_esconderijos.md`](../mecanicas/furtividade_e_esconderijos.md)).
9. **Sem assets pagos.** Toda a arte é produzida pelo Davi: peça por issue com o rótulo `arte` e use **placeholder** enquanto ela não chega (seção 12).
10. **Escopo de faculdade:** uma sala perfeita vale mais que cinco pela metade.

---

## 4. O Gabriel: o que ele pode fazer

Fontes: [`../mecanicas/`](../mecanicas/README.md), principalmente `movimentacao_e_terreno.md`, `itens_e_inventario.md` e `vida_e_checkpoint.md`.

| Capacidade | Valor |
|---|---|
| Andar | 60 px/s (`WASD` ou setas). Para o fundo ou a frente da sala, 65% disso |
| Correr | `Shift`, ×1,8. Gasta estamina: 100 de estamina a 12,5/s, ou seja, cerca de 8 s contínuos |
| Exaustão | Estamina zerada: 3 s sem correr, com 40% da velocidade e suspiros audíveis |
| Recuperar estamina | Parado, cerca de 4 s; andando, cerca de 8 s |
| Interagir | `E` (pegar item, atravessar porta, digitar código, ler) |
| Inventário | `Tab` ou `I`; grade de 3 × 4. `N` abre o caderno (anotações) |
| Gadgets | 3 espaços (`1`, `2`, `3`): lanterna, cápsula de clarão, pedra, notebook |
| Vida | 3 corações. Um toque de robô tira 1; 1,5 s de invulnerabilidade; zerou, volta ao último checkpoint com a vida cheia |
| Nicho de parede | Parado por 0,4 s, com a lanterna apagada, fica escondido. Andar ou acender a luz revela |
| Hackear | Notebook parado a 44 px de uma porta trancada: minigame (Sequência ou Sincronia, 3 dificuldades). Num robô, só **por trás**: desliga 8 s |

**Gadgets:**

| Gadget | Efeito | Limite |
|---|---|---|
| **Lanterna** | Cone de luz. Os robôs enxergam o Gabriel de mais longe com ela acesa | Bateria de 4 min; pilhas no mapa |
| **Cápsula de clarão** | Paralisa por 3,5 s os robôs a até 110 px (Sentinela ×1,5, Rastreador ×0,6) | No máximo 2 |
| **Pedra** | Jogada a ~110 px, faz barulho onde cai: os robôs que ouvem vão investigar | No máximo 5 |
| **Notebook** | Hackeia porta ou robô; a tela acesa conta como luz | 25% da bateria por hack (4 hacks) |

**Medidas úteis para dimensionar um espaço:** a tela mostra 320 × 180 px. Um corredor de 2560 px são **8 telas**. Gabriel anda uma tela em cerca de 5 s e corre uma em cerca de 3 s. A pedra alcança uma distância equivalente a um terço de uma tela.

---

## 5. Os robôs

Fontes: [`../historia/personagens/robos.md`](../historia/personagens/robos.md) e [`../computacao/ia_e_perseguicao.md`](../computacao/ia_e_perseguicao.md). Os dois tipos usam o mesmo script (`scripts/personagens/robo.gd`); o que muda são os números no Inspetor.

| | **Sentinela** (visão) | **Rastreador** (audição) |
|---|---|---|
| Visual | 2,1 m, magra, um olho, farol vermelho mostra para onde olha | Quadrúpede de 0,8 m, três olhos, antenas parabólicas |
| Cena | `cenas/personagens/robo_sentinela.tscn` | `cenas/personagens/robo_rastreador.tscn` |
| Visão | 170 px, cone de 60° | 80 px, cone de 100° |
| Visão com luz | ×1,7 (289 px) | ×1,3 (104 px) |
| Audição (`fator_audicao`) | ×0,5 | ×1,8 |
| Velocidade (patrulha / perseguição) | 18 / 36 px/s (lenta) | 24 / 50 px/s (rápida) |
| Paralisado pelo clarão | ×1,5 (sofre mais) | ×0,6 |

**Como eles percebem o Gabriel:**

- **Visão:** ele é visto se estiver a até **20 px** do robô, ou se estiver dentro do alcance, dentro do cone (produto escalar) e **sem parede no caminho** (raio). "Com luz" é: lanterna ou notebook acesos, ou o Gabriel a menos de **56 px** de uma luz que revela (o luar do 1º andar do Bloco de salas, as luzes de emergência da Biblioteca). Gabriel escondido num nicho não é visto, mas o contato ainda vale.
- **Audição:** cada passo gera um som de alcance-base de **5 células** andando e **14 correndo** (célula de 16 px). O alcance de cada robô é `int(base × fator_do_piso × fator_audicao)`, e uma busca em largura (BFS) pela grade livre da sala corta depois desse número de passos. **Obstáculos bloqueiam o som.** A grade é **por sala**: o som que passa para outra sala é repassado por evento (a sirene, a pedra pelo buraco).
- **Fator do piso** (só nos corredores do Bloco de salas): oeste ×0,5, centro ×1,0, leste ×1,5. Alcance resultante, em células, andando e correndo:

| Robô | Oeste (×0,5) | Centro (×1,0) | Leste (×1,5) |
|---|---|---|---|
| Sentinela | 1 e 3 | 2 e 7 | 3 e 10 |
| Rastreador | 4 e 12 | 9 e 25 | 13 e 37 |

- **Estados:** rotina → investigando (ouviu ou viu luz suspeita) → perseguindo (vê o Gabriel; persegue por A\*) → procurando → volta à rotina. Atordoado (clarão ou hack) não anda, não vê, não ouve, não ataca.
- **Rota:** uma sequência de pontos (`Marker2D`) que o robô percorre. Pode ter uma **segunda rota** que entra quando uma marca de progresso é acesa (foi assim que a Sentinela passou a cobrir a 206 e a escada depois do alicate).
- **Distração:** `distrair(onde, segundos)` faz o robô ir investigar e ignorar o resto (a sirene da 104 prende o Rastreador por 20 s).
- **Não falam.** Ser pego é game over. Por que caçam (capturar ou eliminar) é pendência (Enredo 12.2).

---

## 6. Os mapas: como as fases estão hoje

### 6.1 Visão geral

Cada **sala é uma cena** (`cenas/salas/<fase>/<sala>.tscn`) e as salas se ligam por portas (`Porta`). Salas são vértices; portas, arestas; cadeados, condições nas arestas. Menu **Fases** do jogo lista todas (`dados/fases/*.tres`); as que ainda não têm cena aparecem apagadas.

| Fase | Status | Cenas | Posição na história | Documento |
|---|---|---|---|---|
| **Biblioteca** | Implementada (a primeira fase) | 8 | Ato 1 | [`biblioteca.md`](biblioteca.md) |
| **Bloco de salas** | **Jogável do começo ao fim** + melhorias de 2026-10-12 | 15 | Ato 2 | [`bloco_de_salas.md`](bloco_de_salas.md) |
| **Centro de Convivência** | **Não existe.** Só nome e posição; proposta no PR #97 | 0 (`04_convivencia.tres` tem `cena` vazia) | Ato 2, depois do Bloco de salas | [`centro_de_convivencia.md`](centro_de_convivencia.md) |
| **Bunker** | Em desenvolvimento: 9 cenas, só o Henrique aparece, salas lacradas | 9 | Ato 3 (posição na ordem de fases: não decidida) | [`bunker.md`](bunker.md) |
| **Labirinto** | Jogável, sem lugar na história | 1 | A definir | [`labirinto.md`](labirinto.md) |
| **DTEC** | Mapa pronto, sem robôs e sem lugar na história | 10 | A definir (o D-Tec é onde fica o Carlos) | [`dtec.md`](dtec.md) |

Ordem já decidida: **Biblioteca → Bloco de salas → Centro de Convivência**. Por enquanto, a porta corta-fogo do Bloco de salas abre a entrada do **Bunker**, de forma **provisória**.

### 6.2 Biblioteca (a fase que vem antes)

Vale ler para ver o padrão que o Bloco de salas repete e o que o jogador já sabe quando chega nele.

```
 [1 CABINE]──[2 SALÃO PRINCIPAL]════[GRADE]════[7 ALA LESTE]──► saída (Bloco de salas)
                │      │      │                      │
       [3 BALCÃO]  [4 ACERVO SUL]  [corredor de serviço]  [acervo leste]
                │                        │
     [8 SALA DE TERMINAIS]       [5 MANUTENÇÃO] (sala segura)

     [9 OBRAS RARAS] (porta barrada por dentro)
```

| Cena | Tamanho (L × A px) | O que tem |
|---|---|---|
| `cabine` | 320 × 180 | Onde Gabriel acorda; a lanterna |
| `salao` | 960 × 420 | Centro da fase; árvore, acampamento do Baltazar, Sentinela |
| `balcao` | 400 × 260 | Telefone, rádio, quadro de chaves |
| `acervo` | 560 × 420 | Estantes; chave da manutenção; Rastreador |
| `corredor_servico` | 480 × 180 | Liga o salão à manutenção |
| `manutencao` | 400 × 240 | Quadro de energia, clarão, pilha; **sala segura** |
| `terminais` | 400 × 260 | Terminal com o bilhete e o disquete da Clarice |
| `ala_leste` | 480 × 420 | Grade, acervo leste, porta de saída |

Cadeia: `lanterna → rádio → chave da manutenção → energia → terminal ligado → código da grade → grade aberta → telefone → porta de saída`. O que o jogador aprendeu ao chegar ao Bloco de salas: andar em vez de correr, luz acesa denuncia, passar pelas costas do robô, voltar a um lugar e achá-lo diferente, e que **não está sozinho** (a voz da Clarice no rádio).

### 6.3 Bloco de salas

Dois corredores, um em cima do outro, com seis salas de aula em cada. **Noite**, com luar azulado entrando pelas janelas e pelos buracos do teto. O térreo está meio enterrado na areia; no 1º andar o teto caiu, com mato e duas árvores no corredor. Em quase toda sala a lousa ainda está presa, coberta de **tracinhos contados** em grupos de cinco.

```
 1º ANDAR  ══[201]══[202]══[203]══[204]══[205]══[206]══[ESCADA]══[PORTA CORTA-FOGO]──► saída
 (teto aberto)         ╎ ◄─porta de serviço─► ╎    │ buraco no chão       ║
                                                   ▼ (só desce)           ║ grade com cadeado
 TÉRREO    ══[101]══[102]══[103]══[104]══[105]══[106]══[ESCADA]
 (areia)     ╎◄─brecha─►╎      │
             ▲          posto da Clarice (sala segura)
       vem da Biblioteca
```

- Brecha **101 ↔ 102**; porta de serviço **203 ↔ 206** (começa trancada, com o trinco do lado do depósito); buraco **204 → 104**, só desce.
- A **escada** começa fechada por uma grade com cadeado. A **saída** é a porta corta-fogo no fim do 1º andar, acorrentada.

**Os corredores e seus três setores** (2560 px, 8 telas; as portas ficam na mesma ordem nos dois andares):

```
 x:  0              768              1536                       2560
     │    OESTE     │     CENTRO     │          LESTE            │
     │ areia (térreo)│ lajota e tapete│ lajota solta              │
     │ mato (1º and.)│                │                           │
     │ som ×0,5     │ som ×1,0       │ som ×1,5                  │
     │ x01   x02    │ x03     x04    │ x05     x06    escada     │
     281   601       921    1401      1721   2041    2360   ← x das portas
```

**As cenas** (`cenas/salas/bloco_de_salas/`):

| Cena | L × A px | Papel | O que tem | Robô |
|---|---|---|---|---|
| `corredor_terreo` | 2560 × 180 | Chegada, eixo do térreo | Rádio na chegada, 2 nichos, estalos no teto, checkpoint | **Rastreador** |
| `sala_101` | 480 × 560 | Pista do código | Lousa com 7 tracinhos | — |
| `sala_102` | 400 × 480 | Chave da escada | Molho de chaves caído na areia, 3 pedras | — (o Rastreador passa na porta) |
| `sala_103` | 480 × 560 | **Posto da Clarice (e da Diana); sala segura** | Clarice, acampamento, 2 pilhas, checkpoint, fresta da barricada, lousa-mapa | — |
| `sala_104` | 480 × 560 | Distração e fim do atalho | Terminais acesos; **teste de alarme**; embaixo do buraco da 204, caixas amortecem a queda | — |
| `sala_105` | 400 × 480 | Respiro | 2 robôs desmontados, 2 pilhas; a mais escura | — |
| `sala_106` | 480 × 560 | Respiro | Árvore e luar | — |
| `corredor_primeiro_andar` | 2560 × 180 | Eixo do andar de cima | Luar em faixas, mato, 2 nichos | **Sentinela** |
| `sala_201` | 640 × 720 | Pista do código | Auditório; lousa da esquerda com 3 tracinhos | — |
| `sala_202` | 480 × 560 | Respiro | 2 árvores, 1 pedra | — |
| `sala_203` | 400 × 480 | Cadeado de segredo | **Claviculário** (código de 3 números) e quadro de avisos com a pista | — |
| `sala_204` | 480 × 560 | Atalho | Buraco no chão (desce para a 104), 1 clarão | — |
| `sala_205` | 400 × 480 | Pista do código e mistério | Lousa limpa com 8 tracinhos, calha fluorescente, zumbido de 60 Hz. **Intacta demais** (sem explicação) | — |
| `sala_206` | 400 × 480 | Ferramenta da saída | Alicate corta-corrente, 1 pilha. Trancada | **Rastreador** |
| `fim_do_bloco` | 960 × 180 | Tela "Você saiu do bloco" | Leva à entrada do Bunker, provisoriamente | — |

**A cadeia principal** (o resto do detalhe está em [`bloco_de_salas.md`](bloco_de_salas.md), seção 3):

```
rádio da Clarice → alarme da 104 → posto da Clarice → molho (102) → chave da fita azul → grade da escada
                                                                                       ↓
saída ← corrente cortada ← alicate (206) ← chave do depósito ← cadeado do claviculário ← tracinhos (101, 201, 205)
```

O atalho 204 → 104 é opcional e fica fora da cadeia. Quando o Gabriel pega o alicate, a **Sentinela muda de ronda** e passa a cobrir o trecho entre a 206 e a escada (a "virada"). O código do claviculário é **738** (7 + 3 + 8, na ordem 101 · 201 · 205).

### 6.4 Bunker, DTEC e Labirinto (resumo)

- **Bunker** (`cenas/salas/bunker/`): 2 corredores (2560 e 2240 px) e 7 salas, dois setores (A em cima, B embaixo, alagado). Concreto e tinta verde-oliva, tubos fluorescentes e luz de emergência vermelha. **Os robôs não descem aqui.** Seis portas lacradas são ganchos para fases futuras (escotilha, elevador, arsenal, laboratório, arquivo, comporta do núcleo). Quem vive aqui: **Zane** (computador da central de dados) e **Henrique** (mesma sala, com as câmeras).
- **DTEC:** laboratório lacrado e mais inteiro que o resto; no Lab Central, uma máquina grande e brilhante que **não tem nome nem papel na história**. Sem robôs.
- **Labirinto:** subsolo escuro, três robôs, sem checkpoint. Feito a partir de um mapa em texto (`dados/labirinto/mapa_labirinto.tres`).

---

## 7. Os itens do jogo

Os itens são recursos `Item` em `dados/itens/*.tres`. No mapa entram por `cenas/itens/item_no_chao.tscn` (a origem é o pé). Todo coletável tem uma luz fraca que pulsa e um brilho de pixel, para o jogador achar sem seta.

### 7.1 Catálogo

| Item (`id`) | Tipo | Onde está hoje | Para quê |
|---|---|---|---|
| **Lanterna** (`lanterna`) | Gadget | Biblioteca (cabine e salão); também no corredor do térreo do Bloco, para quem entra pelo menu | Ilumina; denuncia |
| **Pilha** (`pilha_no_chao`, não é `.tres`) | Consumível | Biblioteca (lado escuro); Bloco: 103 (2), 105 (2), 206 (1); Bunker: dormitório, enfermaria, depósito | Recarrega a lanterna; some depois de usada |
| **Rádio portátil** (`radio`) | Item | Biblioteca (balcão); Bloco: corredor do térreo, só se o Gabriel ainda não tem | Sem ele as transmissões não tocam |
| **Chave da manutenção** (`chave_manutencao`) | Chave | Biblioteca, acervo sul (carrinho de livros) | Abre o corredor de serviço |
| **Disquete da Clarice** (`disquete_clarice`) | Item-pista | Biblioteca, sala de terminais | Precisa de um terminal ligado; mostra o código da grade |
| **Cápsula de clarão** (`clarao`) | Gadget (máx. 2) | Biblioteca (manutenção); Bloco: 204 (1); Bunker: refeitório e depósito | Paralisa robôs perto |
| **Pedra** (`pedra`) | Gadget (máx. 5) | Bloco: 102 (3) e 202 (1); Bunker: depósito (2) | Distrai robôs |
| **Notebook** (`notebook`) | Gadget | DTEC (lab de informática) e sala de teste. **Não entra no Bloco de salas** (decisão do Davi) | Hackeia porta ou robô |
| **Molho de chaves** (`molho_de_chaves`) | Item-troca | Bloco: 102, na areia | Devolver à Clarice; ela fica com ele |
| **Chave da fita azul** (`chave_grade`) | Chave | Bloco: entregue pela Clarice na 103 | Abre a grade da escada |
| **Chave do depósito** (`chave_deposito`) | Chave | Bloco: claviculário da 203 | Abre a 206 |
| **Alicate corta-corrente** (`alicate`) | Ferramenta | Bloco: 206 | Corta a corrente da porta corta-fogo; **troca a ronda da Sentinela** |

**Documentos** (`dados/documentos/`): `bilhete_clarice`, `diario_baltazar`, `disquete_clarice`, `ordem_disjuntores`. **Transmissões de rádio** (`dados/transmissoes/`): `clarice_biblioteca_01` e `_02` (Biblioteca), `clarice_01` a `_04` (Bloco), `zane_01` (o telefone da Biblioteca). **Diálogos em pessoa** (`dados/dialogos/*.json`): Clarice no Bloco (4 conversas), Henrique no bunker.

### 7.2 Marcas de progresso (autoload `Progresso`)

Uma **marca** é uma palavra que o jogo acende quando algo acontece. Portas, grades, luzes, transmissões e rotas dos robôs reagem a ela. É a cola do level design: quase todo "isso muda quando aquilo acontece" é uma marca.

| Fase | Marcas |
|---|---|
| Biblioteca | `energia`, `codigo_grade`, `grade_aberta`, `saida_tentada`, `saida_destrancada` |
| Bloco de salas | `alarme_104`, `molho_devolvido`, `escada_destrancada`, `claviculario_aberto`, `trinco_206`, `alicate`, `corrente_cortada` |

**O que não é desfeito ao morrer:** itens pegos (a lanterna não reaparece, pilhas usadas não voltam), anotações do caderno e transmissões já ouvidas. Ao morrer, a fase é recarregada inteira e os robôs voltam à origem.

---

## 8. Os personagens

Fichas em [`../historia/personagens/`](../historia/personagens/) (cada uma tem a mesma autoridade do Enredo). Resumo em [`resumo.md`](../historia/personagens/resumo.md).

### 8.1 Quem é quem e onde fica

| Personagem | Época | Em uma frase | Onde fica no jogo | Parte para consertar a Âncora |
|---|---|---|---|---|
| **Gabriel Magalhães** | 2026 | Observador, ironia seca, prefere observar a agir. **O protagonista**, o último a chegar | — | O caderno, com as equações da cadeira |
| **Clarice** | 1994 | Aluna de processamento de dados. Rápida, debochada, explica tudo como lógica, não pede ajuda | **Sala 103 do Bloco de salas**, atrás de uma barricada. **É a voz do rádio** desde a Biblioteca, com o que o Henrique vê | Código: faz os terminais da Âncora funcionarem. Mapeou as rondas e sabe o que cada chave abre |
| **Diana** | 1978 | Recruta da polícia. Dramática, ansiosa, impulsiva | **Sala 103**, acolhida pela Clarice. **Ainda sem visual definido** | Investigação: onde fica o núcleo e as passagens |
| **Henrique** | 2019 | Aluno de iniciação científica. Pausado, técnico, perfeccionista. **O primeiro a chegar. Mente para o grupo** (pendência 12.7) | **Sala de dados do bunker**, com as câmeras. Passa à Clarice o que vê | A teoria por trás das equações |
| **Zane** | 2123 | Jovem com implantes. Confiante, gírias de um futuro que ninguém reconhece | **Computador do bunker**: mantém o rádio e liga pelos telefones velhos | A tecnologia mais próxima da Âncora |
| **Baltazar** | ~1750 | Devoto e encantado com tudo, fala português arcaico. **Antepassado de Gabriel** | **Escondido numa sala da Biblioteca** desde que chegou (qual sala: pendente) | As estrelas, que acertam a data de volta |
| **Carlos** | 3026 | O cientista que criou a Âncora. **O antagonista** | Laboratório do D-Tec, de onde nunca sai | — |
| **Os robôs** | 3026 | Controlados pelo Carlos | Patrulham o campus | — |

**Ordem de chegada** (já decidida, falta só o Baltazar): Henrique primeiro, Zane antes da Clarice, Diana depois da Clarice, Gabriel por último.

### 8.2 Quem aparece em cada fase

| Fase | Em pessoa | Pelo rádio ou telefone |
|---|---|---|
| Biblioteca | Ninguém (o acampamento do Baltazar está vazio) | Clarice (rádio), Zane (telefone) |
| Bloco de salas | **Clarice** (sala 103). A Diana está lá, mas não aparece | Clarice (guia pelo rádio, com o que o Henrique vê) |
| Centro de Convivência | **Nenhum personagem tem esse lugar** (ver 11.3) | Provavelmente a Clarice, como nas outras fases |
| Bunker | **Henrique** (primeiro encontro em pessoa). O Zane ainda não tem cena | — |

### 8.3 Como cada um fala (para falas, bilhetes e placas)

- **Clarice:** gírias dos anos 90 ("Isso é totalmente surreal", "Não confie nas luzes"), deboche, explica tudo como lógica. **Não pede ajuda**: para ela, devolver o molho é uma permuta. Chama o Gabriel de "meu filho".
- **Henrique:** fala pausado e técnico, **se corrige no meio da frase**, fala pouco.
- **Zane:** direto, irreverente, gírias de futuro.
- **Baltazar:** "Vossa Mercê", latim quando aflito, português arcaico.
- **Diana:** fala rápido, com exclamações, mistura jargão de polícia com drama de novela.
- **Gabriel:** ironia seca ("Ótimo. Mil anos de atraso pra aula.").

### 8.4 O que ainda é pendência sobre eles

Segredo do Henrique (seção 12.7 do Enredo), se a Clarice fica na 103 até o fim, qual sala da Biblioteca esconde o Baltazar, visual da Diana, o que o Zane fazia quando foi puxado. **Nada disso deve ser resolvido pelo level design.**

---

## 9. Como se monta uma sala no Godot

Resumo operacional. Detalhes em [`../mecanicas/movimentacao_e_terreno.md`](../mecanicas/movimentacao_e_terreno.md) (portas) e [`../mecanicas/itens_e_inventario.md`](../mecanicas/itens_e_inventario.md) (itens).

### 9.1 A cena de uma sala

Toda sala **herda `cenas/salas/modelo_sala.tscn`**, que já traz o HUD, o inventário, o rádio, a tela de morte e a caixa de diálogo. Nós, de trás para a frente:

| Nó | O que vai nele |
|---|---|
| `Ceu` | Céu noturno com estrelas (`ceu_noite.png`) |
| `Paredes` | Peças de parede do kit, lado a lado, de 80 em 80 px. Os números das salas em cima das portas são `Label` aqui dentro |
| `Chao` | Peças de chão (128 px de largura) e as peças de fundo |
| `Objetos` | **Tudo que o Gabriel cruza, na ordem de profundidade (`y_sort`)**: móveis, itens, portas, robôs, o próprio Gabriel. A origem de cada objeto é o **pé** |
| `Efeitos` | Poeira, raios de sol, estalos do teto |
| `Frente` | O que passa na frente do Gabriel (raízes, colunas) |
| `Luzes` | As luzes (`luz_emergencia`, `luz_lampada`, `luz_tubo`, `luz_fria`, `luz_sol`, `luz_maquina`) |

### 9.2 Medidas

| O quê | Valor |
|---|---|
| Tela | 320 × 180 px |
| `largura` e `altura` da sala | Definem o limite da câmera. Padrão 960 × 180. Salas altas (480 a 720 px) rolam na vertical |
| `chao_fundo` | Linha do fundo do chão. Padrão **120** |
| `chao_frente` | Linha da frente do chão (padrão 176; nas salas altas, `altura - 4`) |
| Faixa andável | Entre `chao_fundo` e `chao_frente`. Num corredor (altura 180) são **56 px** de profundidade; numa sala de altura 560, 436 px |
| `margem_lados` | 20 px de cada lado sem andar |
| Peça de parede | 80 px de largura (a porta é uma peça de 80 px, com a `Porta` no meio do vão) |
| Peça de chão | 128 px de largura |
| Célula da grade dos robôs | 16 px |

Os limites de colisão (`LimitesAutomaticos`) são criados sozinhos a partir desses valores.

### 9.3 O kit de peças (`cenas/cenario/`)

| Grupo | Peças |
|---|---|
| **Chão** | areia, lajotas, mato, tapete (cada um com a versão "fundo") |
| **Paredes** | lisa, rachada, desabada, buraco, janela, porta, arandela, fluorescente, estante, placa, mural, pilar; lousas (`parede_lousa`, com 0, 3, 7, 8 tracinhos, a 8 limpa e a "mapa" da Clarice); escadas (sobe e desce); laterais (porta e brecha); nichos (armário e bebedouro) |
| **Objetos** | carteira (em pé e caída), mesa de leitura, cadeira, estante (caída, quebrada, vazia), terminal, árvore, entulho, livros, robô desmontado, cabine, carrinho, lâmpada, acampamento do Baltazar, caixas de queda |
| **Efeitos** | poeira, raios de sol |
| **Luzes** | emergência, lâmpada, tubo, fria, sol, máquina |
| **Bunker e DTEC** | kits próprios em `cenas/cenario/bunker/` e `cenas/cenario/dtec/` |

As peças são **geradas por script** (`assets/modelagem/cenario/gerar_kit.py` e os geradores por fase). Peça nova = função no gerador, rodar o script, abrir o Godot para gerar o `.import`. **Isso é do Davi**: peça por issue `arte` e use placeholder.

### 9.4 Sistemas que se pode instanciar (`cenas/sistemas/`)

| Cena | O que faz | Campos principais |
|---|---|---|
| `porta.tscn` | Passagem entre cenas, ou dentro da sala | `id`, `cena_destino`, `porta_destino`, `direcao_entrar`, `trancada`, `bloqueada`, `chave`, `marca_ao_destrancar`, `trinco_deste_lado`, `dificuldade_hack` |
| `checkpoint.tscn` | Poste que salva o ponto e devolve os 3 corações | `id` |
| `painel_codigo.tscn` | Cadeado de segredo com código | `codigo`, `marca_energia` (vazia = sem energia), `marca`, `item_ao_abrir` |
| `grade_seguranca.tscn` | Grade de aço que sobe quando uma marca acende | `marca` |
| `gatilho_transmissao.tscn` | Toca uma transmissão de rádio quando o Gabriel passa | `transmissao`, `item_necessario`, `marca_necessaria` |
| `nicho_esconderijo.tscn` | Reentrância da parede onde o Gabriel parado e sem luz some | `segundos_para_esconder` |
| `terminal_alarme.tscn` e `sirene.tscn` | Liga um alarme que atrai o robô por 20 s | `marca`, `segundos_tocando` |
| `buraco_no_chao.tscn` | Passagem de mão única; a pedra que cai faz barulho embaixo | `segundos_robo_embaixo` |
| `estalo_do_teto.tscn` | Estalo e poeira de tempos em tempos (cenário vivo) | `segundos_minimos`, `segundos_maximos` |
| `saida_fase.tscn` | Fim da fase | `cena_destino`, `sair_ao_carregar` |
| `quadro_energia.tscn`, `terminal_com_energia.tscn`, `telefone.tscn`, `toque_distante.tscn`, `som_do_outro_lado.tscn` | Peças da Biblioteca (energia, terminal, telefone, sons à distância) | ver os scripts |

Dois sistemas não são cenas: são **scripts que se põem num nó** (`Node2D` ou a própria peça):

| Script (`scripts/sistemas/`) | O que faz | Campos principais |
|---|---|---|
| `visivel_com_marca.gd` (`VisivelComMarca`) | A peça aparece ou some quando uma marca acende. Também faz as **faixas de luar que revelam** o Gabriel | `marca`, `some_com_marca`, `revela_quem_passa` |
| `zona_de_piso.gd` (`ZonaDePiso`) | Retângulo do chão com um fator de ruído para o som dos passos | `tamanho`, `fator_ruido`, `nome_piso` |

### 9.5 Robôs numa sala

1. Instancie `robo_sentinela.tscn` ou `robo_rastreador.tscn` em `Objetos`.
2. Crie um `Node2D` com `Marker2D` filhos (a **rota**) e aponte o campo `rota` do robô para ele.
3. Para a "virada", crie uma segunda rota e preencha `rota_com_marca` e `marca_da_rota`.
4. Adicione um nó `RobosDaSala` (`scripts/salas/robos_da_sala.gd`) na sala: ele monta sozinho a grade de 16 px com os obstáculos e entrega aos robôs. Sem ele os robôs não ouvem.

### 9.6 Criar uma sala nova, na ordem

1. Duplique uma sala parecida (herdam do modelo) e troque o `id`.
2. Defina `largura`, `altura`, `chao_fundo` e `chao_frente`.
3. Monte `Paredes` e `Chao` com o kit.
4. Ponha a(s) `Porta`(s) e ligue os `id` das duas pontas (`porta_destino` aponta para o `id` da outra).
5. Ponha itens, pistas, luzes, robôs e (se for sala segura) o `Checkpoint`.
6. Registre a fase em `dados/fases/` se for a primeira cena (o do Centro é `04_convivencia.tres`, com `cena` vazia).
7. Abra no Godot e jogue a sala. O Godot gera `.import` e `.uid`: **commite os dois**.

---

## 10. Bloco de salas: o que existe e o que está em aberto

### 10.1 O que já está no jogo

Tudo da cadeia da seção 6.3, e, desde 2026-10-12 (PR #98), as melhorias propostas na seção 12 de `bloco_de_salas.md`:

| Melhoria | Como ficou |
|---|---|
| Brecha 101 ↔ 102 | Passagem lateral na altura y = 272, atalho de fuga entre as duas |
| Porta de serviço 203 ↔ 206 | Trancada; o trinco fica do lado da 206 (primeiro `E` destranca, o segundo atravessa); da 203, "Trancada pelo outro lado" |
| Três setores de piso nos corredores | Oeste areia/mato ×0,5; centro lajota e tapete ×1,0; leste lajota solta ×1,5 |
| Nichos de parede | 2 por corredor (x 1280 e 1920 no térreo e no 1º andar), longe das faixas de luar |
| Fresta da barricada (103) | "Espiar o corredor": o Gabriel vê o corredor de dentro da 103 antes de sair |
| Mapa de giz | A lousa da 103 virou o mapa do bloco desenhado pela Clarice |
| Estalos do teto | 5 pontos no térreo, a cada 12 a 28 s, se o Gabriel estiver a menos de 280 px |
| Pedra pelo buraco | O Rastreador do térreo fica 18 s dentro da 104, investigando |
| Queda amortecida | Caixas de papelão embaixo do buraco, com baque abafado |
| Sala 205 | Lousa limpa com 8 tracinhos, calha fluorescente, zumbido de 60 Hz: "intacta demais" |

### 10.2 Limites conhecidos

- O robô "dentro da 104" é contado em tempo real: se o jogador pausar, a janela de 18 s continua.
- Os estalos do teto são sorteados e não seguem a posição real da Sentinela.
- O nicho esconde da **visão**, não do **contato**: se a rota do robô passar colada à parede, ele esbarra no Gabriel.
- O fator de piso é **por zona de corredor**; as salas com chão de areia ou mato (102, 106, 202, 204, 206) têm fator 1, então o chão "de areia" delas não abafa.
- A validação das melhorias foi **estática** (leitura de cena e código). Vale jogar a fase inteira antes de redesenhar qualquer coisa.

### 10.3 Pendente

- **Por que a sala 205 está intacta** (decisão de história, não do level design).
- **A Diana** está na 103 mas não aparece (sem visual).
- **O sonho** da sala segura: o que ele mostra é pendência do Enredo (12.4), e dormir ainda não existe.
- **A saída**: a porta corta-fogo hoje abre a entrada do Bunker. Quando o Centro de Convivência existir, a `fim_do_bloco` deve levar a ele.
- **A seção 12.7** do `bloco_de_salas.md` (a formalização acadêmica) está sendo atualizada no PR #99 com os números do #98.

---

## 11. Centro de Convivência: o ponto de partida

### 11.1 O que está decidido (na `main`)

| O quê | Decisão |
|---|---|
| **Nome** | Centro de Convivência |
| **Posição** | Depois do Bloco de salas: Biblioteca → Bloco de salas → Centro de Convivência |
| **Como se chega** | Pela porta corta-fogo do 1º andar do Bloco de salas |
| **O que vem depois** | **Não decidido.** O Bunker continua sendo o Ato 3, mas a posição dele na ordem das fases está em aberto |

**Todo o resto é pendência.** Pelo documento da fase na `main`, o que está em aberto é:

1. Qual é o objetivo do Gabriel aqui e o que bloqueia o caminho.
2. Qual personagem aparece (ou se a fase não tem personagem) e qual parte ele traz.
3. Quais robôs ficam aqui e o que a fase ensina de novo.
4. Onde fica a sala segura.
5. Para onde leva a saída (Bunker, Labirinto ou outra área).
6. Como fica o visual e quanto dele mostra a tecnologia de 3026.

**O que do GDD não vale mais:** "os Calouros andam em grupo" (os inimigos são os robôs) e a tabela da semana de provas (roteiro antigo). O que vale como esboço, se o grupo confirmar: "estrutura aberta tomada pelo mato, balcões e mesas cobertos de raízes, o céu aparecendo pela cobertura", área ampla com poucos esconderijos. O Enredo cita a **cantina** como uma das relíquias do campus; se ela fica nesta fase, falta decidir.

### 11.2 A proposta do PR #97 (não aprovada)

O **PR #97** (`docs/fase-centro-de-convivencia`, aberto) propõe um projeto completo para a fase. **Não está na `main`**, e vários pontos dele dependem de decisão do Davi (ver 11.3). Serve como ponto de partida para discutir.

```
                     [PASSARELA DE ACESSO] (do Bloco de salas)
                              │
                              ▼ (escada)
    [ALA DAS CANTINAS] ◄───► [PÁTIO CENTRAL] ◄───► [ANEXO DA GRÁFICA]
            │                 (amplo, Sentinelas)          │
            ▼                         │                    ▼
   [DEPÓSITO / CÂMARA]                ▼            [POSTO DE MANUTENÇÃO]
 (Célula de Energia)         [RAMPA DO SUBSOLO]      (sala segura)
                                      │
                                      ▼
                               (para o Bunker)
```

| Cena proposta | Função | Tamanho proposto | Piso | Robô |
|---|---|---|---|---|
| `passarela_acesso` | Chegada (mezanino) | 640 × 180 | Concreto | — |
| `patio_central` | Pátio das mesas e raízes (descampado sob o luar) | 1280 × 360 | Lajota, terra, areia | 2 **Sentinelas** em rotas cruzadas |
| `cantina` | Balcões e cacos de louça (piso que denuncia) | 640 × 260 | Cerâmica e vidro | 1 **Rastreador** (patrulha por fora) |
| `deposito_cantina` | Câmara frigorífica; **Célula de Energia** | 400 × 240 | Concreto liso | — |
| `grafica_rapida` | Quadro de comutação; **puzzle de coloração de grafos** | 480 × 260 | Lajota | — |
| `posto_manutencao` | **Sala segura** | 400 × 240 | Concreto e tapete | — |
| `rampa_subsolo` | Comporta que dá no Bunker | 640 × 360 | Concreto e brita | Sentinela com rota nova depois da energia |

**O arco proposto:** chegar pela passarela → atravessar o pátio aberto entre as Sentinelas, usando mesas e raízes como cobertura → achar a sala segura (a ordem de manutenção diz onde está a Célula de Energia) → infiltrar a cantina, contornando os cacos ou distraindo o Rastreador com pedra → pegar a Célula → resolver o **puzzle de coloração de grafos** na gráfica (4 setores, 3 frequências) → com a energia, **holofotes giratórios** acendem no pátio e a ronda muda → voltar pelo pátio e abrir a comporta da rampa.

**Itens propostos:** Célula de Energia (item-chave), 3 pilhas, 1 clarão, 3 pedras, e 2 documentos (panfleto da Semana Universitária de 2024; ordem de manutenção de 3026).

### 11.3 O que precisa de decisão antes de construir

| Ponto | Por quê |
|---|---|
| **Falta um personagem** | A regra do Ato 2 é "cada fase leva a um personagem". Todos já têm lugar: Clarice e Diana na 103, Zane e Henrique no bunker, Baltazar na Biblioteca, Carlos no D-Tec. A proposta não põe ninguém no Centro. Ou a regra se flexibiliza, ou alguém muda de lugar. **É decisão do Davi e do grupo** |
| **A proposta fixa "Centro → Bunker"** | Ela altera o Enredo (seções 8 e 12.5) para dizer isso, mas a `main` diz que a posição do Bunker **não está decidida**. O Enredo só se edita quando o Davi pedir |
| **A Diana no rádio** | A proposta diz que "Clarice e Diana guiam pelo rádio". No cânone, quem fala pelo rádio é a **Clarice** (com o que o Henrique vê); a Diana não tem voz definida |
| **Peças de kit novas** | Mesa redonda de concreto, raízes, balcão de cantina, holofote giratório, cancela da rampa. Toda arte é do Davi (issue `arte`, placeholder enquanto isso) |
| **Escopo** | São 7 cenas, um puzzle novo (`painel_comutacao.tscn`, que não existe), holofotes e uma cadeia de Markov nas Sentinelas. Pergunte ao Davi quanto disso entra |
| **Conflito de arquivos** | O PR #97 nasceu antes do #98 e mexe em `docs/`; pode precisar de atualização com a `main` |

### 11.4 Para o Centro de Convivência funcionar com o que já existe

- **Para cada sala,** o documento da fase usa o formato de [`template_fase.md`](template_fase.md): topologia, objetivos, robôs, puzzles, sala segura, registros.
- **Reaproveitável:** `painel_codigo` (cadeado), `grade_seguranca`, `visivel_com_marca` (luar e holofote por marca), `zona_de_piso` (cacos de vidro na cantina: fator > 1), `terminal_alarme`/`sirene` (distração), `nicho_esconderijo`, `checkpoint`, `gatilho_transmissao`.
- **Não existe ainda:** o puzzle de coloração de grafos, o holofote giratório, a cadeia de Markov nas rotas (hoje as rotas são sequências fixas de pontos), e as peças de cenário do Centro.
- **Computação que a fase pode mostrar** (requisito da disciplina): coloração de grafos (puzzle), Markov (rondas), BFS (cacos de vidro denunciam), produto escalar (visão em campo aberto). Ver [`../computacao/grade_e_coloracao.md`](../computacao/grade_e_coloracao.md).

---

## 12. Como trabalhar e entregar

O grupo é de 4 pessoas e o Davi é o revisor principal. As regras completas estão em [`CONTRIBUTING.md`](../../CONTRIBUTING.md); o essencial:

1. **Nunca faça commit nem push direto na `main`.** Trabalhe numa branch `tipo/descricao-curta` (ex.: `feat/centro-convivencia-patio`, `docs/centro-convivencia`).
2. **Commits pequenos**, no formato `tipo: o que mudou`, em português.
3. **Abra o PR** para a `main` usando o modelo de `.github/pull_request_template.md`. O Davi é o revisor principal, e o PR só é mesclado depois da revisão.
4. **Godot 4.7.x**, a mesma versão de todos. Abra o `project.godot` da sua pasta.
5. **Commite os `.import` e `.uid`.** Nunca commite `.godot/`.
6. **Scripts `.gd` não têm comentários** (nem `#` nem `##`). O que precisa de explicação vai para `docs/`.
7. **Nomes** em `snake_case`, em português, sem acento em nome de arquivo. Uma cena por sistema, sala e personagem.
8. **Não edite cena ou arte de outra pessoa** sem combinar.
9. **Comunicação entre sistemas por sinais**, não por referência direta entre cenas.
10. **Arte:** abra uma issue com o rótulo `arte` dizendo o quê, para onde (qual sala), como (descrição e referência), tamanho e quando. Use placeholder enquanto não chega.
11. **Decisão de design ou de história** (uma sala nova, um puzzle novo, um personagem num lugar) entra em `docs/decisoes.md`. Se for de história, entra **no mesmo PR** no Enredo Principal, **mas só se o Davi pedir**.
12. **Documente a fase** em `docs/fases/<fase>.md`, no formato do template, e atualize o índice em `docs/README.md` e `docs/fases/README.md`.

**Antes de abrir o PR:** abra a cena no Godot e jogue. Confira que as portas ligam nas duas pontas, que os `.import` e `.uid` estão no commit e que não há comentário nos `.gd`.

---

## 13. Onde ler mais

| Para saber de… | Leia |
|---|---|
| A história inteira e as pendências | [`../historia/enredo_principal.md`](../historia/enredo_principal.md) |
| Cada personagem | [`../historia/personagens/`](../historia/personagens/) |
| Os robôs | [`../historia/personagens/robos.md`](../historia/personagens/robos.md) e [`../computacao/ia_e_perseguicao.md`](../computacao/ia_e_perseguicao.md) |
| Bloco de salas, completo | [`bloco_de_salas.md`](bloco_de_salas.md) (seção 12: melhorias; 12.8: o que foi implementado) |
| Centro de Convivência (o que está decidido) | [`centro_de_convivencia.md`](centro_de_convivencia.md) |
| Modelo para documentar uma fase | [`template_fase.md`](template_fase.md) |
| Andar, correr, som, piso, portas | [`../mecanicas/movimentacao_e_terreno.md`](../mecanicas/movimentacao_e_terreno.md) |
| Esconderijos e distração | [`../mecanicas/furtividade_e_esconderijos.md`](../mecanicas/furtividade_e_esconderijos.md) |
| Luz e lanterna | [`../mecanicas/iluminacao_e_lanterna.md`](../mecanicas/iluminacao_e_lanterna.md) |
| Itens, inventário e gadgets | [`../mecanicas/itens_e_inventario.md`](../mecanicas/itens_e_inventario.md) |
| Hackeamento de portas | [`../mecanicas/hackeamento.md`](../mecanicas/hackeamento.md) |
| Vida e checkpoint | [`../mecanicas/vida_e_checkpoint.md`](../mecanicas/vida_e_checkpoint.md) |
| Registros, transmissões e caderno | [`../mecanicas/registros_e_caderno.md`](../mecanicas/registros_e_caderno.md) |
| Grafos, A\*, Markov, coloração | [`../computacao/`](../computacao/README.md) |
| Estilo de arte | [`../visao_geral/estilo_artistico.md`](../visao_geral/estilo_artistico.md) |
| Papéis do grupo e como pedir arte | [`../equipe.md`](../equipe.md) |
| Histórico de decisões | [`../decisoes.md`](../decisoes.md) |
| Regras de git | [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md) |
