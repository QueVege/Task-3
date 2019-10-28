import random
from functions import chosen_squad
from classes import *

Empire = Army(0)
Rebels = Army(1)

print("Please choose a strategy:\n\nRandom\t\t1\nWeakest\t\t2\nStrongest\t3\n")
empire_strategy = int(input("Empire: "))
rebels_strategy = int(input("Rebels: "))

battles = 0

while Empire.is_active() and Rebels.is_active():

    battles += 1

    attaсking_army = random.choice([Empire, Rebels])

    if attaсking_army == Empire:
        attacked_army = Rebels
        strategy = empire_strategy
    else:
        attacked_army = Empire
        strategy = rebels_strategy

    attaсking_squad_id = random.choice(attaсking_army.active_squads())
    attaсking_squad = attaсking_army.squads[attaсking_squad_id]

    attacked_squad = chosen_squad(attacked_army, strategy)
    
    for i in attacked_army.active_squads():
        attacked_army.squads[i].recharge(False)
    for i in attaсking_army.active_squads():
        attaсking_army.squads[i].recharge(False)

    if attaсking_squad.attack_success() >= attacked_squad.attack_success():
        damage_points = attaсking_squad.damage()
        attacked_squad.get_damage(damage_points)
        attaсking_squad.level_up()
        attaсking_squad.recharge(True)

if Empire.is_active():
    print("\n*** Empire wins! ***\n")
else:
    print("\n*** Rebels win! ***\n")

print("It takes", battles, "battles")