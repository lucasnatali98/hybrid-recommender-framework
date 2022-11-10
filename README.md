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

![alt text](docs/imgs/arquiteturaFramework_ptbr.png?raw=true)

O módulo de preprocessamento será responsável por todo processo inicial antes de pensarmos em recomendações, então depois de carregar uma base de dados podemos submeter essa base ao calculo das metafeatures e/ou processamento dos scores constituintes, após feita estas etapas o resultado é submetido ao processamento dos recursos gerados para ao final desse processo gerar como artefato um conjunto de recursos.

Ṕosteriormente, com os recursos gerados partiremos para parte da modelagem e treinamento dos modelos para obtermos ao final um conjunto de itens recomendados.

Esses itens recomendados serão usados na última fase do framework que envolve a avaliação e visualização dos resultados gerados pelas outras etapas do framework. Aqui podemos aplicar diferentes métricas para avaliar os resultados e deles criar visualizações utilizando diferentes bibliotecas de visualização.


### Dependências importantes do projeto

Esse framework faz uso de outros trabalhos com isso é importante que tenhamos
conhecimento sobre o objetivo desses trabalhos e também como podemos utilizá-los. Os dois principais projetos
que iremos usar são o Xperimentor e o MetricsCalculator 2.0. Abaixo
estão as documentações para os projetos e através delas teremos
um maior entendimento sobre cada um


[Xperimentor](external/xperimentor/README.md)

[Task-Executor](external/task-executor/README.md)


## Princípios de funcionamento do framework
Toda a execução do framework parte de um único ponto, um arquivo de configuração JSON que contêm todas as informações necessarias para a criação das classes que estarão envolvidas no processo da experimentação, em termos práticos cada experimento será definido por um conjunto de objetos que descrevem classes e seus parâmetros de forma que poderemos instanciar base de dados, diferentes preprocessamentos, modelos e avaliadores.

A partir das instâncias geradas do arquivo de configração, podemos preencher containers que vão armazenar todas as instâncias... Ou seja, para uma base de dados X podemos ter um container de preprocessamentos que vão realizar normalização, splitting e encoding, por exemplo.


## Os módulos do framework:
- Módulo de pré-processamento:
- Módulo de meta-features:
- Módulo de métricas:
- Módulo de recomendadores:
- Módulo de resultados:
- Módulo de visualização:
- Módulo de recomendação hibrida
- Módulo de dados
- Módulo dos experimentos


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

Primeiro faça o clone do projeto para sua máquina
```
git clone https://github.com/lucasnatali98/hybrid-recommender-framework.git
```
Em sequência você irá precisar criar um ambiente para o projeto e suas depedências, e para isso você pode utilizar de diversas ferramentas. Nesse caso, vou utilizar o Virtualenv

```
virtualenv venv
```

Com o ambiente devidamente criado, vamos ativá-lo:

```
source venv/bin/activate
```

Com o ambiente ativado, podemos fazer a instalação das dependências
do projeto utilizando pip
```
pip install -r requirements.txt
```

Isso deve ser suficiente para baixar todas as dependências e a
partir dai já estaremos prontos para utilizar o projeto

## ☕ Usando o Hybrid Recommender Framework

Para usar hybrid recommender framework, o intuito é que você
prepare todo o arquivo de configuração, definindo os experimentos
com seus respectivos algoritmos, preprocessamentos, dentre outras
operações. Com esse arquivo configurado, basta que seja executado:

```
python main.py
```

## 📫 Contribuindo para o Hybrid Recommender Framework
<!---Se o seu README for longo ou se você tiver algum processo ou etapas específicas que deseja que os contribuidores sigam, considere a criação de um arquivo CONTRIBUTING.md separado--->
Para contribuir com o hybrid recommender framework, siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch: `git checkout -b <nome_branch>`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`
4. Envie para o branch original: `git push origin <nome_do_projeto> / <local>`
5. Crie a solicitação de pull.

Como alternativa, consulte a documentação do GitHub em [como criar uma solicitação pull](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## 🤝 Autores

<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://media-exp1.licdn.com/dms/image/C4E03AQHcrrceSpVcDw/profile-displayphoto-shrink_800_800/0/1579646560279?e=1673481600&v=beta&t=ZNYdW2-J5gF_d2VcVgVbJMaiMxdk0klwyLr7JvoJPSM" width="100px;" alt="Foto do Lucas"/><br>
        <sub>
          <b>Lucas Natali</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://media-exp1.licdn.com/dms/image/C4D03AQEKsc-CUUX56A/profile-displayphoto-shrink_800_800/0/1516837380603?e=1673481600&v=beta&t=FkNii-p4tkKDfN16HTrdE4k1ChaDmAeB3-Tusg-fsE8" width="100px;" alt="Foto do Reinaldo"/><br>
        <sub>
          <b>Reinaldo Silva Fortes</b>
        </sub>
      </a>
    </td>
    
  </tr>
</table>


## Seja um dos contribuidores<br>

Quer fazer parte desse projeto? Entre em contato com:

- lucas.natali@aluno.ufop.edu.br
- rei.fortes@ufop.edu.br
