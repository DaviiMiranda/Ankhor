# Fase — Bunker

> **Status:** Em desenvolvimento (cenário, portas, o Henrique na estação e o primeiro diálogo prontos; robôs, salas antigas e salas lacradas para depois)  
> **Área:** bunker de pesquisa embaixo do núcleo da Âncora ("ÂNCORA-03")  
> **No menu Fases:** **Bunker** (começa na entrada)

---

## 1. Visão Geral da Área

- **O que é:** um bunker do centro de pesquisa, construído para proteger a equipe da Âncora. Fechado e seco, ainda de pé depois de mil anos, mas gasto: concreto aparente em cima e tinta verde-oliva descascando embaixo, eletrocalhas com cabos pendurados, portas de aço de correr, faixas de perigo amarelas e pretas.
- **Luz:** tubos fluorescentes frios que piscam e luzes de emergência vermelhas. O setor B (lá embaixo) está quase todo no vermelho e alagado.
- **Som:** a trilha do bunker (grave e opressiva, em Dó frígio, com a fita da Clarice ao longe) em todas as salas, por baixo do zumbido do transformador e do ar parado do duto, goteiras no setor B e o motor do gerador.
- **Quem vive aqui:** o **Henrique**, **sozinho**, numa sala de dados **trancada** (a central de dados), com acesso às câmeras do campus e ao rádio. Diz que está ali tentando consertar tudo. A cena mostra o Henrique na estação, de costas, olhando as câmeras. A Clarice e a Diana ficam no Bloco de salas, na 103. Decidido em 2026-10-15 (Enredo Principal, seção 8, Ato 3).
- **O Zane chega depois:** Gabriel chega ao bunker pelo alçapão da oficina do Zane, no fim do Labirinto, e o Zane disse que ia atrás dele depois. O que o Zane faz quando chega, e onde fica na sala de dados, está pendente (Enredo Principal, seção 12.3). Ele ainda não aparece no bunker.
- **O Carlos nunca vem ao bunker.**
- **Os robôs patrulham o bunker** (decidido em 2026-10-15). Ainda não estão nas cenas: falta escolher quais robôs, as rotas nos corredores e se eles entram também no setor B (Enredo Principal, seção 12.5). Quando entrarem, o bunker deixa de ser um lugar seguro, e os cantos protegidos são a sala de dados trancada do Henrique e a **sala segura**.
- **As salas antigas:** uma ou mais salas do bunker são montadas como **interiores de casas e lugares antigos dos séculos XIX e XX**. Mostram a obsessão do Carlos pelo passado **sem explicar**: o jogo não diz quem as montou nem por quê, e nenhum personagem comenta. Quantas são, de que épocas e lugares e onde ficam está pendente (Enredo Principal, seção 12.5). Ainda não existem.
- **Pichações pelas paredes:** "NÃO CONFIE NAS LUZES" pichado no corredor, a seta "→ DADOS C." apontando para a sala de dados, "NÃO ABRE. JÁ TENTEI. C." perto das portas lacradas, e o grafo das rotas dos robôs na parede da central. Foram feitas quando a Clarice morava aqui; agora ela fica na 103 desde que chegou, e falta decidir quem as fez ou se saem (uma opção: virar marcas antigas dos Faroleiros; Enredo Principal, seção 12.3).

---

## 2. Topologia e Salas (Nós do Grafo)

Cada ligação é uma `Porta` (`cenas/sistemas/porta.tscn`) com o som da porta blindada. As escadas ficam no mesmo x nos dois corredores.

```
                 ENTRADA ── (escotilha: lacrada)
                    │       (elevador: lacrado)
                    │
  CORREDOR A ── SALA SEGURA (DESCANSO, ao lado da entrada)
              ── dormitório
   (setor A)  ── refeitório
              ── enfermaria
              ── central de dados (Henrique, trancada)
              ── ARSENAL (lacrado)
                    │ escada
                    │
  CORREDOR B ── gerador
   (setor B)  ── depósito
              ── LABORATÓRIO (lacrado)
              ── ARQUIVO (lacrado)
              ── NÚCLEO (comporta, lacrada)
```

| Cena (`cenas/salas/bunker/`) | Largura | O que tem | Itens |
|---|---|---|---|
| `entrada` | 480 × 560 | Escada da superfície, descontaminação (chuveiros e faixas de perigo), armários, posto de guarda (mesa, cadeira, lampião), planta de evacuação, elevador lacrado e a porta para o setor A | — |
| `corredor_a` | 2560 × 180 | O corredor principal: portas com placas, janela para a sala dos servidores, canos, quadros elétricos, as pichações assinadas "C." e a escada para o setor B | — |
| `corredor_b` | 2240 × 180 | Nível de baixo: água no chão, luz vermelha, infiltração nas paredes, três portas lacradas e a **comporta do núcleo** | — |
| `sala_segura` | 320 × 180 | A **sala segura** do modelo (os óculos do Zane para salvar, o piano), com a luz de um verde-oliva. A porta é a DESCANSO no corredor A, ao lado da entrada, com a **luz verde** em cima ([`../mecanicas/sala_segura.md`](../mecanicas/sala_segura.md)) | — |
| `dormitorio` | 480 × 560 | Fileiras de beliches (três por fileira), armários, caixas | 1 pilha |
| `refeitorio` | 480 × 560 | Fileiras de mesas compridas de aço, prateleiras de latas, planta do bunker | 1 cápsula de clarão |
| `enfermaria` | 400 × 480 | Duas fileiras de macas com biombos entre elas, suportes de soro, armários de remédios | 1 pilha |
| `central_dados` | 560 × 640 | **A sala de dados** do Henrique, trancada: corredores de racks de servidores, janela para os servidores, a parede do grafo, a estação (`estacao_dados.png`: três monitores de tubo que mostram as câmeras do campus) e o canto onde ele dorme (colchão, cobertor roxo, latas, lampião). Hoje a porta abre normalmente: na conversa, o Henrique diz que abriu para Gabriel porque o viu chegando | — |
| `gerador` | 480 × 560 | Dois geradores a diesel ligados, tambores de combustível, quadros elétricos | — |
| `deposito` | 400 × 480 | Corredores de estantes, caixotes, tambores | 1 pilha, 1 cápsula de clarão, 2 pedras |

### Salas lacradas (para fazer depois)

As portas existem, com placa e o visual de porta lacrada (fita vermelha e branca, corrente e cadeado), mas usam `bloqueada = true`: apertar `E` só mostra o aviso e toca a maçaneta emperrada. O notebook não abre porta bloqueada. Quando uma sala for feita, basta tirar o `bloqueada`, preencher `cena_destino` e `porta_destino` e trocar a peça da parede por `bunker_porta`.

| Porta (`id`) | Onde | Aviso de hoje | Ideia |
|---|---|---|---|
| `escada_superficie` | entrada | "A escotilha lá em cima emperrou." | Por onde o Gabriel chega, por enquanto vindo da saída do Labirinto |
| `elevador` | entrada | "O elevador está sem energia." | Atalho entre os setores depois de religar a energia no gerador |
| `arsenal` | corredor A | "Arsenal: acesso só com autorização." | Cápsulas de clarão e equipamento |
| `laboratorio` | corredor B | "Lacrada pelo sistema. O Zane está tentando abrir." | Pesquisa da Âncora; talvez parte da pesquisa do professor |
| `arquivo` | corredor B | idem | Registros da Âncora (o nome de usuário de 2026?) |
| `nucleo` | corredor B (comporta) | "A comporta do núcleo não se mexe. Nem um milímetro." | Acesso ao núcleo da Âncora: reta final |

O Henrique explica no diálogo que o setor B está lacrado pelo sistema e que o Zane está tentando quebrar a senha: as salas fechadas viram gancho de história, não parede invisível.

---

## 3. Objetivos e Progressão

- **Hoje:** explorar o bunker, achar o Henrique na sala de dados e conversar com ele (a conversa anota "Henrique, na sala de dados" no caderno). Gabriel o reconhece pela lenda do campus: o aluno que sumiu na Biblioteca em 2019 (Enredo Principal, seção 7.2). Na conversa, o Henrique diz que está tentando consertar tudo; a mentira dele não aparece aqui (Enredo Principal, seção 8, "A virada").
- **Chegada e saída:** o Bunker é a **5ª fase**, depois do Centro de Convivência (a rampa do subsolo do Convivência leva à `entrada`). A comporta do núcleo no fim do Corredor B (`Porta_nucleo`) leva à 6ª fase, o **Laboratório (D-Tec)**.
- **A definir com a equipe:** o que destrava o setor B (senhas nos disquetes? religar o gerador?); quais robôs patrulham o bunker e se entram no setor B; as salas antigas (quantas, de que épocas, onde); a cena do Zane quando ele chega.

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
| Clarice, sentada (sem uso) | `cenas/personagens/clarice.tscn` e `clarice_primeiro_encontro.json`, `clarice_de_novo.json`: ficaram da versão em que ela morava aqui |
| Sons | `assets/modelagem/audio/gerar_efeitos_bunker.py` |
| Música | `assets/modelagem/audio/gerar_trilha_bunker.py`, tocada por `cenas/sistemas/musica_bunker.tscn` |

### Peças do kit do bunker

- **Paredes (80 × 112):** `bunker_lisa`, `bunker_rachada` (infiltração), `bunker_canos`, `bunker_luminaria` (tubo fluorescente: ponha uma `luz_tubo` em x + 40, y 34), `bunker_emergencia` (giroflex: `luz_emergencia` em x + 40, y 30), `bunker_porta` (aberta), `bunker_porta_fechada`, `bunker_porta_lacrada`, `bunker_comporta`, `bunker_armarios`, `bunker_painel`, `bunker_mapa`, `bunker_grafo`, `bunker_vidro`, `bunker_prateleiras`, `bunker_remedios`, `bunker_descontaminacao`, `bunker_escada_sobe`, `bunker_escada_desce`, e o `pilar_bunker` (16 px) para as pontas.
- **Chão (128 × 68):** `chao_bunker`, `chao_bunker_grade`, `chao_bunker_agua`, `chao_bunker_faixa`.
- **Salas fundas:** as salas (não os corredores) são mais altas que largas. Abaixo da peça de chão normal vão as peças de fundo (128 × 64, repetem para baixo): `chao_bunker_fundo`, `chao_bunker_grade_fundo`, `chao_bunker_agua_fundo`; nos lados, `bunker_lateral` (16 × 64; a da direita com `flip_h`). No `Sala`, `altura` e `chao_frente` (= altura - 4).
- **Objetos:** `beliche`, `mesa_refeitorio`, `maca`, `suporte_soro`, `biombo`, `gerador`, `tambor`, `tambor_verde`, `caixas`, `rack_servidor`, `colchao`, `estante_metal`, `latas`, `mesa_metal`.
- **Placas das portas:** são `Label` dentro de `Paredes` (fundo de aço escuro, letra amarela), em cima da plaquinha que as peças de porta já trazem. As pichações também são `Label`, em vermelho.
