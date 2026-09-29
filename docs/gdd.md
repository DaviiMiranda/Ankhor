# GDD — respostas dos itens 1 a 4

> **Título do Jogo:** Ankhor  
> **Hierarquia:** Para decisões recentes, consulte [`decisoes.md`](decisoes.md). Para a documentação técnica aprofundada, consulte o índice mestre em [`README.md`](README.md).

> [!TIP]
> **Documentação Modular Detalhada:**
> - 🎯 **[Visão Geral e Pilares](visao_geral/conceito.md)** | **[Estilo Artístico 2.5D](visao_geral/estilo_artistico.md)**
> - ⚙️ **[Mecânicas e Core Loop](mecanicas/README.md)** | **[Furtividade](mecanicas/furtividade_e_esconderijos.md)** | **[Iluminação](mecanicas/iluminacao_e_fungos.md)** | **[Sono e Sonhos](mecanicas/sono_e_sonhos.md)**
> - 💻 **[Conceitos de Computação](computacao/README.md)** (Grafos, Coloração, BFS, A*, Markov, Shaders)
> - 📜 **[Estrutura Narrativa](historia/README.md)** | **[Template de Documentos](historia/template_documento.md)**
> - 👥 **[Personagens e IA](personagens/README.md)** ([Gabriel](personagens/gabriel.md), [Robôs](personagens/robos.md), [Template](personagens/template_personagem.md))
> - 🗺️ **[Design de Fases](fases/README.md)** | **[Template de Fase](fases/template_fase.md)**
> - 💬 **[Sistema de Diálogos](dialogos/README.md)** | **[Template de Diálogo](dialogos/template_dialogo.md)**

*Versão com o protagonista acordando mil anos no futuro. Os lugares da Unifor são usados apenas como cenário; pessoas, pesquisa e acontecimentos são fictícios.*

---

## 1. Visão Geral

**Gênero:** terror atmosférico e sobrevivência, com exploração, investigação e furtividade. Fugir e se esconder é a regra; defender-se é a exceção.

**Plataforma(s):** PC (Windows).

**Público-alvo:** adolescentes e adultos, a partir de 14 anos. Terror de tensão, sem violência explícita. Pensado primeiro para quem conhece a Unifor: alunos e ex-alunos reconhecem cada prédio, mesmo em ruínas.

**Resumo do Conceito:** Gabriel acorda mil anos no futuro, no ano de 3026. Ele descobre que a Unifor tornou-se um centro de pesquisa em física do tempo e que a explosão de um aparelho chamado **Âncora** rasgou o tempo dentro do campus. Essa fenda temporal encosta em momentos aleatórios do passado e puxa quem estiver por perto — numa madrugada de 2026, puxou Gabriel da Biblioteca. A fenda está em expansão contínua e, caso não seja fechada, engolirá o passado do campus e a própria época de Gabriel. Ele descobre que não foi o primeiro: antes vieram uma aluna de 1994, um segurança de 2008, um professor de 2019 e alguém de 2041, e nenhum deles conseguiu. A primeira fase do jogo é a Biblioteca.

O que torna o jogo diferente:
- **Estranhamento do familiar:** o jogador reconhece a catraca, o bebedouro, o quadro, a Biblioteca. O mundo em volta não reconhece mais nada disso.
- **Os perseguidores seguem a grade horária** da semana de provas, mil anos depois. Quem descobre a grade sabe onde cada um vai estar.
- **Dormir é salvar e é voltar ao passado.** Cada sono leva o protagonista, em sonho, à última semana antes de tudo — e é só lá que ele aprende a grade, as senhas e a verdade.

**Visão Artística:** pixel art em vista lateral 2.5D, com camadas de profundidade, no estilo de *Five Nights at Freddy's: Into the Pit*. O jogo retrata a Unifor mil anos no futuro como uma ruína tomada pela natureza: concreto rachado e desabado, árvores crescendo dentro das salas, areia de dunas cobrindo corredores, e objetos do cotidiano de hoje transformados em relíquias. A atmosfera é de mistério, solidão e estranhamento — um terror silencioso, mais de tensão do que de susto, em que o maior choque é perceber quanto tempo passou. Luz natural filtrada pela vegetação contrasta com interiores escuros iluminados só pelo brilho frio de fungos bioluminescentes. Nos sonhos, o mesmo campus aparece cheio, iluminado e normal.

---

## 2. Mecânicas de Jogo

### Jogabilidade Central

O jogador explora as ruínas em vista lateral, sala por sala e prédio por prédio, procurando passagens, itens e pistas, enquanto evita os **robôs** que patrulham o campus.

**Explorar.** Andar, correr (faz barulho), se espremer por frestas, atravessar tetos desabados, vasculhar o que restou, examinar objetos e marcas nas paredes.

**Iluminar.** Nada elétrico funciona depois de mil anos. A luz vem de **fungos bioluminescentes** que cresceram nas ruínas: o protagonista os recolhe em potes e usa como lanterna. Luz ajuda a ver e ajuda a ser visto, e o brilho enfraquece com o tempo.

**Rondas e rotinas.** Cada robô cumpre sua rotina de patrulha programada pelo campus. Fora da rotina, quando ouve ou vê o protagonista, o robô sai do protocolo padrão e caça.

**Esconder-se.** Armários enferrujados, buracos no piso, raízes, cabines de estudo. Com um robô por perto, o jogador passa por um **microgame** rápido e diferente em cada esconderijo: prender a respiração no tempo certo, segurar a porta, ficar imóvel.

**Distrair.** Jogar pedras e objetos, derrubar estantes, fazer ruído num lugar para atrair os robôs para longe.

**Defender-se (limitado).** Esmagar uma **cápsula de fungo** libera um clarão forte por um instante e atordoa o robô por alguns segundos. As cápsulas são escassas — é para escapar, não para vencer.

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
- **Recursos:** fungos para luz e cápsulas de clarão, sempre escassos.
- **Verdade:** cada pista, marca na parede e sonho revela uma parte do mistério. A história é a principal recompensa.
- **Colecionáveis:** relíquias do cotidiano (um crachá, um celular fossilizado, uma caneca da cantina) com a descrição de quem eram seus donos, e páginas do diário que o protagonista vai escrevendo.
- **Final:** o que o jogador descobriu muda as opções disponíveis no final.

### OBRIGATÓRIO — recursos de Computação

Os conteúdos de computação estão **dentro das mecânicas**, não só no código:

| Conteúdo | Onde aparece no jogo |
|---|---|
| **Grafos** | O campus é um grafo: cada sala é um nó, cada porta, corredor, escada ou buraco no teto é uma aresta com peso (distância e barulho). Desabamentos removem arestas; passagens abertas pelo jogador criam novas. |
| **Coloração de grafos** | ⚠️ _A definir com a nova premissa:_ antes, a grade horária da semana de provas era gerada por coloração de grafos: aulas que dividem professor ou sala não podem ter o mesmo horário. Essa grade definia onde cada Insone estava a cada hora. Com os robôs em patrulha programada (`docs/personagens/robos.md`), falta decidir de onde vem a grade. |
| **Busca em largura (BFS)** | O som se propaga pelo grafo e enfraquece a cada sala. Um passo correndo é ouvido a duas salas; uma estante caindo, a cinco. |
| **A\* (caminho mínimo)** | Quando um robô ouve ou vê o jogador, sai da rotina e o persegue pelo menor caminho no grafo. |
| **Cadeia de Markov** | Fora da rotina, cada robô escolhe a próxima sala por probabilidade, com chances que crescem a cada dia. É o modelo de movimento dos perseguidores do FNAF, formalizado. |
| **Máquina de estados** | Cada robô alterna entre *rotina*, *investigando*, *perseguindo*, *atordoado* e *retornando* (`docs/personagens/robos.md`). |
| **Estruturas de dados** | Inventário em grade (matriz), fila de eventos da rotina de cada robô, dicionário de flags do mundo (passagens abertas, pistas encontradas, sonhos vistos). |
| **Matemática / geometria** | Campo de visão dos robôs por produto escalar e linha de visão por *ray casting*; luz dos fungos decaindo com o tempo e com a distância. |

---

## 3. Mundo e Narrativa

### Cenário

O campus da **Unifor**, em Fortaleza, **mil anos no futuro**. Os prédios que sobraram estão rachados, sem teto ou parcialmente enterrados; árvores atravessam salas de aula; dunas avançaram sobre os caminhos entre os blocos; o mato cobre o que era estacionamento. Não há cidade em volta — só vegetação até onde a vista alcança. O que resiste são as coisas duras: concreto, metal, vidro, pedra.

E, nos sonhos, o mesmo campus **na última semana antes de tudo**: cheio, iluminado, barulhento e normal.

### História e Personagens

**O começo.** Gabriel, um estudante universitário, acorda no ano de 3026 (mil anos no futuro) na Biblioteca da Unifor. Ele descobre que o campus se transformou em um centro de pesquisa em física do tempo e que a explosão de um aparelho experimental chamado **Âncora** rasgou o tempo dentro do campus.

**A Fenda Temporal e o Colapso:**
- A fenda encosta em momentos aleatórios do passado e puxa quem estiver por perto — numa madrugada de 2026, puxou Gabriel da Biblioteca.
- A fenda está em expansão contínua: caso não seja fechada, engolirá todo o passado do campus, incluindo a época original de Gabriel.
- **Os que vieram antes:** Gabriel descobre que não foi o primeiro. Antes dele, a fenda puxou pessoas de diferentes épocas:
  1. Uma aluna de 1994
  2. Um segurança de 2008
  3. Um professor de 2019
  4. Alguém de 2041
  - Ninguém conseguiu fechar a fenda ou reverter o processo.

**Fases:**
- A primeira fase do jogo é a **Biblioteca**.

**Personagens:**
- **Gabriel** — o protagonista. Estudante universitário puxado de uma madrugada de 2026 para 3026 pela fenda da Âncora. Precisa entender o que aconteceu e fechar a fenda antes que ela consuma seu próprio tempo.
- **Os antecessores** — pessoas puxadas antes de Gabriel, que deixaram pistas pelo campus: Mestre Baltazar (~1750), Inspetor Agostinho (1978), Clarice (1994), Seu Valdir (2008, fala com Gabriel pelo rádio), um professor de 2019 cuja pesquisa virou a cadeira de Gabriel, e Zane (2123). A pessoa de 2041 ainda está a definir. Fichas em [`personagens/antecessores.md`](personagens/antecessores.md).
- *(Revelação central em avaliação: [`historia/revelacao_central.md`](historia/revelacao_central.md))*

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
| **Espaço Cultural** | Galeria escura e fechada, obras irreconhecíveis, fungos brilhando nas paredes | Puzzles visuais e as primeiras peças do projeto VIGÍLIA-7. |
| **NAMI** | Corredores de azulejo rachado, macas de metal, o andar de baixo alagado, a luz fria dos fungos como única iluminação | O ponto alto da tensão e das revelações. |
| **Reitoria e portão** | O prédio mais conservado, com o cofre e os arquivos; do lado de fora do portão, só vegetação | O final. |

### Desafios e Obstáculos

- **Os robôs**, cada tipo com seu sensor dominante (som, visão, luz) e padrão de patrulha (`docs/personagens/robos.md`).
- **Barulho:** correr, pisar em entulho e derrubar coisas se ouve pelo grafo.
- **Escuridão:** os fungos ajudam a ver e ajudam a ser visto; o brilho enfraquece.
- **Recursos escassos:** fungos para luz e cápsulas de clarão nunca sobram.
- **O próprio lugar:** pisos que cedem, passagens enterradas, andares alagados, caminhos que só existem por cima.
- **O tempo da grade:** a mesma sala é segura num horário e perigosa no seguinte, e o jogador só conhece a grade pelo que viu nos sonhos.
