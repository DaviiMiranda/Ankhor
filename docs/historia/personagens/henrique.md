# Henrique (2019), o pesquisador

> **Status:** Em definição.
> **Lei do projeto:** esta ficha faz parte do [Enredo Principal](../enredo_principal.md) e tem a mesma autoridade: quem o Henrique é vale como está escrito aqui. A história em volta dele (o acidente, a ordem dos acontecimentos, as pendências) está no Enredo.

---

## 1. Quem é

- **Época de origem:** 2019.
- **Quem é:** aluno de iniciação científica da Unifor, com cerca de 20 anos.
- **História:** fazia uma **pesquisa sobre viagem no tempo** e estudava à noite na Biblioteca quando sumiu. A mãe dele tinha morrido antes disso. Em 2026, o sumiço dele é **lenda do campus** ("o aluno que sumiu na Biblioteca em 2019"), e o orientador levou a pesquisa adiante até ela virar a cadeira de **Modelagem e Simulação**, a que Gabriel cursa: as equações do caderno de Gabriel vêm dela, sem ele saber de quem eram.
- **Em 3026:** **foi o primeiro a chegar** e é quem está lá há mais tempo. O Carlos o achou e prometeu levá-lo de volta **para antes da morte da mãe**; o Henrique acreditou e passou a trabalhar para ele. O Carlos só o usa: a função dele é **atrasar o grupo** enquanto o Carlos conserta a Âncora. Fica **sozinho** numa sala de dados **trancada** do bunker, com acesso às **câmeras** do campus: de lá **ajuda a Clarice e a Diana pelo rádio**, na frequência que o Zane mantém, e é dele o que a Clarice repassa a Gabriel como dica de patrulha desde a Biblioteca. Diz que está tentando consertar tudo, mas **não faz nada pelo grupo**: usa a **IA de 3026** para continuar a própria pesquisa, só para voltar a antes da morte da mãe. É ele quem diz ao grupo que estão em 3026 (sabe pelo Carlos). Fala pouco e fica na dele. As dicas que passa são verdadeiras, mas mantém cada um no seu canto, e tudo o que o grupo sabe passa por ele. Quando o grupo descobre a mentira, todos vão atrás do Carlos.

## 2. Personalidade

- **Essência:** um gênio quieto que desconfia ter causado tudo.
- **Traços:** introvertido, perfeccionista, ansioso, gentil. Brilhante em teoria e sem jeito com gente.
- **Como fala:** pausado e técnico. Se corrige no meio da frase.
- **O que quer:** voltar para antes da morte da mãe. Como o Carlos, quer fugir para um passado que não é mais o dele.
- **O que teme:** que a pesquisa dele tenha levado à Âncora.
- **Defeito:** guarda segredos, e mente para o grupo.
- **Arco:** da mentira à verdade: quando o grupo descobre que ele enganou todo mundo, ele precisa assumir a responsabilidade.

## 3. Relações

| Com | Dinâmica |
|---|---|
| [Carlos](carlos.md) | Trabalha para ele, por causa da promessa sobre a mãe. O Carlos só o usa para atrasar o grupo |
| O grupo | Ajuda pelo rádio, mas fala pouco e fica na dele. Mantém cada um no seu canto. Engana todos, e a mentira é descoberta |
| [Zane](zane.md) | O Zane desconfia dele e passa dias tentando invadir o bunker para ver o que ele faz. Só consegue com Gabriel, no Labirinto |
| [Clarice](clarice.md) e [Diana](diana.md) | Falam com ele pelo rádio, da 103 do Bloco de salas: ele as ajuda com o que vê nas câmeras, e elas juntam isso com o que descobrem. A Clarice repassa a Gabriel |
| [Gabriel](gabriel.md) | Não fala direto com ele pelo rádio: o que o ajuda chega pela Clarice. O primeiro contato dos dois é em pessoa, no bunker, e Gabriel o reconhece pela lenda do campus. Quando a mentira aparece, quem ajudou Gabriel o jogo todo, por trás da Clarice, era quem escondia a verdade |

## 4. No jogo

- **Onde aparece:** pelo que a Clarice repassa, desde a Biblioteca. Em pessoa, na sala de dados do bunker.
- **Esconderijo:** o **bunker**, sozinho, na **sala de dados** (a central de dados), trancada e difícil de alcançar, com acesso às **câmeras** do campus e ao rádio. Os robôs patrulham o resto do bunker. O Carlos nunca vai lá.
- **Como chega ao jogador:** pela voz da **Clarice** no rádio (o rádio portátil é um item comum do inventário) e, depois, em pessoa.
- **Função na jogabilidade:** dicas sobre as **rotinas de patrulha dos robôs**, vendo pelas câmeras e passando para a Clarice, que as diz a Gabriel ("Antes de virar, ele dá um bipe. Ouviu o bipe, se esconde."). As dicas continuam valendo porque os robôs repetem a mesma rotina há séculos. As transmissões tocam sem pausar o jogo. Ver [`../../mecanicas/registros_e_caderno.md`](../../mecanicas/registros_e_caderno.md).
- **Parte para consertar a Âncora:** a teoria por trás das equações.

## 5. Registros

- **Suporte:** pendente. Uma sugestão que combina com ele: folhas de rascunho cheias de contas riscadas e corrigidas, na letra miúda de quem se corrige no meio da frase.
- **Já escritos:** as duas conversas em pessoa do bunker. Ele não tem transmissão própria: as da Biblioteca e do Bloco de salas que eram dele passaram a ser da Clarice (`clarice_biblioteca_01`, `clarice_biblioteca_02` e `clarice_04`).

## 6. Direção de arte

- **O que a aparência precisa comunicar:** um aluno de 2019 de 20 anos, introvertido e cansado, que fala pouco e anota muito.
- **Visual definido:** [`assets/sprites/personagens/henrique/visual.md`](../../../assets/sprites/personagens/henrique/visual.md). Camisa de flanela xadrez aberta sobre camiseta cinza, jeans preto, tênis de lona, óculos redondos de aro fino, cabelo bagunçado na testa, o caderno sempre na mão e um lápis atrás da orelha.
- **Cor de identificação:** laranja-queimado.
- Sprites em resolução dobrada, com o mesmo conjunto do Gabriel (ver `CLAUDE.md`).

## 7. Arquivos

- **Sprites:** `assets/sprites/personagens/henrique/`, gerados por `assets/modelagem/personagens/gerar_henrique.py`.
- **Cena:** `cenas/personagens/henrique.tscn` (parado) e `cenas/personagens/henrique_na_estacao.tscn` (de costas, na estação da sala de dados do bunker, olhando as câmeras).
- **Diálogos em pessoa:** `dados/dialogos/henrique_primeiro_encontro.json` e `henrique_de_novo.json`, no bunker.

## 8. Pendências

- Como e quando o grupo descobre a mentira, e o que ele faz depois (Enredo Principal, seção 10.3).
- Como e quando a mãe morreu; onde a lenda do campus aparece para o jogador (Enredo Principal, seção 10.3).
- Se o acesso às câmeras vira uma mecânica ([pendências de produção](../../pendencias_de_producao.md)).
- As conversas do bunker (`henrique_primeiro_encontro.json` e `henrique_de_novo.json`) precisam ser conferidas: ele agora está sozinho e diz que está tentando consertar tudo ([pendências de produção](../../pendencias_de_producao.md)).
