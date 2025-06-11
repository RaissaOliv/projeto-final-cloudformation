# Projeto Final CloudFormation - Servidor de Tarefas (gRPC + RabbitMQ + DynamoDB)

Este projeto provisiona uma instância EC2 na AWS que executa um servidor gRPC para gerenciamento de tarefas, integra com RabbitMQ para eventos e utiliza DynamoDB para persistência. O provisionamento é feito via AWS CloudFormation.

---

## Sumário

- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Deploy com CloudFormation](#deploy-com-cloudformation)
- [Acesso à Instância EC2](#acesso-à-instância-ec2)
- [Configuração do Cliente](#configuração-do-cliente)
- [Testando o Sistema](#testando-o-sistema)
- [Gerando arquivos gRPC a partir do .proto](#gerando-arquivos-grpc-a-partir-do-proto)
- [Estrutura dos Arquivos](#estrutura-dos-arquivos)
- [Dicas e Solução de Problemas](#dicas-e-solução-de-problemas)

---

## Arquitetura

- **EC2**: Executa o servidor gRPC (`tarefas_server.py`) e o RabbitMQ.
- **RabbitMQ**: Gerencia eventos de tarefas.
- **DynamoDB**: Persistência das tarefas.
- **CloudFormation**: Provisiona toda a infraestrutura.
- **Cliente Python**: Interage via gRPC e consome eventos do RabbitMQ.

---

## Pré-requisitos

- Conta AWS com permissões para EC2, CloudFormation e DynamoDB.
- AWS CLI configurado.
- Chave SSH para acesso à EC2.
- Python 3.12+ e `pip` na máquina local.

---

## Deploy com CloudFormation

1. **Crie um par de chaves EC2**  
   No console AWS: EC2 > Par de chaves > Criar par de chaves.

2. **Descubra seu IP público**  
   ```sh
   curl ifconfig.me
   ```
   Use este IP para o parâmetro `SSHLocation` (ex: `X.X.X.X/32`).

3. **Crie a stack**  
   No console AWS > CloudFormation > Criar stack > Com novos recursos.  
   Faça upload do arquivo `cloudformation.yaml` e preencha os parâmetros.

4. **Aguarde a criação**  
   Ao final, anote os valores de `PublicIP` e `PublicDNS` nos Outputs.

5. **(Opcional) Crie a tabela DynamoDB**  
   No console AWS > DynamoDB > Criar tabela  
   - Nome: `TarefasTable`
   - Chave primária: `id` (String)

---

## Acesso à Instância EC2

Conecte-se via SSH:
```sh
ssh -i /caminho/para/sua-chave.pem ubuntu@<PublicIP>
```

---

## Configuração do Cliente

1. **Edite o arquivo `tarefas_client.py`**  
   Substitua:
   ```python
   GRPC_SERVER_ADDRESS = '<PublicIP>:50051'
   RABBITMQ_HOST = '<PublicIP>'
   ```
   Use o IP público da EC2.

2. **Instale as dependências localmente**  
   ```sh
   pip install grpcio grpcio-tools pika boto3
   ```

---

## Testando o Sistema

1. **Execute o cliente gRPC**
   ```sh
   python tarefas_client.py
   ```

2. **Consuma eventos do RabbitMQ**  
   Descomente a linha `consume_rabbitmq_messages()` no final do `tarefas_client.py` e execute em outro terminal:
   ```sh
   python tarefas_client.py
   ```

---

## Gerando arquivos gRPC a partir do .proto

Se modificar o arquivo `.proto`, gere novamente os arquivos Python:

```sh
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tarefas.proto
```

Isso criará/atualizará `tarefas_pb2.py` e `tarefas_pb2_grpc.py`.

---

## Estrutura dos Arquivos

```
projeto-final-cloudformation/
├── cloudformation.yaml
├── tarefas_server.py
├── tarefas_client.py
├── tarefas.proto
├── tarefas_pb2.py
├── tarefas_pb2_grpc.py
└── ...
```

---

## Dicas e Solução de Problemas

- **Permissão negada ao usar chave SSH**  
  Use: `chmod 400 sua-chave.pem`
- **Erro de módulo não encontrado**  
  Instale dependências no virtualenv ou localmente.
- **Erro com boto3**  
  Adicione `boto3` nas dependências do pip.
- **Erro com arquivos gRPC**  
  Gere novamente os arquivos `.py` a partir do `.proto`.
- **RabbitMQ não conecta**  
  Verifique se a porta 5672 está aberta no Security Group e se o serviço está rodando.

---

## Créditos

Projeto adaptado para AWS Playground por [RaissaOliv](https://github.com/RaissaOliv).

---