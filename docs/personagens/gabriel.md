# Personagens — Gabriel (Funcionamento do Jogador)

Este documento descreve como o personagem controlado pelo jogador funciona em termos de mecânica, estados e sistemas.

---

## 1. Identificação Básica

- **Nome:** Gabriel *(decisão registrada em `docs/decisoes.md`)*
- **Tipo:** Protagonista / Personagem Controlável pelo Jogador
- **Origem Temporal:** Madrugada de 2026 (puxado da Biblioteca pela fenda temporal)
- **Papel:** Estudante que acorda em 3026 após a explosão da Âncora. Precisa investigar o campus e fechar a fenda antes que ela engula o passado e sua própria época.

---

## 2. Estados de Movimentação (FSM do Jogador)

O script do jogador opera sob uma máquina de estados finita:

| Estado | Velocidade | Emissão de Ruído Acústico | Consumo de Estamina | Descrição |
|---|---|---|---|---|
| **PARADO** | 0 px/s | Nula | Regeneração rápida | Em repouso. |
| **ANDANDO** | Padrão (100%) | Baixo (mesma sala) | Nulo | Movimento padrão de exploração. |
| **CORRENDO** | Rápido (180%) | **Alto** (propaga no grafo) | Alto (~4s contínuos) | Fuga rápida; alerta robôs próximos. |
| **ESCONDIDO** | 0 px/s | Condicionado ao microgame | Nulo | Dentro de armário ou cabine. |
| **EXAUSTO** | Lento (40%) | Respiração ofegante | Nulo (bloqueio temporário) | Ocorre quando a estamina se esgota totalmente. |

---

## 3. Gestão de Inventário e Ferramentas

O jogador interage com o ambiente através de itens específicos:

- **Lanterna (a pilha):**
  - Liga e desliga com a tecla do espaço de gadget. O feixe aponta para onde ele anda.
  - Ilumina à frente, mas os robôs enxergam o Gabriel de mais longe com ela acesa. A bateria acaba (4 min) e é trocada com pilhas achadas no mapa. Ver [`../mecanicas/iluminacao_e_lanterna.md`](../mecanicas/iluminacao_e_lanterna.md).
- **Vida:** 3 corações; toque de robô tira 1. Ver [`../mecanicas/vida_e_checkpoint.md`](../mecanicas/vida_e_checkpoint.md).
- **Cápsulas de Clarão:**
  - Item consumível de defesa (máximo 2 unidades).
  - Provoca sobrecarga e atordoa temporariamente robôs próximos para permitir fuga.
- **Objetos de Arremesso (Pedras/Entulho):**
  - Geram distração acústica em salas distantes via propagação BFS.
- **Caderno de Anotações:**
  - Registra pistas, bilhetes deixados pelos antecessores e detalhes descobertos.

---

## 4. Integração Técnica

- **Cena:** `cenas/personagens/gabriel.tscn`
- **Script:** `scripts/personagens/gabriel.gd`
- **Assets de Arte:** `assets/sprites/personagens/gabriel/` e `assets/modelagem/personagens/gabriel.blend`
