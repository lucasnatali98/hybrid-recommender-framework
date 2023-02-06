# MetricsCalculator

O projeto do MetricsCalculator será responsável pelo cálculo
das metafeatures relacionadas tanto a filtragem colaborativa
quanto a baseada em conteúdo. Esse é um projeto em java que utiliza de um arquivo de configuração
em XML para definir informações importantes para o cálculo dessas metafeatures. Um exemplo desse arquivo pode ser encontrado em: [Arquivo de configuração](external/MetricsCalculator/config_exemplo.xml)

Nesse arquivo tem explicado o que cada chave desse XML significa e como pode ser usada
para tentar tornar ainda mais simples, no texto é definida a seguinte tabela
para relacionar cada informação:

![alt text](https://github.com/lucasnatali98/hybrid-recommender-framework/blob/c2060c874cb8e7cc4bba63a92e1c5f0d8004a327/docs/imgs/recmetrics_xml_file_inputs.png)

A partir de um arquivo de texto contendo todas as avaliações de usuários e itens, é
criada uma matriz de avaliações item-usuário utilizando da estrutura DataModel do framework
Apache Mahout. Inicialmente é criado um vetor de preferências do arquivo texto lido, esse vetor
é processado por um número arbitrário de threads que irão utilizar dos dados para calcular os
resultados. Por fim, um objeto de saída é acessado concorrentemente pelas threads para escrever
os resultados em um arquivo texto em disco.


O framework RecMetrics possui limitações como, por exemplo, trabalhar apenas com
dados de filtragem colaborativa, utiliza cerca de vinte argumentos de configuração do usuário
incluindo as meta-features e arquivos de entrada e saída que serão utilizados. A inclusão de todos
esses elementos aliado à necessidade de intervenção no código para algumas alterações torna-o
complicado de utilizar.

## Execução do projeto
Esse projeto pode ser utilizado através da linha de comando e recebe alguns parâmetros
como a base de dados, os folds, caminho para leitura do arquivo de configuração e o caminho
que desejamos salvar o resultado da execução, além de outros possíveis argumentos. Um exemplo seria:

```
java -jar MetricCalculator.jar <arg1> <arg2> <arg3> <arg4> <arg5>    
```

Dentre esses parâmetros temos a possibilidade de informar coisas como:
número de cores para o processamento, caminho base para a base de dados,
o caminho para os dados, o caminho para o arquivo recurso, qual a pasta vai armazenar a saída
o nome da classe da métrica, tamanho do buffer

Seu funcionamento básico pode ser obtido apenas informando o arquivo com a configuração das metafeatures
e um possível local para armazenar os resultados.

## Métricas

### Colaborativas

-   QualitativeMetrics.GiniIndex
-	QualitativeMetrics.PearsonCorrelation
-	QualitativeMetrics.PqMean
-	QualitativeMetrics.StandardDeviation
-	QuantitativeMetrics.LogOfDateRatings
-	QuantitativeMetrics.LogOfQtdRatings
-	QuantitativeMetrics.LogSdevDate >> Logaritimo do Desvio Padrão
-	QuantitativeMetrics.NormalizedProportionOfCommomRatings
-	QuantitativeMetrics.NormalizedProportionOfRatings
-	QuantitativeMetrics.PRDateRatings
-	QuantitativeMetrics.ProportionOfCommomRatings
-	QuantitativeMetrics.ProportionOfRatings
-	QuantitativeMetrics.RatingsMean >> Media dos ratings

### Baseadas em conteúdo
- Cosine
- Dice
- Jaccard
- Entropy
- SimilarRatingsMean >> Media de similaridade dos documentos considerados similares
- SimilarRatingsSD >> Desvio padrao da similaridade dos documentos considerados similares

	