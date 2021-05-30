import unittest

from automat_biletowy_mpk import *


class TestTicketMachineCase(unittest.TestCase):
    def test_coin_equality(self):
        c1 = coins.Coin(1.0)
        c2 = coins.Coin(1.0)
        c3 = coins.Coin(1.1)

        self.assertNotEqual(c1, c3)
        self.assertEqual(c1, c1)
        self.assertEqual(c1, c2)

    def test_coin_generator(self):
        gen = acceptable_coins()
        self.assertEqual(len(list(gen)), 12)


if __name__ == '__main__':
    unittest.main()
