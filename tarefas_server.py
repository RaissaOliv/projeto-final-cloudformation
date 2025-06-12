import grpc
import tarefas_pb2
import tarefas_pb2_grpc
import pika
import uuid
from concurrent import futures
import threading # 

# Configuração do RabbitMQ 
RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE = 'tarefas_eventos'

# In-memory storage for tasks
tarefas_db = {}
tarefas_lock = threading.Lock() # lock para proteger o acesso ao banco de dados em memória

class TarefasService(tarefas_pb2_grpc.TarefasServiceServicer):
    def CriarTarefa(self, request, context):
        tarefa_id = str(uuid.uuid4())
        item = {
            'id': tarefa_id,
            'titulo': request.titulo,
            'descricao': request.descricao,
            'status': 'PENDENTE'
        }
        with tarefas_lock: #dar lock antes de modificar o banco de dados
            tarefas_db[tarefa_id] = item

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
        with tarefas_lock: # dar lock para ler o banco de dados
            tarefas = [tarefas_pb2.Tarefa(**item) for item in tarefas_db.values()]
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