import pickle
import socket
import json

server_address = ('localhost', 8000)
continueData = True
timeout_ = 50

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
except:
    print("ERROR : Server Not found.")

timeout_count = 0
loop_reciver = True

while loop_reciver:
    try:
        data_chunks = []
        while True:
            try:
                sock.settimeout(1)
                received_data = sock.recv(1024*1024)
                if not received_data:
                    timeout_count += 1
                    if timeout_ <= timeout_count:
                        loop_reciver = False
                    break
                continueData = True
            except socket.timeout:
                if continueData:
                    continueData = False
                break
            except:
                break
            data_chunks.append(received_data)
        if len(data_chunks) == 0:
            continue
        data = b''.join(data_chunks)
        decordedData = pickle.loads(data)
        json_data = json.dumps(decordedData)
        print(json_data)
    except:
        break

sock.close()
