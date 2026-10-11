# Zane (2123), o das comunicações

> **Status:** Em desenvolvimento. Visual e sprites prontos; ainda sem cena no bunker.
> **Lei do projeto:** esta ficha faz parte do [Enredo Principal](../enredo_principal.md) e tem a mesma autoridade: quem o Zane é vale como está escrito aqui. A história em volta dele (o acidente, a ordem dos acontecimentos, as pendências) está no Enredo.

---

## 1. Quem é

- **Época de origem:** 2123, quando a Unifor já era um polo de IA.
- **Quem é:** jovem com implantes cibernéticos, com cerca de 20 anos, que morava no que sobrou do bairro.
- **História:** é quem mais entende a tecnologia da Âncora. Chegou a 3026 **antes da Clarice e de Gabriel**, achou o **bunker** e montou ali, no **computador da central de dados**, o centro das comunicações do grupo: mantém a **frequência de rádio** de todos e liga pelos telefones velhos do campus. É ele quem liga para Gabriel no fim da Biblioteca e destranca, pelo sistema, a porta de saída.

## 2. Personalidade

- **Essência:** filho de um mundo já cheio de máquinas, que sabe tudo de tecnologia e nada de sobreviver.
- **Traços:** confiante, direto, irreverente, elétrico, e mais assustado do que admite.
- **Como fala:** rápido, com gírias de um futuro que ninguém reconhece. Interrompe os outros.
- **O que quer:** no começo, voltar. Mais tarde, entender o que a IA virou, porque na época dele a IA ainda estava começando.
- **O que teme:** a IA. Ele sabe melhor que ninguém do que as máquinas são capazes.
- **Defeito:** confia demais na tecnologia: acha que toda máquina tem conserto, até a IA. É a contradição dele: tem medo da IA e, ao mesmo tempo, acha que consegue domá-la.
- **Arco:** no fim, **escolhe ficar em 3026**: voltar para 2123 é voltar para o mundo que vai virar o da IA, e ele decide ficar para tentar domar a IA por dentro.

## 3. Relações

| Com | Dinâmica |
|---|---|
| [Gabriel](gabriel.md) | A voz do telefone que abre a saída da Biblioteca. Do computador do bunker, mantém Gabriel em contato com todo mundo |
| [Diana](diana.md) | Dividem o bunker |
| [Baltazar](baltazar.md) | Os dois extremos do tempo: fé contra tecnologia, e ainda assim os dois mais curiosos do grupo |

## 4. No jogo

- **Onde aparece:** pelo telefone desde a Biblioteca. Em pessoa, no **bunker**, sentado no computador da central de dados.
- **Esconderijo:** o **bunker**, com a Diana.
- **Como chega ao jogador:** **telefone** (a primeira ligação é no balcão da Biblioteca), a frequência de rádio do grupo e, no bunker, em pessoa.
- **Função na jogabilidade:** as **comunicações**: põe Gabriel em contato com os outros, abre portas pelo sistema e tenta quebrar a senha do setor B do bunker. Por entender de tecnologia, é um candidato natural a trazer o **notebook** (gadget de hackear portas e robôs), mas isso não está decidido.
- **Parte para consertar a Âncora:** a tecnologia mais próxima da Âncora.

## 5. Registros

- **Suporte:** áudio com interface holográfica: tela ciano com forma de onda e falhas de sinal. Ainda não existe no jogo.
- **Já escritos:** a ligação do fim da Biblioteca, `dados/transmissoes/zane_01.tres`.

## 6. Direção de arte

- **O que a aparência precisa comunicar:** um rapaz de 20 anos de 2123, com implantes visíveis, roupa de um futuro que ninguém reconhece, confiante e elétrico. Tem que destoar de todos os outros: é o único que veio de depois de Gabriel.
- **Visual definido:** [`assets/sprites/personagens/zane/visual.md`](../../../assets/sprites/personagens/zane/visual.md). Braço direito de prótese com linhas de luz ciano, olho de implante, placa na têmpora e porta na nuca; jaqueta técnica curta amarelo-ácido com gola alta; cabelo raspado dos lados com o topo descolorido.
- **Cor de identificação:** amarelo-ácido (Gabriel vermelho, Clarice verde-azulado).
- Sprites em resolução dobrada, com o mesmo conjunto do Gabriel (ver `CLAUDE.md`).
- **Falta:** o Zane **sentado na estação de trabalho do bunker**. Hoje a estação é desenhada junto com a Clarice (`gerar_clarice.py`).

## 7. Arquivos

- **Sprites:** `assets/sprites/personagens/zane/`
- **Gerador:** `assets/modelagem/personagens/gerar_zane.py`
- **Cena:** `cenas/personagens/zane.tscn` (parado, por enquanto só na sala de teste).
- **Ligação:** `dados/transmissoes/zane_01.tres`, tocada pelo telefone do balcão (`cenas/sistemas/telefone.tscn`).

## 8. Pendências

- O que fazia no ponto quando foi puxado (Enredo Principal, seção 12.3).
- A arte dele na estação de trabalho e as conversas do bunker, que hoje são da Clarice (seção 12.4).
- O arco dele (medo da IA, ficar para domá-la) depende de a IA continuar existindo (seção 12.2).
