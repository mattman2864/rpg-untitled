import json

itemsjsonfile = open("items.json")
itemsjson = json.load(itemsjsonfile)

class Item: # Represents Item that can go into inventory
    def __init__(self, name):
        self.name = name
    def __str__(self) -> str:
        return self.name

class Weapon(Item): # Represents Weapon that can go into inventory or weapon slot
    def __init__(self, name, damage, reloadTime):
        super().__init__(name)
        self.damage = damage
        self.reloadTime = reloadTime

class Sword(Weapon):
    def __init__(self, name, damage, reloadTime):
        super().__init__(name, damage, reloadTime)

class Bow(Weapon): # Represents
    def __init__(self, name, damage, reloadTime, description):
        super().__init__(name, damage, reloadTime)
        self.description = description
    def getDescription(self) -> str:
        return f'''{self.name}\n\tDamage: {self.damage}\n\tReload Time: {self.reloadTime}\n\t{self.description}'''
    

class Shield(Weapon):
    def __init__(self, name, defense):
        super().__init__(name, defense, 1)

class Character: # Character class describes entitities
    def __init__(self, name: str, health: int, armor: dict, weapons: dict):
        self.name = name
        self.health = health
        self.armor = armor
        self.weapons = weapons
    def getHealth(self):
        return self.health
    def getName(self):
        return self.name
    def getArmor(self, display: bool):
        if display:
            print(f"{self.name}'s Armor")
            for i in ["head", "chest", "legs"]:
                if self.armor[i]:
                    print(f"\t{i}: {self.armor[i]}")
                else:
                    print(f"\t{i}: Empty")
        else:
            return self.armor
    def getWeapons(self, display: bool):
        if display:
            print(f"{self.name}'s Weapons")
            for i in [Sword, Bow, Shield]:
                if self.weapons[i]:
                    print(f"\t{i}: {self.weapons[i]}")
                else:
                    print(f"\t{i}: Empty")
        else:
            return self.weapons
        
class Player(Character): # Represents playable character
    def __init__(self, name: str):
        super().__init__(name, 
                         100,
                         {"head":None, "chest":None, "legs":None, }, 
                         {Sword:None, Bow:None, Shield:None})
        self.inventory = []
    def getInventory(self, display: bool):
        if display:
            print(f"{self.name}'s Inventory")
            for item in list(self.inventory):
                print(f"\t-{str(item)}")
    def pickUpItem(self, item: Item):
        if issubclass(type(item), Item):
            self.inventory.append(item)
    def addToWeaponsSlot(self, item: Item):
        if item in self.inventory:
            self.weapons[type(item)] = item
            self.inventory.remove(item)
    def addToArmorSlot(self, item: Item):
        if item in self.inventory:
            self.armor.append(item)
            self.inventory.remove(item)
print("What is your name?")
inputname = input(">>> ")
player = Player(inputname)
player.pickUpItem(TravelersBow())
player.pickUpItem(TravelersBow())
player.pickUpItem(TravelersBow())
player.pickUpItem(Sword("Traveler's Sword", 10, 1))
player.getInventory(True)