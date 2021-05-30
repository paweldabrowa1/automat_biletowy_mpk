import unittest

from automat_biletowy_mpk import *
from automat_biletowy_mpk.coins import coins_holder
from automat_biletowy_mpk.ticket_machine import ticket_machine, ticket


class TestTicketMachineCase(unittest.TestCase):

    def setUp(self) -> None:
        self.t1 = ticket.Ticket("Ticket 1", "ULGOWY", 1.0)
        self.t2 = ticket.Ticket("Ticket 2", "ULGOWY", 2.0)
        self.t3 = ticket.Ticket("Ticket 3", "NORMALNY", 3.5)
        self.tm = ticket_machine.TicketMachine([self.t1, self.t2, self.t3])

        self.c001 = Coin(0.01)
        self.c01 = Coin(0.1)
        self.c05 = Coin(0.5)
        self.c1 = Coin(1.0)
        self.c2 = Coin(2.0)

    def test_1(self):
        self.tm.set_chosen_amount(self.t1, 1)
        self.tm.get_payment_holder().append(self.c001, 99)

        with self.assertRaises(ticket_machine.NotEnoughCoinToPayForTicketsException):
            self.tm.pay()

        startup_storage = {(coin, 10) for coin in acceptable_coins()}
        self.tm.append_all(startup_storage)

        self.tm.get_payment_holder().append(self.c001, 1)

        rest = self.tm.pay()
        self.assertEqual(len(rest), 0)
        self.assertEqual(self.tm.get_amount(self.c001), 110)
        self.assertEqual(self.tm.get_amount(self.c01), 10)

    def test_2(self):
        self.tm.set_chosen_amount(self.t2, 1)
        self.tm.get_payment_holder().append(self.c2, 100)

        with self.assertRaises(ticket_machine.NoCoinsToRefundException):
            self.tm.pay()

        startup_storage = {(coin, 10) for coin in acceptable_coins()}
        self.tm.append_all(startup_storage)

        # 198.01
        self.tm.get_payment_holder().append(self.c001, 1)

        rest = self.tm.pay()
        self.assertEqual(len(rest), 6)

        total = sum([a * key.value for key, a in rest])
        self.assertEqual(200.01 - 2, total)

        # 10 bazowo + 100 z placenia - 1 z wydania reszty
        self.assertEqual(self.tm.get_amount(self.c2), 109)
        self.assertEqual(self.tm.get_amount(self.c01), 10)

        # powinien byc pusty
        self.assertEqual(self.tm.get_payment_holder().sum_all_coins_value(), 0)

    def test_3(self):
        self.tm.set_chosen_amount(self.t2, 1)
        self.tm.get_payment_holder().append(self.c001, 2)
        self.tm.get_payment_holder().append(self.c1, 1)
        self.tm.get_payment_holder().append(self.c2, 1)

        with self.assertRaises(ticket_machine.NoCoinsToRefundException):
            self.tm.pay()

        self.tm.append(self.c2, 2)

        # automat ma 4 zł
        # portfel ma 3.02 zł

        # wyrzuocony blad w UI go sie lapie i wywala okienko
        with self.assertRaises(ticket_machine.NoCoinsToRefundException):
            self.tm.pay()

        # Nie pobralo nic z portfela
        # czyli tutaj zostana zwrocone wszystkie monety jak byly o takich samych nominalach
        self.assertEqual(self.tm.get_payment_holder().sum_all_coins_value(), 3.02)
        # Nie dodalo nic do automatu
        self.assertEqual(self.tm.sum_all_coins_value(), 4)

        # sprawdzenie nominalow
        ph = self.tm.get_payment_holder()
        self.assertEqual(ph.get_amount(self.c01), 0)  # jeden ktorego nie bylo dodanego
        self.assertEqual(ph.get_amount(self.c001), 2)
        self.assertEqual(ph.get_amount(self.c1), 1)
        self.assertEqual(ph.get_amount(self.c2), 1)

    def test_4(self):
        self.tm.set_chosen_amount(self.t1, 1)
        self.tm.get_payment_holder().append(self.c001, 100)
        self.tm.append(self.c1, 1)

        rest = self.tm.pay()
        self.assertEqual(len(rest), 0)

        # sprawdzenie jeszcze czy zwroci jedna monete 0.01 z 1.01
        self.tm.reset()
        self.tm.get_payment_holder().append(self.c001, 101)
        self.tm.append(self.c1, 1)

        with self.assertRaises(ticket_machine.NoCoinsToRefundException):
            self.tm.pay()

        self.tm.append(self.c001, 1)

        rest = self.tm.pay()
        self.assertEqual(len(rest), 1)
        self.assertEqual(rest[0][0], self.c001)
        self.assertEqual(rest[0][1], 1)

    def test_5(self):
        self.tm.set_chosen_amount(self.t3, 1)  # 1 * 3.5
        self.tm.set_chosen_amount(self.t2, 2)  # 2 * 2
        self.assertEqual(self.tm.sum_all_chosen_tickets_cost(), 7.5)

    def test_6(self):
        # dodanie biletu
        self.tm.set_chosen_amount(self.t1, 5)
        # dodanie monet
        self.tm.get_payment_holder().append(self.c1, 4)
        # dodanie bieltu
        self.tm.set_chosen_amount(self.t2, 1)
        # dodanie monet
        self.tm.get_payment_holder().append(self.c1, 3)

        rest = self.tm.pay()  # brak reszty bo wrzucone 7zł a dodano 5 biletów 1zł i jeden 2 zł
        self.assertEqual(len(rest), 0)
        self.assertEqual(self.tm.get_amount(self.c1), 7)

    def test_7(self):
        # tutaj jest rzucany blad i mozna go lapac i wyswietlic komunikat
        with self.assertRaises(coins_holder.WrongAppendAmountException) as context:
            self.tm.append(self.c1, -10)

if __name__ == '__main__':
    unittest.main()
