import re

class Player:
    '''main player class that holds inventory'''
    def __init__(self):
        self.health = 100
        self.inventory = []
    def addToInventory(self, item):
        '''takes item class and adds to self.inventory'''
        self.inventory += item
    def displayInventory(self) -> str:
        '''returns a string list of inventory'''
        invdisp = "Inventory:"
        for i in self.inventory:
            invdisp += f"\n   -{i}"
        return invdisp

class Item:
    def __init__(self, name, stats):
        self.name = name
        self.stats = stats
    def __str__(self) -> str:
        return f"{self.name} ({self.stats})"

class Sword(Item):
    def __init__(self, name, damage):
        super().__init__(name, f"🗲 {damage}")
        self.damage = damage

class Bow(Item):
    def __init__(self, name, damage, reloadSpeed):
        super().__init__(name, f"🗲 {damage} ⟳ {reloadSpeed}")
        self.damage = damage
        self.reloadSpeed = reloadSpeed
    
class Food(Item):
    def __init__(self, name, calories):
        super().__init__(name, f" {calories}")

class Game:
    def __init__(self):
        self.commandOptions = [["help", [""], "displays this message"],
                               ["move", ["dir"], "search around the area"],
                               ["inv", [""],"displays inventory"],
                               ["desc", ["item"], "shows more details about an item"],
                               ]
        self.running = True
        self.availableCommands = self.commandOptions.copy()
    def explore(self):
        pass
    def displayAvailableCommands(self):
        for i in self.availableCommands:
            args = [f"<{j}>" for j in i[1] if j]
            argsformatted = ""
            for j in args:
                argsformatted += j + " "
            totalcmd = str(i[0]+" "+argsformatted)
            print("\t{:<20}{}".format(totalcmd, i[2]))
    def prompt(self):
        return input(">>> ")
    def checkCommandValidity(self, command):
        command = re.split('\s+', command)
        validity = False
        for i in enumerate(self.commandOptions):
            if not command[0] == self.commandOptions[i][0]:
                validity = False
            # else:
            #     if len(command) - 1 == len(self.commandOptions[i][1]):
            #         validity = True
            #         break
        return validity

if __name__ == "__main__":
    player = Player()
    game = Game()
    game.displayAvailableCommands()
    while game.running:
        print(game.checkCommandValidity(game.prompt()))
