# Personagens — Os que vieram antes (antecessores)

> **Status:** Em definição  
> **Origem:** proposta de personagens secundários recebida pelo grupo em 2026-09-29 (registrada em [`../decisoes.md`](../decisoes.md)).

Antes de Gabriel, a fenda da Âncora puxou outras pessoas para 3026. Nenhuma conseguiu fechar a fenda, mas cada uma deixou alguma coisa para trás: bilhetes, mapas, disquetes, áudios, um diário. São os **antecessores**, e são eles que contam a história para o jogador.

Todos foram puxados **no mesmo lugar**: o chão onde hoje fica a Biblioteca (ou onde ela ainda viria a ser construída). Ver [`../historia/revelacao_central.md`](../historia/revelacao_central.md).

> [!NOTE]
> Na proposta, o aparelho é chamado de "Ankhor". Neste repositório, **Ankhor é o nome do jogo** e o aparelho continua se chamando **Âncora**.

---

## 1. Linha do tempo

| Ano de origem | Personagem | Quem era | Como aparece no jogo | Situação em 3026 |
|---|---|---|---|---|
| ~1750 | **Mestre Baltazar** | Naturalista e astrônomo português | Diário e objetos pessoais | Desaparecido |
| 1978 | **Inspetor Agostinho** | Policial investigando um sumiço na obra do campus | Bilhetes, mapa desenhado à mão; NPC nos sonhos | Morto (envelheceu em 3026) |
| 1994 | **Clarice** | Aluna de processamento de dados | Bilhetes, disquetes e **ligações** | **Viva** (o jogador acha que morreu) |
| 2008 | **Seu Valdir** | Segurança noturno da Unifor | Voz no rádio | Morto há décadas; o rádio repete as gravações dele |
| 2019 | **O professor** *(nome a definir)* | Professor e pesquisador da Unifor | A definir | A definir |
| 2026 | **Gabriel** | Estudante (protagonista) | — | — |
| 2041 | *Alguém (a definir)* | — | — | — |
| 2123 | **Zane** | Jovem com implantes cibernéticos | Mensagens de áudio; NPC nos sonhos | A definir |

Clarice é a "aluna de 1994" e Valdir é o "segurança de 2008" já decididos em 2026-09-26. Baltazar, Agostinho e Zane são novos. A pessoa de 2041 continua sem ficha (ver seção 5).

---

## 2. Fichas

### 2.1 Mestre Baltazar (~1750)

- **Tipo:** Registro (diário e objetos pessoais). Não fala.
- **História:** Naturalista e astrônomo português que explorava o Ceará colonial com lunetas e diários, quando a área do campus era só mata e sítio. Numa noite, viu pela luneta uma luz estranha sobre a mata, no ponto onde hoje fica a Biblioteca. Foi até lá investigar e foi puxado.
- **Como ele vê 3026:** acha que a Âncora é o "Tormento de Leviatã", um Juízo Final. Escreve em português arcaico, com trechos em latim.
- **No jogo:** Gabriel acha um **nicho entre as raízes da árvore** no meio do salão da Biblioteca, arrumado como um acampamento: a luneta de latão com a lente rachada, um toco de vela, e o diário embrulhado em pano encerado. Na casca e na pedra ao redor, mapas de estrelas riscados à faca. Ali perto, um único robô desmontado peça por peça, com as peças enfileiradas como num estudo. **Não há corpo.** A última página do diário é ambígua ("Hei de seguir a luz até onde ella nasce") e ninguém sabe o que aconteceu com ele.
- **Item:** **diário ilustrado**, com desenhos à pena dos robôs mostrando o **ponto fraco dos sensores ópticos**.
- **Função mecânica:** ensina onde o clarão funciona melhor (liga com a cápsula de clarão e com o sensor óptico de [`robos.md`](robos.md)).

### 2.2 Inspetor Agostinho (1978)

- **Tipo:** Registro (bilhetes) + NPC de sonho.
- **História:** Policial nos anos da ditadura, quando o campus ainda estava sendo erguido. Investigava o sumiço de um lote de material de construção, seguiu uma pista até o matagal à noite e foi engolido por uma faísca temporal. O material não foi roubado: foi **a primeira coisa que a fenda engoliu**, no mesmo ponto.
- **Como ele vê 3026:** chama os robôs de "autômatos demoníacos" ou "tecnologia comunista do futuro". Viveu em 3026 até ficar velho.
- **Item:** anotações táticas sobre como se esconder nos **dutos**, e um **mapa desenhado à mão** com a estrutura antiga do campus, que mostra passagens que não existem nos mapas de 3026.
- **Função mecânica:** revela **arestas escondidas no grafo do campus** (atalhos e passagens secretas).

### 2.3 Clarice (1994)

- **Tipo:** **NPC vivo**, só por voz (ligações), + bilhetes e disquetes.
- **História:** Aluna prodígio de processamento de dados. Foi puxada numa madrugada na Biblioteca, tentando rodar um código em disquete num dos terminais de lá. Chegou a 3026 poucos meses antes de Gabriel.
- **Papel:** foi a primeira a perceber que a ruína tinha **padrões lógicos**: as rotas dos robôs formam um grafo e as patrulhas seguem uma rotina.
- **O que o jogador acredita:** que ela morreu tentando invadir o terminal da Biblioteca. O bilhete que Gabriel acha lá parece uma despedida.
- **A verdade:** o bilhete é de um **ciclo anterior**. Ela conseguiu entrar no sistema da Âncora e vive escondida perto do núcleo, num lugar aonde Gabriel não consegue chegar. Usa a rede da Âncora para **ligar para os telefones velhos do campus**.
- **As ligações:** um telefone toca numa sala (o balcão da Biblioteca, uma sala segura, uma cabine) e Gabriel atende com `E`. As conversas são só por voz: os dois nunca se veem até o fim.
  - *Ideia de mecânica:* o toque do telefone é um **som no grafo** (BFS). Se Gabriel demora a atender, os robôs ouvem.
- **A que lembra:** Clarice é a **única que lembra dos loops**. Ela grava tudo no sistema da Âncora, a única coisa que o reinício não apaga. Para Gabriel, ela é uma desconhecida sarcástica que ajuda com senhas. Para ela, é a vigésima vez que o conhece: sabe a piada que ele vai fazer, a música de que ele gosta e como ele morreu em cada ciclo. Aos poucos ela deixa escapar demais: *"Você sempre pergunta isso."*
- **Item:** disquetes e anotações com as primeiras **senhas dos terminais**.
- **Voz:** gírias dos anos 90 ("Isso é totalmente surreal", "Se alguém ler isso, não confie nas luzes").
- **Função mecânica:** guia por voz ao longo do jogo; senhas e explicação das rotinas de patrulha (ponte para os conteúdos de computação).
- **Final:** os dois ficam juntos em 2026. Ver [`../historia/revelacao_central.md`](../historia/revelacao_central.md), seção 5.

### 2.4 Seu Valdir (2008)

- **Tipo:** Voz no rádio. A sala dele é descoberta no fim.
- **História:** O guarda noturno lendário da Unifor, que conhecia cada canto do campus. Foi puxado durante a ronda da Biblioteca, com o rádio amador e uma lanterna antiga.
- **Papel:** se recusava a aceitar que estava em 3026 ("isso aqui não é 3026, rapaz"). Trancou-se numa sala de manutenção e transformou o lugar no seu "posto de guarda". Fala com Gabriel pelo rádio desde a primeira fase, e parece responder na hora.
- **A virada:** no fim, Gabriel acha o posto de guarda e descobre que Valdir **morreu há décadas**. O rádio só repete as gravações dele, num loop. A negação dele ganha outro peso: ele passou o resto da vida fazendo ronda num lugar que não existia mais. *(Em aberto: por que as gravações parecem responder ao Gabriel. Pode ser coincidência, ou o próprio loop da Âncora.)*
- **Função mecânica:** dá dicas sobre as **rotinas de patrulha dos robôs** ("Aquele robô do Bloco K sempre faz o giro de 180 graus quando dá o bipe..."). As dicas continuam valendo porque os robôs repetem a mesma rotina há séculos. O posto de guarda pode servir de **sala segura**.

### 2.5 O professor (2019)

- **Tipo:** A definir (bilhetes, sonho ou os dois).
- **História:** Professor e pesquisador da Unifor. Sumiu em 2019, numa noite de estudo na Biblioteca, e deixou uma pesquisa pela metade. As anotações dele ficaram no acervo, e o material virou a base da **cadeira que Gabriel cursa em 2026**. O caderno de Gabriel continua as equações do professor, sem Gabriel saber de quem eram.
- **Em 3026:** entende que o caderno é a origem da Âncora e **apaga o nome do criador dos arquivos**, para proteger Gabriel ou para quebrar o loop. É por isso que Zane só encontra "um nome de usuário de 2026".
- **Nome, voz e destino:** a definir.

### 2.6 Zane (2123)

- **Tipo:** Mensagens de áudio + NPC de sonho.
- **História:** Jovem rebelde com implantes e cibernética experimental, de uma época em que a Unifor já era um polo de IA e a Âncora estava sendo rascunhada na teoria. Foi até o ponto da Biblioteca para impedir o criador da Âncora e foi puxado.
- **Papel:** entende a tecnologia da Âncora melhor que ninguém, mas perdeu a sanidade ao perceber que o tempo em 3026 está em colapso circular.
- **Fala-chave:** *"Eu vim de 2123 para impedir o criador da Âncora... mas o arquivo do criador foi apagado da história. Só sobrou um nome de usuário antigo de 2026."*
- **Função narrativa:** é quem aponta para a revelação central.

---

## 3. Aparência dos registros

Cada época tem um suporte próprio, para o jogador reconhecer o autor antes de ler. A fonte do jogo (**Ark Pixel**) só funciona nos tamanhos 10 e 20, então a diferença vem do **papel, da cor e da moldura**, nunca de outra fonte.

| Personagem | Suporte | Visual |
|---|---|---|
| Baltazar | Diário de pergaminho escrito à pena | Papel amarelado, tinta marrom, desenhos a traço |
| Agostinho | Relatório policial datilografado | Papel timbrado, carimbo, tinta preta falhada |
| Clarice | Folha de caderno com adesivo + disquete; telefone | Pautas azuis, adesivo colorido, disquete com etiqueta escrita à mão; na ligação, só a voz e o chiado da linha |
| Valdir | Livro de ocorrências do vigia + rádio | Tabela com data e hora; o rádio com chiado na tela |
| Professor | A definir | A definir |
| Zane | Áudio com interface holográfica | Tela ciano com forma de onda e falhas de sinal |
| "G." (ciclos anteriores) | Folha arrancada do caderno do Gabriel | O mesmo papel do caderno do jogador (ver a revelação central) |

---

## 4. Como os antecessores entram no jogo

- **Bilhetes, diários, disquetes e áudios** seguem o modelo de [`../historia/template_documento.md`](../historia/template_documento.md).
- **Sonhos:** ao dormir numa sala segura, Gabriel conversa com um antecessor no passado ou assiste a um **eco temporal**: os minutos antes daquela pessoa ser puxada (ver [`../mecanicas/sono_e_sonhos.md`](../mecanicas/sono_e_sonhos.md)).
- **Caderno do Gabriel:** toda pista útil (sensor óptico, atalho no grafo, senha, rotina de patrulha) vai para o caderno, e é de lá que o jogador tira a solução dos puzzles no presente.
- **Na Biblioteca (primeira fase)** só entram três: o nicho e o diário de Baltazar, o bilhete de despedida da Clarice e a primeira chamada do Valdir pelo rádio. Os outros ficam para as próximas fases (ver [`../fases/biblioteca.md`](../fases/biblioteca.md)).

---

## 5. Em aberto

- **Pessoa de 2041:** decidida em 2026-09-26, mas ainda sem ficha. Falta decidir se continua ou se Zane toma o lugar dela.
- **Terminais e eletricidade:** as senhas e as ligações de Clarice e o rádio de Valdir pedem algo elétrico funcionando, e o GDD diz que "nada elétrico funciona depois de mil anos". Como em 3026 o campus era um centro de pesquisa ativo (e os robôs funcionam), dá para dizer que só os sistemas da Âncora ainda têm energia, e que é a Clarice quem leva essa energia até os telefones.
- **Onde a Clarice está escondida**, e se Gabriel chega perto dela antes do final.
- **Destino de Zane:** vivo, morto ou preso no colapso circular.
- **Qual antecessor aparece em qual fase** depois da Biblioteca.
