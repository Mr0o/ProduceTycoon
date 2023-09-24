import pygame
import json

class PlayerData:
    data = {
        'money': 1000
    }

    def load(filePath):
        try:
            with open(filePath + "playerData.json", 'r') as savefile:
                PlayerData.data = json.load(savefile)
        except FileNotFoundError:
            # if the file is not found then create a json file with default data
            PlayerData.save(filePath)

    def save(filePath):
        with open(filePath + "playerData.json", 'w') as savefile:
            json.dump(PlayerData.data, savefile, indent=4)
