# Fase — Centro de Convivência

> **Status:** Projeto da fase planejado e detalhado (2026-10-11). Define topologia, objetivos, robôs, puzzles e a ligação entre o Bloco de salas e o Bunker.
> **Área:** Centro de Convivência da Unifor, em 3026.
> **Posição na história:** Ato 2 (depois do Bloco de salas, antes do Bunker).
> **Como se chega:** Pela porta corta-fogo do 1º andar do Bloco de salas ([`bloco_de_salas.md`](bloco_de_salas.md)).
> **Saída:** Rampa técnica que leva à escotilha de entrada do Bunker ([`bunker.md`](bunker.md)).
> **No menu Fases:** Cadastrado em `dados/fases/04_convivencia.tres` ("Convivência").

---

## 1. Visão Geral da Área

- **Nome do Local:** Centro de Convivência da Unifor, ano de 3026.
- **Ambientação Visual:**
  - **É noite** sob céu escuro com estrelas (`ceu_noite.png`).
  - O Centro de Convivência é um grande espaço arquitetônico semi-aberto que conectava os blocos de aulas aos demais setores do campus.
  - Em 3026, a antiga cobertura metálica e translúcida desabou em vários pontos, permitindo que o luar azulado ilumine diretamente o chão.
  - O chão mistura lajotas rachadas, faixas de areia fina trazidas pelas dunas vizinhas e mato alto crescendo pelas frestas do piso.
  - Árvores de grande porte cresceram furando o piso de concreto; raízes espessas serpenteiam e engolem as tradicionais mesas redondas de concreto e os bancos fixos da praça de alimentação.
  - A antiga **cantina** (com balcões de aço inoxidável manchados, cacos de louça/vidro e placas de avisos desbotadas) e a **gráfica rápida** permanecem como relíquias do cotidiano universitário de mil anos atrás.
  - **Tecnologia futurista de 3026:** postes de refletores perimetrais com fiações blindadas expostas que levam energia em direção ao Bloco M, e câmeras de monitoramento predial automatizadas cujos motores giram suavemente (o Henrique acompanhando o pátio a partir da sala de dados do Bunker).
- **Atmosfera Sonora:**
  - Vento soprando através dos vãos da cobertura quebrada;
  - Estalos distantes de chapas metálicas e folhas secas raspando no piso;
  - Zumbido elétrico intermitente dos refletores que acendem na segunda metade da fase;
  - Transmissões de rádio da Clarice pontuadas por bipes de aviso.
- **Contraste no Passado (Sonho):**
  - O mesmo Centro de Convivência repleto de luz natural do meio-dia de Fortaleza, movimentado por dezenas de estudantes conversando, cheiro de café e salgados da cantina, barulho de passos e risadas — o choque dramático da solidão de 3026.

---

## 2. Topologia e Salas (Nós do Grafo)

### 2.1 Mapa do Grafo

```
                     [PASSARELA DE ACESSO] (do Bloco de salas)
                              │
                              ▼ (escada)
    [ALA DAS CANTINAS] ◄───► [PÁTIO CENTRAL] ◄───► [ANEXO DA GRÁFICA]
            │                 (Amplo, Sentinelas)          │
            ▼                         │                    ▼
   [DEPÓSITO / CÂMARA]                ▼            [POSTO DE MANUTENÇÃO]
 (Célula de Energia)         [RAMPA DO SUBSOLO]      (Sala Segura)
                                      │
                                      ▼
                               (para o Bunker)
```

### 2.2 Tabela de Salas

| ID da Cena | Nome / Função | Dimensões | Tipo de Piso | Conexões | Esconderijos | Ameaça |
|---|---|---|---|---|---|---|
| `passarela_acesso` | Passarela Superior / Mezanino | 640 × 180 px | Concreto | Bloco de salas, escada para o `patio_central` | Guarda-corpo e pilares | Nenhuma (ponto de chegada e rádio) |
| `patio_central` | Pátio das Mesas e Raízes | 1280 × 360 px | Lajota, terra e areia | `passarela_acesso`, `cantina`, `grafica_rapida`, `rampa_subsolo` | Atrás de mesas de concreto tombadas, raízes espessas | 2 **Sentinelas** (rotas cruzadas sob o luar) |
| `cantina` | Quiosque da Cantina / Balcões | 640 × 260 px | Cerâmica e cacos de vidro | `patio_central`, `deposito_cantina` | Embaixo da bancada do balcão | 1 **Rastreador** (patrulha do lado externo) |
| `deposito_cantina` | Depósito e Câmara Frigorífica | 400 × 240 px | Concreto liso | `cantina` | Entre prateleiras de mantimentos | Nenhuma |
| `grafica_rapida` | Anexo da Gráfica e Serviços | 480 × 260 px | Lajota | `patio_central`, `posto_manutencao` | Atrás de máquinas copiadoras | Nenhuma |
| `posto_manutencao` | Posto de Controle e Segurança | 400 × 240 px | Concreto e tapete | `grafica_rapida` | **Sala Segura** (robôs não entram) | Nenhuma |
| `rampa_subsolo` | Pátio de Carga e Rampa Técnica | 640 × 360 px | Concreto e brita | `patio_central`, comporta para o Bunker | Caçambas e contêineres de entulho | Sentinela com nova rota (após energização) |

---

## 3. Objetivos e Progressão

### 3.1 Objetivo Principal
Atravessar o descampado do Centro de Convivência e **destrancar a comporta de contenção da Rampa do Subsolo** para acessar o **Bunker** (onde estão Henrique e Zane).

### 3.2 O Obstáculo
A comporta magnética da rampa está sem alimentação elétrica primária. O relé manual de comutação na Gráfica está desarmado e necessita de uma **Célula de Energia de Alta Densidade** (armazenada na câmara da Cantina) e do alinhamento de frequências no quadro elétrico.

### 3.3 Passo a Passo

1. **Chegada e Alerta no Rádio (`passarela_acesso`):**
   - Gabriel chega pelo mezanino. Clarice avisa no rádio:
     > *"Gabriel, você tá na passarela do Convivência. O Henrique tá acompanhando o pátio pelas câmeras do circuito: tem duas Sentinelas cobrindo o pátio aberto em rotas cruzadas. Como a cobertura desabou, o luar revela qualquer um em pé no meio do descampado. Desce com calma e usa as mesas de concreto e as raízes pra quebrar a linha de visão."*
2. **Descida ao Pátio Central (`patio_central`):**
   - Gabriel desce as escadas. No pátio aberto, andar desprotegido sob os feixes de luar atrai a visão das Sentinelas.
   - O jogador aplica a mecânica de furtividade de pátio: agachar atrás das mesas de concreto tombadas e entre as raízes (`mecanicas/furtividade_e_esconderijos.md`).
3. **Inspeção da Rampa (`rampa_subsolo`):**
   - Gabriel tenta abrir a comporta da rampa. Mensagem: *"Cancela bloqueada. Relé de comutação sem carga auxiliar."*
4. **Localização da Sala Segura (`posto_manutencao`):**
   - Pelo anexo sul (passando pela antiga Gráfica), Gabriel encontra a sala de manutenção e a tranca por dentro com uma alavanca de aço.
   - Ponto de descanso e salvamento (checkpoint).
   - No quadro de avisos, uma ordem de manutenção de 3026 indica: *"Célula de energia reserva realocada para o gerador de emergência da câmara frigorífica da cantina (Setor Norte)."*
5. **Travessia até a Cantina e Infiltração (`cantina` e `deposito_cantina`):**
   - Gabriel precisa cruzar o pátio em direção à ala norte.
   - Próximo à cantina, um **Rastreador** patrulha. O piso diante do balcão está coberto de cacos de pratos e vidros quebrados (piso tático que amplifica o som dos passos).
   - Gabriel deve contornar pela passadeira de borracha da área de serviço ou lançar uma **pedra** para desviar o Rastreador.
   - No `deposito_cantina`, Gabriel recolhe a **Célula de Energia de Alta Densidade** e uma **pilha**.
6. **O Puzzle da Gráfica (`grafica_rapida`):**
   - Gabriel retorna à gráfica e insere a Célula de Energia no Quadro de Comutação.
   - O painel exige resolver o **Puzzle de Coloração de Grafos**: 4 nós de circuitos interconectados precisam ter suas frequências de fase reguladas (Cores: Azul, Amarelo, Vermelho) sem que dois setores vizinhos compartilhem a mesma frequência, evitando ressonância na rede de alta voltagem.
   - Ao resolver, uma chave geral arma: a energia é direcionada para a rampa.
7. **Mudança no Pátio (Holofotes de Vigilância Ativados):**
   - Com o circuito armado, os **holofotes perimetrais** do pátio acendem e passam a varrer o chão em arcos lentos (luz móvel programada).
   - Henrique/Clarice avisam no rádio: *"Gabriel, a comutação funcionou, mas armou os holofotes do pátio! O padrão das Sentinelas mudou, fica nas sombras!"*
   - O retorno pelo pátio exige cronometrar o deslocamento entre a sombra das mesas e o movimento dos refletores.
8. **Abertura da Rampa e Saída (`rampa_subsolo`):**
   - Na rampa, o painel agora exibe luz verde. Gabriel aciona a alavanca da comporta.
   - A comporta de aço sobe com um ruído mecânico pesado, revelando a descida protegida que dá na entrada do **Bunker**.
   - Fim da fase; transição para a fase do Bunker.

### 3.4 Grafo de Dependências

```
Passarela → Pátio → Verificar Rampa (cancela travada) → Sala Segura (pista da célula)
   → Infiltração na Cantina → Coleta da Célula de Energia → Puzzle de Coloração na Gráfica
   → Energização do Circuito (holofotes ativos / ronda alterada) → Comporta da Rampa destrancada → Entrada do Bunker
```

### 3.5 Tabela de Itens e Recursos

| Item | Local | Tipo | Utilidade |
|---|---|---|---|
| Célula de Energia | `deposito_cantina` | Item-chave | Alimenta o painel de comutação da Gráfica |
| Pilhas de Lanterna (3) | `passarela_acesso`, `deposito_cantina`, `posto_manutencao` | Consumível | Manter a lanterna operacional |
| Cápsula de Clarão (1) | `posto_manutencao` | Gadget | Defesa de emergência contra Sentinelas |
| Pedras (3) | `patio_central` (junto ao canteiro de entulho) | Gadget | Distrair o Rastreador nos cacos da Cantina |
| Panfleto Universitário (2024) | `grafica_rapida` | Registro | Documento de lore sobre a vida estudantil do passado |
| Ordem de Manutenção (3026) | `posto_manutencao` | Registro | Documento técnico explicando a localização da Célula |

---

## 4. Robôs e Ameaças

| Robô | Onde | Sentido Forte | O que o Jogador Aprende |
|---|---|---|---|
| **Sentinela (Alfa e Beta)** | `patio_central` | Visão ampla (cone de 60°) sob luar | Usar mesas de concreto e raízes para quebrar visão em áreas abertas; esperar o cone de visão passar |
| **Rastreador** | Área externa de `cantina` | Audição apurada | Evitar pisos com cacos de vidro/louça; usar passadeiras ou lançar pedras para distração |
| **Holofotes Perimetrais** | `patio_central` (após ligar energia) | Iluminação dinâmica ambiental | Cronometrar avanço com base em feixes de luz móveis |

- **Rotinas e Cadeia de Markov:** As Sentinelas no pátio não patrulham em linha reta óbvia; cada Sentinela possui um grafo de nós de vigilância (bancos, canteiros, postes) e seleciona o próximo nó com base em probabilidades de transição estocásticas (Cadeia de Markov), tornando a movimentação no descampado tensa e imprevisível.

---

## 5. Puzzles e Requisitos de Computação Gráfica

### 5.1 Puzzle de Coloração de Grafos (Quadro de Comutação da Gráfica)
- **Problema:** O comutador possui 4 polos de distribuição de carga que formam um grafo com arestas de interferência mútua (Topologia em anel com aresta diagonal: Setores Norte, Leste, Sul, Oeste).
- **Regra:** Cada setor precisa de um seletor de fase (representado pelas frequências $f_1, f_2, f_3$, com cores luminosas Azul, Amarelo, Vermelho). Dois setores adjacentes não podem ter a mesma frequência para não causar sobrecarga harmônica.
- **Número Cromático:** O grafo exige exatamente 3 frequências (número cromático $\chi(G) = 3$). O jogador resolve o minigame ajustando os seletores até que nenhum canal adjacente apresente conflito.
- **Relevância para a disciplina:** Demonstração prática do algoritmo de Coloração de Grafos aplicado a interfaces de puzzle interativo.

### 5.2 Propagação Acústica (BFS em Área Aberta vs Espaço Confinado)
- No pátio aberto, o ruído de passos se dissipa em raio radial amplo (atenuação com inverso do quadrado da distância), mas árvores e raízes atuam como barreiras com fator de amortecimento sonoro.
- Na cantina, pisar em cacos de louça dispara evento sonoro amplificado (180%), alertando o Rastreador do lado de fora via busca em largura (BFS) na malha de navegação.

---

## 6. Sala Segura e Sonho

- **Local:** `posto_manutencao` (Posto de Manutenção Predial, anexo à Gráfica).
- **Por que é segura:** Sala de alvenaria sólida reforçada, com porta corta-fogo manual trancável por ferrolho interno. Robôs não possuem rota nem detecção para dentro da sala.
- **Ambiente:** Um sofá antigo rasgado, mesa de apoio com lampião fraco, rádio de mesa e terminal de diagnóstico offline.
- **Evento do Sono:** Gabriel dorme no sofá. O sonho mostra o Centro de Convivência vivo em 2026: risos, sol da tarde, fila da cantina e o murmúrio dos universitários. Gabriel acorda no silêncio desolador e escuro de 3026 com estalos metálicos ao fundo.

---

## 7. Registros e Comunicações

- **Clarice no rádio:**
  - Chegada na passarela: aviso sobre o pátio aberto e as Sentinelas sob o luar.
  - Alerta pós-energização: aviso sobre a ativação dos holofotes e nova ronda dos robôs.
- **Documento 1 — Panfleto da Semana Universitária (2024):** Encontrado na Gráfica. Mostra a programação cultural de um tempo em que o campus vivia normalmente.
- **Documento 2 — Registro de Manutenção Técnica (3026):** Encontrado na Sala Segura. Dá a dica da Célula de Energia na câmara frigorífica da cantina e menciona evacuação de emergência do pessoal para as instalações subterrâneas (Bunker).

---

## 8. Estrutura Técnica no Godot

| Recurso | Caminho Previsto | Descrição |
|---|---|---|
| **Cenas das Salas** | `cenas/salas/centro_de_convivencia/` | 7 cenas (`passarela_acesso.tscn`, `patio_central.tscn`, `cantina.tscn`, `deposito_cantina.tscn`, `grafica_rapida.tscn`, `posto_manutencao.tscn`, `rampa_subsolo.tscn`) herdando `modelo_sala.tscn` |
| **Fase no Menu** | `dados/fases/04_convivencia.tres` | `nome = "Convivência"`, apontando para a cena inicial |
| **Kit de Cenário Novo** | `cenas/cenario/convivencia/` | Mesas redondas de concreto, raízes trepadeiras, balcões de cantina, holofotes rotativos, cancela da rampa |
| **Gerador de Assets** | `assets/modelagem/cenario/gerar_convivencia.py` | Script em Python para geração procedural dos blocos e texturas da fase |
| **Puzzle de Coloração** | `cenas/sistemas/painel_comutacao.tscn` | Interface de minigame de alinhamento de fases elétricas (coloração de grafos) |
