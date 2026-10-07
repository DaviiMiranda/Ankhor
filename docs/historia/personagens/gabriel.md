# Gabriel Magalhães (2026), o protagonista

> **Status:** Em desenvolvimento. Jogável.
> **Lei do projeto:** história, personalidade e arco estão no [Enredo Principal](../enredo_principal.md), seção 4.3 ("Gabriel Magalhães"), e a família na seção 5. Esta ficha descreve como o personagem controlado pelo jogador funciona: mecânica, estados e sistemas.

---

## 1. Identificação Básica

- **Nome:** Gabriel Magalhães
- **Tipo:** Protagonista / Personagem Controlável pelo Jogador
- **Origem Temporal:** Madrugada de 2026. Pegou no sono na Biblioteca e foi puxado pela fenda. É o penúltimo a chegar a 3026.
- **Em uma frase:** um estudante comum que prefere observar a agir, até não ter mais escolha. Irônico, de ironia seca.
- **Papel:** Estudante que acorda em 3026. Precisa fugir dos robôs da IA, encontrar os outros que caíram na fenda, descobrir o que aconteceu e consertar a Âncora para que todos voltem às suas épocas. A parte dele para o conserto é o **caderno**, com as equações da cadeira.

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
  - Ilumina à frente, mas os robôs enxergam o Gabriel de mais longe com ela acesa. A bateria acaba (4 min) e é trocada com pilhas achadas no mapa. Ver [`../../mecanicas/iluminacao_e_lanterna.md`](../../mecanicas/iluminacao_e_lanterna.md).
- **Vida:** 3 corações; toque de robô tira 1. Ver [`../../mecanicas/vida_e_checkpoint.md`](../../mecanicas/vida_e_checkpoint.md).
- **Cápsulas de Clarão:**
  - Item consumível de defesa (máximo 2 unidades).
  - Provoca sobrecarga e atordoa temporariamente robôs próximos para permitir fuga.
- **Objetos de Arremesso (Pedras/Entulho):**
  - Geram distração acústica em salas distantes via propagação BFS.
- **Caderno de Anotações:**
  - Registra pistas, bilhetes deixados pelos outros personagens e detalhes descobertos.
- **Anel da avó:**
  - Anel desgastado que está no inventário desde o começo, sem função aparente. No meio do jogo, o jogador o compara com o anel do Baltazar e descobre o parentesco (Enredo Principal, seção 5). Ainda não implementado.

---

## 4. Integração Técnica

- **Cena:** `cenas/personagens/gabriel.tscn`
- **Script:** `scripts/personagens/gabriel.gd`
- **Assets de Arte:** `assets/sprites/personagens/gabriel/` e `assets/modelagem/personagens/gabriel.blend`
