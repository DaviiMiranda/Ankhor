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
- Quase nada elétrico funciona. Funcionam os sistemas da Âncora (luzes de emergência, bunker, terminais, telefones) e os robôs.

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
| Clarice (1994) | Código: faz os terminais da Âncora funcionarem |
| Rafael (2008) | Conhece o campus e as rondas, e sabe o que cada chave abre |
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
- **Ordem de chegada:** o **Zane é o último** a chegar, e **Gabriel é o penúltimo**. Os outros cinco chegaram antes dele, em ordem ainda pendente. Como o Zane chega depois de Gabriel, **a fenda pulsa durante o jogo**: a chegada dele acontece enquanto Gabriel já está em 3026, e é Gabriel quem o recebe.

### 4.2 Fichas

| Época | Personagem |
|---|---|
| ~1750 | [Baltazar Magalhães](personagens/baltazar.md) |
| 1978 | [Diana](personagens/diana.md) |
| 1994 | [Clarice](personagens/clarice.md) |
| 2008 | [Rafael](personagens/rafael.md) |
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
| **Bunker**, embaixo do núcleo da Âncora. O maior e mais seguro: os robôs não descem lá | Clarice e Henrique. Depois, o Zane, quando Gabriel o traz |
| **Posto de guarda**, a sala de manutenção que o Rafael transformou | Rafael |
| **Biblioteca**, num esconderijo dentro dela | Baltazar |
| **Bloco de salas**, numa das salas de aula | Diana |

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
| 2019 | Henrique | Estudava à noite na Biblioteca |
| 2026 | Gabriel | Dormiu na Biblioteca com o caderno aberto |
| 2123 | Zane | *A definir* |

### 7.2 Ordem dos acontecimentos

1. **Antes do jogo:** a sociedade e o planeta ficam muito ruins, e o pouco que sobrou da humanidade vai embora para outro planeta. O Carlos fica e constrói a Âncora no D-Tec.
2. **3026:** o Carlos começa a tentar ir para os anos 80. A cada tentativa, a fenda se abre no chão da Biblioteca.
3. **Os pulsos:** com dias de diferença, a fenda puxa uma pessoa de cada época. Cada uma acorda sozinha, foge dos robôs e acha um canto para sobreviver. Cinco chegam antes de Gabriel.
4. **O jogo:** Gabriel, o penúltimo, acorda na Biblioteca, encontra os outros um a um, descobre o que aconteceu e tenta consertar a Âncora para todos voltarem.
5. **Durante o jogo:** uma nova tentativa do Carlos traz o **Zane**, o último. Gabriel o recebe.

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
- **Bloco de salas** ([`../fases/bloco_de_salas.md`](../fases/bloco_de_salas.md)): dois andares, 12 salas de aula, noite. É onde fica o esconderijo da **Diana**, numa das salas. Hoje só tem cenário e portas.
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
| **Rádio** | Rafael ao vivo, sem pausar o jogo | [`../mecanicas/registros_e_caderno.md`](../mecanicas/registros_e_caderno.md) |
| **Ligações e diálogos** | Clarice por telefone; todos em pessoa nos esconderijos, com retratos e escolhas | [`../dialogos/README.md`](../dialogos/README.md) |
| **Sonhos** | O sono continua como mecânica; o que os sonhos mostram está pendente | [`../mecanicas/sono_e_sonhos.md`](../mecanicas/sono_e_sonhos.md) |
| **Cutscenes** | A abertura (`seg_acordar`) e as que o grupo decidir | [`roteiro/cutscenes/`](roteiro/cutscenes/) |

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

- **Quanto tempo Gabriel tem:** se a fenda crescendo vira um prazo que o jogador sente (dias contados, pulsos que estremecem o campus) ou fica só na história.
- **Como cada um volta:** todos de uma vez no final, ou um por um, conforme a Âncora vai sendo consertada.
- **O final** de Gabriel e Clarice. O final antigo ("A mesma madrugada": os dois acordam juntos em 2026, e ela rasga a página das equações) foi escrito para a versão com loops e precisa ser revisto.

### 12.2 O Carlos, a Âncora e a IA

- **Como o Carlos consegue o conhecimento** que falta para a Âncora funcionar: roubando a consciência dos puxados, construindo uma super IA, ou as duas (a super IA feita das consciências roubadas).
- **A IA continua existindo?** Pode ser a super IA do Carlos, outra coisa que ele controla, ou sair da história. O arco do Zane (medo da IA, ficar para domá-la) depende disso.
- **O Carlos domina as IAs, e elas o ajudam?** Proposta do Davi: em vez de uma IA só, várias IAs, todas sob o controle do Carlos e trabalhando para ele. Falta decidir quantas são, o que cada uma faz (os robôs, a Âncora, os sistemas do D-Tec) e como ele as domina.
- **Por que os robôs caçam os humanos:** para capturar e levar ao Bloco M, ou para eliminar quem atrapalha.
- **O Carlos:** idade, aparência, como fala, o que teme, defeito e arco; e **quando o jogador descobre** que ele existe.
- **Quando a humanidade foi embora**, e como a Unifor virou um centro de pesquisa em física do tempo.
- **Por que a fenda se abre sempre na Biblioteca.**

### 12.3 Personagens

- **Gabriel falhando na tela:** enquanto o Baltazar estiver fora de 1750, o sprite de Gabriel pisca ou se desfaz, como a foto em *De Volta para o Futuro*. Seria um shader (bom para a apresentação de Computação Gráfica).
- **Henrique:** como ele aparece no jogo.
- **Zane:** o que fazia no ponto quando foi puxado, e em que fase do jogo ele chega (e se o jogador vê o pulso acontecer).
- **Ordem de chegada dos outros cinco** (Baltazar, Diana, Clarice, Rafael e Henrique), que chegaram antes de Gabriel. Não precisa seguir a ordem dos anos.
- **Qual sala de aula** do Bloco de salas é o esconderijo da Diana.
- **Onde fica, dentro da Biblioteca, o esconderijo do Baltazar**, e como ele combina com o acampamento vazio que Gabriel acha no começo do jogo e com a última página do diário ("Hei de seguir a luz até onde ella nasce").
- **Como o Rafael parece ver Gabriel** pelo rádio ("Ele falou como se estivesse me vendo").

### 12.4 Textos já escritos que citam a versão antiga

- `dados/dialogos/clarice_primeiro_encontro.json`: as falas "Você sempre lê", "E sempre chega aqui com essa cara de quem viu assombração" e "E você sempre repara" vinham dos loops e precisam ser reescritas.
- [`../mecanicas/sono_e_sonhos.md`](../mecanicas/sono_e_sonhos.md): **o que os sonhos mostram** agora que não há loops (memória, o passado do campus, outra coisa).

### 12.5 Estrutura e fases

- **Ordem das fases** depois da Biblioteca: onde entram o Labirinto, o Bunker e o Bloco de salas, e qual personagem aparece em cada uma.
- **Objetivo, robôs e história do Bloco de salas.**
- **O que destrava o setor B do bunker** (senhas nos disquetes, religar o gerador) e se os robôs entram lá.
- **O D-Tec (Bloco M)** como fase: se é a última, e como o grupo enfrenta o Carlos sem lutar (Gabriel não é combatente).
- **Cenários mais futuristas.** Pedido do Davi: os cenários precisam mostrar mais a tecnologia de 3026 (telas, máquinas, a estrutura do centro de pesquisa e do D-Tec), misturada às ruínas e à vegetação. Falta decidir quanto do campus tem esse visual futurista e onde ele aparece mais.
- **Redesenho das áreas do GDD** (Centro de Convivência, Espaço Cultural, NAMI, Reitoria) para a premissa da fenda.
- **De onde vem a grade horária dos robôs.** Antes vinha da coloração de grafos da semana de provas; hoje a patrulha é programada (pelo Carlos ou pela IA: seção 12.2).

### 12.6 Mecânicas que dependem da história

- **Energia:** quais sistemas são da Âncora e quais são do Carlos. Hoje: luzes de emergência, bunker, terminais e telefones são da Âncora; os robôs obedecem ao Carlos.
- **Gadgets e personagens:** em que fase cada gadget aparece e se cada um vem de um personagem.

### 12.7 A mentira do Henrique

As perguntas que faltam responder sobre "A virada" (seção 8):

1. **O Henrique trabalha para o Carlos por vontade própria, ou foi enganado por ele?**
2. **O que exatamente o Henrique esconde do grupo?** (A ideia 12 de [`outras_ideias.md`](outras_ideias.md) é uma opção.)
3. **Como e quando o grupo descobre a mentira?**
