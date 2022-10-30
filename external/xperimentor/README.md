# Xperimentor

A general purpose framework to manage distributed computational experiments

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