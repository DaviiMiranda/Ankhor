# Gabriel Magalhães (2026), o protagonista

> **Status:** Em desenvolvimento. Jogável.
> **Lei do projeto:** esta ficha faz parte do [Enredo Principal](../enredo_principal.md) e tem a mesma autoridade: quem o Gabriel é vale como está escrito aqui. A história em volta dele (o acidente, a ordem dos acontecimentos, as pendências) está no Enredo.

---

## 1. Quem é

- **Época de origem:** 2026.
- **Quem é:** estudante da Unifor, com cerca de 20 anos. A família Magalhães vive na região há séculos, mas ele não sabe.
- **História:** dormiu na Biblioteca de madrugada, com o caderno de equações da cadeira aberto na mesa. Acorda em 3026, na cabine de estudo onde pegou no sono, sem saber o que aconteceu. Não é um herói: precisa entender o campus, evitar os robôs e achar os outros. Na mochila carrega um **anel desgastado** que a avó deu para ele. É o **penúltimo** a chegar a 3026.

## 2. Personalidade

- **Essência:** um estudante comum que prefere observar a agir, até não ter mais escolha.
- **Traços:** observador, reservado, curioso e **irônico**. A ironia seca é o jeito dele de lidar com o absurdo. Mais ouvinte que falante, o que ajuda o jogador a se colocar no lugar dele.
- **Como fala:** frases curtas, informal e atual, com ironia seca e sem rir da própria piada. Comenta o absurdo como se fosse normal ("Ótimo. Mil anos de atraso pra aula."). É essa ironia que faz ele se dar bem com a Clarice: os dois se provocam no mesmo tom.
- **O que quer:** voltar para casa. Depois, que todos voltem.
- **O que teme:** não fazer diferença, ser só mais um.
- **Defeito:** foge de conflito e adia decisões.
- **Arco:** de quem só sobrevive a quem une o grupo. Descobrir que é Magalhães, ligado àquele chão há séculos, faz ele sentir que tem um lugar na história.

## 3. Relações

| Com | Dinâmica |
|---|---|
| [Baltazar](baltazar.md) | Família descoberta. Gabriel conta ao Baltazar que é descendente dele |
| [Clarice](clarice.md) | Duelo de ironias: os dois se provocam o tempo todo no mesmo tom, e é assim que a relação cresce ao longo do jogo |
| [Zane](zane.md) | Gabriel deixa de ser o novato e vira o veterano que explica tudo |

## 4. No jogo

- **Papel:** fugir dos robôs da IA, encontrar os outros que caíram na fenda, descobrir o que aconteceu e consertar a Âncora para que todos voltem às suas épocas.
- **Parte para consertar a Âncora:** o **caderno**, com as equações da cadeira.

### 4.1 Estados de movimentação (máquina de estados do jogador)

| Estado | Velocidade | Emissão de Ruído Acústico | Consumo de Estamina | Descrição |
|---|---|---|---|---|
| **PARADO** | 0 px/s | Nula | Regeneração rápida | Em repouso. |
| **ANDANDO** | Padrão (100%) | Baixo (mesma sala) | Nulo | Movimento padrão de exploração. |
| **CORRENDO** | Rápido (180%) | **Alto** (propaga no grafo) | Alto (~4s contínuos) | Fuga rápida; alerta robôs próximos. |
| **ESCONDIDO** | 0 px/s | Condicionado ao microgame | Nulo | Dentro de armário ou cabine. |
| **EXAUSTO** | Lento (40%) | Respiração ofegante | Nulo (bloqueio temporário) | Ocorre quando a estamina se esgota totalmente. |

### 4.2 Inventário e ferramentas

- **Lanterna (a pilha):** liga e desliga com a tecla do espaço de gadget. O feixe aponta para onde ele anda. Ilumina à frente, mas os robôs enxergam o Gabriel de mais longe com ela acesa. A bateria acaba (4 min) e é trocada com pilhas achadas no mapa. Ver [`../../mecanicas/iluminacao_e_lanterna.md`](../../mecanicas/iluminacao_e_lanterna.md).
- **Vida:** 3 corações; toque de robô tira 1. Ver [`../../mecanicas/vida_e_checkpoint.md`](../../mecanicas/vida_e_checkpoint.md).
- **Cápsulas de clarão:** consumível de defesa (máximo 2). Atordoa por um tempo os robôs próximos, para permitir a fuga.
- **Objetos de arremesso (pedras, entulho):** distração acústica em salas distantes, propagada pelo grafo com BFS.
- **Caderno de anotações:** registra pistas, bilhetes deixados pelos outros personagens e detalhes descobertos.
- **Anel da avó:** anel desgastado que está no inventário desde o começo, sem função aparente. No meio do jogo, o jogador o compara com o anel do Baltazar e descobre o parentesco (Enredo Principal, seção 5). Ainda não implementado.

## 5. Registros

- **Suporte:** folha quadriculada de caderno de faculdade, com espiral (`papel = caderno_gabriel`).

## 6. Direção de arte

- **Cor de identificação:** vermelho, o oposto do verde-azulado da Clarice.
- Sprites em resolução dobrada (ver `CLAUDE.md`).

## 7. Arquivos

- **Cena:** `cenas/personagens/gabriel.tscn`
- **Script:** `scripts/personagens/gabriel.gd`
- **Arte:** `assets/sprites/personagens/gabriel/` e `assets/modelagem/personagens/gabriel.blend`

## 8. Pendências

- Gabriel falhando na tela enquanto o Baltazar estiver fora de 1750 (Enredo Principal, seção 12.3).
- O final dele com a Clarice (seção 12.1).
