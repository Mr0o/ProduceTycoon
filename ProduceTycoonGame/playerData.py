import pygame
import json

class PlayerData:
    data = {
        'money': 1000
    }

    def load():
        try:
            # load the data from the file
            with open('./Resources/Playerdata/player.json', 'r') as loadfile:
                PlayerData.data = json.load(loadfile)
        except FileNotFoundError:
            # if the file doesn't exist, create it using the default data
            PlayerData.save()

    def save(filePath):
        with open(filePath + "playerData.json", 'w') as savefile:
            json.dump(PlayerData.data, savefile, indent=4)
