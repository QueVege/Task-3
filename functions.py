import random

def chosen_squad(army, strategy_num):
    
    if strategy_num == 1:

        ran_id = random.choice(army.active_squads())
        target = army.squads[ran_id]

    elif strategy_num == 2:

        weakest_id = army.active_squads()[0]
        for i in army.active_squads():
            if army.squads[i].strength() < army.squads[weakest_id].strength():
                weakest_id = i
        target = army.squads[weakest_id]

    elif strategy_num == 3:

        strongest_id = army.active_squads()[0]
        for i in army.active_squads():
            if army.squads[i].strength() > army.squads[strongest_id].strength():
                strongest_id = i
        target = army.squads[strongest_id]

    return target