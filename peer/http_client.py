import requests

def download_file(peer_ip, file_name):
    url = f"http://{peer_ip}:5000/files/{file_name}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"Archivo {file_name} descargado con éxito desde {peer_ip}.")
    else:
        print(f"Error al descargar el archivo desde {peer_ip}.")
