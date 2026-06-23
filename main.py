import socket
import queue
import threading
import time
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = Broker_Client("temperatureSensor")
    print("Hello!")
    thread = threading.Thread(
        target=client.boot,
        daemon=True
    )
    thread.start()

    yield

app = FastAPI(lifespan=lifespan)

def Broker_Client(id: str):
    client_id = id
    

    def closure():
        pass

    def boot():
        sock = socket.socket()
        connected = False
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
            while not connected:
                try:
                    connected = start_connection(sock)
                
                except:
                    print("Waiting for connection...")
                    time.sleep(1) # Wait a bit between connection attempts
                
            handler = message_handler()
            threading.Thread(target=handle_connection,args=(sock,handler)).start()

            handler.process()

    def get_id():
        return id
   

    closure.get_id = get_id
    closure.boot = boot


    return closure

def message_handler():
    message_queue = queue.Queue()
    is_working = True

    def closure():
        pass

    def add(payload):
        message_queue.put(payload)

    def process_messages():
        nonlocal is_working
        while is_working or not message_queue.empty():
            try:
                payload = message_queue.get(timeout=5)
                topic, message = payload.split(" ",1)
                print(f"Received message on topic \"{topic}\": {message}")
            except Exception as e:
                pass

    def shutdown():
        nonlocal is_working
        is_working = False
    

    closure.add = add
    closure.process = process_messages
    closure.close = shutdown
    return closure

def handle_connection(socket,message_closure):
    try:
        subscribe_to_topic(socket,"temperature") 

        while True:
            data = socket.recv(1024)
            if not data: raise Exception("The Socket has been Closed!")
            decoded_data = decode(data)
            message_closure.add(decoded_data)            

    except Exception as e:
        print(repr(e))
        print("Lost connection!")
        print("Closing down the API!")
        message_closure.close()

def subscribe_to_topic(socket,topic):
    response = ""
    while response != "SUBACK":
        socket.send(encode(f"SUB {topic}"))
        data = socket.recv(1024)
        if not data: raise Exception("Unable to Contact Socket!")
        response = decode(data)
    print(f"Subscribed to the topic \"{topic}\"")


def start_connection(socket) -> bool:
    socket.connect(("localhost",9988))
    socket.send(b"CONN api")
    byteResult = socket.recv(1024)
    result = decode(byteResult)
    return result == "CONNACK"

def decode(byteResult):
    return byteResult.decode('utf-8')

def encode(string):
    return string.encode('utf-8')

temperature_sensor = {}

@app.get("/temperature/{sensor_id}")
async def get_temperature(sensor_id: str):
    return temperature_sensor.get(sensor_id,{"message": "Couldn't find the sensor!"}) 


if __name__ == "__main__":
    main()
