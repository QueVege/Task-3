from statistics import geometric_mean
from units import Soldier, Vehicle
from config_data import SOLDIERS_COUNT, VEHICLES_COUNT


class Squad:

    def __init__(self, id, army_id):
        self.id = id
        self.army_id = army_id

        self.soldiers = [Soldier(i, self.id)
                         for i in range(SOLDIERS_COUNT)]
        self.vehicles = [Vehicle(i, self.id)
                         for i in range(VEHICLES_COUNT)]

    @property
    def is_active(self):
        return len(self.soldiers) > 0 or len(self.vehicles) > 0

    @property
    def strength(self):
        return sum([sold.health
                    for sold in self.soldiers] +
                   [veh.strength
                    for veh in self.vehicles])

    @property
    def attack_success(self):
        units_success = [sold.attack_success
                         for sold in self.soldiers
                         if not sold.recharge] + \
                        [veh.attack_success
                         for veh in self.vehicles
                         if not veh.recharge]

        if units_success:
            return geometric_mean(units_success)
        else:
            return 0

    @property
    def damage(self):
        return sum([sold.damage
                    for sold in self.soldiers
                    if not sold.recharge] +
                   [veh.damage
                    for veh in self.vehicles
                    if not veh.recharge])

    def get_damage(self, points):
        dam = points / len(self.soldiers + self.vehicles)

        for sold in self.soldiers:
            sold.get_damage(dam)
        self.soldiers = [sold
                         for sold in self.soldiers
                         if sold.is_active]

        for veh in self.vehicles:
            veh.get_damage(dam)
        self.vehicles = [veh
                         for veh in self.vehicles
                         if veh.is_active]

    def level_up(self):
        for sold in self.soldiers:
            if not sold.recharge:
                sold.level_up()

        for veh in self.vehicles:
            if not veh.recharge:
                veh.level_up()

    def set_recharge(self):
        for sold in self.soldiers:
            if not sold.recharge:
                sold.set_recharge(0)

        for veh in self.vehicles:
            if not veh.recharge:
                veh.set_recharge(0.000001)
