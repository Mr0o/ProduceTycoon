import json

class PlayerData:
    data = {
        'money': 1000
    }

    @staticmethod
    def load(filePath):
        with open(filePath + "playerData.json", 'r') as savefile:
            PlayerData.data = json.load(savefile)

    @staticmethod
    def save(filePath):
        with open(filePath + "playerData.json", 'w') as savefile:
            json.dump(PlayerData.data, savefile, indent=4)
