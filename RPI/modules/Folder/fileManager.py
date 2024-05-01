class FileManager: 
    def __init__(self,file):
        self.file = file
        pass

    def read(self):
        with open(self.file) as f:
            text = f.read()
        self.file.close()
        return text
    
    def write(self,data):
        if not type(data)==type(""):
            data = str(data)
        
        with open(self.file) as f:
            text = f.write()
        self.file.close()
        return text
