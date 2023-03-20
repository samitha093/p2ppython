import time
from util import requestModel
from errorList import errMsg

def seedProx(mySocket,USERID,MODE,MOBILEMODELPARAMETERS,MODELPARAMETERS,SHELL_TIMEOUT):
    ModelParamLoop = True
    print(errMsg.MSG004.value)
    peerTypeReq = ["PEERTYPE",MODE]
    mySocket.request(requestModel(USERID,peerTypeReq))
    ########################################################################
    timerCal =0
    while ModelParamLoop:
        tempDataSet = mySocket.RECIVEQUE.copy()
        if len(tempDataSet) > 0:
            for x in tempDataSet:
                mySocket.queueClean(x)
                if x.get("Data")[0] == "MODELREQUEST":
                    print("RECIVED MODEL REQUEST FROM : ",x.get("Sender"))
                    modelparameters = ["MODELPARAMETERS",MODELPARAMETERS]
                    mySocket.request(requestModel(USERID,modelparameters,x.get("Sender")))
                    print("MODEL PARAMETERS SEND TO : ",x.get("Sender"))
                elif x.get("Data")[0] == "MOBILEMODELPARAMETERS":
                    print("parameter requst from Mobile client")
                    #need more develop more details
                else:
                    print("UNKNOWN MESSAGE : ",x)
        time.sleep(1)
        timerCal +=1
        if timerCal == SHELL_TIMEOUT:
            ModelParamLoop = False
    ########################################################################
    mySocket.close(0,USERID)
    return