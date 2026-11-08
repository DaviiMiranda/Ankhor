# seg_acordar — O despertar de Gabriel

- **Quando:** depois do prólogo, que termina no pulso da fenda.
- **Onde:** na cabine da Biblioteca em que Gabriel adormeceu, agora em 3026.
- **Personagem:** Gabriel, sozinho.
- **Formato:** três ilustrações em pixel art, sem falas.
- **Status:** em produção. A cena no Godot usa provisoriamente a imagem da cabine de 2026; os três quadros abaixo ainda precisam ser gerados e integrados.

## Referência comum para os três quadros

Usar como referência `assets/sprites/cutscenes/seg_prologo/cena_07_cabine_noite.png`, especialmente para o rosto, o cabelo castanho, o moletom vermelho e a composição da cabine. Manter o anel desgastado no dedo de Gabriel, o caderno de equações, o relógio e a mochila. Pixel art narrativa 2.5D de graphic novel, imagem horizontal 16:9, acabamento e escala de pixels coerentes com o prólogo, luz dramática e atmosfera de suspense. A Biblioteca está envelhecida e tomada pela natureza, com tecnologia de 3026 integrada ao ambiente; não mostrar outras pessoas, robôs, Carlos ou a Âncora. Sem legendas, letras legíveis, logotipos ou marcas-d’água. Os quadros são imagens únicas, sem divisão em painéis.

### Quadro 1 — A cabine transformada

Mesmo enquadramento da cabine do prólogo: Gabriel continua dormindo com a cabeça sobre os braços, diante do caderno aberto. A luminária, o relógio e a mochila ajudam a reconhecer o lugar. A cabine agora apresenta desgaste e sinais de natureza ao redor; painéis discretos emitem luz ciano e um holograma aceso paira sobre o caderno. A luz fria recorta o moletom vermelho e substitui o aconchego anterior por estranheza. Gabriel ainda não percebeu a mudança.

### Quadro 2 — Abrindo os olhos

Plano médio, no mesmo lado da cabine e com os mesmos objetos em posições consistentes. Gabriel está se erguendo devagar da mesa e esfregando os olhos, sonolento. O anel aparece na mão; o caderno e o holograma continuam à frente dele. O brilho ciano dos painéis ilumina parcialmente seu rosto e contrasta com o vermelho do moletom. A expressão passa do sono à confusão, sem ação exagerada.

### Quadro 3 — A Biblioteca desconhecida

Plano mais aberto a partir da cabine: Gabriel já está erguido, olhando em volta sem entender, com a mesa e o caderno próximos. Revelar a Biblioteca envelhecida e a vegetação, com estantes e torres de equipamentos entre elas, iluminadas por pequenos pontos ciano. Gabriel permanece sozinho e em escala humana diante do espaço. A composição deve orientar o olhar da cabine para o ambiente desconhecido.

## Integração prevista

Gerar as três imagens com a mesma aparência de personagem e cenário, preparar versões finais em 640 × 360 e colocá-las em `assets/sprites/cutscenes/seg_acordar/`. Montar as transições na animação `principal` da cena `cenas/cutscenes/seg_acordar.tscn`. A duração e os sons dos novos quadros ainda precisam ser definidos na montagem. O botão Pular e Esc continuam levando à cabine jogável. A imagem provisória atual é `cena_07_cabine_noite.png` e não representa a versão final em 3026.
