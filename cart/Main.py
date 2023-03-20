import random
import signal
import sys
import sys
import time
from soc9k import peerCom
from enumList import conctionType
from com import communicationProx
from seed import seedProx

HOST = '172.20.2.3'
PORT = 9000

########################################################################
#------------------------------PEER   DATA-----------------------------#
MODELPARAMETERS  = "jhjhhkhkhkl"
# MODELPARAMETERS  = bytes(1024)  # 1 KB
# MODELPARAMETERS  = bytes(100*1024)  # 100 KB
# MODELPARAMETERS  = bytes(1024*1024)  # 1 MB
# MODELPARAMETERS  = bytes(3*1024*1024)  # 3 MB
# MODELPARAMETERS  = bytes(5*1024*1024)  # 5 MB
########################################################################

########################################################################
#------------------------------MOBILE MODEL----------------------------#
MOBILEMODELPARAMETERS  = bytes(1024)  # 1 KB
########################################################################

def sigint_handler(signal, frame, mySocket, USERID):
    print('Exiting program...')
    mySocket.close(0,USERID)
    sys.exit(0)

def mainFunn(MODE, TIMEOUT = 12, RECIVER_TIMEOUT = 60, SYNC_CONST = 1):
    try:
        mySocket = peerCom(HOST, PORT, TIMEOUT , MODE, SYNC_CONST)
        signal.signal(signal.SIGINT, lambda signal, frame: sigint_handler(signal, frame, mySocket, USERID))
        USERID = mySocket.connect()
        mySocket.start_receiver()
        mySocket.start_sender()
        print("USER TYPE  : ",MODE)
        print("USER ID    : ",USERID)
        if MODE == conctionType.KERNEL.value:
            MODELPARAMETERLIST = communicationProx(mySocket,USERID,MODE,RECIVER_TIMEOUT,MODELPARAMETERS)
        if MODE == conctionType.SHELL.value:
            seedProx(mySocket,USERID,MODE,MOBILEMODELPARAMETERS,MODELPARAMETERS,RECIVER_TIMEOUT)
    except Exception as e:
        print("Error occurred while running in", MODE, " mode ")

#Call from Separat thread
if __name__ == "__main__":
    while True:
        randomNo= random.randint(0, 50)
        time.sleep(randomNo)
        if randomNo > 15:
            mainFunn("SHELL")
        else:
            mainFunn("KERNEL")
