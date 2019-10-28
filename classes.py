import random
from statistics import geometric_mean

SQUADS_NUM = 2
SOLDIERS_NUM = 5
VEHICLES_NUM = 2
OPERATORS_NUM = 3

#----------------------------------------
class Soldier():

    health = 100
    experience = 0
    recharge = 0

    def __init__(self, id_num, squad_id):

        self.id_num = id_num
        self.squad_id = squad_id

    def attack_success(self):

        return 0.5 * (1 + self.health / 100) * random.randint(50 + self.experience, 100) / 100

    def damage(self):

        return 0.05 + self.experience / 100

    def is_active(self):

        if self.health > 0:
            return True
        else:
            return False

    def get_damage(self, points):

        if self.health > points:
            self.health -= points
        else:
            self.health = 0

    def level_up(self):

        if self.experience < 50:
            self.experience += 1

#----------------------------------------
class Operator(Soldier):

    def __init__(self, id_num, vehicle_id):

        self.id_num = id_num
        self.vehicle_id = vehicle_id

#----------------------------------------
class Vehicle():

    health = 200
    recharge = 0

    def __init__(self, id_num, squad_id):

        self.id_num = id_num
        self.squad_id = squad_id

        self.operators = []
        for i in range(OPERATORS_NUM):
            self.operators.append(Operator(i, self.id_num))


    def active_operators(self):

        ids = []

        for i in range(OPERATORS_NUM):
            if self.operators[i].is_active():
                ids.append(self.operators[i].id_num)

        return ids

    def strength(self):

        total_health = 0

        for i in self.active_operators():
            total_health += self.operators[i].health

        return total_health + self.health

    def attack_success(self):

        op_success = []
        for i in self.active_operators():
            op_success.append(self.operators[i].attack_success())

        return 0.5 * (1 + self.health / 100) * geometric_mean(op_success)

    def damage(self):

        op_expirience = []
        for i in self.active_operators():
            op_expirience.append(self.operators[i].experience)

        return 0.1 + sum(op_expirience) / 100

    def is_active(self):

        if self.active_operators() and self.health > 0:
            return True
        else:
            return False

    def get_damage(self, points):

        if self.health > points * 0.6:
            self.health -= points * 0.6
        else:
            self.health = 0

        ids = self.active_operators().copy()

        loser_id = random.choice(ids)

        self.operators[loser_id].get_damage(points * 0.2)

        ids.remove(loser_id)

        for i in ids:
            self.operators[i].get_damage(points * 0.2 / len(ids))

    def level_up(self):

        for i in self.active_operators():
            self.operators[i].level_up()

#----------------------------------------
class Squad():

    def __init__(self, id_num, army_id):

        self.id_num = id_num
        self.army_id = army_id

        self.soldiers = []
        for i in range(SOLDIERS_NUM):
            self.soldiers.append(Soldier(i, self.id_num))

        self.vehicles = []
        for i in range(VEHICLES_NUM):
            self.vehicles.append(Vehicle(i, self.id_num))

    
    def active_soldiers(self):
        
        ids = []

        for i in range(SOLDIERS_NUM):
            if self.soldiers[i].is_active():
                ids.append(self.soldiers[i].id_num)

        return ids

    def active_vehicles(self):
        
        ids = []

        for i in range(VEHICLES_NUM):
            if self.vehicles[i].is_active():
                ids.append(self.vehicles[i].id_num)

        return ids

    def strength(self):

        total_health = 0

        for i in self.active_soldiers():
            total_health += self.soldiers[i].health

        for i in self.active_vehicles():
            total_health += self.vehicles[i].strength()

        return total_health

    def attack_success(self):

        units_success = []

        for i in self.active_soldiers():
            if not self.soldiers[i].recharge:
                units_success.append(self.soldiers[i].attack_success())

        for i in self.active_vehicles():
            if not self.vehicles[i].recharge:
                units_success.append(self.vehicles[i].attack_success())
        
        if not units_success:
        	return 0
        else:
            return geometric_mean(units_success)

    def damage(self):

        total_damage = 0
        
        for i in self.active_soldiers():
            if not self.soldiers[i].recharge:
                total_damage += self.soldiers[i].damage()

        for i in self.active_vehicles():
            if not self.vehicles[i].recharge:
                total_damage += self.vehicles[i].damage()

        return total_damage

    def is_active(self):

        if self.active_soldiers() or self.active_vehicles():
            return True
        else:
            return False

    def get_damage(self, points):

        total_numb = len(self.active_soldiers()) + len(self.active_vehicles())

        for i in self.active_soldiers():
            self.soldiers[i].get_damage(points / total_numb)

        for i in self.active_vehicles():
            self.vehicles[i].get_damage(points / total_numb)

    def level_up(self):

        for i in self.active_soldiers():
            if not self.soldiers[i].recharge:
                self.soldiers[i].level_up()

        for i in self.active_vehicles():
            if not self.vehicles[i].recharge:
                self.vehicles[i].level_up()

    def recharge(self, flag):

        if flag:
            for i in self.active_soldiers():
                if not self.soldiers[i].recharge:
                    self.soldiers[i].recharge += 2

            for i in self.active_vehicles():
                if not self.vehicles[i].recharge:
                    self.vehicles[i].recharge += 3

        else:
            for i in self.active_soldiers():
                if self.soldiers[i].recharge:
                    self.soldiers[i].recharge -= 1

            for i in self.active_vehicles():
                if self.vehicles[i].recharge:
                    self.vehicles[i].recharge -= 1

#----------------------------------------
class Army:

    def __init__(self, id_num):

        self.id_num = id_num

        self.squads = []
        for i in range(SQUADS_NUM):
            self.squads.append(Squad(i, self.id_num))

    def active_squads(self):

        ids = []

        for i in range(SQUADS_NUM):
            if self.squads[i].is_active():
                ids.append(self.squads[i].id_num)

        return ids

    def is_active(self):

        if self.active_squads():
            return True
        else:
            return False