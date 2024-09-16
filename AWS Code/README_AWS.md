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
- **Bibliotecas**:
  - Flask 2.0.1
  - Requests 2.26.0
  - grpcio 1.43.0
  - protobuf 3.19.4

### Cómo se compila y ejecuta

1. **Compila el archivo `.proto`**:
   - Ejecuta `protoc --python_out=. --grpc_python_out=. tracker.proto` en la carpeta del proyecto para generar `tracker_pb2.py` y `tracker_pb2_grpc.py`.

2. **Ejecuta el Tracker**:
   - Navega a la carpeta del tracker y ejecuta:
     ```bash
     python tracker.py
     ```

3. **Ejecuta los Peers**:
   - En diferentes terminales, ejecuta:
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
  - Tracker escucha en el puerto 50051.
  - Peers utilizan los puertos 5000, 5001, 5002 para HTTP.

## 4. Descripción del ambiente de EJECUCIÓN (en producción)

- **Lenguaje de Programación**: Python 3.8 o superior
- **Bibliotecas**:
  - Flask 2.0.1
  - Requests 2.26.0
  - grpcio 1.43.0
  - protobuf 3.19.4

### IP o nombres de dominio en nube o en la máquina servidor

- **Tracker**: `<IP_DEL_TRACKER>`
- **Peers**: `<IP_DE_LAS_INSTANCIAS_PEER>`

### Cómo se configura el proyecto

- **IP y Puertos**:
  - Asegúrate de abrir los puertos 5000, 5001, 5002 en el grupo de seguridad de la instancia EC2.
  - Configura la IP del tracker en los archivos `peer.py` y asegúrate de que los peers apunten al tracker correcto.

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
- Utiliza el menú en el peer para ver archivos disponibles, solicitar archivos o salir de la red.
  
## 5. Otra información relevante
Dependencias: Verifica que todas las dependencias estén instaladas correctamente usando pip install.
Referencias
Documentación de Flask
Documentación de Requests
Documentación de gRPC
Documentación de Protobuf

