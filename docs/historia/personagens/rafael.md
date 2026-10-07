# Rafael (2008)

> **Status:** Em desenvolvimento. Já fala pelo rádio na Biblioteca.
> **Lei do projeto:** história, personalidade e arco estão no [Enredo Principal](../enredo_principal.md), seção 4.3 ("Rafael"). Esta ficha guarda só o que a produção precisa.

---

## 1. Resumo

- **Época de origem:** 2008.
- **Em uma frase:** o otimista teimoso que prefere acreditar que é reforma a encarar o fim do mundo.
- **Quem é:** segurança noturno da Unifor no primeiro emprego, com cerca de 20 anos, morador do bairro. Faz questão de ser chamado de "Seu Rafael".

## 2. No jogo

- **Onde aparece:** pelo rádio desde a Biblioteca. Em pessoa, no posto de guarda (fase pendente).
- **Esconderijo:** o "posto de guarda", uma sala de manutenção que ele transformou. Pode servir de **sala segura**.
- **Como chega ao jogador:** **rádio ao vivo** (o rádio portátil é um item comum do inventário) e, depois, em pessoa.
- **Função na jogabilidade:** dicas sobre as **rotinas de patrulha dos robôs** ("Antes de virar, ele dá um bipe. Ouviu o bipe, se esconde."). As dicas continuam valendo porque os robôs repetem a mesma rotina há séculos. As transmissões tocam sem pausar o jogo. Ver [`../../mecanicas/registros_e_caderno.md`](../../mecanicas/registros_e_caderno.md).
- **Parte para consertar a Âncora:** conhece o campus e as rondas, e sabe o que cada chave abre.

## 3. Registros

- **Suporte:** livro de ocorrências do vigia (tabela com data e hora) e o rádio, com chiado na tela.
- **Registros já escritos:** `dados/transmissoes/rafael_01.tres` e `rafael_02.tres`.

## 4. Direção de arte

- **O que a aparência precisa comunicar:** um rapaz de 20 anos de uniforme de segurança de 2008, um pouco largo nele, tentando parecer mais velho. Rádio HT e lanterna antiga sempre no cinto.
- **Visual definido:** o rádio portátil está em `assets/modelagem/interface/gerar_interface.py`. O personagem, ainda não.

## 5. Arquivos

- **Transmissões:** `dados/transmissoes/rafael_*.tres`, gatilhos `GatilhoRafael1` e `GatilhoRafael2` em `cenas/salas/biblioteca.tscn`.
- **Som do rádio:** `assets/audio/efeitos/objetos/radio_chiado.wav` (gerado por `assets/modelagem/audio/gerar_efeitos_registros.py`).
- **Cena, sprites e diálogos em pessoa:** ainda não existem.

## 6. Pendências

- Como o Rafael parece ver Gabriel pelo rádio ("Ele falou como se estivesse me vendo") (Enredo Principal, seção 12.3).
- Onde fica o posto de guarda e em que fase Gabriel o encontra.
- As falas do rádio ainda não têm voz gravada.
