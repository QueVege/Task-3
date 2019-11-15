import unittest
from units import Soldier, Vehicle
from random import Random
from config_data import seed


class TestClassSoldier(unittest.TestCase):

    def setUp(self):
        self.sold = Soldier(0, 0)
        self.R = Random(seed)

    def test_attack_success(self):
        self.sold.health = 0.7
        self.sold.experience = 50
        self.assertEqual(self.sold.attack_success, 0.5)

    def test_strength(self):
        self.sold.health = 0.7
        self.sold.experience = 10
        self.assertEqual(self.sold.strength, 0.9)

    def test_get_damage(self):
        self.sold.health = 0.8
        self.sold.get_damage(0.32)
        self.assertEqual(self.sold.health, 0.48)

    def test_get_damage_out_of_limit(self):
        self.sold.health = 0.2
        self.sold.get_damage(0.32)
        self.assertEqual(self.sold.health, 0)

    def test_damage(self):
        self.sold.experience = 27
        self.assertEqual(self.sold.damage, 0.32)

    def test_level_up(self):
        self.sold.experience = 12
        self.sold.level_up()
        self.assertEqual(self.sold.experience, 13)

    def test_level_up_out_of_limit(self):
        self.sold.experience = 50
        self.sold.level_up()
        self.assertEqual(self.sold.experience, 50)

    def test_is_active(self):
        self.sold.health = 0
        self.assertFalse(self.sold.is_active)


class TestClassVehicle(unittest.TestCase):

    def setUp(self):
        self.veh = Vehicle(0, 0)
        self.R = Random(seed)

    def test_damage(self):
        for op in self.veh.operators:
            op.experience = 10
        self.assertEqual(self.veh.damage, 0.4)

    def test_strength(self):
        self.veh.health = 2.2
        for op in self.veh.operators:
            op.health = 0.5
            op.experience = 12
        self.assertEqual(self.veh.strength, 4.42)

    def test_get_damage(self):
        self.veh.health = 2.2
        for op in self.veh.operators:
            op.health = 0.5
        self.veh.get_damage(0.5)
        self.assertEqual(self.veh.health, 1.9)
        self.assertEqual(self.veh.operators[0].health, 0.4)
        self.assertEqual(self.veh.operators[1].health, 0.45)
        self.assertEqual(self.veh.operators[2].health, 0.45)

    def test_get_damage_out_of_limit(self):
        self.veh.health = 0.24
        for op in self.veh.operators:
            op.health = 0.1
        self.veh.get_damage(0.5)
        self.assertEqual(self.veh.health, 0)
        self.assertEqual(self.veh.operators[0].health, 0.05)
        self.assertEqual(self.veh.operators[1].health, 0.05)

    def test_is_active_without_ops(self):
        self.veh.health = 2
        self.veh.operators = []
        self.assertFalse(self.veh.is_active)

    def test_is_active_without_veh(self):
        self.veh.health = 0
        for op in self.veh.operators:
            op.health = 0.7
        self.assertFalse(self.veh.is_active)


if __name__ == '__main__':
    unittest.main()
