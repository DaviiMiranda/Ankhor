# Henrique (2019), o pesquisador

> **Status:** Em definição.
> **Lei do projeto:** esta ficha faz parte do [Enredo Principal](../enredo_principal.md) e tem a mesma autoridade: quem o Henrique é vale como está escrito aqui. A história em volta dele (o acidente, a ordem dos acontecimentos, as pendências) está no Enredo.

---

## 1. Quem é

- **Época de origem:** 2019.
- **Quem é:** aluno de iniciação científica da Unifor, com cerca de 20 anos.
- **História:** estudava à noite na Biblioteca e sumiu. O orientador transformou o projeto dele na cadeira que Gabriel cursa, e as equações do caderno de Gabriel continuam esse trabalho sem Gabriel saber de quem eram. Em 3026, fica **sozinho num posto de monitoramento**, de onde vê o campus pelas câmeras e guia o grupo pelo rádio, na frequência que a Clarice montou. É a voz que dá as dicas de patrulha a Gabriel desde a Biblioteca. Fala pouco e fica distante dos outros. E **engana o grupo**: esconde a ligação que tem com o **Carlos**. Se trabalha para ele ou foi enganado por ele está pendente. Quando o grupo descobre a mentira, todos vão atrás do Carlos.

## 2. Personalidade

- **Essência:** um gênio quieto que desconfia ter causado tudo.
- **Traços:** introvertido, perfeccionista, ansioso, gentil. Brilhante em teoria e sem jeito com gente.
- **Como fala:** pausado e técnico. Se corrige no meio da frase.
- **O que quer:** entender a Âncora para provar a si mesmo que não é culpado.
- **O que teme:** que a pesquisa dele tenha levado à Âncora.
- **Defeito:** guarda segredos, e mente para o grupo.
- **Arco:** da mentira à verdade: quando o grupo descobre que ele enganou todo mundo, ele precisa assumir a responsabilidade.

## 3. Relações

| Com | Dinâmica |
|---|---|
| [Carlos](carlos.md) | Trabalha para ele ou foi enganado por ele (pendente) |
| O grupo | Guia todos pelo rádio, mas fala pouco e fica distante. Engana todos, e a mentira é descoberta |
| [Gabriel](gabriel.md) | É a voz que o guia desde a primeira fase. Quando a mentira aparece, quem ajudou Gabriel o jogo todo era quem escondia a verdade |

## 4. No jogo

- **Onde aparece:** pela voz no rádio desde a Biblioteca. Em pessoa, no posto de monitoramento (fase pendente).
- **Esconderijo:** o **posto de monitoramento**, sozinho, com as câmeras e o rádio (onde fica, pendente).
- **Como chega ao jogador:** **rádio ao vivo** (o rádio portátil é um item comum do inventário) e, depois, em pessoa.
- **Função na jogabilidade:** dicas sobre as **rotinas de patrulha dos robôs**, vendo pelas câmeras ("Antes de virar, ele dá um bipe. Ouviu o bipe, se esconde."). As dicas continuam valendo porque os robôs repetem a mesma rotina há séculos. As transmissões tocam sem pausar o jogo. Ver [`../../mecanicas/registros_e_caderno.md`](../../mecanicas/registros_e_caderno.md).
- **Parte para consertar a Âncora:** a teoria por trás das equações.

## 5. Registros

- **Suporte:** pendente. Uma sugestão que combina com ele: folhas de rascunho cheias de contas riscadas e corrigidas, na letra miúda de quem se corrige no meio da frase.
- **Já escritos:** `dados/transmissoes/henrique_01.tres` (Biblioteca, balcão) e `henrique_02.tres` (Biblioteca, acervo). No rádio, fala pausado e técnico, se corrigindo, e não diz de quem é a frequência.

## 6. Direção de arte

- **O que a aparência precisa comunicar:** um aluno de 2019 de 20 anos, introvertido e cansado, que fala pouco e anota muito.
- **Visual definido:** [`assets/sprites/personagens/henrique/visual.md`](../../../assets/sprites/personagens/henrique/visual.md). Camisa de flanela xadrez aberta sobre camiseta cinza, jeans preto, tênis de lona, óculos redondos de aro fino, cabelo bagunçado na testa, o caderno sempre na mão e um lápis atrás da orelha.
- **Cor de identificação:** laranja-queimado.
- Sprites em resolução dobrada, com o mesmo conjunto do Gabriel (ver `CLAUDE.md`).

## 7. Arquivos

- **Sprites:** `assets/sprites/personagens/henrique/`, gerados por `assets/modelagem/personagens/gerar_henrique.py`.
- **Cena:** `cenas/personagens/henrique.tscn` (parado, por enquanto só na sala de teste).
- **Transmissões:** `dados/transmissoes/henrique_*.tres`, gatilhos `GatilhoHenrique1` (em `cenas/salas/biblioteca/balcao.tscn`) e `GatilhoHenrique2` (em `acervo.tscn`).
- **Som do rádio:** `assets/audio/efeitos/objetos/radio_chiado.wav` (gerado por `assets/modelagem/audio/gerar_efeitos_registros.py`).

## 8. Pendências

- Se trabalha para o Carlos ou foi enganado por ele, o que exatamente esconde, e como e quando o grupo descobre (Enredo Principal, seção 12.7).
- Onde fica o posto de monitoramento, e quando Gabriel o encontra em pessoa.
- As falas do rádio ainda não têm voz gravada.
