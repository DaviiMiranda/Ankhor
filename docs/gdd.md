# GDD — respostas dos itens 1 a 4

> **Título do Jogo:** Ankhor  
> **Hierarquia:** Para **história, mundo e personagens**, a lei do projeto é o [Enredo Principal](historia/enredo_principal.md): se este GDD contradizer o Enredo, vale o Enredo. Para decisões recentes de design e técnica, consulte [`decisoes.md`](decisoes.md). Para a documentação técnica aprofundada, consulte o índice mestre em [`README.md`](README.md).

> [!TIP]
> **Documentação Modular Detalhada:**
> - 🎯 **[Visão Geral e Pilares](visao_geral/conceito.md)** | **[Estilo Artístico 2.5D](visao_geral/estilo_artistico.md)**
> - ⚙️ **[Mecânicas e Core Loop](mecanicas/README.md)** | **[Furtividade](mecanicas/furtividade_e_esconderijos.md)** | **[Iluminação](mecanicas/iluminacao_e_lanterna.md)** | **[Vida e Checkpoint](mecanicas/vida_e_checkpoint.md)** | **[Sono e Sonhos](mecanicas/sono_e_sonhos.md)**
> - 💻 **[Conceitos de Computação](computacao/README.md)** (Grafos, Coloração, BFS, A*, Markov, Shaders)
> - 📜 **[Enredo Principal](historia/enredo_principal.md)** | **[Índice da História](historia/README.md)** | **[Modelo de Documento](historia/template_documento.md)**
> - 👥 **[Personagens](historia/personagens/)** ([Gabriel](historia/personagens/gabriel.md), [Robôs](historia/personagens/robos.md), [Modelo de ficha](historia/template_personagem.md))
> - 🗺️ **[Design de Fases](fases/README.md)** | **[Template de Fase](fases/template_fase.md)**
> - 💬 **[Sistema de Diálogos](dialogos/README.md)** | **[Template de Diálogo](dialogos/template_dialogo.md)**

*Versão com o protagonista acordando mil anos no futuro. Os lugares da Unifor são usados apenas como cenário; pessoas, pesquisa e acontecimentos são fictícios.*

---

## 1. Visão Geral

**Gênero:** terror atmosférico e sobrevivência, com exploração, investigação e furtividade. Fugir e se esconder é a regra; defender-se é a exceção.

**Plataforma(s):** PC (Windows).

**Público-alvo:** adolescentes e adultos, a partir de 14 anos. Terror de tensão, sem violência explícita. Pensado primeiro para quem conhece a Unifor: alunos e ex-alunos reconhecem cada prédio, mesmo em ruínas.

**Resumo do Conceito:** Gabriel Magalhães, estudante de 2026, pega no sono na Biblioteca da Unifor e acorda mil anos no futuro, no ano de 3026. A humanidade abandonou a Terra e uma IA dominou o planeta. No antigo centro de pesquisa da Unifor, uma máquina abandonada, a **Âncora**, falhou e abriu uma fenda no tempo no chão da Biblioteca, que por acaso puxou, com dias de diferença, jovens de épocas diferentes. Gabriel precisa encontrá-los, fugir dos robôs da IA, descobrir o que aconteceu e achar um jeito de todos voltarem. A primeira fase do jogo é a Biblioteca. A história completa está no [Enredo Principal](historia/enredo_principal.md).

O que torna o jogo diferente:
- **Estranhamento do familiar:** o jogador reconhece a catraca, o bebedouro, o quadro, a Biblioteca. O mundo em volta não reconhece mais nada disso.
- **Os perseguidores seguem a grade horária** da semana de provas, mil anos depois. Quem descobre a grade sabe onde cada um vai estar.
- **Dormir é salvar e é voltar ao passado.** Cada sono leva o protagonista, em sonho, à última semana antes de tudo — e é só lá que ele aprende a grade, as senhas e a verdade.

**Visão Artística:** pixel art em vista lateral 2.5D, com camadas de profundidade, no estilo de *Five Nights at Freddy's: Into the Pit*. O jogo retrata a Unifor mil anos no futuro como uma ruína tomada pela natureza: concreto rachado e desabado, árvores crescendo dentro das salas, areia de dunas cobrindo corredores, e objetos do cotidiano de hoje transformados em relíquias. A atmosfera é de mistério, solidão e estranhamento — um terror silencioso, mais de tensão do que de susto, em que o maior choque é perceber quanto tempo passou. Luz natural filtrada pela vegetação contrasta com interiores escuros iluminados só por luzes de emergência que piscam e pela lanterna. Nos sonhos, o mesmo campus aparece cheio, iluminado e normal.

---

## 2. Mecânicas de Jogo

### Jogabilidade Central

O jogador explora as ruínas em vista lateral, sala por sala e prédio por prédio, procurando passagens, itens e pistas, enquanto evita os **robôs** que patrulham o campus.

**Explorar.** Andar, correr (faz barulho), se espremer por frestas, atravessar tetos desabados, vasculhar o que restou, examinar objetos e marcas nas paredes.

**Iluminar.** Quase nada elétrico funciona: só as luzes de emergência do centro de pesquisa. O protagonista usa uma **lanterna a pilha**. Luz ajuda a ver e ajuda a ser visto (os robôs enxergam mais longe), e a bateria acaba: é preciso achar pilhas.

**Rondas e rotinas.** Cada robô cumpre sua rotina de patrulha programada pelo campus. Fora da rotina, quando ouve ou vê o protagonista, o robô sai do protocolo padrão e caça.

**Esconder-se.** Armários enferrujados, buracos no piso, raízes, cabines de estudo. Com um robô por perto, o jogador passa por um **microgame** rápido e diferente em cada esconderijo: prender a respiração no tempo certo, segurar a porta, ficar imóvel.

**Distrair.** Jogar pedras e objetos, derrubar estantes, fazer ruído num lugar para atrair os robôs para longe.

**Defender-se (limitado).** Disparar uma **cápsula de clarão** (um flash descartável) libera um clarão forte por um instante e atordoa o robô por alguns segundos. As cápsulas são escassas — é para escapar, não para vencer.

**Dormir.** Em salas seguras e fechadas, o jogador pode dormir. Dormir **salva o jogo** e leva a um **sonho**: o mesmo lugar no passado antes de tudo. Nos sonhos não há perigo — há conversas, detalhes e senhas que servem no presente.

### Objetivos e Progressão

> ⚠️ **A definir com a nova premissa** (fenda da Âncora, 3026 — `docs/decisoes.md`, 2026-09-26). O texto abaixo é da premissa antiga (Insones e semana de provas) e fica como referência até o grupo decidir.

**Objetivo geral:** descobrir o que aconteceu, por que ele dormiu mil anos, e sair do campus.

**Estrutura em cinco dias**, um para cada dia da semana de provas que os Insones continuam repetindo. Cada dia abre uma nova área e fica mais perigoso: mais Insones ativos, rotinas mais agressivas, menos recursos.

| Dia | Área principal | O que se descobre |
|---|---|---|
| Segunda | Biblioteca | Ele dormiu muito. As pessoas ainda estão aqui — ou o que sobrou delas. |
| Terça | Blocos de aula | Os Insones seguem a grade da semana de provas. Os tracinhos contados nas paredes indicam séculos. |
| Quarta | Centro de Convivência e Espaço Cultural | Havia uma pesquisa com voluntários naquela semana. |
| Quinta | NAMI | O estimulante, os testes, a lista de voluntários — e o nome dele nela. |
| Sexta | Reitoria e portão principal | Quanto tempo passou de verdade, e o que aconteceu com o mundo lá fora. |

A progressão entre áreas é por **passagens abertas, mecanismos e senhas**, parte encontrada nas ruínas e parte aprendida nos sonhos.

### Sistema de Recompensas

- **Acesso:** novas áreas do campus e atalhos entre elas.
- **Recursos:** pilhas para a lanterna e cápsulas de clarão, sempre escassos.
- **Verdade:** cada pista, marca na parede e sonho revela uma parte do mistério. A história é a principal recompensa.
- **Colecionáveis:** relíquias do cotidiano (um crachá, um celular fossilizado, uma caneca da cantina) com a descrição de quem eram seus donos, e páginas do diário que o protagonista vai escrevendo.
- **Final:** o que o jogador descobriu muda as opções disponíveis no final.

### OBRIGATÓRIO — recursos de Computação

Os conteúdos de computação estão **dentro das mecânicas**, não só no código:

| Conteúdo | Onde aparece no jogo |
|---|---|
| **Grafos** | O campus é um grafo: cada sala é um nó, cada porta, corredor, escada ou buraco no teto é uma aresta com peso (distância e barulho). Desabamentos removem arestas; passagens abertas pelo jogador criam novas. |
| **Coloração de grafos** | ⚠️ _A definir com a nova premissa:_ antes, a grade horária da semana de provas era gerada por coloração de grafos: aulas que dividem professor ou sala não podem ter o mesmo horário. Essa grade definia onde cada Insone estava a cada hora. Com os robôs em patrulha programada (`docs/historia/personagens/robos.md`), falta decidir de onde vem a grade. |
| **Busca em largura (BFS)** | O som se propaga pelo grafo e enfraquece a cada sala. Um passo correndo é ouvido a duas salas; uma estante caindo, a cinco. |
| **A\* (caminho mínimo)** | Quando um robô ouve ou vê o jogador, sai da rotina e o persegue pelo menor caminho no grafo. |
| **Cadeia de Markov** | Fora da rotina, cada robô escolhe a próxima sala por probabilidade, com chances que crescem a cada dia. É o modelo de movimento dos perseguidores do FNAF, formalizado. |
| **Máquina de estados** | Cada robô alterna entre *rotina*, *investigando*, *perseguindo*, *atordoado* e *retornando* (`docs/historia/personagens/robos.md`). |
| **Estruturas de dados** | Inventário em grade (matriz), fila de eventos da rotina de cada robô, dicionário de flags do mundo (passagens abertas, pistas encontradas, sonhos vistos). |
| **Matemática / geometria** | Campo de visão dos robôs por produto escalar e linha de visão por *ray casting*; luz da lanterna em cone (a mesma conta do produto escalar) e decaindo com a bateria. |

---

## 3. Mundo e Narrativa

### Cenário

O campus da **Unifor**, em Fortaleza, **mil anos no futuro**. Os prédios que sobraram estão rachados, sem teto ou parcialmente enterrados; árvores atravessam salas de aula; dunas avançaram sobre os caminhos entre os blocos; o mato cobre o que era estacionamento. Não há cidade em volta — só vegetação até onde a vista alcança. O que resiste são as coisas duras: concreto, metal, vidro, pedra.

E, nos sonhos, o mesmo campus **na última semana antes de tudo**: cheio, iluminado, barulhento e normal.

### História e Personagens

> A história, o mundo e os personagens estão no **[Enredo Principal](historia/enredo_principal.md)**, que é a lei do projeto. Aqui fica só o resumo.

- **O mundo:** em 3026 a humanidade abandonou a Terra e uma IA sem rosto dominou. Os robôs da IA veem humanos como invasores e caçam.
- **A Âncora e a fenda:** a Âncora é só uma máquina, abandonada no centro de pesquisa da Unifor. Ela falhou e abriu uma fenda no chão da Biblioteca, que pulsa e, por acaso, puxa quem estiver ali em alguma época.
- **Os personagens:** jovens de cerca de 20 anos, todos vivos, puxados com dias de diferença: Baltazar Magalhães (~1750, antepassado de Gabriel), Diana (1978), Clarice (1994), Rafael (2008), Henrique (pesquisador, 2019), **Gabriel Magalhães** (2026, o protagonista, penúltimo a chegar) e Zane (2123, o último).
- **O objetivo:** encontrar os outros, descobrir o que aconteceu e consertar a Âncora para que todos voltem às suas épocas.
- **A primeira fase** é a **Biblioteca**.

---

## 4. Níveis e Ambientes

> O detalhamento de cada fase (salas, puzzles, sonhos) fica em [`fases.md`](fases.md).

### Estrutura dos Níveis

> ⚠️ **A definir com a nova premissa** (fenda da Âncora, 3026 — `docs/decisoes.md`, 2026-09-26). O texto abaixo é da premissa antiga (Insones e semana de provas) e fica como referência até o grupo decidir.

Um campus contínuo, dividido em **cinco áreas** ligadas entre si, uma aberta a cada dia. As áreas visitadas continuam acessíveis — voltar faz parte do jogo, e cada volta encontra os Insones num horário diferente da grade.

As áreas externas entre prédios são as mais expostas: abertas, com dunas e mato alto, poucos esconderijos, e a rota do Vigia. Em vários pontos, o caminho entre dois prédios não é mais pelo chão: é por um teto desabado, uma árvore caída ou um andar enterrado.

### Design dos Ambientes

> ⚠️ **A definir com a nova premissa** (fenda da Âncora, 3026 — `docs/decisoes.md`, 2026-09-26). A coluna "Função" ainda cita a premissa antiga (a Bibliotecária, o Professor e os Calouros, que eram Insones, e o projeto VIGÍLIA-7) e fica como referência até o grupo decidir.

| Área | Visual | Função |
|---|---|---|
| **Biblioteca** | Estantes caídas e vazias, uma árvore no meio do salão, luz do sol por um teto aberto, poeira e pólen no ar | Tutorial e primeiro contato. Silêncio é regra: correr aqui chama a Bibliotecária. |
| **Blocos de aula** | Corredores parcialmente enterrados em areia, salas sem teto, quadros ainda presos às paredes, paredes cobertas de tracinhos | Onde a grade mais importa: o Professor muda de sala a cada horário. |
| **Centro de Convivência** | Estrutura aberta tomada pelo mato, balcões e mesas cobertos de raízes, o céu aparecendo pela cobertura | Área ampla, poucos esconderijos, os Calouros andam em grupo. |
| **Espaço Cultural** | Galeria escura e fechada, obras irreconhecíveis, só as luzes de emergência piscando | Puzzles visuais e as primeiras peças do projeto VIGÍLIA-7. |
| **NAMI** | Corredores de azulejo rachado, macas de metal, o andar de baixo alagado, as luzes de emergência como única iluminação | O ponto alto da tensão e das revelações. |
| **Reitoria e portão** | O prédio mais conservado, com o cofre e os arquivos; do lado de fora do portão, só vegetação | O final. |

### Desafios e Obstáculos

- **Os robôs**, cada tipo com seu sensor dominante (som, visão, luz) e padrão de patrulha (`docs/historia/personagens/robos.md`).
- **Barulho:** correr, pisar em entulho e derrubar coisas se ouve pelo grafo.
- **Escuridão:** a lanterna ajuda a ver e ajuda a ser visto; a bateria acaba.
- **Recursos escassos:** pilhas e cápsulas de clarão nunca sobram.
- **O próprio lugar:** pisos que cedem, passagens enterradas, andares alagados, caminhos que só existem por cima.
- **O tempo da grade:** a mesma sala é segura num horário e perigosa no seguinte, e o jogador só conhece a grade pelo que viu nos sonhos.
