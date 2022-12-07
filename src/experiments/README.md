# O módulo de experimentos

Esse módulo é responsável por gerenciar toda a parte de experimentos
do framework, isso envolve utilizar dos recursos internos da aplicação
mas também conseguir lidar com projetos externos como o
Xperimentor.

Como o Xperimentor trabalha de forma distribuida em um cluster
Kubernetes, uma das etapas que o módulo de experimentos terá que 
passar é pelo processo de deploy das aplicações do projeto.


Precisamos instanciar o Task Executor e também o Xperimentor,
esse processo será feito através de arquivos shell e também de scripts Python
que vão automatizar esse processo de deploy.

Espera-se que possamos a partir daqui salvar os resultados dos experimentos realizados


