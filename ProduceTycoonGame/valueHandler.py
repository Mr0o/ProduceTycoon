import pygame

class ValueHandler():
    s_playerValues = {
        "currency": 1000,
        "Watermelon-amount": 1,
        "Watermelon-price": 5,
        "Watermelon-sell-price": 5,
        "Banana-amount": 1,
        "Banana-price": 5,
        "Banana-sell-price": 5,
        "Apple-amount": 1,
        "Apple-price": 5,
        "Apple-sell-price": 5,
        "Tomato-amount": 1,
        "Tomato-price": 5,
        "Tomato-sell-price": 5
    }
    def __init__(self, playerValues: dict = {}):
        self.playerValues = playerValues
    
    def addValue(self, valueName: str, value: int):
        self.playerValues[valueName] += value

    def subtractValue(self, valueName: str, value: int):
        self.playerValues[valueName] -= value

    def setValue(self, valueName: str, value: int):
        self.playerValues[valueName] = value

    def setValue(self, valueName: str, value: str):
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
