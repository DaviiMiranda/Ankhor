# Fase — Centro de Convivência

> **Status:** Jogável (7 salas, puzzle de Coloração de Grafos, Célula de Energia, holofotes e transmissões do Zane pelo rádio)  
> **Área:** o Centro de Convivência da Unifor, em 3026  
> **Ordem na história:** **quarta fase**, depois do Labirinto ([`labirinto.md`](labirinto.md)) e antes do Bunker ([`bunker.md`](bunker.md)).  
> **Como se chega:** Pelo duto do alçapão da oficina do Zane no fim do Labirinto, saindo em `passarela_acesso`.  
> **Saída:** Comporta da Rampa do Subsolo (`rampa_subsolo`), que desce para a entrada do Bunker.  
> **No menu Fases:** Cadastrado em `dados/fases/04_convivencia.tres` ("Convivência").

---

## 1. Visão Geral da Área

- **Nome do Local:** Centro de Convivência da Unifor, ano de 3026.
- **Ambientação Visual:**
  - **É noite** sob céu escuro com estrelas (`ceu_noite.png`).
  - O Centro de Convivência é um grande espaço arquitetônico semi-aberto. A cobertura desabou em vários pontos, deixando o luar azulado iluminar o pátio.
  - O chão mistura lajotas rachadas, faixas de areia fina e mato crescendo pelas frestas.
  - Árvores cresceram furando o piso; raízes e musgo cobrem as mesas redondas de concreto e os bancos fixos.
  - A antiga **cantina** (com balcões de aço inoxidável manchados e cacos de louça e vidro no chão) e a **gráfica rápida** permanecem como relíquias do cotidiano universitário.
  - **Tecnologia de 3026:** painéis ciano, torres de equipamentos e **holofotes perimetrais** que acendem quando o circuito de alta tensão é armado.
- **Comunicação:**
  - Não há nenhum personagem em pessoa nesta fase. Todo o contato e orientação vêm do **Zane pelo rádio** (`zane_convivencia_01` e `zane_convivencia_02`).

---

## 2. Topologia e Salas (Nós do Grafo)

### 2.1 Mapa do Grafo

```
                     [PASSARELA DE ACESSO] (vem do Labirinto)
                              │
                              ▼ (escada)
    [CANTINA] ◄─────────► [PÁTIO CENTRAL] ◄─────────► [GRÁFICA RÁPIDA]
        │                 (Amplo, Sentinelas)                │
        ▼                         │                          ▼
[DEPÓSITO / CÂMARA]               ▼                [POSTO DE MANUTENÇÃO]
(Célula de Energia)      [RAMPA DO SUBSOLO]            (Sala Segura)
                                  │
                                  ▼
                           (para o Bunker)
```

### 2.2 Tabela de Salas

| ID da Cena (`cenas/salas/centro_de_convivencia/`) | Nome / Função | Dimensões | Tipo de Piso | Conexões | Esconderijos | Ameaça |
|---|---|---|---|---|---|---|
| `passarela_acesso` | Passarela Superior | 640 × 180 px | Lajota | Escada para `patio_central` | Nicho do bebedouro | Nenhuma (chegada, checkpoint e rádio do Zane) |
| `patio_central` | Pátio das Mesas e Raízes | 1280 × 360 px | Lajota, mato e areia | `passarela_acesso`, `cantina`, `grafica_rapida`, `rampa_subsolo` | Mesas de concreto, árvores, nichos | 2 **Sentinelas** (rotas cruzadas sob o luar e holofotes) |
| `cantina` | Quiosque da Cantina / Balcões | 640 × 260 px | Lajota, tapete e cacos de vidro | `patio_central`, `deposito_cantina` | Nicho do armário, balcões | 1 **Rastreador** |
| `deposito_cantina` | Depósito e Câmara Frigorífica | 400 × 240 px | Lajota | `cantina` | Estantes de metal | Nenhuma |
| `grafica_rapida` | Anexo da Gráfica e Serviços | 480 × 260 px | Lajota | `patio_central`, `posto_manutencao` | Bancadas | Nenhuma |
| `posto_manutencao` | Posto de Manutenção Predial | 400 × 240 px | Tapete | `grafica_rapida` | **Sala Segura** (checkpoint) | Nenhuma |
| `rampa_subsolo` | Pátio de Carga e Rampa Técnica | 640 × 360 px | Lajota e areia | `patio_central`, comporta para o Bunker (`fim_da_convivencia`) | Nicho do armário, caixas e mesa | 1 **Sentinela** |

---

## 3. Objetivos e Progressão

### 3.1 Objetivo Principal
Atravessar o pátio do Centro de Convivência, localizar a **Célula de Energia** na câmara da Cantina, resolver o **Puzzle de Coloração de Grafos** no comutador da Gráfica Rápida e destrancar a comporta da **Rampa do Subsolo** para entrar no **Bunker**.

### 3.2 Passo a Passo

1. **Chegada e Contato do Zane (`passarela_acesso`):**
   - Gabriel sai pelo duto na passarela superior. O **Zane** chama pelo rádio (`zane_convivencia_01`), alertando sobre as duas Sentinelas no pátio aberto iluminado pelo luar e orientando a procurar o Posto de Manutenção passando pela Gráfica.
2. **Travessia do Pátio Central (`patio_central`):**
   - Gabriel desce para o pátio (1280 × 360 px) e usa as mesas redondas de concreto, as árvores e os nichos para evitar os cones de visão das duas Sentinelas. No pátio há 3 pedras para distração.
3. **Sala Segura e Pista da Célula (`grafica_rapida` e `posto_manutencao`):**
   - Na Gráfica Rápida está o **Quadro de Comutação Trifásico** (`PainelComutacao`), sem carga primária, e o documento **Panfleto da Semana Universitária (2024)**.
   - Ao lado fica o **Posto de Manutenção** (Sala Segura com checkpoint, 1 pilha e 1 cápsula de clarão), onde a **Ordem de Manutenção Técnica (3026)** informa que a Célula de Energia reserva foi levada para o gerador da câmara frigorífica da Cantina.
4. **Infiltração na Cantina (`cantina` e `deposito_cantina`):**
   - Na Cantina, um **Rastreador** patrulha perto de uma faixa central de **cacos de louça e vidro** (`ZonaDePiso` com `fator_ruido = 2.0`).
   - O jogador contorna pelas passadeiras laterais (`fator_ruido = 0.6`) ou distrai o Rastreador com pedras para entrar em `deposito_cantina` e pegar a **Célula de Energia** (`celula_energia.tres`) e 1 pilha.
5. **Puzzle de Coloração de Grafos (`grafica_rapida`):**
   - De volta à Gráfica, Gabriel usa a Célula de Energia no comutador e resolve o **Puzzle de Coloração de Grafos**: 4 setores (Norte, Leste, Sul, Oeste) em anel com diagonal Norte-Sul (5 arestas: N-L, L-S, S-O, O-N, N-S) precisam receber uma das 3 fases (Fase A azul, Fase B amarela, Fase C vermelha) sem que setores vizinhos compartilhem a mesma fase ($\chi(G) = 3$).
   - Ao sincronizar as fases, a marca `convivencia_energia` é ativada.
6. **Holofotes Acesos e Saída pela Rampa (`patio_central` e `rampa_subsolo`):**
   - Com `convivencia_energia`, os **holofotes perimetrais** acendem no pátio e na rampa (`revela_quem_passa = true`), e as Sentinelas mudam de rota.
   - O **Zane** avisa pelo rádio (`zane_convivencia_02`) que a comporta da rampa destravou, mas os holofotes ligaram.
   - Em `rampa_subsolo`, a comporta de aço (`ComportaRampa`) se recolhe e a porta leva a `fim_da_convivencia.tscn`, abrindo a entrada do **Bunker**.

---

## 4. Itens, Documentos e Transmissões

| Recurso | Arquivo | Onde fica |
|---|---|---|
| **Célula de Energia** | `dados/itens/celula_energia.tres` | `deposito_cantina` |
| **Pilhas (3)** | `cenas/itens/pilha_no_chao.tscn` | `passarela_acesso`, `deposito_cantina`, `posto_manutencao` |
| **Cápsula de Clarão (1)** | `dados/itens/clarao.tres` | `posto_manutencao` |
| **Pedras (3)** | `dados/itens/pedra.tres` | `patio_central` |
| **Panfleto Universitário (2024)** | `dados/documentos/panfleto_universitario.tres` | `grafica_rapida` |
| **Ordem de Manutenção (3026)** | `dados/documentos/ordem_manutencao_convivencia.tres` | `posto_manutencao` |
| **Zane no rádio (chegada)** | `dados/transmissoes/zane_convivencia_01.tres` | `passarela_acesso` |
| **Zane no rádio (holofotes)** | `dados/transmissoes/zane_convivencia_02.tres` | `patio_central` (requer `convivencia_energia`) |

---

## 5. Onde está no projeto

| O quê | Onde |
|---|---|
| Cenas das salas | `cenas/salas/centro_de_convivencia/` |
| Kit da Convivência | `cenas/cenario/convivencia/`, sprites em `assets/sprites/cenario/convivencia/` |
| Gerador de sprites | `assets/modelagem/cenario/gerar_convivencia.py` |
| Montador das cenas | `assets/modelagem/salas/centro_de_convivencia/montar_convivencia.py` |
| Puzzle de Coloração de Grafos | `cenas/sistemas/painel_comutacao.tscn`, script `scripts/sistemas/painel_comutacao.gd` |
| Fase no menu | `dados/fases/04_convivencia.tres` |
