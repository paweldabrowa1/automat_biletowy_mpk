class Ticket:
    def __init__(self, name, type, cost):
        self.__name = name
        self.__type = type
        self.__cost = cost

    def __str__(self) -> str:
        return "%s [%s] (%s zł)" % (self.__name, self.__type, self.__cost)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, othr):
        return (self.__name, self.__type) == (othr.__name, othr.__type)

    def __hash__(self):
        return hash((self.__name, self.__type))

    def name(self):
        return self.__name

    def type(self):
        return self.__type

    def cost(self):
        return self.__cost
