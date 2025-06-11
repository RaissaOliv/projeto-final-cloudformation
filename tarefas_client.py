# tarefas_client.py
import grpc
import tarefas_pb2
import tarefas_pb2_grpc
import pika
import time
import logging

# Configuração de logging para o cliente
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Endereço do servidor gRPC (IP público da EC2 ou DNS)
#TODO: substituir pelo ip da EC2 depois de criar no CLI
GRPC_SERVER_ADDRESS = 'YOUR_EC2_PUBLIC_IP_OR_DNS:50051'

# TODO: substituir pelo output do cloudformation ><
RABBITMQ_HOST = 'YOUR_EC2_PUBLIC_IP_OR_DNS'
RABBITMQ_QUEUE = 'tarefas_eventos'

def run_grpc_client():
    logging.info(f"Conectando ao servidor gRPC em: {GRPC_SERVER_ADDRESS}")
    with grpc.insecure_channel(GRPC_SERVER_ADDRESS) as channel:
        stub = tarefas_pb2_grpc.TarefasServiceStub(channel)

        # Criar uma tarefa
        logging.info("Criando tarefa: Estudar CloudFormation e gRPC...")
        response = stub.CriarTarefa(tarefas_pb2.CriarTarefaRequest(titulo="Estudar CloudFormation e gRPC", descricao="Aprofundar em IaC e comunicação distribuída"))
        logging.info(f"Tarefa criada: ID={response.tarefa.id}, Título='{response.tarefa.titulo}', Status={response.tarefa.status}")
        created_task_id = response.tarefa.id 

        time.sleep(1)

        # Listar tarefas
        logging.info("\nListando todas as tarefas...")
        response = stub.ListarTarefas(tarefas_pb2.ListarTarefasRequest())
        if response.tarefas:
            for tarefa in response.tarefas:
                logging.info(f"- ID: {tarefa.id}, Título: '{tarefa.titulo}', Descrição: '{tarefa.descricao}', Status: {tarefa.status}")
        else:
            logging.info("Nenhuma tarefa encontrada.")

        time.sleep(1)

       
def consume_rabbitmq_messages():
    logging.info(f"Conectando ao RabbitMQ em: {RABBITMQ_HOST}...")
    logging.info("Consumindo mensagens do RabbitMQ (CTRL+C para sair)...")
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

        def callback(ch, method, properties, body):
            logging.info(f" [x] Recebido: {body.decode()}")

        channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Erro de conexão com RabbitMQ. Verifique o IP ({RABBITMQ_HOST}) e o Security Group: {e}")
    except Exception as e:
        logging.error(f"Erro ao consumir RabbitMQ: {e}")
        logging.error("Certifique-se de que o RabbitMQ está acessível e a fila existe.")

if __name__ == '__main__':
    # Para rodar o cliente gRPC:
    run_grpc_client()

    # Para rodar o consumidor de mensagens do RabbitMQ (idealmente em outro terminal):
    # Descomente a linha abaixo e execute o script novamente em um novo terminal.
    # consume_rabbitmq_messages()