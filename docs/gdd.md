# GDD — respostas dos itens 1 a 4

> **Título do Jogo:** Ankhor  
> **Hierarquia:** Para **história, mundo e personagens**, a lei do projeto é o [Enredo Principal](historia/enredo_principal.md): se este GDD contradizer o Enredo, vale o Enredo. Para decisões recentes de design e técnica, consulte [`decisoes.md`](decisoes.md). Para a documentação técnica aprofundada, consulte o índice mestre em [`README.md`](README.md).

> [!TIP]
> **Documentação Modular Detalhada:**
> - 🎯 **[Visão Geral e Pilares](visao_geral/conceito.md)** | **[Estilo Artístico 2.5D](visao_geral/estilo_artistico.md)**
> - ⚙️ **[Mecânicas e Core Loop](mecanicas/README.md)** | **[Furtividade](mecanicas/furtividade_e_esconderijos.md)** | **[Iluminação](mecanicas/iluminacao_e_lanterna.md)** | **[Vida e Checkpoint](mecanicas/vida_e_checkpoint.md)** | **[Sono e Sonhos](mecanicas/sono_e_sonhos.md)**
> - 💻 **[Conceitos de Computação](computacao/README.md)** (Grafos, Coloração, BFS, A*, Markov, Shaders)
> - 📜 **[Enredo Principal](historia/enredo_principal.md)** | **[Índice da História](historia/README.md)** | **[Modelo de Documento](historia/template_documento.md)**
> - 👥 **[Personagens](historia/personagens/)** ([Baltazar](historia/personagens/baltazar.md), [Diana](historia/personagens/diana.md), [Clarice](historia/personagens/clarice.md), [Henrique](historia/personagens/henrique.md), [Gabriel](historia/personagens/gabriel.md), [Zane](historia/personagens/zane.md), [Carlos](historia/personagens/carlos.md), [Robôs](historia/personagens/robos.md), [Modelo de ficha](historia/template_personagem.md))
> - 🗺️ **[Design de Fases](fases/README.md)** | **[Template de Fase](fases/template_fase.md)**
> - 💬 **[Sistema de Diálogos](dialogos/README.md)** | **[Template de Diálogo](dialogos/template_dialogo.md)**

*Versão com o protagonista acordando mil anos no futuro. Os lugares da Unifor são usados apenas como cenário; pessoas, pesquisa e acontecimentos são fictícios.*

---

## 1. Visão Geral

**Gênero:** terror atmosférico e sobrevivência, com exploração, investigação e furtividade. Fugir e se esconder é a regra; defender-se é a exceção.

**Plataforma(s):** PC (Windows).

**Público-alvo:** adolescentes e adultos, a partir de 14 anos. Terror de tensão, sem violência explícita. Pensado primeiro para quem conhece a Unifor: alunos e ex-alunos reconhecem cada prédio, mesmo em ruínas.

**Resumo do Conceito:** Numa madrugada de 2026, o estudante **Gabriel Magalhães** pega no sono na Biblioteca da Unifor e acorda mil anos no futuro, no ano de **3026**, no mesmo lugar, agora uma ruína tomada pela natureza. A sociedade e o planeta ficaram tão ruins que a humanidade se dividiu: os ***Homo sideralis***, uma espécie humana evoluída feita para o espaço, foram embora para outro planeta, e os poucos *sapiens* que ficaram formaram uma resistência que defende a Terra, os **Faroleiros**. Um deles se afastou do grupo e se isolou na Unifor: **Carlos**, um cientista obcecado pelos anos 80, que construiu no **D-Tec** (a parte de tecnologia da Unifor, no Bloco M) uma máquina, a **Âncora**, para ir viver naquela época. A Âncora é imprecisa: a cada tentativa do Carlos, abre uma **fenda** no tempo no chão da Biblioteca e puxa, por acaso, quem estiver naquele ponto em alguma época. Outros jovens de épocas diferentes (**antecessores**) caíram ali com dias de diferença e tentam sobreviver cada um num canto do campus, enquanto os **robôs**, controlados pelo Carlos, caçam qualquer humano que aparecer. Gabriel precisa encontrar os outros, descobrir o que aconteceu — inclusive que um deles é seu antepassado e que outro mente para o grupo a serviço do Carlos — e achar um jeito de consertar a Âncora para todos voltarem às suas épocas. A primeira fase do jogo é a Biblioteca. A história completa está no [Enredo Principal](historia/enredo_principal.md).

O que torna o jogo diferente:
- **Estranhamento do familiar:** o jogador reconhece a catraca, o bebedouro, o quadro de horários, a Biblioteca. O mundo em volta não reconhece mais nada disso.
- **Os perseguidores seguem rotinas de patrulha programadas:** os robôs repetem o mesmo caminho há séculos pelo grafo do campus. Com a ajuda dos antecessores pelo rádio e pelas câmeras, quem entende a ronda sabe por onde cada robô vai passar.
- **Cada antecessor traz uma parte da solução:** jovens puxados de épocas diferentes (~1750 a 2123) dominam partes distintas para consertar a Âncora (as estrelas, as plantas de 1978, o código, a teoria das equações e a tecnologia de 2123), e o **caderno do Gabriel** é o único lugar onde o quadro inteiro se junta.

**Visão Artística:** pixel art em vista lateral 2.5D, com camadas de profundidade, no estilo de *Five Nights at Freddy's: Into the Pit*. O jogo retrata a Unifor mil anos no futuro como uma ruína tomada pela natureza: concreto rachado e desabado, árvores crescendo dentro das salas, areia de dunas cobrindo corredores, e objetos do cotidiano de hoje transformados em relíquias, contrastando com a tecnologia de 3026 (painéis de luz **ciano**), o **vermelho** do Carlos e dos robôs, e as marcas em **âmbar** deixadas pelos Faroleiros. A atmosfera é de mistério, solidão e estranhamento — um terror silencioso, mais de tensão do que de susto, em que o maior choque é perceber quanto tempo passou. Luz natural filtrada pela vegetação contrasta com interiores escuros iluminados por luzes de emergência e pela lanterna a pilha.

---

## 2. Mecânicas de Jogo

### Jogabilidade Central

O jogador explora as ruínas em vista lateral, sala por sala e prédio por prédio, procurando passagens, itens e pistas, enquanto evita os **robôs** que patrulham o campus e o bunker.

**Explorar.** Andar, correr (faz barulho), se espremer por frestas, atravessar tetos desabados, vasculhar o que restou, examinar objetos e marcas nas paredes.

**Iluminar.** O campus tem áreas escuras onde circuitos foram desligados ou quebrados. O protagonista usa uma **lanterna a pilha**. Luz ajuda a ver e ajuda a ser visto (os robôs enxergam mais longe), e a bateria acaba: é preciso achar pilhas.

**Rondas e rotinas.** Cada robô cumpre sua rotina de patrulha programada pelo campus. Fora da rotina, quando ouve ou vê o protagonista, o robô sai do protocolo padrão e caça. Se um robô pega Gabriel, é *game over* e o jogo volta ao último checkpoint.

**Esconder-se.** Armários enferrujados, buracos no piso, raízes, cabines de estudo. Com um robô por perto, o jogador passa por um **microgame** rápido e diferente em cada esconderijo: prender a respiração no tempo certo, segurar a porta, ficar imóvel.

**Distrair.** Jogar pedras e objetos, derrubar estantes, fazer ruído num lugar para atrair os robôs para longe.

**Defender-se (limitado).** Disparar uma **cápsula de clarão** (um flash descartável) libera um clarão forte por um instante e atordoa o robô por alguns segundos. As cápsulas são escassas — é para escapar, não para vencer.

**Dormir.** Em salas seguras e fechadas, o jogador pode dormir para **salvar o jogo** e iniciar um **sonho** (o que os sonhos mostram na premissa atual está em definição na [seção 10.5 do Enredo Principal](historia/enredo_principal.md#105-a-estrutura-da-história)).

### Objetivos e Progressão

**Objetivo geral:** encontrar os outros jovens puxados pela fenda (**antecessores**), descobrir o que aconteceu (a criação da **Âncora** pelo **Carlos** no **D-Tec** e a mentira do **Henrique**) e consertar a Âncora para que todos voltem às suas épocas — incluindo convencer **Baltazar Magalhães**, antepassado de Gabriel, a voltar para 1750 para que a família de Gabriel exista.

**Estrutura por fases e esconderijos:** ninguém consegue consertar a Âncora sozinho. Em cada fase, Gabriel precisa achar um antecessor em seu esconderijo, ganhar a confiança dele e receber a parte que ele traz ([Enredo Principal, seção 3.1](historia/enredo_principal.md#31-como-voltar-cada-um-traz-uma-parte)):

| Quem | Esconderijo | O que traz |
|---|---|---|
| **Baltazar Magalhães** (~1750) | **Biblioteca**, isolado numa sala trancada | **As estrelas:** o céu é o único relógio que não muda, usado para acertar a data de volta de cada um |
| **Diana** (1978) | **Bloco de salas**, na sala 103 (com a Clarice) | **As plantas:** estagiária de arquitetura na obra de 1978, conhece as galerias antigas que não aparecem nos mapas de 3026 e descobre por elas onde fica o núcleo e as passagens até lá |
| **Clarice** (1994) | **Bloco de salas**, na sala 103, atrás de uma barricada | **Código:** faz os terminais da Âncora funcionarem, mapeou as rondas dos robôs como um grafo e sabe o que cada chave abre |
| **Henrique** (2019) | **Bunker**, trancado sozinho na sala de dados | **A teoria** por trás das equações (mas trabalha para o Carlos em troca da promessa de voltar a antes da morte da mãe, atrasando o grupo) |
| **Zane** (2123) | **Labirinto**, numa oficina no subsolo da Âncora | **A tecnologia** mais próxima da Âncora e a manutenção da frequência de rádio e das ligações pelos telefones do campus |
| **Gabriel Magalhães** (2026) | Passa por todos os esconderijos | **O caderno do Gabriel**, onde anota o que cada um sabe e onde todas as partes se juntam |

**Ordem das fases ([Enredo Principal, seção 8](historia/enredo_principal.md#8-estrutura-da-história)):**
Já está definida a sequência inicial **Biblioteca → Bloco de salas → Labirinto**, abrindo provisoriamente a entrada para o **Bunker**, antes da reta final envolvendo o **D-Tec (Bloco M)** e o **Núcleo da Âncora**. O lugar definitivo do Bunker, do Centro de Convivência e das demais áreas após o Labirinto está em definição na [seção 10.5 do Enredo Principal](historia/enredo_principal.md#105-a-estrutura-da-história).

A progressão entre áreas é feita por **passagens abertas, chaves, terminais, invasão de nós de controle e senhas**, com apoio dos antecessores pelo rádio e pelos telefones do campus.

### Sistema de Recompensas

- **Acesso:** novas áreas do campus, esconderijos e atalhos entre eles.
- **Recursos:** pilhas para a lanterna e cápsulas de clarão, sempre escassos.
- **Verdade:** cada pista, documento, marca dos Faroleiros na parede e conversa com os antecessores revela uma parte do mistério. A história é a principal recompensa.
- **Colecionáveis:** relíquias do cotidiano (um crachá, um celular fossilizado, uma caneca da cantina), páginas do diário de Baltazar e registros reunidos no **caderno do Gabriel**.
- **Final:** reunir as partes de todos para consertar a Âncora (os detalhes da volta e do desfecho estão na [seção 10.6 do Enredo Principal](historia/enredo_principal.md#106-a-volta-e-o-fim)).

### OBRIGATÓRIO — recursos de Computação

Os conteúdos de computação estão **dentro das mecânicas**, não só no código:

| Conteúdo | Onde aparece no jogo |
|---|---|
| **Grafos** | O campus é um grafo: cada sala é um nó, cada porta, corredor, escada ou buraco no teto é uma aresta com peso (distância e barulho). Desabamentos removem arestas; passagens abertas pelo jogador criam novas. |
| **Coloração de grafos** | ⚠️ _Em adaptação para a premissa atual:_ usada na alocação de rotinas e setores de patrulha dos robôs (`docs/historia/personagens/robos.md`) para evitar conflitos de rota no grafo. |
| **Busca em largura (BFS)** | O som se propaga pelo grafo e enfraquece a cada sala. Um passo correndo é ouvido a duas salas; uma estante caindo, a cinco. |
| **A\* (caminho mínimo)** | Quando um robô ouve ou vê o jogador, sai da rotina e o persegue pelo menor caminho no grafo. |
| **Cadeia de Markov** | Fora da rotina, cada robô escolhe a próxima sala por probabilidade. É o modelo de movimento dos perseguidores do FNAF, formalizado. |
| **Máquina de estados** | Cada robô alterna entre *rotina*, *investigando*, *perseguindo*, *atordoado* e *retornando* (`docs/historia/personagens/robos.md`). |
| **Estruturas de dados** | Inventário em grade (matriz), fila de eventos da rotina de cada robô, dicionário de flags do mundo (passagens abertas, pistas encontradas, estados de progresso). |
| **Matemática / geometria** | Campo de visão dos robôs por produto escalar e linha de visão por *ray casting*; luz da lanterna em cone (a mesma conta do produto escalar) e decaindo com a bateria. |

---

## 3. Mundo e Narrativa

### Cenário

O campus da **Unifor**, em Fortaleza, **mil anos no futuro (3026)**, depois de ter se tornado um centro de pesquisa em física do tempo. A **Âncora** e o laboratório do **Carlos** ficam no **D-Tec**, no **Bloco M**. Os prédios que sobraram estão rachados, sem teto ou parcialmente enterrados; árvores atravessam salas de aula; dunas avançaram sobre os caminhos entre os blocos; o mato cobre o que era estacionamento. Não há cidade em volta — só vegetação até onde a vista alcança. O que resiste são as coisas duras: concreto, metal, vidro, pedra.

A **eletricidade funciona normalmente** em 3026: onde algo está apagado numa fase (como na Biblioteca antes de religar os disjuntores), trata-se de um circuito desligado ou quebrado, não falta de energia. Pelo cenário também aparecem as marcas em **âmbar** dos **Faroleiros** (um farol de três traços): inteiro em lugares seguros, sem raios e riscado onde há perigo, ou com os raios riscados em **vermelho**, marcando a traição do Carlos.

### História e Personagens

> A história, o mundo e os personagens estão no **[Enredo Principal](historia/enredo_principal.md)**, que é a lei do projeto, junto com as fichas em [`historia/personagens/`](historia/personagens/). Aqui fica só o resumo.

- **O mundo em 3026:** a sociedade e o planeta ficaram muito ruins. Parte da humanidade evoluiu nos ***Homo sideralis*** ("o homem das estrelas", adaptados a implantes e ao espaço) e partiu para outro planeta há menos de 100 anos. Os humanos não evoluídos (***sapiens***) que ficaram formaram uma resistência para defender a Terra: os **Faroleiros**. A **IA** e a robótica são avançadas, mas a IA **não tem consciência** — é apenas uma ferramenta. Não existe uma IA que domina a Terra; os **robôs** e sistemas do campus são ferramentas controladas pelo **Carlos**.
- **O Carlos, a Âncora e a fenda:** o **Carlos** era um Faroleiro que saiu do grupo e se isolou na Unifor durante anos, obcecado pelos anos 80. Construiu no **D-Tec (Bloco M)** a **Âncora** — que é só uma máquina de física do tempo, sem consciência — para ir viver naquela época. Como a máquina é imprecisa, cada tentativa do Carlos abre uma **fenda** no chão da Biblioteca, que pulsa e puxa, **por acaso**, quem estiver naquele ponto em alguma época.
- **Os personagens:** todos os puxados têm cerca de 20 anos, têm ligação com a região da Unifor e chegaram a 3026 com dias de diferença. Estão todos vivos:
  - **[Baltazar Magalhães](historia/personagens/baltazar.md)** (~1750): antepassado de Gabriel; viu uma luz pela luneta no sítio da família e foi investigar. Isolou-se com medo numa sala da Biblioteca.
  - **[Diana](historia/personagens/diana.md)** (1978): estagiária de arquitetura que vigiava a obra do campus à noite. Está na sala 103 do Bloco de salas com a Clarice.
  - **[Clarice](historia/personagens/clarice.md)** (1994): rodava um programa num terminal da Biblioteca de madrugada. Guia Gabriel pelo rádio a partir da sala 103.
  - **[Henrique](historia/personagens/henrique.md)** (2019): o primeiro a chegar. Estudava viagem no tempo na Biblioteca (seu sumiço virou lenda em 2026 e deu origem à cadeira de Modelagem e Simulação que Gabriel cursa). Fica trancado na sala de dados do Bunker com as câmeras e o rádio; finge ajudar a consertar tudo, mas **trabalha para o Carlos** atrasando e dividindo o grupo em troca da promessa de voltar para antes da morte da mãe.
  - **[Zane](historia/personagens/zane.md)** (2123): mantém a frequência de rádio e liga pelos telefones velhos a partir da oficina no Labirinto; desconfia do Henrique e tenta invadir o Bunker.
  - **[Gabriel Magalhães](historia/personagens/gabriel.md)** (2026): o protagonista e último a chegar, após dormir na Biblioteca com seu caderno aberto.
  - **[Carlos](historia/personagens/carlos.md)** (3026): o antagonista, cientista *sapiens* isolado no laboratório do D-Tec.
  - **[Os robôs](historia/personagens/robos.md)** (3026): inimigos controlados pelo Carlos (como a **Sentinela**, focada em visão, e o **Rastreador**, focado em audição).
- **A família Magalhães:** Gabriel começa o jogo com um **anel desgastado** da avó no inventário e, no meio do jogo, descobre o mesmo anel novo no dedo de Baltazar. Baltazar acha 3026 um milagre e quer ficar, mas Gabriel precisa convencê-lo a voltar para 1750, ou a família Magalhães pode nunca existir.
- **A primeira fase** é a **Biblioteca**.

---

## 4. Níveis e Ambientes

> O detalhamento de cada fase fica em [`fases/README.md`](fases/README.md) e nos documentos de cada área em [`fases/`](fases/).

### Estrutura dos Níveis

Um campus contínuo modelado como grafo, onde cada fase leva a um personagem e ao esconderijo dele. A ordem inicial definida no [Enredo Principal (seção 8)](historia/enredo_principal.md#8-estrutura-da-história) é **Biblioteca → Bloco de salas → Labirinto**, abrindo provisoriamente a passagem para o **Bunker**. O posicionamento definitivo do Bunker, do Centro de Convivência e das demais áreas após o Labirinto está listado nas pendências da [seção 10.5 do Enredo Principal](historia/enredo_principal.md#105-a-estrutura-da-história).

### Design dos Ambientes

| Área | Visual | Função na História e no Jogo |
|---|---|---|
| **Biblioteca** ([`fases/biblioteca.md`](fases/biblioteca.md)) | Estantes caídas e vazias, uma árvore no meio do salão, luz do sol por um teto aberto, painéis com luz ciano e torres de equipamentos de 3026 | **1ª fase (Ato 1).** Onde a fenda se abre e Gabriel acorda. Tutorial de furtividade, lanterna e pilhas. Contém o acampamento vazio de Baltazar (que se isolou numa sala trancada), o terminal com o bilhete da Clarice, o rádio deixado pelo Zane no balcão (com a primeira dica da Clarice) e o telefone que o Zane usa para destrancar a saída. |
| **Bloco de salas** ([`fases/bloco_de_salas.md`](fases/bloco_de_salas.md)) | Dois andares e 12 salas de aula à noite, corredores parcialmente tomados pela ruína e salas trancadas | **2ª fase (Ato 2).** Onde fica o esconderijo da **Clarice** e da **Diana** (sala 103, atrás de uma barricada). Gabriel devolve o molho de chaves da Clarice para ganhar sua confiança e passa a ser guiado por ela pelo rádio (com o grafo das rondas e o que cada chave abre) até sair pela porta corta-fogo do 1º andar. |
| **Labirinto** ([`fases/labirinto.md`](fases/labirinto.md)) | Subsolo escuro do centro de pesquisa da Âncora, corredores que se cruzam, oficina cheia de componentes eletrônicos e telas holográficas | **3ª fase (Ato 2).** Seis robôs patrulham o subsolo. Base do **Zane**, que desconfia do Henrique e entrega seu notebook para Gabriel invadir três nós de controle em três salões, destravando o alçapão na oficina que desce para o Bunker. |
| **Bunker** ([`fases/bunker.md`](fases/bunker.md)) | Subterrâneo embaixo do núcleo da Âncora ("ÂNCORA-03") com dois setores, corredores patrulhados por robôs e salas montadas como interiores de casas dos séculos XIX e XX | **Em desenvolvimento (Ato 3, posição provisória).** As salas antigas mostram, sem explicar, a obsessão do Carlos pelo passado. Onde o **Henrique** fica sozinho na sala de dados trancada com as câmeras do campus, e onde fica o setor B lacrado com a comporta do núcleo. |
| **D-Tec (Bloco M)** | Área de tecnologia da Unifor, laboratório do Carlos e núcleo da Âncora | Onde o **Carlos** se isolou (ele nunca sai de lá) e onde a Âncora foi construída. Reta final após o grupo descobrir a mentira do Henrique. |
| **Centro de Convivência e demais áreas** ([`fases/centro_de_convivencia.md`](fases/centro_de_convivencia.md)) | Estrutura aberta tomada pelo mato, balcões e mesas cobertos de raízes | ⚠️ **Em definição ([Enredo Principal, seção 10.5](historia/enredo_principal.md#105-a-estrutura-da-história)):** deixou de ser a fase seguinte ao Bloco de salas; sua posição na ordem, quem Gabriel encontra lá e as demais áreas (Espaço Cultural, NAMI, Reitoria) ainda serão definidos pelo grupo. |

### Desafios e Obstáculos

- **Os robôs**, controlados pelo Carlos, cada tipo com seu sentido dominante (visão na Sentinela, audição no Rastreador) e padrão de patrulha (`docs/historia/personagens/robos.md`).
- **Barulho:** correr, pisar em entulho e derrubar coisas se propaga pelo grafo (BFS).
- **Escuridão:** a lanterna ajuda a ver e ajuda a ser visto; a bateria acaba.
- **Recursos escassos:** pilhas e cápsulas de clarão nunca sobram.
- **O próprio lugar:** pisos que cedem, portas e setores lacrados pelo sistema, circuitos desligados e rotas patrulhadas no campus e no bunker.
- **Rotinas de patrulha:** cada sala pode estar livre num momento e patrulhada no seguinte; avançar exige observar as rondas e usar as informações passadas pelo rádio.

