import sys
import os
import grpc
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'tracker'))

import requests
from flask import Flask, request, send_from_directory
from concurrent import futures
from threading import Thread

from tracker import tracker_pb2
from tracker import tracker_pb2_grpc


PEER_ID = sys.argv[1] if len(sys.argv) > 1 else "peer_1"
TRACKER_IP = "172.31.79.21"
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

# Cliente gRPC para dejar la red
def leave_network(peer_id):
    with grpc.insecure_channel(f'{TRACKER_IP}:{TRACKER_PORT}') as channel:
        stub = tracker_pb2_grpc.TrackerServiceStub(channel)
        response = stub.LeavePeer(tracker_pb2.LeavePeerRequest(peer_id=peer_id))
        if response.success:
            print(f"Peer {peer_id} ha dejado la red con éxito.")
        else:
            print(f"Error al intentar que el peer {peer_id} deje la red.")


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
    url = f"http://172.31.65.144:5000/files/{file_name}"
    print(f"Intentando conectar al peer en {peer_ip} para descargar el archivo '{file_name}'...")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Conexión establecida con el peer {peer_ip}.")
            file_path = os.path.join(UPLOAD_FOLDER, file_name)
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print(f"Conexión exitosa. Archivo '{file_name}' descargado con éxito desde {peer_ip}.")
        else:
            print(f"Error al descargar el archivo desde {peer_ip}: Estado HTTP {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Fallo al conectar con el peer {peer_ip}: {e}")


# Subir archivo directamente desde consola local  usando requests (POST)
def upload_file_to_peer():
    print("\nUsa el siguiente comando `curl` desde tu computadora local para subir el archivo:")
    print(f'curl -F "file=@/ruta/del/archivo" http://{PEER_ID}:{HTTP_PORT}/upload')
    print("\nReemplaza '/ruta/del/archivo' con la ruta del archivo en tu computadora.")
# Solicitar el nombre del archivo para verificar si ha sido subido
    file_name = input("\nIngresa el nombre del archivo que subiste para verificar que se haya subido correctamente: ")
    
    # Esperar hasta que el archivo esté disponible en el peer
    while not os.path.exists(os.path.join(UPLOAD_FOLDER, file_name)):
        print(f"Esperando que el archivo '{file_name}' sea subido...")
        time.sleep(5)  # Espera de 5 segundos antes de verificar nuevamente
    
    print(f"Archivo '{file_name}' subido correctamente al peer.")


# Servidor HTTP para compartir archivos
@app.route('/files/<filename>', methods=['GET'])
def share_file(filename):
    peer_requesting = request.remote_addr  # Obtener la IP del peer solicitante
    print(f"Conexión establecida con el peer {peer_requesting}. Solicitud de archivo '{filename}'.")
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

# El peer deja la red (leave)
def stop_peer():
    leave_network(PEER_ID)

# Mostrar opciones y permitir solicitar archivos
def peer_menu():
    while True:
        print("\nOpciones:")
        print("1. Mostrar archivos disponibles")
        print("2. Solicitar archivo (get)")
        print("3. Subir archivo (put)")
        print("4. Salir de la red (leave)")
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
            upload_file_to_peer()
        elif option == "4":
            print("Saliendo de la red...")
            stop_peer()
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == '__main__':
    start_peer()  # Registrar archivos y conectarse al tracker
    # Ejecutar el servidor HTTP en segundo plano para compartir archivos
    from threading import Thread
    server_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=HTTP_PORT, use_reloader=False))
    server_thread.start()

    # Mostrar el menú de opciones para el peer
    peer_menu()
