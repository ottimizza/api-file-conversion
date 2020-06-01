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

Estratégia de conversão onde são considerados Caixas de Texto. Cada caixa de texto pode conter mais de uma linha. Vamos utilizar o mesmo exemplo acima.

#### Exemplo 1:

* *PDF Original*

    | Descricao                   	| Valor         	| ... 	|
    |-----------------------------	|---------------	|-----	|
    | SUPERMERCADO<br>WALMOR LTDA 	| R$ 896.43<br><br>	| ... 	|
    | ...                         	| ...           	| ... 	|

* *CSV Convertido*

    | Descricao                   	| Valor     	| ... 	|
    |-----------------------------	|-----------	|-----	|
    | SUPERMERCADO WALMOR LTDA   	| R$ 896.43 	| ... 	|
    | ...                         	| ...       	| ... 	|

> Parece ser a conversão perfeita! Mas estamos lindando com PDF aqui. Devido as diversas formas que um PDF pode ser gerado, muitas vezes nem tudo é o que parece, veja o exemplo abaixo.


* *PDF Original*

    | Portador 	| Descricao                       	| Valor     	| Juros    	| ... 	|
    |----------	|---------------------------------	|-----------	|----------	|-----	|
    | BB       	| PARC EMPRESTIMO <br>REF 10/2019 	| R$ 896.43 	| R$ 23.45 	| ... 	|
    |          	| ...                             	| ...       	|          	| ... 	|


* *CSV Convertido*

    | Portador                           	| Descricao    	| Valor Juros         	|        	| ... 	|
    |-----------------------------------	|-------------	|-------------------	|----------	|-----	|
    | BB PARC EMPRESTIMO <br>REF 10/2019	|            	| R$ 896.43 R$ 23.45	|        	| ... 	|
    |                                   	| ...         	| ...                	|          	| ... 	|

> Podemos observar que o que pareciam ser duas colunas na verdade era só uma! 

---

### 3. LTTextBoxHorizontal (Quebras como Múltiplas Células/Colunas)

