**ST0263 Tópicos Especiales en Telemática**

**Estudiante(s):** Sara Isabel Ortiz, siortizh@eafit.edu.co & Sara Dominguez, sdominguer@eafit.edu.co

**Profesor:** Juan Carlos Montoya, jcmonoy@eafit.edu.co

# Proyecto de Intercambio de Archivos P2P

## 1. Breve descripción de la actividad

Este proyecto implementa un sistema de intercambio de archivos basado en la arquitectura Peer-to-Peer (P2P) utilizando HTTP y gRPC. Cada peer puede actuar tanto como cliente para solicitar archivos, como servidor para compartir sus propios archivos. Los peers se registran en un tracker, el cual mantiene un registro de las direcciones IP y los archivos disponibles en la red.

## 1.1. Aspectos cumplidos de la actividad propuesta

- Implementación de la comunicación P2P utilizando HTTP y gRPC.
- Registro de peers y archivos en un tracker.
- Habilidad para compartir y solicitar archivos entre peers.

## 1.2. Aspectos NO cumplidos de la actividad propuesta

- No se incluye un sistema de autenticación para los peers.
- No se ha implementado un sistema de encriptación para la transferencia de archivos.

## 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

- **Arquitectura**: Basada en el modelo Peer-to-Peer (P2P) con un servidor tracker para mantener el registro de archivos.
- **Patrones**: Uso de gRPC para la comunicación entre peers y el tracker. HTTP para compartir archivos.
- **Mejores prácticas**: Modularización del código en archivos separados para el tracker y los peers. Registro de actividad para depuración.

## 3. Descripción del ambiente de desarrollo y técnico

- **Lenguaje de Programación**: Python 3.8 o superior
  ```bash
   sudo apt install python3-pip

- **Bibliotecas**:
  - Flask 2.0.1  `pip install Flask`
  - Requests 2.26.0 `pip install requests`
  - grpcio 1.43.0 `pip install grpcio grpcio-tools`
  - protobuf 3.19.4 `pip install protobuf`
 
- **Requisitos**:
  - Docker en las instancias. `sudo apt install docker.io`
  - Acceso SSH a las instancias.

### Cómo se compila y ejecuta

1. **Compila el archivo `.proto`**:
   - Ejecuta `protoc --python_out=. --grpc_python_out=. tracker.proto` en la carpeta del proyecto para generar `tracker_pb2.py` y `tracker_pb2_grpc.py`.
  
2. **Instalar y ejecutar Docker en las 2 instancias**:
   - Instalar los paquetes necesarios para que funcione docker:
     ```bash
     sudo apt install apt-transport-https ca-certificates curl software-properties-common
     ```
   - Instalar Docker:
     ```bash
     sudo apt install docker-ce
     ```
   - Verificar la instalación:
     ```bash
     docker --version
     ```
  - Habilitar docker para que inicie automáticamente al iniciar el sistema:
     ```bash
     sudo systemctl enable docker
     ```
  - Permitir ejecutar docker sin `sudo`:
     ```bash
     sudo usermod -aG docker ${USER}
     ```

4. **Uso de Docker para las instancias**:
   Crear el Dockerfile en ambas instancias.
   - tracker:
     ```bash
     docker build -t tracker-app .
     ```
     ```bash
     docker run -d -p 50051:50051 tracker-app
     ```
   - peer:
     ```bash
     docker build -t peer-app .
     ```
     Asignar puertos distintos para cada peer de la instancia
     ```bash
     docker run -d -p 5000:5000 peer-app
     docker run -d -p 5001:5001 peer-app
     docker run -d -p 5002:5002 peer-app
     ```
   - Ver contenedores en ejecución:
      ```bash
     docker ps
     ```

5. **Ejecuta el Tracker**:
   - En la instancia del tracker ejecutar:
     ```bash
     python tracker.py
     ```

6. **Ejecuta los Peers**:
   - En diferentes terminales, ejecuta para cada peer:
     ```bash
     python peer.py <PEER_ID> <PUERTO_HTTP> <DIRECTORIO_ARCHIVOS>
     ```
   - Ejemplo:
     ```bash
     python peer.py peer_1 5000 ./peer1_files
     ```

### Detalles del desarrollo

- El archivo `tracker.py` maneja la lógica del tracker y las solicitudes de los peers.
- El archivo `peer.py` implementa la lógica de cada peer, incluyendo el registro y la búsqueda de archivos.

### Detalles técnicos

- **IP y puertos**:
  - Tracker escucha en el puerto 50051 a los peers con gRPC.
  - Peers utilizan los puertos 5000, 5001, 5002 para HTTP.

## 4. Descripción del ambiente de EJECUCIÓN (en producción)

- **Lenguaje de Programación**: Python 3.8 o superior
- **Bibliotecas**:
  - Flask 2.0.1
  - Requests 2.26.0
  - grpcio 1.43.0
  - protobuf 3.19.4

### IP o nombres de dominio en nube o en la máquina servidor

- **Tracker**: `IP pública: 3.235.198.58` e `IP privada: 172.31.79.21`
- **Peers**: `IP pública: 98.80.99.230` e `IP privada: 172.31.65.144`

### Cómo se configura el proyecto

- **IP y Puertos**:
  - Para la instancia del `peer` asegúrate de abrir los puertos 5000, 5001, 5002 en el grupo de seguridad de la instancia EC2; para la comunicación HTTP entre peers.
  - En ambas instancias `peer y tracker` debes abrir el puerto 50051 para la comunicación gRPC entre las instancias.
  - Configura la IP del tracker en los archivos `peer.py` y asegúrate de que los peers apunten a la instancia del `tracker`.

### Cómo se lanza el servidor

1. **Inicia el tracker**:
   ```bash
   python tracker.py
2. **Inicia los peers:**
   ```bash
   python peer.py <PEER_ID> <PUERTO_HTTP> <DIRECTORIO_ARCHIVOS>

### Mini guía de uso
- Inicia el tracker.
- Inicia uno o más peers.
- Unirse a la red (Join):
  Cuando se inicia un peer se conectara automáticamente al tracker. El tracker va a registrar los archivos que tiene el peer y otros peers podran solicitarlos.
- Menú del peer
  ```bash
  Peer peer_1 registrado con éxito en el tracker.

  Opciones:
    1. Mostrar archivos disponibles
    2. Solicitar archivo (get)
    3. Subir archivo (put)
    4. Salir de la red (leave)
  Seleccione una opción:
  ```
  - Buscar un archivo:
    Selecciona la opción `1`. Ingresa el nombre del archivo que deseas buscar y el sistema te dirá en que peers está disponible.
    ```bash
    Ingrese el nombre del archivo que desea buscar: Ejemplo1.txt
    Archivo 'Ejemplo1.txt' encontrado en los peers: ['peer_1']
    El archivo 'Ejemplo1.txt' está disponible en los siguientes peers: ['peer_1']
    ```

  - Solicitar un Archivo GET (Simulación):
    Selecciona la opción `2` y escribe el nombre del archivo que deseas descargar. El sistema simulara la descarga del archivo desde otro peer y mostrará un mensaje indicando desde que peer se está descargando.
    ```bash
    Ingrese el nombre del archivo que desea descargar: Ejemplo1.txt
    Archivo 'Ejemplo1.txt' encontrado en los peers: ['peer_1']
    Descargando el archivo 'Ejemplo1.txt' desde peer_1...
    Descargando archivo desde http://peer_1:5000/files/Ejemplo1.txt...
    ```

  - Subir un archivo PUT:
    Selecciona la opción `3` para subir un archivo. El sistema mostrará el comando `curl -F "file=@<path-to-your-local-file>" http://<peer-ip>:<peer-port>/upload` que debe ejecutarse desde tu computadora local para subir un archivo al peer.

  - Salir de la red (Leave):
    Selecciona la opción 4 para que el peer deje la red. Esto permite que el peer se elimine del tracker.
    ```bash
    Saliendo de la red...
    Peer peer_1 ha dejado la red con éxito.
    ```
  
## 5. Otra información relevante
Dependencias: Verifica que todas las dependencias estén instaladas correctamente usando pip install.
Referencias
Documentación de Flask
Documentación de Requests
Documentación de gRPC
Documentación de Protobuf

