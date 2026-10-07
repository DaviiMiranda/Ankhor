# Personagens

> **Lei do projeto:** quem cada personagem é (história, personalidade, como fala, o que quer, o que teme, defeito, arco e relações) está no [Enredo Principal](../enredo_principal.md), seção 4. As fichas desta pasta **não repetem nem mudam** isso: guardam o que a produção precisa (onde o personagem aparece, como chega ao jogador, função no jogo, direção de arte e arquivos). Se uma ficha contradisser o Enredo, vale o Enredo.

---

## Quem é quem

Todos têm cerca de 20 anos, estão vivos e foram puxados pela fenda no chão da Biblioteca, com dias de diferença.

| Ficha | Época | Em uma frase | Estado no jogo |
|---|---|---|---|
| [Gabriel Magalhães](gabriel.md) | 2026 | O protagonista. Estudante irônico que prefere observar a agir. Penúltimo a chegar | Jogável |
| [Baltazar Magalhães](baltazar.md) | ~1750 | Homem de fé com olhos de cientista. Antepassado de Gabriel | Acampamento e diário na Biblioteca |
| [Diana](diana.md) | 1978 | Recruta da polícia dramática, ansiosa e impulsiva | Só no papel |
| [Clarice](clarice.md) | 1994 | Mente brilhante que usa o sarcasmo como armadura | Em pessoa no Bunker, com diálogos |
| [Rafael](rafael.md) | 2008 | Segurança otimista que jura que tudo é reforma | Voz no rádio da Biblioteca |
| [O pesquisador](pesquisador.md) | 2019 | Gênio quieto que desconfia ter causado tudo (nome pendente) | Só no papel |
| [Zane](zane.md) | 2123 | Filho de um mundo de máquinas, o último a chegar | Só no papel |
| [Os robôs](robos.md) | 3026 | Os inimigos, controlados pela IA | Sentinela e Rastreador no Labirinto |

A **IA** que domina a Terra não tem ficha: não tem rosto nem voz e aparece só pelos robôs (Enredo Principal, seção 4.5).

---

## Como os personagens funcionam no Godot

Cada personagem e inimigo é uma **cena isolada** (`.tscn`) com seu script (`.gd`):

1. **O jogador (Gabriel):** `CharacterBody2D` controlado pelo jogador, com máquina de estados de locomoção. Ver [`gabriel.md`](gabriel.md).
2. **Os robôs:** `CharacterBody2D` com máquina de estados (Rotina, Investigando, Perseguindo, Atordoado, Retornando) e sensores (visão por produto escalar e raycast, audição pelo grafo com BFS, luz). Ver [`robos.md`](robos.md).
3. **Os outros personagens:** NPCs fixos nos esconderijos, que conversam pelo sistema de diálogos (ver [`../../dialogos/README.md`](../../dialogos/README.md)). A Clarice é o primeiro (`cenas/personagens/clarice.tscn`). Também chegam ao jogador por registros, rádio e telefone (ver [`../../mecanicas/registros_e_caderno.md`](../../mecanicas/registros_e_caderno.md)).

---

## Como criar uma ficha nova

Use o modelo em [`template_personagem.md`](template_personagem.md). Antes, o personagem precisa estar no Enredo Principal: personagem novo é decisão de história, e entra primeiro lá e em [`../../decisoes.md`](../../decisoes.md).
