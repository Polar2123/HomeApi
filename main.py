import socket
def main():
    sock = socket.socket()
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.connect(("localhost",9988))
    
        sock.send(b"SUB topic")

        byteResult = sock.recv(1024)
        result = byteResult.decode('utf-8')

        print(result)


if __name__ == "__main__":
    main()
