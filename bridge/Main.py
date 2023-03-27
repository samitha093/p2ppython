import asyncio
import base64
import json
import pickle
import threading
import signal
from aiohttp import web
import sys
import time

from rndGen import generateId
from util import requestModel

HOST = 'http://localhost'
PORT = 9000
MOBILE_PORT = 8000
HTTPPORT = 5000

DATALIST = {}

DeviceTable = []
ClusterTable = {}
clusterSize = 2
SYNC_CONST = 1

shared_data = {}
MOBILEDATARECORDER = {}
DATARECORDER = {}

def responceModel(msgTo, data, msgFrom="SERVER"):
    return {
        'Sender':msgFrom,
        'Receiver': msgTo,
        'Data':data
    }

def reqirementHandler(data,writer,addr):
    global MOBILEDATARECORDER
    global DATARECORDER
    #############################################################
    ##Clustering Process Start        ---------------------------
    User = data.get("Sender")
    req = data.get("Data")
    if req[0] == "PEERTYPE":
        if User != req[2]:
            User = req[2]
        if req[1] == "KERNEL":
            print(User, " : ",req[1])
            if len(DeviceTable) >= clusterSize:
                temptable  = DeviceTable[:clusterSize]
                new_array = list(temptable)
                del DeviceTable[:clusterSize]
                ClusterId = generateId(12)
                ClusterTable[ClusterId] = new_array
                print("Custer created : ",ClusterId," : ",ClusterTable.get(ClusterId))
            ##Clustering Process END          ---------------------------
                defineCluster = ["CLUSTERID",ClusterId, "PEERLIST",ClusterTable.get(ClusterId)]
                tempData = responceModel(User,defineCluster)
                mailBox = DATARECORDER.get(User)
                mailBox.append(tempData)
            else:
                dataError = ["ERROR","There were not enough SHELL peers available at that time. Please try again later."]
                tempData = responceModel(User,dataError)
                mailBox = DATARECORDER.get(User)
                mailBox.append(tempData)
        elif req[1] == "SHELL":
            DeviceTable.append(User)
            print(User, " : ",req[1])
    elif req[0] == "EXIT":
        print("exit request from : ",User)
        if User in DeviceTable:
            DeviceTable.remove(User)
        dataAuth = ["EXITDONE"]
        tempData = responceModel(User,dataAuth)
        mailBox = DATARECORDER.get(User)
        mailBox.append(tempData)
        print(User, " : ",req[0])
    elif req[0] == "SENDMOBILEMODELPARAMETERS":
        print("recived mobile parameters")
        mobilemailBox = MOBILEDATARECORDER.get(req[1])
        mobilemailBox.append(data)

def requestHandler(data):
    User = data.get("Receiver")
    req = data.get("Data")
    if req[0] == "MODELREQUEST":
        mailBox = DATARECORDER.get(User)
        mailBox.append(data)
    if req[0] == "MODELPARAMETERS":
        mailBox = DATARECORDER.get(User)
        mailBox.append(data)

# This is the coroutine that will handle incoming cart connections
async def handle_client(reader, writer):
    global shared_data
    print('----------------------------------------------------------------')
    addr = writer.get_extra_info('peername')
    print('Connected by', addr)
    ##################USER_ID####################################
    userId = generateId(16)
    DATARECORDER[userId] = []
    print('User id : ', userId)
    writer.write(userId.encode())
    await writer.drain()
    ######################RUNNER_ENGINE##########################
    while True:
        #Sender handler -----------------------------------------
        if len(DATARECORDER.get(userId)) > 0:
            mailBox = DATARECORDER.get(userId)
            if mailBox[0].get("Data")[0] == "MODELPARAMETERS":
                    print("****MODELPARAMETERS FROM ",mailBox[0].get("Sender")," TO : ", userId)
            mailData = pickle.dumps(mailBox[0])
            data_size = sys.getsizeof(mailData)
            data_size_kb = data_size / 1024
            if data_size_kb < 1:
                writer.write(mailData)
                await writer.drain()
            else:
                print("OVERLOADED DATA FOUND : ",data_size_kb,"KB")
                MAX_CHUNK_SIZE = 1024
                chunks = [mailData[i:i+MAX_CHUNK_SIZE] for i in range(0, len(mailData), MAX_CHUNK_SIZE)]
                print("NO OF CHUNKS : ",len(chunks)," : SENDED")
                for x in chunks:
                    writer.write(x)
                    await writer.drain()
            mailBox.remove(mailBox[0])
        #Reciver handler-----------------------------------------
        try:
            # Receive and concatenate the data chunks
            data_chunks = []
            while True:
                try:
                    data = await asyncio.wait_for(reader.read(1024*1024), timeout=SYNC_CONST)
                except asyncio.TimeoutError:
                    break
                data_chunks.append(data)
            # Concatenate the chunks into a single bytes object
            if len(data_chunks) == 0:
                continue
            data = b''.join(data_chunks)
            decordedData = pickle.loads(data)
        except Exception as e:
            print("######## STATUS INFO : ",e)
            break
        if decordedData.get("Receiver") == "SERVER":
            req = decordedData.get("Data")
            if req[0] == "PEERTYPE":
                if userId != req[2]:
                    print("USER ID Replaced : ",userId," => ",req[2])
                    userId = req[2]
                    DATARECORDER[userId] = []
            reqirementHandler(decordedData,writer,addr)
        else:
            requestHandler(decordedData)
    #############################################################
    writer.close()
    print('Connection Closed : ',addr)

# This is the coroutine that will handle incoming mobile app connections
async def handle_mobile(reader, writer):
    global MOBILEDATARECORDER
    global DATARECORDER
    print('*****************************************************************')
    addr = writer.get_extra_info('peername')
    print('Connected by', addr)
    ##################USER_ID####################################
    userId = generateId(16)
    MOBILEDATARECORDER[userId] = []
    print('Mobile User id : ', userId)
    ######################RUNNER_ENGINE##########################
    if len(DeviceTable) > 0:
        tempReq = requestModel(DeviceTable[0],["MOBILEMODELPARAMETERS",userId])
        mailBox = DATARECORDER.get(DeviceTable[0])
        mailBox.append(tempReq)
        while True:
            time.sleep(5)
            if len(MOBILEDATARECORDER.get(userId)) > 0:
                myTempdata = MOBILEDATARECORDER.get(userId)
                myTempdata1 = myTempdata[0]
                myTempdatadataID = myTempdata1.get("Data")[1]
                myTempdatadataPARAMETERS = myTempdata1.get("Data")[2]
                print(type(myTempdatadataPARAMETERS)," : ", len(myTempdatadataPARAMETERS)/1024 , " KB")
                add_path(myTempdatadataID,myTempdatadataPARAMETERS)
                httpLink = HOST+":5000/download?ID="+myTempdatadataID
                writer.write(httpLink.encode() + b'\n')
                await writer.drain()
                myTempdata.remove(myTempdata1)
                break
    else:
        print("No active peer devices")
    #############################################################
    writer.close()
    print('Mobile Connection Closed : ',addr)

# This is the http server
async def handle_download(request):
    id = request.query.get('ID')
    if id in DATALIST:
        data = DATALIST[id]
        return web.Response(status=200, body=data)
    else:
        return web.Response(status=404)

def function_1():
    async def cart_Server():
        server = await asyncio.start_server(handle_client, '', PORT)
        print(f"Server listening on {''}:{PORT}")
        async with server:
            await server.serve_forever()
    try:
        asyncio.run(cart_Server())
    except KeyboardInterrupt:
        print("cart server stopped by user.")
        sys.exit(0)
    except:
        print("cart server stopped: Rutime error")
        sys.exit(0)

def function_2():
    async def mobile_Server():
        mobile_server = await asyncio.start_server(handle_mobile, '', MOBILE_PORT)
        print(f"Mobile server listening on {''}:{MOBILE_PORT}")
        async with mobile_server:
            await mobile_server.serve_forever()
    try:
        asyncio.run(mobile_Server())
    except KeyboardInterrupt:
        print("mobile server stopped by user.")
        sys.exit(0)
    except:
        print("mobile server stopped: Rutime error")
        sys.exit(0)

def add_path(userId,data):
    DATALIST[userId] = data

def function_3():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    async def run_server():
        app = web.Application()
        app.add_routes([web.get('/download', handle_download)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', HTTPPORT)
        await site.start()
        print(f"HTTP Proxy at http://localhost:{HTTPPORT}")
        await asyncio.sleep(3600*24*365)

    loop.create_task(run_server())

    five_mb_bytes = b'\x00' * 5 * 1024 * 1024
    add_path('123',five_mb_bytes)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

if __name__ == "__main__":
    running = True
    try:
        thread1 = threading.Thread(target=function_1)
        thread2 = threading.Thread(target=function_2)
        thread3 = threading.Thread(target=function_3)

        thread1.start()
        thread2.start()
        thread3.start()

        while running:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Program stopped by user.")
        running = False
        sys.exit(0)
    except:
        print("Program stopped: Rutime error")
        running = False
        sys.exit(0)
    finally:
        thread1.join()
        thread2.join()
        thread3.join()