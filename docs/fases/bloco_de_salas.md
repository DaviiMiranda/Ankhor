# Fase — Bloco de salas

> **Status:** Em desenvolvimento (primeira versão jogável: cenário e portas, ainda sem robôs e sem história)  
> **Área:** um bloco de salas de aula da Unifor, dois andares (no GDD: "Blocos de aula")

---

## 1. Visão Geral da Área

- **Nome do Local:** Bloco de salas de aula, em 3026.
- **Ambientação Visual:** **é noite.** Dois corredores longos, um em cima do outro, com seis salas de aula em cada. Pouca luz: o luar azulado entrando pelas janelas e pelos buracos do teto (céu escuro com estrelas, `ceu_noite.png`) e alguns lampiões espalhados. A lanterna faz diferença. O **térreo** está parcialmente enterrado na areia das dunas. No **primeiro andar** o teto caiu em vários pontos: céu, mato no chão e duas árvores crescendo no corredor. Em quase toda sala a lousa ainda está presa na parede, coberta de **tracinhos contados** em grupos de cinco (docs/gdd.md, Blocos de aula).
- **Implementação no Godot:** uma cena por corredor e uma por sala, em `cenas/salas/bloco_de_salas/`. Tudo montado com o kit de cenário (herdando `modelo_sala.tscn`). No menu Fases: **Bloco de salas** (abre o corredor do térreo).

---

## 2. Topologia e Salas (Nós do Grafo)

Cada porta é uma `Porta` (`cenas/sistemas/porta.tscn`): `[E]` e o Gabriel atravessa. A escada fica no mesmo ponto dos dois corredores (x = 2360). As **salas são fundas**: mais altas que largas (400 × 480, 480 × 560 e o auditório 640 × 720). A parede do fundo tem a porta, a lousa e as janelas; o chão desce para a câmera, cheio de fileiras de carteiras, e cada sala organiza essa parte do seu jeito (ver tabela). Os corredores continuam compridos: são corredores.

| Cena | O que é | Piso | Conexões |
|---|---|---|---|
| `corredor_terreo` | Corredor do térreo, 2560 px (8 telas), meio enterrado na areia. Tem uma **lanterna** no começo (some se o Gabriel já tiver uma) | lajota e areia | salas 101 a 106, escada (sobe) |
| `corredor_primeiro_andar` | Corredor do 1º andar, 2560 px, teto aberto | mato e lajota | salas 201 a 206, escada (desce) |
| `sala_101` | Sala de aula comum: oito fileiras de carteiras até a frente, lousa, mesa do professor | lajota | térreo |
| `sala_102` | Invadida pela duna: chão de areia, teto caído, metade das carteiras tombadas entre montes de entulho (3 pedras) | areia | térreo |
| `sala_103` | Barricada: uma linha de carteiras tombadas e estantes atravessa a sala; atrás dela, o acampamento com lampiões (2 pilhas) | lajota e tapete | térreo |
| `sala_104` | Laboratório de informática: fileiras de terminais com cadeiras; telas ainda acesas, verdes | tapete e lajota | térreo |
| `sala_105` | Sala sem janela, a mais escura: carteiras reviradas, dois robôs desmontados e um lampião (2 pilhas) | lajota | térreo |
| `sala_106` | Teto desabado com uma árvore no meio do chão e o luar caindo nela | lajota, mato e areia | térreo |
| `sala_201` | Auditório: doze fileiras de carteiras, duas lousas | tapete | 1º andar |
| `sala_202` | Duas árvores furando o chão, cada uma com carteiras em volta e luar por cima | mato e lajota | 1º andar |
| `sala_203` | Sala dos professores: oito mesas com cadeiras, estantes, quadro de avisos | tapete e lajota | 1º andar |
| `sala_204` | O chão cedeu: um monte de entulho no meio, carteiras tombadas em volta (1 cápsula de clarão) | lajota e areia | 1º andar |
| `sala_205` | Intacta demais: seis fileiras de carteiras perfeitamente alinhadas, sem entulho, a mais clara. Estranha | lajota | 1º andar |
| `sala_206` | Depósito: corredores de estantes, carteiras empilhadas, só um lampião (1 pilha) | lajota e areia | 1º andar |

Para não ficar repetitivo, cada sala tem uma **ideia** (acima), paredes e chão diferentes, a porta ora na esquerda, ora na direita, e luz e escuridão próprias (luar, lampião ou quase nada).

---

## 3. Objetivos e Progressão

- **Personagem:** o esconderijo da **Diana** fica numa das salas de aula deste bloco (qual sala, a definir). Ver [`../historia/personagens/diana.md`](../historia/personagens/diana.md).
- **A definir com a equipe:** o que o Gabriel procura aqui, onde entram os robôs e como o bloco se liga à Biblioteca (a porta de saída da Biblioteca fica no fim da ala leste, esperando por esta fase).

---

## 4. Peças novas do kit

Criadas para este bloco em `assets/modelagem/cenario/gerar_kit.py` (servem para qualquer sala):

| Peça | Cena |
|---|---|
| Lousa com restos de giz e tracinhos | `cenas/cenario/paredes/parede_lousa.tscn` |
| Quadro de avisos de cortiça | `cenas/cenario/paredes/parede_mural.tscn` |
| Escada subindo (térreo) e descendo (1º andar) | `parede_escada_sobe.tscn`, `parede_escada_desce.tscn` |
| Carteira universitária, em pé e tombada | `cenas/cenario/objetos/carteira.tscn`, `carteira_caida.tscn` |

Os números das salas em cima das portas são `Label` com a fonte do jogo, dentro de `Paredes`.

---

## 5. Ainda não feito

- Robôs (a IA de hoje depende do mapa do labirinto).
- História, bilhetes e objetivo.
- Ligação com a Biblioteca.
- Música só nos corredores (ao entrar numa sala ela para; ao voltar, recomeça).
