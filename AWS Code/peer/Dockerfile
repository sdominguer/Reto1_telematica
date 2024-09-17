# Dockerfile para los peers

# Usa una imagen base de Python
FROM python:3.8-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del peer
COPY . /app

# Instalar las dependencias necesarias
RUN pip install grpcio grpcio-tools flask requests

# Exponer el puerto 5000 para HTTP y otros puertos para más peers
EXPOSE 5000
EXPOSE 5001
EXPOSE 5002

# Comando para ejecutar el peer
CMD ["python", "peer.py", "peer_1", "5000", "./peer1_files"]
