import unittest

from AstroLibrary.Rock import Rock


class RockTests(unittest.TestCase):

    def test_init(self):
        rock = Rock(50,50)
        self.assertEqual(rock.get_position(), (50,50))

    def test_set_position(self):
        rock = Rock(0,0)
        self.assertEqual(rock.get_position(), (0,0))
        rock.set_position(40,30)
        self.assertEqual(rock.get_position(), (40,30))


    def test_movement(self):
        rock = Rock(6000, 6000)
        rock.move(0,0,6.1e30, 2000)