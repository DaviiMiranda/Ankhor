# Baltazar Magalhães (~1750), o antepassado

> **Status:** Em definição. O acampamento e o diário já estão na Biblioteca.
> **Lei do projeto:** esta ficha faz parte do [Enredo Principal](../enredo_principal.md) e tem a mesma autoridade: quem o Baltazar é vale como está escrito aqui. A história em volta dele (o acidente, a família Magalhães, as pendências) está no Enredo.

---

## 1. Quem é

- **Época de origem:** ~1750, Ceará colonial.
- **Quem é:** filho de colonos portugueses, com cerca de 20 anos, curioso, com uma luneta herdada do pai. A família tem um sítio na mata onde hoje fica o campus. **Antepassado de Gabriel**, umas dez gerações antes dele.
- **História:** viu pela luneta uma luz estranha sobre a mata, no sítio da família, foi investigar e foi puxado. Acha que tudo aquilo é o Juízo Final ("o Tormento de Leviatã"). Na Biblioteca, deixou um **acampamento** entre as raízes da árvore: luneta rachada, vela, diário e um robô desmontado peça por peça. Depois seguiu em frente ("Hei de seguir a luz até onde ella nasce"), e Gabriel o encontra mais tarde.

## 2. Personalidade

- **Essência:** um homem de fé com olhos de cientista, preso entre o milagre e a explicação.
- **Traços:** cerimonioso, educado, corajoso por curiosidade, devoto, encantado com tudo.
- **Como fala:** português arcaico e formal. Trata todos por "Vossa Mercê" e solta latim quando está aflito.
- **O que quer:** entender o que vê. Para ele, observar o céu é uma forma de rezar. Por isso, em 3026, **quer ficar**: tudo ali é um milagre a estudar.
- **O que teme:** que aquilo seja castigo divino pelos pecados dele.
- **Defeito:** teimoso. Explica tudo pela religião antes de aceitar outra explicação.
- **Arco:** do "Juízo Final" à compreensão. Ao saber que Gabriel é descendente dele, fica protetor e orgulhoso, com um humor terno ("meu neto de mil anos"). No fim, quer ficar em 3026, mas **precisa voltar**, ou a família de Gabriel não existe. Gabriel tem que convencer o próprio antepassado a ir embora.

## 3. Relações

| Com | Dinâmica |
|---|---|
| [Gabriel](gabriel.md) | Família descoberta. No fim, é Gabriel quem o convence a voltar para 1750 |
| [Zane](zane.md) | Os dois extremos do tempo: fé contra tecnologia, e ainda assim os dois mais curiosos do grupo |

## 4. No jogo

- **Onde aparece:** na Biblioteca, só o acampamento que ele deixou. Em pessoa, numa fase mais à frente (pendente).
- **Esconderijo:** na **Biblioteca**, num esconderijo dentro dela (o ponto exato está pendente).
- **Como chega ao jogador:** primeiro pelo **diário** e pelo acampamento; depois em pessoa.
- **Função na jogabilidade:** o diário ensina o **ponto fraco do sensor óptico**: os robôs de um olho só não veem quem passa pelas costas ou pelo lado, e luz forte no olho os cega por alguns segundos. Liga com a cápsula de clarão.
- **O anel:** o mesmo anel que Gabriel tem gasto no inventário aparece novo no dedo do Baltazar. A comparação no inventário é como o jogador descobre o parentesco.
- **Parte para consertar a Âncora:** as estrelas: o céu é o único relógio que não muda, e é por ele que se acerta a data de volta de cada um.

## 5. Registros

- **Suporte:** diário de pergaminho escrito à pena (`papel = pergaminho`). Papel amarelado, tinta marrom, desenhos a traço. Português arcaico, com latim.
- **Já escritos:** `dados/documentos/diario_baltazar.tres` (4 páginas).
- **No cenário:** luneta de latão com a lente rachada, toco de vela, diário embrulhado em pano encerado, mapas de estrelas riscados na casca da árvore e um robô desmontado peça por peça.

## 6. Direção de arte

- **O que a aparência precisa comunicar:** um rapaz de 20 anos do século XVIII, de família de sítio, sem nada de nobre. Roupa simples de colono, gasta pelos dias em 3026. A luneta sempre por perto. O **anel** visível na mão.
- **Visual definido:** [`assets/sprites/personagens/baltazar/visual.md`](../../../assets/sprites/personagens/baltazar/visual.md). Tricórnio, cabelo preso com fita, casaca vinho gasta e remendada, colete, calções, meias e sapato de fivela; a luneta de latão numa bandoleira de couro e o anel de ouro na mão direita.
- **Cor de identificação:** vinho (pau-brasil), um eco escuro do vermelho do Gabriel.
- Sprites em resolução dobrada, com o mesmo conjunto do Gabriel (ver `CLAUDE.md`).

## 7. Arquivos

- **Acampamento:** `assets/modelagem/cenario/gerar_antecessores.py`, nó `AcampamentoBaltazar` em `cenas/salas/biblioteca.tscn`.
- **Diário:** `dados/documentos/diario_baltazar.tres`, nó `DiarioBaltazar` na Biblioteca.
- **Sprites:** `assets/sprites/personagens/baltazar/`, gerados por `assets/modelagem/personagens/gerar_baltazar.py`.
- **Cena:** `cenas/personagens/baltazar.tscn` (parado, por enquanto só na sala de teste).
- **Diálogos:** ainda não existem.

## 8. Pendências

- Em que fase Gabriel o encontra e onde fica, dentro da Biblioteca, o esconderijo dele (Enredo Principal, seção 12.3).
- Gabriel falhando na tela enquanto o Baltazar estiver fora de 1750 (seção 12.3).
- O item do anel no inventário ainda não existe.
