# Henrique (2019), o pesquisador

> **Status:** Em definição.
> **Lei do projeto:** esta ficha faz parte do [Enredo Principal](../enredo_principal.md) e tem a mesma autoridade: quem o Henrique é vale como está escrito aqui. A história em volta dele (o acidente, a ordem dos acontecimentos, as pendências) está no Enredo.

---

## 1. Quem é

- **Época de origem:** 2019.
- **Quem é:** aluno de iniciação científica da Unifor, com cerca de 20 anos.
- **História:** estudava à noite na Biblioteca e sumiu. O orientador transformou o projeto dele na cadeira que Gabriel cursa, e as equações do caderno de Gabriel continuam esse trabalho sem Gabriel saber de quem eram. Em 3026, fica na **sala de dados do bunker**, junto do Zane, com acesso às **câmeras** do campus: de lá vê tudo e guia o grupo pelo rádio, na frequência que o Zane mantém. É a voz que dá as dicas de patrulha a Gabriel desde a Biblioteca. Fala pouco e fica na dele. E **engana o grupo**: esconde a ligação que tem com o **Carlos**. Se trabalha para ele ou foi enganado por ele está pendente. Quando o grupo descobre a mentira, todos vão atrás do Carlos.

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
| O grupo | Guia todos pelo rádio, mas fala pouco e fica na dele. Engana todos, e a mentira é descoberta |
| [Zane](zane.md) | Dividem a sala de dados do bunker: o Zane cuida da frequência e das ligações, o Henrique das câmeras |
| [Clarice](clarice.md) e [Diana](diana.md) | Falam com ele pelo rádio, da 103 do Bloco de salas: passam o que descobrem, e ele confere nas câmeras |
| [Gabriel](gabriel.md) | É a voz que o guia desde a primeira fase. Quando a mentira aparece, quem ajudou Gabriel o jogo todo era quem escondia a verdade |

## 4. No jogo

- **Onde aparece:** pela voz no rádio desde a Biblioteca. Em pessoa, na sala de dados do bunker.
- **Esconderijo:** o **bunker**, na **sala de dados** (a central de dados), com o Zane e com acesso às **câmeras** do campus e ao rádio.
- **Como chega ao jogador:** **rádio ao vivo** (o rádio portátil é um item comum do inventário) e, depois, em pessoa.
- **Função na jogabilidade:** dicas sobre as **rotinas de patrulha dos robôs**, vendo pelas câmeras ("Antes de virar, ele dá um bipe. Ouviu o bipe, se esconde."). As dicas continuam valendo porque os robôs repetem a mesma rotina há séculos. As transmissões tocam sem pausar o jogo. Ver [`../../mecanicas/registros_e_caderno.md`](../../mecanicas/registros_e_caderno.md).
- **Parte para consertar a Âncora:** a teoria por trás das equações.

## 5. Registros

- **Suporte:** pendente. Uma sugestão que combina com ele: folhas de rascunho cheias de contas riscadas e corrigidas, na letra miúda de quem se corrige no meio da frase.
- **Já escritos:** `dados/transmissoes/henrique_01.tres` (Biblioteca, balcão), `henrique_02.tres` (Biblioteca, acervo) e `henrique_03.tres` (Bloco de salas), mais as duas conversas em pessoa do bunker. No rádio, fala pausado e técnico, se corrigindo.

## 6. Direção de arte

- **O que a aparência precisa comunicar:** um aluno de 2019 de 20 anos, introvertido e cansado, que fala pouco e anota muito.
- **Visual definido:** [`assets/sprites/personagens/henrique/visual.md`](../../../assets/sprites/personagens/henrique/visual.md). Camisa de flanela xadrez aberta sobre camiseta cinza, jeans preto, tênis de lona, óculos redondos de aro fino, cabelo bagunçado na testa, o caderno sempre na mão e um lápis atrás da orelha.
- **Cor de identificação:** laranja-queimado.
- Sprites em resolução dobrada, com o mesmo conjunto do Gabriel (ver `CLAUDE.md`).

## 7. Arquivos

- **Sprites:** `assets/sprites/personagens/henrique/`, gerados por `assets/modelagem/personagens/gerar_henrique.py`.
- **Cena:** `cenas/personagens/henrique.tscn` (parado) e `cenas/personagens/henrique_na_estacao.tscn` (de costas, na estação da sala de dados do bunker, olhando as câmeras).
- **Diálogos em pessoa:** `dados/dialogos/henrique_primeiro_encontro.json` e `henrique_de_novo.json`, no bunker.
- **Transmissões:** `dados/transmissoes/henrique_*.tres`, gatilhos `GatilhoHenrique1` (em `cenas/salas/biblioteca/balcao.tscn`) e `GatilhoHenrique2` (em `acervo.tscn`).
- **Som do rádio:** `assets/audio/efeitos/objetos/radio_chiado.wav` (gerado por `assets/modelagem/audio/gerar_efeitos_registros.py`).

## 8. Pendências

- Se trabalha para o Carlos ou foi enganado por ele, o que exatamente esconde, e como e quando o grupo descobre (Enredo Principal, seção 12.7).
- Quando Gabriel o encontra em pessoa na sala de dados, e se o acesso às câmeras vira uma mecânica (Enredo Principal, seção 12.3).
- As falas do rádio ainda não têm voz gravada.
