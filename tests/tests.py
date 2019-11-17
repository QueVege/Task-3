import unittest
from mock import patch
from random import Random
from strategy import choose_squad
from config_data import seed
from units import Soldier, Vehicle
from squad import Squad
import army


class TestStrategy(unittest.TestCase):

    """Testing the squad choosing function

    according to the specified strategy

    """

    def setUp(self):
        """Initialization of Army object

        contains 2 squads with different strength values

        """
        self.army = army.Army(0, "random_squad")
        self.army.squads[0].get_damage(0.6)
        self.army.squads[1].get_damage(0.9)

    def test_weakest_squad(self):
        """Checking choosing squad with the lowest strength value"""

        sq = choose_squad("weakest_squad", self.army)
        self.assertIs(sq, self.army.squads[1])

    def test_strongest_squad(self):
        """Checking choosing squad with the highest strength value"""

        sq = choose_squad("strongest_squad", self.army)
        self.assertIs(sq, self.army.squads[0])


class TestClassArmy(unittest.TestCase):

    """Testing the Army class"""

    @patch("army.SQUADS_COUNT", 4)
    def test_init_army(self):
        """Checking initialization of Army object"""

        self.army = army.Army(0, "random_squad")
        self.assertEqual(len(self.army.squads), 4)
        for sq in self.army.squads:
            self.assertIsInstance(sq, Squad)


class TestClassSoldier(unittest.TestCase):

    """Testing the Soldier class"""

    def setUp(self):
        """Initialization of Soldier object"""

        self.sold = Soldier(0, 0)
        self.R = Random(seed)

    def test_attack_success(self):
        """Checking the attack success calculation"""

        self.sold.health = 0.7
        self.sold.experience = 50
        self.assertEqual(self.sold.attack_success, 0.5)

    def test_strength(self):
        """Checking the strength calculation"""

        self.sold.health = 0.7
        self.sold.experience = 10
        self.assertEqual(self.sold.strength, 0.9)

    def test_get_damage(self):
        """Checking the health calculation after getting damage

        damage is less than health

        """
        self.sold.health = 0.8
        self.sold.get_damage(0.32)
        self.assertEqual(self.sold.health, 0.48)

    def test_get_damage_out_of_limit(self):
        """Checking the health calculation after getting damage

        damage is more than health

        """
        self.sold.health = 0.2
        self.sold.get_damage(0.32)
        self.assertEqual(self.sold.health, 0)

    def test_damage(self):
        """Checking the damage calculation"""

        self.sold.experience = 27
        self.assertEqual(self.sold.damage, 0.32)

    def test_level_up(self):
        """Checking the experience incrementation"""

        self.sold.experience = 12
        self.sold.level_up()
        self.assertEqual(self.sold.experience, 13)

    def test_level_up_out_of_limit(self):
        """Checking the experience incrementation

        experience reached the max value

        """
        self.sold.experience = 50
        self.sold.level_up()
        self.assertEqual(self.sold.experience, 50)

    def test_is_active(self):
        """Checking the soldier's activity without any health"""

        self.sold.health = 0
        self.assertFalse(self.sold.is_active)


class TestClassVehicle(unittest.TestCase):

    """Testing the Vehicle class"""

    def setUp(self):
        """Initialization of Vehicle object"""

        self.veh = Vehicle(0, 0)
        self.R = Random(seed)

    def test_damage(self):
        """Checking the damage calculation"""

        for op in self.veh.operators:
            op.experience = 10
        self.assertEqual(self.veh.damage, 0.4)

    def test_strength(self):
        """Checking the strength calculation"""

        self.veh.health = 2.2
        for op in self.veh.operators:
            op.health = 0.5
            op.experience = 12
        self.assertEqual(self.veh.strength, 4.42)

    def test_get_damage(self):
        """Checking the health calculation after getting damage

        damage is less than vehicle's health and operator's health

        """
        self.veh.health = 2.2
        for op in self.veh.operators:
            op.health = 0.5
        self.veh.get_damage(0.5)
        self.assertEqual(self.veh.health, 1.9)
        self.assertEqual(self.veh.operators[0].health, 0.4)
        self.assertEqual(self.veh.operators[1].health, 0.45)
        self.assertEqual(self.veh.operators[2].health, 0.45)

    def test_get_damage_out_of_limit(self):
        """Checking the health calculation after getting damage

        damage is more than vehicle's health and operator's health

        """
        self.veh.health = 0.24
        for op in self.veh.operators:
            op.health = 0.1
        self.veh.get_damage(0.5)
        self.assertEqual(self.veh.health, 0)
        self.assertEqual(self.veh.operators[0].health, 0.05)
        self.assertEqual(self.veh.operators[1].health, 0.05)

    def test_is_active_without_ops(self):
        """Checking the vehicle's activity without any operator"""

        self.veh.health = 2
        self.veh.operators = []
        self.assertFalse(self.veh.is_active)

    def test_is_active_without_veh(self):
        """Checking the vehicle's activity if it's destroyed"""

        self.veh.health = 0
        for op in self.veh.operators:
            op.health = 0.7
        self.assertFalse(self.veh.is_active)


if __name__ == '__main__':
    unittest.main()
