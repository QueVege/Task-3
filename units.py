from threading import Timer
from random import Random
from statistics import geometric_mean
from config_data import seed, SOLDIERS_HP, VEHICLES_HP, OPERATORS_COUNT

R = Random(seed)


class Unit:
    def __init__(self, id, squad_id, hp):
        self.id = id
        self.squad_id = squad_id
        self.health = hp
        self.recharge = False

    def drop_recharge(self):
        self.recharge = False

    def set_recharge(self, recharge_time):
        self.recharge = True
        t = Timer(recharge_time, self.drop_recharge)
        t.start()


class Soldier(Unit):

    def __init__(self, id, squad_id):
        self.experience = 0
        super().__init__(id, squad_id, SOLDIERS_HP)

    @property
    def is_active(self):
        return self.health > 0

    @property
    def attack_success(self):
        return 0.5 * (1 + self.health / 100) * \
              R.randint(50 + self.experience, 100) / 100

    @property
    def damage(self):
        return 0.05 + self.experience / 100

    def get_damage(self, points):
        self.health = max(self.health - points, 0)

    def level_up(self):
        self.experience = min(self.experience + 1, 50)


class Operator(Soldier):

    def __init__(self, id, vehicle_id, squad_id):
        self.vehicle_id = vehicle_id
        super().__init__(id, squad_id)


class Vehicle(Unit):

    def __init__(self, id, squad_id):
        self.operators = [Operator(i, id, squad_id)
                          for i in range(OPERATORS_COUNT)]
        super().__init__(id, squad_id, VEHICLES_HP)

    @property
    def is_active(self):
        return len(self.operators) > 0 and self.health > 0

    @property
    def strength(self):
        return sum([op.health for op in self.operators]) + self.health

    @property
    def attack_success(self):
        op_success = [op.attack_success for op in self.operators]
        return 0.5 * (1 + self.health / 100) * geometric_mean(op_success)

    @property
    def damage(self):
        op_expirience = [op.experience for op in self.operators]
        return 0.1 + sum(op_expirience) / 100

    def get_damage(self, points):
        self.health = max(self.health - 0.6 * points, 0)
        loser = R.choice(self.operators)

        for op in self.operators:
            if op is loser:
                op.get_damage(0.2 * points)
            else:
                op.get_damage(0.2 * points / (len(self.operators) - 1))

        self.operators = [op for op in self.operators if op.is_active]

    def level_up(self):
        for op in self.operators:
            op.level_up()
