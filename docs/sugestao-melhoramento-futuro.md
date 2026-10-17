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

- [ ] **Tela especial ao pegar um item pela primeira vez (como em *Resident Evil*):**
  - Na **primeira vez** que o jogador pega um tipo de item, o jogo pausa e abre uma tela só para ele: o item **grande, no centro**, com o **nome** e uma **descrição** curta. Um botão (`E`) fecha e volta ao jogo.
  - Nas vezes seguintes, o mesmo item aparece só com o aviso de hoje ("Você pegou: ...").
  - **Hoje:** ao pegar, aparece só a mensagem no HUD, e a descrição fica no inventário (ver [`mecanicas/itens_e_inventario.md`](mecanicas/itens_e_inventario.md)). A tela nova reaproveita o `nome` e a `descricao` que cada item já tem em `dados/itens/`.
  - **Toque de computação gráfica:** o item pode **girar devagar** na tela, com os quadros renderizados do modelo 3D pelo mesmo pipeline do Blender dos personagens. Bom exemplo para a apresentação da disciplina.
  - **Depende de:** uma imagem grande de cada item, além do ícone do inventário, e de guardar quais itens o jogador já viu (no save).

- [ ] **Mapa de fase colecionável e rastreador de completude:**
  - Cada fase principal (Biblioteca, Bloco de Salas, Centro de Convivência, Labirinto, D-Tec, Bunker) pode conter um **mapa esquemático ou planta baixa** escondido pelo cenário, para ser encontrado como um **item coletável** (ex.: planta da biblioteca num quadro de avisos, mapa de evacuação no bloco de salas, guia do campus no centro de convivência).
  - **Visualização:** ao ser achado, o mapa pode ser aberto e consultado a qualquer momento (pela mochila/caderno ou por uma tecla de atalho dedicada, como `M`). A interface exibe a planta no estilo do jogo (papel técnico desgastado ou esquema digital em pixel art).
  - **Indicadores de exploração e completude:**
    - **Salas visitadas:** mostra o desenho das salas já exploradas e conexões descobertas vs. áreas ainda não visitadas (reveladas conforme o jogador explora ou já desenhadas com demarcação do que foi visitado).
    - **Itens e colecionáveis da fase:** exibe um resumo da completude da fase (ex.: quantos itens-chave, documentos/anotações e colecionáveis/easter eggs foram encontrados do total da fase).
    - **Status da fase:** indica se a fase foi 100% concluída/explorada ou se ainda restam segredos e itens pendentes para trás.
  - **Toque de computação gráfica / computação:** conexão direta com o modelo do campus como grafo (GDD 2.4). O mapa pode destacar os nós (salas) e arestas (portas/corredores) já percorridos, calculando o percentual de cobertura do grafo da fase em tempo real.
  - **Depende de:** arte das plantas/telas de mapa de cada fase, registro de itens/salas coletados por fase no estado do jogo e persistência no sistema de save.

- [ ] **Sala Segura (*Safe Room*), salvamento em arquivo e retorno a fases anteriores:**
  - Criação de uma **sala segura dedicada por fase** (ex.: sala dos servidores na Biblioteca, sala dos professores no Bloco de Salas, depósito isolado no Centro de Convivência, oficina do Zane no Labirinto).
  - **Zona livre de perigo:** robôs não conseguem entrar ou perdem a perseguição na porta. A sala possui iluminação estável, tranca funcional e música ambiente característica de calma/alívio (estilo clássico de *survival horror*).
  - **Ponto de salvamento permanente:** além dos checkpoints voláteis espalhados pela fase (postos de emergência), a Safe Room contém o ponto para salvar o jogo em arquivo definitivo (mecânica de dormir/descansar ou terminal de registro), garantindo a persistência do progresso entre sessões de jogo.
  - **Retorno a fases anteriores (*Backtracking* interligado):**
    - A sala segura funciona como ponto de conexão ou rota de atalho para transitar de volta para fases já exploradas.
    - Permite revisitar setores anteriores com novos itens, ferramentas e senhas obtidas mais adiante, viabilizando abrir portas trancadas, resgatar colecionáveis/relíquias deixados para trás e buscar 100% de exploração no mapa de cada fase.
  - **Toque de computação gráfica / computação:** uso da estrutura de grafos do campus (GDD 2.4) para modelar as conexões bidirecionais entre os nós de salas seguras, aplicando busca em largura (BFS) ou Dijkstra para calcular e validar atalhos acessíveis e garantir que rotas de retorno não quebrem o fluxo da história.
  - **Depende de:** sistema de persistência/savegame em disco, portas de transição inter-fases nas salas seguras e trilha/efeitos sonoros de alívio dedicados.

## Conteúdo extra

- [ ] **Easter eggs colecionáveis que dão conquistas:**
  - Objetos escondidos pelo campus, fora do caminho principal, que o jogador pode achar e guardar. Cada um (ou cada conjunto) **desbloqueia uma conquista**.
  - **Nunca são obrigatórios:** não abrem portas nem ajudam a avançar. São recompensa para quem explora.
  - **Sugestões de objetos** (precisam seguir o [Enredo Principal](historia/enredo_principal.md)): relíquias de cada época dos personagens, como uma moeda colonial (Baltazar), um disquete com adesivo (Clarice), um crachá da Unifor de 2026 (Gabriel) e um chip de 2123 (Zane); e fitas cassete e pôsteres dos anos 80, a obsessão do Carlos, espalhados perto do D-Tec.
  - **Onde aparecem:** numa tela de conquistas no menu principal (existe uma branch `feat/menu-conquistas` criada para isso, mas até agora os commits dela são só do fundo do menu) e, ao achar o objeto, um aviso curto no HUD, como o das anotações.
  - **Depende de:** sistema de save, para as conquistas continuarem desbloqueadas entre uma partida e outra.
