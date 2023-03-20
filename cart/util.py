from enumList import peerType

def requestModel(msgFrom, data,msgTo = peerType.SERVER.value):
    return {
        'Sender':msgFrom,
        'Receiver': msgTo,
        'Data':data
    }