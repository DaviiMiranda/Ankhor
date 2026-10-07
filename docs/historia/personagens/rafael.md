# Rafael (2008)

> **Status:** Em desenvolvimento. Já fala pelo rádio na Biblioteca.
> **Lei do projeto:** esta ficha faz parte do [Enredo Principal](../enredo_principal.md) e tem a mesma autoridade: quem o Rafael é vale como está escrito aqui. A história em volta dele (o acidente, a ordem dos acontecimentos, as pendências) está no Enredo.

---

## 1. Quem é

- **Época de origem:** 2008.
- **Quem é:** segurança noturno da Unifor no primeiro emprego, com cerca de 20 anos. Mora no bairro e conhece o campus de cor.
- **História:** fazia a ronda da Biblioteca e foi puxado com o rádio e a lanterna. Recusa-se a aceitar que está em 3026 ("isso aqui não é 3026 coisa nenhuma, é reforma") e transformou uma sala de manutenção no seu "posto de guarda". **Fala ao vivo** com Gabriel pelo rádio e dá dicas de patrulha.

## 2. Personalidade

- **Essência:** o otimista teimoso que prefere acreditar que é reforma a encarar o fim do mundo.
- **Traços:** caloroso, brincalhão, protetor. Conhece todo mundo do bairro e todo canto do campus.
- **Como fala:** jeito cearense ("rapaz", "macho"), rádio cheio de "câmbio". Faz questão de ser chamado de "Seu Rafael" para parecer mais velho.
- **O que quer:** proteger quem estiver na área dele. Continua fazendo a ronda.
- **O que teme:** que tudo seja real e ele nunca mais veja a mãe.
- **Defeito:** nega a realidade.
- **Arco:** aceitar onde está. O momento em que ele admite "não é reforma" deve ser o mais triste do jogo.

## 3. Relações

| Com | Dinâmica |
|---|---|
| [Diana](diana.md) | Dois de farda em épocas diferentes. Ele é calmo e brincalhão, e é o único que consegue acalmá-la |

## 4. No jogo

- **Onde aparece:** pelo rádio desde a Biblioteca. Em pessoa, no posto de guarda (fase pendente).
- **Esconderijo:** o "posto de guarda", uma sala de manutenção, onde fica sozinho. Pode servir de **sala segura**.
- **Como chega ao jogador:** **rádio ao vivo** (o rádio portátil é um item comum do inventário) e, depois, em pessoa.
- **Função na jogabilidade:** dicas sobre as **rotinas de patrulha dos robôs** ("Antes de virar, ele dá um bipe. Ouviu o bipe, se esconde."). As dicas continuam valendo porque os robôs repetem a mesma rotina há séculos. As transmissões tocam sem pausar o jogo. Ver [`../../mecanicas/registros_e_caderno.md`](../../mecanicas/registros_e_caderno.md).
- **Parte para consertar a Âncora:** conhece o campus e as rondas, e sabe o que cada chave abre.

## 5. Registros

- **Suporte:** livro de ocorrências do vigia (tabela com data e hora) e o rádio, com chiado na tela. O papel ainda não foi desenhado no jogo.
- **Já escritos:** `dados/transmissoes/rafael_01.tres` e `rafael_02.tres`.

## 6. Direção de arte

- **O que a aparência precisa comunicar:** um rapaz de 20 anos de uniforme de segurança de 2008, um pouco largo nele, tentando parecer mais velho. Rádio HT e lanterna antiga sempre no cinto.
- **Visual definido:** [`assets/sprites/personagens/rafael/visual.md`](../../../assets/sprites/personagens/rafael/visual.md). Camisa azul-celeste de manga curta, larga demais, com dragonas e bolsos azul-marinho, emblema amarelo, boné, bigodinho ralo, rádio HT e lanterna no cinto. O rádio do inventário está em `assets/modelagem/interface/gerar_interface.py`.
- **Cor de identificação:** azul-celeste.
- Sprites em resolução dobrada, com o mesmo conjunto do Gabriel (ver `CLAUDE.md`).

## 7. Arquivos

- **Transmissões:** `dados/transmissoes/rafael_*.tres`, gatilhos `GatilhoRafael1` e `GatilhoRafael2` em `cenas/salas/biblioteca.tscn`.
- **Som do rádio:** `assets/audio/efeitos/objetos/radio_chiado.wav` (gerado por `assets/modelagem/audio/gerar_efeitos_registros.py`).
- **Sprites:** `assets/sprites/personagens/rafael/`, gerados por `assets/modelagem/personagens/gerar_rafael.py`.
- **Cena e diálogos em pessoa:** ainda não existem.

## 8. Pendências

- Como o Rafael parece ver Gabriel pelo rádio ("Ele falou como se estivesse me vendo") (Enredo Principal, seção 12.3).
- Onde fica o posto de guarda e em que fase Gabriel o encontra.
- As falas do rádio ainda não têm voz gravada.
