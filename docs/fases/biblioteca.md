# Fase 1 — Biblioteca

> **Status:** Primeira fase confirmada / Em desenvolvimento  
> **Área:** Biblioteca da Unifor  
> **Ponto de Partida:** Gabriel acorda nesta fase após ser puxado de uma madrugada de 2026 para o ano de 3026 pela fenda temporal da Âncora.

---

## 1. Visão Geral da Área

- **Nome do Local:** Biblioteca Central da Unifor (Ano 3026).
- **Ambientação Visual:** O campus mil anos no futuro como centro de física do tempo arruinado pela explosão da Âncora. Vegetação, poeira e feixes de luz natural.
- **Implementação no Godot:**
  - Cena: `cenas/salas/biblioteca.tscn`
  - Script: `scripts/salas/biblioteca.gd`
  - Formato: Sala em vista lateral 2.5D ampliada: 1440 × 420 px (4,5 telas de largura; parte sul com profundidade y-sort de 122 a 416).
  - **Ala leste** (x de 960 a 1440, depois da coluna do meio): a sala de periódicos. Um terceiro buraco no teto com uma árvore nova embaixo, mesas de leitura, cabines e, no fundo sul, um segundo acervo com corredores para se esconder. A **porta de saída** (para os Blocos de aula) fica no fim dela.
  - Itens iniciais: lanterna perto do ponto de despertar do Gabriel; três pilhas (duas no lado escuro do salão, uma no acervo leste); doze lampiões de emergência e seis luminárias de parede.

---

## 2. Topologia e Salas

- **Ponto de Início:** O local da cabine/salão da Biblioteca onde Gabriel desperta em 3026.
- **Salas e Conexões:** *(A definir com a equipe o mapeamento dos nós vizinhos e saídas da Biblioteca)*

---

## 3. Objetivos e Progressão

- **Objetivo Principal:** Explorar a Biblioteca, recuperar os primeiros itens (como a lanterna), encontrar bilhetes deixados pelas pessoas de outras épocas, evitar os robôs de patrulha e encontrar a saída/acesso para as próximas áreas.
- **Passos e Puzzles:** *(A definir com a equipe)*

---

## 4. Registros dos antecessores

Só três antecessores aparecem na Biblioteca (fichas em [`../historia/personagens/`](../historia/personagens/)):

- **Acampamento de Baltazar:** um nicho entre as raízes da árvore no meio do salão, com a luneta de latão rachada, um toco de vela e o **diário** embrulhado em pano. Mapas de estrelas riscados na casca e um robô desmontado peça por peça. Sem corpo: o que aconteceu com ele fica em aberto. O diário ensina o ponto fraco dos sensores ópticos.
- **Bilhete da Clarice:** perto de um terminal, com gírias dos anos 90 e o aviso "não confie nas luzes". Parece uma despedida, e o jogador acha que ela morreu.
- **Gancho (opcional):** no fim da fase, o telefone do balcão toca pela primeira vez. É a Clarice.
- **Primeira chamada do Rafael:** Gabriel acha um rádio portátil, e a voz do Rafael dá a primeira dica de patrulha.
- **Segunda chamada do Rafael:** ao entrar no acervo com o rádio, ele fala como se estivesse vendo o Gabriel.
- **Implementado.** Posições, gatilhos e como funciona em [`../mecanicas/registros_e_caderno.md`](../mecanicas/registros_e_caderno.md). O gancho do telefone ainda não.

---

## 5. Inimigos e Ameaças

- *(A definir com a equipe quais modelos de robôs patrulham a Biblioteca)*

---

## 6. Sala Segura e Sonho

- *(A definir com a equipe a localização da sala segura e a interação correspondente)*
