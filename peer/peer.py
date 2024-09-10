import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tracker'))

from flask import Flask, request, send_from_directory
import grpc
from tracker import tracker_pb2
from tracker import tracker_pb2_grpc
import requests



PEER_ID = sys.argv[1] if len(sys.argv) > 1 else "peer_1"
TRACKER_IP = "localhost"
TRACKER_PORT = 50051
HTTP_PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
UPLOAD_FOLDER = sys.argv[3] if len(sys.argv) > 3 else './files'


# Verifica si la carpeta de archivos existe, si no, la crea
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

# Buscar archivo en el tracker (gRPC)
def search_file_in_tracker(file_name):
    with grpc.insecure_channel(f'{TRACKER_IP}:{TRACKER_PORT}') as channel:
        stub = tracker_pb2_grpc.TrackerServiceStub(channel)
        response = stub.SearchFile(tracker_pb2.SearchFileRequest(file_name=file_name))
        if response.peers:
            print(f"Archivo '{file_name}' encontrado en los peers: {response.peers}")
            return response.peers
        else:
            print(f"Archivo '{file_name}' no encontrado en ningún peer.")
            return None

# Descargar archivo de otro peer (HTTP)
def download_file_from_peer(peer_ip, file_name):
    url = f"http://{peer_ip}:5000/files/{file_name}"
    print(f"Descargando archivo desde {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"Archivo '{file_name}' descargado con éxito desde {peer_ip}.")
    else:
        print(f"Error al descargar el archivo desde {peer_ip}: {response.status_code}")

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

# Mostrar opciones y permitir solicitar archivos
def peer_menu():
    while True:
        print("\nOpciones:")
        print("1. Mostrar archivos disponibles")
        print("2. Solicitar archivo")
        print("3. Salir")
        option = input("Seleccione una opción: ")

        if option == "1":
            file_name = input("Ingrese el nombre del archivo que desea buscar: ")
            peers_with_file = search_file_in_tracker(file_name)
            if peers_with_file:
                print(f"El archivo '{file_name}' está disponible en los siguientes peers: {peers_with_file}")
        elif option == "2":
            file_name = input("Ingrese el nombre del archivo que desea descargar: ")
            peers_with_file = search_file_in_tracker(file_name)
            if peers_with_file:
                print(f"Descargando el archivo '{file_name}' desde {peers_with_file[0]}...")
                download_file_from_peer(peers_with_file[0], file_name)
            else:
                print(f"Archivo '{file_name}' no disponible.")
        elif option == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == '__main__':
    start_peer()  # Registrar archivos y conectarse al tracker
    # Ejecutar el servidor HTTP en segundo plano para compartir archivos
    from threading import Thread
    server_thread = Thread(target=lambda: app.run(port=HTTP_PORT, use_reloader=False))
    server_thread.start()

    # Mostrar el menú de opciones para el peer
    peer_menu()