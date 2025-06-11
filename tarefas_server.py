# tarefas_server.py
import grpc
import tarefas_pb2
import tarefas_pb2_grpc
import boto3
import pika
import uuid
from concurrent import futures

# Configuração do DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1') # Use sua região
table = dynamodb.Table('TarefasTable') # Nome da tabela que você vai criar no CF

# Configuração do RabbitMQ
RABBITMQ_HOST = 'YOUR_RABBITMQ_EC2_IP_OR_HOSTNAME' # Substitua pelo IP da EC2 do RabbitMQ
RABBITMQ_QUEUE = 'tarefas_eventos'

class TarefasService(tarefas_pb2_grpc.TarefasServiceServicer):
    def CriarTarefa(self, request, context):
        tarefa_id = str(uuid.uuid4())
        item = {
            'id': tarefa_id,
            'titulo': request.titulo,
            'descricao': request.descricao,
            'status': 'PENDENTE'
        }
        table.put_item(Item=item)

        # Publicar evento no RabbitMQ
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            channel = connection.channel()
            channel.queue_declare(queue=RABBITMQ_QUEUE)
            message = f"Tarefa '{request.titulo}' criada com ID: {tarefa_id}"
            channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=message)
            connection.close()
            print(f"Mensagem RabbitMQ publicada: {message}")
        except Exception as e:
            print(f"Erro ao publicar no RabbitMQ: {e}")

        return tarefas_pb2.TarefaResponse(tarefa=tarefas_pb2.Tarefa(**item))

    def ListarTarefas(self, request, context):
        response = table.scan()
        tarefas = [tarefas_pb2.Tarefa(**item) for item in response['Items']]
        return tarefas_pb2.ListarTarefasResponse(tarefas=tarefas)

   

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tarefas_pb2_grpc.add_TarefasServiceServicer_to_server(TarefasService(), server)
    server.add_insecure_port('[::]:50051') # Porta gRPC
    server.start()
    print("Servidor gRPC iniciado na porta 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()