import socket
import threading
import os
import hashlib

# Configuración del tracker (servidor centralizado para registrar peers)
TRACKER_HOST = 'localhost'
TRACKER_PORT = 5000
peers = {}  # Diccionario para almacenar archivos y los peers que los tienen

# Función del tracker para manejar conexiones de los peers
def handle_peer(conn, addr):
    global peers
    conn.send(b"Bienvenido al Tracker. Envia 'LIST' para ver archivos o 'REGISTER <archivo>' para registrar uno.\n")
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            
            command = data.split()
            if command[0] == 'REGISTER' and len(command) > 1:
                filename = command[1]
                # Registrar el archivo y el peer en la lista
                if filename in peers:
                    peers[filename].append(addr[0])
                else:
                    peers[filename] = [addr[0]]
                conn.send(f"Archivo {filename} registrado con éxito.\n".encode())
            elif command[0] == 'LIST':
                # Enviar la lista de archivos y sus peers
                file_list = '\n'.join([f"{key}: {', '.join(value)}" for key, value in peers.items()])
                conn.send(file_list.encode() if file_list else b"No hay archivos registrados.\n")
        except:
            break
    conn.close()

# Función para iniciar el tracker
def tracker():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TRACKER_HOST, TRACKER_PORT))
    server.listen(5)
    print(f"Tracker escuchando en {TRACKER_HOST}:{TRACKER_PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_peer, args=(conn, addr)).start()

# Función para que un peer actúe como cliente y se conecte al tracker
def peer_client(tracker_host, tracker_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((tracker_host, tracker_port))
    print(client.recv(1024).decode())
    while True:
        cmd = input("Ingrese comando: ")
        client.send(cmd.encode())
        response = client.recv(4096).decode()
        print(response)
        if cmd.startswith("REGISTER"):
            filename = cmd.split()[1]
            threading.Thread(target=peer_server, args=(filename,)).start()

# Función para que el peer actúe como servidor de archivos y comparta datos en fragmentos
def peer_server(filename, port=0, chunk_size=1024):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(1)
    port = server.getsockname()[1]  # Obtener el puerto asignado dinámicamente
    print(f"Compartiendo {filename} en el puerto {port}")
    
    while True:
        conn, addr = server.accept()
        print(f"Enviando {filename} a {addr}")
        with open(filename, 'rb') as f:
            while chunk := f.read(chunk_size):
                conn.send(chunk)
        conn.close()

# Función para descargar un archivo desde otro peer en fragmentos
def download_file(peer_ip, peer_port, filename, chunk_size=1024):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((peer_ip, peer_port))
    with open(f"downloaded_{filename}", 'wb') as f:
        while True:
            chunk = client.recv(chunk_size)
            if not chunk:
                break
            f.write(chunk)
    client.close()
    print(f"Archivo {filename} descargado con éxito.")
    
    # Verificación de integridad del archivo usando hash MD5
    original_hash = hashlib.md5(open(filename, 'rb').read()).hexdigest()
    downloaded_hash = hashlib.md5(open(f"downloaded_{filename}", 'rb').read()).hexdigest()
    if original_hash == downloaded_hash:
        print("El archivo se descargó correctamente y es íntegro.")
    else:
        print("Error: El archivo descargado no coincide con el original.")

# Punto de entrada del programa
if __name__ == "__main__":
    option = input("¿Ejecutar como Tracker (T) o Peer (P)? ")
    if option.lower() == 't':
        tracker()
    elif option.lower() == 'p':
        peer_client(TRACKER_HOST, TRACKER_PORT)

