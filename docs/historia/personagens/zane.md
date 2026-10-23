# Zane (2123), o das comunicações

> **Status:** Em desenvolvimento. Visual e sprites prontos; ainda sem cena no bunker.
> **Lei do projeto:** esta ficha faz parte do [Enredo Principal](../História_Completa.md) e tem a mesma autoridade: quem o Zane é vale como está escrito aqui. A história em volta dele (o acidente, a ordem dos acontecimentos, as pendências) está no Enredo.

---

## 1. Quem é

- **Época de origem:** 2123, quando a Unifor já era um polo de IA.
- **Quem é:** jovem com implantes cibernéticos, com cerca de 20 anos, que morava no que sobrou do bairro.
- **História:** é quem mais entende a tecnologia da Âncora. Chegou a 3026 **antes da Clarice e de Gabriel** e montou na **oficina do Labirinto**, no subsolo, o centro das comunicações do grupo: mantém a **frequência de rádio** de todos e liga pelos telefones velhos do campus. Depois que a Clarice passou dias sozinha antes de alguém achá-la, deixou um rádio sintonizado no balcão da Biblioteca, para que o próximo não passasse pelo mesmo. É ele quem liga para Gabriel no fim da Biblioteca e destranca, pelo sistema, a porta de saída. Quer muito resolver tudo aquilo e **desconfia do Henrique**: está há dias na oficina tentando invadir o bunker, onde o Henrique fica, e só consegue com a ajuda de Gabriel, no Labirinto.
- **Objeto-símbolo:** os **óculos**. A Clarice também usa óculos (grandes e redondos), então os dois pares precisam ser fáceis de distinguir.

## 2. Personalidade

- **Essência:** filho de um mundo já cheio de máquinas, que sabe tudo de tecnologia e nada de sobreviver.
- **Traços:** confiante, direto, irreverente, elétrico, e mais assustado do que admite.
- **Como fala:** rápido, com gírias de um futuro que ninguém reconhece. Interrompe os outros.
- **O que quer:** resolver tudo aquilo e descobrir o que o Henrique esconde.
- **O que teme:** pendente. O medo antigo (a IA) saiu: em 3026 a IA é uma ferramenta, sem consciência (Enredo Principal, seção 2.1).
- **Defeito:** confia demais na tecnologia: acha que toda máquina tem conserto.
- **Arco:** pendente (Enredo Principal, seção 10.4). O arco antigo, ficar em 3026 para domar a IA, saiu.

## 3. Relações

| Com | Dinâmica |
|---|---|
| [Gabriel](gabriel.md) | A voz do telefone que abre a saída da Biblioteca. Da oficina do Labirinto, mantém Gabriel em contato com todo mundo, e precisa dele para invadir o bunker |
| [Henrique](henrique.md) | Desconfia dele. Passa dias tentando invadir o bunker para ver o que o Henrique faz lá |
| [Baltazar](baltazar.md) | Os dois extremos do tempo: fé contra tecnologia, e ainda assim os dois mais curiosos do grupo |

## 4. No jogo

- **Onde aparece:** pelo telefone desde a Biblioteca. Em pessoa, primeiro na **oficina do Labirinto** e depois no **bunker**, aonde chega depois de Gabriel: quando Gabriel religa a energia, ele quebra a senha do setor B, chama Gabriel pelo rádio e está no encontro do grupo na sala de dados (Enredo, Ato 3). As falas ali são rascunho.
- **Esconderijo:** a **oficina do Labirinto**, num canto do subsolo, perto de onde Gabriel chega. É a base dele. Só entra no bunker depois que Gabriel quebra a trava.
- **Como chega ao jogador:** **telefone** (a primeira ligação é no balcão da Biblioteca), a frequência de rádio do grupo e, em pessoa, na oficina do Labirinto e no bunker.
- **Função na jogabilidade:** as **comunicações**: põe Gabriel em contato com os outros, abre portas pelo sistema e tenta quebrar a senha do setor B do bunker. No Labirinto ele **entrega o notebook** a Gabriel (gadget de hackear portas e robôs) e pede que invada três nós de controle da rede do subsolo, que guardam a trava do bunker, porque de longe ele não consegue; quando o terceiro cai, chama Gabriel de volta pelo rádio e revela o alçapão escondido da oficina, que é a saída.
- **Parte para consertar a Âncora:** a tecnologia mais próxima da Âncora.

## 5. Registros

- **Suporte:** áudio com interface holográfica: tela ciano com forma de onda e falhas de sinal. Ainda não existe no jogo.
- **Já escritos:** a ligação do fim da Biblioteca, `dados/transmissoes/zane_01.tres`; as conversas da oficina, `dados/dialogos/zane_labirinto_primeiro_encontro.json`, `zane_labirinto_notebook.json`, `zane_labirinto_de_novo.json`, `zane_labirinto_alcapao.json` (revela o alçapão) e `zane_labirinto_alcapao_de_novo.json`; e o chamado pelo rádio quando o terceiro nó cai, `dados/transmissoes/zane_labirinto_01.tres`.

## 6. Direção de arte

- **O que a aparência precisa comunicar:** um rapaz de 20 anos de 2123, com implantes visíveis, roupa de um futuro que ninguém reconhece, confiante e elétrico. Tem que destoar de todos os outros: é o único que veio de depois de Gabriel.
- **Visual definido:** [`assets/sprites/personagens/zane/visual.md`](../../../assets/sprites/personagens/zane/visual.md). Braço direito de prótese com linhas de luz ciano, olho de implante, placa na têmpora e porta na nuca; jaqueta técnica curta amarelo-ácido com gola alta; cabelo raspado dos lados com o topo descolorido.
- **Cor de identificação:** amarelo-ácido (Gabriel vermelho, Clarice verde-azulado).
- Sprites em resolução dobrada, com o mesmo conjunto do Gabriel (ver `CLAUDE.md`).
- **Feito:** o Zane **na oficina do Labirinto** (`cenas/personagens/zane_na_oficina.tscn`), parado, em pé em frente à mesa com o computador, entre bancadas, racks e telas holográficas.
- **Falta:** o Zane **na sala de dados do bunker**. A estação agora existe sozinha (`assets/sprites/cenario/objetos/estacao_dados.png`) e quem aparece nela é o Henrique; o Zane precisa de um lugar na sala (a mesma estação, uma segunda ou o computador do gerador).

## 7. Arquivos

- **Sprites:** `assets/sprites/personagens/zane/`
- **Gerador:** `assets/modelagem/personagens/gerar_zane.py`
- **Cena:** `cenas/personagens/zane.tscn` (parado) e `cenas/personagens/zane_na_oficina.tscn` (com a conversa, no Labirinto).
- **Ligação:** `dados/transmissoes/zane_01.tres`, tocada pelo telefone do balcão (`cenas/sistemas/telefone.tscn`).

## 8. Pendências

- Os óculos do Zane ainda não estão no visual dele (`assets/sprites/personagens/zane/visual.md` e `gerar_zane.py`).
- O que fazia no ponto quando foi puxado (Enredo Principal, seção 10.4).
- A cena e as conversas dele na sala de dados do bunker, que hoje só mostram o Henrique ([pendências de produção](../../pendencias_de_producao.md)).
- O que teme e o final dele (seção 10.4). Opções em conversa: ficar em 3026 para guardar a Âncora, ficar para se juntar aos Faroleiros, ou voltar para 2123.
