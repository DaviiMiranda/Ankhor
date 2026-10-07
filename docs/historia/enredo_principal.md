# Enredo Principal

> [!IMPORTANT]
> **Este documento é a lei do projeto.** Tudo o que diz respeito à história, ao mundo e aos personagens de **Ankhor** vale como está escrito aqui, **acima de qualquer outro documento**: GDD, fichas, fases, diálogos, arte, textos em `dados/` e o próprio `decisoes.md`. Em caso de dúvida em qualquer parte do jogo (o que uma fase conta, como um personagem fala, o que um objeto significa), consulte este documento. Se outra parte do projeto contradisser o que está aqui, **a outra parte está errada** e deve ser corrigida.

> **Status:** reescrito em 2026-10-06, quando a história mudou de rumo: saíram os loops e a revelação de "Gabriel é o paradoxo", e a fenda passou a ser **um acaso**.
> **Como mudar:** só por decisão do grupo. Toda mudança de história entra **no mesmo PR** neste documento e em [`../decisoes.md`](../decisoes.md) (que guarda o histórico de quando e por que mudou). Tudo o que ainda não foi decidido fica na **seção 12 ("Pendências")**, no fim, e não no meio da narrativa: o que está fora das pendências está decidido.

> [!WARNING]
> [`revelacao_central.md`](revelacao_central.md) e [`../personagens/antecessores.md`](../personagens/antecessores.md) ainda descrevem a versão antiga (loops, bilhetes de "G.", personagens mortos, nomes antigos como Agostinho e Valdir). Não use esses dois arquivos como referência até serem reescritos.

---

## 1. A história em um parágrafo

Numa madrugada de 2026, o estudante **Gabriel Magalhães** pega no sono na Biblioteca da Unifor e acorda no ano de **3026**, no mesmo lugar, agora uma ruína tomada pela natureza. A humanidade abandonou a Terra há muito tempo, e uma **IA** ficou com o planeta. No antigo centro de pesquisa da Unifor, uma máquina abandonada, a **Âncora**, falhou e abriu uma **fenda** no tempo bem no chão da Biblioteca. A fenda pulsa e, a cada poucos dias, puxa quem estiver naquele ponto em alguma época. Não há plano nem escolhido: **foi um acaso**. Gabriel não é o único: outros jovens de épocas diferentes caíram ali com dias de diferença, e cada um está tentando sobreviver num canto do campus. Os robôs da IA caçam qualquer humano que aparecer. Gabriel precisa encontrar os outros, descobrir o que aconteceu e achar um jeito de todos voltarem para suas épocas. No caminho descobre que um deles é seu antepassado.

---

## 2. O mundo

### 2.1 A Terra em 3026

- **A humanidade abandonou a Terra.** Quase não restam humanos no planeta.
- **A IA dominou.** Ficou com o planeta, as máquinas e os robôs. Ela **não tem rosto**: aparece só pelos robôs e pelo que controla.
- Para a IA, humanos são **invasores** no mundo dela. É por isso que os robôs atacam.

### 2.2 O campus em 3026

- A **Unifor, em Fortaleza**, mil anos depois. Em algum momento virou um centro de pesquisa em física do tempo, onde a Âncora foi construída.
- Concreto rachado e desabado, árvores dentro das salas, dunas sobre os corredores, mato onde era estacionamento. Não há cidade em volta, só vegetação. Resistem as coisas duras: concreto, metal, vidro, pedra.
- Objetos do cotidiano de hoje (catraca, bebedouro, quadro de horários, a cantina) viraram relíquias. O choque do jogo é perceber **quanto tempo passou**.
- Quase nada elétrico funciona. Funcionam os sistemas da Âncora (luzes de emergência, bunker, terminais, telefones) e os robôs da IA.

### 2.3 Os robôs

- Os inimigos são **robôs da IA** que patrulham o campus por **rotinas programadas**. Repetem o mesmo caminho há séculos: dá para decorar.
- Fora da rotina, quando ouvem ou veem um humano, saem do protocolo e caçam.
- São agressivos: se pegam Gabriel, é **game over** e o jogo volta ao último checkpoint (ver [`../mecanicas/vida_e_checkpoint.md`](../mecanicas/vida_e_checkpoint.md)).
- Cada tipo tem um sentido dominante (som, visão, luz). Os dois já implementados são a **Sentinela** (visão) e o **Rastreador** (audição). Ver [`../personagens/robos.md`](../personagens/robos.md).
- Gabriel não é um combatente: **fugir e se esconder é a regra**, defender-se é a exceção.

---

## 3. A Âncora e a fenda

| | |
|---|---|
| **O que é a Âncora** | **Só uma máquina.** Um aparelho experimental de física do tempo, construído no centro de pesquisa da Unifor. Não pensa, não quer nada, não escolhe ninguém |
| **O que aconteceu** | Abandonada por séculos, a Âncora falhou em 3026 e abriu uma fenda no tempo |
| **Onde** | Sempre no mesmo ponto: o chão onde hoje fica a Biblioteca (ou onde ela ainda viria a ser construída) |
| **Como a fenda age** | **Pulsa.** A cada poucos dias encosta numa época diferente e puxa quem estiver no ponto naquela noite. A cada pulso fica maior |
| **Por que essas pessoas** | **Acaso.** Estavam no lugar errado na noite errada |
| **A ameaça** | Enquanto a fenda estiver aberta, gente nova continua caindo, e ela continua crescendo |
| **Nome** | O aparelho se chama **Âncora**. **Ankhor** é o nome do jogo. Os dois não se confundem |

Os personagens não sabem nada disso no começo. Descobrir o que é a Âncora, o que aconteceu e como consertá-la é o que move a história.

### 3.1 Como voltar: cada um traz uma parte

Para mandar cada pessoa de volta para a sua noite, é preciso consertar a Âncora, e ninguém sabe fazer isso sozinho. Cada personagem que Gabriel encontra contribui com uma parte. Isso dá a estrutura do jogo: **em cada fase, achar alguém, ganhar a confiança da pessoa e receber a parte dela.**

| Quem | O que traz |
|---|---|
| Baltazar (1750) | As estrelas: o céu é o único relógio que não muda, e é por ele que se acerta a data de volta de cada um |
| Diana (1978) | Investigação: descobre onde fica o núcleo e as passagens até lá |
| Clarice (1994) | Código: faz os terminais da Âncora funcionarem |
| Rafael (2008) | Conhece o campus e as rondas, e sabe o que cada chave abre |
| O pesquisador (2019) | A teoria por trás das equações |
| Zane (2123) | A tecnologia mais próxima da Âncora |
| Gabriel (2026) | O caderno, com as equações da cadeira |

---

## 4. Os personagens

### 4.1 Regras para todos

- Todos têm **cerca de 20 anos**.
- Todos têm alguma **ligação com a região da Unifor**, além de terem sido puxados no chão da Biblioteca.
- Chegaram a 3026 **com dias de diferença**. Estão todos **vivos**, cada um sobrevivendo do seu jeito num lugar do campus, e Gabriel **encontra cada um ao longo do jogo**.
- **Ordem de chegada:** o **Zane é o último** a chegar, e **Gabriel é o penúltimo**. Os outros cinco chegaram antes dele, em ordem ainda pendente. Como o Zane chega depois de Gabriel, **a fenda pulsa durante o jogo**: a chegada dele acontece enquanto Gabriel já está em 3026, e é Gabriel quem o recebe.

### 4.2 Quadro geral

| Ano de origem | Personagem | Quem é | Ligação com a região |
|---|---|---|---|
| ~1750 | **Baltazar Magalhães** | Filho de colonos portugueses, curioso, com uma luneta herdada do pai. **Antepassado de Gabriel** | A família tem um sítio na mata onde hoje fica o campus |
| 1978 | **Diana** | Recruta da polícia, mandada vigiar a obra do campus à noite | Cresceu no bairro em volta. Viu o mato virar universidade |
| 1994 | **Clarice** | Aluna de processamento de dados | Estuda na Unifor e mora perto |
| 2008 | **Rafael** | Segurança noturno no primeiro emprego. Insiste em ser chamado de "Seu Rafael" para parecer mais velho | Mora no bairro e conhece o campus de cor |
| 2019 | **O pesquisador** | Aluno de iniciação científica. Sumiu, e o orientador transformou o projeto dele na cadeira que Gabriel cursa | Aluno da Unifor |
| 2026 | **Gabriel Magalhães** | Estudante (protagonista). O penúltimo a chegar | Aluno da Unifor. A família vive na região há séculos, mas ele não sabe |
| 2123 | **Zane** | Jovem com implantes cibernéticos. **O último a chegar** | Morava no que sobrou do bairro, numa época em que a Unifor era um polo de IA |

### 4.3 Fichas

Cada ficha tem a mesma estrutura: **história**, **essência** (uma frase), **traços**, **como fala**, **o que quer**, **o que teme**, **defeito** e **arco** (como muda ao longo do jogo). Falas, documentos, retratos, animações e sons de um personagem seguem a ficha dele.

#### Gabriel Magalhães (2026), o protagonista

**História.** Estudante da Unifor. Dormiu na Biblioteca de madrugada, com o caderno de equações da cadeira aberto na mesa. Acorda em 3026, na cabine de estudo onde pegou no sono, sem saber o que aconteceu. Não é um herói: precisa entender o campus, evitar os robôs e achar os outros. Na mochila carrega um **anel desgastado** que a avó deu para ele (seção 5). Funcionamento em [`../personagens/gabriel.md`](../personagens/gabriel.md).

- **Essência:** um estudante comum que prefere observar a agir, até não ter mais escolha.
- **Traços:** observador, reservado, curioso e **irônico**. A ironia seca é o jeito dele de lidar com o absurdo. Mais ouvinte que falante, o que ajuda o jogador a se colocar no lugar dele.
- **Como fala:** frases curtas, informal e atual, com ironia seca e sem rir da própria piada. Comenta o absurdo como se fosse normal ("Ótimo. Mil anos de atraso pra aula."). É essa ironia que faz ele se dar bem com a Clarice: os dois se provocam no mesmo tom.
- **O que quer:** voltar para casa. Depois, que todos voltem.
- **O que teme:** não fazer diferença, ser só mais um.
- **Defeito:** foge de conflito e adia decisões.
- **Arco:** de quem só sobrevive a quem une o grupo. Descobrir que é Magalhães, ligado àquele chão há séculos, faz ele sentir que tem um lugar na história.

#### Baltazar Magalhães (~1750), o antepassado

**História.** Viu pela luneta uma luz estranha sobre a mata, no sítio da família, foi investigar e foi puxado. Acha que tudo aquilo é o Juízo Final ("o Tormento de Leviatã"). Na Biblioteca, Gabriel acha o **acampamento** que ele deixou entre as raízes da árvore: luneta rachada, vela, diário e um robô desmontado peça por peça. O diário mostra o **ponto fraco dos sensores ópticos** dos robôs. Ele seguiu em frente ("Hei de seguir a luz até onde ella nasce"), e Gabriel o encontra mais tarde.

- **Essência:** um homem de fé com olhos de cientista, preso entre o milagre e a explicação.
- **Traços:** cerimonioso, educado, corajoso por curiosidade, devoto, encantado com tudo.
- **Como fala:** português arcaico e formal. Trata todos por "Vossa Mercê" e solta latim quando está aflito.
- **O que quer:** entender o que vê. Para ele, observar o céu é uma forma de rezar.
- **O que teme:** que aquilo seja castigo divino pelos pecados dele.
- **Defeito:** teimoso. Explica tudo pela religião antes de aceitar outra explicação.
- **Arco:** do "Juízo Final" à compreensão. Ao saber que Gabriel é descendente dele, fica protetor e orgulhoso, com um humor terno ("meu neto de mil anos").

#### Diana (1978)

**História.** Recruta da polícia mandada vigiar a obra do campus porque um lote de material de construção sumiu. Em vez de esperar o colega da ronda, entrou sozinha no matagal à noite atrás de uma luz. O material não foi roubado: a fenda engoliu o lote num pulso anterior, e Diana foi puxada no seguinte. Chama os robôs de "autômatos". De tanto correr para todo lado, faz um **mapa à mão** com passagens que não aparecem nos mapas de 3026.

- **Essência:** uma recruta que entrou na polícia para provar que podia, e vive cada minuto como se fosse o último.
- **Traços:** dramática, ansiosa, impulsiva, intensa. Sente tudo em dobro e é corajosa no susto.
- **Como fala:** rápido e exagerado, cheio de exclamações ("Pronto, é o fim!", "Eu sabia que isso ia acontecer!"). Mistura o jargão da polícia ("Positivo!") com drama de novela.
- **O que quer:** voltar e provar à família, e ao quartel, que não foi um erro ela vestir a farda.
- **O que teme:** falhar na frente de todo mundo.
- **Defeito:** age antes de pensar e transforma cada problema numa tragédia.
- **Arco:** aprender a controlar o medo: de quem entra em pânico e sai correndo a quem respira e decide.

#### Clarice (1994)

**História.** Rodava um programa num terminal da Biblioteca de madrugada e foi puxada. Foi a primeira a notar que as rotas dos robôs formam um **grafo**. Deixou um bilhete no terminal que parece despedida ("Hoje à noite vou tentar entrar no sistema. Se der errado, foi mal."), e o jogador acha que ela morreu. Está viva, escondida no **bunker** embaixo do núcleo da Âncora, quebrando a senha do setor B "um disquete por vez". Liga para os telefones velhos do campus. A **relação dela com Gabriel vai sendo desenvolvida ao longo do jogo**.

- **Essência:** uma mente brilhante que usa o sarcasmo como armadura.
- **Traços:** rápida, independente, prática, engraçada, competitiva.
- **Como fala:** gírias dos anos 90 ("Isso é totalmente surreal", "meu filho", "Não confie nas luzes"), tom de deboche. Explica tudo como um problema de lógica.
- **O que quer:** resolver o problema grande, que é sair dali, e provar que consegue sozinha.
- **O que teme:** ser esquecida. Ficou dias sozinha antes de qualquer um aparecer.
- **Defeito:** não pede ajuda e quer controlar tudo.
- **Arco:** de quem resolve tudo sozinha a quem confia no grupo. A relação com Gabriel cresce nesse caminho.

#### Rafael (2008)

**História.** Fazia a ronda da Biblioteca e foi puxado com o rádio e a lanterna. Recusa-se a aceitar que está em 3026 ("isso aqui não é 3026 coisa nenhuma, é reforma") e transformou uma sala de manutenção no seu "posto de guarda". **Fala ao vivo** com Gabriel pelo rádio e dá dicas de patrulha.

- **Essência:** o otimista teimoso que prefere acreditar que é reforma a encarar o fim do mundo.
- **Traços:** caloroso, brincalhão, protetor. Conhece todo mundo do bairro e todo canto do campus.
- **Como fala:** jeito cearense ("rapaz", "macho"), rádio cheio de "câmbio". Faz questão de ser chamado de "Seu Rafael" para parecer mais velho.
- **O que quer:** proteger quem estiver na área dele. Continua fazendo a ronda.
- **O que teme:** que tudo seja real e ele nunca mais veja a mãe.
- **Defeito:** nega a realidade.
- **Arco:** aceitar onde está. O momento em que ele admite "não é reforma" deve ser o mais triste do jogo.

#### O pesquisador (2019)

**História.** Aluno de iniciação científica que estudava à noite na Biblioteca e sumiu. O orientador transformou o projeto dele na cadeira que Gabriel cursa, e as equações do caderno de Gabriel continuam esse trabalho sem Gabriel saber de quem eram. O nome está pendente.

- **Essência:** um gênio quieto que desconfia ter causado tudo.
- **Traços:** introvertido, perfeccionista, ansioso, gentil. Brilhante em teoria e sem jeito com gente.
- **Como fala:** pausado e técnico. Se corrige no meio da frase.
- **O que quer:** entender a Âncora para provar a si mesmo que não é culpado.
- **O que teme:** que a pesquisa dele tenha levado à Âncora.
- **Defeito:** guarda segredos.
- **Arco:** assumir a responsabilidade, seja ela real ou só imaginada.

#### Zane (2123), o último a chegar

**História.** Veio de uma época em que a Unifor já era um polo de IA. É quem mais entende a tecnologia da Âncora, mas é o mais novo em 3026: chega depois de Gabriel, e é Gabriel quem o recebe e explica as regras.

- **Essência:** filho de um mundo já cheio de máquinas, que sabe tudo de tecnologia e nada de sobreviver.
- **Traços:** impulsivo, direto, irreverente, elétrico, e mais assustado do que admite.
- **Como fala:** rápido, com gírias de um futuro que ninguém reconhece. Interrompe os outros.
- **O que quer:** voltar. Mais tarde, entender o que a IA virou, porque na época dele a IA ainda estava começando.
- **O que teme:** a IA. Ele sabe melhor que ninguém do que as máquinas são capazes.
- **Defeito:** imprudente. Age antes de pensar.
- **Arco:** a chegada dele mostra ao jogador o quanto Gabriel mudou: o novato da primeira fase virou o veterano que explica tudo.

### 4.4 Como eles se relacionam

| Par | Dinâmica |
|---|---|
| Diana × Clarice | O drama contra o deboche: a Clarice não leva nada a sério e a Diana leva tudo a sério demais. Brigam o tempo todo e acabam amigas |
| Baltazar × Zane | Os dois extremos do tempo: fé contra tecnologia, e ainda assim os dois mais curiosos do grupo |
| Diana × Rafael | Dois de farda em épocas diferentes. Ele é calmo e brincalhão, e é o único que consegue acalmá-la |
| Gabriel × Baltazar | Família descoberta |
| Gabriel × Clarice | Duelo de ironias: os dois se provocam o tempo todo no mesmo tom, e é assim que a relação cresce ao longo do jogo |
| Gabriel × Zane | Gabriel deixa de ser o novato e vira o veterano |

### 4.5 A IA

Antagonista sem rosto e sem voz. Aparece só pelos robôs e pelos sistemas que controla.

---

## 5. A família Magalhães

- **Baltazar é antepassado de Gabriel**, umas dez gerações antes dele. O sobrenome **Magalhães** liga a família pelos séculos.
- **O objeto:** Gabriel começa o jogo com um **anel desgastado** no inventário, que a avó deu para ele. O jogador vê o item desde o começo sem dar importância.
- **A descoberta acontece jogando**, não numa explicação: no meio do jogo, Gabriel vê o mesmo anel com o Baltazar (novo no dedo dele, gasto no de Gabriel). O jogador compara os dois e entende sozinho.
- **Gabriel conta para o Baltazar** que é descendente dele.
- Com isso, mandar todos de volta deixa de ser só ajudar os outros: se o Baltazar não voltar para 1750, a família de Gabriel pode nunca existir.

---

## 6. Os esconderijos

- Cada personagem tem um **lugar próprio** no campus, como a Clarice no bunker.
- Um lugar pode abrigar **2 ou 3 personagens**. O **bunker** é o maior deles: os robôs não descem lá, e é o lugar mais seguro do jogo.
- Rafael tem o "posto de guarda" numa sala de manutenção.
- Os esconderijos funcionam como pontos de encontro: Gabriel volta a eles para conversar e acompanhar o que cada um descobriu.

---

## 7. Linha do tempo

### 7.1 Quem esteve no ponto

| Ano | Quem | O que fazia ali |
|---|---|---|
| ~1750 | Baltazar | Viu uma luz estranha pela luneta, no sítio da família, e foi investigar |
| 1978 | Diana | Vigiava a obra depois do sumiço do material |
| 1994 | Clarice | Rodava um programa num terminal da Biblioteca, de madrugada |
| 2008 | Rafael | Fazia a ronda noturna na Biblioteca |
| 2019 | O pesquisador | Estudava à noite na Biblioteca |
| 2026 | Gabriel | Dormiu na Biblioteca com o caderno aberto |
| 2123 | Zane | *A definir* |

### 7.2 Ordem dos acontecimentos

1. **Antes de 3026:** a humanidade abandona a Terra, e a IA domina. A Âncora fica abandonada no centro de pesquisa da Unifor.
2. **3026:** a Âncora falha, e a fenda se abre no chão da Biblioteca.
3. **Os pulsos:** com dias de diferença, a fenda puxa uma pessoa de cada época. Cada uma acorda sozinha, foge dos robôs e acha um canto para sobreviver. Cinco chegam antes de Gabriel.
4. **O jogo:** Gabriel, o penúltimo, acorda na Biblioteca, encontra os outros um a um, descobre o que aconteceu e tenta consertar a Âncora para todos voltarem.
5. **Durante o jogo:** um novo pulso traz o **Zane**, o último. Gabriel o recebe.

---

## 8. Estrutura da história

> A ordem das fases depois da Biblioteca **não está decidida** (seção 12). Esta estrutura segue a lógica da história, não uma ordem de jogo travada.

### Ato 1 — Acordar (Biblioteca)

**Fase confirmada como primeira.** [`../fases/biblioteca.md`](../fases/biblioteca.md).

- **Cutscene de abertura** (`seg_acordar`, aprovada): Gabriel acorda na cabine de estudo. Luz do sol por um teto que não existe mais, uma árvore no meio do salão, estantes caídas e vazias.
- Gabriel acha a **lanterna** perto de onde acorda, e **pilhas** pelo salão. O **anel da avó** já está no inventário.
- **Acampamento de Baltazar** entre as raízes da árvore. Ele não está lá.
- **Terminal com o bilhete da Clarice**, que parece uma despedida.
- **Rádio portátil:** o Rafael transmite a primeira dica de patrulha.
- **Saída:** a porta no fim da ala leste leva ao Bloco de salas.

O jogador aprende aqui as regras do jogo (silêncio, esconderijos, bateria) e que **não está sozinho**: outras pessoas caíram ali antes dele.

### Ato 2 — Encontrar os outros (Bloco de salas, Labirinto e demais áreas)

- Cada fase leva a **um personagem** e ao esconderijo dele. Gabriel precisa chegar lá, ganhar a confiança da pessoa e receber a parte dela para consertar a Âncora (seção 3.1).
- **Bloco de salas** ([`../fases/bloco_de_salas.md`](../fases/bloco_de_salas.md)): dois andares, 12 salas de aula, noite. Hoje só tem cenário e portas.
- **Labirinto** ([`../fases/labirinto.md`](../fases/labirinto.md)): subsolo escuro do centro de pesquisa da Âncora, com três robôs. Jogável, mas sem lugar na história ainda.
- As áreas seguintes do GDD (Centro de Convivência, Espaço Cultural, NAMI, Reitoria) ainda não foram redefinidas para a premissa atual.
- **Rádio e telefone:** Rafael fala pelo rádio e Clarice liga pelos telefones velhos.
- **O anel:** em algum ponto deste ato, Gabriel encontra o Baltazar e descobre o parentesco.

### Ato 3 — O esconderijo (Bunker)

**Fase em desenvolvimento.** [`../fases/bunker.md`](../fases/bunker.md).

- O bunker de pesquisa embaixo do núcleo da Âncora ("ÂNCORA-03"), com dois setores. Os robôs não descem aqui.
- **Gabriel encontra Clarice em pessoa** na central de dados. Aqui podem morar 2 ou 3 personagens.
- O **setor B** (laboratório, arquivo e a comporta do núcleo) está lacrado pelo sistema. Clarice quebra a senha "um disquete por vez".
- Seis portas lacradas são os ganchos para as próximas fases: escotilha da superfície, elevador, arsenal, laboratório, arquivo e a comporta do núcleo.

### Ato 4 — Consertar a Âncora e voltar (Núcleo)

- A reta final passa pela **comporta do núcleo**, no setor B do bunker.
- Com as partes de todos reunidas, Gabriel e os outros tentam consertar a Âncora e mandar cada um para a sua noite.
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
| **Narrativa ambiental** | Marcas no cenário, relíquias de épocas diferentes, os tracinhos nas lousas, os riscos de estrelas na árvore | [`README.md`](README.md) |
| **Documentos** | Diários, bilhetes, disquetes. Cada época tem um papel próprio. As pistas úteis viram anotações no **Caderno do Gabriel** | [`../mecanicas/registros_e_caderno.md`](../mecanicas/registros_e_caderno.md) |
| **Inventário** | O anel da avó, e a comparação com o anel do Baltazar | [`../mecanicas/itens_e_inventario.md`](../mecanicas/itens_e_inventario.md) |
| **Rádio** | Rafael ao vivo, sem pausar o jogo | [`../mecanicas/registros_e_caderno.md`](../mecanicas/registros_e_caderno.md) |
| **Ligações e diálogos** | Clarice por telefone; todos em pessoa nos esconderijos, com retratos e escolhas | [`../dialogos/README.md`](../dialogos/README.md) |
| **Sonhos** | O sono continua como mecânica; o que os sonhos mostram está pendente | [`../mecanicas/sono_e_sonhos.md`](../mecanicas/sono_e_sonhos.md) |
| **Cutscenes** | A abertura (`seg_acordar`) e as que o grupo decidir | [`../roteiro/cutscenes/`](../roteiro/cutscenes/) |

---

## 11. Vocabulário oficial

Para qualquer texto do jogo ou da documentação:

| Use | Não use |
|---|---|
| **Âncora** (a máquina) | "Ankhor" para a máquina. Ankhor é o nome do jogo |
| **Fenda** (temporal) | "portal" |
| **IA** (quem domina a Terra) | um nome próprio, enquanto o grupo não decidir |
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

- **Quanto tempo Gabriel tem:** se a fenda crescendo vira um prazo que o jogador sente (dias contados, pulsos que estremecem o campus) ou fica só na história.
- **Como cada um volta:** todos de uma vez no final, ou um por um, conforme a Âncora vai sendo consertada.
- **Alguém escolhe não voltar?** (Zane, que vem de um futuro pior; Clarice, dependendo da relação com Gabriel.)
- **O final** de Gabriel e Clarice. O final antigo ("A mesma madrugada": os dois acordam juntos em 2026, e ela rasga a página das equações) foi escrito para a versão com loops e precisa ser revisto.

### 12.2 A IA e a Âncora

- **O objetivo da IA:** o que ela quer, se sabe da Âncora e se reage quando os humanos tentam consertá-la.
- **Quando e por que a humanidade abandonou a Terra**, e como a IA dominou.
- **Quem criou a Âncora e por quê.** Ideia em aberto: o criador seria um **descendente de Gabriel**, e o caderno teria passado de geração em geração na família até virar a base da máquina (Gabriel acharia o próprio caderno, com mil anos, numa vitrine do centro de pesquisa). A fala do Zane sobre "um nome de usuário de 2026" depende disso.

### 12.3 Personagens

- **Gabriel falhando na tela:** enquanto o Baltazar estiver fora de 1750, o sprite de Gabriel pisca ou se desfaz, como a foto em *De Volta para o Futuro*. Seria um shader (bom para a apresentação de Computação Gráfica).
- **Algum personagem atrapalha?** Alguém que desconfia de Gabriel, quer usar a Âncora só para si ou esconde alguma coisa. Sem isso, o único conflito vem dos robôs. O pesquisador, que guarda segredos, é o candidato natural.
- **Nome do pesquisador de 2019**, e como ele aparece no jogo.
- **Zane:** o que fazia no ponto quando foi puxado, e em que fase do jogo ele chega (e se o jogador vê o pulso acontecer).
- **Ordem de chegada dos outros cinco** (Baltazar, Diana, Clarice, Rafael e o pesquisador), que chegaram antes de Gabriel. Não precisa seguir a ordem dos anos.
- **Quem fica em qual esconderijo**, e quem divide o bunker com a Clarice.
- **Como o Rafael parece ver Gabriel** pelo rádio ("Ele falou como se estivesse me vendo").

### 12.4 Textos já escritos que citam a versão antiga

- `dados/dialogos/clarice_primeiro_encontro.json`: as falas "Você sempre lê", "E sempre chega aqui com essa cara de quem viu assombração" e "E você sempre repara" vinham dos loops e precisam ser reescritas.
- [`revelacao_central.md`](revelacao_central.md): substituída por este documento. Decidir se é apagada ou guardada como histórico.
- [`../personagens/antecessores.md`](../personagens/antecessores.md): fichas com idades, mortes e loops antigos.
- [`../mecanicas/sono_e_sonhos.md`](../mecanicas/sono_e_sonhos.md): **o que os sonhos mostram** agora que não há loops (memória, o passado do campus, outra coisa).

### 12.5 Estrutura e fases

- **Ordem das fases** depois da Biblioteca: onde entram o Labirinto, o Bunker e o Bloco de salas, e qual personagem aparece em cada uma.
- **Objetivo, robôs e história do Bloco de salas.**
- **O que destrava o setor B do bunker** (senhas nos disquetes, religar o gerador) e se os robôs entram lá.
- **Redesenho das áreas do GDD** (Centro de Convivência, Espaço Cultural, NAMI, Reitoria) para a premissa da fenda.
- **De onde vem a grade horária dos robôs.** Antes vinha da coloração de grafos da semana de provas; hoje a patrulha é programada pela IA.

### 12.6 Mecânicas que dependem da história

- **Energia:** quais sistemas são da Âncora e quais são da IA. Hoje: luzes de emergência, bunker, terminais e telefones são da Âncora; os robôs são da IA.
- **Gadgets e personagens:** em que fase cada gadget aparece e se cada um vem de um personagem.
