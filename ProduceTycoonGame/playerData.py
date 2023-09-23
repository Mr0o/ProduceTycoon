import pygame
import json

class PlayerData:
    data = {
        'money': 1000
    }

    def load(filePath):
        with open(filePath, 'r') as savefile:
            PlayerData.data = json.load(savefile)

    def save(filePath):
        with open('./Resources/Playerdata/player.json', 'w') as savefile:
            json.dump(PlayerData.data, savefile, indent=4)
