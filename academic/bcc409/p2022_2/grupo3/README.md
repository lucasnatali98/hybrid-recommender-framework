# Documentação do Grupo 3

# Introdução

Com o grande fluxo de informações na web, os sistemas de recomendação ganharam grande importancia, na medida que auxiliam os usuários a encontrar o conteudo mais relevante para eles.
Entretanto, nem sempre os sistemas de recomendação tratam todos os usuários de maneira igualitaria, o que acaba resultando em recomendações injustas.
Neste trabalho, exploramos a justiça no lado dos itens na recomendação, verificando se o algoritmo KNN apresenta imparcialidade nas recomendações.


## Justificativa

É fato que a popularidade dos sistemas de recomendação cresceu muito com o aumento de usuários na internet. Portanto garantir que esses sistemas não reforcem os preconceitos já existentes na sociedade é muito importante.
Com base nisso, propomos um estudo em cima do conceito de justiça nas recomendações, com o objetivo de obter informações relevantes para 
auxiliar na obtenção de recomendações mais igualitarias. 
## Objetivos

A proposta deste estudo é verificar se existe ponderação adequada ao recomendar um determinado artista à um usuário em um sistema de recomendações. O objetivo é verificar se existe justiça entre a recomendação de gêneros classificados como feminino, masculino ou não-binário.



## Conjunto de dados

Nome: LastFM - Dataset

Link para download: [https://files.grouplens.org/datasets/hetrec2011/hetrec2011-lastfm-2k.zip](https://files.grouplens.org/datasets/hetrec2011/hetrec2011-lastfm-2k.zip)

O conjunto de dados é formado por uma amostragem 37.711 itens. Esse conjunto é oriundo de um montante de 92.835 registros.

A tabela user_artist.dat contém registros compostos por usuário (userID), artista (artistID), contador de quantas vezes cada usuário ouviu o artista (wheight).

Essa tabela foi relacionada com outra cujo o nome é artist.dat referente ao mesmo dataset. Formada por identificação do registro(id), nome do artista (name), página do artista (url) e identificação para a imagem do artista (pictureURL).

<!-- TODO: Quantidade dos generos -->

Nesse conjunto, a quanitdade de artistas identificados como feminino eram: 999999999

Masculinos: 999999999

não-binário: 0000009999

female           14036
male             12483
mostly_female     8861
mostly_male       1414
andy               917


## Pré-processamento

O pré-processamento teve como base, presumir o gênero dos artistas, independente da autoclassificação pessoal deles, classificando somente pelo nome escrito. Para essa classificação, utilizamos uma biblioteca chamada **gender_guesser**. Essa biblioteca retorna diferentes classes de gênero: andy(não-binário), feminino(female), majoritariamente feminino(mostly_female), majoritariamente masculino(mostly_male), masculino(male) e por fim não reconhecidos (unknow). Para alcançar estes resultados aplicamos as seguintes técnicas: retirada dos caracteres especiais; considerar somente os nomes maiores que 2 caracteres; considerar somente o primeiro nome em caso de nomes compostos; desconsiderar os gêneros não-reconhecidos.

Os arquivos originais estão no formato **.dat**, ao finalizar todas as etapas de limpeza de dados tivemos um **.csv** como dataset.

Com esse processamento, os números de 92.835, reduziram para a amostragem de 37.711 registros.

## Framework

Após o pré-processamento, carregamos os dados para o hybrid_recomender_framework do Lucas Natalli.
Neste framework foi aplicada a normalização do peso (ratings), que significa quantas vezes cada usuário ouviu o artista, em uma escala de [0-1].

Com isso, foi aplicado o algoritmo de recomendação chamado **LenskitItemKNN**. LenskitItemKNN é um algoritmo de recomendação de filtragem colaborativa baseado em itens e ratings. Conssiste na implementação do algoritmo de vizinhos mais próximos (k-nearest neighbors) em que os itens são usados como base para gerar recomendações. O algoritmo utiliza a similaridade entre os itens para recomendar novos itens para os usuários.

Após a aplicação do modelo LenskitItemKNN, foi possível gerar a recomendação de 10 itens para cada usuário.



## Conclusão
Com isso, foi possível ter a relação de gênero com as recomendações para os usuários. Conforme os dados, foi possível perceber que ainda que a quantidade de artistas com o gênero identificados como feminino nas recomendações, perdeu volume,
enquanto as recomendações de artistas do genero masculino cresceu, em relação ao conjunto original de artistas.
Dessa maneira concluimos que o algoritmo KNN de filtragem colaborativa não tem sucesso em equilibrar o resultados das recomendações
privilegiando certos grupos em detrimento de outros.



Dados originais
| Gender          | Count |
|-----------------|-------|
| female          | 14036 |
| male            | 12483 |
| mostly_female   | 8861  |
| mostly_male     | 1414  |
| andy            | 917   |


Recomendaçòes:
| Gender          | Count |
|-----------------|-------|
| female          | 2560  |
| male            | 2885  |
| mostly_female   | 1467  |
| mostly_male     | 314   |
| andy            | 268   |


# Referências Bibliográficas

Cite aqui as referências usadas ao longo do trabalho.

