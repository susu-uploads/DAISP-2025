import random

class Warrior:
    def __init__(self, name):
        self.health = 100
        self.name = name
        self.damage = 20
        print(f"{self.name} created with {self.health} hp")
    
    def __del__(self):
        print(f"До свидания, воин {self.name}!")
    
    def attack(self, enemy):
        enemy.health -= self.damage
        print(f"{self.name} attack {enemy.name}! {enemy.name}: {enemy.health} HP")
        return enemy.is_alive()
    
    def is_alive(self):
        return self.health > 0
    

def battle(warrior1: Warrior, warrior2: Warrior):
    print("=" * 30)
    print('='*9 + "Battle Start" + '='*9)
    print("=" * 30)

    print(f"{warrior1.name}: ({warrior1.health} hp) VS {warrior2.name}: ({warrior2.health}hp)")
    
    round_num = 1
    
    while True:
        print(f"\nRound {round_num}:")
        
        # Random attacker selection
        if random.choice([True, False]):
            # warrior1 attacks warrior2
            is_alive = warrior1.attack(warrior2)
            if not is_alive:
                print(f"\n{warrior1.name} winner!")
                break
        else:
            is_alive = warrior2.attack(warrior1)
            if not is_alive:
                print(f"\n{warrior2.name} winner!")
                break
        
        round_num += 1
    
    print("=" * 30)
    print('='*10 + "Battle End" + '='*10)
    print("=" * 30)


# Creating two instances of Warrior class
warrior_first = Warrior("Warrior First")
warrior_second = Warrior("Warrior Second")

# Conducting battle
battle(warrior_first, warrior_second)

print(f"\nResults:")
print(f"{warrior_first.name}: {warrior_first.health} hp")
print(f"{warrior_second.name}: {warrior_second.health} hp")

# Warrior First created with 100 hp
# Warrior Second created with 100 hp
# ==============================
# =========Battle Start=========
# ==============================
# Warrior First: (100 hp) VS Warrior Second: (100hp)
#
# Round 1:
# Warrior Second attack Warrior First! Warrior First: 80 HP
#
# Round 2:
# Warrior Second attack Warrior First! Warrior First: 60 HP
#
# Round 3:
# Warrior First attack Warrior Second! Warrior Second: 80 HP
#
# Round 4:
# Warrior First attack Warrior Second! Warrior Second: 60 HP
#
# Round 5:
# Warrior Second attack Warrior First! Warrior First: 40 HP
#
# Round 6:
# Warrior First attack Warrior Second! Warrior Second: 40 HP
#
# Round 7:
# Warrior Second attack Warrior First! Warrior First: 20 HP
#
# Round 8:
# Warrior First attack Warrior Second! Warrior Second: 20 HP
#
# Round 9:
# Warrior First attack Warrior Second! Warrior Second: 0 HP
#
# Warrior First winner!
# ==============================
# ==========Battle End==========
# ==============================
#
# Results:
# Warrior First: 20 hp
# Warrior Second: 0 hp
# До свидания, воин Warrior First!
# До свидания, воин Warrior Second!
