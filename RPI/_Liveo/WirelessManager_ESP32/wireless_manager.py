
class CommunicationCallback:
    
    def __init__(self):
        pass
    
    def connectionCallback(self):
        print("Connected")
    
    def disconnectionCallback(self):
        print("Disconected")
    
    def didReceiveCallback(self,value):
        print(f"Received {value}")
    
    
class WirelessManager:
    
    def __init__(self,wsCallback = None):
        self.wsCallback = wsCallback
        
            
        if self.wsCallback != None:
            from ws_server import WSServer
            self.server = WSServer(self.wsCallback.connectionCallback,self.wsCallback.disconnectionCallback,self.wsCallback.didReceiveCallback)
            self.server.start()
    
    def isConnected(self):
        if self.wsCallback != None:
            return self.server.isConnected
    
                
    def sendDataToWS(self,data):
        if self.wsCallback != None:
            if self.server.isConnected:
                self.server.sendData(data)
    
    def process(self):
        if self.wsCallback != None:
            self.server.process_all()
    