import pygame
import json

class Produce:
    data = {
        'Watermelon': {
            'name': "Watermelon",
            'amount': 0,
            'sell': 10,
            'buy': 5
        },
        'Bananas':{
            'name': "Bananas",
            'amount': 0,
            'sell': 20,
            'buy': 10
        }, 
        'Apples':{
            'name': "Apples",
            'amount': 0,
            'sell': 30,
            'buy': 15
        }, 
        'Tomatoes': {
            'name': "Tomatoes",
            'amount': 0,
            'sell': 40,
            'buy': 20
        }
    }

    @staticmethod
    def load():
        try:
            # load the data from the file
            with open('./Resources/Playerdata/produce.json', 'r') as loadfile:
                Produce.data = json.load(loadfile)
        except FileNotFoundError:
            # if the file doesn't exist, create it using the default data
            Produce.save()

    @staticmethod
    def save(filePath):
        with open(filePath + "produce.json", 'w') as savefile:
            json.dump(Produce.data, savefile, indent=4)