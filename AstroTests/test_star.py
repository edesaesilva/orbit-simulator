import unittest

from AstroLibrary.Star import Star


class StarTests(unittest.TestCase):

    def test_init(self):
        #test a sun like star
        star1 = Star(7e5, 2e30, 0, 0)
        self.assertEqual(star1.get_mass(), 2e30)
        self.assertEqual(star1.get_radius(), 7e5)
        self.assertEqual(star1.get_position(), (0,0))
        #test a very low density star
        star2a = Star(9e9, 2e30, 60, 60)
        self.assertEqual(star2a.get_mass(), 2e30)
        self.assertEqual(star2a.get_radius(), 1e8)
        self.assertEqual(star2a.get_position(), (60,60))
        star2b = Star(6e5, 2e22, 60, 60)
        self.assertEqual(star2b.get_mass(), 2e29)
        self.assertEqual(star2b.get_radius(), 6e5)
        self.assertEqual(star2b.get_position(), (60,60))
        #test a very high density star
        star3a = Star(6e5, 9e40, 500, 500)
        self.assertEqual(star3a.get_mass(), 3e32)
        self.assertEqual(star3a.get_radius(), 6e5)
        self.assertEqual(star3a.get_position(), (500, 500))
        star3b = Star(200, 6e30, 500, 500)
        self.assertEqual(star3b.get_mass(), 6e30)
        self.assertEqual(star3b.get_radius(), 1e5)
        self.assertEqual(star3b.get_position(), (500, 500))

    def test_set_position(self):
        star = Star(6e5, 6e30, 60, 60)
        self.assertEqual(star.get_position(), (60,60))
        star.set_position(40,70)
        self.assertEqual(star.get_position(), (40,70))


    def test_movement(self):
        star = Star(6e5, 6e30, 0, 0)
        star.move(0,0,6.1e30, 20000)