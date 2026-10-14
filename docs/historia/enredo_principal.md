# Enredo Principal

> [!IMPORTANT]
> **Este documento é a lei do projeto**, junto com as fichas de [`personagens/`](personagens/) (uma por personagem), que fazem parte dele. Tudo o que diz respeito à história, ao mundo e aos personagens de **Ankhor** vale como está escrito aqui e nas fichas, **acima de qualquer outro documento**: GDD, fases, diálogos, arte, textos em `dados/` e o próprio `decisoes.md`. Em caso de dúvida em qualquer parte do jogo (o que uma fase conta, como um personagem fala, o que um objeto significa), consulte este documento e a ficha do personagem. Se outra parte do projeto contradisser o que está aqui, **a outra parte está errada** e deve ser corrigida.

> **Status:** reescrito em 2026-10-06, quando a história mudou de rumo: saíram os loops e a revelação de "Gabriel é o paradoxo", e a fenda passou a ser **um acaso** para quem cai nela. Em 2026-10-07 entrou o antagonista, o **Carlos**.
> **Como mudar:** só por decisão do grupo. Toda mudança de história entra **no mesmo PR** neste documento e em [`../decisoes.md`](../decisoes.md) (que guarda o histórico de quando e por que mudou). Tudo o que ainda não foi decidido fica na **seção 12 ("Pendências")**, no fim, e não no meio da narrativa: o que está fora das pendências está decidido.

---

## 1. A história em um parágrafo

Numa madrugada de 2026, o estudante **Gabriel Magalhães** pega no sono na Biblioteca da Unifor e acorda no ano de **3026**, no mesmo lugar, agora uma ruína tomada pela natureza. A sociedade e o planeta ficaram tão ruins que o pouco que sobrou da humanidade foi embora para outro planeta. Um homem ficou: **Carlos**, um cientista obcecado pelos **anos 80**, que construiu uma máquina no **D-Tec**, a parte de tecnologia da Unifor, no Bloco M: a **Âncora**, para ir viver naquela época. A Âncora é imprecisa: a cada tentativa do Carlos, abre uma **fenda** no tempo no chão da Biblioteca e puxa quem estiver naquele ponto, em alguma época. Para quem cai, **é um acaso**: o Carlos não escolhe ninguém. Gabriel não é o único: outros jovens de épocas diferentes caíram ali com dias de diferença, e cada um está tentando sobreviver num canto do campus. Os robôs, controlados pelo Carlos, caçam qualquer humano que aparecer. Gabriel precisa encontrar os outros, descobrir o que aconteceu e achar um jeito de todos voltarem para suas épocas. No caminho descobre que um deles é seu antepassado, que outro mente para o grupo, e que por trás de tudo existe alguém.

---

## 2. O mundo

### 2.1 A Terra em 3026

- **A Terra ficou muito ruim**: a sociedade e o planeta. Por isso, o pouco que sobrou da humanidade **foi embora para outro planeta**. Quase não restam humanos na Terra.
- **O Carlos ficou**, para usar a Âncora e ir viver nos anos 80 (seção 4.3).
- **A IA:** versões anteriores desta história diziam que uma IA dominou a Terra. Se ela continua existindo, e qual a relação dela com o Carlos, está pendente (seção 12.2).

### 2.2 O campus em 3026

- A **Unifor, em Fortaleza**, mil anos depois. Em algum momento virou um centro de pesquisa em física do tempo.
- A **Âncora** e o laboratório do **Carlos** ficam no **D-Tec**, a parte de tecnologia da Unifor, no **Bloco M**.
- Concreto rachado e desabado, árvores dentro das salas, dunas sobre os corredores, mato onde era estacionamento. Não há cidade em volta, só vegetação. Resistem as coisas duras: concreto, metal, vidro, pedra.
- Objetos do cotidiano de hoje (catraca, bebedouro, quadro de horários, a cantina) viraram relíquias. O choque do jogo é perceber **quanto tempo passou**.
- **A eletricidade funciona normalmente.** Onde algo está apagado numa fase (como a grade da Biblioteca antes de religar os disjuntores), é um circuito desligado ou quebrado, não falta de energia.

### 2.3 Os robôs

- Os inimigos são **robôs** controlados pelo **Carlos**, que patrulham o campus por **rotinas programadas**. Repetem o mesmo caminho há séculos: dá para decorar.
- Fora da rotina, quando ouvem ou veem um humano, saem do protocolo e caçam. Por que caçam (para capturar ou para eliminar) está pendente (seção 12.2).
- São agressivos: se pegam Gabriel, é **game over** e o jogo volta ao último checkpoint (ver [`../mecanicas/vida_e_checkpoint.md`](../mecanicas/vida_e_checkpoint.md)).
- Cada tipo tem um sentido dominante (som, visão, luz). Os dois já implementados são a **Sentinela** (visão) e o **Rastreador** (audição). Ver [`personagens/robos.md`](personagens/robos.md).
- Gabriel não é um combatente: **fugir e se esconder é a regra**, defender-se é a exceção.

---

## 3. A Âncora e a fenda

| | |
|---|---|
| **O que é a Âncora** | **Só uma máquina.** Um aparelho experimental de física do tempo. Não pensa, não quer nada, não escolhe ninguém |
| **Onde está a Âncora** | No **D-Tec**, a parte de tecnologia da Unifor, no Bloco M, junto do laboratório do Carlos |
| **Quem criou** | O **Carlos** (seção 4.3), para ir viver nos anos 80 |
| **O que aconteceu** | O Carlos tenta usar a Âncora para ir para os anos 80, mas a máquina é **imprecisa**: não acerta a época nem escolhe quem puxa. Cada tentativa abre uma fenda no tempo |
| **Onde a fenda se abre** | Sempre no mesmo ponto: o chão onde hoje fica a Biblioteca (ou onde ela ainda viria a ser construída) |
| **Como a fenda age** | **Pulsa.** A cada tentativa do Carlos, a cada poucos dias, encosta numa época diferente e puxa quem estiver no ponto naquela noite. A cada pulso fica maior |
| **Por que essas pessoas** | **Acaso.** O Carlos não escolhe quem a fenda puxa: estavam no lugar errado na noite errada |
| **A ameaça** | Enquanto o Carlos continuar tentando, gente nova continua caindo, e a fenda continua crescendo |
| **Nome** | O aparelho se chama **Âncora**. **Ankhor** é o nome do jogo. Os dois não se confundem |

Os personagens não sabem nada disso no começo. Descobrir o que é a Âncora, quem está por trás dela e como consertá-la é o que move a história.

### 3.1 Como voltar: cada um traz uma parte

Para mandar cada pessoa de volta para a sua noite, é preciso consertar a Âncora, e ninguém sabe fazer isso sozinho. Cada personagem que Gabriel encontra contribui com uma parte. Isso dá a estrutura do jogo: **em cada fase, achar alguém, ganhar a confiança da pessoa e receber a parte dela.**

| Quem | O que traz |
|---|---|
| Baltazar (1750) | As estrelas: o céu é o único relógio que não muda, e é por ele que se acerta a data de volta de cada um |
| Diana (1978) | Investigação: descobre onde fica o núcleo e as passagens até lá |
| Clarice (1994) | Código: faz os terminais da Âncora funcionarem. Mapeou as rondas dos robôs como um grafo e sabe o que cada chave abre |
| Henrique (2019) | A teoria por trás das equações |
| Zane (2123) | A tecnologia mais próxima da Âncora |
| Gabriel (2026) | O caderno, com as equações da cadeira |

---

## 4. Os personagens

**Quem cada personagem é** (história, personalidade, como fala, o que quer, o que teme, defeito, arco e relações) está na ficha dele, em [`personagens/`](personagens/). Cada ficha faz parte deste documento e tem a mesma autoridade. Falas, documentos, retratos, animações e sons de um personagem seguem a ficha dele.

### 4.1 Regras para todos

- Todos os puxados pela fenda têm **cerca de 20 anos**.
- Todos têm alguma **ligação com a região da Unifor**, além de terem sido puxados no chão da Biblioteca.
- Chegaram a 3026 **com dias de diferença**. Estão todos **vivos**, cada um sobrevivendo do seu jeito num lugar do campus, e Gabriel **encontra cada um ao longo do jogo**.
- **Ordem de chegada:** o **Henrique é o primeiro** a chegar, e **Gabriel é o último**. No meio: o **Zane** chegou antes da **Clarice**, e a **Diana** chegou depois da Clarice (apareceu na 103 quando a Clarice já estava lá). Só a posição do **Baltazar** ainda está pendente.

### 4.2 Fichas

| Época | Personagem |
|---|---|
| ~1750 | [Baltazar Magalhães](personagens/baltazar.md) |
| 1978 | [Diana](personagens/diana.md) |
| 1994 | [Clarice](personagens/clarice.md) |
| 2019 | [Henrique](personagens/henrique.md), o pesquisador |
| 2026 | [Gabriel Magalhães](personagens/gabriel.md) (protagonista) |
| 2123 | [Zane](personagens/zane.md) |
| 3026 | [Carlos](personagens/carlos.md) (antagonista) |
| 3026 | [Os robôs](personagens/robos.md) (inimigos) |

### 4.3 O Carlos, o antagonista

O antagonista é o **Carlos**, cientista de 3026 que criou a Âncora, ficou na Terra quando a humanidade partiu e controla os robôs. Quem ele é está na [ficha dele](personagens/carlos.md). O **Henrique** engana o grupo por causa dele (seção 8, "A virada"). Muita coisa sobre o Carlos ainda está pendente (seção 12.2).

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
| **Bunker**, embaixo do núcleo da Âncora. O maior e mais seguro: os robôs não descem lá | Zane, no computador da central de dados (depois do Labirinto: ver 12.3); Henrique, na mesma sala de dados, com as câmeras do campus e o rádio. Diz que está escondido ali, tentando entender tudo |
| **Labirinto**, numa oficina no começo do subsolo da Âncora | Zane, entre componentes eletrônicos jogados por todo lado e telas holográficas. Não consegue invadir de longe a rede do subsolo, e pede ajuda a Gabriel |
| **Biblioteca**, escondido numa sala que o jogador ainda não consegue abrir, com medo | Baltazar, isolado dos outros, ali desde que chegou |
| **Bloco de salas**, na sala 103, atrás de uma barricada | Clarice, que foi para lá depois de chegar à Biblioteca, e Diana, que apareceu depois e foi acolhida por ela. Desde então tentam descobrir o que aconteceu, com a ajuda do Henrique pelo rádio |
| **D-Tec**, no laboratório | Carlos, que nunca sai de lá |

### 6.1 Como eles se comunicam

- O **Zane**, do computador do bunker, faz a **comunicação de todos**: mantém a **frequência de rádio** do grupo e deixou um rádio sintonizado nela na **Biblioteca**, no balcão de atendimento, porque é lá que quem cai na fenda acorda. Ele também liga pelos telefones velhos do campus.
- O **Henrique**, da sala de dados do bunker, vê o campus pelas **câmeras** e passa o que vê **pelo rádio para a Clarice e a Diana**, não direto para Gabriel. Diz que está escondido ali, tentando entender tudo, e foi ele quem disse ao grupo que, de alguma forma, estão em 3026. Fala pouco e fica na dele, mesmo dividindo a sala com o Zane.
- **Clarice e Diana**, da 103, também falam pela frequência e estão em contato com o **Henrique**: ele confere o campus nas câmeras e conta o que vê, e elas juntam isso com o que descobrem. A **Clarice é a voz que guia Gabriel pelo rádio**, desde a Biblioteca e depois no Bloco de salas, com as dicas de patrulha que vêm das câmeras do Henrique, e é ela quem conta a Gabriel que fala com ele.
- O **Baltazar** teve dificuldade com o rádio e com a tecnologia de 3026, ficou com medo e **se isolou**: não está na frequência. Gabriel só fala com ele em pessoa.

- Os esconderijos funcionam como pontos de encontro: Gabriel volta a eles para conversar e acompanhar o que cada um descobriu.

---

## 7. Linha do tempo

### 7.1 Quem esteve no ponto

| Ano | Quem | O que fazia ali |
|---|---|---|
| ~1750 | Baltazar | Viu uma luz estranha pela luneta, no sítio da família, e foi investigar |
| 1978 | Diana | Vigiava a obra depois do sumiço do material |
| 1994 | Clarice | Rodava um programa num terminal da Biblioteca, de madrugada |
| 2019 | Henrique | Estudava à noite na Biblioteca |
| 2026 | Gabriel | Dormiu na Biblioteca com o caderno aberto |
| 2123 | Zane | *A definir* |

### 7.2 Ordem dos acontecimentos

1. **Antes do jogo:** a sociedade e o planeta ficam muito ruins, e o pouco que sobrou da humanidade vai embora para outro planeta. O Carlos fica e constrói a Âncora no D-Tec.
2. **3026:** o Carlos começa a tentar ir para os anos 80. A cada tentativa, a fenda se abre no chão da Biblioteca.
3. **Os pulsos:** com dias de diferença, a fenda puxa uma pessoa de cada época. Cada uma acorda sozinha, foge dos robôs e acha um canto para sobreviver. Todos chegam antes de Gabriel. O Henrique é o primeiro, o Zane chega antes da Clarice, e a Diana depois da Clarice.
4. **O jogo:** Gabriel, o último, acorda na Biblioteca, encontra os outros um a um, descobre o que aconteceu e tenta consertar a Âncora para todos voltarem.

---

## 8. Estrutura da história

> Já decidido: **Biblioteca → Bloco de salas → Labirinto** (2026-10-14). O Labirinto é a terceira fase e é nele que Gabriel encontra o Zane em pessoa. Por enquanto a saída do Labirinto abre a entrada do Bunker (o Ato 3 abaixo), de forma provisória. O Centro de Convivência deixou de ser a fase seguinte ao Bloco de salas e está sem lugar na ordem. Onde entram o Bunker, o Centro de Convivência e as outras áreas **não está decidido** (seção 12). Esta estrutura segue a lógica da história, não uma ordem de jogo travada.

### Ato 1 — Acordar (Biblioteca)

**Fase confirmada como primeira.** [`../fases/biblioteca.md`](../fases/biblioteca.md).

- **Cutscenes de abertura:**
  - **Prólogo ilustrado** (`seg_prologo`, aprovada): ilustrações sequenciais em pixel art retratando a rotina comum de Gabriel em 2026 (acordar, anel da avó, trajeto na Washington Soares, campus vivo da Unifor, aula de cálculo com o caderno de equações, até cair no sono de madrugada na cabine da Biblioteca antes da fenda se abrir).
  - **O despertar** (`seg_acordar`, pronta, um vídeo curto): Gabriel desperta na cabine de estudo, mil anos depois. A cabine e a biblioteca em volta já têm a tecnologia de 3026: painéis com luz ciano, um holograma aceso sobre o caderno, torres de equipamentos entre as estantes. Ele esfrega os olhos e olha em volta sem entender onde está.
- Gabriel acha a **lanterna** perto de onde acorda, e **pilhas** pelo salão. O **anel da avó** já está no inventário.
- **Acampamento de Baltazar** entre as raízes da árvore. Ele não está lá.
- **Terminal com o bilhete da Clarice.**
- **Rádio portátil:** sintonizado na frequência do grupo. A voz da **Clarice** dá a primeira dica de patrulha, com o que o **Henrique** vê pelas câmeras.
- **Saída:** a porta no fim da ala leste leva ao Bloco de salas.

- **O telefone:** no fim da fase, o telefone do balcão toca. É o **Zane**, que destranca pelo sistema a porta de saída.

O jogador aprende aqui as regras do jogo (silêncio, esconderijos, bateria) e que **não está sozinho**: outras pessoas caíram ali antes dele.

### Ato 2 — Encontrar os outros (Bloco de salas, Labirinto e demais áreas)

- Cada fase leva a **um personagem** e ao esconderijo dele. Gabriel precisa chegar lá, ganhar a confiança da pessoa e receber a parte dela para consertar a Âncora (seção 3.1).
- **Bloco de salas** ([`../fases/bloco_de_salas.md`](../fases/bloco_de_salas.md)): dois andares, 12 salas de aula, noite. É onde fica o esconderijo da **Clarice** e da **Diana**, a **sala 103**, atrás de uma barricada. A Clarice foi para lá depois de chegar à Biblioteca; a Diana apareceu depois e foi acolhida por ela. Desde então as duas tentam descobrir o que aconteceu, com a ajuda do Henrique pelo rádio, e a Clarice conta isso a Gabriel. Gabriel ganha a confiança dela devolvendo o molho de chaves que ela perdeu (para ela, é uma permuta, não um pedido de ajuda); daí em diante a Clarice o guia pelo rádio (o que cada chave abre, por onde os robôs passam, que ela mapeou como um grafo) e fica no posto quando Gabriel sai pela porta corta-fogo do 1º andar. A saída, a porta corta-fogo do 1º andar, leva à próxima fase, o **Labirinto**.
- **Labirinto** ([`../fases/labirinto.md`](../fases/labirinto.md)): a terceira fase. Subsolo escuro do centro de pesquisa da Âncora, com seis robôs patrulhando corredores que se cruzam. No começo fica a **oficina do Zane**: uma sala cheia de componentes eletrônicos, desorganizada, com telas holográficas. O Zane não consegue invadir a rede do subsolo de longe, então entrega a Gabriel o **notebook** dele e pede que invada **três nós de controle**, em três salões espalhados pelo labirinto (cada salão tem uma entrada só). Quando o terceiro cai, o Zane abre a porta de saída pelo rádio e diz que vai atrás depois. Decidido pelo Davi em 2026-10-14; o que os nós são exatamente é proposta (seção 12.5).
- **Centro de Convivência** ([`../fases/centro_de_convivencia.md`](../fases/centro_de_convivencia.md), ainda não feito): deixou de ser a fase seguinte ao Bloco de salas (2026-10-14) e está sem lugar na ordem. O que acontece nela, quem Gabriel encontra e o que ela ensina continua indefinido.
- As outras áreas do GDD (Espaço Cultural, NAMI, Reitoria) ainda não foram redefinidas para a premissa atual.
- **Rádio e telefone:** a Clarice fala pelo rádio, na frequência que o Zane mantém, com o que o Henrique vê nas câmeras, e o Zane liga pelos telefones velhos.
- **O anel:** em algum ponto deste ato, Gabriel encontra o Baltazar e descobre o parentesco.

### Ato 3 — O esconderijo (Bunker)

**Fase em desenvolvimento.** [`../fases/bunker.md`](../fases/bunker.md).

- O bunker de pesquisa embaixo do núcleo da Âncora ("ÂNCORA-03"), com dois setores. Os robôs não descem aqui.
- **De onde Gabriel chega aqui não está decidido.** Por enquanto a saída do Labirinto abre a entrada do bunker, de forma provisória (seção 12.5).
- **O Gabriel já encontrou o Zane em pessoa no Labirinto**, e o Zane disse que ia atrás dele depois. O que o Zane faz na central de dados quando Gabriel chega está pendente (seção 12.3). O **Henrique** fica na sala de dados, com o acesso às câmeras do campus, e é quem Gabriel encontra em pessoa aqui.
- O **setor B** (laboratório, arquivo e a comporta do núcleo) está lacrado pelo sistema, e o Zane tenta quebrar a senha.
- Seis portas lacradas são os ganchos para as próximas fases: escotilha da superfície, elevador, arsenal, laboratório, arquivo e a comporta do núcleo.

### A virada — A mentira do Henrique

- O **Henrique** engana o grupo: esconde a ligação que tem com o **Carlos**. Ou trabalha para ele, ou foi enganado por ele (pendente, seção 12.7).
- Em algum momento, o grupo **descobre a mentira**.
- É aí que todos **vão atrás do Carlos**, no D-Tec.

### Ato 4 — Consertar a Âncora e voltar (Núcleo)

- A reta final passa pela **comporta do núcleo**, no setor B do bunker.
- Com as partes de todos reunidas, Gabriel e os outros tentam consertar a Âncora e mandar cada um para a sua noite.
- **O Zane escolhe ficar.** Voltar para 2123 é voltar para o mundo que vai virar o da IA. Fiel ao defeito dele (acha que toda máquina tem conserto), ele decide ficar em 3026 para tentar domar a IA por dentro. Um final agridoce que não tira o final dos outros. (Depende de a IA continuar existindo: seção 12.2.)
- **O Baltazar volta para 1750**, mesmo querendo ficar: Gabriel precisa convencê-lo (seção 5).
- **O Carlos:** como o grupo o enfrenta, sem lutar, está pendente (seção 12.5).
- Como isso acontece e como o jogo termina está nas pendências (seção 12).

---

## 9. Temas e tom

- **Estranhamento do familiar:** o jogador reconhece a catraca, o bebedouro, a Biblioteca. O mundo em volta não reconhece mais nada disso.
- **Gente de épocas diferentes:** jovens da mesma idade e do mesmo lugar, separados por séculos, tentando se entender (gírias, costumes, tecnologia).
- **Família e origem:** Gabriel descobre que a família dele sempre esteve naquele chão.
- **Tempo como relógio mortal:** os robôs seguem rotinas, e quem aprende a rotina sobrevive.
- **Vulnerabilidade:** Gabriel é um estudante, não um soldado.
- Terror silencioso, de tensão e mistério, mais do que de susto. O maior choque é perceber **quanto tempo passou**.
- **Público:** 14+, sem violência explícita. Os lugares da Unifor são só cenário; pessoas, pesquisa e acontecimentos são fictícios.

---

## 10. Como a história chega ao jogador

| Camada | O que é | Onde está |
|---|---|---|
| **Narrativa ambiental** | Marcas no cenário, relíquias de épocas diferentes, os tracinhos nas lousas, os riscos de estrelas na árvore | [`../fases/`](../fases/) |
| **Documentos** | Diários, bilhetes, disquetes. Cada época tem um papel próprio. As pistas úteis viram anotações no **Caderno do Gabriel** | [`../mecanicas/registros_e_caderno.md`](../mecanicas/registros_e_caderno.md) e o modelo [`template_documento.md`](template_documento.md) |
| **Inventário** | O anel da avó, e a comparação com o anel do Baltazar | [`../mecanicas/itens_e_inventario.md`](../mecanicas/itens_e_inventario.md) |
| **Rádio** | Clarice ao vivo, na frequência do grupo, com o que o Henrique vê nas câmeras, sem pausar o jogo | [`../mecanicas/registros_e_caderno.md`](../mecanicas/registros_e_caderno.md) |
| **Ligações e diálogos** | Zane por telefone; todos em pessoa nos esconderijos, com retratos e escolhas | [`../dialogos/README.md`](../dialogos/README.md) |
| **Sonhos** | O sono continua como mecânica; o que os sonhos mostram está pendente | [`../mecanicas/sono_e_sonhos.md`](../mecanicas/sono_e_sonhos.md) |
| **Cutscenes** | A abertura (`seg_prologo` e `seg_acordar`) e as que o grupo decidir | [`roteiro/cutscenes/`](roteiro/cutscenes/) |

---

## 11. Vocabulário oficial

Para qualquer texto do jogo ou da documentação:

| Use | Não use |
|---|---|
| **Âncora** (a máquina) | "Ankhor" para a máquina. Ankhor é o nome do jogo |
| **Fenda** (temporal) | "portal" |
| **Carlos** (o antagonista) | — |
| **D-Tec** (a parte de tecnologia da Unifor, no Bloco M, onde ficam a Âncora e o laboratório do Carlos) | — |
| **IA** (se continuar existindo: seção 12.2) | um nome próprio, enquanto o grupo não decidir |
| **Robôs** (os inimigos) | "Insones", "Bibliotecária", "Calouros", "Vigia" (premissa antiga) |
| **Lanterna a pilha** e **luzes de emergência** | "fungos", "pote de fungos" |
| **Antecessores** (quem caiu antes de Gabriel) | "viajantes" ou "vítimas" como termo oficial |
| **Cápsula de clarão** | "granada" |
| **Caderno do Gabriel** | "diário" para o caderno dele (o diário é o do Baltazar) |
| **Bunker** (embaixo do núcleo da Âncora) | — |

---

## 12. Pendências

Nada aqui está decidido. Quando o grupo decidir algum item, ele vai para `decisoes.md` e sai desta lista.

### 12.1 A volta e o fim

- **Como cada um volta:** todos de uma vez no final, ou um por um, conforme a Âncora vai sendo consertada.
- **O final** de Gabriel e Clarice. O final antigo ("A mesma madrugada": os dois acordam juntos em 2026, e ela rasga a página das equações) foi escrito para a versão com loops e precisa ser revisto.

### 12.2 O Carlos, a Âncora e a IA

- **Como o Carlos consegue o conhecimento** que falta para a Âncora funcionar: roubando a consciência dos puxados, construindo uma super IA, ou as duas (a super IA feita das consciências roubadas).
- **A IA continua existindo?** Pode ser a super IA do Carlos, outra coisa que ele controla, ou sair da história. O arco do Zane (medo da IA, ficar para domá-la) depende disso.
- **O Carlos domina as IAs, e elas o ajudam?** Proposta do Davi: em vez de uma IA só, várias IAs, todas sob o controle do Carlos e trabalhando para ele. Falta decidir quantas são, o que cada uma faz (os robôs, a Âncora, os sistemas do D-Tec) e como ele as domina.
- **Por que os robôs caçam os humanos:** para capturar e levar ao Bloco M, ou para eliminar quem atrapalha.
- **O Carlos:** idade exata, como fala, o que teme, defeito e arco; e **quando o jogador descobre** que ele existe.
- **Quando a humanidade foi embora**, e como a Unifor virou um centro de pesquisa em física do tempo.
- **Por que a fenda se abre sempre na Biblioteca.**

### 12.3 Personagens

- **Gabriel falhando na tela:** enquanto o Baltazar estiver fora de 1750, o sprite de Gabriel pisca ou se desfaz, como a foto em *De Volta para o Futuro*. Seria um shader (bom para a apresentação de Computação Gráfica).
- **Henrique:** quando Gabriel o encontra em pessoa na sala de dados do bunker, e se o acesso às câmeras vira uma mecânica (ver o campus, avisar de ronda nova).
- **Clarice e Diana:** se as duas continuam na 103 até o fim ou se juntam ao grupo no bunker mais tarde (o final da Clarice com Gabriel está em 12.1). As pichações assinadas "C." no bunker ("NÃO CONFIE NAS LUZES") não combinam com a Clarice estar na 103 desde que chegou: falta decidir quem as fez ou se saem.
- **Diana na 103:** ela ainda não tem visual, então a cena da 103 mostra só a Clarice.
- **Zane:** o que fazia no ponto quando foi puxado.
- **Zane no Labirinto:** ele aparece em pessoa numa oficina no começo do Labirinto (decidido em 2026-10-14), e não só no bunker. Falta decidir como isso conversa com as seções 6 e 6.1 (o computador do bunker, a frequência de rádio): se a oficina é um segundo ponto dele, quando ele vai para o bunker (a conversa do fim do Labirinto diz que ele "vai atrás") e o que ele está fazendo na central de dados quando Gabriel chega lá.
- **Ordem de chegada:** só falta a posição do **Baltazar** (já decidido: o Henrique é o primeiro, o Zane vem antes da Clarice, a Diana depois da Clarice, e Gabriel é o último). Não precisa seguir a ordem dos anos.
- **Qual sala da Biblioteca** é o esconderijo do Baltazar (uma que o jogador ainda não consegue abrir; a sala de obras raras, barrada por dentro, é a candidata) e **quando ela passa a ficar acessível**. Ele está ali desde que chegou: o acampamento vazio do começo foi o primeiro abrigo dele, e a última página do diário ("Hei de seguir a luz até onde ella nasce") combina com ficar, porque a luz nasce no chão da Biblioteca (seção 3).

### 12.4 Textos já escritos que citam a versão antiga

- **O bunker:** as conversas `dados/dialogos/clarice_primeiro_encontro.json` e `clarice_de_novo.json` e a arte da estação de trabalho (`gerar_clarice.py`) foram feitas para a Clarice no computador da central de dados. A Clarice agora fica no Bloco de salas, e a cena do bunker mostra o **Henrique** na estação, com conversas novas (`henrique_primeiro_encontro.json` e `henrique_de_novo.json`). As conversas da Clarice, com as falas de loop ("Você sempre lê" e outras), ficaram sem uso e podem ser apagadas. Falta a cena do **Zane** na mesma sala de dados.
- [`../mecanicas/sono_e_sonhos.md`](../mecanicas/sono_e_sonhos.md): **o que os sonhos mostram** agora que não há loops (memória, o passado do campus, outra coisa).

### 12.5 Estrutura e fases

- **Ordem das fases:** onde entram o Bunker, o Centro de Convivência e as outras áreas, e qual personagem aparece em cada uma. Já decidido: Biblioteca → Bloco de salas → Labirinto. Por enquanto a saída do Labirinto abre a entrada do Bunker, de forma provisória.
- **Labirinto:** o que os três nós de controle são na história (a proposta atual: terminais da trava do sistema do subsolo, que lacra a saída e só lê de dentro), por que a rede do subsolo é fechada para o Zane, e por onde o Gabriel chega do Bloco de salas ao subsolo.
- **Bloco de salas:** por que a sala 205 está intacta. O objetivo e os robôs foram decididos em 2026-10-11 ([`../fases/bloco_de_salas.md`](../fases/bloco_de_salas.md)).
- **O que destrava o setor B do bunker** (senhas nos disquetes, religar o gerador) e se os robôs entram lá.
- **O D-Tec (Bloco M)** como fase: se é a última, e como o grupo enfrenta o Carlos sem lutar (Gabriel não é combatente).
- **Cenários mais futuristas.** Pedido do Davi: os cenários precisam mostrar mais a tecnologia de 3026 (telas, máquinas, a estrutura do centro de pesquisa e do D-Tec), misturada às ruínas e à vegetação. A cabine de estudo da Biblioteca já aparece assim no vídeo do despertar (`seg_acordar`). Falta decidir quanto do resto do campus tem esse visual futurista e onde ele aparece mais.
- **Redesenho das áreas do GDD** (Centro de Convivência, Espaço Cultural, NAMI, Reitoria) para a premissa da fenda. O Centro de Convivência perdeu o lugar de fase seguinte ao Bloco de salas (2026-10-14) e está sem lugar na ordem.
- **De onde vem a grade horária dos robôs.** Antes vinha da coloração de grafos da semana de provas; hoje a patrulha é programada (pelo Carlos ou pela IA: seção 12.2).

### 12.6 Mecânicas que dependem da história

- **Gadgets e personagens:** em que fase cada gadget aparece e se cada um vem de um personagem.

### 12.7 A mentira do Henrique

As perguntas que faltam responder sobre "A virada" (seção 8):

1. **O Henrique trabalha para o Carlos por vontade própria, ou foi enganado por ele?**
2. **O que exatamente o Henrique esconde do grupo?** (A ideia 12 de [`outras_ideias.md`](outras_ideias.md) é uma opção.)
3. **Como e quando o grupo descobre a mentira?**
4. **É verdade o que o Henrique conta?** Ele diz que está escondido no bunker, tentando entender tudo, e que, de alguma forma, estão em 3026. Falta decidir se isso é verdade ou parte do que ele esconde.
