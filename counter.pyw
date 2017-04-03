#!/usr/bin/env python3

import re
import tkinter as tk


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.previous_price = DEFAULT_PRICE
        self.wrong_entry = False
        self.title("Salary counter")
        self.resizable(width=0, height=0)
        tk.Frame(self, height=10).grid(row=0)
        mainframe = tk.Frame(self)
        mainframe.grid(row=1, padx=10)
        tk.Label(mainframe, text="Enter spent time \n(HH:MM):").grid(row=0, column=0)
        tk.Label(mainframe, text="Enter price of one hour:").grid(row=0, column=1)
        self.quantity = tk.Entry(mainframe, width=10)
        self.quantity.grid(row=1, column=0, pady=5)
        self.hourly_cost = tk.DoubleVar(mainframe, value=DEFAULT_PRICE)
        self.hourly_cost_entry = tk.Entry(mainframe, width=10, textvariable=self.hourly_cost)
        self.hourly_cost_entry.grid(row=1, column=1)
        tk.Frame(mainframe, height=5).grid(row=2)
        tk.Label(mainframe, text="Total hours in decimal:").grid(row=3, column=0)
        tk.Label(mainframe, text="Total price:").grid(row=3, column=1)
        self.total_hours = tk.StringVar(mainframe)
        tk.Label(mainframe, relief="sunken", width=10, textvariable=self.total_hours).grid(row=4, column=0, pady=5)
        self.total_price = tk.StringVar(mainframe)
        tk.Label(mainframe, relief="sunken", width=10, textvariable=self.total_price).grid(row=4, column=1)
        tk.Frame(self, height=20).grid(row=2)
        tk.Button(self, text="Calculate", command=self.calculate).grid(row=3, pady=10)
        self.bind("<Return>", lambda e: self.calculate())
        self.bind("<Escape>", lambda e: self.quit())
        self.bind("<Control-c>", lambda e: self.copy())
        self.hourly_cost_entry.bind("<FocusIn>", lambda e: self.get_price())
        self.hourly_cost_entry.bind("<FocusOut>", lambda e: self.fill_price())
        self.quantity.bind("<FocusIn>", lambda e: self.clear_hours())
        self.quantity.bind("<Key>", lambda e: self.clear_hours())
        self.quantity.focus()
        self.mainloop()

    def calculate(self):
        try:
            hours = self.quantity.get()
        except tk.TclError:
            self.display_error()
        else:
            try:
                cost = self.hourly_cost.get()
            except tk.TclError:
                cost = self.previous_price
            else:
                self.previous_price = cost
            if re.compile("^[0-9]{1,6}:[0-5][0-9]{0,1}$").match(hours):
                match = True
            elif re.compile("^[0-9]{1,6}$").match(hours):
                hours += ":00"
                match = True
            else:
                match = False
            if match:
                self.wrong_entry = False
                res = calculate(cost, hours)
                self.total_hours.set(res[0])
                self.total_price.set(res[1])
            else:
                self.display_error()

    def display_error(self):
        self.quantity.delete(0, "end")
        self.quantity.insert(0, "Error")
        self.wrong_entry = True

    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.total_price.get())

    def get_price(self):
        self.previous_price = self.hourly_cost_entry.get()
        self.hourly_cost_entry.delete(0, "end")

    def fill_price(self):
        try:
            self.hourly_cost.get()
        except tk.TclError:
            self.hourly_cost.set(self.previous_price)

    def clear_hours(self):
        if self.wrong_entry:
            self.quantity.delete(0, "end")
            self.wrong_entry = False


def calculate(hour_price, total_hours):
    full_time = total_hours.split(":")
    minutes = int(full_time[1])
    time_minutes = (minutes * 100 / 60) / 100
    time_decimal = ".".join((full_time[0], "{}".format(time_minutes).split(".")[1]))
    time_decimal_rounded = ".".join((str(int(full_time[0])), "{:.2f}".format(time_minutes).split(".")[1])).rstrip("0").rstrip(".")
    total = float(time_decimal) * float(hour_price)
    return time_decimal_rounded, "{:.2f}".format(total)


DEFAULT_PRICE = 0.0
if __name__ == "__main__":
    Main()
