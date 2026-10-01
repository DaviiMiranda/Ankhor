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

Cada porta é uma `Porta` (`cenas/sistemas/porta.tscn`): `[E]` e o Gabriel atravessa. A escada fica no mesmo ponto dos dois corredores (x = 2360). As salas têm de 800 a 1280 px de largura (2,5 a 4 telas): a segunda metade de cada uma tem conteúdo próprio, não é cópia da primeira.

| Cena | O que é | Piso | Conexões |
|---|---|---|---|
| `corredor_terreo` | Corredor do térreo, 2560 px (8 telas), meio enterrado na areia. Tem uma **lanterna** no começo (some se o Gabriel já tiver uma) | lajota e areia | salas 101 a 106, escada (sobe) |
| `corredor_primeiro_andar` | Corredor do 1º andar, 2560 px, teto aberto | mato e lajota | salas 201 a 206, escada (desce) |
| `sala_101` | Sala de aula comum: fileiras de carteiras, lousa, mesa do professor | lajota | térreo |
| `sala_102` | Invadida pela duna: chão de areia, teto caído, carteiras soterradas (2 pedras) | areia | térreo |
| `sala_103` | Barricada: carteiras e estante empilhadas na porta, lampiões de quem acampou e, no fundo, uma segunda barreira de carteiras tombadas (2 pilhas) | lajota e tapete | térreo |
| `sala_104` | Laboratório de informática: dez terminais e cabines; uma tela ainda acesa, verde | tapete e lajota | térreo |
| `sala_105` | Sala sem janela, a mais escura, com dois robôs desmontados e um lampião (2 pilhas) | lajota | térreo |
| `sala_106` | Teto desabado com uma árvore no meio | lajota, mato e areia | térreo |
| `sala_201` | Auditório: 42 carteiras em três fileiras, duas lousas | tapete | 1º andar |
| `sala_202` | Dois buracos no teto, cada um com uma árvore e carteiras em volta | mato e lajota | 1º andar |
| `sala_203` | Sala dos professores: mesas, estante, quadro de avisos | tapete e lajota | 1º andar |
| `sala_204` | O chão cedeu: monte de entulho no meio (1 cápsula de clarão) | lajota e areia | 1º andar |
| `sala_205` | Intacta demais: carteiras alinhadas, sem entulho, a mais clara (três janelas de luar). Estranha | lajota | 1º andar |
| `sala_206` | Depósito: estantes, carrinhos e carteiras empilhadas, só um lampião (1 pilha) | lajota e areia | 1º andar |

Para não ficar repetitivo, cada sala tem uma **ideia** (acima), paredes e chão diferentes, a porta ora na esquerda, ora na direita, e luz e escuridão próprias (luar, lampião ou quase nada).

---

## 3. Objetivos e Progressão

- **A definir com a equipe:** o que o Gabriel procura aqui, que antecessor deixou registros no bloco, onde entram os robôs e como o bloco se liga à Biblioteca (a porta de saída da Biblioteca fica no fim da ala leste, esperando por esta fase).

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
