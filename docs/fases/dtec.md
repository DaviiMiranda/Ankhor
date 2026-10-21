# Fase — Laboratório (D-Tec)

> **Status:** Mapa pronto (cenário, portas, luzes e itens). Sexta fase do jogo, depois do Bunker.  
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
- **A definir com a equipe:** como a fase entra na história (a Âncora está aqui, mas o que se faz com ela está nas pendências do Enredo), e se terá robôs.

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
