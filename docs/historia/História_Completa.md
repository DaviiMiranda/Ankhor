# Enredo Principal

> [!IMPORTANT]
> **Este documento é a lei do projeto**, junto com as fichas de [`personagens/`](personagens/) (uma por personagem), que fazem parte dele. Tudo o que diz respeito à história, ao mundo e aos personagens de **Ankhor** vale como está escrito aqui e nas fichas, **acima de qualquer outro documento**: GDD, fases, diálogos, arte, textos em `dados/` e o próprio `decisoes.md`. Em caso de dúvida em qualquer parte do jogo (o que uma fase conta, como um personagem fala, o que um objeto significa), consulte este documento e a ficha do personagem. Se outra parte do projeto contradisser o que está aqui, **a outra parte está errada** e deve ser corrigida.

> **Status:** reescrito em 2026-10-06, quando a história mudou de rumo: saíram os loops e a revelação de "Gabriel é o paradoxo", e a fenda passou a ser **um acaso** para quem cai nela. Em 2026-10-07 entrou o antagonista, o **Carlos**. Em 2026-10-15 entraram os ***Homo sideralis*** (quem foi embora), os **Faroleiros** (quem ficou) e o conteúdo da mentira do **Henrique**.
> **Como mudar:** só por decisão do grupo. Toda mudança de história entra **no mesmo PR** neste documento e em [`../decisoes.md`](../decisoes.md) (que guarda o histórico de quando e por que mudou). Tudo o que ainda não foi decidido fica na **seção 10 ("Pendências")**, no fim, e não no meio da narrativa: o que está fora das pendências está decidido.

---

## 1. A história em um parágrafo

Numa madrugada de 2026, o estudante **Gabriel Magalhães** pega no sono na Biblioteca da Unifor e acorda no ano de **3026**, no mesmo lugar, agora uma ruína tomada pela natureza. A sociedade e o planeta ficaram tão ruins que a humanidade se dividiu: os ***Homo sideralis***, uma espécie humana evoluída, feita para o espaço, foram embora para outro planeta, e os poucos *sapiens* que ficaram formaram uma resistência que defende a Terra, os **Faroleiros**. Um deles se afastou do grupo e se isolou na Unifor: **Carlos**, um cientista obcecado pelos **anos 80**, que construiu uma máquina no **D-Tec**, a parte de tecnologia da Unifor, no Bloco M: a **Âncora**, para ir viver naquela época. A Âncora é imprecisa: a cada tentativa do Carlos, abre uma **fenda** no tempo no chão da Biblioteca e puxa quem estiver naquele ponto, em alguma época. Para quem cai, **é um acaso**: o Carlos não escolhe ninguém. Gabriel não é o único: outros jovens de épocas diferentes caíram ali com dias de diferença, e cada um está tentando sobreviver num canto do campus. Os robôs, controlados pelo Carlos, caçam qualquer humano que aparecer. Gabriel precisa encontrar os outros, descobrir o que aconteceu e achar um jeito de todos voltarem para suas épocas. No caminho descobre que um deles é seu antepassado, que outro mente para o grupo a serviço do Carlos, e que por trás de tudo existe alguém.

---

## 2. O mundo

### 2.1 A Terra em 3026

- **A Terra ficou muito ruim**: a sociedade e o planeta. Quase não restam humanos na Terra.
- **Os *Homo sideralis* foram embora.** Ao longo dos séculos, parte da humanidade evoluiu numa espécie nova, os ***Homo sideralis*** ("o homem das estrelas"): aceitam melhor os implantes cibernéticos e vivem melhor no espaço e em planetas com outra temperatura ou outra gravidade. Foram eles que **partiram para outro planeta**, há **menos de 100 anos**.
- **Os Faroleiros ficaram.** Os humanos ainda não evoluídos, os *sapiens*, não partiram. Os que ficaram formaram uma resistência que **defende o planeta**: os **Faroleiros**. Ainda existem, **longe do campus**. O símbolo deles está na seção 2.4.
- **O Carlos era um Faroleiro.** Saiu do grupo e se isolou na Unifor, sozinho, durante anos, para usar a Âncora e ir viver nos anos 80 (seção 4.3).
- **A IA e a robótica** são muito avançadas, mas a IA **não tem consciência**: é uma ferramenta nas mãos dos humanos. Não existe uma IA que domina a Terra. Os robôs e os sistemas do campus são ferramentas do Carlos.

### 2.2 O campus em 3026

- A **Unifor, em Fortaleza**, mil anos depois. Em algum momento virou um centro de pesquisa em física do tempo.
- A **Âncora** e o laboratório do **Carlos** ficam no **D-Tec**, a parte de tecnologia da Unifor, no **Bloco M**.
- Concreto rachado e desabado, árvores dentro das salas, dunas sobre os corredores, mato onde era estacionamento. Não há cidade em volta, só vegetação. Resistem as coisas duras: concreto, metal, vidro, pedra.
- Objetos do cotidiano de hoje (catraca, bebedouro, quadro de horários, a cantina) viraram relíquias. O choque do jogo é perceber **quanto tempo passou**.
- **A eletricidade funciona normalmente.** Onde algo está apagado numa fase (como a grade da Biblioteca antes de religar os disjuntores), é um circuito desligado ou quebrado, não falta de energia.

### 2.3 Os robôs

- Os inimigos são **robôs** controlados pelo **Carlos**, que patrulham o campus por **rotinas programadas**. Repetem o mesmo caminho há séculos: dá para decorar. São ferramentas: a IA que os move não tem consciência (seção 2.1).
- Patrulham **também o bunker** (seção 6).
- Fora da rotina, quando ouvem ou veem um humano, saem do protocolo e caçam. Por que caçam (para capturar ou para eliminar) está pendente (seção 10.2).
- São agressivos: se pegam Gabriel, é **game over** e o jogo volta ao último checkpoint (ver [`../mecanicas/vida_e_checkpoint.md`](../mecanicas/vida_e_checkpoint.md)).
- Cada tipo tem um sentido dominante (som, visão, luz). Os dois já implementados são a **Sentinela** (visão) e o **Rastreador** (audição). Ver [`personagens/robos.docx`](personagens/robos.docx).
- Gabriel não é um combatente: **fugir e se esconder é a regra**, defender-se é a exceção.

### 2.4 Os Faroleiros e o símbolo deles

- **Quem são:** os *sapiens* que não partiram com os *Homo sideralis* e ficaram para defender a Terra. O nome vem de quem cuida de um farol: alguém que fica para manter a luz acesa para quem está longe. Ainda existem, longe do campus. O Carlos foi um deles.
- **O símbolo:** um farol visto de frente, feito em três traços, para ser pintado à mão e às pressas:
  1. **A torre:** um trapézio alto e estreito, mais largo na base.
  2. **A lanterna:** um quadrado pequeno no topo, com um ponto no centro.
  3. **Três raios** saindo da lanterna **para cima, em leque**, apontando para o céu, para onde os *Homo sideralis* foram: uma luz acesa para quem partiu. Os três raios são o juramento: **ficar, cuidar, esperar**.
- **A cor:** **âmbar**, a luz quente de uma chama. O ciano é a tecnologia de 3026, o vermelho é o Carlos e os robôs; onde aparece âmbar, passou um Faroleiro.
- **Variações no cenário:**

| Marca | O que diz |
|---|---|
| Farol inteiro, com os três raios | Lugar seguro, ou esconderijo antigo dos Faroleiros |
| Farol sem raios, com um traço atravessado | Farol apagado: lugar perdido, perigo |
| Farol com os raios **riscados em vermelho** | A traição do Carlos. Ninguém explica: o jogador vê o vermelho dos robôs por cima da luz dos Faroleiros |

- **Em pixel art:** cabe em 9×12 px (torre de 5 px de base e 7 de altura, lanterna de 3×3, raios de 3 px).

---

## 3. A Âncora e a fenda

| | |
|---|---|
| **O que é a Âncora** | **Só uma máquina.** Um aparelho experimental de física do tempo. Não pensa, não quer nada, não escolhe ninguém |
| **Onde está a Âncora** | No **D-Tec**, a parte de tecnologia da Unifor, no Bloco M, junto do laboratório do Carlos |
| **Quem criou** | O **Carlos** (seção 4.3), para ir viver nos anos 80 |
| **O que aconteceu** | O Carlos tenta usar a Âncora para ir para os anos 80, mas a máquina é **imprecisa**: não acerta a época nem escolhe quem puxa. Cada tentativa abre uma fenda no tempo |
| **Onde a fenda se abre** | Sempre no mesmo ponto: o chão onde hoje fica a Biblioteca (ou onde ela ainda viria a ser construída) |
| **Como a fenda age** | **Pulsa.** A cada tentativa do Carlos, a cada 3 dias, encosta numa época diferente e puxa quem estiver no ponto naquela noite. A cada pulso fica maior |
| **Por que essas pessoas** | **Acaso.** O Carlos não escolhe quem a fenda puxa: estavam no lugar errado na noite errada |
| **A ameaça** | Enquanto o Carlos continuar tentando, gente nova continua caindo, e a fenda continua crescendo |
| **Nome** | O aparelho se chama **Âncora**. **Ankhor** é o nome do jogo. Os dois não se confundem |

Os personagens não sabem nada disso no começo. Descobrir o que é a Âncora, quem está por trás dela e como consertá-la é o que move a história.

### 3.1 Como voltar: cada um traz uma parte

Para mandar cada pessoa de volta para a sua noite, é preciso consertar a Âncora, e ninguém sabe fazer isso sozinho. Cada personagem que Gabriel encontra contribui com uma parte. Isso dá a estrutura do jogo: **em cada fase, achar alguém, ganhar a confiança da pessoa e receber a parte dela.**

| Quem | O que traz |
|---|---|
| Baltazar (1750) | As estrelas: o céu é o único relógio que não muda, e é por ele que se acerta a data de volta de cada um |
| Diana (1978) | O mapa das galerias: estudante de Direito que cresceu cortando caminho pela obra, conhece as galerias de 1978, que não aparecem nos mapas de 3026, e descobre por elas onde fica o núcleo e as passagens até lá |
| Clarice (1990) | Código: faz os terminais da Âncora funcionarem. Mapeou as rondas dos robôs como um grafo e sabe o que cada chave abre |
| Henrique (2019) | A teoria por trás das equações |
| Zane (2123) | A tecnologia mais próxima da Âncora |
| Gabriel (2026) | O caderno, como o lugar onde as partes de todos se juntam. O grupo está espalhado, e Gabriel é o único que passa por todos os esconderijos: anota o que cada um sabe, e no fim o caderno é o único lugar onde o quadro inteiro existe |

---

## 4. Os personagens

**Quem cada personagem é** (história, personalidade, como fala, o que quer, o que teme, defeito, arco e relações) está na ficha dele, em [`personagens/`](personagens/). Cada ficha faz parte deste documento e tem a mesma autoridade. Falas, documentos, retratos, animações e sons de um personagem seguem a ficha dele.

### 4.1 Regras para todos

- Todos os puxados pela fenda têm **cerca de 20 anos**.
- Todos têm alguma **ligação com a região da Unifor**, além de terem sido puxados no chão da Biblioteca.
- Chegaram a 3026 **com 3 dias de intervalo entre uma chegada e a seguinte**. Estão todos **vivos**, cada um sobrevivendo do seu jeito num lugar do campus, e Gabriel **encontra cada um ao longo do jogo**.
- **Ordem de chegada:** o **Henrique é o primeiro** a chegar, e por isso é quem está há mais tempo em 3026. **Gabriel é o último**. No meio: o **Zane** chegou antes da **Clarice**, e a **Diana** chegou depois da Clarice (apareceu na 103 quando a Clarice já estava lá). Só a posição do **Baltazar** ainda está pendente.
- **Quantos dias cada um está lá:** como são 3 dias entre uma chegada e a seguinte, quem chega *n* posições antes de Gabriel chegou 3 × *n* dias antes dele. Sem contar o Baltazar: a Diana, 3 dias antes; a Clarice, 6; o Zane, 9; o Henrique, 12. Se o Baltazar entrar no meio da ordem, quem veio antes dele ganha mais 3 dias.

### 4.2 Fichas

| Época | Personagem |
|---|---|
| ~1750 | [Baltazar Magalhães](personagens/baltazar.docx) |
| 1978 | [Diana](personagens/diana.docx) |
| 1990 | [Clarice](personagens/clarice.docx) |
| 2019 | [Henrique](personagens/henrique.docx), o pesquisador |
| 2026 | [Gabriel Magalhães](personagens/gabriel.docx) (protagonista) |
| 2123 | [Zane](personagens/zane.docx) |
| 3026 | [Carlos](personagens/carlos.docx) (antagonista) |
| 3026 | [Os robôs](personagens/robos.docx) (inimigos) |

### 4.3 O Carlos, o antagonista

O antagonista é o **Carlos**, cientista *sapiens* de 3026 que criou a Âncora e controla os robôs. Era um **Faroleiro**: saiu da resistência e se isolou na Unifor, sozinho durante anos, para ir viver nos anos 80. Quem ele é está na [ficha dele](personagens/carlos.docx).

- **Ele e o Henrique:** quando o Henrique caiu, o primeiro de todos, o Carlos prometeu levá-lo de volta **para antes da morte da mãe dele** e assim ganhou a confiança do Henrique. Na verdade, só o usa: o Henrique serve para **atrasar os outros** enquanto o Carlos conserta a Âncora. O Carlos não se importa com os puxados (seção 8, "A virada").
- **O primeiro registro dele:** a **Folha de calibração**, no Corredor do Tempo do Labirinto (opcional). Ali ele testava a calibração da Âncora com objetos dos anos 80 (um Genius, os três quadros de *De Volta para o Futuro*, um micro e um telefone de disco). Na folha ele conta que a máquina errou de novo, abriu a fenda na Biblioteca e puxou alguém que ele **nem foi ver**; diz que já foi um Faroleiro e que só quer o mundo dos anos 80. **Assina só "C."**: o jogador ainda não sabe o nome dele (quando descobre continua pendente, seção 10.2).
- Muita coisa sobre o Carlos ainda está pendente (seção 10.2).

---

## 5. A família Magalhães

- **Baltazar é antepassado de Gabriel**, umas dez gerações antes dele. O sobrenome **Magalhães** liga a família pelos séculos.
- **O objeto:** Gabriel começa o jogo com um **anel desgastado** no inventário, que a avó deu para ele. O jogador vê o item desde o começo sem dar importância.
- **A descoberta acontece jogando**, não numa explicação: no meio do jogo, Gabriel vê o mesmo anel com o Baltazar (novo no dedo dele, gasto no de Gabriel). O jogador compara os dois e entende sozinho.
- **Gabriel conta para o Baltazar** que é descendente dele.
- Com isso, mandar todos de volta deixa de ser só ajudar os outros: se o Baltazar não voltar para 1750, a família de Gabriel pode nunca existir.
- **O Baltazar quer ficar, mas não pode.** Para ele, 3026 é um milagre a estudar, e ele quer ficar. Só que precisa voltar, ou a família de Gabriel não existe. Gabriel tem que convencer o próprio antepassado a ir embora.

---

## 6. Os esconderijos

- Cada personagem tem um **lugar próprio** no campus. Um lugar pode abrigar **2 ou 3 personagens**.

| Esconderijo | Quem fica |
|---|---|
| **Bunker**, embaixo do núcleo da Âncora. Difícil de alcançar e lacrado pelo sistema. **Os robôs patrulham o bunker** | Henrique, **sozinho**, numa sala de dados **trancada**, com as câmeras do campus e o rádio. Diz que está escondido ali tentando consertar tudo. O Carlos nunca vai lá. O Zane chega depois do Labirinto, com Gabriel. No fim do Bunker, o grupo todo se encontra ali pela primeira vez (Ato 3) |
| **Labirinto**, numa oficina no canto do subsolo da Âncora, perto de onde Gabriel entra | Zane, entre componentes eletrônicos jogados por todo lado e telas holográficas. É a **base dele**: é dali que mantém a frequência do grupo. Desconfia do Henrique e **está há dias tentando invadir o bunker**, sem conseguir de longe. Pede ajuda a Gabriel |
| **Labirinto**, numa sala secreta atrás de um painel solto na parede, que só aparece com a lanterna apontada para ele | Baltazar, sozinho e com medo. Deixou o acampamento da Biblioteca seguindo a luz, desceu ao subsolo e se escondeu ali. Os robôs nunca acharam a sala |
| **Bloco de salas**, na sala 103, atrás de uma barricada | Clarice, que foi para lá depois de chegar à Biblioteca, e Diana, que apareceu depois e foi acolhida por ela. Desde então tentam descobrir o que aconteceu, com a ajuda do Henrique pelo rádio |
| **D-Tec**, no laboratório | Carlos, que nunca sai de lá |

### 6.1 Como eles se comunicam

- O **Zane**, da **oficina do Labirinto**, faz a **comunicação de todos**: mantém a **frequência de rádio** do grupo e liga pelos telefones velhos do campus.
- **O rádio do balcão existe por causa da Clarice.** Ela acordou na Biblioteca e passou dias sozinha antes de alguém achá-la. Depois disso, o Zane deixou um rádio sintonizado na frequência no **balcão de atendimento da Biblioteca**, porque é lá que quem cai na fenda acorda, para que o próximo não passasse pelo mesmo.
- O **Henrique**, sozinho na sala de dados do bunker, vê o campus pelas **câmeras** e passa o que vê **pelo rádio para a Clarice e a Diana**, não direto para Gabriel. Diz que está tentando consertar tudo, e foi ele quem disse ao grupo que estão em 3026 (ele sabe pelo Carlos). Fala pouco e fica na dele. As dicas de patrulha que passa são verdadeiras, e é assim que ganha a confiança do grupo; ao mesmo tempo, **mantém cada um no seu canto**, e tudo o que o grupo sabe passa por ele (seção 8, "A virada").
- **Clarice e Diana**, da 103, também falam pela frequência e estão em contato com o **Henrique**: ele confere o campus nas câmeras e conta o que vê, e elas juntam isso com o que descobrem. A **Clarice é a voz que guia Gabriel pelo rádio**, desde a Biblioteca e depois no Bloco de salas, com as dicas de patrulha que vêm das câmeras do Henrique, e é ela quem conta a Gabriel que fala com ele.
- O **Baltazar** teve dificuldade com o rádio e com a tecnologia de 3026, ficou com medo e **se isolou**: não está na frequência. Ouve as vozes nas "caixas que falam" pelos corredores do subsolo e não responde. Gabriel só fala com ele em pessoa.

- Os esconderijos funcionam como pontos de encontro: Gabriel volta a eles para conversar e acompanhar o que cada um descobriu.

---

## 7. Linha do tempo

### 7.1 Quem esteve no ponto

| Ano | Quem | O que fazia ali |
|---|---|---|
| ~1750 | Baltazar | Viu uma luz estranha pela luneta, no sítio da família, e foi investigar |
| 1978 | Diana | Estudante de Direito: estava numa aula chata de Direito Penal, quase caindo na mesa, quando do nada apareceu na Biblioteca de 3026 |
| 1990 | Clarice | Rodava um programa num terminal da Biblioteca, de madrugada |
| 2019 | Henrique | Estudava à noite na Biblioteca, na pesquisa dele sobre viagem no tempo |
| 2026 | Gabriel | Dormiu na Biblioteca com o caderno aberto |
| 2123 | Zane | *A definir* |

### 7.2 Ordem dos acontecimentos

1. **Antes do jogo:** a sociedade e o planeta ficam muito ruins. A humanidade se divide, e os *Homo sideralis* vão embora para outro planeta, há menos de 100 anos. Os *sapiens* que ficam formam os **Faroleiros**.
2. **O Carlos sai dos Faroleiros** e se isola na Unifor. Passa anos sozinho, constrói a Âncora no D-Tec e toma o controle dos robôs.
3. **3026:** o Carlos começa a tentar ir para os anos 80. A cada tentativa, a fenda se abre no chão da Biblioteca.
4. **O primeiro puxado é o Henrique.** O Carlos promete levá-lo para antes da morte da mãe e passa a usá-lo.
5. **Os outros pulsos:** com 3 dias de intervalo entre um e outro, a fenda puxa uma pessoa de cada época. Cada uma acorda sozinha, foge dos robôs e acha um canto para sobreviver. Todos chegam antes de Gabriel. O Zane chega antes da Clarice, e a Diana depois da Clarice.
6. **O jogo:** Gabriel, o último, acorda na Biblioteca, encontra os outros um a um, descobre o que aconteceu e tenta consertar a Âncora para todos voltarem.

**Em 2026, o sumiço do Henrique virou lenda do campus:** um aluno que sumiu na Biblioteca em 2019. A pesquisa dele sobre viagem no tempo, que ele estava fazendo quando foi puxado, foi levada adiante pelo orientador e virou a cadeira de **Modelagem e Simulação**, a que Gabriel cursa: as equações do caderno de Gabriel vêm dela, sem ele saber de quem eram. Gabriel conhece a lenda, e por isso reconhece o Henrique quando o encontra.

---

## 8. Estrutura da história

> **Sequência oficial de fases (2026-10-16):** **Biblioteca → Bloco de salas → Labirinto → Centro de Convivência → Bunker → Laboratório (D-Tec)**.

### Ato 1 — Acordar (Biblioteca)

**Fase confirmada como primeira.** [`../fases/biblioteca.md`](../fases/biblioteca.md).

- **Cutscenes de abertura:**
  - **Prólogo ilustrado** (`seg_prologo`, aprovada): ilustrações sequenciais em pixel art retratando a rotina comum de Gabriel em 2026 (acordar, anel da avó, trajeto na Washington Soares, campus vivo da Unifor, aula de cálculo com o caderno de equações, até cair no sono de madrugada na cabine da Biblioteca antes da fenda se abrir).
  - **O despertar** (`seg_acordar`, pronta, um vídeo curto): Gabriel desperta na cabine de estudo, mil anos depois. A cabine e a biblioteca em volta já têm a tecnologia de 3026: painéis com luz ciano, um holograma aceso sobre o caderno, torres de equipamentos entre as estantes. Ele esfrega os olhos e olha em volta sem entender onde está.
- Gabriel acha a **lanterna** perto de onde acorda, e **pilhas** pelo salão. O **anel da avó** já está no inventário.
- **Acampamento de Baltazar** entre as raízes da árvore. Ele não está lá.
- **Terminal com o bilhete da Clarice:** pede que, se mais alguém chegou, a procure no Bloco de salas.
- **Rádio portátil:** no balcão, sintonizado na frequência do grupo (o Zane o deixou ali por causa da Clarice: seção 6.1). A voz da **Clarice** dá a primeira dica de patrulha, com o que o **Henrique** vê pelas câmeras.
- **Saída:** a porta no fim da ala leste leva ao Bloco de salas.

- **O telefone:** no fim da fase, o telefone do balcão toca. É o **Zane**, que destranca pelo sistema a porta de saída.

O jogador aprende aqui as regras do jogo (silêncio, esconderijos, bateria) e que **não está sozinho**: outras pessoas caíram ali antes dele.

### Ato 2 — Encontrar os outros (Bloco de salas, Labirinto e Centro de Convivência)

- **Bloco de salas** ([`../fases/bloco_de_salas.md`](../fases/bloco_de_salas.md)): dois andares, 12 salas de aula, noite. É onde fica o esconderijo da **Clarice** e da **Diana**, a **sala 103**, atrás de uma barricada. A Clarice foi para lá depois de chegar à Biblioteca; a Diana apareceu depois e foi acolhida por ela. Desde então as duas tentam descobrir o que aconteceu, com a ajuda do Henrique pelo rádio, e a Clarice conta isso a Gabriel. Gabriel ganha a confiança dela devolvendo o molho de chaves que ela perdeu (para ela, é uma permuta, não um pedido de ajuda); daí em diante a Clarice o guia pelo rádio (o que cada chave abre, por onde os robôs passam, que ela mapeou como um grafo) e fica no posto quando Gabriel sai pela porta corta-fogo do 1º andar. A saída, a porta corta-fogo do 1º andar, leva à próxima fase, o **Labirinto**.
- **Labirinto** ([`../fases/labirinto.md`](../fases/labirinto.md)): a terceira fase. Subsolo escuro do centro de pesquisa da Âncora, com seis robôs patrulhando corredores que se cruzam. Gabriel entra no subsolo e, a poucos passos, chega à **oficina do Zane**: uma sala cheia de componentes eletrônicos, desorganizada, com telas holográficas, a base do Zane. O Zane quer resolver tudo aquilo e **desconfia do Henrique**: está há dias tentando invadir o bunker, onde o Henrique fica, e não consegue de longe. Então entrega a Gabriel o **notebook** dele e pede que invada **três nós de controle**, em três salões espalhados pelo labirinto (cada salão tem uma entrada só). Os três nós guardam a trava que lacra o bunker. Quando o terceiro cai, o Zane chama Gabriel de volta pelo rádio e, na oficina, mostra a saída: um **alçapão escondido sob uma lona**, cujo duto sobe para a passarela do **Centro de Convivência**. No meio do labirinto há uma sala opcional, o **Corredor do Tempo**: quatro salinhas onde quem construiu a Âncora testava a calibração com objetos dos anos 80. Gabriel precisa alinhar os quatro mecanismos antes que um relógio zere; quem vence encontra a Folha de calibração, assinada só "C." (seção 4.3).
- **O esconderijo do Baltazar (Labirinto):** num canto do labirinto, atrás de um **painel solto** na parede, fica o esconderijo do **Baltazar**. O painel parece parede: só aparece com a **lanterna apontada** para ele, riscado com o **Cruzeiro do Sul** e uma **cruz** (as marcas que o Baltazar fez para achar a própria porta). Dentro, uma sala bagunçada: cama de panos, um altar de velas, livros trazidos da Biblioteca, um robô desmontado e uma chapa com o céu de casa riscado a giz. É ali o **primeiro encontro** de Gabriel com ele. O Baltazar se assusta, pergunta se é o fim do mundo, conta que seguiu a luz até o subsolo e **não quer sair**: lá fora andam os robôs, e ali dentro eles não entram. Gabriel diz só o primeiro nome, e o parentesco **ainda não aparece** nesse encontro.
- **Centro de Convivência** ([`../fases/centro_de_convivencia.md`](../fases/centro_de_convivencia.md)): a quarta fase, entre o Labirinto e o Bunker. Gabriel atravessa o pátio aberto sob o luar, sem nenhum personagem em pessoa no local, sendo guiado pelo **Zane pelo rádio**. Ele encontra a Sala Segura no Posto de Manutenção, busca a **Célula de Energia** na câmara da Cantina (contornando os cacos de vidro e o Rastreador), resolve o **Puzzle de Coloração de Grafos** no comutador da Gráfica Rápida (o que acende os holofotes perimetrais do pátio) e abre a comporta da **Rampa do Subsolo** que desce para o **Bunker**.
- **Rádio e telefone:** a Clarice fala pelo rádio na Biblioteca e no Bloco de salas, e o Zane mantém a frequência da oficina, ligando pelos telefones velhos e guiando Gabriel pelo rádio no Labirinto e no Centro de Convivência. A frequência é aberta: a Diana, a Clarice e o Zane conversam entre si e com Gabriel. O Henrique não fala nela: o que ele diz chega pela Clarice (seção 6.1).
- **Alguém de 1750:** no Labirinto, Gabriel conta pelo rádio do acampamento e do diário que achou na Biblioteca. Ninguém na frequência é de 1750: o grupo descobre que há mais alguém no campus, sozinho e fora da rede. Esse alguém é o Baltazar, escondido numa sala secreta do próprio Labirinto (Ato 2); se e como o grupo o traz para junto fica pendente (seção 10.4).
- **O anel:** Gabriel conhece o Baltazar no Labirinto, mas o parentesco fica para depois: em algum ponto, ele compara os dois anéis e descobre (seção 10.5).

### Ato 3 — O esconderijo (Bunker)

**Quinta fase.** [`../fases/bunker.md`](../fases/bunker.md).

- O bunker de pesquisa embaixo do núcleo da Âncora ("ÂNCORA-03"), com dois setores. É difícil de alcançar, e **os robôs patrulham aqui também**.
- **As salas antigas:** no bunker há **duas** salas montadas como **interiores de casa**: a **sala de visitas de um casarão do fim do século XIX** e a **sala de estar de uma casa dos anos 80**. Mostram a obsessão do Carlos pelo passado, **sem explicar**: o jogo não diz quem as montou nem por quê.
- **As marcas dos Faroleiros:** nas paredes do bunker há marcas dos Faroleiros pintadas em âmbar (seção 2.4): o farol inteiro perto da sala segura e o farol apagado perto da comporta do núcleo. Os Faroleiros passaram por ali; o jogo não diz quando.
- **De onde Gabriel chega aqui:** pela rampa técnica do subsolo aberta no fim do **Centro de Convivência**.
- **O Gabriel já encontrou o Zane em pessoa no Labirinto**. O **Henrique** fica **sozinho** numa sala de dados **trancada**, com o acesso às câmeras do campus, e é quem Gabriel encontra em pessoa aqui. Gabriel o reconhece pela lenda: é o aluno que sumiu em 2019 (seção 7.2). O Carlos nunca vai ao bunker.
- **O encontro (fim da fase):** Gabriel religa a energia do bunker e, com ela, o **Zane quebra a senha do setor B**. Na sala de dados, o grupo se encontra **pela primeira vez numa sala só**: Gabriel, o Henrique, o Zane, a Clarice e a Diana. Dali descem pela comporta do núcleo. **A cena é provisória:** o conteúdo da conversa (rascunho em `dados/dialogos/bunker_encontro.json`) e como a Clarice e a Diana chegam ao bunker ficam em aberto para o grupo mudar.
- O **setor B** (laboratório, arquivo e a comporta do núcleo) leva à reta final: a comporta no fim do Corredor B abre o acesso à sexta fase, o **Laboratório (D-Tec)**.

### A virada — A mentira do Henrique

- O **Henrique** engana o grupo: **trabalha para o Carlos**. Quando caiu, o primeiro de todos, o Carlos prometeu levá-lo de volta **para antes da morte da mãe dele**, e ele aceitou. O Carlos só o usa: a função do Henrique é **atrasar os outros** enquanto o Carlos conserta a Âncora para si.
- **O que ele esconde:**
  - a ligação com o Carlos e a promessa;
  - que **não está consertando nada** para o grupo, embora diga que está;
  - que usa a **IA de 3026** para continuar a própria pesquisa sobre viagem no tempo, **só para ele**: para voltar a antes da morte da mãe.
- **Como atrasa sem parecer sabotador:** as dicas de patrulha são verdadeiras (é assim que ganha a confiança), mas ele mantém cada um no seu canto, e tudo o que o grupo sabe passa por ele. Quando Gabriel liga o elevador do Centro de Convivência, o Henrique pede, pela Clarice, que ele não desça ao bunker. **O Henrique divide, o Gabriel une** (seção 3.1).
- **O que é verdade no que ele conta:** está mesmo no bunker, e estão mesmo em 3026 (ele sabe pelo Carlos). É mentira que esteja tentando consertar tudo.
- **O Zane já desconfia dele** desde antes de Gabriel chegar, e é por isso que tenta invadir o bunker (Labirinto, Ato 2).
- Em algum momento, o grupo **descobre a mentira** (como e quando: seção 10.3).
- É aí que todos **vão atrás do Carlos**, no D-Tec.

### Ato 4 — Consertar a Âncora e voltar (Núcleo)

- A reta final passa pela **comporta do núcleo**, no setor B do bunker.
- Com as partes de todos reunidas, Gabriel e os outros tentam consertar a Âncora e mandar cada um para a sua noite.
- **O Zane:** o final dele está pendente (seção 10.4). O final antigo (ficar em 3026 para domar a IA) saiu, porque a IA não tem consciência.
- **O Baltazar volta para 1750**, mesmo querendo ficar: Gabriel precisa convencê-lo (seção 5).
- **O Carlos:** como o grupo o enfrenta, sem lutar, está pendente (seção 10.2).
- Como isso acontece e como o jogo termina está nas pendências (seção 10.6).

---

## 9. Vocabulário oficial

Para qualquer texto do jogo ou da documentação:

| Use | Não use |
|---|---|
| **Âncora** (a máquina) | "Ankhor" para a máquina. Ankhor é o nome do jogo |
| **Fenda** (temporal) | "portal" |
| **Carlos** (o antagonista) | — |
| **D-Tec** (a parte de tecnologia da Unifor, no Bloco M, onde ficam a Âncora e o laboratório do Carlos) | — |
| **IA** (uma ferramenta, sem consciência: seção 2.1) | um nome próprio, ou falar dela como se pensasse ou quisesse algo |
| ***Homo sideralis*** (a espécie que foi embora; em itálico, com *sideralis* em minúscula) | "alienígenas", "os evoluídos" como termo oficial |
| ***sapiens*** (os humanos não evoluídos, como o Carlos, os Faroleiros e todos os puxados) | — |
| **Faroleiros** (a resistência que ficou na Terra) | "a resistência" como nome próprio |
| **Robôs** (os inimigos) | "Insones", "Bibliotecária", "Calouros", "Vigia" (premissa antiga) |
| **Lanterna a pilha** e **luzes de emergência** | "fungos", "pote de fungos" |
| **Antecessores** (quem caiu antes de Gabriel) | "viajantes" ou "vítimas" como termo oficial |
| **Cápsula de clarão** | "granada" |
| **Caderno do Gabriel** | "diário" para o caderno dele (o diário é o do Baltazar) |
| **Bunker** (embaixo do núcleo da Âncora) | — |

---

## 10. Pendências: o que falta decidir na história

Nada aqui está decidido. Cada item é uma **pergunta sobre a história** que o grupo ainda precisa responder. Quando uma for decidida, a resposta entra no texto acima e em `decisoes.md`, e a pergunta sai daqui. Não invente resposta para uma pendência: pergunte ao Davi.

O que falta fazer em arte, mecânica e fases (e não muda a história) fica em [`../pendencias_de_producao.md`](../pendencias_de_producao.md).

### 10.1 O mundo de 3026

- Há quantos anos exatamente os *Homo sideralis* partiram (sabemos que foi há menos de 100), e para onde foram?
- Onde estão os Faroleiros hoje? Eles aparecem no jogo (em pessoa, por rádio, ou só pelas marcas no cenário)? Sabem do Carlos e da Âncora?
- Como a Unifor virou um centro de pesquisa em física do tempo?
- Por que a fenda se abre sempre no chão da Biblioteca?
- Por que a rede do subsolo é fechada para o Zane, a ponto de ele não conseguir invadi-la de longe?
- Por que a sala 205 do Bloco de salas está intacta?

### 10.2 O Carlos

- Como ele consegue o conhecimento que falta para a Âncora funcionar? (A IA é uma ferramenta sem consciência e pode ser parte da resposta.)
- Quantas ferramentas de IA ele usa, e o que cada uma faz (os robôs, a Âncora, os sistemas do D-Tec)?
- Por que os robôs caçam os humanos: para capturar e levar ao Bloco M, ou para eliminar quem atrapalha?
- Qual a idade dele, como fala, o que teme, qual o defeito e qual o arco?
- Por que ele saiu dos Faroleiros, e há quantos anos está sozinho?
- Quando o jogador descobre que ele existe?
- Como o grupo o enfrenta sem lutar (Gabriel não é combatente)? O D-Tec é o último lugar do jogo?

### 10.3 O Henrique e a mentira

Já decidido (seção 8, "A virada"): ele trabalha para o Carlos por causa da promessa sobre a mãe, o Carlos só o usa para atrasar o grupo, ele finge consertar tudo e usa a IA na própria pesquisa.

- Como e quando o grupo descobre a mentira, e que papel tem nisso a desconfiança do Zane?
- O que o Henrique faz depois que a mentira aparece: como assume a responsabilidade (o arco dele)? Ainda tenta voltar para antes da morte da mãe?
- Como e quando a mãe dele morreu?
- Onde a lenda do aluno que sumiu em 2019 aparece para o jogador (no prólogo, numa conversa, num cartaz do campus)?

### 10.4 Os outros personagens

- **Zane:** o que fazia no ponto quando foi puxado? Qual é o final dele (ficar em 3026 para guardar a Âncora, ficar para se juntar aos Faroleiros, ou voltar para 2123)? As falas dele no bunker (a chamada pelo rádio e o encontro) são rascunho.
- **Baltazar:** em que posição da ordem de chegada ele está? (Já decidido: o Henrique é o primeiro, o Zane vem antes da Clarice, a Diana depois da Clarice, e Gabriel é o último; não precisa seguir a ordem dos anos. Cada chegada vem 3 dias depois da anterior, então a posição dele muda quantos dias cada um está lá.) Já decidido: o esconderijo dele é a sala secreta do Labirinto, e o primeiro encontro é lá. Hoje a sala é secreta, então o encontro é **opcional**: ele precisa ser obrigatório, já que o Baltazar traz as estrelas para consertar a Âncora? Como ele sai do esconderijo e se junta ao grupo? E a sala de obras raras da Biblioteca, barrada por dentro, que era a candidata ao esconderijo dele: quem (ou o quê) está do outro lado agora?
- **Clarice e Diana:** já decidido que se juntam ao grupo no encontro do fim do Bunker (Ato 3). Como chegam até lá, e o que fazem depois?
- **Gabriel:** enquanto o Baltazar está fora de 1750, o Gabriel começa a falhar (piscar, se desfazer), como a foto em *De Volta para o Futuro*? (Se sim, vira um shader, bom para a apresentação de Computação Gráfica.)

### 10.5 A estrutura da história

Já decidido: **Biblioteca → Bloco de salas → Labirinto → Centro de Convivência → Bunker → Laboratório (D-Tec)**.

- Por onde Gabriel chega do Bloco de salas ao subsolo do Labirinto?
- Em que momento Gabriel descobre o parentesco com o Baltazar? (O primeiro encontro já é no Labirinto, Ato 2.)
- O que os sonhos mostram, agora que não há loops (memória de cada um, o passado do campus, outra coisa)?

### 10.6 A volta e o fim

- Como cada um volta: todos de uma vez no final, ou um por um, conforme a Âncora vai sendo consertada?
- Qual é o final de Gabriel e Clarice? O final antigo ("A mesma madrugada": os dois acordam juntos em 2026, e ela rasga a página das equações) foi escrito para a versão com loops e precisa ser revisto.
- O que acontece com o Carlos no fim?
- O que acontece com o Henrique no fim?
