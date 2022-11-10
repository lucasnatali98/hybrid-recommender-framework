# task-executor

# Descrição do projeto

O task-executor é um servidor HTTP em python que vai receber um
conjunto de requisições para executar processos

<b>Task Executor</b>: Esta aplicação deve ser conteinerizada e implantada em um cluster Kubernetes onde cada máquina do cluster possui uma réplica do Task Executor que será executado como um serviço. Toda tarefa de um experimento que estiver sendo executada no Xperimentor será direcionada para a aplicação do Task Executor que iniciará um processo e registrará todo fluxo produzidos nos canais de saída padrão.

## Endpoints:

### Status do servidor
Método: GET
URL: /check

response:
```
Server is running
```

### Execução
Método: POST

URL: /run

response:
```
{
 "requestedJSON": task_info,
 "return_code": process.poll(),
 "stdout": async_stdout_call.get(),
 "stderr": async_stderr_call.get()
}
```



# Como executar o projeto
sudo apt-get install python3-venv

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

python3 web_service.py 