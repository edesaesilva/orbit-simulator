import unittest
import poliastro

from AstroLibrary.Planet import Planet


class PlanetTests(unittest.TestCase):

    def test_init(self):
        #test an earth like planet
        planet1 = Planet(6e3, 6e24, 0, 0)
        self.assertEqual(planet1.get_mass(), 6e24)
        self.assertEqual(planet1.get_radius(), 6e3)
        self.assertEqual(planet1.get_position(), (0,0))
        #test a very low density planet
        planet2a = Planet(1.5e5, 6e24, 60, 60)
        self.assertEqual(planet2a.get_mass(), 6e24)
        self.assertEqual(planet2a.get_radius(), 1e5)
        self.assertEqual(planet2a.get_position(), (60,60))
        planet2b = Planet(6e3, 2e22, 60, 60)
        self.assertEqual(planet2b.get_mass(), 1e23)
        self.assertEqual(planet2b.get_radius(), 6e3)
        self.assertEqual(planet2b.get_position(), (60,60))
        #test a very high density planet
        planet3a = Planet(6e3, 9e28, 500, 500)
        self.assertEqual(planet3a.get_mass(), 1e28)
        self.assertEqual(planet3a.get_radius(), 6e3)
        self.assertEqual(planet3a.get_position(), (500, 500))
        planet3b = Planet(200, 6e24, 500, 500)
        self.assertEqual(planet3b.get_mass(), 6e24)
        self.assertEqual(planet3b.get_radius(), 1e3)
        self.assertEqual(planet3b.get_position(), (500, 500))

    def test_set_position(self):
        planet = Planet(6e3, 6e24, 60, 60)
        self.assertEqual(planet.get_position(), (60,60))
        planet.set_position(40,70)
        self.assertEqual(planet.get_position(), (40,70))

    def test_movement(self):
        planet = Planet(6e3, 6e24, 1.5e8, 1)
        planet.move(0,0,2e30, 365*24*3600)
        print(planet.get_position())

