# Ficha de Personagem (Template)

> **Status:** [Em definição / Em desenvolvimento / Concluído]  
> **Responsável:** [Nome do integrante]

---

## 1. Identificação Básica

- **Nome:** [Nome do personagem]
- **Tipo:** [Jogador / Robô (Inimigo) / NPC de Sonho]
- **Papel no Jogo:** Breve resumo de sua função no gameplay ou na narrativa.

---

## 2. Comportamento e Funcionamento Mecânico

- **Velocidade de Movimento:** (ex.: Lento / Médio / Rápido)
- **Sensores e Percepção (Para Robôs Inimigos):**
  - **Sensor Acústico:** [Alto / Médio / Nenhum] — Raio de detecção em nós do grafo.
  - **Sensor Visual:** [Cone angular em graus / Alcance em pixels].
  - **Sensor Fotossensível:** Reage à luz do pote de fungos? [Sim / Não].
- **Rotina Padrão:** O que faz quando não está em perseguição (ex.: ronda programada, varredura de área, etc.).
- **Reação a Distrações / Clarão:** Como responde a pedras jogadas ou cápsulas de clarão de fungos.

---

## 3. Cenas e Assets Associados

- **Cena Godot:** `cenas/personagens/nome_personagem.tscn`
- **Script GDScript:** `scripts/personagens/nome_personagem.gd`
- **Sprites / Render:** `assets/sprites/personagens/nome_personagem/`
- **Modelo 3D (se houver):** `assets/modelagem/personagens/nome_personagem.blend`
