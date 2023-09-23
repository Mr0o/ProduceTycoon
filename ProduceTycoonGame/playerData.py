import pygame
import json

class PlayerData:
    data = {
        'money': 1000
    }

    def load():
        with open('./Resources/Playerdata/player.json', 'r') as savefile:
            PlayerData.data = json.load(savefile)

    def save():
        with open('./Resources/Playerdata/player.json', 'w') as savefile:
            json.dump(PlayerData.data, savefile, indent=4)
