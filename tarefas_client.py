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
# SUBSTITUA PELO IP/DNS REAL OBTIDO DOS OUTPUTS DO CLOUDFORMATION
GRPC_SERVER_ADDRESS = 'YOUR_EC2_PUBLIC_IP_OR_DNS:50051'

# Endereço do RabbitMQ (o mesmo IP público da EC2)
# SUBSTITUA PELO IP/DNS REAL OBTIDO DOS OUTPUTS DO CLOUDFORMATION
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
        created_task_id = response.tarefa.id # Guardar para atualização/exclusão

        time.sleep(1) # Pequena pausa para garantir que o evento do RabbitMQ seja processado

        # Listar tarefas
        logging.info("\nListando todas as tarefas...")
        response = stub.ListarTarefas(tarefas_pb2.ListarTarefasRequest())
        if response.tarefas:
            for tarefa in response.tarefas:
                logging.info(f"- ID: {tarefa.id}, Título: '{tarefa.titulo}', Descrição: '{tarefa.descricao}', Status: {tarefa.status}")
        else:
            logging.info("Nenhuma tarefa encontrada.")

        time.sleep(1)

        # Atualizar uma tarefa
        if created_task_id:
            logging.info(f"\nAtualizando tarefa {created_task_id} para CONCLUIDA...")
            response = stub.AtualizarTarefa(tarefas_pb2.AtualizarTarefaRequest(id=created_task_id, status="CONCLUIDA"))
            if response.tarefa.id:
                logging.info(f"Tarefa atualizada: ID={response.tarefa.id}, Status={response.tarefa.status}")
            else:
                logging.error(f"Falha ao atualizar tarefa {created_task_id}: {response.tarefa.id}")

        time.sleep(1)

        # Obter uma tarefa específica
        if created_task_id:
            logging.info(f"\nObtendo tarefa por ID: {created_task_id}...")
            response = stub.ObterTarefa(tarefas_pb2.ObterTarefaRequest(id=created_task_id))
            if response.tarefa.id:
                logging.info(f"Tarefa obtida: ID={response.tarefa.id}, Título='{response.tarefa.titulo}'")
            else:
                logging.error(f"Falha ao obter tarefa {created_task_id}: {response.tarefa.id}")
        
        time.sleep(1)

        # Excluir uma tarefa
        if created_task_id:
            logging.info(f"\nExcluindo tarefa: {created_task_id}...")
            response = stub.ExcluirTarefa(tarefas_pb2.ExcluirTarefaRequest(id=created_task_id))
            if response.sucesso:
                logging.info(f"Tarefa excluída com sucesso: {response.mensagem}")
            else:
                logging.error(f"Falha ao excluir tarefa: {response.mensagem}")

        time.sleep(1)

        # Listar tarefas novamente para confirmar exclusão
        logging.info("\nListando tarefas após exclusão...")
        response = stub.ListarTarefas(tarefas_pb2.ListarTarefasRequest())
        if response.tarefas:
            for tarefa in response.tarefas:
                logging.info(f"- ID: {tarefa.id}, Título: '{tarefa.titulo}', Status: {tarefa.status}")
        else:
            logging.info("Nenhuma tarefa encontrada (esperado se a tarefa foi excluída).")


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