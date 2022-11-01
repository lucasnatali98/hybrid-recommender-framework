# task-executor

# Descrição do projeto

O task-executor é um servidor HTTP em python que vai receber um
conjunto de requisições para executar processos

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