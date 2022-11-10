# Xperimentor

A general purpose framework to manage distributed computational experiments

Esse trabalho faz a gestão de experimentos computacionais em um ambiente em pararelo utilizando de um cluster Kubernetes, o projeto é estruturado através de um frontend que é responsável por contruir e gerenciar a execução de um experimento e o backend (Task Executor) é um servidor HTTP desenvolvido em Python para tratar as requisições para executar os processos. 

<b>Xperimentor</b>: está é a aplicação principal do framework e tem como responsabilidade construir e gerenciar a execução de um experimento. O projeto conta com uma única página com um editor de código embutido e um painel de visualização onde o experimentador pode observar o status do experimento. Toda a configuração deve ser feita através de um documento YAML, nele estarão contidos todos os dados necessarios para que o framework seja capaz de executar o seu proposito.

Nesse arquivo de configuração são definidas tarefas que possuem identificadores, comandos e suas dependência. Um exemplo de uma dessas tarefas seria:
```
tasks:
  - id: MetaFeatureCalculator
    command: "java -jar MetricCalculator.jar {DB} {Fold} {MF} 60 0"

  - id: PredictionCF
    command: "python -u PredictionCF.py {DB} {Alg} {Fold} 60 0"

  - id: PredictionWHF
    command: "python -u PredictionWHF.py {DB} {HF} {Fold} 60 0"
    deps: [MetaFeatureCalculator, PredictionCF]

  - id: EvaluatorCF
    command: "java -jar MetricCalculator.jar {DB} {Fold} {Eval} CF 60 0"
    deps: [PredictionCF]

  - id: EvaluatorWHF
    command: "java -jar MetricCalculator.jar {DB} {Fold} {Eval} WHF 60 0"
    deps: [PredictionWHF]

  - id: CalculateStatistics
    command: "java -jar MetricCalculator.jar {DB} ALL {Eval} {Stats} 60 0"
    deps: [EvaluatorCF, EvaluatorWHF]

recipeDefaults:
  DB: ["Bookcrossing"]
  Fold: ["F1234-5", "F1235-4", "F1245-3", "F1345-2", "F2345-1"]
  MF: ["PCR", "PR", "GINI", "PEARSON", "PQMEAN", "SD"]
  Alg: ["Sigmoid", "Biased", "MF", "Uknn", "SVD", "Latent", "Factor", "BiPolar", "SO"]
  HF: ["STREAM", "FWLS", "HR"]
  Eval: ["RMSE", "F1", "EPC", "EILD"]
  Stats: ["mean", "IC"]

recipes:
 - id: ExBC
   pruning: [Fold, Eval]
   uses:
      DB:    ["Bookcrossing"]
      Fold:  ["F1234-5", "F1235-4", "F1245-3", "F1345-2", "F2345-1"]
      MF:    ["PCR", "PR", "GINI", "PEARSON", "PQMEAN", "SD"]
      Alg:   ["Sigmoid", "Biased", "MF", "Uknn", "SVD", "Latent", "Factor", "BiPolar", "SO"]
      HF:    ["STREAM", "FWLS", "HR"]
      Eval:  ["RMSE", "F1", "EPC", "EILD"]
      Stats: ["mean", "IC"]
```

Definidas todas as tarefas neste arquivo de configuração o próximo passo é fazer a configuração e execução do cluster Kubernetes, para isso podemos utilizar o Kubernetes tanto localmente quanto em um servidor.

Toda tarefa possui um estado que varia durante a execução do experimento. Existem 8 estados ao total, sendo eles:
- Waiting: estado inicial de toda tarefa
- running: sinaliza uma tarefa em execução
- successfully_finished: sinaliza uma tarefa que finalizou de forma bem sucedida
- finished_with_erros: sinaliza que uma tarefa finalizou com o fluxo de erro padrão não vazio
- finished_with_non_zero: sinaliza que uma tarefa finalizou com código diferente de zero
- finished_with_errors_non_zero: sinaliza que uma tarefa finalizou com o fluxo de erro padrão não vazio e com código diferente de zero
- failed: sinaliza que uma tarefa não pode ser executada
- forced_successfully_finished: sinaliza que uma tarefa foi marcada como bem sucedida


# Xperimentor src/
## Command.ts
Essa é uma classe que abstrai um comando de terminal (linha de comando)

Cada tarefa (Task) gerada por um processo (Process) e um Recipe deveria conter um comando
Esse comando será executado pelo TaskExecutor em tempo de execução

Pelo design, um commando é uma string que possivelmente contém parâmetros declarados entre {}

Por exemplo:

<code>python my-script.py {arg1} -p {arg2} -q</code>

## Process.ts
Essa classe é uma espécie de modelo para gerar comandos que podem ser executados em um terminal de linha de comando.

Alguns processos podem depender de outros processos, essas dependências são propagadas para Tasks tasks gerado por aqueles processos dependentes

## Tasks.ts
Tarefas podem ser vistas como instancias de Processos (Process.ts)

Essas tarefas são a essencia do Xperimentor, esses framework foi inicialmente desenvolvimento para gerenciar essas tarefas

## TaskBuilder.ts

Essa classe é responsável por gerar todas as tarefas (Tasks) usadas pelo framework


## Recipe.ts
São usados para gerar tarefas (Tasks)

Recipes são usadas para gerar um produto cartesiano de ArgumentTypes. Esse produto cartesiano será usada para gerar diferentes tarefas (Tasks) de um processo (Process)

Por exemplo:

Se um processo P tem 3 argumentos, como:

<code>process.sh {A} {B} {C}</code>

E esse processo tem o seguinte recipe:

- A: [A1,A2]
- B: [B1]
- C: [C1,C2]
- Z: [Z1,Z2,Z3] -> será ignorado quando P não tiver argumentos Z


O seguinte produto cartesiano será gerado:


    [A1, B1, C1]
    [A1, B1, C2]
    [A2, B1, C1]
    [A2, B1, C2]


E vai gerar os seguintes comandos de terminal:

process.sh A1 B1 C1 

process.sh A1 B1 C2

process.sh A2 B1 C1

process.sh A2 B1 C2


## Experiment.ts
Essa é a classe principal do projeto, ela é responsável por construir e gerenciar o ciclo de vida de um experimento.

## Run tests
`npm run tests` or `npm t`