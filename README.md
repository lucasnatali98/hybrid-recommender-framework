# Hybrid recommender framework

<!---Esses são exemplos. Veja https://shields.io para outras pessoas ou para personalizar este conjunto de escudos. Você pode querer incluir dependências, status do projeto e informações de licença aqui--->

![GitHub repo size](https://img.shields.io/github/repo-size/iuricode/README-template?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/iuricode/README-template?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/iuricode/README-template?style=for-the-badge)
![Bitbucket open issues](https://img.shields.io/bitbucket/issues/iuricode/README-template?style=for-the-badge)
![Bitbucket open pull requests](https://img.shields.io/bitbucket/pr-raw/iuricode/README-template?style=for-the-badge)

> Esse framework visa fornecer uma estrutura genérica e extensível para trabalhar com recomendação híbrida envolvendo meta-features

### Arquitetura do projeto

O projeto está dividido em três principais módulos: Pré-processamento, modelagem e treinamento e por fim avaliação e visualização dos resultados

Em cada um deles faremos um conjunto de processos que alimentará o próximo módulo. Abaixo segue uma imagem que define os módulos desse projeto em uma visão mais macro.

![alt text](https://raw.githubusercontent.com/lucasnatali98/hybrid-recommender-framework/dev/docs/imgs/arquiteturaFramework_ptbr.png?token=GHSAT0AAAAAABWFNVAT5YV657V7DUJ7SKZ6YYOVJFA)

O módulo de preprocessamento será responsável por todo processo inicial antes de pensarmos em recomendações, então depois de carregar uma base de dados podemos submeter essa base ao calculo das metafeatures e/ou processamento dos scores constituintes, após feita estas etapas o resultado é submetido ao processamento dos recursos gerados para ao final desse processo gerar como artefato um conjunto de recursos.

Ṕosteriormente, com os recursos gerados partiremos para parte da modelagem e treinamento dos modelos para obtermos ao final um conjunto de itens recomendados.

Esses itens recomendados serão usados na última fase do framework que envolve a avaliação e visualização dos resultados gerados pelas outras etapas do framework. Aqui podemos aplicar diferentes métricas para avaliar os resultados e deles criar visualizações utilizando diferentes bibliotecas de visualização.


### Dependências importantes do projeto

Esse framework faz uso de outros trabalhos e, com isso, é importante que tenhamos conhecimento sobre o objetivo deste trabalho e também como podemos utiliza-lo. Os dois principais projetos que iremos usar são o Xperimentor e o MetricsCalculator 2.0

#### Xperimentor
Esse trabalho faz a gestão de experimentos computacionais em um ambiente em pararelo utilizando de um cluster Kubernetes, o projeto é estruturado através de um frontend que é responsável por contruir e gerenciar a execução de um experimento e o backend (Task Executor) é um servidor HTTP desenvolvido em Python para tratar as requisições para executar os processos. 

<b>Task Executor</b>: Esta aplicação deve ser conteinerizada e implantada em um cluster Kubernetes onde cada máquina do cluster possui uma réplica do Task Executor que será executado como um serviço. Toda tarefa de um experimento que estiver sendo executada no Xperimentor será direcionada para a aplicação do Task Executor que iniciará um processo e registrará todo fluxo produzidos nos canais de saída padrão.

<b>Xperimentor</b>: está é a aplicação principal do framework e tem como responsabilidade construir e gerenciar a execução de um experimento. O projeto conta com uma única página com um editor de código embutido e um painel de visualização onde o experimentador pode observar o status do experimento. Toda a configuração deve ser feita através de um documento YAML, nele estarão contidos todos os dados necessarios para que o framework seja capaz de executar o seu proposito.

Nesse arquivo de configuração são definidas tarefas que possuem identificadores, comandos e suas dependência. Um exemplo de uma dessas tarefas seria:

tasks:
  id: <task_id>
  command: "gcc -c main.c main.o"
  deps: [dep1,dep2]


Definidas todas as tarefas neste arquivo de configuração o próximo passo é fazer a configuração e execução do cluster Kubernetes, para isso podemos utilizar o Kubernetes tanto localmente quanto em um servidor.

## Princípios de funcionamento do framework
Toda a execução do framework parte de um único ponto, um arquivo de configuração JSON que contêm todas as informações necessarias para a criação das classes que estarão envolvidas no processo da experimentação, em termos práticos cada experimento será definido por um conjunto de objetos que descrevem classes e seus parâmetros de forma que poderemos instanciar base de dados, diferentes preprocessamentos, modelos e avaliadores.

A partir das instâncias geradas do arquivo de configração, podemos preencher containers que vão armazenar todas as instâncias... Ou seja, para uma base de dados X podemos ter um container de preprocessamentos que vão realizar normalização, splitting e encoding, por exemplo.





## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:
<!---Estes são apenas requisitos de exemplo. Adicionar, duplicar ou remover conforme necessário--->
* Python 3
* Numpy
* Pandas
* Scikit-Learn
* Plotly
* Matplotlib
* LensKit


## 🚀 Instalando o Hybrid Recommender Framework

Para instalar o hybrid recommender framework, siga estas etapas:

Linux e macOS:
```
<comando_de_instalação>
```

Windows:
```
<comando_de_instalação>
```

## ☕ Usando o Hybrid Recommender Framework

Para usar hybrid recommender framework, siga estas etapas:

```
<exemplo_de_uso>
```

Adicione comandos de execução e exemplos que você acha que os usuários acharão úteis. Fornece uma referência de opções para pontos de bônus!

## 📫 Contribuindo para o Hybrid Recommender Framework
<!---Se o seu README for longo ou se você tiver algum processo ou etapas específicas que deseja que os contribuidores sigam, considere a criação de um arquivo CONTRIBUTING.md separado--->
Para contribuir com o hybrid recommender framework, siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch: `git checkout -b <nome_branch>`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`
4. Envie para o branch original: `git push origin <nome_do_projeto> / <local>`
5. Crie a solicitação de pull.

Como alternativa, consulte a documentação do GitHub em [como criar uma solicitação pull](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## 🤝 Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://avatars3.githubusercontent.com/u/31936044" width="100px;" alt="Foto do Iuri Silva no GitHub"/><br>
        <sub>
          <b>Lucas Natali</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://s2.glbimg.com/FUcw2usZfSTL6yCCGj3L3v3SpJ8=/smart/e.glbimg.com/og/ed/f/original/2019/04/25/zuckerberg_podcast.jpg" width="100px;" alt="Foto do Mark Zuckerberg"/><br>
        <sub>
          <b>Reinaldo Silva Fortes</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://miro.medium.com/max/360/0*1SkS3mSorArvY9kS.jpg" width="100px;" alt="Foto do Steve Jobs"/><br>
        <sub>
          <b>Steve Jobs</b>
        </sub>
      </a>
    </td>
  </tr>
</table>


## 😄 Seja um dos contribuidores<br>

Quer fazer parte desse projeto? Clique [AQUI](CONTRIBUTING.md) e leia como contribuir.

## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE.md) para mais detalhes.

[⬆ Voltar ao topo](#hybrid recommender framework)<br>
