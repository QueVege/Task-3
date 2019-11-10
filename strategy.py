from random import Random, choice


STRATEGIES = {}


def strategy(name):
    def adding(s):
        STRATEGIES[name] = s
        return s
    return adding


@strategy('random_squad')
def random_squad(army):
    return choice(army.squads)


@strategy('weakest_squad')
def weakest_squad(army):
    return min(army.squads, key=lambda sq: sq.strength)


@strategy('strongest_squad')
def strongest_squad(army):
    return max(army.squads, key=lambda sq: sq.strength)


def choose_squad(strategy_name, army):
    return STRATEGIES[strategy_name](army)
