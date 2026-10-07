# Enredo Principal

> [!IMPORTANT]
> **Este documento é a lei do projeto**, junto com as fichas de [`personagens/`](personagens/) (uma por personagem), que fazem parte dele. Tudo o que diz respeito à história, ao mundo e aos personagens de **Ankhor** vale como está escrito aqui e nas fichas, **acima de qualquer outro documento**: GDD, fases, diálogos, arte, textos em `dados/` e o próprio `decisoes.md`. Em caso de dúvida em qualquer parte do jogo (o que uma fase conta, como um personagem fala, o que um objeto significa), consulte este documento e a ficha do personagem. Se outra parte do projeto contradisser o que está aqui, **a outra parte está errada** e deve ser corrigida.

> **Status:** reescrito em 2026-10-06, quando a história mudou de rumo: saíram os loops e a revelação de "Gabriel é o paradoxo", e a fenda passou a ser **um acaso**.
> **Como mudar:** só por decisão do grupo. Toda mudança de história entra **no mesmo PR** neste documento e em [`../decisoes.md`](../decisoes.md) (que guarda o histórico de quando e por que mudou). Tudo o que ainda não foi decidido fica na **seção 12 ("Pendências")**, no fim, e não no meio da narrativa: o que está fora das pendências está decidido.

---

## 1. A história em um parágrafo

Numa madrugada de 2026, o estudante **Gabriel Magalhães** pega no sono na Biblioteca da Unifor e acorda no ano de **3026**, no mesmo lugar, agora uma ruína tomada pela natureza. A humanidade abandonou a Terra há muito tempo, e uma **IA** ficou com o planeta. No **Bloco J**, o antigo bloco de tecnologia da Unifor, uma máquina abandonada, a **Âncora**, falhou e abriu uma **fenda** no tempo bem no chão da Biblioteca. A fenda pulsa e, a cada poucos dias, puxa quem estiver naquele ponto em alguma época. Não há plano nem escolhido: **foi um acaso**. Gabriel não é o único: outros jovens de épocas diferentes caíram ali com dias de diferença, e cada um está tentando sobreviver num canto do campus. Os robôs da IA caçam qualquer humano que aparecer. Gabriel precisa encontrar os outros, descobrir o que aconteceu e achar um jeito de todos voltarem para suas épocas. No caminho descobre que um deles é seu antepassado.

---

## 2. O mundo

### 2.1 A Terra em 3026

- **A humanidade abandonou a Terra.** Quase não restam humanos no planeta.
- **A IA dominou.** Ficou com o planeta, as máquinas e os robôs. Ela **não tem rosto**: aparece só pelos robôs e pelo que controla.
- Para a IA, humanos são **invasores** no mundo dela. É por isso que os robôs atacam.

### 2.2 O campus em 3026

- A **Unifor, em Fortaleza**, mil anos depois. Em algum momento virou um centro de pesquisa em física do tempo.
- A **Âncora** está no **Bloco J**, o bloco de tecnologia.
- Concreto rachado e desabado, árvores dentro das salas, dunas sobre os corredores, mato onde era estacionamento. Não há cidade em volta, só vegetação. Resistem as coisas duras: concreto, metal, vidro, pedra.
- Objetos do cotidiano de hoje (catraca, bebedouro, quadro de horários, a cantina) viraram relíquias. O choque do jogo é perceber **quanto tempo passou**.
- Quase nada elétrico funciona. Funcionam os sistemas da Âncora (luzes de emergência, bunker, terminais, telefones) e os robôs da IA.

### 2.3 Os robôs

- Os inimigos são **robôs da IA** que patrulham o campus por **rotinas programadas**. Repetem o mesmo caminho há séculos: dá para decorar.
- Fora da rotina, quando ouvem ou veem um humano, saem do protocolo e caçam.
- São agressivos: se pegam Gabriel, é **game over** e o jogo volta ao último checkpoint (ver [`../mecanicas/vida_e_checkpoint.md`](../mecanicas/vida_e_checkpoint.md)).
- Cada tipo tem um sentido dominante (som, visão, luz). Os dois já implementados são a **Sentinela** (visão) e o **Rastreador** (audição). Ver [`personagens/robos.md`](personagens/robos.md).
- Gabriel não é um combatente: **fugir e se esconder é a regra**, defender-se é a exceção.

---

## 3. A Âncora e a fenda

| | |
|---|---|
| **O que é a Âncora** | **Só uma máquina.** Um aparelho experimental de física do tempo. Não pensa, não quer nada, não escolhe ninguém |
| **Onde está a Âncora** | No **Bloco J**, o bloco de tecnologia da Unifor |
| **O que aconteceu** | Abandonada por séculos, a Âncora falhou em 3026 e abriu uma fenda no tempo |
| **Onde a fenda se abre** | Sempre no mesmo ponto: o chão onde hoje fica a Biblioteca (ou onde ela ainda viria a ser construída) |
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

**Quem cada personagem é** (história, personalidade, como fala, o que quer, o que teme, defeito, arco e relações) está na ficha dele, em [`personagens/`](personagens/). Cada ficha faz parte deste documento e tem a mesma autoridade. Falas, documentos, retratos, animações e sons de um personagem seguem a ficha dele.

### 4.1 Regras para todos

- Todos têm **cerca de 20 anos**.
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
| 2019 | [O pesquisador](personagens/pesquisador.md) |
| 2026 | [Gabriel Magalhães](personagens/gabriel.md) (protagonista) |
| 2123 | [Zane](personagens/zane.md) |
| 3026 | [Os robôs](personagens/robos.md) (inimigos) |

### 4.3 A IA

Antagonista sem rosto e sem voz. Aparece só pelos robôs e pelos sistemas que controla. Não tem ficha.

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
| **Bunker**, embaixo do núcleo da Âncora. O maior e mais seguro: os robôs não descem lá | Clarice e o pesquisador. Depois, o Zane, quando Gabriel o traz |
| **Posto de guarda**, a sala de manutenção que o Rafael transformou | Rafael |
| **Biblioteca**, num esconderijo dentro dela | Baltazar |
| *Pendente* | Diana |

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

1. **Antes de 3026:** a humanidade abandona a Terra, e a IA domina. A Âncora fica abandonada no Bloco J.
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
- **O Zane escolhe ficar.** Voltar para 2123 é voltar para o mundo que vai virar o da IA. Fiel ao defeito dele (acha que toda máquina tem conserto), ele decide ficar em 3026 para tentar domar a IA por dentro. Um final agridoce que não tira o final dos outros.
- **O Baltazar volta para 1750**, mesmo querendo ficar: Gabriel precisa convencê-lo (seção 5).
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
- **Esconderijo da Diana.**
- **Onde fica, dentro da Biblioteca, o esconderijo do Baltazar**, e como ele combina com o acampamento vazio que Gabriel acha no começo do jogo e com a última página do diário ("Hei de seguir a luz até onde ella nasce").
- **Como o Rafael parece ver Gabriel** pelo rádio ("Ele falou como se estivesse me vendo").

### 12.4 Textos já escritos que citam a versão antiga

- `dados/dialogos/clarice_primeiro_encontro.json`: as falas "Você sempre lê", "E sempre chega aqui com essa cara de quem viu assombração" e "E você sempre repara" vinham dos loops e precisam ser reescritas.
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
