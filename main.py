import re
import json

with open("items.json") as f:
    items = json.load(f)

class Player:
    def __init__(self):
        self.health = 100
        self.inventory = []
    def addToInventory(self, item):
        self.inventory.append(item)
        print(f"+1 {item}")
    def displayInventory(self) -> str:
        invdisp = "Inventory:"
        for i in self.inventory:
            invdisp += f"\n   -{i}"
        return invdisp

class Item:
    def __init__(self, itemClass, name):
        self.itemClass = itemClass
        self.id = name
        self.iteminfo = items[self.itemClass][self.id]
        self.name = self.iteminfo["dsiplayName"]
        self.stats = self.iteminfo.remove
    def __str__(self) -> str:
        return f"{self.name} ({self.stats})"
    def getDescription(self):
        return items[self.itemClass][self.id]["description"]
    

class Sword(Item):
    def __init__(self, name):
        self.itemClass = "sword"
        self.damage = items[self.itemClass][self.name]["damage"]
        super().__init__(name, f"🗲 {self.damage}")

class Bow(Item):
    def __init__(self, name):
        self.itemClass = "bow"
        self.damage = items[self.itemClass][self.id]["damage"]
        self.reloadTime = items[self.itemClass][self.id]["reloadTime"]
        super().__init__(name, f"🗲 {self.damage} ⟳ {self.reloadTime}")
    
class Food(Item):
    def __init__(self, name, calories):
        super().__init__(name, f" {calories}")

class Game:
    def __init__(self, player):
        self.commandOptions = [["help", [""], "displays this message"],
                               ["move", ["dir"], "search around the area"],
                               ["inv", [""],"displays inventory"],
                               ["desc", ["item"], "shows more details about an item"],
                               ["get", ["item"], "puts item into your inventory"]
                               ]
        self.running = True
        self.availableCommands = self.commandOptions.copy()
        self.player = player
    def explore(self):
        pass
    def displayAvailableCommands(self):
        print(f"\tCommand{' '*13}Description")
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
        for i in enumerate(self.availableCommands):
            if command[0] == self.availableCommands[i[0]][0]:
                validity = True
        if len(command) == 1:
            return validity, command[0], None
        else:
            return validity, command[0], command[1:len(command)]
    def doCommand(self, command, args):
        if command == "help":
            self.displayAvailableCommands()
        if command == "inv":
            print(self.player.displayInventory())
        if command == "get":
            if not args:
                return None
            if args[0] == "sword":
                self.player.addToInventory(Sword("Iron Sword"))
            elif args[0] == "bow":
                self.player.addToInventory(Bow("King's Bow"))
        if command == "desc":
            for i in self.player.inventory:
                if i.id == args[0]:


if __name__ == "__main__":
    player = Player()
    game = Game(player)
    game.displayAvailableCommands()
    while game.running:
        command = game.prompt()
        validity, command, args = game.checkCommandValidity(command)
        if validity:
            game.doCommand(command, args)
        elif command:
            print(f"\"{command}\" is an invalid command. Type \"help\" for a list of commands.")