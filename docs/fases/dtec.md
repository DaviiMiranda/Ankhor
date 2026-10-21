# Fase — Laboratório (D-Tec)

> **Status:** Mapa pronto (cenário, portas, luzes e itens). Sexta fase do jogo, depois do Bunker. Level design novo, com o confronto final com o Carlos, aprovado e ainda não implementado (seção 3.1).  
> **Área:** o D-Tec, departamento de tecnologia: laboratórios, servidores e o salão da Âncora (a máquina central)  
> **No menu Fases:** **Laboratório** (`dados/fases/09_dtec.tres`, começa na recepção)

---

## 1. Visão Geral da Área

- **O que é:** a **6ª fase**, logo depois do Bunker (acessada pela comporta no fim do Corredor B do Bunker).
- **A máquina:** no salão do meio (Lab Central) há uma **máquina grande e brilhante**: um anel enorme em pé, duas torres com bobinas de cobre e, no centro do anel, um núcleo ciano que pulsa e solta faíscas. A máquina é **animada** (seção 4): o núcleo bate, a onda de choque sai dele até o anel, os raios saltam, a trilha de luz do anel gira com um cometa, a energia sobe pelas bobinas e as luzes das torres piscam, num laço de 2,4 s. **Ela é a Âncora** (decisão de 2026-10-17): o aparelho de física do tempo que o Carlos criou, descrito na seção 3 do [Enredo Principal](../historia/História_Completa.md). O que a Âncora faz nesta fase (consertá-la, o final) ainda não está decidido: ver as pendências 10.2 e 10.6 do Enredo.
- **Visual:** laboratório lacrado, mais inteiro que a Biblioteca, mas com mil anos de poeira. Azulejo branco embaixo e painel cinza em cima, com a faixa azul do DTEC entre os dois; duto de ventilação no teto; janelas de laboratório, quadros brancos (um deles com um grafo), painéis e terminais. Rachaduras com mato entrando e uma planta de escritório que tomou o canto.
- **Luz:** fluorescentes frias que piscam. No Lab Central, a luz ciano da máquina pulsa devagar (`LuzPulsante`), e ela vaza pelas portas do salão nos dois corredores.
- **Som:** o zumbido do prédio em todas as salas e, perto da máquina, um ronco grave (o mesmo zumbido do bunker, com o tom mais baixo).

---

## 2. Topologia e Salas (Nós do Grafo)

Cada ligação é uma `Porta` (`cenas/sistemas/porta.tscn`). O Lab Central fica **no meio do mapa**: os dois corredores chegam nele pela porta do centro.

```
                RECEPÇÃO ── (saída: lacrada)
                   │
 CORREDOR NORTE ── SALA SEGURA (DESCANSO)
                ── eletrônica
                ── informática (o notebook está aqui)
                ── LAB CENTRAL (a Âncora)  ──┐
                ── SERVIDORES (trancada)     │
                ── depósito (lacrada)        │
                ── diretoria (lacrada)       │
                                             │
 CORREDOR SUL  ── LAB CENTRAL ───────────────┘
                ── química
                ── ROBÓTICA (trancada)
                ── controle
                ── emergência (lacrada)
                ── arquivo (lacrada)
```

| Cena (`cenas/salas/dtec/`) | Tamanho | O que tem | Itens |
|---|---|---|---|
| `recepcao` | 640 × 400 | Letreiro DTEC, balcão da recepção, catracas, mesa, plantas, a saída lacrada | lanterna, 1 pilha |
| `corredor_norte` | 2400 × 180 | Seis portas com placa, janelas dos laboratórios, quadro, mural, extintores, painel e a porta larga do Lab Central com a faixa de perigo | 1 pilha, 1 cápsula de clarão |
| `lab_central` | 960 × 560 | **A Âncora (a máquina)** no centro, consoles dos dois lados, racks, cilindros de gás, telões e janelas | 1 cápsula de clarão |
| `corredor_sul` | 2400 × 180 | O outro lado: seis portas, telão, terminal e a porta larga do Lab Central | 1 pilha, 2 pedras |
| `sala_segura` | 320 × 180 | A **sala segura** do modelo (os óculos do Zane para salvar, o piano), com luz mais fria. A porta é a DESCANSO no corredor norte, entre a Recepção e a Eletrônica, com a **luz verde** em cima ([`../mecanicas/sala_segura.md`](../mecanicas/sala_segura.md)) | — |
| `lab_eletronica` | 480 × 560 | Três bancadas de eletrônica (osciloscópio, solda, placas), armário, cilindros | 1 pilha, 1 cápsula de clarão |
| `lab_informatica` | 560 × 560 | Nove mesas com computador em três fileiras, rack, quadro | **notebook**, 1 pilha |
| `sala_servidores` | 480 × 480 | Piso elevado e duas fileiras de racks com corredores entre eles, luz verde | 2 pilhas, 1 cápsula de clarão |
| `lab_quimica` | 400 × 480 | Duas capelas de exaustão, bancadas, armários de reagentes, linhas de gás | 1 pilha |
| `lab_robotica` | 560 × 560 | Braços robóticos, dois robôs desmontados nas mesas de manutenção, bancada | 2 cápsulas de clarão, 1 pilha |
| `sala_controle` | 560 × 480 | Telões com o gráfico da Âncora, três consoles, mesas, janela | 1 pilha |

### Salas trancadas e lacradas

- **Trancadas** (`Porta.trancada`): **Servidores** e **Robótica**. O leitor de cartão da porta está com o LED vermelho. Abrem com o **notebook** (hack), que fica no Laboratório de Informática. São as salas com mais itens.
- **Lacradas** (`Porta.bloqueada`): saída da recepção, depósito, diretoria, emergência e arquivo. Fita amarela e preta em X e placa de acesso restrito. Só mostram o aviso. Quando uma delas virar sala, basta tirar o `bloqueada`, preencher `cena_destino` e `porta_destino` e trocar a peça da parede por `dtec_porta`.

---

## 3. Objetivos e Progressão

- **Hoje:** explorar, pegar o notebook na Informática, hackear as duas salas trancadas e chegar à Âncora.
- **Próximo passo:** o level design novo da seção 3.1 ("A Última Tentativa"), com o confronto final com o Carlos. Ainda não foi implementado.

### 3.1 Level design novo: "A Última Tentativa"

> **Status:** proposta aprovada em 2026-10-21 (ver `docs/decisoes.md`), ainda não implementada. É design de fase, não história: tudo o que depende das pendências do [Enredo Principal](../historia/História_Completa.md) está marcado como **espaço vazio** e não deve ser preenchido sem decisão do grupo.

#### Problemas da versão atual

1. **Sem ameaça:** nenhum robô, esconderijo, checkpoint, documento ou música. As 6 cápsulas de clarão não têm uso.
2. **O objetivo acaba em 30 segundos:** a porta do Lab Central está aberta no corredor norte. As salas trancadas só guardam itens.
3. **A chegada não faz sentido:** o Gabriel vem da comporta do núcleo do bunker (no subsolo) e aparece na recepção, cuja saída está "travada por fora".
4. **O mapa é um pente:** dois corredores de 2400 px com salas sem saída, ligados só pelo Lab Central. O jogador atravessa a sala do clímax no meio da exploração. As portas lacradas são escolhas falsas.
5. **O Carlos não aparece na casa dele:** nenhuma relíquia dos anos 80 (a Biblioteca tem). A Sala de Controle, com os telões da Âncora, guarda só uma pilha.
6. **Itens repetidos:** o notebook (do Zane, desde o Labirinto) e a lanterna (da Biblioteca) aparecem de novo. Só servem para quem começa a fase pelo menu.
7. **Nenhum conteúdo de computação**, que a disciplina exige.

#### A ideia

O Carlos está preparando a **próxima tentativa** (cada uma puxa alguém novo e faz a fenda crescer: Enredo, seção 3). Ele **nunca sai do laboratório** (ficha dele), então luta pelo prédio: os robôs, as portas, as luzes e a **lupa vermelha**. O Gabriel **nunca encosta nele**: o confronto é um duelo de percepção (o Carlos vigia, o Gabriel se esconde e sabota), porque o Enredo diz que o grupo o enfrenta sem lutar. O ex-Faroleiro usa um farol para caçar, não para guiar: o vermelho dele por cima da luz é o mesmo símbolo da traição (Enredo, seção 2.4).

#### Mapa novo (com as salas que já existem)

```
              QUARTO DO CARLOS* (ex-diretoria: quarto anos 80)
                     │
 recepção ── CORREDOR NORTE ── eletrônica [RELÉ] · informática · servidores [RELÉ, trancada]
                     │                          ║ grade
                     │                    LAB CENTRAL (arena)
                     │                          ║ grade
 CORREDOR DE SERVIÇO* (ex-depósito + ex-arquivo: fecha o anel)
                     │
 EMERGÊNCIA* ── CORREDOR SUL ── química · robótica [RELÉ, trancada] · CONTROLE (telão do grafo)
 (chegada: escada que sobe do bunker)

 * sala nova, no lugar de uma porta lacrada
```

- **Chegada pela Emergência:** a escada sobe da comporta do núcleo do bunker. A recepção fica como sala opcional.
- **Sala segura:** a regra de 2026-10-21 põe a sala segura perto de onde o Gabriel chega, então a porta DESCANSO passa do corredor norte para o corredor sul, perto da Emergência.
- **O Lab Central começa fechado**, com uma grade (`GradeSeguranca`) nas duas portas. A luz ciano vaza para os corredores, mas o clímax fica guardado para o fim.
- **O corredor de serviço** liga as pontas dos dois corredores e fecha um **ciclo** no grafo das salas: dá para despistar um robô dando a volta (o A\* ganha caminho alternativo).
- **Os corredores mantêm o tamanho** e ganham nichos (`NichoEsconderijo`) a cada ~400 px, uma **Sentinela** no norte e um **Rastreador** no sul.
- **Itens repetidos:** o notebook e a lanterna só aparecem quando a fase começa pelo menu (o item único que o Gabriel já tem não aparece de novo no chão).

#### Parte 1: Infiltração

O Gabriel chega pela Emergência (checkpoint). Na **Sala de Controle**, o telão mostra a **rede de energia da Âncora como um grafo**: geradores no subsolo, seis relés nas salas e a Âncora no centro.

#### Parte 2: Cortar a rede (o puzzle do grafo)

- Cada relé é um `NoHackeavel` (sem gasto de bateria). Cortar um relé faz o Carlos **redistribuir a energia pelo caminho mais curto (Dijkstra)**. O telão mostra o caminho novo, e um robô muda de rota para vigiar o próximo relé desse caminho.
- **Sem código novo no robô:** `robo.gd` já troca de rota por marca (`rota_com_marca` e `marca_da_rota`). Cada corte só grava uma marca.
- **O corte mínimo são 3 relés:** Eletrônica, Servidores e Robótica. Cortar um relé errado gasta tempo e faz barulho, e o barulho chama os robôs (BFS do som). O puzzle é ler o grafo e achar o gargalo. Duas das salas do corte são as trancadas: o hack ganha função.
- **Na Robótica,** cortar o relé faz o Carlos religar os dois robôs desmontados das mesas de manutenção.
- **Cada corte** apaga as luzes de um trecho, desacelera o pulso da Âncora (`periodo` do `LuzPulsante` e a animação juntos) e dispara uma fala do Carlos pelos alto-falantes (**espaço vazio**: como ele fala está pendente).
- **Com os 3 cortes,** a trava magnética do Lab Central fica sem energia e a grade abre sozinha. Checkpoint na porta.

#### Parte 3: A arena (o confronto com o Carlos)

O Carlos fica no console do fundo do Lab Central, com a Âncora entre ele e o Gabriel. Racks, cilindros e consoles servem de cobertura. A **lupa varre a sala como um holofote**: cone de visão por produto escalar, com oclusão por raycast. Ser visto não mata: o Carlos chama os robôs pelas portas, e quem pega o Gabriel são os robôs.

| Fase | O que o Carlos faz | O que o Gabriel faz |
|---|---|---|
| A | Varredura lenta, um robô na arena | Invade o console 1 |
| B | Fecha uma das portas (`GradeSeguranca`); a Âncora solta a **onda de choque a cada 2,4 s** (o ritmo da animação), que revela quem não está atrás de cobertura | Invade o console 2 |
| C | Varredura rápida, os robôs da Robótica entram | Lança a **cápsula de clarão na lupa** (sensor óptico: fica atordoada como os olhos dos robôs) e avança até o núcleo entre uma onda e outra |

- Cada console invadido é um checkpoint.
- **O fim:** a interação no núcleo leva a uma cena final que é **espaço vazio**: o que acontece com o Carlos e com a Âncora está nas pendências 10.2 e 10.6 do Enredo.

#### Computação (para a apresentação)

| Onde aparece | Conteúdo |
|---|---|
| Redistribuição da energia | Dijkstra num grafo com pesos |
| Os 3 relés certos | Corte mínimo de vértices (teorema de Menger, fluxo máximo e corte mínimo) |
| Lupa do Carlos | Cone de visão por produto escalar e raycast |
| IA do Carlos | Máquina de estados: observando, varrendo, alerta, pulso, atordoado |
| Onda da Âncora | Função periódica r(t) = v · (t mod 2,4) e oclusão |
| Barulho dos cortes | BFS do som (já existe) |
| Fuga pelo anel | A\* com caminho alternativo no ciclo do mapa (já existe) |

#### O que reaproveita e o que é novo

- **Reaproveita:** `Porta` com hack, `NoHackeavel`, `robo.gd` (troca de rota por marca), `GradeSeguranca`, `Sirene`, `NichoEsconderijo`, `Checkpoint`, `LuzPulsante`, cápsula de clarão, `gatilho_transmissao` e `SaidaFase`.
- **Novo:** `rede_energia_dtec.gd` (o grafo, o Dijkstra e o telão), `carlos_chefe.gd` (a máquina de estados e a lupa), `onda_ancora.gd`; as salas `emergencia`, `corredor_servico` e `quarto_carlos`.
- **Cuidado:** o `montar_dtec.py` sobrescreve as salas. As mudanças de mapa entram na descrição das salas dele.

#### Ordem de produção (o menor passo primeiro)

1. **Mapa:** chegada pela Emergência, sala segura no corredor sul, corredor de serviço, grade no Lab Central, nichos, os dois robôs e os checkpoints. Só isso já deixa a fase tensa.
2. **A rede:** o telão do grafo, os relés e a troca de rota dos robôs.
3. **A arena do Carlos.**
4. **O quarto e os registros do Carlos**, que dependem de pendências.

#### O que depende de decisão do grupo

- **Enredo 10.2, como enfrentar o Carlos sem lutar:** esta seção é uma resposta possível do ponto de vista da mecânica. Só entra no Enredo se o grupo aprovar.
- **Como o Carlos fala** (as falas dos alto-falantes) e **o que há no quarto e nos registros dele** (ficha, seções 2 e 5).
- **Quem guia pelo rádio e se os outros estão presentes:** a proposta supõe o Zane, como no Labirinto e no Centro de Convivência (Enredo 3.1 e 10.6).
- **Robôs capturam ou eliminam** (Enredo 10.2): se capturam, ser pego na arena pode virar uma cena em vez de game over.
- **O que acontece com o Carlos e com a Âncora no fim** (Enredo 10.6).

---

## 4. Onde está no projeto

| O quê | Onde |
|---|---|
| Cenas das salas | `cenas/salas/dtec/` |
| Kit do DTEC (paredes, chão, objetos) | `cenas/cenario/dtec/`, sprites em `assets/sprites/cenario/dtec/` |
| Gerador do kit (a arte) | `assets/modelagem/cenario/gerar_dtec.py` |
| Montagem das cenas (kit e salas) | `assets/modelagem/salas/dtec/montar_dtec.py` |
| Luz da máquina (pulsa devagar) | `cenas/cenario/luzes/luz_maquina.tscn`, script `scripts/cenario/luz_pulsante.gd` |
| Animação da máquina | `cenas/cenario/dtec/objetos/maquina.tscn` (nó `Animacao`, um `AnimatedSprite2D` que toca `ativa` sozinho), `assets/sprites/cenario/dtec/objetos/maquina_folha.png` (24 quadros de 176 × 156) e `maquina_quadros.tres` (SpriteFrames, 10 quadros por segundo). Gerada por `gravar_animacao_maquina()` em `gerar_dtec.py`; a matemática está no comentário "A ANIMAÇÃO DA MÁQUINA" no começo dele |
| Fase no menu | `dados/fases/09_dtec.tres` |

**Como refazer:** `python assets/modelagem/cenario/gerar_dtec.py` redesenha as peças; `python assets/modelagem/salas/dtec/montar_dtec.py` remonta as cenas. **Cuidado:** o segundo sobrescreve as salas. Se alguém ajustar uma sala no editor do Godot, passe o ajuste para a descrição da sala no fim do `montar_dtec.py` antes de rodar de novo.

### Peças do kit do DTEC

- **Paredes (80 × 112):** `dtec_lisa`, `dtec_rachada` (com mato), `dtec_luminaria` (fluorescente: `luz_tubo` em x + 40, y 34), `dtec_porta` (aberta, LED verde), `dtec_porta_trancada` (LED vermelho), `dtec_porta_lacrada`, `dtec_porta_central` (a entrada larga do salão, com a luz ciano), `dtec_vidro`, `dtec_quadro`, `dtec_painel`, `dtec_armario`, `dtec_cartaz`, `dtec_terminal`, `dtec_extintor`, `dtec_canos`, `dtec_tela_grande`, e o `pilar_dtec` (16 px) para as pontas.
- **Chão (128 × 68):** `chao_dtec`, `chao_dtec_cabos`, `chao_dtec_elevado` (piso de servidor), `chao_dtec_faixa`.
- **Salas fundas:** como no bunker, `chao_dtec_fundo`, `chao_dtec_elevado_fundo`, `chao_dtec_cabos_fundo`, `chao_dtec_faixa_fundo` (128 × 64) e `dtec_lateral` (16 × 64).
- **Objetos:** `bancada_lab`, `bancada_eletronica`, `mesa_computador`, `cadeira_escritorio`, `rack_dtec`, `armario_quimico`, `capela`, `cilindros`, `braco_robotico`, `robo_desmontado`, `console`, `planta`, `balcao_recepcao`, `catraca`, `caixas_lab` e a `maquina` (176 × 156, animada em laço de 2,4 s, com as faíscas; o `maquina.png` parado continua sendo gerado, mas a cena usa a folha de quadros). O laço tem o mesmo período da luz da máquina (`periodo = 2.4` do `LuzPulsante`) e a mesma fase, então o núcleo e a luz pulsam juntos; se mudar um, mude o outro.
- **Placas das portas:** `Label` dentro de `Paredes` (fundo azul do DTEC, letra clara), em cima da plaquinha que as peças de porta trazem.
