from coins import *
from ticket_machine import *

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

if __name__ == '__main__':
    ticket_machine = TicketMachine(list(TICKETS_GEN))
    startup_storage = {(coin, 1) for coin in acceptable_coins()}
    ticket_machine.append_all(startup_storage)

    TicketMachineUI(
        ticket_machine,
        "Automat biletowy MPK"
    ).mainloop()
