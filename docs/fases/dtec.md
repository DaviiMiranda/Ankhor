# Fase — DTEC

> **Status:** Mapa pronto (cenário, portas, luzes e itens). Sem robôs e sem lugar na história ainda.  
> **Área:** o DTEC, departamento de tecnologia: laboratórios, servidores e o salão de uma máquina grande  
> **No menu Fases:** **DTEC** (começa na recepção)

---

## 1. Visão Geral da Área

- **O que é:** uma **fase solta**, como o Labirinto. Não se chega a ela pelos mapas atuais e ela ainda não tem lugar na história (decisão do Davi). Serve para explorar e, depois, receber robôs e um objetivo.
- **A máquina:** no salão do meio (Lab Central) há uma **máquina grande e brilhante**: um anel enorme em pé, duas torres com bobinas de cobre e, no centro do anel, um núcleo ciano que pulsa e solta faíscas. **Ela não tem nome nem papel na história.** Não é a Âncora: se um dia for, isso entra no Enredo Principal por decisão do grupo.
- **Visual:** laboratório lacrado, mais inteiro que a Biblioteca, mas com mil anos de poeira. Azulejo branco embaixo e painel cinza em cima, com a faixa azul do DTEC entre os dois; duto de ventilação no teto; janelas de laboratório, quadros brancos (um deles com um grafo), painéis e terminais. Rachaduras com mato entrando e uma planta de escritório que tomou o canto.
- **Luz:** fluorescentes frias que piscam. No Lab Central, a luz ciano da máquina pulsa devagar (`LuzPulsante`), e ela vaza pelas portas do salão nos dois corredores.
- **Som:** o zumbido do prédio em todas as salas e, perto da máquina, um ronco grave (o mesmo zumbido do bunker, com o tom mais baixo).

---

## 2. Topologia e Salas (Nós do Grafo)

Cada ligação é uma `Porta` (`cenas/sistemas/porta.tscn`). O Lab Central fica **no meio do mapa**: os dois corredores chegam nele pela porta do centro.

```
                RECEPÇÃO ── (saída: lacrada)
                   │
 CORREDOR NORTE ── eletrônica
                ── informática (o notebook está aqui)
                ── LAB CENTRAL (a máquina) ──┐
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
| `lab_central` | 960 × 560 | **A máquina** no centro, consoles dos dois lados, racks, cilindros de gás, telões e janelas | 1 cápsula de clarão |
| `corredor_sul` | 2400 × 180 | O outro lado: seis portas, telão, terminal e a porta larga do Lab Central | 1 pilha, 2 pedras |
| `lab_eletronica` | 480 × 560 | Três bancadas de eletrônica (osciloscópio, solda, placas), armário, cilindros | 1 pilha, 1 cápsula de clarão |
| `lab_informatica` | 560 × 560 | Nove mesas com computador em três fileiras, rack, quadro | **notebook**, 1 pilha |
| `sala_servidores` | 480 × 480 | Piso elevado e duas fileiras de racks com corredores entre eles, luz verde | 2 pilhas, 1 cápsula de clarão |
| `lab_quimica` | 400 × 480 | Duas capelas de exaustão, bancadas, armários de reagentes, linhas de gás | 1 pilha |
| `lab_robotica` | 560 × 560 | Braços robóticos, dois robôs desmontados nas mesas de manutenção, bancada | 2 cápsulas de clarão, 1 pilha |
| `sala_controle` | 560 × 480 | Telões com o gráfico da máquina, três consoles, mesas, janela | 1 pilha |

### Salas trancadas e lacradas

- **Trancadas** (`Porta.trancada`): **Servidores** e **Robótica**. O leitor de cartão da porta está com o LED vermelho. Abrem com o **notebook** (hack), que fica no Laboratório de Informática. São as salas com mais itens.
- **Lacradas** (`Porta.bloqueada`): saída da recepção, depósito, diretoria, emergência e arquivo. Fita amarela e preta em X e placa de acesso restrito. Só mostram o aviso. Quando uma delas virar sala, basta tirar o `bloqueada`, preencher `cena_destino` e `porta_destino` e trocar a peça da parede por `dtec_porta`.

---

## 3. Objetivos e Progressão

- **Hoje:** explorar, pegar o notebook na Informática, hackear as duas salas trancadas e chegar à máquina.
- **A definir com a equipe:** se a fase entra na história (e onde), se terá robôs, e se a máquina tem algum papel.

---

## 4. Onde está no projeto

| O quê | Onde |
|---|---|
| Cenas das salas | `cenas/salas/dtec/` |
| Kit do DTEC (paredes, chão, objetos) | `cenas/cenario/dtec/`, sprites em `assets/sprites/cenario/dtec/` |
| Gerador do kit (a arte) | `assets/modelagem/cenario/gerar_dtec.py` |
| Montagem das cenas (kit e salas) | `assets/modelagem/salas/dtec/montar_dtec.py` |
| Luz da máquina (pulsa devagar) | `cenas/cenario/luzes/luz_maquina.tscn`, script `scripts/cenario/luz_pulsante.gd` |
| Fase no menu | `dados/fases/09_dtec.tres` |

**Como refazer:** `python assets/modelagem/cenario/gerar_dtec.py` redesenha as peças; `python assets/modelagem/salas/dtec/montar_dtec.py` remonta as cenas. **Cuidado:** o segundo sobrescreve as salas. Se alguém ajustar uma sala no editor do Godot, passe o ajuste para a descrição da sala no fim do `montar_dtec.py` antes de rodar de novo.

### Peças do kit do DTEC

- **Paredes (80 × 112):** `dtec_lisa`, `dtec_rachada` (com mato), `dtec_luminaria` (fluorescente: `luz_tubo` em x + 40, y 34), `dtec_porta` (aberta, LED verde), `dtec_porta_trancada` (LED vermelho), `dtec_porta_lacrada`, `dtec_porta_central` (a entrada larga do salão, com a luz ciano), `dtec_vidro`, `dtec_quadro`, `dtec_painel`, `dtec_armario`, `dtec_cartaz`, `dtec_terminal`, `dtec_extintor`, `dtec_canos`, `dtec_tela_grande`, e o `pilar_dtec` (16 px) para as pontas.
- **Chão (128 × 68):** `chao_dtec`, `chao_dtec_cabos`, `chao_dtec_elevado` (piso de servidor), `chao_dtec_faixa`.
- **Salas fundas:** como no bunker, `chao_dtec_fundo`, `chao_dtec_elevado_fundo`, `chao_dtec_cabos_fundo`, `chao_dtec_faixa_fundo` (128 × 64) e `dtec_lateral` (16 × 64).
- **Objetos:** `bancada_lab`, `bancada_eletronica`, `mesa_computador`, `cadeira_escritorio`, `rack_dtec`, `armario_quimico`, `capela`, `cilindros`, `braco_robotico`, `robo_desmontado`, `console`, `planta`, `balcao_recepcao`, `catraca`, `caixas_lab` e a `maquina` (176 × 156, com as faíscas).
- **Placas das portas:** `Label` dentro de `Paredes` (fundo azul do DTEC, letra clara), em cima da plaquinha que as peças de porta trazem.
