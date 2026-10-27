# Fase — Bunker

> **Status:** Jogável do começo ao fim (2026-10-21): robôs, nichos e checkpoints, o quadro de religação do gerador (árvore geradora mínima), o arsenal, as duas salas antigas, as marcas dos Faroleiros e o encontro do grupo na sala de dados, que destrava a comporta do núcleo. As falas do encontro são rascunho  
> **Área:** bunker de pesquisa embaixo do núcleo da Âncora ("ÂNCORA-03")  
> **No menu Fases:** **Bunker** (começa na entrada)

---

## 1. Visão Geral da Área

- **O que é:** um bunker do centro de pesquisa, construído para proteger a equipe da Âncora. Fechado e seco, ainda de pé depois de mil anos, mas gasto: concreto aparente em cima e tinta verde-oliva descascando embaixo, eletrocalhas com cabos pendurados, portas de aço de correr, faixas de perigo amarelas e pretas.
- **Luz:** tubos fluorescentes frios que piscam e luzes de emergência vermelhas. O setor B (lá embaixo) está quase todo no vermelho e alagado.
- **Som:** a trilha do bunker (grave e opressiva, em Dó frígio, com a fita da Clarice ao longe) em todas as salas, por baixo do zumbido do transformador e do ar parado do duto, goteiras no setor B e o motor do gerador.
- **Quem vive aqui:** o **Henrique**, **sozinho**, numa sala de dados **trancada** (a central de dados), com acesso às câmeras do campus e ao rádio. Diz que está ali tentando consertar tudo. A cena mostra o Henrique na estação, de costas, olhando as câmeras (Enredo Principal, seção 8, Ato 3).
- **O Carlos nunca vem ao bunker.**
- **Os robôs patrulham o bunker:** uma **Sentinela** no Corredor A e um **Rastreador** no Corredor B (o alagado). Os cantos protegidos são a sala de dados do Henrique e a **sala segura**; nos corredores, os **nichos** (o vão do posto de máscaras de gás) escondem quem fica parado no escuro.
- **As salas antigas:** **duas** salas do setor B são montadas como interiores de casa: a **sala de visitas de um casarão do fim do século XIX** (B-02) e a **sala de estar de uma casa dos anos 80** (B-07). Mostram a obsessão do Carlos pelo passado **sem explicar**: o jogo não diz quem as montou nem por quê, e nenhum personagem comenta. O que conta que é um cenário: o papel de parede para antes do teto e aparece a laje de concreto do bunker; atrás do vidro da janela do casarão tem concreto, não rua.
- **As marcas dos Faroleiros:** as antigas pichações assinadas "C." saíram (o "NÃO CONFIE NAS LUZES" é o bordão da Clarice, e ela nunca morou aqui). No lugar, duas marcas dos Faroleiros pintadas em âmbar (Enredo, seção 2.4): o **farol inteiro** (lugar seguro) perto da sala segura, no Corredor A, e o **farol apagado** (perigo) perto da comporta do núcleo, no Corredor B. A pichação "ROTAS = GRAFO" da sala de dados, sem assinatura, ficou.
- **O encontro:** no fim da fase, o grupo todo se encontra pela primeira vez na sala de dados: Gabriel, o Henrique, o Zane, a Clarice e a Diana (seção 3). A cena é **provisória**: as falas são rascunho e como a Clarice e a Diana chegam ao bunker está em aberto (Enredo, seção 10.4).

---

## 2. Topologia e Salas (Nós do Grafo)

Cada ligação é uma `Porta` (`cenas/sistemas/porta.tscn`) com o som da porta blindada. As escadas ficam no mesmo x nos dois corredores.

```
                 ENTRADA ── (escotilha: lacrada)
                    │       ELEVADOR (sem energia; depois, atalho para o Corredor B)
                    │
  CORREDOR A ── SALA SEGURA (DESCANSO, ao lado da entrada)    (Sentinela)
              ── dormitório
   (setor A)  ── refeitório
              ── enfermaria
              ── central de dados (Henrique; o encontro)
              ── ARSENAL (trava elétrica: abre com a energia)
                    │ escada
                    │
  CORREDOR B ── B-02: sala antiga do século XIX                (Rastreador)
   (setor B)  ── gerador (o quadro de religação)
              ── depósito
              ── LABORATÓRIO (lacrado)
              ── B-07: sala antiga dos anos 80
              ── ARQUIVO (lacrado)
              ── NÚCLEO (comporta: abre depois do encontro) ── Laboratório (D-Tec)
```

| Cena (`cenas/salas/bunker/`) | Largura | O que tem | Itens |
|---|---|---|---|
| `entrada` | 480 × 560 | Escada da superfície, descontaminação (chuveiros e faixas de perigo), armários, posto de guarda (mesa, cadeira, lampião), planta de evacuação, o elevador (porta fechada, sem energia) e a porta para o setor A. Checkpoint `bunker_chegada` | — |
| `corredor_a` | 2560 × 180 | O corredor principal: portas com placas, janela para a sala dos servidores, canos, quadros elétricos, **três nichos**, a marca do farol inteiro e a escada para o setor B. **Sentinela** de x 600 a 2200 | — |
| `corredor_b` | 2240 × 180 | Nível de baixo: água no chão, luz vermelha, infiltração nas paredes, as portas B-02 e B-07, duas portas lacradas, **dois nichos**, a marca do farol apagado e a **comporta do núcleo**. **Rastreador** de x 500 a 2100. Checkpoint `bunker_setor_b` ao pé da escada | — |
| `sala_segura` | 320 × 180 | A **sala segura** do modelo (os óculos do Zane para salvar, o piano), com a luz de um verde-oliva. A porta é a DESCANSO no corredor A, ao lado da entrada, com a **luz verde** em cima ([`../mecanicas/sala_segura.md`](../mecanicas/sala_segura.md)) | — |
| `dormitorio` | 480 × 560 | Fileiras de beliches (três por fileira), armários, caixas | 1 pilha |
| `refeitorio` | 480 × 560 | Fileiras de mesas compridas de aço, prateleiras de latas, planta do bunker | 1 cápsula de clarão |
| `enfermaria` | 400 × 480 | Duas fileiras de macas com biombos entre elas, suportes de soro, armários de remédios | 1 pilha |
| `central_dados` | 560 × 640 | **A sala de dados** do Henrique: corredores de racks de servidores, janela para os servidores, a parede do grafo, a estação (`estacao_dados.png`: três monitores de tubo que mostram as câmeras do campus) e o canto onde ele dorme (colchão, cobertor roxo, latas, lampião). Depois que a energia volta, o **Zane, a Clarice e a Diana** estão ali, e o encontro começa sozinho quando Gabriel chega perto | — |
| `arsenal` | 400 × 360 | Armários e prateleiras de aço, estantes, mesa e caixas. Abre quando a energia volta | 2 cápsulas de clarão, 1 pilha |
| `gerador` | 480 × 560 | Dois geradores a diesel ligados, tambores de combustível, quadros elétricos e o **quadro de religação** na frente do painel | — |
| `deposito` | 400 × 480 | Corredores de estantes, caixotes, tambores | 1 pilha, 1 cápsula de clarão, 2 pedras |
| `sala_antiga_xix` | 480 × 360 | **B-02.** Papel de parede vinho, lambri de madeira, moldura dourada, duas janelas com cortina e concreto atrás do vidro, assoalho. Relógio de pêndulo, cristaleira, sofá de veludo, mesa redonda com a toalha de renda e o lampião aceso, duas poltronas | — |
| `sala_antiga_80` | 480 × 360 | **B-07.** Papel de parede bege com losangos marrons e laranja, estante embutida com a TV de tubo, o videocassete, as fitas e os discos, quadro do pôr do sol, carpete. Sofá xadrez, mesinha com o telefone de disco, rack com o toca-discos e as caixas de som, dois abajures de pé | — |

### Portas que abrem com o progresso

| Porta (`id`) | Onde | Como abre | Aviso enquanto não abre |
|---|---|---|---|
| `elevador` | entrada | `liberada_por = "bunker_energia"`: leva ao pé da escada do Corredor B | "O elevador está sem energia." |
| `arsenal` | corredor A | `liberada_por = "bunker_energia"` | "Arsenal: a trava é elétrica. Sem energia, não abre." |
| `nucleo` | corredor B (comporta) | `liberada_por = "bunker_comporta_aberta"`: leva à 6ª fase, o Laboratório | "A comporta do núcleo não se mexe. Nem um milímetro." |

### Salas lacradas (para depois)

| Porta (`id`) | Onde | Aviso de hoje | Ideia |
|---|---|---|---|
| `escada_superficie` | entrada | "A escotilha lá em cima emperrou." | Por onde o Gabriel chega, por enquanto vindo da rampa do Centro de Convivência |
| `laboratorio` | corredor B | "Lacrada pelo sistema. O Zane está tentando abrir." | Pesquisa da Âncora: conteúdo de história, pendente |
| `arquivo` | corredor B | idem | Registros da Âncora: conteúdo de história, pendente |

O Henrique explica no diálogo que o setor B está lacrado pelo sistema e que o Zane está tentando quebrar a senha: as salas fechadas viram gancho de história, não parede invisível.

---

## 3. Objetivos e Progressão

1. **Chegada** pela entrada (checkpoint). No Corredor A, a Sentinela.
2. **A sala de dados:** achar o Henrique e conversar com ele (a conversa anota "Henrique, na sala de dados" no caderno). Gabriel o reconhece pela lenda do campus: o aluno que sumiu na Biblioteca em 2019 (Enredo, seção 7.2). Na conversa, o Henrique diz que está tentando consertar tudo; a mentira dele não aparece aqui (Enredo, seção 8, "A virada").
3. **O setor B:** descer pela escada (checkpoint), passar pelo Rastreador e chegar ao gerador. As duas salas antigas ficam no caminho, sem explicação.
4. **Religar o bunker:** no **quadro de religação** do gerador, levar energia aos sete pontos (gerador, os dois corredores, o elevador, a comporta, o arsenal e a sala de dados) usando só o cabo do carretel, **23 m**. Só existe um jeito: a **árvore geradora mínima** (Kruskal, [`../computacao/arvore_geradora_minima.md`](../computacao/arvore_geradora_minima.md)). Com a energia, o **elevador** vira atalho da entrada ao Corredor B, o **arsenal** abre, e o **Zane chama pelo rádio** (`zane_bunker_01`): "vem pra sala de dados: tá todo mundo aqui".
5. **O encontro:** na sala de dados, o diálogo `bunker_encontro` começa sozinho. O Zane conta que quebrou a senha do setor B; é a primeira vez do grupo todo numa sala só. No fim, a comporta do núcleo destrava.
6. **Saída:** a comporta do núcleo, no fim do Corredor B, leva à 6ª fase, o **Laboratório (D-Tec)**.

**Em aberto (decisão do grupo):** as falas do encontro e da chamada do Zane são **rascunho** (o Davi vai refinar as do Zane); como a Clarice e a Diana chegam ao bunker; se o Baltazar entra nesse encontro (hoje não entra: onde e quando Gabriel o encontra está pendente, Enredo, seção 10.5).

---

## 4. Onde está no projeto

| O quê | Onde |
|---|---|
| Cenas das salas | `cenas/salas/bunker/` |
| Kit do bunker (paredes, chão, objetos) | `cenas/cenario/bunker/`, sprites em `assets/sprites/cenario/bunker/` |
| Gerador do kit | `assets/modelagem/cenario/gerar_bunker.py` |
| Luzes (tubo fluorescente e emergência) | `cenas/cenario/luzes/luz_tubo.tscn`, `luz_emergencia.tscn` |
| Henrique na estação | `cenas/personagens/henrique_na_estacao.tscn` (a estação em `assets/sprites/cenario/objetos/estacao_dados.png`, gerada por `assets/modelagem/cenario/gerar_estacao_dados.py`) |
| Diálogos do Henrique | `dados/dialogos/henrique_primeiro_encontro.json`, `henrique_de_novo.json` |
| O encontro | `dados/dialogos/bunker_encontro.json` (rascunho), começado pelo `GatilhoDialogo` (`cenas/sistemas/gatilho_dialogo.tscn`, script `scripts/sistemas/gatilho_dialogo.gd`); a chamada do Zane em `dados/transmissoes/zane_bunker_01.tres` (rascunho) |
| Quadro de religação | `cenas/sistemas/painel_religacao.tscn`, script `scripts/sistemas/painel_religacao.gd` (o grafo, o Kruskal e a tela) |
| Salas antigas e arsenal | as cenas saem de `assets/modelagem/salas/bunker/montar_salas_bunker.py`; a arte das salas antigas, de `assets/modelagem/cenario/gerar_salas_antigas.py` (em `assets/sprites/cenario/bunker/salas_antigas/`) |
| Marcas dos Faroleiros | `assets/sprites/cenario/objetos/marca_farol_inteiro.png` e `marca_farol_apagado.png`, geradas por `assets/modelagem/cenario/gerar_marcas_faroleiros.py` |
| Clarice, sentada (sem uso) | `cenas/personagens/clarice.tscn`: ficou da versão em que ela morava aqui. As conversas daquela versão foram apagadas em 2026-10-26 |
| Chips hexagonais (3, colecionáveis) | `ChipOculos1` a `3` no `dormitorio`, no `refeitorio` e no `deposito`. Opcionais: ao juntar os três, o quarto do Gabriel ganha os óculos do Zane no criado-mudo (ver [`../mecanicas/colecionaveis.md`](../mecanicas/colecionaveis.md)) |
| Sons | `assets/modelagem/audio/gerar_efeitos_bunker.py` |
| Música | `assets/modelagem/audio/gerar_trilha_bunker.py`, tocada por `cenas/sistemas/musica_bunker.tscn` |

### Peças do kit do bunker

- **Paredes (80 × 112):** `bunker_nicho` (o vão do posto de máscaras de gás: ponha um `NichoEsconderijo` em x + 40, y 128), `bunker_lisa`, `bunker_rachada` (infiltração), `bunker_canos`, `bunker_luminaria` (tubo fluorescente: ponha uma `luz_tubo` em x + 40, y 34), `bunker_emergencia` (giroflex: `luz_emergencia` em x + 40, y 30), `bunker_porta` (aberta), `bunker_porta_fechada`, `bunker_porta_lacrada`, `bunker_comporta`, `bunker_armarios`, `bunker_painel`, `bunker_mapa`, `bunker_grafo`, `bunker_vidro`, `bunker_prateleiras`, `bunker_remedios`, `bunker_descontaminacao`, `bunker_escada_sobe`, `bunker_escada_desce`, e o `pilar_bunker` (16 px) para as pontas.
- **Chão (128 × 68):** `chao_bunker`, `chao_bunker_grade`, `chao_bunker_agua`, `chao_bunker_faixa`.
- **Salas fundas:** as salas (não os corredores) são mais altas que largas. Abaixo da peça de chão normal vão as peças de fundo (128 × 64, repetem para baixo): `chao_bunker_fundo`, `chao_bunker_grade_fundo`, `chao_bunker_agua_fundo`; nos lados, `bunker_lateral` (16 × 64; a da direita com `flip_h`). No `Sala`, `altura` e `chao_frente` (= altura - 4).
- **Objetos:** `beliche`, `mesa_refeitorio`, `maca`, `suporte_soro`, `biombo`, `gerador`, `tambor`, `tambor_verde`, `caixas`, `rack_servidor`, `colchao`, `estante_metal`, `latas`, `mesa_metal`.
- **Placas das portas:** são `Label` dentro de `Paredes` (fundo de aço escuro, letra amarela), em cima da plaquinha que as peças de porta já trazem. As pichações também são `Label`, em vermelho.
