import socket
import json

HOST = 'localhost'
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT))
    s.sendall(b"STATUS")
    data = s.recv(16384)
    texto = data.decode('utf-8')
    try:
        estado = json.loads(texto)
        print(json.dumps(estado, indent=2, ensure_ascii=False))
    except Exception:
        print('Respuesta no JSON:')
        print(texto)
except Exception as e:
    print(f"ERROR: no se pudo conectar a {HOST}:{PORT} -> {e}")
finally:
    try:
        s.close()
    except:
        pass
