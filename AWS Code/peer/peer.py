import sys  # Importa el módulo sys para manejar argumentos de línea de comandos
import os  # Importa el módulo os para manejar rutas y archivos
import grpc  # Importa la biblioteca grpc para la comunicación entre el peer y el tracker
import time  # Importa el módulo time para usar la función sleep


sys.path.append(os.path.join(os.path.dirname(__file__), 'tracker'))  # Añade la carpeta 'tracker' al sys.path para importar los archivos generados por gRPC

import requests  # Biblioteca para manejar peticiones HTTP (usada en la descarga de archivos)
from flask import Flask, request, send_from_directory  # Importa Flask para crear un servidor HTTP
from concurrent import futures  # Importa futures para manejar la concurrencia en el servidor gRPC
from threading import Thread  # Importa threading para ejecutar el servidor HTTP en segundo plano

from tracker import tracker_pb2  # Importa las clases generadas a partir del archivo .proto
from tracker import tracker_pb2_grpc  # Importa el stub gRPC para interactuar con el tracker

# Variables globales que se inicializan con valores pasados en la línea de comandos
PEER_ID = sys.argv[1] if len(sys.argv) > 1 else "peer_1"  # ID del peer, por defecto "peer_1"
TRACKER_IP = "172.31.79.21"  # Dirección IP del tracker
TRACKER_PORT = 50051  # Puerto del tracker
HTTP_PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5000  # Puerto HTTP del peer, por defecto 5000
UPLOAD_FOLDER = sys.argv[3] if len(sys.argv) > 3 else './files'  # Directorio donde se almacenan los archivos del peer

# Verifica si la carpeta de archivos existe, si no, la crea
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Crea el directorio de archivos si no existe

# Inicializa la aplicación Flask para manejar el servidor HTTP
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Configura la carpeta donde Flask busca los archivos

# Middleware que se ejecuta antes de cada petición HTTP para registrar la petición
@app.before_request
def log_request_info():
    print(f"Recibiendo petición: {request.method} {request.url}")  # Muestra en consola el método y URL de cada petición HTTP

# Función para registrar un peer en el tracker vía gRPC
def register_with_tracker(peer_id, files):
    with grpc.insecure_channel(f'{TRACKER_IP}:{TRACKER_PORT}') as channel:  # Establece el canal gRPC con el tracker
        stub = tracker_pb2_grpc.TrackerServiceStub(channel)  # Crea el stub para interactuar con el servicio tracker
        response = stub.RegisterPeer(tracker_pb2.RegisterPeerRequest(peer_id=peer_id, files=files))  # Llama al método RegisterPeer del tracker con el ID del peer y su lista de archivos
        if response.success:  # Si el registro fue exitoso
            print(f"Peer {peer_id} registrado con éxito en el tracker.")  # Muestra un mensaje de confirmación

# Función para informar al tracker que un peer deja la red
def leave_network(peer_id):
    with grpc.insecure_channel(f'{TRACKER_IP}:{TRACKER_PORT}') as channel:  # Establece el canal gRPC con el tracker
        stub = tracker_pb2_grpc.TrackerServiceStub(channel)  # Crea el stub para interactuar con el tracker
        response = stub.LeavePeer(tracker_pb2.LeavePeerRequest(peer_id=peer_id))  # Llama al método LeavePeer con el ID del peer
        if response.success:  # Si la solicitud fue exitosa
            print(f"Peer {peer_id} ha dejado la red con éxito.")  # Muestra un mensaje de confirmación
        else:
            print(f"Error al intentar que el peer {peer_id} deje la red.")  # Informa en caso de error

# Función para buscar un archivo en el tracker
def search_file_in_tracker(file_name):
    with grpc.insecure_channel(f'{TRACKER_IP}:{TRACKER_PORT}') as channel:  # Establece el canal gRPC con el tracker
        stub = tracker_pb2_grpc.TrackerServiceStub(channel)  # Crea el stub para interactuar con el tracker
        response = stub.SearchFile(tracker_pb2.SearchFileRequest(file_name=file_name))  # Llama al método SearchFile con el nombre del archivo
        if response.peers:  # Si el archivo fue encontrado en algún peer
            print(f"Archivo '{file_name}' encontrado en los peers: {response.peers}")  # Muestra en qué peers está disponible el archivo
            return response.peers  # Retorna los peers que tienen el archivo
        else:
            print(f"Archivo '{file_name}' no encontrado en ningún peer.")  # Si no se encontró el archivo, muestra un mensaje
            return None  # Retorna None

# Función para descargar un archivo de otro peer usando HTTP
def download_file_from_peer(peer_ip, file_name):
    url = f"http://{peer_ip}:5000/files/{file_name}"  # Construye la URL para descargar el archivo desde el peer
    print(f"Intentando conectar al peer en {peer_ip} para descargar el archivo '{file_name}'...")  # Informa que intentará la conexión

    try:
        response = requests.get(url)  # Realiza la petición GET para descargar el archivo
        if response.status_code == 200:  # Si la descarga fue exitosa
            print(f"Conexión establecida con el peer {peer_ip}.")  # Informa que la conexión se ha establecido correctamente
            with open(file_name, 'wb') as f:  # Abre el archivo en modo escritura binaria
                f.write(response.content)  # Escribe el contenido descargado en el archivo
            print(f"Conexión exitosa. Archivo '{file_name}' descargado con éxito desde {peer_ip}.")  # Informa que el archivo fue descargado correctamente
        else:
            print(f"Error al descargar el archivo desde {peer_ip}: Estado HTTP {response.status_code}")  # Muestra un mensaje de error en caso de fallo
    except requests.exceptions.RequestException as e:  # Maneja errores de conexión
        print(f"Fallo al conectar con el peer {peer_ip}: {e}")  # Informa sobre el fallo de conexión

# Función que instruye al usuario a usar curl para subir un archivo
def upload_file_to_peer():
    print("\nUsa el siguiente comando `curl` desde tu computadora local para subir el archivo:")  # Informa al usuario cómo usar curl
    print(f'curl -F "file=@/ruta/del/archivo" http://{PEER_ID}:{HTTP_PORT}/upload')  # Muestra el comando curl con la dirección del peer y puerto
    print("\nReemplaza '/ruta/del/archivo' con la ruta del archivo en tu computadora.")  # Indica al usuario que debe reemplazar la ruta del archivo
    # Solicitar el nombre del archivo para verificar si ha sido subido
    file_name = input("\nIngresa el nombre del archivo que subiste para verificar que se haya subido correctamente: ")  # Pide al usuario el nombre del archivo subido
    
    # Esperar hasta que el archivo esté disponible en el peer
    while not os.path.exists(os.path.join(UPLOAD_FOLDER, file_name)):  # Verifica si el archivo ha sido subido correctamente
        print(f"Esperando que el archivo '{file_name}' sea subido...")  # Informa que está esperando que el archivo se suba
        time.sleep(5)  # Espera 5 segundos antes de volver a verificar
    
    print(f"Archivo '{file_name}' subido correctamente al peer.")  # Informa que el archivo se ha subido exitosamente

# Ruta en el servidor HTTP para compartir archivos
@app.route('/files/<filename>', methods=['GET'])
def share_file(filename):
    peer_requesting = request.remote_addr  # Obtiene la IP del peer solicitante
    print(f"Conexión establecida con el peer {peer_requesting}. Solicitud de archivo '{filename}'.")  # Informa que se ha establecido la conexión
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)  # Envía el archivo solicitado al peer solicitante

# Ruta en el servidor HTTP para subir archivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:  # Verifica si hay un archivo en la solicitud
        return "No se encontró archivo", 400  # Si no, devuelve un error
    file = request.files['file']  # Obtiene el archivo de la solicitud
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))  # Guarda el archivo en la carpeta de subida
    return "Archivo subido correctamente", 200  # Devuelve un mensaje de éxito

# Función que registra al peer en el tracker al inicio
def start_peer():
    files = os.listdir(UPLOAD_FOLDER)  # Lista los archivos disponibles en el peer
    register_with_tracker(PEER_ID, files)  # Registra el peer y los archivos en el tracker

# Función que informa al tracker que el peer está dejando la red
def stop_peer():
    leave_network(PEER_ID)  # Llama a la función leave_network para informar al tracker

# Menú interactivo para manejar las operaciones del peer
def peer_menu():
    while True:  # Bucle para mostrar el menú constantemente
        print("\nOpciones:")
        print("1. Mostrar archivos disponibles")
        print("2. Solicitar archivo (get)")
        print("3. Subir archivo (put)")
        print("4. Salir de la red (leave)")
        option = input("Seleccione una opción: ")  # Pide al usuario que seleccione una opción

        if option == "1":  # Mostrar archivos disponibles
            file_name = input("Ingrese el nombre del archivo que desea buscar: ")
            peers_with_file = search_file_in_tracker(file_name)  # Busca el archivo en el tracker
            if peers_with_file:
                print(f"El archivo '{file_name}' está disponible en los siguientes peers: {peers_with_file}")  # Muestra los peers que tienen el archivo
        elif option == "2":  # Descargar archivo
            file_name = input("Ingrese el nombre del archivo que desea descargar: ")
            peers_with_file = search_file_in_tracker(file_name)  # Busca el archivo en el tracker
            if peers_with_file:
                print(f"Descargando el archivo '{file_name}' desde {peers_with_file[0]}...")  # Informa desde qué peer se descargará
                download_file_from_peer(peers_with_file[0], file_name)  # Descarga el archivo desde el primer peer encontrado
            else:
                print(f"Archivo '{file_name}' no disponible.")  # Informa si no se encontró el archivo
        elif option == "3":  # Subir archivo
            upload_file_to_peer()  # Llama a la función para subir un archivo
        elif option == "4":  # Salir de la red
            print("Saliendo de la red...")
            stop_peer()  # Llama a la función para salir de la red
            break  # Rompe el bucle y sale
        else:
            print("Opción no válida. Inténtelo de nuevo.")  # Muestra un mensaje si la opción es inválida

# Función principal que arranca el peer y el servidor HTTP
if __name__ == '__main__':
    start_peer()  # Registra al peer y sus archivos en el tracker
    # Ejecuta el servidor HTTP en segundo plano para compartir archivos
    from threading import Thread  # Importa el módulo de hilos para ejecutar el servidor en segundo plano
    server_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=HTTP_PORT, use_reloader=False))  # Arranca el servidor Flask en todos los hosts
    server_thread.start()  # Inicia el servidor en un hilo separado

    # Mostrar el menú de opciones para el peer
    peer_menu()  # Muestra el menú interactivo para el peer
