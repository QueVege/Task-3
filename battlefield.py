import json
from random import Random
from config_data import seed, armies_config
from strategy import choose_squad
from army import Army

R = Random(seed)


class Battlefield:

    def __init__(self, log_type, file=None):
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

            att_army = R.choice(self.armies)
            def_army = R.choice([army
                                 for army in self.armies
                                 if army is not att_army])

            att_sq = R.choice(att_army.squads)
            def_sq = choose_squad(att_army.strategy, def_army)

            dp = att_sq.damage

            if att_sq.attack_success >= def_sq.attack_success and dp:

                self.battles_counter += 1
                battle_report = {"Battle": self.battles_counter}

                battle_report["Attacking"] = \
                    f"Squad #{att_sq.id} from army {att_army.id}. " \
                    f"Contains {len(att_sq.soldiers)} soldiers" \
                    f" and {len(att_sq.vehicles)} vehicles"

                battle_report["Defending"] = \
                    f"Squad #{def_sq.id} from army {def_army.id}. " \
                    f"Contains {len(def_sq.soldiers)} soldiers" \
                    f" and {len(def_sq.vehicles)} vehicles"

                def_sq.get_damage(dp)
                battle_report["Outcome"] = \
                    f"Defending squad get {dp:.2f} damage points"

                def_army.left_active_squads()

                att_sq.level_up()

                self.armies = [army
                               for army in self.armies
                               if army.is_active]
                battle_report["Losses"] = \
                    f"Army {def_army.id} is not active anymore"

                self.report["battles"].append(battle_report)

        self.report["conclusion"] = \
            f"It takes {self.battles_counter} battles. " \
            f"Winner: {self.armies[0].id}"

        self.to_print()

    def to_print(self):
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
