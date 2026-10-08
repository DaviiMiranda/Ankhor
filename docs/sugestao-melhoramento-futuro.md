# Melhorias e Polimento

Registro de melhorias secundárias, polimento visual, sonoro e ajustes de qualidade de vida (QoL). São itens que aumentam a imersão e o acabamento do jogo, mas não bloqueiam o escopo principal nem as entregas prioritárias.

---

## Animação e Visual

- [ ] **Animação de abrir a mochila (Inventário):**
  - Adicionar animação do Gabriel parando e abrindo a mochila ao acionar a tela de inventário (`Tab` / `I`).
  - Transição visual suave conectando a postura de exploração à abertura da interface.

- [ ] **Animação de transição em portas:**
  - Animação específica do Gabriel atravessando ou abrindo uma porta na mudança de sala, em vez de corte seco ou apenas fade.

## Áudio e Feedback

- [ ] **Respiração ofegante durante perseguição:**
  - Efeito sonoro de respiração pesada/ofegante do Gabriel quando estiver sendo ativamente perseguido por robôs ou em momentos de fuga sob alta tensão.

- [ ] **Efeitos sonoros de interface:**
  - ~~Som de zíper/abertura de mochila ao entrar no inventário.~~ Feito no PR #30 (abrir e fechar).
  - Efeito sutil ao equipar/desequipar gadgets.

## Interface e Qualidade de Vida (QoL)

- [ ] **Indicadores de contexto:**
  - Transições e pequenos efeitos visuais (fade/escala) ao selecionar itens na grade do inventário.

## Conteúdo extra

- [ ] **Easter eggs colecionáveis que dão conquistas:**
  - Objetos escondidos pelo campus, fora do caminho principal, que o jogador pode achar e guardar. Cada um (ou cada conjunto) **desbloqueia uma conquista**.
  - **Nunca são obrigatórios:** não abrem portas nem ajudam a avançar. São recompensa para quem explora.
  - **Sugestões de objetos** (precisam seguir o [Enredo Principal](historia/enredo_principal.md)): relíquias de cada época dos personagens, como uma moeda colonial (Baltazar), um disquete com adesivo (Clarice), um crachá da Unifor de 2026 (Gabriel) e um chip de 2123 (Zane); e fitas cassete e pôsteres dos anos 80, a obsessão do Carlos, espalhados perto do D-Tec.
  - **Onde aparecem:** numa tela de conquistas no menu principal (já existe uma branch `feat/menu-conquistas` com trabalho no menu) e, ao achar o objeto, um aviso curto no HUD, como o das anotações.
  - **Depende de:** sistema de save, para as conquistas continuarem desbloqueadas entre uma partida e outra.
