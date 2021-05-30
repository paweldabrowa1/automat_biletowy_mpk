def acceptable_coins():
    return (Coin(0.01 * 10 ** multiplier * coinsDeg) for multiplier in range(4) for coinsDeg in [1, 2, 5])


class Coin:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return "%s zł" % self.value

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, othr):
        return self.value == othr.value

    def __hash__(self):
        return hash(self.value)
