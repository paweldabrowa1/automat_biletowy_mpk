import math

from automat_biletowy_mpk.coins import CoinsHolder


class NotEnoughCoinToPayForTicketsException(Exception):
    """Thrown when someone is trying pay for tickets and amount in payment holder is smaller than ticket cost"""
    pass


class NoCoinsToRefundException(Exception):
    """Thrown when TicketMachine cannot return giveback the change"""
    pass


class TicketMachine(CoinsHolder):
    def __init__(self, tickets):
        super().__init__()
        # self.__tickets = list(zip(tickets, [0 for _ in range(len(tickets))]))
        self.__tickets = {}
        for ticket in tickets:
            self.__tickets[ticket] = 0
        self.__payment_holder = PaymentCoinsHolder()

    def get_payment_holder(self):
        """Returns payment holder"""
        return self.__payment_holder

    def get_tickets(self):
        """Returns dictionary of tickets and their amounts"""
        return self.__tickets

    def set_chosen_amount(self, ticket, amount):
        """Sets certain amount of ticket"""
        self.__tickets[ticket] = amount

    def sum_all_chosen_tickets_amount(self):
        """Returns total amount of chosen tickets"""
        count = 0
        for ticket, amount in self.__tickets.items():
            count += amount
        return count

    def sum_all_chosen_tickets_cost(self):
        """Returns total cost of chossen tickets"""
        cost_total = 0
        for ticket, amount in self.__tickets.items():
            cost_total += amount * ticket.cost()
        return cost_total

    def pay(self):
        """Wrapper method for payment holder, used to payment for tickets"""
        return self.get_payment_holder()._pay(self)


class PaymentCoinsHolder(CoinsHolder):
    """Each ticket machine have payment holder (CoinsHolder) which is used to holds users coins entered to ticket
    machine """
    def _pay(self, refund_holder: TicketMachine):
        """Main payment holder method for checking giveback change possibility"""
        total = self.sum_all_coins_value()
        tickets_cost = refund_holder.sum_all_chosen_tickets_cost()
        rest = total - tickets_cost

        # print(total, tickets_cost, rest)

        if rest < 0:
            raise NotEnoughCoinToPayForTicketsException()

        return_coins = []

        if rest == 0:
            refund_holder.append_holder(self)
            self.reset()
            return return_coins

        for coin in reversed(self.get_coins_dict().keys()):
            amount = refund_holder.get_amount(coin)

            if amount != 0:
                back = int(rest / coin.value)
                if back != 0:
                    if back > amount:
                        back = amount

                    sub = back * coin.value
                    rest -= sub
                    rest = round(rest, 2)
                    return_coins.append((coin, int(back)))

            if rest == 0:
                break

        if rest != 0:
            raise NoCoinsToRefundException()

        refund_holder.append_holder(self)
        self.reset()

        # remove all return_coins
        for coin, amount in return_coins:
            refund_holder.remove(coin, amount * -1)

        return return_coins
