import socket


def server_start():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 8000))
        server.listen(4)
        while True:
            print('Working...')
            client_socket, address = server.accept()
            data = client_socket.recv(1024).decode('utf-8')
            HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charsert=utf-8\r\n\r\n'
            content = 'TOKEN OK'.encode('utf-8')
            client_socket.send(HDRS.encode('utf-8') + content)
            client_socket.shutdown(socket.SHUT_RDWR)
            print('Close.')
            print(data)
    except KeyboardInterrupt:
        server.close()

