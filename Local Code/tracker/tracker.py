import grpc
from concurrent import futures
import tracker_pb2
import tracker_pb2_grpc

# Middleware para gRPC
class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        print(f"Interceptando llamada: {handler_call_details.method}")
        return continuation(handler_call_details)

class TrackerService(tracker_pb2_grpc.TrackerServiceServicer):
    def __init__(self):
        self.peers = {}
    
    # Registrar un peer en la red
    def RegisterPeer(self, request, context):
        self.peers[request.peer_id] = request.files
        print(f"Peer {request.peer_id} registrado con los archivos: {request.files}")
        return tracker_pb2.RegisterPeerResponse(success=True)
    
    # Buscar un archivo en la red
    def SearchFile(self, request, context):
        peers_with_file = [peer_id for peer_id, files in self.peers.items() if request.file_name in files]
        return tracker_pb2.SearchFileResponse(peers=peers_with_file)
    
    # Eliminar un peer de la red (funcionalidad leave)
    def LeavePeer(self, request, context):
        peer_id = request.peer_id
        if peer_id in self.peers:
            del self.peers[peer_id]
            print(f"Peer {peer_id} ha dejado la red.")
            return tracker_pb2.LeavePeerResponse(success=True)
        else:
            return tracker_pb2.LeavePeerResponse(success=False)

def serve():
    # Agregando el interceptor al servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[LoggingInterceptor()])
    tracker_pb2_grpc.add_TrackerServiceServicer_to_server(TrackerService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Tracker corriendo en el puerto 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()