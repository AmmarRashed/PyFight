import random

from weapons import weapons_dict
from text_utils import colorify, valid_colors, print_winner


class Player:
    def __init__(self, name, color, weapon, hp_potions=3):
        self.name = name
        self.color = color
        self.hp = 100
        self.weapon = weapon
        self.hp_potions = hp_potions

    def drink_hp(self):
        if self.hp_potions > 0:
            self.hp_potions -= 1
            self.hp = min(self.hp + 40, 100)  # can't exceed 100 hp

    def attack(self, other):
        print(f"{self.name} attacks!")
        damage = self.weapon.calculate_damage()
        if damage < 0:  # healing
            self.hp = min(self.hp - damage, 100)
        elif random.random() <= other.weapon.dodge_rate:
            print(f"{other.name} Dodged!")
        else:
            print(f"{self.name} deals {damage} damage to {other.name}")
            other.hp -= damage

    def print_hp(self):
        sticks = "|" * (int(self.hp / 2))
        return colorify(f"HP[{self.hp}]:{sticks}", self.color)

    def print_name(self):
        return colorify(f"{self.name} ({self.weapon.symbol})", self.color)


class Game:
    def __init__(self):
        self.player1 = Game.create_player()

        self.player2 = Game.create_player(
            forbidden_name=self.player1.name,
            forbidden_color=self.player1.color
        )

        self.current_player = random.choice([self.player1, self.player2])
        self.winner = None

    def print_players_hp(self):
        print(f"{self.player1.print_name()}\t{self.player2.print_name()}".expandtabs(70))
        print(f"{self.player1.print_hp()}\t{self.player2.print_hp()}".expandtabs(70))

    def next_player(self):
        return self.player2 if self.current_player == self.player1 else self.player1

    def turn(self):
        self.print_players_hp()
        print(f"{self.current_player.name}'s Turn!")
        next_player = self.next_player()
        while True:
            choice = input(
                f"(A)ttack, "
                f"(HP) to drink a potion-available "
                f"({self.current_player.hp_potions})"
            ).strip().upper()
            if choice == "A":
                self.current_player.attack(next_player)
                break
            elif choice == "HP":
                self.current_player.drink_hp()
                break
            else:
                print("Sorry, try again.")

        # switch players
        self.current_player = next_player
        self.check_winner()

    def check_winner(self):
        if self.player1.hp <= 0:
            self.winner = self.player2
        elif self.player2.hp <= 0:
            self.winner = self.player1

    def play(self):
        while self.winner is None:
            self.turn()
        self.print_players_hp()
        print_winner(self.winner.name)

    @staticmethod
    def create_player(forbidden_name=None, forbidden_color=None):
        while True:
            name = input("Name: ").strip()
            if name == forbidden_name:
                print("Name already taken")
                continue
            break

        while True:
            color = input("Color (R)ed, (Y)ellow, (B)lue, (G)reen: ").strip().upper()
            if color not in ["R", "Y", "B", "G"]:
                print("Invalid color, try again.")
                continue
            color = valid_colors[color]
            if color == forbidden_color:
                print("Color already taken")
                continue
            break
        while True:
            weapon_name = input("(S)word🗡, (B)ow🏹, (M)agic staff🌠").strip().upper()
            if weapon_name in weapons_dict:
                weapon = weapons_dict[weapon_name]
                hp_potions = 1 if weapon_name == "M" else 3
                return Player(name=name, color=color, weapon=weapon, hp_potions=hp_potions)
            print("Invalid weapon, try again")
