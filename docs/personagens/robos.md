# Personagens — Funcionamento dos Robôs (Inimigos de IA)

Este documento descreve como a inteligência artificial e os tipos mecânicos de robôs que patrulham o campus em 3026 funcionam no sistema do jogo.

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
   - **Sensor Fotossensível:** Detecta feixes de luz do pote de fungos do jogador a distâncias maiores em áreas escuras.

---

## 2. Tipos de Comportamento dos Robôs Planejados

Os robôs inimigos são categorizados pelo seu sentido ou padrão de comportamento predominante:

| Tipo de Robô | Sensor Dominante | Comportamento Principal | Ponto Fraco / Resposta do Jogador |
|---|---|---|---|
| **Sensor Acústico** | Audição apurada | Detecta passos correndo e ruídos de impacto a múltiplas salas de distância | Mover-se agachado; distrair com arremesso de pedras |
| **Patrulha Programada** | Rotina de circuito | Percorre salas e corredores em horários e rotas fixas pelo grafo | Mapear os horários de patrulha para planejar rotas seguras |
| **Sentinela Fotossensível** | Varredura óptica de luz | Patrulha áreas abertas e detecta lanternas acesas a longa distância | Tampar/apagar o pote de fungos ao cruzar seu campo visual |
| **Unidades de Enxame** | Proximidade em grupo | Movem-se em conjunto, bloqueando passagens e corredores estreitos | Uso de cápsula de clarão para dispersar temporariamente o grupo |
| **Perseguidor Persistente** | Rastreamento contínuo | Persegue o jogador por múltiplos cômodos via $A^*$ sem desistir facilmente | Microgames de esconderijo e controle de respiração até o robô passar |
