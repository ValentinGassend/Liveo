import json

class Meeting:
    def __init__(self, filename):
        self.filename = filename

    def add(self, new_data):
        with open(self.filename, 'r+') as file:
            file_data = json.load(file)
            new_data["id"] = len(file_data["rendezvous"]) + 1
            file_data["rendezvous"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def remove(self, info):
        with open(self.filename, 'r+') as file:
            file_data = json.load(file)
            for item in file_data["rendezvous"]:
                if info in item['titre']:
                    file_data["rendezvous"].remove(item)
                    break
        with open(self.filename, 'w') as f:
            json.dump(file_data, f, indent=2)