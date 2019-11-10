from config_data import SQUADS_COUNT
from squad import Squad


class Army:

    def __init__(self, id, chosen_strategy):
        self.id = id
        self.strategy = chosen_strategy
        self.squads = [Squad(i, self.id)
                       for i in range(SQUADS_COUNT)]

    @property
    def is_active(self):
        return len(self.squads) > 0

    def left_active_squads(self):
        self.squads = [sq
                       for sq in self.squads
                       if sq.is_active]
