from statistics import geometric_mean
from units import Soldier, Vehicle
from config_data import SOLDIERS_COUNT, VEHICLES_COUNT


class Squad:

    def __init__(self, id, army_id):
        self.id = id
        self.army_id = army_id

        self.units = ([Soldier(i, self.id)
                       for i in range(SOLDIERS_COUNT)] +
                      [Vehicle(i, self.id)
                       for i in range(VEHICLES_COUNT)])

    @property
    def is_active(self):
        return len(self.units) > 0

    @property
    def strength(self):
        return sum([unit.strength
                    for unit in self.units])

    @property
    def attack_success(self):
        units_success = [unit.attack_success
                         for unit in self.units
                         if not unit.recharge]

        if units_success:
            return geometric_mean(units_success)
        else:
            return 0

    @property
    def damage(self):
        return sum([unit.damage
                    for unit in self.units
                    if not unit.recharge])

    def get_damage(self, points):
        dam = points / len(self.units)

        for unit in self.units:
            unit.get_damage(dam)
        self.units = [unit
                      for unit in self.units
                      if unit.is_active]

    def level_up(self):
        for unit in self.units:
            if not unit.recharge:
                unit.level_up()

    def set_recharge(self):
        for unit in self.units:
            if not unit.recharge:
                unit.set_recharge(0.000001)
