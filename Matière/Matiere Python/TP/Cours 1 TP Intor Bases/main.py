class Soldier:

    def __init__(self, speed=0, health=100, armor=100):
        self.speed = speed
        self.health = health
        self.armor = armor

    def attack(self):
        print("Yes my lord !")

    def move(self, newspeed):
        print("yes, running at", newspeed)
        self.speed = newspeed    

    def get_speed(self):
        print(self.speed)


class Archer(Soldier):
    def __init__(self, speed=0, health=100, armor=100, arrows=30):
        super().__init__(speed, health, armor)
        self.arrows = arrows

    def reload(self):
        print("I'm reloading my lord")

    def getArmor(self):
        return self.armor

    def setArmor(self, newArmor):
        return self.armor