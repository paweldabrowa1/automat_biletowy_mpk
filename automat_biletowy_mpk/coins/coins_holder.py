from automat_biletowy_mpk.coins import *


class WrongAppendAmountException(Exception):
    pass


class WrongRemoveAmountException(Exception):
    pass


class CoinsHolder:
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
        if amount <= 0:
            raise WrongAppendAmountException()
        self.__coins[coin] = self.__coins[coin] + amount

    def remove(self, coin, amount):
        if amount >= 0:
            raise WrongRemoveAmountException()
        self.__coins[coin] = self.__coins[coin] + amount

    def set(self, coin, amount):
        self.__coins[coin] = amount

    def get_amount(self, coin):
        return self.__coins[coin]

    def get_coins_dict(self):
        return self.__coins

    def sum_all_coins_value(self):
        total = 0
        for coin, amount in self.__coins.items():
            total += amount * coin.value
        return total

    def append_all(self, coin_dict):
        for coin, amount in coin_dict:
            self.append(coin, amount)

    def append_holder(self, holder):
        for coin, amount in holder.get_coins_dict().items():
            if amount == 0:
                continue
            self.append(coin, amount)

    def reset(self):
        for c in self.get_coins_dict():
            self.set(c, 0)
