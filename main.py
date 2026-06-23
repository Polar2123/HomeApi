import socket
import queue
import threading

def main():
    sock = socket.socket()
    connected = False
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        while not connected:
            try:
                connected = startConnection(sock)
            except:
                pass

        handleConnection(sock)
        

def handleConnection(socket):
    try:
        while True:
            data = socket.recv(1024)
            if not data: raise Exception("The Socket has been Closed!")
             

    except Exception as e:
        print(repr(e))
        print("Closing down the API!")

def startConnection(socket) -> bool:
    socket.connect(("localhost",9988))
    socket.send(b"CONN api")
    byteResult = socket.recv(1024)
    result = decode(byteResult)
    return result == "CONNACK"

def decode(byteResult):
    return byteResult.decode('utf-8')

if __name__ == "__main__":
    main()
