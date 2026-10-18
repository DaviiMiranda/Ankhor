# GDD — respostas dos itens 1 a 4

> **Título do Jogo:** Ankhor  
> **Hierarquia:** Para **história, mundo e personagens**, a lei do projeto é o [Enredo Principal](historia/História_Completa.md): se este GDD contradizer o Enredo, vale o Enredo. Para decisões recentes de design e técnica, consulte [`decisoes.md`](decisoes.md). Para a documentação técnica aprofundada, consulte o índice mestre em [`README.md`](README.md).

> [!TIP]
> **Documentação Modular Detalhada:**
> - 🎯 **[Visão Geral e Pilares](visao_geral/conceito.md)** | **[Estilo Artístico 2.5D](visao_geral/estilo_artistico.md)**
> - ⚙️ **[Mecânicas e Core Loop](mecanicas/README.md)** | **[Furtividade](mecanicas/furtividade_e_esconderijos.md)** | **[Iluminação](mecanicas/iluminacao_e_lanterna.md)** | **[Vida e Checkpoint](mecanicas/vida_e_checkpoint.md)** | **[Sono e Sonhos](mecanicas/sono_e_sonhos.md)**
> - 💻 **[Conceitos de Computação](computacao/README.md)** (Grafos, Coloração, BFS, A*, Markov, Shaders)
> - 📜 **[Enredo Principal](historia/História_Completa.md)** | **[Índice da História](historia/README.md)** | **[Modelo de Documento](historia/template_documento.md)**
> - 👥 **[Personagens](historia/personagens/)** ([Gabriel](historia/personagens/gabriel.md), [Robôs](historia/personagens/robos.md), [Modelo de ficha](historia/template_personagem.md))
> - 🗺️ **[Design de Fases](fases/README.md)** | **[Template de Fase](fases/template_fase.md)**
> - 💬 **[Sistema de Diálogos](dialogos/README.md)** | **[Template de Diálogo](dialogos/template_dialogo.md)**

*Versão com o protagonista acordando mil anos no futuro. Os lugares da Unifor são usados apenas como cenário; pessoas, pesquisa e acontecimentos são fictícios.*

---

## 1. Visão Geral

**Gênero:** terror atmosférico e sobrevivência, com exploração, investigação e furtividade. Fugir e se esconder é a regra; defender-se é a exceção.

**Plataforma(s):** PC (Windows).

**Público-alvo:** adolescentes e adultos, a partir de 14 anos. Terror de tensão, sem violência explícita. Pensado primeiro para quem conhece a Unifor: alunos e ex-alunos reconhecem cada prédio, mesmo em ruínas.

**Resumo do Conceito:** Gabriel Magalhães, estudante de 2026, pega no sono na Biblioteca da Unifor e acorda mil anos no futuro, no ano de 3026. A humanidade abandonou a Terra e uma IA dominou o planeta. No antigo centro de pesquisa da Unifor, uma máquina abandonada, a **Âncora**, falhou e abriu uma fenda no tempo no chão da Biblioteca, que por acaso puxou, com dias de diferença, jovens de épocas diferentes. Gabriel precisa encontrá-los, fugir dos robôs da IA, descobrir o que aconteceu e achar um jeito de todos voltarem. A primeira fase do jogo é a Biblioteca. A história completa está no [Enredo Principal](historia/História_Completa.md).

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

**Iluminar.** O campus é escuro. O protagonista usa uma **lanterna a pilha**. Luz ajuda a ver e ajuda a ser visto (os robôs enxergam mais longe), e a bateria acaba: é preciso achar pilhas.

**Rondas e rotinas.** Cada robô cumpre sua rotina de patrulha programada pelo campus. Fora da rotina, quando ouve ou vê o protagonista, o robô sai do protocolo padrão e caça.

**Esconder-se.** Armários enferrujados, buracos no piso, raízes, cabines de estudo. Com um robô por perto, o jogador passa por um **microgame** rápido e diferente em cada esconderijo: prender a respiração no tempo certo, segurar a porta, ficar imóvel.

**Distrair.** Jogar pedras e objetos, derrubar estantes, fazer ruído num lugar para atrair os robôs para longe.

**Defender-se (limitado).** Disparar uma **cápsula de clarão** (um flash descartável) libera um clarão forte por um instante e atordoa o robô por alguns segundos. As cápsulas são escassas — é para escapar, não para vencer.

**Dormir.** Em salas seguras e fechadas, o jogador pode dormir. Dormir **salva o jogo** e leva a um **sonho**: o mesmo lugar no passado antes de tudo. Nos sonhos não há perigo — há conversas, detalhes e senhas que servem no presente.

### Objetivos e Progressão

**Objetivo geral:** encontrar os outros jovens puxados pela fenda, descobrir o que aconteceu e consertar a Âncora para voltar para 2026.

**Estrutura em seis fases sequenciais:**

| Ordem | Fase | O que acontece |
|---|---|---|
| 1ª | **Biblioteca** | Despertar em 3026, primeiro contato pelo rádio com a Clarice, religar os disjuntores e sair pela ala leste. |
| 2ª | **Bloco de salas** | Encontrar a Clarice e a Diana na sala 103, devolver o molho de chaves e abrir a porta corta-fogo do 1º andar. |
| 3ª | **Labirinto** | Encontrar o Zane na oficina do subsolo, pegar o notebook, invadir os três nós de controle e descer pelo alçapão. |
| 4ª | **Centro de Convivência** | Guiado pelo Zane no rádio, pegar a Célula de Energia na câmara fria do Self Nebulosa, resolver o comutador trifásico (Coloração de Grafos) na cozinha da Pizzaria Quasar e usar o elevador de carga do Churrasco Solar. |
| 5ª | **Bunker** | Encontrar o Henrique na sala de dados e atravessar o setor B até a comporta do núcleo. |
| 6ª | **Laboratório (D-Tec)** | Chegar ao laboratório de tecnologia do Bloco M, onde ficam o Carlos e a Âncora. |

A progressão entre áreas é por **passagens abertas, mecanismos, puzzles de grafos e senhas**.

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

> A história, o mundo e os personagens estão no **[Enredo Principal](historia/História_Completa.md)**, que é a lei do projeto. Aqui fica só o resumo.

- **O mundo:** em 3026 o pouco que sobrou da humanidade foi para outro planeta. Ficou o **Carlos**, cientista obcecado pelos anos 80, que criou a Âncora e controla os robôs, que caçam humanos.
- **A Âncora e a fenda:** a Âncora é só uma máquina, abandonada no centro de pesquisa da Unifor. Ela falhou e abriu uma fenda no chão da Biblioteca, que pulsa e, por acaso, puxa quem estiver ali em alguma época.
- **Os personagens:** jovens de cerca de 20 anos, todos vivos, puxados com dias de diferença: Baltazar Magalhães (~1750, antepassado de Gabriel), Diana (1978), Clarice (1990), Henrique (2019, o pesquisador), **Gabriel Magalhães** (2026, o protagonista, último a chegar) e Zane (2123). O antagonista é o Carlos (3026).
- **O objetivo:** encontrar os outros, descobrir o que aconteceu e consertar a Âncora para que todos voltem às suas épocas.
- **A primeira fase** é a **Biblioteca**.

---

## 4. Níveis e Ambientes

> O detalhamento de cada fase (salas, puzzles, sonhos) fica em [`fases.md`](fases.md).

### Estrutura dos Níveis

Um campus contínuo dividido em **seis fases sequenciais**: **Biblioteca → Bloco de salas → Labirinto → Centro de Convivência → Bunker → Laboratório (D-Tec)**.

### Design dos Ambientes

| Área | Visual | Função |
|---|---|---|
| **Biblioteca** | Estantes e racks de arquivo, uma árvore no meio do salão, luz do sol por um teto aberto, poeira e tecnologia de 3026 acordando com a energia | Tutorial e primeiro contato. Silêncio, disjuntores e senha da grade. |
| **Bloco de salas** | Dois corredores e 12 salas de aula futuristas em ruínas (cadeiras VR, lousas holográficas, professor robô desligado) | Encontro com Clarice na 103, distração com o alarme da 104, claviculário e alicate. |
| **Labirinto** | Corredores escuros no subsolo com 6 robôs, oficina do Zane cheia de hologramas e 3 salões de nós | Furtividade no escuro e invasão dos 3 nós de controle com o notebook do Zane. |
| **Centro de Convivência** | Praça de alimentação em arco sob uma cúpula de vidro quebrada, com mesas de holograma, árvores que brilham e quatro restaurantes de neon (tapiocaria, self-service, pizzaria e churrasco), mais um segundo andar opcional com gráfica, loja da universidade e cinema | Contato com Zane pelo rádio, Célula de Energia, Puzzle de Coloração de Grafos e elevador de carga, com letreiros e holofotes que acendem. |
| **Bunker** | Dois setores subterrâneos ("ÂNCORA-03"), corredor alagado no setor B e central de dados | Encontro com Henrique em pessoa e acesso à comporta para o Laboratório. |
| **Laboratório (D-Tec)** | Laboratórios de eletrônica, informática, química, robótica, servidores e o salão central da máquina | Fase final no departamento de tecnologia do Bloco M. |

### Desafios e Obstáculos

- **Os robôs**, cada tipo com seu sensor dominante (som, visão, luz) e padrão de patrulha (`docs/historia/personagens/robos.md`).
- **Barulho:** correr, pisar em entulho e derrubar coisas se ouve pelo grafo.
- **Escuridão:** a lanterna ajuda a ver e ajuda a ser visto; a bateria acaba.
- **Recursos escassos:** pilhas e cápsulas de clarão nunca sobram.
- **O próprio lugar:** pisos que cedem, passagens enterradas, andares alagados, caminhos que só existem por cima.
- **O tempo da grade:** a mesma sala é segura num horário e perigosa no seguinte, e o jogador só conhece a grade pelo que viu nos sonhos.
