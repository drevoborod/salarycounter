#!/usr/bin/env python3

import re
import tkinter as tk


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Salary counter")
        self.resizable(width=0, height=0)
        tk.Frame(self, height=10).grid(row=0)
        mainframe = tk.Frame(self)
        mainframe.grid(row=1, padx=10)
        tk.Label(mainframe, text="Enter spent time \n(HH:MM):").grid(row=0, column=0)
        tk.Label(mainframe, text="Enter price of one hour:").grid(row=0, column=1)
        self.quantity = tk.Entry(mainframe, width=10)
        self.quantity.grid(row=1, column=0, pady=5)
        self.hourly_cost = tk.DoubleVar(mainframe)
        tk.Entry(mainframe, width=10, textvariable=self.hourly_cost).grid(row=1, column=1)
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
        self.quantity.focus()
        self.mainloop()

    def calculate(self):
        try:
            self.quantity.get()
        except tk.TclError:
            pass
        else:
            if re.compile("^[0-9]{1,6}:[0-5][0-9]$").match(self.quantity.get()):
                res = calculate(self.hourly_cost.get(), self.quantity.get())
                self.total_hours.set(res[0])
                self.total_price.set(res[1])


def calculate(hour_price, total_hours):
    full_time = total_hours.split(":")
    minutes = int(full_time[1])
    time_minutes = (minutes * 100 / 60) / 100
    time_decimal = ".".join((full_time[0], "{}".format(time_minutes).split(".")[1]))
    time_decimal_rounded = ".".join((str(int(full_time[0])), "{:.2f}".format(time_minutes).split(".")[1])).rstrip("0").rstrip(".")
    total = float(time_decimal) * hour_price
    return time_decimal_rounded, "{:.2f}".format(total)


if __name__ == "__main__":
    Main()
