import json
from random import Random, choice
from config_data import armies_config
from strategy import *
from army import Army


class Battlefield:

    def __init__(self, log_type, file = "log.json"):
        self.armies = [Army(army["id"], army["chosen_strategy"]) 
                       for army in armies_config]
        self.battles_counter = 0
        self.report = {
                        "introduction": "", 
                        "battles": [],
                        "conclusion": ""
                      }
        self.log_type = log_type
        self.file = file

    def start(self):
        self.report["introduction"] = \
        f"There are {len(self.armies)} armies in the battle: " + \
        f"{', '.join([army.id for army in self.armies])}"

        while len(self.armies) > 1:
             
            self.battles_counter += 1
            battle_report = {"battle_#": self.battles_counter}

            att_army = choice(self.armies)
            def_army = choice([army
                                    for army in self.armies
                                    if army is not att_army])

            att_sq = choice(att_army.squads)
            battle_report["Attacking"] = \
            f"Squad #{att_sq.id} from army {att_army.id}"

            def_sq = choose_squad(att_army.strategy, def_army)
            battle_report["Defending"] = \
            f"Squad #{def_sq.id} from army {def_army.id}"

            if not att_sq.attack_success < def_sq.attack_success:
                battle_report["Outcome"] = \
                "No damage is dealt to either side"

            else:
                dp = att_sq.damage

                def_sq.get_damage(dp)
                battle_report["Outcome"] = \
                f"Defending squad get {dp:.2f} damage points"

                att_sq.level_up()

                def_army.left_active_squads()

                if not def_army.is_active:
                    battle_report["Losses"] = \
                    f"Army {def_army.id} is not active anymore"

                self.armies = [army
                               for army in self.armies
                               if army.is_active]

            self.report["battles"].append(battle_report)

        self.report["conclusion"] = \
        f"It takes {self.battles_counter} battles." \
        f"Winner: {self.armies[0].id}"

        if self.log_type == 1:
            return self.console_log()
        elif self.log_type == 2:
            return self.file_log()

    def console_log(self):
        print(self.report["introduction"])
        for battle_report in self.report["battles"]:
            for p in battle_report:
                print(f"{p}: {battle_report[p]}")
            print("\n")
        print(self.report["conclusion"])

    def file_log(self):
        if not self.file:
            raise Exception("File for logging is not found.")
        with open(self.file, "w") as log_file:
            json.dump(self.report, log_file, indent=4)
        log_file.close()
