# Reto 1 Telemática

Este proyecto implementa un sistema de intercambio de archivos basado en la arquitectura Peer-to-Peer (P2P) utilizando HTTP y gRPC. Cada peer puede actuar tanto como cliente para solicitar archivos, como servidor para compartir sus propios archivos. Los peers se registran en un tracker, el cual mantiene un registro de las direcciones IP y los archivos disponibles en la red.

## Características

- **Registro de Peers:** Cada peer se registra en un tracker centralizado con los archivos que tiene disponibles.
- **Búsqueda de Archivos:** Los peers pueden buscar archivos en otros peers mediante el tracker.
- **Transferencia de Archivos:** Los peers descargan archivos entre sí utilizando HTTP.
- **Desconexión de Peers:** Los peers pueden salir de la red, y el tracker elimina su información.

El sistema utiliza **gRPC** para la comunicación entre el tracker y los peers, y **HTTP** para la transferencia directa de archivos entre peers.

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

## Estructura del Proyecto

- **tracker.py:** Implementa el servidor tracker que mantiene el registro de los peers y los archivos disponibles en la red.
- **peer.py:** Implementa un peer que puede registrarse en el tracker, buscar archivos y compartir archivos con otros peers.

## Configuración en AWS

Para ejecutar este sistema en AWS, debes seguir estos pasos adicionales:

### Configuración de Instancias

1. **Tracker:** Configura una instancia en AWS EC2 para ejecutar el archivo `tracker.py`. Esta instancia será el tracker central donde los peers se registrarán.

2. **Peers:** Para cada peer, configura una instancia de EC2 que ejecute el archivo `peer.py`. Cada peer debe especificar su ID, el puerto HTTP y la carpeta donde almacenará sus archivos.

### Puertos de Acceso para Peers

Los peers utilizan los siguientes puertos para la transferencia de archivos a través de HTTP:

- Puerto **5000**: Para el primer peer.
- Puerto **5001**: Para el segundo peer.
- Puerto **5002**: Para el tercer peer.

Debes asegurarte de que estos puertos estén abiertos en la configuración de seguridad de las instancias de EC2 para que los peers puedan comunicarse entre sí. Para esto:

1. Ve a la consola de **EC2** en AWS.
2. En la sección de **Grupos de seguridad**, abre los puertos **5000-5002** en las reglas de entrada para permitir conexiones desde otros peers.

### Ejecución en AWS

Para ejecutar el sistema en AWS:

1. Sube los archivos `tracker.py`, `peer.py` y el archivo `.proto` correspondiente a las instancias.
2. En la instancia del **tracker**, ejecuta el archivo `tracker.py`:

        python tracker.py

3. En las instancias de los **peers**, ejecuta el archivo `peer.py` con los argumentos correspondientes para el ID del peer, el puerto HTTP y la carpeta de archivos:

        python peer.py peer_1 5000 ./files
        python peer.py peer_2 5001 ./files
        python peer.py peer_3 5002 ./files

### Ejemplo de Uso

- Los peers pueden subir archivos mediante el endpoint `/upload`.
- Para buscar un archivo en la red, ingresa el nombre del archivo y el tracker devolverá la lista de peers que lo poseen.
- Una vez que se encuentra el archivo, el peer puede descargarlo desde otro peer utilizando HTTP.
