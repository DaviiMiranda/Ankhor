# Fase — Centro de Convivência (a Praça de Alimentação)

> **Status:** Jogável (11 salas: a praça com 4 restaurantes e o segundo andar com 3 lojas, puzzle de Coloração de Grafos, Célula de Energia, letreiros e holofotes que acendem com a energia, transmissões do Zane pelo rádio)  
> **Área:** o Centro de Convivência da Unifor, em 3026: uma praça de alimentação sob uma cúpula de vidro quebrada  
> **Ordem na história:** **quarta fase**, depois do Labirinto ([`labirinto.md`](labirinto.md)) e antes do Bunker ([`bunker.md`](bunker.md)).  
> **Como se chega:** Pelo duto do alçapão da oficina do Zane no fim do Labirinto, saindo em `passarela_acesso`.  
> **Saída:** O elevador de carga do Churrasco Solar (`loja_4`), que desce para a entrada do Bunker (`fim_da_convivencia`).  
> **No menu Fases:** Cadastrado em `dados/fases/04_convivencia.tres` ("Convivência").

---

## 1. Visão Geral da Área

- **Nome do Local:** Centro de Convivência da Unifor, ano de 3026.
- **O formato é um arco.** A planta é um semicírculo: a **entrada** no meio de cima e **quatro restaurantes** na curva. Em vista lateral, o fundo da sala (a parede de trás) desce para os lados, e cada restaurante fica numa altura diferente (ver a seção 6).
- **Ambientação Visual:**
  - **É noite**, sob uma **cúpula de vidro** de nervuras de aço. Vários painéis quebraram e o céu e o luar entram. As nervuras e os anéis da cúpula são desenhados por código (seção 6).
  - O piso é de placas de pedra escura de 40 × 16 px, com musgo que brilha, rachaduras e, no meio, o **emblema** de anéis com o holograma central.
  - As fachadas são de cerâmica clara e grafite, com vitrines, toldos e **letreiros de neon**, **cada restaurante de uma cor**: âmbar, verde, vermelho e magenta. A cor é a mesma da luz que a vitrine joga no chão, da trilha de piso que liga a porta ao emblema e do interior do restaurante.
  - **Tecnologia de 3026:** mesas com projetor de cardápio em holograma, guarda-sóis de luz, totens de pedido, postes de luz âmbar, árvores que cresceram sob a cúpula e brilham em verde-água.
  - Quando o puzzle da cozinha é resolvido (marca `convivencia_energia`), a energia volta: os **letreiros e as vitrines acendem** e os **holofotes da cúpula** ligam (as Sentinelas mudam de rota).
- **Comunicação:**
  - Não há nenhum personagem em pessoa nesta fase. Todo o contato e orientação vêm do **Zane pelo rádio** (`zane_convivencia_01` e `zane_convivencia_02`).

---

## 2. Topologia e Salas (Nós do Grafo)

### 2.1 Mapa do Grafo

```
                       [PASSARELA DE ACESSO] (vem do Labirinto)
                                  │
                           [entrada da praça]
        LOJA 2            LOJA 1  │  PRAÇA CENTRAL  │  LOJA 3            LOJA 4
   (Self Nebulosa)    (Tapioca)  ─┴─  (arco, 2       ─┴─  (Pizzaria        (Churrasco
        │              Orbital)        Sentinelas)         Quasar)           Solar)
        ▼             sala segura                       quadro de comutação     │
  [CÂMARA FRIA]                                                                 ▼
  (Célula de Energia)                                              [ELEVADOR DE CARGA]
                                                                       (para o Bunker)
```

A praça é o centro do grafo: as quatro lojas, a passarela e a escada do mezanino ligam só a ela. A única sala do térreo que não liga à praça é a **câmara fria**, que se alcança pelo Self Nebulosa.

O **segundo andar** (opcional, seção 7) é outro pedaço do grafo, pendurado na praça pela escada:

```
   [PRAÇA CENTRAL] ──escada──► [SEGUNDO ANDAR (mezanino)]
                                  │            │            │
                            [GRÁFICA     [LOJA            [CINE
                             QUÂNTICA]  UNIVERSITÁRIA]   ANDRÔMEDA]
```

### 2.2 Tabela de Salas

| ID da Cena (`cenas/salas/centro_de_convivencia/`) | Nome / Função | Dimensões | Piso | Conexões | Esconderijos | Ameaça |
|---|---|---|---|---|---|---|
| `passarela_acesso` | Passarela Superior (chegada, checkpoint, rádio) | 640 × 180 px | chapa de aço | `praca_central` | — | Nenhuma |
| `praca_central` | Praça Central, em arco, com 4 restaurantes, a entrada e a escada do mezanino | 2000 × 560 px | pedra e musgo | passarela, as 4 lojas e a escada | Mesas, árvores, 2 nichos de manutenção | 2 **Sentinelas** (rotas em volta das mesas) |
| `loja_1` | **Tapioca Orbital**: cafeteria, **sala segura** com a Ordem de Serviço | 400 × 240 px | madeira clara | `praca_central` | — | Nenhuma |
| `loja_2` | **Self Nebulosa**: restaurante de bufê, com a faixa de louça quebrada | 640 × 280 px | xadrez brilhante | `praca_central`, `camara_fria` | Nicho de serviço | 1 **Rastreador** |
| `camara_fria` | Câmara fria do Self Nebulosa: onde está a **Célula de Energia** | 400 × 240 px | grade de aço e gelo | `loja_2` | — | Nenhuma |
| `loja_3` | **Pizzaria Quasar**: cozinha com o forno de plasma e o **quadro de comutação** (o puzzle) | 480 × 260 px | ladrilho vermelho | `praca_central` | — | Nenhuma |
| `loja_4` | **Churrasco Solar**: bar com a grelha solar e o **elevador de carga** (a saída) | 640 × 360 px | piso escuro com frisos | `praca_central`, elevador | Nicho de serviço | 1 **Sentinela** |
| `segundo_andar` | **Mezanino** (opcional): o anel em volta do vazio, com corrimão de vidro | 2000 × 640 px | placas de aço e passadeira | escada da praça, `grafica`, `loja_uni`, `cinema` | 2 nichos de manutenção | 1 **Sentinela** (ronda de ida e volta) |
| `loja_uni` | **Loja Universitária**: moletons, araras, o brasão e o provador | 560 × 240 px | carpete azul | `segundo_andar` | Provador (nicho) | Nenhuma |
| `grafica` | **Gráfica Quântica**: plotters, copiadoras e a ordem de impressão parada | 560 × 240 px | concreto polido | `segundo_andar` | Nicho dos fundos | Nenhuma |
| `cinema` | **Cine Andrômeda**: saguão com bilheteria e bomboniere, a sala com a tela que chia e o **cofre** (puzzle da seção 7.5) | 800 × 280 px | carpete de veludo | `segundo_andar` | Nicho atrás da cortina | Nenhuma |

---

## 3. Objetivos e Progressão

### 3.1 Objetivo Principal
Atravessar a praça, achar a **Célula de Energia** na câmara fria do Self Nebulosa, resolver o **Puzzle de Coloração de Grafos** no quadro de comutação da cozinha da Pizzaria Quasar e usar a energia para destravar o **elevador de carga** do Churrasco Solar, que desce para o **Bunker**.

### 3.2 Passo a Passo

1. **Chegada e Contato do Zane (`passarela_acesso`):**
   - Gabriel sai pelo duto na passarela. A escotilha se fecha atrás dele. O **Zane** chama pelo rádio (`zane_convivencia_01`): fala das duas Sentinelas na praça, manda usar as mesas, as árvores e os nichos, e aponta a **Tapioca Orbital** como sala segura.
2. **Travessia da Praça (`praca_central`):**
   - Gabriel entra pelo portão do meio. As Sentinelas rondam em volta do conjunto de mesas, por corredores livres (`rota`). Mesas, árvores e postes cortam a linha de visão, e os 2 nichos de manutenção (nas fachadas) escondem quem fica parado no escuro. Há 3 pedras para distração.
3. **Sala Segura e Pista da Célula (`loja_1`):**
   - Na Tapioca Orbital há um **checkpoint**, uma pilha, uma cápsula de clarão e a **Ordem de Serviço** (`ordem_manutencao_convivencia`), que diz que a célula reserva foi levada para o gerador da **câmara fria do Self Nebulosa**.
4. **Infiltração no Self Nebulosa (`loja_2` e `camara_fria`):**
   - No salão, um **Rastreador** patrulha perto de uma faixa de **cacos de louça e vidro** (`ZonaDePiso` com `fator_ruido = 2.0`).
   - O jogador contorna pelas passadeiras das pontas (`fator_ruido = 0.6`) ou distrai o Rastreador com pedras para entrar na câmara fria e pegar a **Célula de Energia** (`celula_energia.tres`) e 1 pilha.
5. **Puzzle de Coloração de Grafos (`loja_3`):**
   - Na cozinha da Pizzaria Quasar, Gabriel usa a Célula de Energia no **quadro de comutação** e resolve o **Puzzle de Coloração de Grafos**: 4 setores (Norte, Leste, Sul, Oeste) em anel com diagonal Norte-Sul (5 arestas: N-L, L-S, S-O, O-N, N-S) precisam receber uma das 3 fases (Fase A azul, Fase B amarela, Fase C vermelha) sem que setores vizinhos compartilhem a mesma fase ($\chi(G) = 3$).
   - Ao sincronizar as fases, a marca `convivencia_energia` é ativada.
6. **Letreiros acesos e Saída pelo Elevador (`praca_central` e `loja_4`):**
   - Com `convivencia_energia`, os letreiros e as vitrines da praça acendem e os **holofotes da cúpula** ligam (`revela_quem_passa = true`); as Sentinelas mudam de rota (`rota_energia`).
   - O **Zane** avisa pelo rádio (`zane_convivencia_02`) que o elevador destravou, mas as luzes ligaram.
   - Na `loja_4`, a porta do elevador de carga se recolhe e a porta leva a `fim_da_convivencia.tscn`, abrindo a entrada do **Bunker**.
7. **Segundo andar (opcional):** a escada ao lado da entrada da praça sobe para o mezanino, que tem uma Sentinela de ronda, mais pedras e pilhas, três lojas para explorar e dois nichos. Não é preciso para terminar a fase (seção 7).

---

## 4. Itens, Documentos e Transmissões

| Recurso | Arquivo | Onde fica |
|---|---|---|
| **Célula de Energia** | `dados/itens/celula_energia.tres` | `camara_fria` |
| **Pilhas (7)** | `cenas/itens/pilha_no_chao.tscn` | `passarela_acesso`, `loja_1`, `camara_fria`, `segundo_andar`, `loja_uni`, `grafica`, `cinema` |
| **Cápsulas de Clarão (2)** | `dados/itens/clarao.tres` | `loja_1` e o prêmio do cofre do `cinema` |
| **Pedras (9)** | `dados/itens/pedra.tres` | `praca_central` (3), `segundo_andar` (2), `grafica` (2), `loja_uni` (1), `cinema` (1) |
| **Panfleto da Semana Universitária (2024)** | `dados/documentos/panfleto_universitario.tres` | `loja_3` |
| **Ordem de Serviço (3026)** | `dados/documentos/ordem_manutencao_convivencia.tres` | `loja_1` |
| **Aviso da Loja Universitária (2025)** | `dados/documentos/aviso_loja_universitaria.tres` | `loja_uni` |
| **Ordem de Impressão (3026)** | `dados/documentos/ordem_impressao_grafica.tres` | `grafica` (explica por que a escada de emergência da praça está interditada) |
| **Canhoto do Cine Andrômeda** | `dados/documentos/ingresso_cine_andromeda.tres` | `cinema` (não tem nome: não é pista do cofre) |
| **Bilhete do lanterninha** | `dados/documentos/bilhete_lanterninha_cofre.tres` | `cinema`, no balcão da bomboniere |
| **Canhoto do Léo, da Bia e do Caio** | `dados/documentos/canhoto_leo.tres`, `canhoto_bia.tres`, `canhoto_caio.tres` | `cinema`: o do Léo no saguão, o da Bia na frente da fileira de trás da sala e o do Caio dentro do nicho da cortina |
| **Zane no rádio (chegada)** | `dados/transmissoes/zane_convivencia_01.tres` | `passarela_acesso` |
| **Zane no rádio (luzes acesas)** | `dados/transmissoes/zane_convivencia_02.tres` | `praca_central` (requer `convivencia_energia`) |

---

## 5. Onde está no projeto

| O quê | Onde |
|---|---|
| Cenas das salas | `cenas/salas/centro_de_convivencia/` |
| A descrição de cada sala (objetos, itens, rotas dos robôs, luzes) | `assets/modelagem/salas/centro_de_convivencia/salas_convivencia.py` |
| Montador das cenas (e das peças do kit) | `assets/modelagem/salas/centro_de_convivencia/montar_convivencia.py` |
| Kit da praça (porta, letreiros, objetos) | `cenas/cenario/praca/`, sprites em `assets/sprites/cenario/praca/` |
| Fundo da praça, em arco (cúpula, fachadas, piso) | `assets/modelagem/cenario/gerar_praca.py` |
| Fundos dos restaurantes, da câmara e da passarela, e os letreiros | `assets/modelagem/cenario/gerar_interiores.py` e `gerar_restaurantes.py` |
| Objetos (mesas, balcões, forno, árvore...) | `assets/modelagem/cenario/gerar_praca_objetos.py` |
| Segundo andar: fundo do mezanino, corrimão, escadas, fachadas e letreiros | `assets/modelagem/cenario/gerar_andar2.py` |
| Fundos das três lojas do mezanino | `assets/modelagem/cenario/gerar_interiores_andar2.py` |
| Objetos do mezanino e das lojas (e a tela animada do cinema) | `assets/modelagem/cenario/gerar_andar2_objetos.py` |
| Som da escada | `assets/modelagem/audio/gerar_efeitos_escada.py` |
| Cofre do cinema (cena, script e como reutilizar) | `cenas/sistemas/cofre.tscn`, `scripts/sistemas/cofre.gd` e [`../mecanicas/cofre_e_codigos.md`](../mecanicas/cofre_e_codigos.md) |
| Porta de vidro dos restaurantes | `assets/modelagem/cenario/gerar_porta_restaurante.py` e o som em `assets/modelagem/audio/gerar_efeitos_porta_restaurante.py` |
| Base comum (geometria do arco, cores de neon, texto em pixel) | `assets/modelagem/cenario/gerar_praca_base.py` |
| Célula de Energia (item) | `assets/modelagem/cenario/gerar_convivencia.py` |
| Puzzle de Coloração de Grafos | `cenas/sistemas/painel_comutacao.tscn`, script `scripts/sistemas/painel_comutacao.gd` |
| Fase no menu | `dados/fases/04_convivencia.tres` |

Para refazer tudo, nesta ordem:

```bash
python assets/modelagem/cenario/gerar_porta_restaurante.py
python assets/modelagem/cenario/gerar_praca.py
python assets/modelagem/cenario/gerar_restaurantes.py
python assets/modelagem/cenario/gerar_praca_objetos.py
python assets/modelagem/cenario/gerar_andar2.py
python assets/modelagem/cenario/gerar_andar2_objetos.py
python assets/modelagem/audio/gerar_efeitos_porta_restaurante.py
python assets/modelagem/audio/gerar_efeitos_escada.py
python assets/modelagem/salas/centro_de_convivencia/montar_convivencia.py
```

---

## 6. Conteúdo de computação: o arco, o piso e o brilho

- **A parede em arco (equação da elipse).** A sala tem 25 colunas de 80 px. A parede de cada coluna encosta no chão na altura `y = 112 + H * (1 - raiz(1 - (k * u)^2))`, com `u` indo de -1 (ponta esquerda) a 1 (ponta direita) e `H = 420`: no meio dá 112, como numa sala comum, e nas pontas a curva fica quase vertical, como o arco da planta. As alturas são arredondadas para múltiplos de 16 px. As colisões são uma caixa por coluna, do topo da sala até essa altura (`LimitesArco`), e valem também para os robôs.
- **O piso sem emenda.** As placas de 40 × 16 px são contadas a partir do canto da sala, e não de cada coluna, e a fileira de baixo começa 20 px adiante (como tijolos). Como a altura de cada coluna é múltipla de 16, uma coluna continua a vizinha sem emenda, mesmo com a parede acabando em alturas diferentes.
- **A cúpula (coordenadas polares).** As nervuras saem de um ponto abaixo da imagem. Cada pixel tem um ângulo e uma distância até esse ponto: nervura onde o ângulo está perto de um múltiplo de 6°, anel onde a distância está perto de um múltiplo de 64. Cada retângulo curvo é um vidro, e um sorteio decide se está inteiro, quebrado ou coberto de cipó.
- **O emblema (elipse normalizada).** Cada anel é um intervalo de `d = raiz(((x - cx)/rx)^2 + ((y - cy)/ry)^2)`; os 16 raios vêm do seno do ângulo (`|sen(8 * theta)|` pequeno).
- **O brilho dos neons (mapa de luz).** O Godot escurece a sala toda e não dá para "acender" uma imagem só pintando mais claro. Então cada fundo ganha uma segunda imagem só com os pixels que brilham (os que têm a cor exata de um tom claro de neon). Ela entra como a **textura de uma `PointLight2D`**, e a luz multiplica o que está embaixo: `cor_final = cor * (escuridão + luz)`. Os pixels de neon, que são coloridos e claros, ficam muito mais brilhantes que o resto. Na praça essa luz só liga com a marca `convivencia_energia`.
- **Busca em grafo.** O puzzle de coloração e a patrulha dos robôs (A*, BFS do som) são os de sempre; ver [`../computacao/`](../computacao/).

---

## 7. O segundo andar (o mezanino)

O Davi desenhou a planta de um segundo andar: um **anel em volta do vazio da praça**, com o **hall** (onde o jogador chega pela escada) no meio de cima, a **Gráfica** e a **loja de roupas da universidade** de um lado, o **cinema** do outro, **corrimão nas bordas** e o andar de baixo escuro, que não aparece. É uma área opcional, para explorar com a ameaça de uma Sentinela.

### 7.1 Como se chega

- **A escada da praça** fica na coluna 14, ao lado da entrada (`porta praca_escada`, com a placa MEZANINO), e leva ao hall do mezanino (`mezanino_escada`, com a placa PRAÇA). O som é `escada.wav`.
- **A escada da coluna 10 está interditada** (grade e fita de aviso): a porta avisa e não abre. A Ordem de Impressão da gráfica explica o porquê: a máquina parou no meio de uma ordem de milhares de avisos de área interditada.

### 7.2 O corredor

- O corredor é uma **faixa de 112 px de profundidade que acompanha o arco da praça**: a parede de trás está em `y_base(c)` (a mesma equação da seção 6) e a **beirada da laje** em `y_frente(c) = y_base(c) + 112`. Como `y_base` muda de 16 em 16 px (de 64 px nas pontas), a beirada vira uma escada de degraus.
- **Colisões:** as caixas por coluna da parede de trás (`LimitesArco`, como na praça) mais uma caixa por coluna na beirada (`Beirada<c>`, do `y_frente - 4` para baixo). O Gabriel e os robôs andam só na faixa.
- **O corrimão** é um sprite à parte (`corrimao_andar2.png`) na camada `Frente`, desenhado por cima do Gabriel (ele anda sempre atrás dele): passa-mão de aço com uma linha de luz ciano, painéis de vidro em pontilhado (para ver o Gabriel através), postes de 40 em 40 px, painéis quebrados aqui e ali e, a cada degrau da beirada, um poste alto que cobre o desnível. A luz do corrimão entra no mesmo mapa de luz do fundo.
- **O vazio** abaixo da beirada é quase preto, com uma névoa azulada que sobe e uns pontinhos de neon bem longe (o térreo, que o jogador não vê).
- **Ameaça:** uma **Sentinela** faz ronda de ida e volta pelo corredor, um ponto por coluna (`y_base + 56`). Os nichos das colunas 5 e 19, as lojas e a escada são os refúgios.
- **Energia:** com a marca `convivencia_energia`, os neons, os letreiros e o corrimão do mezanino acendem, como na praça.

### 7.3 As lojas

| Loja | Cor | O que tem |
|---|---|---|
| **Gráfica Quântica** (`grafica`, coluna 2) | limão | plotter, copiadora, guilhotina, impressora 3D, estante de resmas, mesa de corte; as faixas de segurança no piso; a Ordem de Impressão; 2 pedras, 1 pilha |
| **Loja Universitária** (`loja_uni`, coluna 7) | azul | araras, manequins de moletom, estante de camisetas, espelho, o brasão da universidade e o provador de cortina (nicho); o aviso da loja; 1 pedra, 1 pilha |
| **Cine Andrômeda** (`cinema`, coluna 22) | violeta | saguão com bilheteria, bomboniere e cordões de fila; a sala com a tela larga que chia ("sem sinal", animada, com a luz piscando) e duas fileiras de poltronas; o **cofre** do lanterninha e as pistas dele; 1 pilha, 1 pedra |

Cada loja tem a sua cor, a mesma da porta de vidro, do letreiro e da luz que a vitrine joga no chão do corredor. As portas de vidro e os letreiros são os mesmos tipos dos restaurantes (seção 5), em três cores novas (azul, limão e violeta).

### 7.4 Conteúdo de computação

- **A beirada em degraus** é a mesma equação do arco (seção 6) deslocada de 112 px: `y_frente(c) = y_base(c) + 112`.
- **O vazio** é um degradê vertical (`(1 - t)^1,4`, com `t` a profundidade abaixo da beirada) somado a um ruído de valor e a um pontilhado sorteado, em que a chance de cada pixel acender é proporcional a um feixe gaussiano `exp(-((x - x0)/46)^2)` que some com a profundidade.
- **A tela do cinema:** quatro quadros de barras de teste que deslocam uma barra a cada quadro, com chiado sorteado por pixel e uma faixa clara que sobe; a luz dela é uma `PointLight2D` com o script `luz_tremula.gd`.

### 7.5 O puzzle do cofre do cinema

Cada sala do mezanino vai ganhar um puzzle próprio, mesmo que não leve a história adiante. O do **Cine Andrômeda** é o primeiro:

- **O cofre cinza** fica no saguão, ao lado do arco da sala (`cenas/sistemas/cofre.tscn`, código de 3 dígitos). O prêmio é **1 cápsula de clarão**, que cai no chão ao abrir.
- **O bilhete do lanterninha** (na bomboniere) diz que o código são as poltronas dos três amigos dele, o **Léo**, a **Bia** e o **Caio**, só o número, sem a fileira, e que **a ordem foi embaralhada de propósito**. Não dá o código.
- **Os três canhotos** estão espalhados pelo cinema, cada um com o nome do amigo, a fileira e a poltrona: **Léo, fileira C, poltrona 4**, no saguão; **Bia, fileira F, poltrona 7**, na frente da fileira de trás da sala; **Caio, fileira B, poltrona 2**, escondido no nicho da cortina. Há ainda um canhoto sem nome (fileira F, poltrona 12) que não faz parte do puzzle.
- **A combinação** é **Bia, Caio, Léo: 7-2-4**. Com três números, o jogador testa no máximo 6 ordens (4-7-2, 4-2-7, 7-4-2, 7-2-4, 2-4-7, 2-7-4) até o cofre abrir. Errar não tem castigo.
- **Dica de leitura:** a anotação de cada documento vai para o Caderno (`N`), então o jogador consulta os números fora do painel.

Como o sistema funciona e como montar outros cofres: [`../mecanicas/cofre_e_codigos.md`](../mecanicas/cofre_e_codigos.md).
