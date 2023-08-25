import pygame

class ValueHandler():
    s_playerValues = {
        "currency": 1000,
        "watermelon-amount": 1,
        "watermelon-price": 5,
        "watermelon-sell-price": 5,
        "banana-amount": 1,
        "banana-price": 5,
        "banana-sell-price": 5,
        "apple-amount": 1,
        "apple-price": 5,
        "apple-sell-price": 5,
        "tomato-amount": 1,
        "tomato-price": 5,
        "tomato-sell-price": 5
    }
    def __init__(self, playerValues: dict = {}):
        self.playerValues = playerValues
    
    def addValue(self, valueName: str, value: int):
        self.playerValues[valueName] += value

    def subtractValue(self, valueName: str, value: int):
        self.playerValues[valueName] -= value

    def setValue(self, valueName: str, value: int):
        self.playerValues[valueName] = value
    
    def removeValue(self, valueName: str):
        del self.playerValues[valueName]

    def getValue(self, valueName: str):
        return self.playerValues[valueName]

    def hasValue(self, valueName: str):
        return valueName in self.playerValues

    @staticmethod
    def addStaticValue(valueName: str, value: int):
        ValueHandler.s_playerValues[valueName] += value
    
    @staticmethod
    def subtractStaticValue(valueName: str, value: int):
        ValueHandler.s_playerValues[valueName] -= value

    @staticmethod
    def setStaticValue(valueName: str, value: int):
        ValueHandler.s_playerValues[valueName] = value
    
    @staticmethod
    def removeStaticValue(valueName: str):
        del ValueHandler.s_playerValues[valueName]
    
    @staticmethod
    def getStaticValue(valueName: str):
        return ValueHandler.s_playerValues[valueName]

    @staticmethod
    def getStaticValues():
        return ValueHandler.s_playerValues

    @staticmethod
    def hasStaticValue(valueName: str):
        return valueName in ValueHandler.s_playerValues
