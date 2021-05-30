from automat_biletowy_mpk.coins import *


class WrongAppendAmountException(Exception):
    """Throw when user gives negative number at CoinsHolder.append"""
    pass


class WrongRemoveAmountException(Exception):
    """Throw when user gives positive number at CoinsHolder.remove"""
    pass


class CoinsHolder:
    """
    Some kind dictionary for managing Coins with some useful helpers.
    It's initialized with basic set of acceptable coins
    """
    def __init__(self):
        self.__coins = {}
        for coin in acceptable_coins():
            self.__coins[coin] = 0

    def __str__(self) -> str:
        s = ""
        for key, value in self.__coins.items():
            s += "%s: \t%d\n" % (key, value)
        return s

    def append(self, coin, amount):
        """Used to add certain amount of coins to holder. Can't be negative!"""
        if amount <= 0:
            raise WrongAppendAmountException()
        self.__coins[coin] = self.__coins[coin] + amount

    def remove(self, coin, amount):
        """Used to remove certain amount of coins to holder. Can't be positive"""
        if amount >= 0:
            raise WrongRemoveAmountException()
        self.__coins[coin] = self.__coins[coin] + amount

    def set(self, coin, amount):
        """Used to set amount of coins in holder. Minimum is 0."""
        if amount < 0:
            amount = 0
        self.__coins[coin] = amount

    def get_amount(self, coin):
        """Used to retrieve amount of coins in holder"""
        return self.__coins[coin]

    def get_coins_dict(self):
        """Returns dictionary of coins to their amount"""
        return self.__coins

    def sum_all_coins_value(self):
        """Returns total value of coins in holder"""
        total = 0
        for coin, amount in self.__coins.items():
            total += amount * coin.value
        return total

    def append_all(self, coin_dict):
        """Used to adding dictionary of coins and their amount to holder"""
        for coin, amount in coin_dict:
            self.append(coin, amount)

    def append_holder(self, holder):
        """Used to union holder coins amounts"""
        for coin, amount in holder.get_coins_dict().items():
            if amount == 0:
                continue
            self.append(coin, amount)

    def reset(self):
        """Sets every coin amount to 0."""
        for c in self.get_coins_dict():
            self.set(c, 0)
