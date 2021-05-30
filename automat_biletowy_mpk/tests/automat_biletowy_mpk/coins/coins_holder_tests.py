import unittest

from automat_biletowy_mpk.coins import coins
from automat_biletowy_mpk.coins import coins_holder


class TestCoinsHolderCase(unittest.TestCase):
    def test_basic_setup(self):
        ch = coins_holder.CoinsHolder()
        self.assertEqual(len(ch.get_coins_dict()), 12)

        c = coins.Coin(1.0)
        c2 = coins.Coin(2.0)

        self.assertEqual(ch.get_amount(c), 0)

        ch.append(c, 10)

        self.assertEqual(ch.get_amount(c), 10)

        with self.assertRaises(coins_holder.WrongAppendAmountException) as context:
            ch.append(c, -10)

        with self.assertRaises(coins_holder.WrongRemoveAmountException) as context:
            ch.remove(c, 10)

        ch.remove(c, -1)

        ch.append(c2, 2)

        self.assertEqual(9 + 2 * 2, ch.sum_all_coins_value())

if __name__ == '__main__':
    unittest.main()
