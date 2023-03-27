# Documentação do Grupo 4


# Introdução

Nos últimos anos, os sistemas de recomendação vêm ganhando cada vez mais importância no mundo da tecnologia. Empresas como a Netflix e o Spotify utilizam esses sistemas para oferecer conteúdos personalizados aos seus usuários, com base em suas preferências e histórico de uso. E é nesse contexto que surge o Spotify Blend, uma ferramenta cujo objetivo é criar playlists colaborativas entre dois usuários, combinando seus gostos musicais em uma única lista de reprodução. Para que o Blend possa oferecer uma experiência satisfatória aos usuários, é preciso que o algoritmo por trás dele consiga analisar e combinar as preferências musicais de cada indivíduo de forma inteligente e eficiente. 

Uma das principais abordagens utilizadas para melhorar o desempenho de sistemas de recomendação é a filtragem colaborativa, que consiste em analisar os padrões de comportamento dos usuários e identificar padrões de similaridade entre eles. No caso do Spotify Blend, essa abordagem pode ser utilizada para comparar os gostos musicais de dois usuários e gerar uma lista de reprodução que seja agradável e equilibrada para ambos. Isso é importante porque, apesar de ser uma ferramenta criativa e divertida, o Blend pode se tornar frustrante para os usuários se a lista de reprodução gerada não refletir suas preferências musicais ou se houver um desequilíbrio entre as contribuições de cada um. Ao melhorar o algoritmo de recomendação do Blend por meio de técnicas de filtragem colaborativa, é possível garantir que a experiência dos usuários seja a mais satisfatória possível, incentivando o engajamento com a plataforma e a fidelização dos usuários.

Neste texto, exploraremos como os sistemas de recomendação funcionam no Spotify Blend e também discutiremos o que foi apresentado no artigo \textit{Whisk: A Music Recommender System for Two Users using Item-to-Item Collaborative Filtering with Implicit Binary Positive-only Feedback}
## Justificativa

Apesar de uma ferramenta muito útil, ainda existe ponto de melhora quanto a essas recomendações. Quando dois usuários com gostos musicais muito diferentes utilizam o Spotify Blend para gerar uma playlist, pode haver dificuldades em encontrar um equilíbrio entre as preferências musicais de ambos, resultando em uma playlist que não seja agradável para ambos ou que não contenha novidades musicais para ambos.


## Objetivos

O objetivo da recomendação por filtragem colaborativa item-item para o Spotify Blend é melhorar a precisão e a qualidade das recomendações geradas pelo sistema. Essa técnica utiliza o histórico de uso dos usuários para identificar padrões de comportamento e preferências musicais, gerando sugestões personalizadas que sejam atraentes e relevantes para cada usuário. Ao utilizar a filtragem colaborativa item-item, o Spotify Blend consegue identificar não apenas as preferências musicais de cada usuário, mas também a similaridade entre as músicas que eles ouviram. Com base nessa similaridade, o sistema pode gerar recomendações personalizadas que sejam mais precisas e relevantes para cada usuário, aumentando assim a satisfação e o engajamento dos usuários com a plataforma. Além disso, a recomendação por filtragem colaborativa item-item também ajuda a diversificar as recomendações geradas pelo sistema, sugerindo músicas e artistas que os usuários ainda não conhecem, mas que sejam similares às suas preferências musicais. Em resumo, o objetivo da recomendação por filtragem colaborativa item-item para o Spotify Blend é melhorar a qualidade e a eficácia das recomendações, aumentando a satisfação e o engajamento dos usuários com a plataforma.


# Revisão Bibliográfica

## Fundamentação teórica
### Spotify Blend
O Spotify é uma plataforma de streaming de música, podcast e vídeo fundada em 2006 na Suécia. Com mais de 356 milhões de usuários ativos em mais de 178 países, o Spotify é um dos principais serviços de streaming de música do mundo.

O Spotify Blend é uma ferramenta introduzida em 2020, que permite aos usuários criar uma playlist personalizada para duas pessoas com base em seus gostos musicais. Ao usar o Spotify Blend, os usuários podem criar uma playlist colaborativa com amigos, familiares ou parceiros, combinando suas músicas favoritas em uma única lista de reprodução. O sistema utiliza algoritmos de aprendizado de máquina para identificar as preferências musicais de ambos os usuários, criando uma lista de reprodução personalizada para eles. Com o Blend, os usuários podem descobrir novas músicas e artistas, e compartilhar suas músicas favoritas com seus amigos e familiares.

### Sistema de recomendação

Um sistema de recomendações é um conjunto de algoritmos que tem como objetivo sugerir itens (produtos, serviços, conteúdos, entre outros) para os usuários com base em suas preferências e histórico de uso. Esses algoritmos utilizam técnicas de análise de dados e inteligência artificial para identificar padrões de comportamento e criar perfis personalizados de cada usuário. Com base nesses perfis, o sistema é capaz de recomendar itens que sejam relevantes e atraentes para cada usuário, aumentando a satisfação e o engajamento dos usuários com a plataforma. Alguns exemplos de sistemas de recomendação são os algoritmos de sugestão de produtos da Amazon, os algoritmos de recomendação de filmes e séries da Netflix e, é claro, o Spotify Blend, que utiliza sistemas de recomendação para criar listas de reprodução personalizadas a partir dos gostos musicais dos usuários. Em resumo, os sistemas de recomendação são ferramentas poderosas para melhorar a experiência do usuário e aumentar a eficiência das plataformas em oferecer conteúdos relevantes e atraentes.

### Filtragem colaborativo

A filtragem colaborativa é uma técnica de análise de dados utilizada em sistemas de recomendação que consiste em identificar padrões de similaridade entre os usuários e utilizar esses padrões para gerar recomendações personalizadas. Essa técnica se baseia na premissa de que usuários que têm gostos e comportamentos similares em relação a determinados itens também tendem a ter opiniões similares em relação a outros itens que ainda não experimentaram. Por exemplo, se dois usuários têm um histórico de ouvir artistas e gêneros musicais semelhantes no Spotify, é provável que eles também gostem de outras músicas e artistas que o outro usuário ainda não ouviu. 

Com base nessa premissa, o algoritmo de filtragem colaborativa analisa o histórico de uso de cada usuário e identifica padrões de comportamento e preferências musicais, gerando assim sugestões personalizadas que sejam atraentes e relevantes para cada usuário. A filtragem colaborativa é uma das técnicas mais eficazes para melhorar a precisão e a qualidade das recomendações em sistemas de recomendação, e é amplamente utilizada em plataformas como o Spotify Blend, que utilizam a colaboração entre usuários para gerar sugestões personalizadas.

# Desenvolvimento

Foi decidido adotar uma abordagem para analisar a proposta dos autores e identificar possíveis melhorias a serem implementadas. A intenção é avaliar cuidadosamente o que foi proposto pelos autores, visando identificar pontos fortes e fracos do sistema de recomendação do Spotify Blend e, com base nessa análise, propor melhorias que possam aprimorar a experiência do usuário. A abordagem escolhida tem como foco não só a identificação de problemas, mas também a sugestão de soluções que possam aumentar a precisão e a personalização das recomendações geradas pelo sistema.

Até o momento, estamos enfrentando um desafio em relação à replicação do pseudo código exemplificado no artigo e na leitura da base de dados. Essa análise será realizada a partir desse pseudo código, mas estamos enfrentando algumas dificuldades técnicas em sua implementação. Além disso, a leitura da base de dados também tem se mostrado um obstáculo, exigindo uma abordagem cuidadosa e atenção aos detalhes para garantir a precisão da análise.

# Resultados

--

# Conclusões

--

# Referências Bibliográficas

Andrade, R., van Keulen, J., Snoep, M., Thai, D., & Wolters, R. (2022). Whisk: A music re-
commender system for two users using item-to-item collaborative filtering with implicit binary
positive-only feedback. Artech Journal of Effective Research in Engineering and Technology.
5
