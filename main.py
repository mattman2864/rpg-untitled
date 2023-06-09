import re
import json
import random
from termcolor import colored, cprint
import keyboard

with open("items.json") as f:
    items = json.load(f)
with open("enemies.json") as f:
    enemies = json.load(f)

class Enemy:
    def __init__(self, name):
        self.id = name
        self.info = enemies[self.id]
        self.name = self.info["displayName"]
        self.health = self.info["health"]
        self.damage = self.info["damage"]
    def __str__(self):
        return self.name
    def displayBattleStats(self):
        return f"{self.name}\n\tHealth: {colored(self.health, 'green')}\n\tDamage: {colored(self.damage, 'red')}"
    def attack(self):
        return 10
        


class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.hunger = 100
        self.defense = 0
        self.gold = 0
        self.inventory = []
        self.armorSlots = {"helmet":None, "chest":None, "legs":None, "boots":None}
        self.weaponSlots = {"sword":None, "bow":None}
    def __str__(self):
        return self.name
    def addToInventory(self, item):
        self.inventory.append(item)
        print(f"+1 {item}")
    def removeFromInventory(self, item):
        for i in self.inventory:
            if i.id == item:
                self.inventory.remove(i)
                print(f"-1 {i.name}")
                break
    def displayInventory(self) -> str:
        inventoryDisplay = "Inventory:"
        for i in self.inventory:
            inventoryDisplay += f"\n   -{i}"
        return inventoryDisplay
    def equipArmor(self, item):
        for i in self.inventory:
            if i.id == item and i.itemClass in ["helmet", "chest", "legs", "boots"]:
                if self.armorSlots[i.itemClass]:
                    self.addToInventory(self.armorSlots[i.itemClass])
                self.armorSlots[i.itemClass] = i
                self.defense += i.defense
                self.inventory.remove(i)
                return i.name
    def equipWeapon(self, item):
        for i in self.inventory:
            if i.id == item and i.itemClass in ["sword", "bow"]:
                if self.weaponSlots[i.itemClass]:
                    self.addToInventory(self.weaponSlots[i.itemClass])
                self.weaponSlots[i.itemClass] = i
                self.inventory.remove(i)
                return i.name
    def equip(self, item):
        for i in self.inventory:
            if i.id == item:
                if i.itemClass in ["sword", "bow"]:
                    print(f"Equipped {self.equipWeapon(item)}")
                    break
                elif i.itemClass in ["helmet", "chest", "legs", "boots"]:
                    print(f"Equipped {self.equipArmor(item)}")
                    break
    def displayEquipment(self):
        weaponIter = self.weaponSlots.copy()
        weaponIter.update({"":"",None:""})
        print("\t{:<30}{}".format("Armor", "Weapons"))
        for armor, weapon in zip(self.armorSlots, weaponIter):
            if weapon:
                print("\t{:<30}{}".format(f"{armor}: {self.armorSlots[armor]}", f"{weapon}: {weaponIter[weapon]}"))
            else:
                print("\t{:<30}{}".format(f"{armor}: {self.armorSlots[armor]}", ""))
    def displayStats(self):
        return f"{self}\n\tHealth:{colored(self.health, 'green')}\n\tHunger:{colored(self.hunger, 166)}\n\tGold:{colored(self.gold, 'yellow')}\n\tDefense:{colored(self.defense, 'blue')}"
    def addGold(self, amount):
        self.gold += amount
        print(f"+{amount} Gold")
    def attack(self, weaponType):
        return self.weaponSlots[weaponType].damage
    def displayBattleStats(self):
        return f"Player {self.name}\n\tHealth:{colored(self.health, 'green')}\n\tDefense:{colored(self.defense, 'blue')}\n\tSword: {self.weaponSlots['sword']}\n\tBow: {self.weaponSlots['bow']}"
    def findItem(self, item):
        for i in self.inventory:
            if i.id == item:
                return i
    def findType(self, type):
        if type == "food":
            for i in self.inventory:
                if i.itemClass == "food":
                    return True
    def updateStats(self):
        if self.hunger >= 85 and self.health != 100:
            healthAdd = min(max(round(0.1*self.health), 1), 100-self.health)
            print(f"+{healthAdd} Health")
            self.health += healthAdd
        if self.hunger == 0:
            healthSubtract = min(max(round(0.1*self.health), 1), self.health)
            print(f"{colored('-'+healthSubtract+' '+'Health', 'green')} (Starving!)")
            self.health -= healthSubtract

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
    def __init__(self, player, map):
        self.commandOptions = [["help", [""], "displays this message"],
                               ["key", [""], "gives a key for iconds on map"],
                               ["n", [""], "move north"],
                               ["e", [""], "move east"],
                               ["s", [""], "move south"],
                               ["w", [""], "move west"],
                               ["inv", [""],"displays inventory"],
                               ["desc", ["item"], "shows more details about an item"],
                               ["get", ["item"], "puts item into your inventory"],
                               ["equip", ["item"], "equip armor or weapon - will replace gear in slot"],
                               ["gear", [""], "displays equipment"],
                               ["stats", [""], "displays player stats"],
                               ["drop", ["item"], "removes item from inventory"],
                               ["eat", ["food item"], "eats a given item to replenish hunger"]
                               ]
        self.running = True
        self.availableCommands = self.commandOptions.copy()
        self.player = player
        self.map = map
    def explore(self):
        pass
    def displayAvailableCommands(self):
        print(f"\tCommand{' '*13}Description")
        for i in self.availableCommands:
            args = [f"<{x}>" for x in i[1] if x]
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
                self.player.addToInventory([Sword("iron_sword"), Sword("small_dagger"), Sword("rapier")][random.randint(0,2)])
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
            elif not found:
                print("You must give an item to find the description of")
        if command == "equip":
            if not args:
                print("You must provide an item to equip")
            else:
                self.player.equip(args[0])
        if command == "gear":
            self.player.displayEquipment()
        if command == "stats":
            print(self.player.displayStats())
        if command in ["n", "e", "s", "w"]:
            if self.player.hunger >= 4:
                self.map.moveChar(command)
                self.player.hunger -= 4
                print("-4 Hunger")
                self.player.updateStats()
            else:
                print(f"You only have {self.player.hunger} hunger.")
        if command == "key":
            for (i, tile) in enumerate(self.map.tiles):
                if not i == "  ":
                    print("{}\t{:<10}".format(tile, self.map.tileKeys[i]))
        if command == "drop":
            self.player.removeFromInventory(args[0])
        if command == "eat" and args:
            if not self.player.findType("food"):
                print(f"You have no food!")
            elif not player.findItem(args[0]):
                print(f"You do not have {args[0]} in your inventory!")
            else:
                replenishment = min(self.player.findItem(args[0]).calories, 100-self.player.hunger)
                self.player.hunger += replenishment
                print(f"Ate {self.player.findItem(args[0])}. You now have {self.player.hunger}/100 hunger.")
                self.player.removeFromInventory(args[0])
    def openChest(self):
        print("You found a chest!")
        chestLootTable = ["gold", Sword("rapier"), Sword("small_dagger"), Bow("wooden_bow")]
        chestLootTableDist = [10, 10, 10, 10]
        loot = random.choices(chestLootTable, weights=chestLootTableDist)[0]
        if loot == "gold":
            self.player.addGold(random.randint(1, 100))
        else:
            self.player.addToInventory(loot)
    def battle(self, enemy):
        attackOptions = ["flee", "slash", "shoot"]
        if not self.player.weaponSlots["sword"]:
            attackOptions.remove("slash")
        if not self.player.weaponSlots["bow"]:
            attackOptions.remove("shoot")
        print(f"You have entered a battle against {enemy}!")
        print(self.player.displayBattleStats())
        print(enemy.displayBattleStats())
        battle = True
        while battle:
            if self.player.health <= 0:
                print(f"You have been defeated by {enemy}!")
                battle = False
                game.running = False
                break
            elif enemy.health <= 0:
                print(f"You have defeated {enemy}!")
                self.map.removeObject(self.map.charPos)
                battle = False
                break
            print("Attacks:")
            for i in attackOptions:
                print("\t"+i)
            attack = input(">>> ")
            while attack not in attackOptions:
                attack = input(">>> ")
            if attack == "flee":
                battle = False
                print("You have successfully run away!")
                break
            if attack == "slash":
                damage = min(self.player.weaponSlots["sword"].damage, enemy.health)
                enemy.health -= damage
                print(f"You slashed for {damage} damage!")
            if attack == "shoot":
                damage = min(self.player.weaponSlots["bow"].damage, enemy.health)
                enemy.health -= damage
                print(f"You shot for {damage} damage!")
            enemyDamage = min(enemy.damage, self.player.health)
            print(f"{enemy} attacked for {enemyDamage} damage!")
            self.player.health -= enemyDamage

            print(self.player.displayBattleStats())
            print(enemy.displayBattleStats())

class Map:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.map = [["" for x in range(self.w)] for y in range(self.h)]
        self.tiles =             ["  ", "Ro", "Ca", colored("Ch", "yellow"), colored("En", "red")]
        self.tileKeys =          ["  ", "Rock", "Cave", "Chest", "Enemy"]
        self.tileDistributions = [75, 10, 10, 2, 3]

        self.charPos = [0, 0]

        for i in enumerate(self.map):
            for j in enumerate(i[1]):
                self.map[i[0]][j[0]] = random.choices(self.tiles, weights=self.tileDistributions)[0]

    def printMap(self):
        print("╔" + "═"*(4*self.w) + "╗")
        for i in enumerate(self.map):
            print("║", end="")
            for j in enumerate(i[1]):
                if [i[0], j[0]] == self.charPos:
                    cprint(" "+self.map[i[0]][j[0]]+" ", "white", "on_green", end="")
                else:      
                    print(" "+self.map[i[0]][j[0]]+" ", end="")
            print("║")
        print("╚" + "═"*(4*self.w) + "╝")
    def moveChar(self, dir):
        if dir == "n" and self.charPos[0] > 0:
            self.charPos[0] -= 1   
        elif dir == "s" and self.charPos[0] < self.h-1:
            self.charPos[0] += 1 
        elif dir == "e" and self.charPos[1] < self.w-1:
            self.charPos[1] += 1 
        elif dir == "w" and self.charPos[1] > 0:
            self.charPos[1] -= 1 
        self.printMap()    
    def checkSquare(self, square):
        return self.map[square[0]][square[1]]
    def checkForEnemy(self):
        if self.checkSquare(self.charPos) == colored("En", "red"):
            game.battle(Enemy("zombie"))
        return False
    def removeObject(self, square):
        self.map[square[0]][square[1]] = "  "
        print(self.map[square[0]][square[1]])
    def checkForChest(self):
        if self.checkSquare(self.charPos) == colored("Ch", "yellow"):
            if input("Would you like to open the chest? ") in ["yes", "y"]:
                self.removeObject(self.charPos)
                game.openChest()
        return False

if __name__ == "__main__":
    print("""
    ____        __          __           _____                  _         
   / __ )__  __/ /_ __     / /_ ___     / ___/__  _____ __   __(_)   __ __ 
  / __  / / / / __/ _ \   / __/ __ \    \__ \/ / / / __/| | / / | | / / _ \\
 / /_/ / /_/ / /_/  __/  / /_/ /_/ /   ___/ / /_/ / /   | |/ / /| |/ /  __/
/_____/\__, /\__/\___/   \__/\____/   /____/\__,_/_/    |___/_/ |___/\___/ 
      /____/                                                               
      """)
    print("What is your name?")
    player = Player(input(">>> "))
    print("World size:\n\t-Small (10x10)\n\t-Medium (15x15)\n\t-Large (20x20)")
    while 1:
        size = input(">>> ").lower()
        if size == "small":
            map = Map(10, 10)
            break
        elif size == "medium":
            map = Map(15, 15)
            break
        elif size == "large":
            map = Map(20, 20)
            break
        else:
            print('You must provide a valid world size ("small", "medium", or "large")')
    game = Game(player, map)
    game.displayAvailableCommands()
    game.map.printMap()
    while game.running:
        game.map.checkForChest()
        game.map.checkForEnemy()
        if not game.running:
            break
        command = game.prompt()
        validity, command, args = game.checkCommandValidity(command)
        if validity:
            game.doCommand(command, args)
        elif command:
            print(f"\"{command}\" is an invalid command. Type \"help\" for a list of commands.")
    cprint("GAME OVER", "red")