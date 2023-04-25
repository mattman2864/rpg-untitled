import re
import json

with open("items.json") as f:
    items = json.load(f)

class Entity:
    def __init__(self, health, defense):
        pass

class Player:
    def __init__(self):
        self.health = 100
        self.hunger = 100
        self.defense = 0
        self.inventory = []
        self.armorSlots = {"helmet":None, "chest":None, "legs":None, "boots":None}
        self.weaponSlots = {"sword":None, "bow":None}
    def addToInventory(self, item):
        self.inventory.append(item)
        print(f"+1 {item}")
    def displayInventory(self) -> str:
        inventoryDisplay = "Inventory:"
        for i in self.inventory:
            inventoryDisplay += f"\n   -{i}"
        return inventoryDisplay
    def equipArmor(self, item):
        found = False
        for i in self.inventory:
            if i.id == item and i.itemClass in ["helmet", "chest", "legs", "boots"]:
                found = True
                self.armorSlots[i.itemClass] = i
                self.inventory.remove(i)
    def equipWeapon(self, item):
        found = False
        for i in self.inventory:
            if i.id == item and i.itemClass in ["sword", "bow"]:
                found = True
                self.weaponSlots[i.itemClass] = i
                self.inventory.remove(i)  
    def equip(self, item):
        for i in self.inventory:
            if i.id == item:
                if i.itemClass in ["sword", "bow"]:
                    self.equipWeapon(item)
                if i.itemClass in ["helmet", "chest", "legs", "boots"]:
                    self.equipArmor(item)
    def displayEquipment(self):
        weaponIter = self.weaponSlots.copy()
        weaponIter.update({"":"",None:""})
        print("\t{:<30}{}".format("Armor", "Weapons"))
        for armor, weapon in zip(self.armorSlots, weaponIter):
            if weapon:
                print("\t{:<30}{}".format(f"{armor}: {self.armorSlots[armor]}", f"{weapon}: {weaponIter[weapon]}"))
            else:
                print("\t{:<30}{}".format(f"{armor}: {self.armorSlots[armor]}", ""))


class Item:
    def __init__(self, itemClass, name):
        self.itemClass = itemClass
        self.id = name
        self.iteminfo = items[self.itemClass][self.id]
        self.name = self.iteminfo["displayName"]
        self.description = items[self.itemClass][self.id]["description"]
        self.stats = {}
        for i in self.iteminfo:
            if not i in ["description", "displayName"]:
                self.stats[i] = self.iteminfo[i]
        self.displaystats = ""
        for i in self.stats:
            self.displaystats += f"{i}: {self.stats[i]} "

    def __str__(self) -> str:
        return f"{self.name}"
    def getDescription(self):
        details = f"{self.name}"
        for i in self.stats:
            if not i in ["description", "displayName"]:
                details += f"\n\t{i}: {self.stats[i]}"
        details += f"\n\t{self.description}"
        return details
    
class Sword(Item):
    def __init__(self, name):
        self.itemClass = "sword"
        self.id = name
        self.damage = items[self.itemClass][self.id]["damage"]
        super().__init__(self.itemClass, self.id)

class Bow(Item):
    def __init__(self, name):
        self.itemClass = "bow"
        self.id = name
        self.damage = items[self.itemClass][self.id]["damage"]
        self.reloadTime = items[self.itemClass][self.id]["reloadTime"]
        super().__init__(self.itemClass, name)

class Helmet(Item):
    def __init__(self, name):
        self.itemClass = "helmet"
        self.id = name
        self.defense = items[self.itemClass][self.id]["defense"]
        super().__init__(self.itemClass, name)

class Chestplate(Item):
    def __init__(self, name):
        self.itemClass = "chest"
        self.id = name
        self.defense = items[self.itemClass][self.id]["defense"]
        super().__init__(self.itemClass, name)

class Leggings(Item):
    def __init__(self, name):
        self.itemClass = "legs"
        self.id = name
        self.defense = items[self.itemClass][self.id]["defense"]
        super().__init__(self.itemClass, name)

class Boots(Item):
    def __init__(self, name):
        self.itemClass = "boots"
        self.id = name
        self.defense = items[self.itemClass][self.id]["defense"]
        super().__init__(self.itemClass, name)
    
class Food(Item):
    def __init__(self, name):
        self.itemClass = "food"
        self.id = name
        self.calories = items[self.itemClass][self.id]["calories"]
        super().__init__(self.itemClass, self.id)

class Game:
    def __init__(self, player):
        self.commandOptions = [["help", [""], "displays this message"],
                               ["move", ["dir"], "search around the area"],
                               ["inv", [""],"displays inventory"],
                               ["desc", ["item"], "shows more details about an item"],
                               ["get", ["item"], "puts item into your inventory"],
                               ["equip", ["item"], "equip weapon or armor piece - will replace armor in slot"],
                               ["gear", [""], "displays equipment"]
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
                self.player.addToInventory(Sword("iron_sword"))
            elif args[0] == "bow":
                self.player.addToInventory(Bow("soldiers_bow"))
            elif args[0] == "food":
                self.player.addToInventory(Food("apple"))
            elif args[0] == "helmet":
                self.player.addToInventory(Helmet("iron_helm"))
            elif args[0] == "chest":
                self.player.addToInventory(Chestplate("iron_chestplate"))
            elif args[0] == "legs":
                self.player.addToInventory(Leggings("iron_leggings"))
            elif args[0] == "boots":
                self.player.addToInventory(Boots("iron_boots"))
        if command == "desc":
            found = False
            for i in self.player.inventory:
                if i.id == args[0]:
                    print(i.getDescription())
                    found = True
            if (not found) and args:
                print(f"You do not have {args[0]} in your inventory.")
            else:
                print("You must give an item to find the description of")
        if command == "equip":
            self.player.equip(args[0])
        if command == "gear":
            self.player.displayEquipment()

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