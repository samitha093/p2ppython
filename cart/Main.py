import random
import signal
import sys
import sys
import time
import os
from soc9k import peerCom
from enumList import conctionType
from com import communicationProx
from seed import seedProx
from file import getID

HOST = '141.145.200.6' #141.145.200.6
PORT = 9000

########################################################################
#------------------------------PEER   DATA-----------------------------#
# MODELPARAMETERS  = "jhjhhkhkhkl"
MODELPARAMETERS  = bytes(1024)  # 1 KB
# MODELPARAMETERS  = bytes(100*1024)  # 100 KB
# MODELPARAMETERS  = bytes(1024*1024)  # 1 MB
# MODELPARAMETERS  = bytes(3*1024*1024)  # 3 MB
# MODELPARAMETERS  = bytes(5*1024*1024)  # 5 MB
########################################################################

########################################################################
#------------------------------MOBILE MODEL----------------------------#
# MOBILEMODELPARAMETERS  = "jhjhhkhkhkl"
MOBILEMODELPARAMETERS  = bytes(1024)  # 1 KB
# MOBILEMODELPARAMETERS  = bytes(1024*1024)  # 1 MB
# MOBILEMODELPARAMETERS  = bytes(5*1024*1024)  # 5 MB
########################################################################

def sigint_handler(signal, frame, mySocket, USERID):
    print('Exiting program...')
    mySocket.close(0,USERID)
    sys.exit(0)

def mainFunn(MODE, TIMEOUT = 12, RECIVER_TIMEOUT = 5*60, SYNC_CONST = 1):
    try:
        mySocket = peerCom(HOST, PORT, TIMEOUT , MODE, SYNC_CONST)
        signal.signal(signal.SIGINT, lambda signal, frame: sigint_handler(signal, frame, mySocket, USERID))
        TEMPUSERID = mySocket.connect()
        USERID = getID(TEMPUSERID)
        mySocket.start_receiver()
        mySocket.start_sender()
        print("USER TYPE  : ",MODE)
        if MODE == conctionType.KERNEL.value:
            MODELPARAMETERLIST = communicationProx(mySocket,TEMPUSERID,MODE,RECIVER_TIMEOUT,MODELPARAMETERS,USERID)
        if MODE == conctionType.SHELL.value:
            seedProx(mySocket,TEMPUSERID,MODE,MOBILEMODELPARAMETERS,MODELPARAMETERS,RECIVER_TIMEOUT,USERID)
    except Exception as e:
        print("Error occurred while running in", MODE, " mode ")

#Call from Separat thread
if __name__ == "__main__":
    while True:
        randomNo= random.randint(0, 50)
        if randomNo > 15:
            mainFunn("SHELL")
        else:
            mainFunn("KERNEL")
        time.sleep(randomNo)
