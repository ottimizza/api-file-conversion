# Estratégias de Leitura e Conversão 

### 1. LTTextLine (Quebras como Múltiplas Linhas) - PADRÃO

Estratégia padrão de conversão de **PDFs**. Cada quebra de linha dentro das caixas de texto, são convertidas em novas linhas no CSV final.

#### Exemplo 1:

* *PDF Original*

    | Descricao                   	| Valor         	| ... 	|
    |-----------------------------	|---------------	|-----	|
    | SUPERMERCADO<br>WALMOR LTDA 	| R$ 896.43<br><br>	| ... 	|
    | ...                         	| ...           	| ... 	|

* *CSV Convertido*

    | Descricao                   	| Valor     	| ... 	|
    |-----------------------------	|-----------	|-----	|
    | SUPERMERCADO               	| R$ 896.43 	| ... 	|
    | WALMOR LTDA                	|           	|    	|
    | ...                         	| ...       	| ... 	|

> Repare que no exemplo acima, o campo **Valor** está alinhado com a primeira linha do campo **Descricao**. Casos onde o conteúdo das células estão alinhados verticalmente, veja o ***Exemplo 2***.

#### Exemplo 2:

* *PDF Original*

    | Descricao                   	| Valor         	| ... 	|
    |-----------------------------	|---------------	|-----	|
    | SUPERMERCADO<br>WALMOR LTDA 	| R$ 896.43     	| ... 	|
    | ...                         	| ...           	| ... 	|

* *CSV Convertido*

    | Descricao                   	| Valor     	| ... 	|
    |-----------------------------	|-----------	|-----	|
    | SUPERMERCADO                	|           	|    	|
    |                           	| R$ 896.43 	| ... 	|
    | WALMOR LTDA                	|           	|    	|
    | ...                         	| ...       	| ... 	|

> Neste exemplo podemos ver que o campo **Valor** não está alinhado com nenhuma das linhas da **Descrição**. Logo, ele gerará uma nova linha para adicionar o valor desse campo. Nestes casos, talvez o ideal seja utilizar a **Estratégia de Conversão 2** (LTTextBoxHorizontal Quebras como Célula Única).

--- 

### 2. LTTextBoxHorizontal (Quebras como Célula Única)

### 3. LTTextBoxHorizontal (Quebras como Múltiplas Células/Colunas)
