from tkinter import *
from tkinter.messagebox import *

from automat_biletowy_mpk import acceptable_coins
from automat_biletowy_mpk.ticket_machine import *

TICKET_SCALE = 1.4
TICKET_WIDTH = int(135 * TICKET_SCALE)
TICKET_HEIGHT = int(40 * TICKET_SCALE)
TICKET_COUNT_WIDTH = int(2 / 3 * TICKET_HEIGHT)
BORDER_SPACING = 20
TICKET_SPACING = 8

# COLOR_BACKGROUND = "#aecce2"
# COLOR_TICKET = "#08366d"
COLOR_BACKGROUND = "#dddddd"
COLOR_TICKET = "#7f0000"
COLOR_TICKET_BORDER = "#c09c9c"

FONT = "Courier"


class TicketMachineUI(Tk):
    def __init__(self, ticket_machine: TicketMachine, title: str):
        super().__init__()
        self.resizable(False, False)

        self.ticket_machine = ticket_machine

        self.title(title)
        self.configure(bg=COLOR_BACKGROUND)

        tickets = ticket_machine.get_tickets()
        tickets_len = len(tickets)

        tickets_frame_width = \
            BORDER_SPACING * 2 + TICKET_WIDTH + \
            TICKET_SPACING * 2 + \
            TICKET_HEIGHT + \
            TICKET_COUNT_WIDTH + \
            TICKET_HEIGHT
        tickets_frame_height = \
            BORDER_SPACING * 2 + \
            TICKET_HEIGHT * tickets_len + \
            TICKET_SPACING * (tickets_len - 1)
        # podsumowanie i przycisk od kupuje
        tickets_frame_height += TICKET_SPACING + TICKET_HEIGHT

        ct_frame = ChooseTicketsFrame(self, tickets, tickets_frame_width, tickets_frame_height, self)
        ct_frame.pack(
            side=TOP,
            anchor=NW
        )
        self.ct_frame = ct_frame

        payment_frame = PaymentFrame(self, tickets, tickets_frame_width, tickets_frame_height, self)
        payment_frame.pack(
            side=TOP,
            anchor=NW,
        )
        payment_frame.pack_forget()
        self.payment_frame = payment_frame
        self.payment_mode = False

        self.geometry("%dx%d" % (tickets_frame_width, tickets_frame_height))

    def switch_window(self):
        self.payment_mode = not self.payment_mode
        if self.payment_mode:
            self.payment_frame.pack()
            self.ct_frame.pack_forget()

            self.payment_frame.refresh_req_label()

            self.payment_frame.try_buy()
        else:
            self.payment_frame.pack_forget()
            self.ct_frame.pack()

            # self.payment_frame.reset()

    def report_callback_exception(self, exc, val, tb):
        n = exc.__name__
        # bo python slabo ogarnia trace w tkinterze
        if n == NoCoinsToRefundException.__name__:
            showwarning(
                title="UWAGA!",
                message="Tylko odliczona kwota"
            )
            self.payment_frame.reset()
            self.payment_frame.refresh_current_label()
            self.payment_frame.force_ref_coin_amm_labels()
            self.payment_frame.force_ref_coin_storage_amm_labels()

            self.switch_window()

            # TUTAJ NIE RESETUJE BILETOW!

        if n == NotEnoughCoinToPayForTicketsException.__name__:
            showerror(
                title="ERR X001",
                message="Ta sytuacja nie powinna wystapic, przez ifa u gory!"
            )


class PaymentFrame(Frame):
    def __init__(
            self, master,
            tickets, tickets_frame_width, tickets_frame_height,
            ticket_machine_ui: TicketMachineUI
    ):
        self.ticket_machine_ui = ticket_machine_ui

        super().__init__(
            master,
            width=tickets_frame_width,
            height=tickets_frame_height,
            bg=COLOR_BACKGROUND,
            # fill=BOTH
        )

        coins = acceptable_coins()

        btn_size = 12
        buy_button = Button(
            self,
            text="Zmień ilość biletów",
            command=self.buy_action
        )
        buy_button.config(font=(FONT, btn_size))
        buy_button.grid(row=0, column=0, columnspan=5, pady=20)

        sum_amount_title = Label(
            self,
            text="WRZUCONO:",
            bg=COLOR_BACKGROUND,
        )
        sum_amount_title.config(font=(FONT, 14, 'bold'))
        sum_amount_title.grid(row=3, column=5, rowspan=2, padx=10)
        sum_amount = Label(
            self,
            text="0.00 zł",
            bg=COLOR_BACKGROUND,
        )
        sum_amount.config(font=(FONT, 12))
        sum_amount.grid(row=4, column=5, rowspan=2, padx=10)
        self.sum_amount = sum_amount

        req_amount_title = Label(
            self,
            text="NA:",
            bg=COLOR_BACKGROUND,
        )
        req_amount_title.config(font=(FONT, 14, 'bold'))
        req_amount_title.grid(row=5, column=5, rowspan=2, padx=10)
        req_amount = Label(
            self,
            text="-",
            bg=COLOR_BACKGROUND,
        )
        req_amount.config(font=(FONT, 12))
        req_amount.grid(row=6, column=5, rowspan=2, padx=10)
        self.req_amount = req_amount

        iwm_title = Label(
            self,
            text="Ilosc wrzucanych\nmonet:",
            bg=COLOR_BACKGROUND,
        )
        iwm_title.config(font=(FONT, 8))
        iwm_title.grid(row=8, column=5, padx=10)

        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        iwm_input = Entry(self, validate='key', validatecommand=vcmd)
        iwm_input.insert(END, '1')
        iwm_input.config(font=(FONT, 8))
        iwm_input.grid(row=9, column=5, padx=10)
        self.iwm_input = iwm_input

        self.coins_storage_data_labels = {}
        self.coins_data_labels = {}

        for index, coin in enumerate(coins):
            title = Label(
                self,
                text=coin,
                bg=COLOR_BACKGROUND,
            )

            r = 2 + index

            title.grid(row=r, column=0, pady=5)

            count_storage = Label(
                self,
                text="< %d >" % self.ticket_machine_ui.ticket_machine.get_amount(coin),
                width=5,
                bg=COLOR_BACKGROUND,
            )
            count_storage.grid(row=r, column=1)

            count = Label(
                self,
                text="0",
                width=5,
                bg=COLOR_BACKGROUND,
            )
            count.grid(row=r, column=3)

            decrease = Button(
                self,
                text="-",
                command=lambda c=coin: self.add_coin(c, -1)
            )
            decrease.grid(row=r, column=2)

            append = Button(
                self,
                text="+",
                command=lambda c=coin: self.add_coin(c, 1)
            )
            append.grid(row=r, column=4)

            self.coins_storage_data_labels[coin] = count_storage
            self.coins_data_labels[coin] = count
            self.last_sum = 0

    def reset(self):
        self.ticket_machine_ui.ticket_machine.get_payment_holder().reset()

        for coin, label in self.coins_data_labels.items():
            label['text'] = 0
        self.refresh_current_label()

    def add_coin(self, coin, multiplier):
        ph = self.ticket_machine_ui.ticket_machine.get_payment_holder()
        label = self.coins_data_labels[coin]

        app = int(self.iwm_input.get())

        if app < 1:
            app = 1

        app *= multiplier

        a = ph.get_amount(coin)
        a += app
        if a < 0:
            a = 0
        elif a > 999:
            a = 999
        ph.set(coin, a)
        label['text'] = a

        self.try_buy()

    def force_ref_coin_storage_amm_labels(self):
        for coin, label in self.coins_storage_data_labels.items():
            label['text'] = "< " + \
                            str(self.ticket_machine_ui.ticket_machine.get_amount(coin)) + " >"

    def force_ref_coin_amm_labels(self):
        for coin, label in self.coins_data_labels.items():
            label['text'] = self.ticket_machine_ui.ticket_machine \
                .get_payment_holder().get_amount(coin)

    def buy_action(self):
        self.ticket_machine_ui.switch_window()

    def refresh_current_label(self):
        self.last_sum = self.ticket_machine_ui.ticket_machine.get_payment_holder().sum_all_coins_value()
        self.sum_amount['text'] = "{:.2f} zł".format(self.last_sum)

    def refresh_req_label(self):
        self.req_amount['text'] = "{:.2f} zł" \
            .format(self.ticket_machine_ui.ticket_machine.sum_all_chosen_tickets_cost())

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def try_buy(self):
        self.refresh_current_label()
        ticket_cost = self.ticket_machine_ui.ticket_machine.sum_all_chosen_tickets_cost()

        if self.last_sum < ticket_cost:
            return

        rest = self.ticket_machine_ui.ticket_machine.pay()

        msg = "Reszta "

        if len(rest) == 0:
            msg += ": Nie ma"
        else:
            msg += "(" + str(self.last_sum - ticket_cost) + " zł):"
            for coin, a in rest:
                msg += "\n - " + str(a) + "x " + str(coin) + " (" + str(a * coin.value) + " zł)"

        showinfo(
            title="Wszystko OK, drukuje bilety...",
            message=msg
        )
        self.refresh_current_label()
        self.force_ref_coin_amm_labels()
        self.force_ref_coin_storage_amm_labels()

        self.ticket_machine_ui.switch_window()

        self.ticket_machine_ui.ct_frame.reset_tickets()

class ChooseTicketsFrame(Frame):
    def __init__(
            self, master,
            tickets, tickets_frame_width, tickets_frame_height,
            ticket_machine_ui: TicketMachineUI
    ):
        self.ticket_machine_ui = ticket_machine_ui
        tickets_len = len(tickets)

        super().__init__(
            master,
            width=tickets_frame_width,
            height=tickets_frame_height,
            bg=COLOR_BACKGROUND,
        )

        self.tickets_frames = {}

        for index, ticket in enumerate(tickets.keys()):
            ticket_frame = ChooseTicketFrame(self, ticket, self.change_event)
            ticket_frame.place(
                x=BORDER_SPACING,
                y=BORDER_SPACING + index * (TICKET_HEIGHT + TICKET_SPACING)
            )
            self.tickets_frames[ticket] = ticket_frame

        sum_frame = Frame(
            master=self,
            width=TICKET_WIDTH,
            height=TICKET_HEIGHT,
            bg=COLOR_TICKET_BORDER,
        )
        sum_frame.place(
            x=BORDER_SPACING,
            y=BORDER_SPACING + tickets_len * (TICKET_HEIGHT + TICKET_SPACING)
        )

        c_size = 10
        t_size = 7
        price_size = 16

        c_label = Label(
            sum_frame,
            width=23,
            text="-",
            bg=COLOR_TICKET_BORDER
        )
        c_label.config(font=(FONT, c_size))
        c_label.place(x=0, y=0)
        self.c_label = c_label

        price_label = Label(
            sum_frame,
            width=14,
            text="",
            bg=COLOR_TICKET_BORDER
        )
        price_label.config(font=(FONT, price_size))
        price_label.place(x=0, y=c_size + t_size + 10)
        self.price_label = price_label

        t_label = Label(
            sum_frame,
            width=37,
            text="DO ZAPŁATY:",
            bg=COLOR_TICKET_BORDER
        )
        t_label.config(font=(FONT, t_size))
        t_label.place(x=0, y=c_size + 5)

        self.refresh_label_count()
        self.refresh_label_cost()

        btn_size = 20
        buy_button = Button(
            self,
            text="KUPUJĘ",
            command=self.buy_action
        )
        buy_button.config(font=(FONT, btn_size))
        buy_button.place(
            x=BORDER_SPACING + TICKET_WIDTH + TICKET_SPACING + 15,
            y=BORDER_SPACING + tickets_len * (TICKET_HEIGHT + TICKET_SPACING) + 2
        )

    def change_event(self, ticket, current_amount):
        # print(ticket, current_amount)
        self.ticket_machine_ui.ticket_machine.set_chosen_amount(ticket, current_amount)
        # print(self.ticket_machine_ui.ticket_machine.get_tickets())
        self.refresh_label_count()
        self.refresh_label_cost()

    def refresh_label_count(self):
        self.c_label['text'] = "LICZBA BILETÓW: %d" % \
                               self.ticket_machine_ui.ticket_machine.sum_all_chosen_tickets_amount()

    def refresh_label_cost(self):
        self.price_label['text'] = "{:.2f} zł" \
            .format(self.ticket_machine_ui.ticket_machine.sum_all_chosen_tickets_cost())

    def buy_action(self):
        ticket_count = self.ticket_machine_ui.ticket_machine.sum_all_chosen_tickets_amount()

        if ticket_count == 0:
            showwarning(
                title="UWAGA!",
                message="Aby przejsc do kupna musisz wybrac\n"
                        "conajmniej jeden bilet!"
            )
            return

        self.ticket_machine_ui.switch_window()

    def reset_tickets(self):
        for ticket in self.ticket_machine_ui.ticket_machine.get_tickets():
            self.ticket_machine_ui.ticket_machine.set_chosen_amount(ticket, 0)
            tf = self.tickets_frames[ticket]
            tf.count = 0
            tf.count_label['text'] = 0

        self.refresh_label_count()
        self.refresh_label_cost()


class ChooseTicketFrame(Frame):
    def __init__(self, master, ticket: Ticket, change_event):
        self.ticket = ticket
        self.change_event = change_event
        width = TICKET_WIDTH + TICKET_SPACING * 2 + \
                TICKET_HEIGHT + \
                TICKET_COUNT_WIDTH + \
                TICKET_HEIGHT
        height = TICKET_HEIGHT

        super().__init__(
            master,
            width=width,
            height=height,
            bg=COLOR_BACKGROUND,
        )

        TicketImageBox(self, ticket).place(x=0, y=0)

        btn_size = 20
        count_size = 20

        self.count = 0
        count_label = Label(
            self,
            text=self.count,
            width=2,
            bg=COLOR_BACKGROUND
        )
        count_label.config(font=(FONT, count_size))
        count_label.place(x=TICKET_WIDTH + TICKET_HEIGHT + TICKET_SPACING + 3, y=10)
        self.count_label = count_label

        decrease_button = Button(
            self,
            width=3,
            height=1,
            text="-",
            command=self.decrease
        )
        decrease_button.config(font=(FONT, btn_size))
        decrease_button.place(x=TICKET_WIDTH + TICKET_SPACING, y=2)

        append_button = Button(
            self,
            width=3,
            height=1,
            text="+",
            command=self.append
        )
        append_button.config(font=(FONT, btn_size))
        append_button.place(x=TICKET_WIDTH + TICKET_HEIGHT + TICKET_SPACING + 40, y=2)

    def decrease(self):
        self.count -= 1
        if self.count < 0:
            self.count = 0
            return
        self.count_label['text'] = self.count
        self.change_event(self.ticket, self.count)

    def append(self):
        self.count += 1
        if self.count > 99:
            self.count = 99
            return
        self.count_label['text'] = self.count
        self.change_event(self.ticket, self.count)


class TicketImageBox(Frame):
    def __init__(self, master, ticket: Ticket):
        width = TICKET_WIDTH
        height = TICKET_HEIGHT

        super().__init__(
            master,
            width=width,
            height=height,
            bg=COLOR_TICKET,
            highlightbackground=COLOR_TICKET_BORDER,
            highlightthickness=1
        )

        n_size = 10
        t_size = 8
        price_size = 12

        n_label = Label(
            self,
            text=ticket.name(),
            fg="white",
            bg=COLOR_TICKET
        )
        n_label.config(font=(FONT, n_size))
        n_label.place(x=0, y=0)

        t_label = Label(
            self,
            text=ticket.type(),
            fg="white",
            bg=COLOR_TICKET
        )
        t_label.config(font=(FONT, t_size))
        t_label.place(x=4, y=n_size + 8)

        price_label = Label(
            self,
            text="{:.2f}zł".format(ticket.cost()),
            fg="white",
            bg=COLOR_TICKET
        )
        price_label.config(font=(FONT, price_size, 'bold'))
        price_label.place(x=TICKET_WIDTH - 70, y=TICKET_HEIGHT - price_size * 2 - 4)
