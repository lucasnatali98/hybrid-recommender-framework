# Documentação do Grupo 5

## Membros do grupo
- Daniel
- Danielle 
- Fabrício
- Gabriel
- Guilherme 

# Introdução

Os jogos eletrônicos são uma forma de entretenimento que existem desde os anos 60 e desde então foram evoluindo de maneira cada vez mais imersiva e incorporando mais tecnologias. O termo 'gaming' já é algo presente na vida de várias pessoas presentes na internet e hoje com isso há o crescimento exponencial da quantidade de jogos disponíveis, já que a cada dia novos jogos são lançados por pequenas e grandes produtoras. Essa quantidade imensa de jogos requer que existam formas de recomendar jogos de forma mais personalizada para que estes não fiquem sobrecarregados de escolhas que em sua maioria podem ser irrelevantes. Esse estudo faz uma análise do modelo de recomendação itemKNN com diversos parâmetros diferentes na questão da sua precisão quanto ao recomendar um jogo a um usuário, fazendo um estudo de caso da base de dados Steam Video Games. 

## Justificativa

A principal ideia de um estudo como este é compreender como sistemas de recomendação para a mídia de jogos eletrônicos. Compreender essas ferramentas é importante não só para que se obtenha conhecimento técnico sobre o assunto mas também para entender como nós, os usuários, somos influenciados por essas plataformas.

## Objetivos

Como objetivo geral principal desse estudo temos a testagem de alguns modelos de recomendação de filtragem colaborativa presentes no Framework disponibilizado e fazer uma pequena análise comparativa entre eles para a recomendação para um usuário.

Dentre os objetivos específicos temos:
 - Implementar as chamadas dos modelos presentes no framework e gerar as recomendações.
 - Analisar cada modelo de forma comparativa de acordo com a sua recomendação.

# Revisão Bibliográfica
## Fundamentação teórica

Nesta seção vamos introduzir alguns conceitos básicos que irão auxiliar no entendimento do trabalho realizado.
### Steam
A Steam é uma plataforma online de distribuição de jogos eletrônicos para computadores que foi lançada em 2002 pela Valve, e tinha como intuito inicial facilitar as atualizações para jogos da própria distribuidora. 

### ItemKNN
O algoritmo de recomendação ItemKNN (Item k-Nearest Neighbors) é um método de filtragem colaborativa que utiliza a similaridade entre os itens para fazer recomendações personalizadas. Ele funciona encontrando os k itens mais semelhantes ao item que um usuário gostou e recomenda esses itens ao usuário.

### Pop score
O algoritmo de recomendação Popularity Score (Pontuação de Popularidade) é um método simples de recomendação que classifica os itens com base em sua popularidade entre os usuários. Ele recomenda os itens mais populares (com maior número de interações ou visualizações) aos usuários, independentemente de suas preferências individuais. É um algoritmo fácil de implementar e pode ser usado como uma referência de base para comparar a eficácia de outros algoritmos mais complexos de recomendação.

### BiasedSVD
O algoritmo de recomendação BiasedSVD (Decomposição em Valores Singulares com Viés) é um método de filtragem colaborativa que utiliza uma abordagem de decomposição matricial para encontrar as características latentes dos usuários e itens. Ele considera tanto a avaliação média de um usuário quanto a avaliação média de um item para criar um modelo mais preciso de recomendação.

### UserKNN
O algoritmo de recomendação User KNN (User k-Nearest Neighbors) é um método de filtragem colaborativa que utiliza a similaridade entre os usuários para fazer recomendações personalizadas. Ele funciona encontrando os k usuários mais semelhantes ao usuário que está recebendo a recomendação e recomenda os itens que esses usuários gostaram.

# Desenvolvimento

## Base de dados
A Base de dados utilizada no projeto é a Steam Vieo Games que pode ser encontrada no website Kaggle a partir do seguinte link: https://www.kaggle.com/datasets/tamber/steam-video-games. O arquivo csv referente a essa base é formado por quatro colunas distintas:

- **id**: Identificador do usuário, variável qualitativa identificadora, que representa o identificador de um usuário único.
- **game_name**: Nome do jogo, variável qualitativa nominal que descreve o título do jogo.
- **action**: Ação do usuário, variável qualitativa binária que indica a ação que o usuário fez com aquele jogo, que pode ter dois valores distintos: Purchase que indica a compra do jogo e Play que indica que o usuário jogou aquele jogo.
- **play_time**: Tempo de jogo, variável quantitativa contínua que indica a quantidade de horas jogadas daquele jogo caso sua action seja do tipo "play". Se a action for do tipo "purchase" o padrão desse valor é 1.0.

## Pré-processamento dos dados

Os dados da base SteamVideoGames foram pré-processados préviamente antes de serem enviados para o framework. Alguns dos dados da tabela são irrelevantes para a nossa análise e são descartados enquanto outros são transformados. As alterações feitas nessa etapa são descritas abaixo.

### Remoção de colunas irrelevantes
Inicialmente removemos colunas e linhas que não serão relevantes para a nossa análise. Inicialmente removemos todas as linhas que possuiam a ação "purchase" já que vamos utilizar apenas a análise de tempo de jogo como referência. Após isso a coluna action é tambem removida já que todas as linhas terão o mesmo valor nesse atributo (no caso seria "play").

### Criação de um id unico para o jogo
Os jogos dentro desse dataset são descritos unicamente pelo seu nome. Nomes em string não são muito interessantes para se trabalhar diretamente e funcionam melhor de maneira relacional. Para que tivéssemos um id atrelado a cada jogo utilizamos a função factorize do pandas.

### Transformação de playtime em ratings
O tempo de jogo vai ser o principal argumento utilizado para fazer as recomendações pela filtragem colaborativa. Para que ele siga o padrão adequado foi feito um remapeamento do atributo para valores numéricos de 1 a 5 estrelas em que 5 representa uma ótima avaliação e 1 representa uma avaliação ruim. Esse mapeamento foi feito utilizando o método select da biblioteca numpy e teve como critério os seguintes espaços:
- 0 a 2 horas: 1 estrela
- 2 a 4 horas: 2 estrelas
- 4 a 10 horas: 3 estrelas
- 10 a 20 horas: 4 estrelas
- mais de 20 horas: 5 estrelas

Os valores das horas foram escolhidos de maneira que usuários que jogam o jogo por muito tempo tenham uma avaliação mais alta do jogo. Como poucos jogadores jogam mais de 40 horas o limite de 20 horas para 5 estrelas se mostrou adequado.

### Separação das tabelas
A partir dessas transformações resta fazer com que as base de dados siga a especificação do framework. Para isso dividimos o arquivo em tres novos arquivos que consistem em:

- **Users.csv**: Possui apenas a coluna de id, ou seja apenas uma coluna, que relaciona o usuário.
- **Items.csv**: Possui duas colunas: game_id e game_name que são respectivamente o id e o título do jogo.
- **Ratings.csv**: Possui quatro colunas: user_id, game_id, play_time e rating que relaciona as outras duas tabelas numa tabela de ratings.

## Implementação
Neste estudo vamos basicamente testar alguns dos algoritmos que existem no framework. Foram testados exatos quatro algoritmos que são o ItemKNN, o UserKNN, o Pop Score e o Biased SVD.

# Resultados

Nesta seção vamos apresentar alguns resultados com variados algoritmos de recomendação. Para fazer essa análise fazemos a recomendação para um usuário. O score mais alto indica que aquele item é o mais recomendado para aquele usuário através das similaridades obtidas com outros usuários pelo modelo.

No Item KNN o score médio das recomendações para esse usuário único foi de 6.028. No User KNN essa média se torna 5.962 e no biasedSVD obtem um score médio das recomendações de 5.689.

O popscore possui uma métrica diferente que ficou com uma média de 0.841 o que indica que a recomendação de itens populares para esse usuário foi relativamente eficaz.

# Conclusões

Em resumo, podemos ver que os modelos obtiveram performances parecidas para um usuário. Esse experimento mostra que mesmo com poucas informações sobre os usuários, que no nosso caso são apenas o tempo de jogo, já conseguimos fazer um sistema de recomendação razoável usando os modelos prontos do LensKit.

# Referências Bibliográficas

