# Os robôs (inimigos)

> **Lei do projeto:** esta ficha faz parte do [Enredo Principal](../enredo_principal.md) (que fala dos robôs nas seções 2.1 e 2.3) e descreve como eles funcionam no jogo.

## 0. Na história

- Os robôs são controlados pelo **Carlos**, o antagonista (ficha em [`carlos.md`](carlos.md)). Se existe também uma IA, e qual a relação dela com o Carlos, está pendente (Enredo Principal, seção 12.2).
- Caçam qualquer pessoa que encontram. Por que caçam (para capturar e levar ao Bloco M, ou para eliminar) está pendente.
- Patrulham o campus por **rotinas programadas** e repetem o mesmo caminho há séculos: dá para decorar.
- Se pegam Gabriel, é game over e o jogo volta ao último checkpoint.
- Não falam.

---

## 1. Arquitetura da Inteligência Artificial

Cada robô inimigo é controlado por um script derivado de uma classe base de IA (`RoboBase.gd` ou `InimigoBase.gd`), operando sob:

1. **Máquina de Estados Finita (FSM):**
   - **ROTINA:** Executa sua ronda ou protocolo de patrulha programado no grafo de salas.
   - **INVESTIGANDO:** Alerta disparado por emissão sonora no grafo (BFS) ou luz suspeita; move-se para o nó de origem da perturbação.
   - **PERSEGUINDO:** Linha de visão direta com o jogador confirmada via produto escalar e raycasting; persegue utilizando o algoritmo $A^*$.
   - **ATORDOADO:** Estado temporário (3 a 5 segundos) após sobrecarga provocada por uma cápsula de clarão.
   - **RETORNANDO:** Retorna à rota de patrulha programada após perder o contato com o jogador.

2. **Sensores de Percepção:**
   - **Sensor Acústico:** Conectado aos eventos sonoros emitidos no grafo do campus via BFS (passos correndo, colisões, pedras arremessadas).
   - **Sensor Óptico / Visual:** Cone angular calculado via produto escalar ($\vec{u} \cdot \vec{v}$) e verificação de oclusão física por raycasting 2D.
   - **Sensor Fotossensível:** Detecta o Gabriel a distâncias maiores quando a lanterna está acesa.

---

## 2. Tipos de Comportamento dos Robôs Planejados

Os robôs inimigos são categorizados pelo seu sentido ou padrão de comportamento predominante:

| Tipo de Robô | Sensor Dominante | Comportamento Principal | Ponto Fraco / Resposta do Jogador |
|---|---|---|---|
| **Sensor Acústico** | Audição apurada | Detecta passos correndo e ruídos de impacto a múltiplas salas de distância | Andar sem correr; distrair com arremesso de pedras |
| **Patrulha Programada** | Rotina de circuito | Percorre salas e corredores em horários e rotas fixas pelo grafo | Mapear os horários de patrulha para planejar rotas seguras |
| **Sentinela Fotossensível** | Varredura óptica de luz | Patrulha áreas abertas e detecta lanternas acesas a longa distância | Apagar a lanterna ao cruzar seu campo visual |
| **Unidades de Enxame** | Proximidade em grupo | Movem-se em conjunto, bloqueando passagens e corredores estreitos | Uso de cápsula de clarão para dispersar temporariamente o grupo |
| **Perseguidor Persistente** | Rastreamento contínuo | Persegue o jogador por múltiplos cômodos via $A^*$ sem desistir facilmente | Microgames de esconderijo e controle de respiração até o robô passar |

---

## 3. Robôs implementados (Labirinto)

Os dois primeiros tipos foram modelados no Blender (`assets/modelagem/personagens/gerar_robos.py`, mesmo pipeline do Gabriel) e têm IA completa. Os olhos são renderizados numa tira separada e desenhados **sem luz** no Godot: no escuro, o jogador vê os pontos vermelhos antes do robô.

| | **Sentinela** (tipo "Sentinela Fotossensível") | **Rastreador** (tipo "Sensor Acústico") |
|---|---|---|
| Visual | 2,1 m, magra, curvada para a frente, braços que quase arrastam no chão, garras de 3 dedos, cabeça-globo com **um olho** (a lente é o sensor óptico) | Quadrúpede de 0,8 m, corpo de placas e cabos, espinhos nas costas, **três olhos** e **antenas parabólicas** no lugar das orelhas |
| Sentido forte | Visão: cone de 60°, 170 px; farol vermelho mostra para onde olha | Audição ×1,8; visão curta e larga (80 px, 100°) |
| Velocidade | lenta (patrulha 18, perseguição 36 px/s) | rápida (24 / 50 px/s) |
| Som | pisada pesada de metal, zumbido, guincho | garras correndo no concreto, zumbido mais agudo, guincho |
| Cena | `cenas/personagens/robo_sentinela.tscn` | `cenas/personagens/robo_rastreador.tscn` |

Os dois usam o mesmo script (`scripts/personagens/robo.gd`); o que muda são os números no Inspetor. Um tipo novo = uma cena nova com outros números e outros sprites.

Sprites: `assets/sprites/personagens/robos/<robo>_andar_<lado|frente|costas>.png` (8 quadros) e `..._olhos.png`. Folha de referência: `robos_referencia.png`.

IA (máquina de estados, cone de visão, BFS, A\*, Markov): [`../../computacao/ia_e_perseguicao.md`](../../computacao/ia_e_perseguicao.md), seção 5.
