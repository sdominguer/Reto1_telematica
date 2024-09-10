import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tracker'))

from flask import Flask, request, send_from_directory
import grpc
from tracker import tracker_pb2
from tracker import tracker_pb2_grpc




PEER_ID = sys.argv[1] if len(sys.argv) > 1 else "peer_1"
TRACKER_IP = "localhost"
TRACKER_PORT = 50051
HTTP_PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
UPLOAD_FOLDER = sys.argv[3] if len(sys.argv) > 3 else './files'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Middleware para registrar las peticiones HTTP
@app.before_request
def log_request_info():
    print(f"Recibiendo petición: {request.method} {request.url}")

# Cliente gRPC para registrar archivos
def register_with_tracker(peer_id, files):
    with grpc.insecure_channel(f'{TRACKER_IP}:{TRACKER_PORT}') as channel:
        stub = tracker_pb2_grpc.TrackerServiceStub(channel)
        response = stub.RegisterPeer(tracker_pb2.RegisterPeerRequest(peer_id=peer_id, files=files))
        if response.success:
            print(f"Peer {peer_id} registrado con éxito en el tracker.")

# Servidor HTTP para compartir archivos
@app.route('/files/<filename>', methods=['GET'])
def share_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Subir archivos al peer
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No se encontró archivo", 400
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return "Archivo subido correctamente", 200

# Registrar archivos al iniciar el peer
def start_peer():
    files = os.listdir(UPLOAD_FOLDER)
    register_with_tracker(PEER_ID, files)

if __name__ == '__main__':
    start_peer()
    app.run(port=5000)  # Servidor HTTP corriendo en el puerto 5000
