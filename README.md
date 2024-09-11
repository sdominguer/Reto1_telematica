Este proyecto implementa un sistema de intercambio de archivos basado en la arquitectura Peer-to-Peer (P2P) utilizando HTTP y gRPC. Cada peer puede actuar tanto como cliente para solicitar archivos, como servidor para compartir sus propios archivos. Los peers se registran en un tracker, el cual mantiene un registro de las direcciones IP y los archivos disponibles en la red.

Requisitos
Python

Bibliotecas adicionales:
flask
requests
grpcio
protobuf

Para instalar las dependencias necesarias, puedes ejecutar:
pip install flask requests grpcio protobuf
