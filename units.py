import random
from statistics import geometric_mean
from input_data import *

class Soldier():

    health = 100
    experience = 0
    recharge = 0

    def __init__(self, id, squad_id):

        self.id = id
        self.squad_id = squad_id

    @property
    def is_active(self):

        return self.health > 0

    def attack_success(self):

        return 0.5 * (1 + self.health / 100) * random.randint(50 + self.experience, 100) / 100

    def damage(self):

        return 0.05 + self.experience / 100

    def get_damage(self, points):

        self.health = max(self.health - points, 0)

    def level_up(self):

        self.experience = min(self.experience + 1, 50)

#----------------------------------------
class Operator(Soldier):

    def __init__(self, id, vehicle_id):

        self.id = id
        self.vehicle_id = vehicle_id

#----------------------------------------
class Vehicle:

    health = 500
    recharge = 0

    def __init__(self, id, squad_id):

        self.id = id
        self.squad_id = squad_id

        self.operators = [Operator(i, self.id) for i in range(OPERATORS_COUNT)]

    @property
    def is_active(self):

        return any([op.is_active for op in self.operators]) and self.health > 0

    def strength(self):

        return sum([op.health for op in self.operators])

    def attack_success(self):

        op_success = [op.attack_success() for op in self.operators]

        return 0.5 * (1 + self.health / 100) * geometric_mean(op_success)

    def damage(self):

        op_expirience = [op.experience for op in self.operators]

        return 0.1 + sum(op_expirience) / 100

    def get_damage(self, points):

        self.health = max(self.health - 0.6 * points, 0)

        loser = random.choice(self.operators)

        for op in self.operators:
            if op is loser:
                op.get_damage(0.2 * points)
            else:
                op.get_damage(0.2 * points / (len(self.operators) - 1))

        self.operators = [op for op in self.operators if op.is_active]

    def level_up(self):

        for op in self.operators:
            op.level_up()