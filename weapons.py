import random

DEFAULT_CRITICAL_CHANCE = 0.25


class Weapon:
    damage_min = None
    damage_max = None
    hit_chance_scalar = 1
    critical_chance = DEFAULT_CRITICAL_CHANCE
    dodge_rate = 0
    symbol = None

    def calculate_damage(self):
        print(f"Charge an attack between {self.damage_min} and {self.damage_max}")
        while True:
            damage = input("").strip()
            if not damage.isnumeric():
                print("Invalid input. Try again.")
                continue
            damage = float(damage)
            if not (self.damage_min <= damage <= self.damage_max):
                print(f"Must be between {self.damage_min} and {self.damage_max}")
                continue
            break

        # damage = random.randint(self.damage_min, self.damage_max)
        hit_chance = min(1, ((100 - damage) / 100) * self.hit_chance_scalar)
        if random.random() > hit_chance:
            damage = 0  # miss
        elif random.random() <= self.critical_chance:
            print(f"Critical Strike!")
            damage *= 2
        return damage


class Sword(Weapon):
    hit_chance_scalar = 2
    damage_min = 15
    damage_max = 30
    symbol = "🗡"


class Bow(Weapon):
    hit_chance_scalar = 0.75
    dodge_rate = 0.25
    damage_min = 20
    damage_max = 40
    symbol = "🏹"


class MagicStaff(Weapon):
    symbol = "🌠"

    def calculate_damage(self):
        while True:
            choice = input("(R)anged - (M)alee - (H)eal").strip().upper()
            if choice == "R":
                self.damage_min = 5
                self.damage_max = 15
                self.dodge_rate = 0.25
                self.hit_chance_scalar = 0.75
                # calling the original calculate_damage function
                return super(MagicStaff, self).calculate_damage()
            elif choice == "M":
                self.damage_min = 10
                self.damage_max = 20
                self.dodge_rate = 0
                self.hit_chance_scalar = 1
                # calling the original calculate_damage function
                return super(MagicStaff, self).calculate_damage()
            elif choice == "H":
                self.dodge_rate = 0.25
                return -random.randint(20, 40)
            else:
                print("Sorry, try again")


weapons_dict = {
    "S": Sword(),
    "B": Bow(),
    "M": MagicStaff()
}
