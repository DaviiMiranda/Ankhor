# Mecânicas — Furtividade e Esconderijos

## 1. Esconderijos no Cenário

Quando um robô está patrulhando ou perseguindo Gabriel, a principal forma de quebrar a linha de visão é entrar em um esconderijo interativo pressionando `E`:

| Esconderijo | Ocorrência Típica | Microgame Associado | Nível de Segurança |
|---|---|---|---|
| **Armário Metálico de Vestiário** | Blocos de Aula e Laboratórios | Segurar a porta contra a vibração | Alto |
| **Cabine Individual de Estudo** | Biblioteca Central | Prender a respiração no timing correto | Médio (visível se tiver frestas) |
| **Raízes Caídas e Mesas Quebradas** | Pátios e Convivência | Ficar imóvel (manter tecla pressionada) | Médio |
| **Macas com Cortinas Desfiadas** | Enfermarias e Clínicas | Controle de batimento cardíaco / respiração | Médio-Alto |
| **Nicho de parede** (bebedouro ou armários) | Corredores do Bloco de salas | Ficar imóvel, sem `E`: parado no nicho com a lanterna apagada | Médio (contato ainda denuncia) |

**Já no jogo:** a cabine de estudo da Biblioteca, com o microgame de respiração (2026-11-04, [`mecanicas_de_fase.md`](mecanicas_de_fase.md), seção 2). O nicho de parede (2026-10-12). Ficar parado por 0,4 s dentro dele, com a lanterna apagada, esconde o Gabriel da visão dos robôs; andar ou acender a luz revela. Ver `docs/fases/bloco_de_salas.md`, seção 12.8. O Bunker usa o vão do posto de máscaras de gás (`bunker_nicho`, ver `docs/fases/bunker.md`), e o Laboratório usa o mesmo esconderijo com outra peça de parede, o vão da estação de emergência (`dtec_nicho`, ver `docs/fases/dtec.md`).

---

## 2. Microgames de Tensão (*Into the Pit Style*)

Ficar dentro de um esconderijo não é garantia passiva de imunidade. Se um robô se aproximar da mesma sala ou passar em frente ao esconderijo, um **microgame de tensão rápida** é acionado:

### A. Prender a Respiração (*Timing Bar*)
- Uma barra oscilante surge na tela com uma pequena zona segura verde.
- O jogador precisa pressionar a tecla `Espaço` no compasso correto para que Gabriel contenha a respiração ofegante.
- Falhar em três pulsos faz Gabriel soltar um engasgo audível, denunciando o esconderijo.

### B. Segurar a Porta (*Tensão Mecânica*)
- A porta enferrujada do armário tende a ranger e se abrir pela ação do vento ou vibração dos passos pesados do robô.
- O jogador deve manter a tecla de ação pressionada com força contínua, ajustando a pressão conforme os solavancos.

### C. Imobilidade Absoluta (*Dead Silence*)
- Requer não tocar em nenhum controle de direção ou ação durante a passagem do perseguidor por um período de 3 a 5 segundos.

### D. Respiração Contida (no jogo desde 2026-11-06, com o Ciborgue do bunker)
- **Quando:** só com o Gabriel **escondido** (parado num nicho, com a lanterna apagada) e o **Ciborgue** parado do lado de fora, a até 56 px. Fora do esconderijo não há minijogo: ele simplesmente pega o Gabriel.
- **A barra:** acima da cabeça do Gabriel, com uma faixa verde no meio e um marcador. À esquerda é prender o ar demais; à direita, respirar alto (ofegante).
- **O controle:** **segure `E`** para prender o ar (o marcador vai para a esquerda) e **solte** para respirar (vai para a direita). Sozinho, ele sobe, porque o Gabriel está ofegante; e balança um pouco, para não dar para achar um ritmo fixo. A tecla `E` não aciona nada perto do nicho enquanto o minijogo está aberto.
- **O ruído:** fora do verde, uma segunda barra vermelha, embaixo, enche; dentro, ela esvazia. Cheia, o Gabriel engasga (tosse), o Ciborgue ouve, tira o Gabriel do esconderijo e o ataca.
- **A ansiedade e o cansaço pesam:** com ansiedade alta, a faixa verde fica mais estreita e a respiração sobe mais rápido; cansado, a faixa encolhe mais 20%.
- **Aguentar:** o Ciborgue espera de 7 a 11 s e vai embora. O minijogo termina quando ele se afasta.
- **Números** (`scripts/sistemas/respiracao_contida.gd`, no Inspetor da cena `respiracao_contida.tscn`):

| | Calmo | Ansioso |
|---|---|---|
| Largura da faixa verde | 40% | 26% |
| Subida sem apertar | 0,12 / s | 0,22 / s |
| Descida segurando `E` | 0,30 / s | 0,30 / s |

O balanço soma $0{,}15 \cdot \sin(2{,}1t)\,\sin(0{,}63t + 1)$ por segundo. O ruído enche 0,45 por segundo fora da faixa e esvazia 0,25 dentro: saindo do verde sem reagir, o Gabriel tem uns 2 a 3 s até engasgar.

---

## 3. Mecânica de Distração por Arremesso

Gabriel pode carregar pequenos fragmentos de concreto, pedras ou cacos de cerâmica recolhidos pelo chão:
- **Arremesso (Botão Direito do Mouse / `F`):** Uma linha pontilhada simples indica o arco parabólico de lançamento.
- **Impacto e Ruído:** Ao atingir uma parede ou piso distante, o objeto emite um estalo sonoro pontual.
- **Desvio de Rota:** O som ativa o algoritmo BFS nos nós do grafo: se o robô estiver dentro do raio de alcance de seus sensores acústicos, ele transita do estado *Rotina* para *Investigando*, movendo-se em direção ao ponto de impacto e liberando o caminho para Gabriel.
