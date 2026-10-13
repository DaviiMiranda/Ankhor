# Fase — Centro de Convivência

> **Status:** Projeto da fase planejado e detalhado (2026-10-13), baseado na proposta de level design aprovada. Define topologia, objetivos, robôs, puzzles e a transição entre o Bloco de salas e o Bunker.
> **Área:** Centro de Convivência da Unifor, no ano de 3026.
> **Posição na história:** Ato 2 (depois do Bloco de salas, conectando à rampa de acesso do Bunker).
> **Como se chega:** Pela porta corta-fogo do 1º andar do Bloco de salas ([`bloco_de_salas.md`](bloco_de_salas.md)).
> **Saída:** Rampa técnica com cancela/comporta que dá na escotilha de entrada do Bunker ([`bunker.md`](bunker.md)).
> **No menu Fases:** Cadastrado em `dados/fases/04_convivencia.tres` ("Convivência").

---

## 1. Visão Geral da Área

- **Nome do Local:** Centro de Convivência da Unifor, ano de 3026.
- **Ambientação Visual:**
  - **É noite** sob céu escuro com estrelas (`ceu_noite.png`).
  - O Centro de Convivência é um grande espaço arquitetônico semiaberto que conectava os blocos de aulas aos demais setores do campus.
  - Em 3026, a antiga cobertura metálica e translúcida desabou em vários trechos, permitindo que o luar azulado ilumine diretamente o chão em feixes amplos.
  - O chão mistura lajotas rachadas, faixas de areia fina trazidas pelas dunas vizinhas e mato alto crescendo pelas frestas do piso de concreto.
  - Árvores de grande porte cresceram furando o piso de concreto; raízes espessas serpenteiam e engolem as tradicionais mesas redondas de concreto e os bancos fixos da praça de alimentação, criando quebras de linha de visão orgânicas.
  - A antiga **cantina** (com balcões de aço inoxidável manchados, cacos de louça/vidro no chão e placas de avisos desbotadas) e o **anexo da gráfica rápida** permanecem como relíquias do cotidiano universitário de mil anos atrás.
  - **Tecnologia futurista de 3026:** postes perimetrais com holofotes giratórios automatizados (com fiações blindadas expostas que levam energia em direção ao Bloco M) e câmeras de monitoramento predial automatizadas cujos servomotores giram suavemente (o Henrique acompanhando o pátio a partir da sala de dados do Bunker).
- **Atmosfera Sonora:**
  - Vento soprando através dos vãos da cobertura de aço retorcida;
  - Estalos distantes de chapas metálicas e folhas secas raspando no piso;
  - Zumbido elétrico intermitente e feixes de luz dos holofotes que acendem na segunda metade da fase;
  - Transmissões de rádio da Clarice pontuadas por bipes de aviso e estática.
- **Contraste no Passado (Sonho):**
  - O mesmo Centro de Convivência repleto de luz natural do meio-dia de Fortaleza em 2026, movimentado por dezenas de estudantes conversando, cheiro de café e salgados da cantina, barulho de passos e risadas — criando o contraste dramático com a solidão de 3026.

---

## 2. Topologia e Salas (Nós do Grafo)

### 2.1 Mapa do Grafo

```
                     [PASSARELA DE ACESSO] (do Bloco de salas)
                              │
                              ▼ (escada)
    [CANTINA ABANDONADA] ◄──► [PÁTIO CENTRAL] ◄──► [ANEXO DA GRÁFICA]
            │                 (descampado amplo)           │
            ▼                         │                    ▼
   [DEPÓSITO DA CANTINA]              │           [POSTO DE MANUTENÇÃO]
    (Célula de Energia)               ▼               (Sala Segura)
                             [RAMPA DO SUBSOLO]
                                      │
                                      ▼
                               (para o Bunker)
```

### 2.2 Tabela de Salas

| ID da Cena | Nome / Função | Dimensões | Tipo de Piso | Conexões | Esconderijos / Cobertura | Ameaça |
|---|---|---|---|---|---|---|
| `passarela_acesso` | Passarela Superior / Mezanino | 640 × 180 px | Concreto | Bloco de salas, escada para o `patio_central` | Guarda-corpo e pilares de concreto | Nenhuma (ponto de observação inicial) |
| `patio_central` | Pátio das Mesas e Raízes | 1280 × 360 px | Lajota, terra e areia | `passarela_acesso`, `cantina`, `grafica_rapida`, `rampa_subsolo` | Mesas de concreto tombadas, raízes espessas e troncos | 2 **Sentinelas** (rotas cruzadas sob o luar) |
| `cantina` | Cantina Abandonada / Balcões | 640 × 260 px | Cerâmica e cacos de vidro (Ruído ×2,0) | `patio_central`, `deposito_cantina` | Embaixo da bancada do balcão de inox | 1 **Rastreador** (patrulha área externa) |
| `deposito_cantina` | Depósito e Câmara Frigorífica | 400 × 240 px | Concreto liso | `cantina` | Entre prateleiras de mantimentos | Nenhuma |
| `grafica_rapida` | Anexo da Gráfica e Serviços | 480 × 260 px | Lajota | `patio_central`, `posto_manutencao` | Atrás de maquinários de impressão antigos | Nenhuma |
| `posto_manutencao` | Posto de Manutenção Predial | 400 × 240 px | Concreto e tapete | `grafica_rapida` | **Sala Segura** (robôs não entram) | Nenhuma |
| `rampa_subsolo` | Pátio de Carga e Rampa Técnica | 640 × 360 px | Concreto e brita | `patio_central`, comporta para o Bunker | Caçambas e contêineres de entulho | Sentinela reposicionada (após energização) |

---

## 3. Objetivos e Progressão

### 3.1 Objetivo Principal
Atravessar o descampado do Centro de Convivência e **destrancar a comporta de contenção da Rampa do Subsolo** para acessar o **Bunker** (onde estão Henrique e Zane).

### 3.2 O Obstáculo
A comporta magnética da rampa está desativada. O relé manual de comutação na Gráfica necessita de uma **Célula de Energia de Alta Densidade** (armazenada na câmara frigorífica da Cantina) e do alinhamento de frequências no quadro elétrico (resolução de conflito de fases por coloração de grafos).

### 3.3 Passo a Passo

1. **Chegada e Alerta no Rádio (`passarela_acesso`):**
   - Gabriel chega pelo mezanino vindo do Bloco de salas. A Clarice avisa pelo rádio:
     > *"Gabriel, você tá na passarela do Convivência. O Henrique tá acompanhando o pátio pelas câmeras do circuito: tem duas Sentinelas cobrindo o descampado em rotas cruzadas. Como a cobertura desabou, o luar revela qualquer um em pé no meio do pátio. Desce com cuidado e usa as mesas de concreto e as raízes pra quebrar a linha de visão."*
2. **Descida ao Pátio Central (`patio_central`):**
   - Gabriel desce as escadas. No pátio aberto (1280 px de largura), andar desprotegido sob os feixes de luar atrai a visão das Sentinelas a distâncias maiores.
   - O jogador aplica a mecânica de furtividade em descampado: agachar atrás das mesas de concreto tombadas e contornar as raízes para evitar os cones de luz dos robôs.
3. **Inspeção da Rampa (`rampa_subsolo`):**
   - Gabriel chega à rampa e tenta abrir a comporta. O painel informa: *"Cancela bloqueada. Relé de comutação sem alimentação primária."*
4. **Localização da Sala Segura (`posto_manutencao`):**
   - Pelo anexo sul (atravessando a antiga Gráfica), Gabriel encontra o Posto de Manutenção Predial e fecha a porta de aço por dentro.
   - Encontra o ponto de descanso e salvamento (checkpoint).
   - No quadro de avisos, uma **Ordem de Manutenção Técnica de 3026** indica: *"Célula de energia reserva realocada para o gerador de emergência da câmara frigorífica da cantina (Setor Norte)."*
5. **Travessia até a Cantina e Infiltração (`cantina` e `deposito_cantina`):**
   - Gabriel cruza o pátio em direção à ala norte.
   - Diante da cantina, um **Rastreador** patrulha. O piso diante do balcão está coberto de cerâmica estilhaçada e cacos de vidro (piso tático de alto ruído com Fator `2.0`, amplificando o som dos passos).
   - Gabriel deve andar devagar pelas passadeiras de borracha ou arremessar uma **pedra** (ou uma **lata de refrigerante**) para afastar o Rastreador.
   - No `deposito_cantina`, Gabriel recolhe a **Célula de Energia de Alta Densidade** e uma **pilha**.
6. **O Puzzle da Gráfica (`grafica_rapida`):**
   - Gabriel retorna à gráfica e insere a Célula de Energia no Quadro de Comutação.
   - O painel abre a interface do **Puzzle de Coloração de Grafos**: 4 nós de circuitos interconectados precisam ter suas frequências de fase reguladas (Azul, Amarelo, Vermelho) sem que dois setores vizinhos compartilhem a mesma frequência, prevenindo sobrecarga harmônica na rede.
   - Ao solucionar o grafo, a chave geral arma e direciona carga elétrica para a comporta da rampa.
7. **A Virada no Pátio (Holofotes de Vigilância Ativados):**
   - Com o circuito armado, os **holofotes perimetrais** do pátio acendem e iniciam varreduras lentas em arcos giratórios.
   - A Clarice avisa no rádio (com o que Henrique reporta das câmeras): *"Gabriel, a energia voltou, mas ligou os refletores do pátio! O padrão das Sentinelas mudou, fica nas sombras!"*
   - O retorno exige sincronizar o avanço entre as sombras das mesas e os intervalos de passagem dos feixes dos holofotes.
8. **Abertura da Rampa e Saída (`rampa_subsolo`):**
   - Na rampa, o painel agora exibe luz verde estável. Gabriel aciona o mecanismo da comporta.
   - A comporta pesada sobe, revelando a descida protegida que leva ao **Bunker**.
   - Fim da fase e transição de nível.

### 3.4 Grafo de Dependências

```
Passarela → Pátio → Checar Rampa (bloqueada) → Sala Segura (ordem de manutenção)
   → Travessia à Cantina (cacos de vidro) → Coletar Célula de Energia
   → Puzzle de Coloração na Gráfica → Energização do Circuito (holofotes ativos / nova ronda)
   → Comporta da Rampa liberada → Entrada do Bunker
```

### 3.5 Tabela de Itens e Recursos

| Item | Local | Tipo | Utilidade |
|---|---|---|---|
| **Célula de Energia** | `deposito_cantina` | Item-chave | Alimenta o painel de comutação da Gráfica |
| **Pilhas de Lanterna (3)** | `passarela_acesso`, `deposito_cantina`, `posto_manutencao` | Consumível | Manter a lanterna carregada |
| **Cápsula de Clarão (1)** | `posto_manutencao` | Gadget | Defesa emergencial contra Sentinelas |
| **Pedras (3)** | `patio_central` (junto ao canteiro de entulho) | Gadget | Distrair o Rastreador nos cacos da Cantina |
| **Panfleto Universitário (2024)** | `grafica_rapida` | Registro | Documento de lore sobre a vida estudantil antes do colapso |
| **Ordem de Manutenção (3026)** | `posto_manutencao` | Registro | Pista técnica indicando a localização da Célula de Energia |

---

## 4. Robôs e Ameaças

| Robô | Onde | Sentido Forte | O que o Jogador Aprende |
|---|---|---|---|
| **Sentinelas (2 unidades)** | `patio_central` | Visão ampla (cone de 60°) sob o luar | Usar mesas de concreto e raízes como barreiras visuais em espaço aberto; esperar o cone passar |
| **Rastreador** | Área externa de `cantina` | Audição apurada | Evitar pisos com cacos de vidro/louça (Fator `2.0`); usar passadeiras ou distrações arremessáveis |
| **Holofotes Perimetrais** | `patio_central` (após ligar energia) | Iluminação dinâmica ambiental | Cronometrar avanço entre feixes móveis de luz |

- **Rotinas e Cadeia de Markov:** No Pátio Central (1280 px), as Sentinelas não realizam patrulhas em linha reta previsíveis. Cada robô utiliza um grafo de nós de vigilância (bancos, canteiros, postes) e seleciona o próximo destino com base em probabilidades de transição estocásticas (**Cadeia de Markov**), conferindo tensão e comportamento dinâmico à travessia em campo aberto.

---

## 5. Puzzles e Requisitos de Computação Gráfica

### 5.1 Puzzle de Coloração de Grafos (Quadro de Comutação da Gráfica)
- **Problema:** O comutador possui 4 polos de distribuição de carga que formam um grafo com arestas de interferência mútua (Topologia em anel com aresta diagonal: Setores Norte, Leste, Sul, Oeste).
- **Regra:** Cada setor precisa de um seletor de frequência ($f_1, f_2, f_3$, representados visualmente pelas cores Azul, Amarelo, Vermelho). Dois setores adjacentes não podem ter a mesma frequência para evitar ressonância harmônica na rede de alta tensão.
- **Número Cromático:** O grafo exige exatamente 3 frequências (número cromático $\chi(G) = 3$). O jogador resolve o minigame ajustando os seletores até que nenhuma aresta conectada apresente conflito.
- **Aplicação acadêmica:** Aplicação prática do algoritmo de Coloração de Vértices ($k$-Coloring) em mecânica de puzzle interativo.

### 5.2 Propagação Acústica (BFS em Área Aberta vs Espaço Confinado)
- No pátio aberto, o som dissipa em raio radial, com árvores e raízes atuando como obstáculos que quebram a grade de navegação.
- Diante da cantina, pisar em cacos de louça e vidro ativa um multiplicador de ruído de piso (Fator `2.0`), acionando a busca em largura (**BFS**) com o dobro do alcance normal, alertando o Rastreador do lado de fora.

### 5.3 Cone de Visão e Produto Escalar em Descampado
- Em área aberta com luar, o raio de detecção visual $R$ das Sentinelas é ampliado nas faixas iluminadas, validando a fórmula de produto escalar:
  $$\frac{(\vec{p}_{\text{gabriel}} - \vec{p}_{\text{robô}}) \cdot \vec{d}}{\lVert \vec{p}_{\text{gabriel}} - \vec{p}_{\text{robô}} \rVert} \ge \cos\left(\frac{\theta}{2}\right)$$
- As mesas de concreto tombadas e raízes grossas bloqueiam o raio `LinhaLivre`, recompensando o uso estratégico de cobertura baixa.

---

## 6. Sala Segura e Sonho

- **Local:** `posto_manutencao` (Posto de Manutenção Predial, anexo à Gráfica).
- **Por que é segura:** Sala de alvenaria reforçada com porta de serviço trancável por ferrolho interno. Robôs não entram nem possuem nós de navegação nela.
- **Ambiente:** Um sofá rasgado, mesa de apoio com lampião fraco, rádio de mesa e terminal de diagnóstico offline.
- **Evento do Sono:** Gabriel descansa no sofá. O sonho evoca o Centro de Convivência vivo em 2026: risos, sol da tarde, fila da cantina e o murmúrio dos universitários. Gabriel acorda no silêncio escuro de 3026 com estalos metálicos ao fundo.

---

## 7. Registros e Comunicações

- **Clarice no rádio:**
  - Chegada na passarela: instrução sobre o descampado aberto e os cones das Sentinelas sob o luar.
  - Alerta pós-energização: aviso sobre a ativação dos holofotes móveis e a alteração da rota dos robôs.
- **Documento 1 — Panfleto da Semana Universitária (2024):** Encontrado na Gráfica. Traz a programação cultural do campus vivo, acentuando o contraste temporal.
- **Documento 2 — Ordem de Manutenção Técnica (3026):** Encontrado na Sala Segura. Dá a pista sobre a Célula de Energia na câmara frigorífica da cantina e menciona evacuação de emergência do pessoal para as instalações subterrâneas (Bunker).

---

## 8. Novas Sugestões de Itens Táticos

Sugestões para expandir as opções de sobrevivência do jogador mantendo o equilíbrio de *survival horror*:

### 1. Lata de Refrigerante Antiga (Consumível de Arremesso)
- **Categoria:** Gadget / Arremessável.
- **Descrição:** Uma lata de alumínio enferrujada do século XX.
- **Mecânica:** Ao colidir com o chão, rola produzindo barulho metálico contínuo. Atrai o **Rastreador** por 15 segundos (50% a mais que a pedra comum).
- **Limite no Inventário:** Máximo 2 unidades.

### 2. Fusível Industrial de 20A (Item Técnico de Controle de Luz)
- **Categoria:** Item Técnico / Consumível.
- **Descrição:** Um fusível cerâmico de alta amperagem encontrado em painéis de manutenção predial.
- **Mecânica:** Pode ser inserido em quadros de distribuição específicos para **desativar a iluminação de um setor**.
- **Uso Tático:** Ao apagar as lâmpadas e holofotes de uma área, cega parcialmente a visão da **Sentinela** (reduzindo seu alcance de visão para o valor base sem luz), embora force Gabriel a avançar na penumbra ou ligar a lanterna.

### 3. Crachá de Acesso da Unifor (Item de Atalho)
- **Categoria:** Item-Chave.
- **Descrição:** Cartão magnético de funcionário da segurança patrimonial de 2026.
- **Mecânica:** Destranca catracas eletrônicas e portas de serviço laterais com dobradiças amortecidas, permitindo contornar setores com pisos ruidosos sem chamar a atenção dos robôs.

---

## 9. Estrutura Técnica no Godot

| Recurso | Caminho Previsto | Descrição |
|---|---|---|
| **Cenas das Salas** | `cenas/salas/centro_de_convivencia/` | 7 cenas (`passarela_acesso.tscn`, `patio_central.tscn`, `cantina.tscn`, `deposito_cantina.tscn`, `grafica_rapida.tscn`, `posto_manutencao.tscn`, `rampa_subsolo.tscn`) herdando `modelo_sala.tscn` |
| **Fase no Menu** | `dados/fases/04_convivencia.tres` | `nome = "Convivência"`, apontando para a cena inicial |
| **Kit de Cenário Novo** | `cenas/cenario/convivencia/` | Mesas redondas de concreto, raízes trepadeiras, balcões de cantina, holofotes rotativos, cancela da rampa |
| **Gerador de Assets** | `assets/modelagem/cenario/gerar_convivencia.py` | Script em Python para geração procedural dos blocos e texturas da fase |
| **Puzzle de Coloração** | `cenas/sistemas/painel_comutacao.tscn` | Interface de minigame de alinhamento de fases elétricas (coloração de grafos) |
