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
    def load(filePath):
        try:
            with open(filePath + "produce.json", 'r') as savefile:
                Produce.data = json.load(savefile)
        except FileNotFoundError:
            # if the file is not found then create a json file with default data
            Produce.save(filePath)

    @staticmethod
    def save(filePath):
        with open(filePath + "produce.json", 'w') as savefile:
            json.dump(Produce.data, savefile, indent=4)