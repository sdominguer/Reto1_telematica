# Reto 1 Telemática - Ejecución Local

Este proyecto implementa un sistema de intercambio de archivos basado en la arquitectura Peer-to-Peer (P2P) utilizando HTTP y gRPC. A continuación, se detallan los pasos para configurar y ejecutar el sistema localmente en tu entorno de desarrollo.

## Estructura del Proyecto


## Requisitos

### Lenguaje de Programación
- Python 3.6 o superior

### Bibliotecas adicionales:
- `flask`: Para implementar el servidor HTTP en los peers.
- `requests`: Para realizar solicitudes HTTP entre peers.
- `grpcio`: Para implementar la comunicación gRPC entre el tracker y los peers.
- `protobuf`: Para la serialización de mensajes gRPC.

Para instalar todas las dependencias necesarias, ejecuta el siguiente comando:

    pip install flask requests grpcio protobuf

## Configuración y Ejecución

### Paso 1: Generar los Archivos Protobuf

1. En la carpeta `/tracker`, asegúrate de que el archivo `tracker.proto` esté presente. Este archivo define los mensajes y servicios gRPC.
2. Genera los archivos de Python a partir del archivo `.proto` ejecutando el siguiente comando en la carpeta `/tracker`:

        python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tracker.proto

   Este comando generará dos archivos: `tracker_pb2.py` y `tracker_pb2_grpc.py`.

### Paso 2: Ejecutar el Tracker

1. Abre una terminal en Visual Studio Code.
2. Navega a la carpeta `/tracker`:

        cd /ruta/a/proyecto/tracker

3. Ejecuta el archivo `tracker.py` con el siguiente comando:

        python tracker.py

   Esto iniciará el servidor tracker en el puerto 50051.

### Paso 3: Ejecutar los Peers

Para cada peer, sigue estos pasos:

1. Abre una nueva terminal en Visual Studio Code.
2. Navega a la carpeta `/peer`:

        cd /ruta/a/proyecto/peer

3. Ejecuta el archivo `peer.py` especificando el ID del peer, el puerto HTTP y la carpeta para almacenar archivos. Por ejemplo:

        python peer.py peer_1 5000 ./peer1_files

   Donde:
   - `peer_1` es el nombre del peer.
   - `5000` es el puerto HTTP que el peer utilizará para compartir archivos.
   - `./peer1_files` es la carpeta donde el peer almacenará los archivos.

4. Repite el paso 3 en diferentes terminales para crear y ejecutar múltiples peers, asegurándote de usar diferentes ID de peer y puertos HTTP para cada uno. Por ejemplo:

        python peer.py peer_2 5001 ./peer2_files

### Notas

- Asegúrate de que el tracker esté en ejecución antes de iniciar los peers.
- Los puertos utilizados en los peers deben estar disponibles y no bloqueados por un firewall local.
- Cada peer debe tener un ID único y un puerto HTTP diferente.

## Ejemplo de Uso

- **Subir archivos:** Utiliza el endpoint `/upload` para subir archivos al peer.
- **Buscar archivos:** Los peers pueden consultar el tracker para buscar archivos disponibles en otros peers.
- **Descargar archivos:** Una vez que se encuentra el archivo, los peers pueden descargarlo desde otro peer utilizando HTTP.


