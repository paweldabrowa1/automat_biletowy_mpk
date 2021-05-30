from .coins import *
from .ticket_machine import *

TICKETS_GEN = [
    Ticket(
        "%d-minutowy" % _time,
        _type,
        _cost / (index + 1)
    )
    for index, _type in enumerate(["NORMALNY", "ULGOWY"])
    for _time, _cost in {
        20: 4.00,
        40: 6.00,
        60: 7.00
    }.items()
]


class Runner:
    """Main Automat Biletowy MPK running class"""
    def start_app(self):
        ticket_machine = TicketMachine(list(TICKETS_GEN))

        startup_storage = lambda amount: {(coin, amount) for coin in acceptable_coins()}

        ticket_machine.append_all(startup_storage(1))

        TicketMachineUI(
            ticket_machine,
            "Automat biletowy MPK"
        ).mainloop()
