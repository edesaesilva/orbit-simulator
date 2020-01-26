import unittest
import json
from AstroLibrary.System import System


class SystemTests(unittest.TestCase):

    def test_init(self):
        system = System()
        self.assertEqual(len(system.get_planets()),0)
        self.assertEqual(len(system.get_stars()), 0)
        self.assertEqual(len(system.get_rocks()), 0)
        self.assertEqual(system.get_center_of_grav(), (0,0))
        self.assertEqual(system.get_mass(), 0)

    def test_add(self):
        system = System()
        system.add_star(7e5, 2e30, 0, 0)
        self.assertEqual(len(system.get_planets()), 0)
        self.assertEqual(len(system.get_stars()), 1)
        self.assertEqual(len(system.get_rocks()), 0)
        self.assertEqual(system.get_center_of_grav(), (0, 0))
        self.assertEqual(system.get_mass(), 2e30)

        system.add_planet(6e3, 6e24, 1e11, 1e11)
        self.assertEqual(len(system.get_planets()), 1)
        self.assertEqual(len(system.get_stars()), 1)
        self.assertEqual(len(system.get_rocks()), 0)
        self.assertAlmostEqual(system.get_mass()/1e30, (2e30+6e24)/1e30)

        system.add_rocks(2e11,2e11)
        self.assertEqual(len(system.get_planets()), 1)
        self.assertEqual(len(system.get_stars()), 1)
        self.assertEqual(len(system.get_rocks()), 1)
        self.assertAlmostEqual(system.get_mass()/1e30, (2e30+6e24)/1e30)

        system.add_planet(6e3, 6e24, 1e11, 1e11) #try to place a planet inside an existing one
        self.assertEqual(len(system.get_planets()), 1)
        self.assertEqual(len(system.get_stars()), 1)
        self.assertEqual(len(system.get_rocks()), 1)
        self.assertAlmostEqual(system.get_mass()/1e30, (2e30+6e24)/1e30)

        system.add_star(7e5, 2e30, 0, 0) #should also fail
        self.assertEqual(len(system.get_planets()), 1)
        self.assertEqual(len(system.get_stars()), 1)
        self.assertEqual(len(system.get_rocks()), 1)
        self.assertAlmostEqual(system.get_mass()/1e30, (2e30+6e24)/1e30)

        system.add_star(7e5, 2e30, 2e11, 0)
        system.add_star(7e5, 2e30, 0, 2e11)  #attempt to add a third star
        self.assertEqual(len(system.get_planets()), 1)
        self.assertEqual(len(system.get_stars()), 2)
        self.assertEqual(len(system.get_rocks()), 1)
        self.assertAlmostEqual(system.get_mass()/1e30, (2e30+6e24+2e30)/1e30)

    def test_simulation(self):
        system = System()
        system.add_star(7e5, 2e30, 0, 0)
        system.add_planet(6e3, 6e24, 1.5e8, 0)
        system.add_rocks(1.5e8,0)
        system.set_dt(31536000)
        for i in range(300):
            system.simulate_time()
        print(system.get_planets()[0].get_position())
        system.add_star(7e5, 2e30, -1.2e7,0)
        system.set_dt(315360000)
        for i in range(300):
            system.simulate_time()
        system.reset_space()
        system.add_planet(6e3, 6e24, 0, 0)
        system.add_rocks(0,6e4)
        system.set_dt(31536)
        for i in range(300):
            system.simulate_time()
        system.reset_space()
        system.add_star(7e5, 2e30, -1.2e7,0)
        system.add_star(7e5, 2e30, 1.2e7,0)
        system.set_dt(31536)
        for i in range(300):
            system.simulate_time()

    def test_read_json(self):
        system = System()
        json_file = open('test.json', 'r')
        data = json.load(json_file)
        json_file.close()
        system.from_json(data)
        self.assertEqual(len(system.get_planets()), 2)
        self.assertEqual(len(system.get_stars()), 1)
        self.assertEqual(len(system.get_rocks()), 5)
        self.assertAlmostEqual(system.get_mass()/1e30, (2e30+6e24+6.6e25)/1e30)

    def test_write_json(self):
        system = System()
        system.add_star(7e5, 2e30, 0, 0)
        system.add_planet(6e3, 6e24, 1.5e8, 1)
        system.add_rocks(1.5e8,0)
        system.to_json('test2.json')
        json_file = open('test2.json', 'r')
        data = json.load(json_file)
        json_file.close()
        system.from_json(data)
        self.assertEqual(len(system.get_planets()), 1)
        self.assertEqual(len(system.get_stars()), 1)
        self.assertEqual(len(system.get_rocks()), 1)
        self.assertAlmostEqual(system.get_mass() / 1e30, (2e30 + 6e24) / 1e30)

    def test_csv(self):
        system = System()
        system.add_star(7e5, 2e30, 0, 0)
        system.add_planet(6e3, 6e24, 1.5e8, 1)
        system.add_rocks(1.5e8, 0)
        system.to_csv('test.csv')
