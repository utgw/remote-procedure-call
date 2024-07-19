import socket
import os
import threading
import json
import math

def floor(x):
    return math.floor(x)
    
def nroot(n, x):
    return x ** (1 / n)
    
def reverse(s):
    return s[::-1]

def validAnagram(str1, str2):
    if len(str1) != len(str2):
        return False
    return sorted(str1) == sorted(str2)

def sort(strArr):
    return strArr.sort()

functions = {
    'floor': floor,
    'nroot': nroot,
    'reverse': reverse,
    'validAnagram': validAnagram,
    'sort': sort
}

def handle_client(connection):
    try:
        while True:
            data = connection.recv(1024)
            if data:
                request = json.loads(data.decode('utf-8'))
                method = request.get('method')
                params = request.get('params')
                request_id = request.get('id')
                if not isinstance(params, (list, tuple)):
                    params = [params]
                
                if method in functions:
                    try:
                      result = functions[method](*params)
                      response = {
                        'result': result,
                        'result_type': type(result).__name__,
                        'id': request_id
                      }
                    except Exception as e:
                        response = {
                            'error': str(e),
                            'id': request_id
                        }
                else:
                    response = {
                        'error': 'Method not found',
                        'id': request_id
                    }
                    
                connection.sendall(json.dumps(response).encode())
            else: 
              break
    finally:
        connection.close()
        
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = '/tmp/socket_file'

try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection, ))
    client_thread.start()